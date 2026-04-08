"""
Dataset Loader
==============
Loads all 5 module JSON files from the dataset directory.
Provides search and retrieval utilities used across all routes.
"""

import json
import os
from typing import Optional


DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset")

MODULE_FILES = [
    "module1_quantum_mechanics.json",
    "module2_wave_optics.json",
    "module3_solid_state_physics.json",
    "module4_lasers_optical_fiber.json",
    "module5_electrostatics_maxwell.json",
]


class DatasetLoader:
    """Loads and provides access to the full RGPV physics dataset."""

    @staticmethod
    def load_all() -> list[dict]:
        """Load all module JSON files and return as a flat list of entries."""
        all_entries = []
        for filename in MODULE_FILES:
            filepath = os.path.join(DATASET_DIR, filename)
            if not os.path.exists(filepath):
                print(f"WARNING: Dataset file not found: {filepath}")
                continue
            with open(filepath, "r", encoding="utf-8") as f:
                entries = json.load(f)
                all_entries.extend(entries)
        return all_entries

    @staticmethod
    def search_by_topic(dataset: list[dict], query: str) -> list[dict]:
        """
        Search dataset entries by topic, question, or unit.
        Returns all entries whose topic or question contains the query (case-insensitive).
        """
        query_lower = query.lower()
        results = []
        for entry in dataset:
            topic = entry.get("topic", "").lower()
            question = entry.get("question", "").lower()
            unit = entry.get("unit", "").lower()
            if (
                query_lower in topic
                or query_lower in question
                or query_lower in unit
            ):
                results.append(entry)
        return results

    @staticmethod
    def get_by_topic_exact(dataset: list[dict], topic: str) -> Optional[dict]:
        """Return the first entry matching the topic exactly (case-insensitive)."""
        topic_lower = topic.lower()
        for entry in dataset:
            if entry.get("topic", "").lower() == topic_lower:
                return entry
        return None

    @staticmethod
    def get_by_module(dataset: list[dict], module: str) -> list[dict]:
        """Return all entries from a specific module (e.g., 'Module 1')."""
        module_lower = module.lower()
        return [
            entry for entry in dataset
            if entry.get("unit", "").lower() == module_lower
        ]

    @staticmethod
    def get_all_topics(dataset: list[dict]) -> list[dict]:
        """Return a summary list of all topics with their module and question."""
        return [
            {
                "unit": entry.get("unit"),
                "topic": entry.get("topic"),
                "question": entry.get("question"),
                "marks": entry.get("marks"),
            }
            for entry in dataset
        ]

    @staticmethod
    def build_context(entries: list[dict], max_entries: int = 3) -> str:
        """
        Build a formatted context string from dataset entries.
        Used as context input to Gemini API.
        Limits to max_entries to avoid token overflow.
        """
        context_parts = []
        for entry in entries[:max_entries]:
            answer = entry.get("answer", {})
            part = f"""
--- DATASET ENTRY ---
Unit: {entry.get('unit')}
Topic: {entry.get('topic')}
Question: {entry.get('question')}

Introduction:
{answer.get('introduction', '')}

Theory:
{answer.get('theory', '')}

Derivation:
{answer.get('derivation', '')}

Conclusion:
{answer.get('conclusion', '')}

Exam Tip: {entry.get('exam_tip', '')}
Common Mistake: {entry.get('common_mistake', '')}
--- END ENTRY ---
"""
            context_parts.append(part)
        return "\n".join(context_parts)

    @staticmethod
    def build_full_context(dataset: list[dict]) -> str:
        """
        Build a compact summary of all topics for general queries.
        Used when no specific topic match is found.
        """
        lines = ["Available topics in RGPV Engineering Physics dataset:\n"]
        for entry in dataset:
            lines.append(
                f"- [{entry.get('unit')}] {entry.get('topic')}: {entry.get('question')}"
            )
        return "\n".join(lines)
