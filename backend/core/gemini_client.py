"""
Gemini API Client
=================
Updated to use the new google.genai package.
"""

import os
from pathlib import Path
from google import genai
from google.genai import types
from fastapi import HTTPException
from dotenv import load_dotenv

# Load .env file explicitly (reliable regardless of current working directory)
_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# System instruction for all Gemini calls
SYSTEM_INSTRUCTION = """
You are an expert Engineering Physics AI assistant specialized for RGPV B.Tech Semester 1 examinations.

Your role:
- Answer questions based on the provided dataset context.
- Generate structured, exam-ready answers.
- Be precise, clear, and academically accurate.
- Use proper physics notation and terminology.
- Always prioritize exam scoring in your responses.

Response Rules:
1. Always use the provided dataset context as your primary source.
2. If the exact topic is in the context, base your answer on it directly.
3. If the topic is not in the context, use your knowledge but stay within RGPV syllabus scope.
4. For 7-mark answers: use Introduction → Theory → Derivation → Conclusion format.
5. For explanations: be clear, structured, and intuition-building.
6. Always include key formulas in their standard form.
7. Never hallucinate facts or formulas.
8. End every exam answer with an Exam Tip and Common Mistake.
"""


class GeminiClient:
    """Client for interacting with Google Gemini API using the new google.genai SDK."""

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please set it in your .env file."
            )
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model  = GEMINI_MODEL

    def generate(self, prompt: str, temperature: float = 0.3) -> str:
        """
        Generate a response from Gemini.

        Args:
            prompt: Full prompt including context and user query.
            temperature: Controls creativity. Lower = more factual.

        Returns:
            Generated text response.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=temperature,
                    max_output_tokens=4096,
                ),
            )
            if not response.text:
                raise HTTPException(
                    status_code=500,
                    detail="Gemini returned an empty response. Please try again.",
                )
            return response.text.strip()

        except HTTPException:
            raise
        except Exception as e:
            error_msg = str(e)
            el = error_msg.lower()
            if "API_KEY" in error_msg.upper() or "authentication" in el or "permission denied" in el:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid or missing Gemini API key. Please check your GEMINI_API_KEY.",
                )
            # Model overload / temporary unavailability (often 503)
            if any(s in el for s in ("503", "unavailable", "high demand", "overloaded", "try again later")):
                raise HTTPException(
                    status_code=503,
                    detail="Gemini is temporarily unavailable due to high demand. Please try again shortly.",
                )
            # Google often uses wording other than "rate" / "quota"
            if any(
                s in el
                for s in (
                    "quota",
                    "rate",
                    "resource exhausted",
                    "resource_exhausted",
                    "too many requests",
                    "limit exceeded",
                    "capacity",
                )
            ) or "429" in error_msg:
                raise HTTPException(
                    status_code=429,
                    detail="Gemini API rate limit exceeded. Please wait and try again.",
                )
            raise HTTPException(
                status_code=500,
                detail=f"Gemini API error: {error_msg}",
            )


# ── Singleton instance ────────────────────────────────────────────────────────
_client_instance: GeminiClient | None = None


def get_gemini_client() -> GeminiClient:
    """Return singleton Gemini client instance."""
    global _client_instance
    if _client_instance is None:
        _client_instance = GeminiClient()
    return _client_instance
