"""Validate DailyDEHub v2 question-bank JSON files."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BANK_ROOT = ROOT / "app" / "data" / "question_bank" / "v2"
REQUIRED_FIELDS = {
    "id",
    "domain",
    "level",
    "type",
    "difficulty",
    "concept",
    "question",
    "explanation",
    "ideal_answer",
    "tags",
}
DESCRIPTIVE_TYPES = {
    "descriptive",
    "scenario",
    "troubleshooting",
    "design_decision",
    "architecture",
    "trade_off",
    "stakeholder_impact",
    "enterprise_architecture",
    "governance",
    "cost_optimization",
    "reliability",
    "multi_region",
    "security",
}


def main() -> int:
    errors: list[str] = []
    seen_ids: set[str] = set()
    summary: list[tuple[str, str, int, Counter]] = []

    for path in sorted(BANK_ROOT.rglob("*.json")):
        if path.name == "schema.json":
            continue

        relative = path.relative_to(BANK_ROOT)
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue

        if not isinstance(data, list):
            errors.append(f"{relative}: root must be a list")
            continue

        type_counts = Counter()
        if data and len(data) < 10:
            errors.append(f"{relative}: completed files must contain at least 10 questions")

        for index, question in enumerate(data, start=1):
            if not isinstance(question, dict):
                errors.append(f"{relative}[{index}]: question must be an object")
                continue

            qid = str(question.get("id", "")).strip()
            if not qid:
                errors.append(f"{relative}[{index}]: missing id")
            elif qid in seen_ids:
                errors.append(f"{relative}[{index}]: duplicate id {qid}")
            else:
                seen_ids.add(qid)

            missing = sorted(REQUIRED_FIELDS - question.keys())
            if missing:
                errors.append(f"{relative}[{index}]: missing fields {', '.join(missing)}")

            if not str(question.get("explanation", "")).strip():
                errors.append(f"{relative}[{index}]: explanation is empty")
            if not str(question.get("ideal_answer", "")).strip():
                errors.append(f"{relative}[{index}]: ideal_answer is empty")

            qtype = str(question.get("type", "")).strip()
            type_counts[qtype] += 1
            _validate_type_specific(relative, index, question, qtype, errors)

        summary.append((relative.parts[0], path.stem, len(data), type_counts))

    for domain, level, count, type_counts in summary:
        counts = ", ".join(f"{qtype}:{amount}" for qtype, amount in sorted(type_counts.items()))
        print(f"{domain}/{level}: {count} questions ({counts or 'pending'})")

    if errors:
        print("\nValidation errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("\nV2 question bank validation passed.")
    return 0


def _validate_type_specific(relative: Path, index: int, question: dict, qtype: str, errors: list[str]) -> None:
    if qtype == "mcq":
        if not question.get("options") or "correct_answer" not in question:
            errors.append(f"{relative}[{index}]: mcq requires options and correct_answer")
    elif qtype == "match":
        for field in ["left_items", "right_items", "correct_pairs"]:
            if not question.get(field):
                errors.append(f"{relative}[{index}]: match requires {field}")
    elif qtype == "fill_blank":
        if not question.get("acceptable_answers"):
            errors.append(f"{relative}[{index}]: fill_blank requires acceptable_answers")
    elif qtype in DESCRIPTIVE_TYPES:
        if not question.get("expected_points"):
            errors.append(f"{relative}[{index}]: {qtype} requires expected_points")


if __name__ == "__main__":
    raise SystemExit(main())
