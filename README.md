# Examforge

Examforge is a data-driven, domain-specific web app that (in its current stage) covers **Engineering Physics** as per the **RGPV Bhopal** syllabus for Semester 1/2.

It uses curated, pre-defined datasets (module-wise) to understand what the user is asking, then uses **Gemini AI** to generate accurate, exam-oriented explanations and answers in an RGPV-friendly format.

## What it does

- **To-the-point explanations** for Engineering Physics topics
- **Exam-ready answer generation** (structured, 7-mark style)
- **Topic search** across the dataset
- **Topic listing** to explore what’s available

## Project structure

- `backend/`: FastAPI backend (Python)
  - `main.py`: API app entrypoint
  - `routes/`: endpoints (`/ask`, `/explain`, `/topic-explanation`, `/exam-answer`, `/search`, `/topics`)
  - `dataset/`: module-wise JSON datasets used as grounding/context
- `frontend/`: React + Vite frontend (JavaScript) with Tailwind
- `start.bat`: one-command local setup + run (Windows)
- `stop.bat`: stop local servers (Windows)

## Tech stack

- **Backend**: FastAPI, Uvicorn, python-dotenv, google-genai, Pydantic
- **Frontend**: React, Vite, TailwindCSS, React Router, lucide-react

## How I built it (my POV)

- I wanted an app that helps students become **exam-ready**, not just “understand concepts”.
- I prepared **module-wise datasets** from reliable sources so the app can stay aligned with the syllabus and the expected answer style.
- I built a **FastAPI backend** that loads the dataset once at startup and exposes simple endpoints for:
  - answering questions
  - explaining topics
  - generating structured exam answers
  - searching and listing topics
- I built a **React frontend** to provide a clean UI to interact with the backend.
- I added `start.bat` and `stop.bat` so anyone can run it locally without manual setup steps.

## Run locally (Windows)

### Prerequisites

- **Python 3.11+** (3.11 or 3.12 recommended)
- **Node.js (LTS recommended)**

### 1) Configure your Gemini key

The backend reads `GEMINI_API_KEY` from `backend/.env`.

- If `backend/.env` does not exist, `start.bat` will create it from `backend/.env.example`.
- Then open `backend/.env` and set:

```env
GEMINI_API_KEY=your_real_key_here
```

You can create a key from `aistudio.google.com/app/apikey`.

### 2) Start everything

From the repo root, double-click or run:

```bash
start.bat
```

This will:
- check Python + Node
- create a backend virtualenv at `backend/venv` (if missing)
- install backend deps from `backend/requirements.txt`
- install frontend deps in `frontend/node_modules` (if missing)
- start:
  - **Backend**: `http://localhost:8000`
  - **Frontend**: `http://localhost:5173`
  - **API Docs**: `http://localhost:8000/docs`

### 3) Stop servers

Run:

```bash
stop.bat
```

## Notes

- **Do not commit secrets**: real `.env` files are intentionally ignored by git.
- If ports are already in use:
  - backend uses **8000**
  - frontend uses **5173**

## Future upgrades (planned)

- diagrams in datasets
- preparation strategy generation (based on time left)
- PYQ analysis

