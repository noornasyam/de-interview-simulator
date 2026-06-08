"""Utilities for the v2 curated question bank.

The v2 bank is intentionally file-based so the app can use curated objective
questions when available and fall back to Gemini-generated questions elsewhere.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Iterable


V2_BANK_ROOT = Path(__file__).resolve().parents[1] / "data" / "question_bank" / "v2"

DOMAIN_ALIASES = {
    "sql": "sql",
    "python": "python",
    "gcp": "gcp_bigquery",
    "gcp / bigquery": "gcp_bigquery",
    "bigquery": "gcp_bigquery",
    "terraform": "terraform",
    "airflow": "airflow",
    "data modeling": "data_modeling",
    "data_modeling": "data_modeling",
}

DOMAIN_LABELS = {
    "sql": "SQL",
    "python": "Python",
    "gcp_bigquery": "GCP / BigQuery",
    "terraform": "Terraform",
    "airflow": "Airflow",
    "data_modeling": "Data Modeling",
}

LEVEL_ALIASES = {
    "beginner": "beginner",
    "junior": "junior_data_engineer",
    "junior data engineer": "junior_data_engineer",
    "mid": "mid_level_data_engineer",
    "mid-level data engineer": "mid_level_data_engineer",
    "mid level data engineer": "mid_level_data_engineer",
    "senior": "senior_data_engineer",
    "senior data engineer": "senior_data_engineer",
    "lead": "lead_data_engineer",
    "lead data engineer": "lead_data_engineer",
    "architect": "architect",
}

LEVEL_LABELS = {
    "beginner": "Beginner",
    "junior_data_engineer": "Junior Data Engineer",
    "mid_level_data_engineer": "Mid-Level Data Engineer",
    "senior_data_engineer": "Senior Data Engineer",
    "lead_data_engineer": "Lead Data Engineer",
    "architect": "Architect",
}

DIFFICULTY_ORDER = {
    "easy": 1,
    "foundation": 1,
    "fundamentals": 1,
    "medium": 2,
    "practical": 2,
    "scenario": 3,
    "hard": 4,
    "advanced": 4,
    "expert": 5,
}


def normalize_domain(domain: str) -> str:
    """Return the v2 folder slug for a user-facing domain label."""

    normalized = str(domain or "").strip().lower().replace("-", " ")
    normalized = " ".join(normalized.split())
    return DOMAIN_ALIASES.get(normalized, normalized.replace(" / ", "_").replace(" ", "_"))


def normalize_level(level: str) -> str:
    """Return the v2 filename slug for a user-facing level label."""

    normalized = str(level or "").strip().lower().replace("_", " ")
    normalized = " ".join(normalized.split())
    return LEVEL_ALIASES.get(normalized, normalized.replace("-", "_").replace(" ", "_"))


def get_available_v2_domains() -> list[str]:
    if not V2_BANK_ROOT.exists():
        return []

    domains = []
    for path in sorted(V2_BANK_ROOT.iterdir()):
        if path.is_dir():
            domains.append(DOMAIN_LABELS.get(path.name, path.name.replace("_", " ").title()))
    return domains


def get_available_v2_levels() -> list[str]:
    return list(LEVEL_LABELS.values())


def load_v2_questions(domain: str, level: str) -> list[dict]:
    """Load curated questions for a domain and level.

    Missing files, invalid JSON, or non-list payloads return an empty list so
    the caller can gracefully fall back to Gemini-generated questions.
    """

    domain_slug = normalize_domain(domain)
    level_slug = normalize_level(level)
    path = V2_BANK_ROOT / domain_slug / f"{level_slug}.json"
    if not path.exists():
        return []

    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    return [question for question in data if isinstance(question, dict)]


def select_session_questions(
    domain: str,
    level: str,
    count: int = 5,
    previous_ids: set | None = None,
) -> list[dict]:
    """Select non-duplicate questions, roughly increasing by complexity."""

    previous_ids = previous_ids or set()
    questions = [
        question
        for question in load_v2_questions(domain, level)
        if question.get("id") and question.get("id") not in previous_ids
    ]
    if not questions:
        return []

    by_rank: dict[int, list[dict]] = {}
    for question in questions:
        rank = _difficulty_rank(question.get("difficulty"))
        by_rank.setdefault(rank, []).append(question)

    selected: list[dict] = []
    for rank in sorted(by_rank):
        bucket = by_rank[rank]
        random.shuffle(bucket)
        selected.extend(bucket)

    return selected[: max(count, 0)]


def has_complete_v2_bank(domain: str, level: str, minimum_count: int = 5) -> bool:
    return len(load_v2_questions(domain, level)) >= minimum_count


def _difficulty_rank(value) -> int:
    if isinstance(value, (int, float)):
        return int(value)

    text = str(value or "").strip().lower()
    return DIFFICULTY_ORDER.get(text, 3)


def unique_question_ids(questions: Iterable[dict]) -> set[str]:
    return {str(question.get("id")) for question in questions if question.get("id")}
