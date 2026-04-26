import streamlit as st
from pathlib import Path
from Data.assignment_store import AssignmentStore
from Services.assignment_manager import AssignmentManager
from UI.assignment_dashboard import AssignmentDashboard

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True

if "role" not in st.session_state:
    st.session_state["role"] = "instructor"

if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"

if st.session_state["logged_in"]:
    if st.session_state["role"] == "instructor":
        store = AssignmentStore(Path("data/assignments.json"))
        manager = AssignmentManager(store.load())
        dashboard = AssignmentDashboard(manager, store)
        dashboard.main()

    elif st.session_state["role"] == "student":
        pass

else:
    # Later development: login / register flow
    pass