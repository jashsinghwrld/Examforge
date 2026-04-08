"""
POST /topic-explanation
======================
Generate an RGPV exam-format explanation for a given topic.
Format: Definition → Explanation → Derivation → Key Points.
"""

import time
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from core.dataset_loader import DatasetLoader
from core.gemini_client import get_gemini_client
from core.prompt_builder import PromptBuilder


router = APIRouter()

_CACHE: dict[tuple[str, str], dict] = {}
_CACHE_TTL_SEC = 6 * 60 * 60  # 6 hours


def _cache_key(topic: str, module: str | None) -> tuple[str, str]:
    return (topic.strip().lower(), (module or "").strip().lower())


def _get_cached(topic: str, module: str | None) -> str | None:
    key = _cache_key(topic, module)
    item = _CACHE.get(key)
    if not item:
        return None
    if (time.time() - item["ts"]) > _CACHE_TTL_SEC:
        _CACHE.pop(key, None)
        return None
    return item["text"]


def _set_cached(topic: str, module: str | None, text: str) -> None:
    key = _cache_key(topic, module)
    _CACHE[key] = {"text": text, "ts": time.time()}


def _should_fallback_from_gemini_error(status_code: int | None, detail: str) -> bool:
    """True when Gemini failed due to overload / quota / rate limits (many phrasings)."""
    if status_code in (429, 503):
        return True
    if status_code not in (None, 500):
        return False
    d = (detail or "").lower()
    return any(
        s in d
        for s in (
            "high demand",
            "unavailable",
            "overloaded",
            "try again later",
            "503",
            "rate limit",
            "quota",
            "resource exhausted",
            "resource_exhausted",
            "too many requests",
            "limit exceeded",
            "429",
        )
    )


def _fallback_exam_format(topic: str, entry: dict | None) -> str:
    """
    Build a minimal exam-format response without Gemini.
    Uses dataset fields when available; otherwise returns a generic scaffold.
    """
    if not entry:
        return (
            "> NOTE: Using fallback mode (Gemini temporarily unavailable or rate-limited).\n"
            "> Reason: The AI model could not be reached right now, so this response is generated from local dataset info only.\n\n"
            "## Definition\n"
            f"{topic}: Not available in dataset.\n\n"
            "## Explanation\n"
            "Gemini is temporarily unavailable and this topic was not found in the local dataset. "
            "Please try again shortly.\n\n"
            "## Derivation\n"
            "Not applicable for this topic.\n\n"
            "## Key Points\n"
            "- Try again after a short wait.\n"
            "- Reduce repeated requests to avoid rate limits.\n"
        )

    answer = entry.get("answer", {}) or {}
    intro = (answer.get("introduction") or "").strip()
    theory = (answer.get("theory") or "").strip()
    derivation = (answer.get("derivation") or "").strip()

    definition = intro.splitlines()[0].strip() if intro else f"{topic}."
    if len(definition) > 240:
        definition = definition[:240].rstrip() + "..."

    explanation_parts = []
    if theory:
        explanation_parts.append(theory)
    elif intro:
        explanation_parts.append(intro)
    else:
        explanation_parts.append("Refer to the dataset context for this topic.")

    if not derivation:
        derivation = "Not applicable for this topic."

    key_points = [
        f"- Module: {entry.get('unit', 'N/A')}",
        f"- Typical exam question: {entry.get('question', 'N/A')}",
        "- Write headings and key equations clearly.",
    ]
    if entry.get("exam_tip"):
        key_points.append(f"- Exam Tip: {entry.get('exam_tip')}")

    return (
        "> NOTE: Using fallback mode (Gemini temporarily unavailable or rate-limited).\n"
        "> Reason: The AI model could not be reached right now, so this response is generated from local dataset info only.\n\n"
        "## Definition\n"
        f"{definition}\n\n"
        "## Explanation\n"
        + "\n\n".join(explanation_parts)
        + "\n\n"
        "## Derivation\n"
        f"{derivation}\n\n"
        "## Key Points\n"
        + "\n".join(key_points)
        + "\n"
    )


class TopicExplanationRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Topic name to generate an exam-format explanation for.",
        example="Heisenberg's Uncertainty Principle",
    )
    module: str | None = Field(
        default=None,
        description="Optional: specify module to narrow context (e.g., 'Module 1').",
        example="Module 1",
    )


class TopicExplanationResponse(BaseModel):
    topic: str
    explanation: str
    matched_topic: str | None
    source_module: str | None
    used_fallback: bool = False
    fallback_reason: str | None = None


@router.post(
    "",
    response_model=TopicExplanationResponse,
    summary="Generate RGPV exam-format topic explanation",
)
async def topic_explanation(request: Request, body: TopicExplanationRequest):
    dataset: list[dict] = request.app.state.dataset

    cached = _get_cached(body.topic, body.module)
    if cached:
        return TopicExplanationResponse(
            topic=body.topic,
            explanation=cached,
            matched_topic=body.topic,
            source_module=body.module,
        )

    # Optionally narrow the context by module
    if body.module:
        search_pool = DatasetLoader.get_by_module(dataset, body.module)
        if not search_pool:
            raise HTTPException(
                status_code=404,
                detail=f"No entries found for module: {body.module}",
            )
    else:
        search_pool = dataset

    matched_entries = DatasetLoader.search_by_topic(search_pool, body.topic)

    if matched_entries:
        context = DatasetLoader.build_context(matched_entries, max_entries=2)
        best_match = matched_entries[0]
        matched_topic = best_match.get("topic")
        source_module = best_match.get("unit")
    else:
        context = DatasetLoader.build_full_context(dataset)
        matched_topic = None
        source_module = None

    prompt = PromptBuilder.build_topic_explanation_prompt(
        topic=body.topic,
        context=context,
    )

    client = get_gemini_client()
    used_fallback = False
    fallback_reason: str | None = None
    try:
        explanation = client.generate(prompt, temperature=0.3)
    except HTTPException as he:
        # FastAPI HTTPException from gemini_client — use fallback on quota/rate-style errors
        detail_str = he.detail if isinstance(he.detail, str) else str(he.detail)
        if _should_fallback_from_gemini_error(he.status_code, detail_str):
            best_entry = matched_entries[0] if matched_entries else None
            explanation = _fallback_exam_format(body.topic, best_entry)
            used_fallback = True
            fallback_reason = detail_str
        else:
            raise
    except Exception as e:
        # Non-HTTP errors from SDK — still try fallback if message looks like rate limit
        msg = str(e)
        if _should_fallback_from_gemini_error(None, msg):
            best_entry = matched_entries[0] if matched_entries else None
            explanation = _fallback_exam_format(body.topic, best_entry)
            used_fallback = True
            fallback_reason = msg
        else:
            raise

    # Mark fallback responses so repeat requests skip Gemini while cache is warm
    _set_cached(body.topic, body.module, explanation)

    return TopicExplanationResponse(
        topic=body.topic,
        explanation=explanation,
        matched_topic=matched_topic,
        source_module=source_module,
        used_fallback=used_fallback,
        fallback_reason=fallback_reason,
    )

