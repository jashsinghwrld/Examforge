"""
POST /ask
=========
General physics query answering endpoint.
Searches dataset for relevant context, then uses Gemini to answer.
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field

from core.dataset_loader import DatasetLoader
from core.gemini_client import get_gemini_client
from core.prompt_builder import PromptBuilder


router = APIRouter()


# ── Request / Response Models ────────────────────────────────────────────────
class AskRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="The physics question or topic to ask about.",
        example="What is the de Broglie wavelength of an electron?",
    )
    module: str | None = Field(
        default=None,
        description="Optional: filter to a specific module (e.g., 'Module 1').",
        example="Module 1",
    )


class AskResponse(BaseModel):
    query: str
    answer: str
    matched_topics: list[str]
    source_module: str | None
    context_used: bool


# ── Route ────────────────────────────────────────────────────────────────────
@router.post("", response_model=AskResponse, summary="Answer any physics query")
async def ask(request: Request, body: AskRequest):
    """
    Answer any Engineering Physics query using dataset context + Gemini AI.

    - Searches the dataset for relevant topics matching the query.
    - Passes matched entries as context to Gemini.
    - Returns a structured, exam-oriented answer.
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

    # Search for relevant entries
    matched_entries = DatasetLoader.search_by_topic(search_pool, body.query)
    context_used = bool(matched_entries)

    # Build prompt
    if matched_entries:
        context = DatasetLoader.build_context(matched_entries, max_entries=3)
        prompt = PromptBuilder.build_ask_prompt(body.query, context)
    else:
        available = DatasetLoader.build_full_context(dataset)
        prompt = PromptBuilder.build_no_context_prompt(body.query, available)

    # Generate answer
    client = get_gemini_client()
    answer = client.generate(prompt, temperature=0.3)

    # Extract matched topic names
    matched_topics = [e.get("topic", "") for e in matched_entries]
    source_module = matched_entries[0].get("unit") if matched_entries else None

    return AskResponse(
        query=body.query,
        answer=answer,
        matched_topics=matched_topics,
        source_module=source_module,
        context_used=context_used,
    )
