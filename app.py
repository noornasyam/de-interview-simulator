import streamlit as st

from app.config.platforms import PLATFORMS
from app.config.levels import LEVELS
from app.services.certification_engine import load_questions, check_answer

st.set_page_config(
    page_title="Data Engineering Career Accelerator",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 Data Engineering Career Accelerator")

mode = st.selectbox(
    "Select mode",
    ["Certification"]
)

platform = st.selectbox(
    "Select cloud platform",
    PLATFORMS
)

level = st.selectbox(
    "Select level",
    LEVELS
)

questions = load_questions(platform, level)

if not questions:
    st.warning("No questions available yet for this platform and level.")
else:
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    current_index = st.session_state.current_question_index

    if current_index < len(questions):
        question = questions[current_index]

        st.subheader(f"Question {current_index + 1} of {len(questions)}")
        st.write(question["question"])

        selected_answer = st.radio(
            "Choose your answer",
            question["options"],
            key=f"question_{question['id']}"
        )

        if st.button("Submit Answer"):
            result = check_answer(question, selected_answer)

            if result["is_correct"]:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Incorrect. Correct answer: {result['correct_answer']}")

            st.info(result["explanation"])

            st.session_state.current_question_index += 1
            st.rerun()

    else:
        st.subheader("Final Result")
        st.write(f"Your score: {st.session_state.score}/{len(questions)}")

        percentage = (st.session_state.score / len(questions)) * 100
        st.write(f"Percentage: {percentage:.2f}%")

        if percentage >= 80:
            st.success("Great work!")
        elif percentage >= 50:
            st.warning("Good start. Keep practicing.")
        else:
            st.error("Needs improvement. Review the fundamentals.")

        if st.button("Restart"):
            st.session_state.current_question_index = 0
            st.session_state.score = 0
            st.rerun()