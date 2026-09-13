import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.graph import app

st.title("Agentic Healthcare Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask something")
if st.button("Submit") and query:
    with st.spinner("Thinking..."):
        result = app.invoke({
            "query": query,
            "patient_id": 1,
            "plan": [],
            "tool_results": {},
            "final_answer": "",
        })
    st.session_state.history.append((query, result["final_answer"]))

for past_query, past_answer in st.session_state.history:
    st.markdown(f"**You:** {past_query}")
    st.markdown(f"**Assistant:** {past_answer}")
    st.markdown("---")
