"""
POST /explain
=============
Full topic explanation generator.
Provides intuition-building, structured explanations for any physics topic.
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field

from core.dataset_loader import DatasetLoader
from core.gemini_client import get_gemini_client
from core.prompt_builder import PromptBuilder


router = APIRouter()


# ── Request / Response Models ────────────────────────────────────────────────
class ExplainRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="The physics topic to explain.",
        example="Heisenberg's Uncertainty Principle",
    )
    depth: str = Field(
        default="standard",
        description="Explanation depth: 'brief', 'standard', or 'detailed'.",
        example="standard",
    )


class ExplainResponse(BaseModel):
    topic: str
    explanation: str
    related_topics: list[str]
    dataset_entry_found: bool


# ── Route ────────────────────────────────────────────────────────────────────
@router.post("", response_model=ExplainResponse, summary="Get full topic explanation")
async def explain(request: Request, body: ExplainRequest):
    """
    Generate a complete explanation for any Engineering Physics topic.

    - Finds the closest matching dataset entry for rich context.
    - Generates an intuition-building explanation using Gemini.
    - Returns related topics from the same module.
    """
    dataset: list[dict] = request.app.state.dataset

    # Validate depth parameter
    valid_depths = {"brief", "standard", "detailed"}
    if body.depth not in valid_depths:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid depth '{body.depth}'. Choose from: {valid_depths}",
        )

    # Search for matching entries
    matched_entries = DatasetLoader.search_by_topic(dataset, body.topic)
    dataset_entry_found = bool(matched_entries)

    # Build context
    if matched_entries:
        context = DatasetLoader.build_context(matched_entries, max_entries=2)
    else:
        context = DatasetLoader.build_full_context(dataset)

    # Adjust prompt based on depth
    base_prompt = PromptBuilder.build_explain_prompt(body.topic, context)

    depth_instructions = {
        "brief": "\nKEEP THE EXPLANATION BRIEF — 150-200 words maximum. Focus on the core concept only.",
        "standard": "\nProvide a standard explanation — 300-500 words. Cover theory, equations, and significance.",
        "detailed": "\nProvide a DETAILED explanation — cover everything thoroughly. Include intuition, derivation hints, applications, and examples.",
    }
    prompt = base_prompt + depth_instructions[body.depth]

    # Generate explanation
    client = get_gemini_client()
    explanation = client.generate(prompt, temperature=0.4)

    # Find related topics from same module
    related_topics = []
    if matched_entries:
        source_module = matched_entries[0].get("unit")
        module_entries = DatasetLoader.get_by_module(dataset, source_module)
        related_topics = [
            e.get("topic", "")
            for e in module_entries
            if e.get("topic", "").lower() != body.topic.lower()
        ][:5]  # Limit to 5 related topics

    return ExplainResponse(
        topic=body.topic,
        explanation=explanation,
        related_topics=related_topics,
        dataset_entry_found=dataset_entry_found,
    )
