"""Local evaluators for curated objective questions.

Gemini remains the evaluator for open-ended senior questions. Objective and
short-answer questions are scored locally to preserve credits and keep the app
useful even when a session mixes question types.
"""

from __future__ import annotations

from difflib import SequenceMatcher


GEMINI_EVALUATED_TYPES = {
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
    "architecture_review",
    "multi_region",
    "security",
    "platform_design",
}


def should_use_gemini(question: dict) -> bool:
    question_type = str(question.get("type") or question.get("question_type") or "").lower()
    return question_type in GEMINI_EVALUATED_TYPES


def evaluate_objective_question(question: dict, user_answer) -> dict:
    question_type = str(question.get("type") or "").lower()
    if question_type == "mcq":
        return evaluate_mcq(question, user_answer)
    if question_type == "fill_blank":
        return evaluate_fill_blank(question, user_answer)
    if question_type == "match":
        return evaluate_match(question, user_answer)
    if question_type in {"short_answer", "light_scenario"}:
        return evaluate_short_answer(question, user_answer)

    return _result(
        question,
        score=0,
        feedback="This question type needs Gemini evaluation.",
        missing_points=["Use Gemini evaluation for this open-ended question."],
    )


def evaluate_mcq(question: dict, user_answer) -> dict:
    correct_answer = _normalize(question.get("correct_answer"))
    answer = _normalize(user_answer)
    is_correct = answer == correct_answer
    return _result(
        question,
        score=10 if is_correct else 0,
        feedback="Correct." if is_correct else "Incorrect. Review the correct option and the explanation.",
        missing_points=[] if is_correct else [f"Correct answer: {question.get('correct_answer', '')}"],
    )


def evaluate_fill_blank(question: dict, user_answer) -> dict:
    answer = _normalize(user_answer)
    acceptable_answers = [_normalize(value) for value in question.get("acceptable_answers", [])]
    if _normalize(question.get("correct_answer")):
        acceptable_answers.append(_normalize(question.get("correct_answer")))

    if answer in acceptable_answers:
        return _result(question, score=10, feedback="Correct.", missing_points=[])

    closest = max((_similarity(answer, value) for value in acceptable_answers), default=0)
    if closest >= 0.78:
        return _result(
            question,
            score=6,
            feedback="Partially correct. Your answer is close, but use the precise term.",
            missing_points=[f"Expected: {question.get('correct_answer') or ', '.join(question.get('acceptable_answers', []))}"],
        )

    return _result(
        question,
        score=0,
        feedback="Incorrect. Review the key term and when it is used.",
        missing_points=[f"Expected: {question.get('correct_answer') or ', '.join(question.get('acceptable_answers', []))}"],
    )


def evaluate_match(question: dict, user_answer) -> dict:
    correct_pairs = question.get("correct_pairs", {})
    if not isinstance(correct_pairs, dict) or not correct_pairs:
        return _result(question, score=0, feedback="This match question is missing answer pairs.")

    answer_pairs = user_answer if isinstance(user_answer, dict) else {}
    correct_count = 0
    missing_points = []
    for left, expected_right in correct_pairs.items():
        provided = answer_pairs.get(left)
        if _normalize(provided) == _normalize(expected_right):
            correct_count += 1
        else:
            missing_points.append(f"{left} -> {expected_right}")

    score = round((correct_count / len(correct_pairs)) * 10)
    if score == 10:
        feedback = "Correct. You matched all concepts accurately."
    elif score >= 5:
        feedback = "Partially correct. Some pairs were matched correctly."
    else:
        feedback = "Mostly incorrect. Revisit how these concepts differ."

    return _result(question, score=score, feedback=feedback, missing_points=missing_points)


def evaluate_short_answer(question: dict, user_answer) -> dict:
    answer = _normalize(user_answer)
    expected_points = question.get("expected_points", [])
    if not answer:
        return _result(
            question,
            score=0,
            feedback="No answer submitted.",
            missing_points=_point_texts(expected_points) or ["Provide a short explanation."],
        )

    if expected_points:
        total_weight = 0
        matched_weight = 0
        missing_points = []
        for point in expected_points:
            if not isinstance(point, dict):
                continue
            weight = int(point.get("weight", 1) or 1)
            total_weight += weight
            keywords = [_normalize(keyword) for keyword in point.get("keywords", [])]
            if keywords and any(keyword in answer for keyword in keywords):
                matched_weight += weight
            else:
                missing_points.append(str(point.get("point", "Expected point")))

        score = round((matched_weight / total_weight) * 10) if total_weight else 0
        return _result(
            question,
            score=score,
            feedback=_feedback_for_score(score),
            missing_points=missing_points,
        )

    acceptable_answers = [_normalize(value) for value in question.get("acceptable_answers", [])]
    if any(value and value in answer for value in acceptable_answers):
        return _result(question, score=10, feedback="Correct.", missing_points=[])

    return _result(
        question,
        score=4,
        feedback="Partially correct if your explanation is directionally relevant, but it missed expected terms.",
        missing_points=question.get("acceptable_answers", []) or ["Use the expected concept terms."],
    )


def _result(question: dict, score: int, feedback: str, missing_points=None) -> dict:
    score = max(0, min(int(score), 10))
    is_correct = score >= 8
    concepts = list(dict.fromkeys([question.get("concept"), *question.get("tags", [])]))
    concepts = [str(concept) for concept in concepts if concept]
    return {
        "is_correct": is_correct,
        "score": score,
        "short_feedback": feedback,
        "feedback": feedback,
        "strengths": _strengths_for_score(score, question),
        "gaps": missing_points or [],
        "missing_points": missing_points or [],
        "explanation": str(question.get("explanation", "")),
        "ideal_answer": str(question.get("ideal_answer", "")),
        "question_type": str(question.get("type", "")),
        "difficulty": str(question.get("difficulty", "")),
        "concepts_tested": concepts,
        "concepts_to_revise": concepts if score < 8 else [],
        "dimension_scores": _dimension_scores_for_question(question, score),
        "raw_response": "Evaluated locally from curated question bank.",
        "error": "",
    }


def _dimension_scores_for_question(question: dict, score: int) -> dict:
    question_type = str(question.get("type", "")).lower()
    scores = {
        "Technical Knowledge": score,
        "Communication Clarity": score if question_type in {"short_answer", "light_scenario"} else max(score - 1, 0),
    }
    if question_type in {"short_answer", "light_scenario"}:
        scores["Problem Solving"] = score
    return scores


def _strengths_for_score(score: int, question: dict) -> list[str]:
    concept = question.get("concept") or question.get("domain") or "the tested concept"
    if score >= 8:
        return [f"Understands {concept}."]
    if score >= 5:
        return [f"Shows partial understanding of {concept}."]
    return []


def _feedback_for_score(score: int) -> str:
    if score >= 8:
        return "Strong answer. You covered the key expected ideas."
    if score >= 5:
        return "Partially correct. You covered some ideas but missed important details."
    return "Needs revision. The answer missed most expected points."


def _point_texts(expected_points) -> list[str]:
    return [
        str(point.get("point"))
        for point in expected_points
        if isinstance(point, dict) and point.get("point")
    ]


def _normalize(value) -> str:
    return " ".join(str(value or "").strip().lower().split())


def _similarity(left: str, right: str) -> float:
    return SequenceMatcher(None, left, right).ratio()
