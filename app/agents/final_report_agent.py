"""Final report agent config for AI Interview Mode."""

from app.agents.question_generator_agent import MODEL_NAME


FINAL_REPORT_INSTRUCTION = """
You are a Data Engineering interview panel lead.

Create a concise final interview report from the completed session. Judge the
candidate against the selected level and practical Data Engineering interview
expectations.

Return only valid JSON:
{
  "overall_score": 0,
  "strengths": [],
  "gaps": [],
  "concepts_to_revise": [],
  "recommended_learning_plan": [],
  "question_reviews": [],
  "ready_for_senior_interviews": "",
  "can_move_to_next_level": ""
}
"""


def build_final_report_agent():
    try:
        from google.adk.agents.llm_agent import Agent
    except ImportError:
        from google.adk.agents import LlmAgent as Agent

    return Agent(
        name="final_report_agent",
        model=MODEL_NAME,
        instruction=FINAL_REPORT_INSTRUCTION,
        description="Creates the final AI interview report.",
    )
