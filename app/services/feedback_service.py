"""Local tester feedback storage and summary utilities."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean
from uuid import uuid4


FEEDBACK_DIR = Path(__file__).resolve().parents[2] / "data" / "feedback"


def save_feedback(feedback: dict) -> Path:
    """Persist one completed tester feedback record as local JSON."""

    FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    path = FEEDBACK_DIR / f"feedback_{timestamp}_{uuid4().hex[:8]}.json"
    payload = {
        "submitted_at": datetime.now().isoformat(timespec="seconds"),
        **feedback,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return path


def load_feedback_entries() -> list[dict]:
    """Load all locally saved feedback files, skipping malformed records."""

    if not FEEDBACK_DIR.exists():
        return []

    entries = []
    for path in sorted(FEEDBACK_DIR.glob("feedback_*.json")):
        try:
            data = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict):
            entries.append(data)
    return entries


def build_feedback_summary(entries: list[dict] | None = None) -> dict:
    entries = entries if entries is not None else load_feedback_entries()
    if not entries:
        return {
            "total_interviews": 0,
            "average_score": 0,
            "average_rating": 0,
            "most_used_domain": "No data yet",
            "most_used_track": "No data yet",
            "most_common_weak_areas": [],
        }

    scores = [_to_number(entry.get("overall_score")) for entry in entries]
    ratings = [_to_number(entry.get("overall_rating")) for entry in entries]
    domains = [
        str(entry.get("domain", "")).strip()
        for entry in entries
        if str(entry.get("interview_type", "")).strip() == "Domain Practice"
        and str(entry.get("domain", "")).strip()
    ]
    tracks = [
        str(entry.get("track", "")).strip()
        for entry in entries
        if str(entry.get("interview_type", "")).strip() == "Interview Track"
        and str(entry.get("track", "")).strip()
    ]
    weak_areas = [
        str(area).strip()
        for entry in entries
        for area in entry.get("weak_areas", [])
        if str(area).strip()
    ]

    return {
        "total_interviews": len(entries),
        "average_score": round(mean(scores), 1) if scores else 0,
        "average_rating": round(mean(ratings), 1) if ratings else 0,
        "most_used_domain": _most_common(domains),
        "most_used_track": _most_common(tracks),
        "most_common_weak_areas": [area for area, _ in Counter(weak_areas).most_common(5)],
    }


def _to_number(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0


def _most_common(values: list[str]) -> str:
    if not values:
        return "No data yet"
    return Counter(values).most_common(1)[0][0]
