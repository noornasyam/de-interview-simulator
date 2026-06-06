import streamlit as st

st.set_page_config(
    page_title="DE Interview Simulator",
    page_icon="🎯",
    layout="centered"
)

questions = {
    "Data Engineer": [
        "What is partitioning in BigQuery?",
        "What is the difference between batch and streaming pipelines?",
        "How do you handle duplicate records in a data pipeline?"
    ],
    "Senior Data Engineer": [
        "How would you design a CDC pipeline?",
        "How do you optimize a slow BigQuery query?",
        "How do you handle schema changes in production?"
    ],
    "Lead Data Engineer": [
        "How would you migrate 100+ Airflow DAGs to Vertex AI Pipelines?",
        "How would you design a cost-efficient GCP data platform?",
        "How do you define ownership between Core Engineering and Operations?"
    ]
}

st.title("Data Engineering Interview Simulator")
st.write("Practice role-based data engineering interview questions.")

role = st.selectbox(
    "Select your target role",
    list(questions.keys())
)

st.subheader("Interview Questions")

for index, question in enumerate(questions[role], start=1):
    st.info(f"Q{index}. {question}")

answer = st.text_area("Write your answer here")

if st.button("Submit Answer"):
    if answer.strip():
        st.success("Answer submitted successfully!")
        st.write("In the next version, we will evaluate this answer using AI.")
    else:
        st.warning("Please write an answer before submitting.")