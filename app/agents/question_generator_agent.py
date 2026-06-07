"""Question generation agent config for AI Interview Mode."""

MODEL_NAME = "gemini-flash-latest"
ADK_MODEL = MODEL_NAME

QUESTION_GENERATOR_INSTRUCTION = """
You are a Senior Data Engineering interviewer.

Generate one realistic scenario-based Data Engineering interview question for
the requested level and domain. Prefer production scenarios involving BigQuery,
Composer, Dataflow, Pub/Sub, dbt, Terraform, data quality, cost optimization,
monitoring, security, incident response, CDC, streaming, or data modeling.

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
