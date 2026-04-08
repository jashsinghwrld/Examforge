"""
POST /search
============
Topic search endpoint.
Searches across all 5 modules and returns matching topics with summaries.
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field

from core.dataset_loader import DatasetLoader
from core.gemini_client import get_gemini_client
from core.prompt_builder import PromptBuilder


router = APIRouter()


# ── Request / Response Models ────────────────────────────────────────────────
class SearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=2,
        max_length=300,
        description="Search query to find matching topics.",
        example="interference",
    )
    module: str | None = Field(
        default=None,
        description="Optional: filter search to a specific module.",
        example="Module 2",
    )
    include_summary: bool = Field(
        default=True,
        description="Whether to include an AI-generated summary of results.",
    )


class TopicResult(BaseModel):
    unit: str
    topic: str
    question: str
    marks: int
    introduction: str
    exam_tip: str
    common_mistake: str


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: list[TopicResult]
    ai_summary: str | None
    used_fallback: bool = False
    fallback_reason: str | None = None


# ── Route ────────────────────────────────────────────────────────────────────
@router.post("", response_model=SearchResponse, summary="Search topics across modules")
async def search(request: Request, body: SearchRequest):
    """
    Search for topics across all 5 Engineering Physics modules.

    - Returns all matching dataset entries.
    - Optionally generates an AI summary of the search results.
    - Can be filtered by module.
    """
    dataset: list[dict] = request.app.state.dataset

    # Filter by module if specified
    if body.module:
        search_pool = DatasetLoader.get_by_module(dataset, body.module)
        if not search_pool:
            raise HTTPException(
                status_code=404,
                detail=f"No entries found for module: {body.module}",
            )
    else:
        search_pool = dataset

    # Search for matches
    matched_entries = DatasetLoader.search_by_topic(search_pool, body.query)

    if not matched_entries:
        return SearchResponse(
            query=body.query,
            total_results=0,
            results=[],
            ai_summary=f"No topics found matching '{body.query}'. Try a different search term.",
        )

    # Build result list
    results = []
    for entry in matched_entries:
        answer = entry.get("answer", {})
        results.append(
            TopicResult(
                unit=entry.get("unit", ""),
                topic=entry.get("topic", ""),
                question=entry.get("question", ""),
                marks=entry.get("marks", 7),
                introduction=answer.get("introduction", "")[:300] + "..."
                if len(answer.get("introduction", "")) > 300
                else answer.get("introduction", ""),
                exam_tip=entry.get("exam_tip", ""),
                common_mistake=entry.get("common_mistake", ""),
            )
        )

    # Generate AI summary if requested
    ai_summary = None
    used_fallback = False
    fallback_reason: str | None = None
    if body.include_summary and matched_entries:
        prompt = PromptBuilder.build_search_prompt(body.query, matched_entries)
        client = get_gemini_client()
        try:
            ai_summary = client.generate(prompt, temperature=0.3)
        except HTTPException as he:
            detail_str = he.detail if isinstance(he.detail, str) else str(he.detail)
            if he.status_code in (429, 503):
                used_fallback = True
                fallback_reason = detail_str
                ai_summary = (
                    "NOTE: Using fallback mode (Gemini temporarily unavailable or rate-limited).\n"
                    f"Reason: {detail_str}\n\n"
                    "You can still use the topic list below. Try again later for an AI-generated summary."
                )
            else:
                raise

    return SearchResponse(
        query=body.query,
        total_results=len(results),
        results=results,
        ai_summary=ai_summary,
        used_fallback=used_fallback,
        fallback_reason=fallback_reason,
    )
