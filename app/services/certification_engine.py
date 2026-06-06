import json
from pathlib import Path


def load_questions(platform: str, level: str):
    platform_key = platform.lower()
    level_key = level.lower().replace(" ", "")

    file_path = Path("app/data/question_bank") / platform_key / f"{level_key}.json"

    if not file_path.exists():
        return []

    with open(file_path, "r") as file:
        return json.load(file)


def check_answer(question: dict, selected_answer: str):
    is_correct = selected_answer == question["correct_answer"]

    return {
        "is_correct": is_correct,
        "correct_answer": question["correct_answer"],
        "explanation": question["explanation"]
    }