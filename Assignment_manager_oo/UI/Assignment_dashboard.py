import streamlit as st

from Assignment_manager_oo.Data.assignment_store import AssignmentStore
from Assignment_manager_oo.Services.assignment_manager import AssignmentManager


class AssignmentDashboard:
    def __init__(
        self,
        manager: "AssignmentManager",
        store: "AssignmentStore",
    ) -> None:
        self._manager = manager
        self._store = store

    def main(self) -> None:
        page = st.session_state["page"]
        st.title("Assignment Dashboard")

        if page == "dashboard":
            self._show_manage_assignments()
        elif page == "add_assignment":
            self._show_add_form()

    def _show_manage_assignments(self) -> None:
        for assignment in self._manager.all():
            st.subheader(assignment["title"])
            st.write(assignment["description"])
            st.write(f"Points: {assignment['points']}")

        if st.button("Add New Assignment"):
            st.session_state["page"] = "add_assignment"
            st.rerun()

    def _show_add_form(self) -> None:
        title = st.text_input("Title")
        description = st.text_area("Description")
        points = st.number_input("Points", min_value=0, step=1)
        assignment_type = st.selectbox("Type", ["homework", "lab", "other"])

        if st.button("Save Assignment"):
            self._manager.add(title, description, int(points), assignment_type)
            self._store.save(self._manager.all())
            st.session_state["page"] = "dashboard"
            st.rerun()

        if st.button("Back to Dashboard"):
            st.session_state["page"] = "dashboard"
            st.rerun()