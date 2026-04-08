"""
GET /topics
===========
Lists all available topics across all modules.
Supports filtering by module.
"""

from fastapi import APIRouter, Request, Query
from pydantic import BaseModel

from core.dataset_loader import DatasetLoader


router = APIRouter()


# ── Response Models ──────────────────────────────────────────────────────────
class TopicSummary(BaseModel):
    unit: str
    topic: str
    question: str
    marks: int


class TopicsResponse(BaseModel):
    total: int
    modules: dict[str, int]
    topics: list[TopicSummary]


class ModuleInfo(BaseModel):
    module: str
    total_topics: int
    topics: list[TopicSummary]


# ── Routes ────────────────────────────────────────────────────────────────────
@router.get("", response_model=TopicsResponse, summary="List all available topics")
async def get_all_topics(
    request: Request,
    module: str | None = Query(
        default=None,
        description="Filter by module name (e.g., 'Module 1')",
        example="Module 1",
    ),
):
    """
    Returns a list of all available topics in the Engineering Physics dataset.

    - Optionally filter by module.
    - Returns topic name, question, unit, and marks for each entry.
    """
    dataset: list[dict] = request.app.state.dataset

    # Filter by module if specified
    if module:
        filtered = DatasetLoader.get_by_module(dataset, module)
    else:
        filtered = dataset

    # Build topic list
    topics = [
        TopicSummary(
            unit=entry.get("unit", ""),
            topic=entry.get("topic", ""),
            question=entry.get("question", ""),
            marks=entry.get("marks", 7),
        )
        for entry in filtered
    ]

    # Count topics per module
    module_counts: dict[str, int] = {}
    for entry in filtered:
        unit = entry.get("unit", "Unknown")
        module_counts[unit] = module_counts.get(unit, 0) + 1

    return TopicsResponse(
        total=len(topics),
        modules=module_counts,
        topics=topics,
    )


@router.get(
    "/modules",
    summary="List all available modules",
)
async def get_modules(request: Request):
    """Returns a list of all modules with their topic counts."""
    dataset: list[dict] = request.app.state.dataset

    module_map: dict[str, list[str]] = {}
    for entry in dataset:
        unit = entry.get("unit", "Unknown")
        topic = entry.get("topic", "")
        if unit not in module_map:
            module_map[unit] = []
        module_map[unit].append(topic)

    return {
        "total_modules": len(module_map),
        "modules": [
            {
                "module": unit,
                "topic_count": len(topics),
                "topics": topics,
            }
            for unit, topics in sorted(module_map.items())
        ],
    }


@router.get(
    "/{module_name}",
    response_model=ModuleInfo,
    summary="Get all topics for a specific module",
)
async def get_topics_by_module(request: Request, module_name: str):
    """
    Returns all topics for a specific module.

    Example: GET /topics/Module%201
    """
    dataset: list[dict] = request.app.state.dataset

    filtered = DatasetLoader.get_by_module(dataset, module_name)

    if not filtered:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail=f"No topics found for module: '{module_name}'. "
                   f"Valid modules: Module 1, Module 2, Module 3, Module 4, Module 5",
        )

    topics = [
        TopicSummary(
            unit=entry.get("unit", ""),
            topic=entry.get("topic", ""),
            question=entry.get("question", ""),
            marks=entry.get("marks", 7),
        )
        for entry in filtered
    ]

    return ModuleInfo(
        module=module_name,
        total_topics=len(topics),
        topics=topics,
    )
