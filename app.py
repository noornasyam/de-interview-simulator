import streamlit as st

from app.config.levels import LEVELS
from app.config.platforms import PLATFORMS
from app.services.certification_engine import (
    evaluate_question,
    load_questions,
    select_random_questions,
)
from app.services.simulator_engine import SimulatorEngine


CERTIFICATION_QUESTION_LIMIT = 5
INTERVIEW_QUESTION_LIMIT = 3


def reset_session():
    for key in [
        "session_questions",
        "session_index",
        "session_score",
        "session_results",
        "question_answered",
        "explanation_shown",
        "waiting_for_next_question",
        "interview_engine",
        "interview_question",
        "interview_history",
        "interview_complete",
        "interview_report",
    ]:
        st.session_state.pop(key, None)


def start_question_session(platform, level):
    questions = load_questions(platform, level, bank="certification")
    selected_questions = select_random_questions(
        questions,
        count=min(CERTIFICATION_QUESTION_LIMIT, len(questions)),
    )

    st.session_state.session_questions = selected_questions
    st.session_state.session_index = 0
    st.session_state.session_score = 0
    st.session_state.session_results = []
    st.session_state.question_answered = False
    st.session_state.explanation_shown = False
    st.session_state.waiting_for_next_question = False


def start_interview(platform, level):
    engine = SimulatorEngine(
        platform=platform,
        level=level,
        question_limit=INTERVIEW_QUESTION_LIMIT,
    )
    first_question = engine.get_next_question()

    st.session_state.interview_engine = engine
    st.session_state.interview_question = first_question
    st.session_state.interview_history = []
    st.session_state.interview_complete = first_question is None
    st.session_state.interview_report = ""


def show_question_input(question, key_prefix):
    question_type = question.get("type", "mcq")

    if question.get("scenario"):
        st.write(question["scenario"])

    st.write(question["question"])

    if question_type == "mcq":
        return st.radio(
            "Choose your answer",
            question.get("options", []),
            key=f"{key_prefix}_{question['id']}",
        )

    if question_type in {"interview", "rubric"}:
        return st.text_area(
            "Your answer",
            key=f"{key_prefix}_{question['id']}",
            height=180,
        )

    return st.text_input("Your answer", key=f"{key_prefix}_{question['id']}")


def show_basic_evaluation(result):
    if result["is_correct"]:
        st.success("Correct.")
    else:
        st.error("Incorrect.")

    st.write(f"Score: {result['score']}/100")
    if result.get("correct_answer"):
        st.write(f"Correct answer: {result['correct_answer']}")
    if result.get("explanation"):
        st.info(result["explanation"])


def get_key_takeaways(question):
    if question.get("key_takeaways"):
        return question["key_takeaways"]

    takeaways = []
    if question.get("domain"):
        takeaways.append(f"Domain focus: {question['domain']}.")
    if question.get("category"):
        takeaways.append(f"Category: {question['category']}.")
    if question.get("explanation"):
        takeaways.append(question["explanation"])

    return takeaways


def show_learning_evaluation(question, result):
    show_basic_evaluation(result)

    takeaways = get_key_takeaways(question)
    if takeaways:
        st.write("Key Takeaways")
        for takeaway in takeaways:
            st.write(f"- {takeaway}")


def show_interview_evaluation(result):
    evaluation = result["evaluation"]
    st.write(f"Score: {evaluation['score']}/100")

    st.write("Matched points")
    if evaluation["matched_points"]:
        for point in evaluation["matched_points"]:
            st.write(f"- {point['point']} ({point['weight']} pts)")
    else:
        st.write("- No expected points matched yet.")

    st.write("Missing points")
    if evaluation["missing_points"]:
        for point in evaluation["missing_points"]:
            st.write(f"- {point['point']} ({point['weight']} pts)")
    else:
        st.write("- No missing points.")

    if evaluation.get("explanation"):
        st.info(evaluation["explanation"])

    follow_ups = evaluation.get("follow_ups", [])
    if follow_ups:
        st.write("Follow-up prompts")
        for follow_up in follow_ups:
            st.write(f"- {follow_up}")


def build_text_report(platform, level, mode, results):
    lines = [
        "Data Engineering Career Accelerator",
        f"{mode} Report",
        "",
        f"Platform: {platform}",
        f"Level: {level}",
        f"Questions answered: {len(results)}",
        "",
    ]

    if results:
        average_score = sum(item["evaluation"]["score"] for item in results) / len(results)
        lines.append(f"Overall score: {average_score:.1f}/100")
        lines.append("")

    for index, item in enumerate(results, start=1):
        question = item["question"]
        evaluation = item["evaluation"]
        lines.extend(
            [
                f"Question {index}: {question['question']}",
                f"Answer: {item['answer']}",
                f"Score: {evaluation['score']}/100",
                f"Explanation: {evaluation.get('explanation', '')}",
                "",
            ]
        )

    return "\n".join(lines)


st.set_page_config(
    page_title="Data Engineering Career Accelerator",
    page_icon="🎯",
    layout="centered",
)

st.title("🎯 Data Engineering Career Accelerator")

mode = st.selectbox(
    "Select mode",
    ["Learning Mode", "Exam Mode", "Interview Mode"],
)

platform = st.selectbox("Select cloud platform", PLATFORMS)
level = st.selectbox("Select level", LEVELS)

if mode == "Exam Mode":
    explanation_mode = "At the end only"
    st.caption("Exam Mode shows explanations at the end only.")
else:
    default_explanation_mode = (
        "After each question" if mode == "Learning Mode" else "At the end only"
    )
    explanation_mode = st.radio(
        "Show explanation",
        ["After each question", "At the end only"],
        index=0 if default_explanation_mode == "After each question" else 1,
        horizontal=True,
    )

selection_key = f"{mode}:{platform}:{level}:{explanation_mode}"
if st.session_state.get("selection_key") != selection_key:
    st.session_state.selection_key = selection_key
    reset_session()


if mode in {"Learning Mode", "Exam Mode"}:
    st.subheader(mode)

    if "session_questions" not in st.session_state:
        if st.button("Start"):
            start_question_session(platform, level)
            st.rerun()
    else:
        questions = st.session_state.session_questions
        index = st.session_state.session_index
        results = st.session_state.session_results

        if not questions:
            st.warning("No certification questions available yet for this platform and level.")
        elif index < len(questions):
            question = questions[index]
            st.write(f"Question {index + 1} of {len(questions)}")

            if mode == "Learning Mode" and st.session_state.get("waiting_for_next_question"):
                if question.get("scenario"):
                    st.write(question["scenario"])
                st.write(question["question"])

                st.divider()
                show_learning_evaluation(question, results[-1]["evaluation"])

                if st.button("Continue to Next Question"):
                    st.session_state.session_index += 1
                    st.session_state.question_answered = False
                    st.session_state.explanation_shown = False
                    st.session_state.waiting_for_next_question = False
                    st.rerun()
            else:
                answer = show_question_input(question, "cert")

                if st.button("Submit Answer"):
                    result = evaluate_question(question, answer)
                    results.append(
                        {
                            "question": question,
                            "answer": answer,
                            "evaluation": result,
                        }
                    )

                    if result["is_correct"]:
                        st.session_state.session_score += 1

                    if mode == "Learning Mode":
                        st.session_state.question_answered = True
                        st.session_state.explanation_shown = True
                        st.session_state.waiting_for_next_question = True
                    else:
                        st.session_state.session_index += 1

                    st.rerun()

        else:
            st.subheader("Final Result")
            st.write(f"Score: {st.session_state.session_score}/{len(questions)}")

            percentage = (st.session_state.session_score / len(questions)) * 100
            st.write(f"Percentage: {percentage:.2f}%")

            st.divider()
            st.write("Review")
            for result in results:
                st.write(result["question"]["question"])
                show_basic_evaluation(result["evaluation"])

            report = build_text_report(platform, level, mode, results)
            st.download_button(
                "Download text report",
                data=report,
                file_name=f"{mode.lower().replace(' ', '_')}_report.txt",
                mime="text/plain",
            )

            if st.button("Restart"):
                reset_session()
                st.rerun()

else:
    st.subheader("Interview Mode")

    if "interview_engine" not in st.session_state:
        if st.button("Start Interview"):
            start_interview(platform, level)
            st.rerun()
    elif st.session_state.interview_complete:
        history = st.session_state.interview_history

        if not history:
            st.warning("No interview questions available yet for this platform and level.")
        else:
            scores = [item["evaluation"]["score"] for item in history]
            average_score = sum(scores) / len(scores)
            st.write(f"Overall score: {average_score:.1f}/100")

            if st.session_state.interview_report:
                st.markdown(st.session_state.interview_report)

            st.divider()
            for result in history:
                st.write(result["question"]["question"])
                show_interview_evaluation(result)

            report = build_text_report(platform, level, mode, history)
            st.download_button(
                "Download text report",
                data=report,
                file_name="interview_report.txt",
                mime="text/plain",
            )

        if st.button("Restart Interview"):
            reset_session()
            st.rerun()
    else:
        history = st.session_state.interview_history
        question = st.session_state.interview_question
        question_number = len(history) + 1

        st.write(f"Question {question_number} of {INTERVIEW_QUESTION_LIMIT}")
        answer = show_question_input(question, "interview")

        if st.button("Submit Answer"):
            if not answer.strip():
                st.warning("Please write an answer before submitting.")
            else:
                engine = st.session_state.interview_engine
                result = engine.submit_answer(question, answer.strip())
                history.append(result)

                used_ids = [item["question"]["id"] for item in history]
                next_question = None
                if len(history) < INTERVIEW_QUESTION_LIMIT:
                    next_question = engine.get_next_question(used_ids=used_ids)

                if next_question:
                    st.session_state.interview_question = next_question
                else:
                    st.session_state.interview_complete = True
                    st.session_state.interview_report = engine.generate_final_report(history)

                st.rerun()

        if explanation_mode == "After each question" and history:
            st.divider()
            st.write("Previous question result")
            show_interview_evaluation(history[-1])
