import streamlit as st
from components.ui import section_title
from core.ask_data import answer_question


def render_ask_data(df,profile):
    section_title("Ask Your Data","Safe, deterministic natural-language queries first. No arbitrary Python or user code is executed.")
    question=st.chat_input("Ask: What is the total sales? Which product is highest? What is the average price?")
    if question:
        with st.chat_message("user"): st.write(question)
        answer=answer_question(df,question)
        with st.chat_message("assistant"): st.write(answer)
    st.info("Examples: 'What is the total revenue?', 'Which product has the highest sales?', 'What is the average price?', 'Show monthly sales trend'.")
