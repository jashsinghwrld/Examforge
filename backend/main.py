"""
RGPV Engineering Physics AI Backend
=====================================
FastAPI backend powered by Google Gemini API.
Uses 5-module dataset as context for all responses.

Features:
- Query answering
- Topic explanation
- Exam answer generation
- Topic search
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
from dotenv import load_dotenv

# Load .env file at startup (reliable regardless of current working directory)
_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

from core.dataset_loader import DatasetLoader
from routes.ask import router as ask_router
from routes.explain import router as explain_router
from routes.exam_answer import router as exam_router
from routes.search import router as search_router
from routes.topics import router as topics_router
from routes.topic_explanation import router as topic_explanation_router


# ── Lifespan: load dataset once at startup ──────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading RGPV Engineering Physics dataset...")
    app.state.dataset = DatasetLoader.load_all()
    print(f"Dataset loaded: {len(app.state.dataset)} entries across all modules.")
    yield
    print("Shutting down Physics API...")


# ── App Initialization ───────────────────────────────────────────────────────
app = FastAPI(
    title="RGPV Engineering Physics AI API",
    description=(
        "AI-powered backend for Engineering Physics (B.Tech Semester 1). "
        "Supports query answering, topic explanation, exam answer generation, "
        "and topic search — powered by Google Gemini API and a structured "
        "5-module dataset."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS Middleware ──────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register Routers ─────────────────────────────────────────────────────────
app.include_router(ask_router,      prefix="/ask",         tags=["Query Answering"])
app.include_router(explain_router,  prefix="/explain",     tags=["Topic Explanation"])
app.include_router(topic_explanation_router, prefix="/topic-explanation", tags=["Topic Explanation"])
app.include_router(exam_router,     prefix="/exam-answer", tags=["Exam Answer Generator"])
app.include_router(search_router,   prefix="/search",      tags=["Topic Search"])
app.include_router(topics_router,   prefix="/topics",      tags=["Topic Listing"])


# ── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "message": "RGPV Engineering Physics API is running.",
        "version": "1.0.0",
    }


# ── Root ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the RGPV Engineering Physics AI API.",
        "docs": "/docs",
        "endpoints": {
            "ask":         "POST /ask          — Answer any physics query",
            "explain":     "POST /explain      — Get full topic explanation",
            "topic_explanation": "POST /topic-explanation — Exam-format topic explanation",
            "exam_answer": "POST /exam-answer  — Generate structured 7-mark answer",
            "search":      "POST /search       — Search topics in dataset",
            "topics":      "GET  /topics       — List all available topics",
            "health":      "GET  /health       — API health check",
        },
    }
