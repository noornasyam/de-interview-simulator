import streamlit as st

questions = {
    "Data Engineer": "What is partitioning in BigQuery?",
    "Senior Data Engineer": "How would you design a CDC pipeline?",
    "Lead Data Engineer": "How would you migrate Airflow DAGs to Vertex AI Pipelines?"
}

st.title("Data Engineering Career Accelerator")

role = st.selectbox(
    "Select your role",
    list(questions.keys())
)

st.subheader("Interview Question")

question = questions[role]

st.info(question)

answer = st.text_area(
    "Write your answer here"
)

rating = st.slider(
    "Rate your answer",
    1,
    10,
    5
)

if st.button("Submit"):
    st.success("Submission Successful!")

    st.write("### Summary")

    st.write(f"Role: {role}")
    st.write(f"Question: {question}")
    st.write(f"Your Rating: {rating}/10")
    st.write(f"Your Answer: {answer}")