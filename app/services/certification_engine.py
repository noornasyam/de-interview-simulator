import json
import random
from pathlib import Path


VALID_CATEGORIES = {
    "sql",
    "storage",
    "streaming",
    "data_modeling",
    "security",
    "monitoring",
    "cost",
    "architecture",
    "leadership",
}


def _platform_key(platform: str):
    return platform.lower().replace(" ", "-")


def _level_key(level: str):
    return level.lower().replace(" ", "")


def _taxonomy_level_key(level: str):
    return level.lower().replace(" ", "_").replace("-", "_")


def load_questions(platform: str, level: str, bank: str = "certification"):
    file_path = (
        Path("app/data/question_bank")
        / _platform_key(platform)
        / bank
        / f"{_level_key(level)}.json"
    )

    if not file_path.exists():
        return []

    try:
        content = file_path.read_text().strip()
        if not content:
            return []

        questions = json.loads(content)
        return questions if isinstance(questions, list) else []
    except json.JSONDecodeError:
        return []


def load_taxonomy_questions(domain: str, level: str, bank: str = "interview"):
    domain_map = {
        "SQL": ("core", "sql"),
        "Python": ("core", "python"),
        "Data Modeling": ("core", "data_modeling"),
        "Production Engineering": ("core", "production_engineering"),
        "GCP": ("cloud", "gcp"),
    }

    taxonomy_path = domain_map.get(domain)
    if not taxonomy_path:
        return []

    group, domain_key = taxonomy_path
    file_path = (
        Path("app/data/question_bank")
        / group
        / domain_key
        / bank
        / f"{_taxonomy_level_key(level)}.json"
    )

    if not file_path.exists():
        return []

    try:
        content = file_path.read_text().strip()
        if not content:
            return []

        questions = json.loads(content)
        return questions if isinstance(questions, list) else []
    except json.JSONDecodeError:
        return []


def select_random_questions(
    questions,
    count=1,
    used_ids=None,
    category=None,
    difficulty=None,
):
    used_ids = set(used_ids or [])
    available_questions = [
        question
        for question in questions
        if question.get("id") not in used_ids
    ]

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
    normalized_answer = user_answer.strip().lower()
    acceptable_answers = [
        answer.strip().lower()
        for answer in question.get("acceptable_answers", [])
    ]
    correct_answer = question.get("correct_answer", "").strip().lower()
    if correct_answer:
        acceptable_answers.append(correct_answer)

    is_correct = normalized_answer in acceptable_answers

    return {
        "is_correct": is_correct,
        "score": 100 if is_correct else 0,
        "correct_answer": question.get("correct_answer", ""),
        "acceptable_answers": question.get("acceptable_answers", []),
        "explanation": question.get("explanation", ""),
    }


def _evaluate_interview(question, user_answer):
    answer = user_answer.lower()
    expected_points = question.get("expected_points", [])
    total_weight = sum(point.get("weight", 0) for point in expected_points) or 100

    matched_points = []
    missing_points = []
    matched_weight = 0

    for expected_point in expected_points:
        keywords = expected_point.get("keywords", [])
        matched_keywords = [
            keyword
            for keyword in keywords
            if keyword.lower() in answer
        ]

        point_result = {
            "point": expected_point.get("point", ""),
            "weight": expected_point.get("weight", 0),
            "matched_keywords": matched_keywords,
        }

        if matched_keywords:
            matched_weight += expected_point.get("weight", 0)
            matched_points.append(point_result)
        else:
            missing_points.append(point_result)

    score = round((matched_weight / total_weight) * 100)

    return {
        "is_correct": score >= 70,
        "score": min(score, 100),
        "matched_points": matched_points,
        "missing_points": missing_points,
        "explanation": question.get("explanation", ""),
        "follow_ups": question.get("follow_ups", []),
        "expected_answer": question.get("expected_answer", ""),
    }
