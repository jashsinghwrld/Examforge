"""
POST /exam-answer
=================
Structured exam answer generator.
Generates full RGPV-style answers optimized for maximum marks.
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field

from core.dataset_loader import DatasetLoader
from core.gemini_client import get_gemini_client
from core.prompt_builder import PromptBuilder


router = APIRouter()


# ── Request / Response Models ────────────────────────────────────────────────
class ExamAnswerRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="The exam question to answer.",
        example="Derive the time-independent Schrödinger equation.",
    )
    marks: int = Field(
        default=7,
        ge=2,
        le=10,
        description="Marks allocated to the question (2, 3, 5, or 7).",
        example=7,
    )
    module: str | None = Field(
        default=None,
        description="Optional: specify module to narrow context (e.g., 'Module 1').",
        example="Module 1",
    )


class ExamAnswerResponse(BaseModel):
    question: str
    marks: int
    answer: str
    matched_topic: str | None
    source_module: str | None
    exam_tip: str | None
    common_mistake: str | None


# ── Route ────────────────────────────────────────────────────────────────────
@router.post(
    "",
    response_model=ExamAnswerResponse,
    summary="Generate structured exam answer",
)
async def exam_answer(request: Request, body: ExamAnswerRequest):
    """
    Generate a complete, structured exam answer for any Engineering Physics question.

    - Finds the best matching dataset entry as context.
    - Uses Gemini to generate a full RGPV-style answer.
    - Format: Introduction → Theory → Derivation → Final Standard Form → Conclusion.
    - Includes Exam Tip and Common Mistake.
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

    # Search for best matching entry
    matched_entries = DatasetLoader.search_by_topic(search_pool, body.question)

    # Build context
    if matched_entries:
        context = DatasetLoader.build_context(matched_entries, max_entries=2)
        best_match = matched_entries[0]
        matched_topic = best_match.get("topic")
        source_module = best_match.get("unit")
        exam_tip = best_match.get("exam_tip")
        common_mistake = best_match.get("common_mistake")
    else:
        context = DatasetLoader.build_full_context(dataset)
        matched_topic = None
        source_module = None
        exam_tip = None
        common_mistake = None

    # Build exam answer prompt
    prompt = PromptBuilder.build_exam_answer_prompt(
        question=body.question,
        marks=body.marks,
        context=context,
    )

    # Generate answer
    client = get_gemini_client()
    answer = client.generate(prompt, temperature=0.2)

    return ExamAnswerResponse(
        question=body.question,
        marks=body.marks,
        answer=answer,
        matched_topic=matched_topic,
        source_module=source_module,
        exam_tip=exam_tip,
        common_mistake=common_mistake,
    )
