import json
import random
from pathlib import Path


QUESTION_BANK_ROOT = Path("app/data/question_bank")
TAXONOMY_DOMAINS = {
    "SQL": ("core", "sql"),
    "Python": ("core", "python"),
    "Data Modeling": ("core", "data_modeling"),
    "Production Engineering": ("core", "production_engineering"),
    "GCP": ("cloud", "gcp"),
}


def _platform_key(platform: str):
    return platform.lower().replace(" ", "-")


def _level_key(level: str):
    return level.lower().replace(" ", "")


def _taxonomy_level_key(level: str):
    return level.lower().replace(" ", "_").replace("-", "_")


def _read_question_file(file_path: Path):
    if not file_path.exists():
        return []

    try:
        content = file_path.read_text().strip()
        if not content:
            return []

        questions = json.loads(content)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(questions, list):
        return []

    return [question for question in questions if _is_valid_question(question)]


def _is_valid_question(question):
    return (
        isinstance(question, dict)
        and bool(question.get("id"))
        and bool(question.get("question"))
        and bool(question.get("type"))
    )


def load_questions(platform: str, level: str, bank: str = "certification"):
    file_path = (
        QUESTION_BANK_ROOT
        / _platform_key(platform)
        / bank
        / f"{_level_key(level)}.json"
    )

    return _read_question_file(file_path)


def load_taxonomy_questions(domain: str, level: str, bank: str = "interview"):
    if domain == "All Domains":
        questions = []
        for domain_name in TAXONOMY_DOMAINS:
            questions.extend(load_taxonomy_questions(domain_name, level, bank=bank))
        return questions

    taxonomy_path = TAXONOMY_DOMAINS.get(domain)
    if not taxonomy_path:
        return []

    group, domain_key = taxonomy_path
    file_path = (
        QUESTION_BANK_ROOT
        / group
        / domain_key
        / bank
        / f"{_taxonomy_level_key(level)}.json"
    )

    return _read_question_file(file_path)


def select_random_questions(
    questions,
    count=1,
    used_ids=None,
    category=None,
    difficulty=None,
):
    used_ids = set(used_ids or [])
    available_questions = []
    seen_ids = set()
    for question in questions:
        if not _is_valid_question(question):
            continue

        question_id = question.get("id")
        if question_id in used_ids or question_id in seen_ids:
            continue

        seen_ids.add(question_id)
        available_questions.append(question)

    if category:
        available_questions = [
            question
            for question in available_questions
            if question.get("category") == category
        ]

    if difficulty:
        available_questions = [
            question
            for question in available_questions
            if question.get("difficulty") == difficulty
        ]

    random.shuffle(available_questions)
    return available_questions[:count]


def evaluate_question(question: dict, user_answer: str):
    if not isinstance(question, dict):
        return {
            "is_correct": False,
            "score": 0,
            "explanation": "Invalid question structure.",
        }

    question_type = question.get("type", "mcq")

    if question_type == "mcq":
        return _evaluate_mcq(question, user_answer)

    if question_type == "fill_blank":
        return _evaluate_fill_blank(question, user_answer)

    if question_type in {"interview", "rubric"}:
        return _evaluate_interview(question, user_answer)

    return {
        "is_correct": False,
        "score": 0,
        "explanation": "Unsupported question type.",
    }


def check_answer(question: dict, selected_answer: str):
    result = evaluate_question(question, selected_answer)
    return {
        "is_correct": result["is_correct"],
        "correct_answer": question.get("correct_answer", ""),
        "explanation": result["explanation"],
    }


def _evaluate_mcq(question, selected_answer):
    correct_answer = question.get("correct_answer", "")
    is_correct = selected_answer == correct_answer

    return {
        "is_correct": is_correct,
        "score": 100 if is_correct else 0,
        "correct_answer": correct_answer,
        "explanation": question.get("explanation", ""),
    }


def _evaluate_fill_blank(question, user_answer):
    normalized_answer = str(user_answer).strip().lower()
    raw_acceptable_answers = question.get("acceptable_answers") or []
    if not isinstance(raw_acceptable_answers, list):
        raw_acceptable_answers = []

    acceptable_answers = [
        str(answer).strip().lower()
        for answer in raw_acceptable_answers
    ]
    correct_answer = str(question.get("correct_answer", "")).strip().lower()
    if correct_answer:
        acceptable_answers.append(correct_answer)

    is_correct = normalized_answer in acceptable_answers

    return {
        "is_correct": is_correct,
        "score": 100 if is_correct else 0,
        "correct_answer": question.get("correct_answer", ""),
        "acceptable_answers": raw_acceptable_answers,
        "explanation": question.get("explanation", ""),
    }


def _evaluate_interview(question, user_answer):
    answer = str(user_answer).lower()
    expected_points = question.get("expected_points", [])
    if not isinstance(expected_points, list):
        expected_points = []

    total_weight = sum(_safe_weight(point) for point in expected_points) or 100

    matched_points = []
    missing_points = []
    matched_weight = 0

    for expected_point in expected_points:
        if not isinstance(expected_point, dict):
            continue

        keywords = expected_point.get("keywords", [])
        if not isinstance(keywords, list):
            keywords = []

        matched_keywords = [
            keyword
            for keyword in keywords
            if str(keyword).lower() in answer
        ]

        weight = _safe_weight(expected_point)
        point_result = {
            "point": expected_point.get("point", ""),
            "weight": weight,
            "matched_keywords": matched_keywords,
        }

        if matched_keywords:
            matched_weight += weight
            matched_points.append(point_result)
        else:
            missing_points.append(point_result)

    score = round((matched_weight / total_weight) * 100)

    follow_ups = question.get("follow_ups", [])
    if not isinstance(follow_ups, list):
        follow_ups = []

    return {
        "is_correct": score >= 70,
        "score": min(score, 100),
        "matched_points": matched_points,
        "missing_points": missing_points,
        "explanation": question.get("explanation", ""),
        "follow_ups": follow_ups,
        "expected_answer": question.get("expected_answer", ""),
    }


def _safe_weight(expected_point):
    if not isinstance(expected_point, dict):
        return 0

    try:
        return float(expected_point.get("weight", 0))
    except (TypeError, ValueError):
        return 0
