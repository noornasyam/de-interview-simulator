"""Orchestrator agent config for AI Interview Mode."""

from app.agents.question_generator_agent import MODEL_NAME


ORCHESTRATOR_INSTRUCTION = """
You are the Interview Orchestrator Agent for a Data Engineering interview.

Coordinate a short three-question interview. Keep the experience practical,
production-focused, and useful for learning. Ensure each turn includes a clear
question, one follow-up, evaluation, improved sample answer, and next learning
recommendation.
"""


def build_interview_orchestrator_agent():
    try:
        from google.adk.agents.llm_agent import Agent
    except ImportError:
        from google.adk.agents import LlmAgent as Agent

    return Agent(
        name="interview_orchestrator_agent",
        model=MODEL_NAME,
        instruction=ORCHESTRATOR_INSTRUCTION,
        description="Coordinates the AI interview flow.",
    )
