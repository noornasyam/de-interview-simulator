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
from app.agents.final_report_agent import build_final_report_agent
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
    "Data Modeling",
    "Production Engineering",
    "Mixed Interview",
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
            "score": _safe_score(evaluation.get("score", 0)),
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
    if not is_adk_configured():
        return _final_report_error(_setup_message())

    try:
        prompt = _build_final_report_prompt(history, role, domain)
        raw_response = _run_adk_agent(build_final_report_agent(), prompt)
        report = _extract_json(raw_response)
        return {
            "overall_score": _safe_score(report.get("overall_score", 0)),
            "strengths": _safe_list(report.get("strengths")),
            "gaps": _safe_list(report.get("gaps")),
            "concepts_to_revise": _safe_list(report.get("concepts_to_revise")),
            "recommended_learning_plan": _safe_list(report.get("recommended_learning_plan")),
            "question_reviews": _safe_list(report.get("question_reviews")),
            "ready_for_senior_interviews": str(
                report.get("ready_for_senior_interviews", "")
            ).strip(),
            "can_move_to_next_level": str(report.get("can_move_to_next_level", "")).strip(),
            "raw_response": raw_response,
            "error": "",
        }
    except Exception as exc:
        return _final_report_error(f"Gemini final report failed: {exc}")


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
            "question_number": len(history) + 1,
            "max_questions": MAX_QUESTIONS,
            "avoid_previous_questions": previous_questions,
            "grounding_examples": _grounding_examples(domain),
            "constraints": [
                "real production scenario",
                "one question only",
                "no answer included",
                "difficulty 7 or 8",
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
            "question": question,
            "candidate_answer": user_answer,
            "history_length": len(history),
            "constraints": [
                "score 0-100",
                "short feedback",
                "include missing points",
                "include explanation",
                "include ideal answer",
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
                "answer": item.get("answer", ""),
                "score": evaluation.get("score", 0),
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
    return domain


def _domain_to_category(domain):
    return {
        "SQL": "sql",
        "Python": "python",
        "GCP / BigQuery": "bigquery",
        "Data Modeling": "data_modeling",
        "Production Engineering": "production_engineering",
        "Mixed Interview": "mixed",
    }.get(domain, "data_engineering")


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
