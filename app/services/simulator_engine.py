from app.services.certification_engine import (
    evaluate_question,
    load_questions,
    select_random_questions,
)


class SimulatorEngine:
    def __init__(self, platform, level, question_limit=3):
        self.platform = platform
        self.level = level
        self.question_limit = question_limit
        self.questions = load_questions(platform, level, bank="interview")

    def get_next_question(self, used_ids=None):
        selected_questions = select_random_questions(
            self.questions,
            count=1,
            used_ids=used_ids,
        )
        return selected_questions[0] if selected_questions else None

    def submit_answer(self, question, answer):
        evaluation = evaluate_question(question, answer)
        return {
            "question": question,
            "answer": answer,
            "evaluation": evaluation,
        }

    def generate_final_report(self, history):
        scores = [item["evaluation"]["score"] for item in history]
        average_score = sum(scores) / len(scores) if scores else 0

        lines = [
            "Final Interview Report",
            "",
            f"Platform: {self.platform}",
            f"Level: {self.level}",
            f"Questions answered: {len(history)}",
            f"Overall score: {average_score:.1f}/100",
            "",
            "Recommended learning path:",
            "- Review missing expected points from each answer.",
            "- Practice explaining trade-offs, monitoring, security, and cost.",
            "- Re-answer the same scenarios using the expected answer as a guide.",
        ]

        return "\n".join(lines)
