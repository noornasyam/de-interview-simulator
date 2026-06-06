import streamlit as st

st.title("Noor's First Streamlit App")

st.write("Learning by Building 🚀")

role = st.selectbox(
    "Select Role",
    ["Data Engineer", "Senior Data Engineer", "Lead Data Engineer"]
)

st.write(f"You selected: {role}")