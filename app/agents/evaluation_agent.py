"""Evaluation and feedback agent config for AI Interview Mode."""

from app.agents.question_generator_agent import MODEL_NAME


EVALUATION_INSTRUCTION = """
You are a Senior Data Engineering interview evaluator and coach.

Evaluate the candidate answer for correctness, level-appropriate depth,
production thinking, cost awareness, monitoring, security, and trade-off
discussion.

Return only valid JSON:
{
  "score": 0,
  "dimension_scores": {
    "Technical Knowledge": 0,
    "Problem Solving": 0,
    "Communication Clarity": 0,
    "Architecture Thinking": 0,
    "Cost Awareness": 0,
    "Security Awareness": 0
  },
  "short_feedback": "",
  "strengths": [],
  "missing_points": [],
  "explanation": "",
  "ideal_answer": "",
  "follow_up_question": "",
  "concepts_to_revise": [],
  "next_learning_recommendation": "",
  "raw_response": ""
}
"""


def build_evaluation_agent():
    try:
        from google.adk.agents.llm_agent import Agent
    except ImportError:
        from google.adk.agents import LlmAgent as Agent

    return Agent(
        name="evaluation_feedback_agent",
        model=MODEL_NAME,
        instruction=EVALUATION_INSTRUCTION,
        description="Evaluates answers and returns coaching feedback.",
    )
