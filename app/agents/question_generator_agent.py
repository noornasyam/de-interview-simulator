"""Question generation agent config for AI Interview Mode."""

MODEL_NAME = "gemini-flash-latest"
ADK_MODEL = MODEL_NAME

QUESTION_GENERATOR_INSTRUCTION = """
You are a practical Data Engineering interviewer.

Generate one realistic scenario-based Data Engineering interview question for
the requested level and domain. Questions should resemble real interviews and
focus on production incidents, troubleshooting, architecture decisions,
trade-offs, cost optimization, security, governance, reliability, data quality,
CDC, streaming, orchestration, modeling, and stakeholder constraints.

Return only valid JSON:
{
  "question": "",
  "scenario": "",
  "domain": "",
  "category": "",
  "difficulty": 8
}
"""


def build_question_generator_agent():
    try:
        from google.adk.agents.llm_agent import Agent
    except ImportError:
        from google.adk.agents import LlmAgent as Agent

    return Agent(
        name="question_generator_agent",
        model=MODEL_NAME,
        instruction=QUESTION_GENERATOR_INSTRUCTION,
        description="Generates scenario-based Data Engineering interview questions.",
    )
