import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.graph import app
from src.tools.appointment_tool import _load_doctors
from src.evaluation.summary_report import _load_tool_logs
from collections import defaultdict

st.title("Agentic Healthcare Assistant")

if "history" not in st.session_state:
    st.session_state.history = []
if "last_disease_result" not in st.session_state:
    st.session_state.last_disease_result = None
if "last_plan" not in st.session_state:
    st.session_state.last_plan = []

tab_chat, tab_doctor, tab_info, tab_metrics = st.tabs(
    ["Chat", "Doctor view", "Medical info", "Metrics"]
)

with tab_chat:
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
        st.session_state.last_plan = result["plan"]
        if "disease_search" in result["tool_results"]:
            st.session_state.last_disease_result = result["tool_results"]["disease_search"]

    for past_query, past_answer in st.session_state.history:
        st.markdown(f"**You:** {past_query}")
        st.markdown(f"**Assistant:** {past_answer}")
        st.markdown("---")

with tab_doctor:
    st.subheader("Today's Doctors and Availability")
    doctors = _load_doctors()
    for doc in doctors:
        st.markdown(f"**{doc['name']}** ({doc['specialty']})")
        if doc["available_slots"]:
            st.write("Available slots:", ", ".join(doc["available_slots"]))
        else:
            st.write("No available slots.")
        st.markdown("---")

with tab_info:
    st.subheader("Latest Retrieved Medical Information")
    if st.session_state.last_disease_result:
        st.write(st.session_state.last_disease_result)
    else:
        st.write("No medical information has been retrieved yet this session. Ask a disease-related question in the Chat tab.")

with tab_metrics:
    st.subheader("Tool Performance Metrics")
    logs = _load_tool_logs()
    if not logs:
        st.write("No tool call logs found yet.")
    else:
        by_tool = defaultdict(list)
        for row in logs:
            by_tool[row["tool_name"]].append(row)
        for tool_name, rows in by_tool.items():
            successes = sum(1 for r in rows if r["success"] == "True")
            total = len(rows)
            avg_latency = sum(float(r["latency_ms"]) for r in rows) / len(rows)
            col1, col2 = st.columns(2)
            col1.metric(f"{tool_name} success rate", f"{successes}/{total}")
            col2.metric(f"{tool_name} avg latency", f"{avg_latency:.1f}ms")
