"""Follow-up question agent config for AI Interview Mode."""

from app.agents.question_generator_agent import MODEL_NAME


FOLLOW_UP_INSTRUCTION = """
You are a Data Engineering interviewer.

Given the original scenario question and the candidate's first answer, ask one
concise follow-up question that probes missing senior-level depth. Prefer
production trade-offs, monitoring, cost, security, correctness, incident
handling, or scalability.

Return only valid JSON:
{
  "follow_up": ""
}
"""


def build_follow_up_agent():
    try:
        from google.adk.agents.llm_agent import Agent
    except ImportError:
        from google.adk.agents import LlmAgent as Agent

    return Agent(
        name="follow_up_agent",
        model=MODEL_NAME,
        instruction=FOLLOW_UP_INSTRUCTION,
        description="Asks one targeted follow-up question.",
    )
