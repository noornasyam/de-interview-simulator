"""Sync-safe Google ADK adapter for AI Interview Mode.

This module keeps Gemini/ADK usage isolated from the existing local Streamlit
flows. AI Interview Mode requires a configured Gemini key; it does not silently
fall back to local scoring.
"""

import asyncio
import json
import os
import random
import uuid
from pathlib import Path

from app.agents.evaluation_agent import build_evaluation_agent
from app.agents.follow_up_agent import build_follow_up_agent
from app.agents.interview_orchestrator_agent import build_interview_orchestrator_agent
from app.agents.question_generator_agent import MODEL_NAME, build_question_generator_agent
from app.services.certification_engine import load_taxonomy_questions


MAX_QUESTIONS = 10
ADK_QUESTION_COUNT = MAX_QUESTIONS
APP_NAME = "de_interview_simulator_ai"
USER_ID = "streamlit_user"
AI_ROLES = [
    "Beginner",
    "Junior Data Engineer",
    "Mid-Level Data Engineer",
    "Senior Data Engineer",
    "Lead Data Engineer",
    "Architect",
]
AI_DOMAINS = [
    "SQL",
    "Python",
    "GCP / BigQuery",
    "AWS",
    "Azure",
    "Databricks",
    "Git",
    "Terraform",
    "Airflow",
    "dbt",
    "Data Modeling",
    "Production Engineering",
    "Mixed Interview",
]
QUESTION_TYPES = [
    "Conceptual",
    "Scenario-based",
    "Troubleshooting",
    "Design decision",
    "Cost optimization",
    "Security/governance",
    "Debugging/root cause analysis",
    "Trade-off comparison",
    "Scenario-based",
    "Design decision",
]
SCORING_DIMENSIONS = [
    "Technical Knowledge",
    "Problem Solving",
    "Communication Clarity",
    "Architecture Thinking",
    "Cost Awareness",
    "Security Awareness",
]


def is_adk_configured():
    return bool(_get_google_api_key())


def start_ai_interview(role="Senior Data Engineer", domain="GCP / BigQuery"):
    _try_build_agent(build_interview_orchestrator_agent)
    return {
        "role": role,
        "domain": domain,
        "question_count": MAX_QUESTIONS,
        "model": MODEL_NAME,
        "configured": is_adk_configured(),
        "history": [],
    }


def generate_ai_question(role, domain, history=None):
    history = history or []
    if not is_adk_configured():
        return _error_payload("question", _setup_message())

    try:
        prompt = _build_question_prompt(role, domain, history)
        raw_response = _run_adk_agent(build_question_generator_agent(), prompt)
        generated = _extract_json(raw_response)
        if not generated.get("question"):
            raise ValueError("Gemini response did not include a question.")

        return {
            "id": f"ai-question-{uuid.uuid4().hex[:8]}",
            "question": str(generated.get("question", "")).strip(),
            "scenario": str(generated.get("scenario", "")).strip(),
            "domain": str(generated.get("domain") or domain).strip(),
            "question_type": str(
                generated.get("question_type") or _question_type_for_index(len(history))
            ).strip(),
            "complexity": _complexity_for_index(len(history)),
            "category": str(generated.get("category") or _domain_to_category(domain)).strip(),
            "difficulty": _safe_score(generated.get("difficulty", 8), maximum=10),
            "raw_response": raw_response,
        }
    except Exception as exc:
        return _error_payload("question", f"Gemini question generation failed: {exc}")


def generate_ai_follow_up(question, user_answer, role, domain, history=None):
    history = history or []
    if not is_adk_configured():
        return _error_payload("follow_up", _setup_message())

    if not str(user_answer).strip():
        return _error_payload("follow_up", "Please answer the main question before requesting a follow-up.")

    try:
        prompt = _build_follow_up_prompt(question, user_answer, role, domain, history)
        raw_response = _run_adk_agent(build_follow_up_agent(), prompt)
        generated = _extract_json(raw_response)
        follow_up = str(generated.get("follow_up", "")).strip()
        if not follow_up:
            raise ValueError("Gemini response did not include a follow-up question.")

        return {"follow_up": follow_up, "raw_response": raw_response}
    except Exception as exc:
        return _error_payload("follow_up", f"Gemini follow-up generation failed: {exc}")


def evaluate_ai_answer(question, user_answer, role, domain, history=None):
    history = history or []
    if not is_adk_configured():
        return _evaluation_error(_setup_message())

    if not str(user_answer).strip():
        return _evaluation_error("Please answer the question before submitting.")

    try:
        prompt = _build_evaluation_prompt(
            question,
            user_answer,
            role,
            domain,
            history,
        )
        raw_response = _run_adk_agent(build_evaluation_agent(), prompt)
        evaluation = _extract_json(raw_response)
        return {
            "score": _safe_score(evaluation.get("score", 0), maximum=10),
            "dimension_scores": _normalize_dimension_scores(evaluation.get("dimension_scores")),
            "short_feedback": str(evaluation.get("short_feedback", "")).strip(),
            "strengths": _safe_list(evaluation.get("strengths")),
            "missing_points": _safe_list(evaluation.get("missing_points") or evaluation.get("gaps")),
            "gaps": _safe_list(evaluation.get("gaps") or evaluation.get("missing_points")),
            "explanation": str(evaluation.get("explanation", "")).strip(),
            "ideal_answer": str(
                evaluation.get("ideal_answer") or evaluation.get("improved_answer", "")
            ).strip(),
            "follow_up_question": str(evaluation.get("follow_up_question", "")).strip(),
            "concepts_to_revise": _safe_list(evaluation.get("concepts_to_revise")),
            "next_learning_recommendation": str(evaluation.get("next_learning_recommendation", "")).strip(),
            "raw_response": raw_response,
            "error": "",
        }
    except Exception as exc:
        return _evaluation_error(f"Gemini evaluation failed: {exc}")


def generate_ai_final_report(history, role, domain):
    scores = [_safe_score(item.get("evaluation", {}).get("score", 0), maximum=10) for item in history]
    correct_count = sum(1 for score in scores if score >= 8)
    partial_count = sum(1 for score in scores if 5 <= score <= 7)
    incorrect_count = sum(1 for score in scores if score < 5)
    total_score = sum(scores)
    average_score = total_score / len(scores) if scores else 0
    readiness_percentage = round(average_score * 10)
    dimension_scores = _aggregate_dimension_scores(history)
    domain_scores = _aggregate_domain_scores(history, domain)
    hiring_recommendation = _hiring_recommendation(average_score)

    strengths = _dedupe(
        strength
        for item in history
        for strength in item.get("evaluation", {}).get("strengths", [])
    )
    weak_areas = _dedupe(
        point
        for item in history
        for point in (
            item.get("evaluation", {}).get("missing_points")
            or item.get("evaluation", {}).get("gaps", [])
        )
    )
    concepts = _dedupe(
        concept
        for item in history
        for concept in item.get("evaluation", {}).get("concepts_to_revise", [])
    )

    return {
        "overall_score": total_score,
        "total_score": total_score,
        "average_score": round(average_score, 1),
        "readiness_percentage": readiness_percentage,
        "correct_count": correct_count,
        "partial_count": partial_count,
        "incorrect_count": incorrect_count,
        "domain_scores": domain_scores,
        "dimension_scores": dimension_scores,
        "strengths": strengths[:8] or ["Completed the interview session."],
        "gaps": weak_areas[:8] or ["Add more detail, examples, and trade-offs."],
        "weak_areas": weak_areas[:8] or ["Add more detail, examples, and trade-offs."],
        "concepts_to_revise": concepts[:8] or weak_areas[:5],
        "recommended_learning_plan": _recommended_next_steps(
            average_score,
            role,
            concepts or weak_areas,
        ),
        "question_reviews": _compact_history(history),
        "can_move_to_next_level": _move_recommendation(average_score, role, concepts or weak_areas),
        "hiring_recommendation": hiring_recommendation,
        "raw_response": "Final summary computed locally from Gemini evaluations.",
        "error": "",
    }


# Backward-compatible names for older imports while app.py transitions to AI naming.
start_adk_interview = start_ai_interview
generate_adk_question = generate_ai_question
evaluate_adk_answer = evaluate_ai_answer


def _get_google_api_key():
    if os.environ.get("GOOGLE_API_KEY"):
        return os.environ["GOOGLE_API_KEY"]

    env_path = Path(".env")
    if not env_path.exists():
        return ""

    for line in env_path.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("GOOGLE_API_KEY="):
            value = stripped.split("=", 1)[1].strip().strip('"').strip("'")
            if value:
                os.environ["GOOGLE_API_KEY"] = value
            return value

    return ""


def _setup_message():
    return "Setup required: set GOOGLE_API_KEY in your environment or local .env file."


def _try_build_agent(builder):
    try:
        return builder()
    except Exception:
        return None


def _build_question_prompt(role, domain, history):
    question_number = len(history) + 1
    question_type = _question_type_for_index(len(history))
    complexity = _complexity_for_index(len(history))
    previous_questions = [
        item.get("question", {}).get("question", "")
        for item in history
        if isinstance(item, dict)
    ]
    return json.dumps(
        {
            "task": "Generate exactly one scenario-based Data Engineering interview question.",
            "role": role,
            "domain": domain,
            "question_number": question_number,
            "max_questions": MAX_QUESTIONS,
            "question_type": question_type,
            "complexity": complexity,
            "avoid_previous_questions": previous_questions,
            "grounding_examples": _grounding_examples(domain),
            "constraints": [
                f"question type must be {question_type}",
                f"complexity must be {complexity}",
                "match selected level and domain",
                "Beginner uses simple language and fundamentals",
                "Architect focuses on enterprise architecture, governance, cost, scalability, reliability, and stakeholder trade-offs",
                "avoid coding-heavy questions unless domain is Python or SQL",
                "one question only",
                "no answer included",
                "vary question types across the session",
                "return valid JSON only",
            ],
        }
    )


def _build_follow_up_prompt(question, user_answer, role, domain, history):
    return json.dumps(
        {
            "task": "Ask exactly one targeted follow-up question.",
            "role": role,
            "domain": domain,
            "question": question,
            "candidate_answer": user_answer,
            "history_length": len(history),
            "constraints": [
                "probe missing senior-level depth",
                "one follow-up question only",
                "return valid JSON only",
            ],
        }
    )


def _build_evaluation_prompt(question, user_answer, role, domain, history):
    return json.dumps(
        {
            "task": "Evaluate the candidate answer and provide coaching feedback.",
            "role": role,
            "domain": domain,
            "criteria": [
                "correctness",
                "senior-level depth",
                "production thinking",
                "cost awareness",
                "monitoring",
                "security",
                "trade-offs",
            ],
            "scoring_dimensions": SCORING_DIMENSIONS,
            "question": question,
            "candidate_answer": user_answer,
            "history_length": len(history),
            "constraints": [
                "score 0-10",
                "dimension_scores must score each relevant dimension 0-10",
                "omit a dimension only if it is genuinely not relevant",
                "short feedback must be easy to understand",
                "missing points must be specific",
                "explanation must explain why the answer is correct or incomplete",
                "explanation must include the key concept behind the question",
                "ideal answer must be concise and level-appropriate",
                "include one follow-up question only if useful",
                "return valid JSON only",
            ],
        }
    )


def _build_final_report_prompt(history, role, domain):
    return json.dumps(
        {
            "task": "Create the final AI interview report.",
            "role": role,
            "domain": domain,
            "session": _compact_history(history),
            "constraints": [
                "overall score 0-100",
                "include whether user can move to the next level",
                "include practical learning plan",
                "return valid JSON only",
            ],
        }
    )


def _compact_history(history):
    compacted = []
    for item in history:
        if not isinstance(item, dict):
            continue
        evaluation = item.get("evaluation", {})
        compacted.append(
            {
                "question": item.get("question", {}).get("question", ""),
                "domain": item.get("question", {}).get("domain", ""),
                "answer": item.get("answer", ""),
                "score": evaluation.get("score", 0),
                "dimension_scores": evaluation.get("dimension_scores", {}),
                "short_feedback": evaluation.get("short_feedback", ""),
                "strengths": evaluation.get("strengths", []),
                "missing_points": evaluation.get("missing_points", evaluation.get("gaps", [])),
                "explanation": evaluation.get("explanation", ""),
                "ideal_answer": evaluation.get("ideal_answer", ""),
            }
        )
    return compacted


def _grounding_examples(domain):
    taxonomy_domain = _domain_to_taxonomy_domain(domain)
    questions = load_taxonomy_questions(taxonomy_domain, "Senior", bank="interview")
    if not questions:
        return []

    examples = random.sample(questions, k=min(2, len(questions)))
    return [
        {
            "scenario": question.get("scenario", ""),
            "question": question.get("question", ""),
            "expected_points": question.get("expected_points", [])[:3],
        }
        for question in examples
    ]


def _domain_to_taxonomy_domain(domain):
    if domain == "GCP / BigQuery":
        return "GCP"
    if domain == "Mixed Interview":
        return "All Domains"
    if domain not in {"SQL", "Python", "Data Modeling", "Production Engineering"}:
        return "All Domains"
    return domain


def _domain_to_category(domain):
    return {
        "SQL": "sql",
        "Python": "python",
        "GCP / BigQuery": "bigquery",
        "AWS": "aws",
        "Azure": "azure",
        "Databricks": "databricks",
        "Git": "git",
        "Terraform": "terraform",
        "Airflow": "airflow",
        "dbt": "dbt",
        "Data Modeling": "data_modeling",
        "Production Engineering": "production_engineering",
        "Mixed Interview": "mixed",
    }.get(domain, "data_engineering")


def _question_type_for_index(index):
    return QUESTION_TYPES[index % len(QUESTION_TYPES)]


def _complexity_for_index(index):
    if index <= 2:
        return "foundation"
    if index <= 6:
        return "practical scenario"
    return "advanced decision-making and trade-offs"


def _dedupe(values):
    result = []
    seen = set()
    for value in values:
        text = str(value).strip()
        if text and text.lower() not in seen:
            seen.add(text.lower())
            result.append(text)
    return result


def _recommended_next_steps(average_score, role, topics):
    if average_score >= 8:
        return [
            f"Move toward the next level after one more {role} mixed interview.",
            "Practice explaining trade-offs with concrete production examples.",
        ]
    if average_score >= 5:
        first_topic = topics[0] if topics else "the missed concepts"
        return [
            "Repeat the same level after focused revision.",
            f"Revise {first_topic}.",
            "Practice adding monitoring, failure modes, and trade-offs to every answer.",
        ]
    first_topic = topics[0] if topics else "fundamentals"
    return [
        "Repeat the same level.",
        f"Revise {first_topic} before attempting a new interview.",
        "Answer with a simple structure: context, approach, trade-offs, validation.",
    ]


def _move_recommendation(average_score, role, topics):
    if average_score >= 8:
        return f"Move to the next level. Your average score is {average_score:.1f}/10."
    if average_score >= 5:
        focus = topics[0] if topics else "the weak areas"
        return f"Partially ready. Repeat {role} after revising {focus}."
    focus = topics[0] if topics else "core fundamentals"
    return f"Repeat the same level. Focus first on {focus}."


def _normalize_dimension_scores(value):
    if not isinstance(value, dict):
        return {}

    normalized = {}
    for dimension in SCORING_DIMENSIONS:
        if dimension in value:
            normalized[dimension] = _safe_score(value.get(dimension), maximum=10)
    return normalized


def _aggregate_dimension_scores(history):
    totals = {dimension: [] for dimension in SCORING_DIMENSIONS}
    for item in history:
        dimensions = item.get("evaluation", {}).get("dimension_scores", {})
        if not isinstance(dimensions, dict):
            continue
        for dimension in SCORING_DIMENSIONS:
            if dimension in dimensions:
                totals[dimension].append(_safe_score(dimensions[dimension], maximum=10))

    return {
        dimension: round(sum(scores) / len(scores), 1)
        for dimension, scores in totals.items()
        if scores
    }


def _aggregate_domain_scores(history, selected_domain):
    totals = {}
    for item in history:
        question = item.get("question", {})
        domain = str(question.get("domain") or selected_domain).strip() or selected_domain
        score = _safe_score(item.get("evaluation", {}).get("score", 0), maximum=10)
        totals.setdefault(domain, []).append(score)

    return {
        domain: round(sum(scores) / len(scores), 1)
        for domain, scores in totals.items()
        if scores
    }


def _hiring_recommendation(average_score):
    if average_score >= 8.5:
        return "Strong Candidate"
    if average_score >= 7:
        return "Ready"
    if average_score >= 5:
        return "Borderline"
    return "Not Ready"


def _run_adk_agent(agent, prompt):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(_run_adk_agent_async(agent, prompt))

    raise RuntimeError("AI Interview Mode cannot run ADK inside an existing event loop.")


async def _run_adk_agent_async(agent, prompt):
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    session_service = InMemorySessionService()
    session_id = f"ai-session-{uuid.uuid4().hex[:8]}"
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    content = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text or ""

    return final_text


def _extract_json(raw_response):
    raw_response = raw_response or ""
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        start = raw_response.find("{")
        end = raw_response.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return {}
        try:
            return json.loads(raw_response[start : end + 1])
        except json.JSONDecodeError:
            return {}


def _error_payload(kind, message):
    return {"error": message, kind: "", "raw_response": ""}


def _evaluation_error(message):
    return {
        "score": 0,
        "short_feedback": "",
        "strengths": [],
        "gaps": [message],
        "missing_points": [message],
        "explanation": "",
        "ideal_answer": "",
        "follow_up_question": "",
        "concepts_to_revise": [],
        "next_learning_recommendation": "",
        "raw_response": "",
        "error": message,
    }


def _final_report_error(message):
    return {
        "overall_score": 0,
        "strengths": [],
        "gaps": [message],
        "concepts_to_revise": [],
        "recommended_learning_plan": [],
        "question_reviews": [],
        "ready_for_senior_interviews": "",
        "can_move_to_next_level": "",
        "raw_response": "",
        "error": message,
    }


def _safe_score(score, maximum=100):
    try:
        return max(0, min(maximum, int(score)))
    except (TypeError, ValueError):
        return 0


def _safe_list(value):
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if value:
        return [str(value)]
    return []
