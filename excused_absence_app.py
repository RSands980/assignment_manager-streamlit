import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Excused Absences", layout="wide")

json_path = Path("requests.json")

if json_path.exists():
    with open(json_path, "r") as f:
        requests = json.load(f)
else:
    requests = []

if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"

if "selected_request" not in st.session_state:
    st.session_state["selected_request"] = None

with st.sidebar:
    if st.button("Excuse Absence Dashboard", use_container_width=True):
        st.session_state["page"] = "dashboard"
        st.rerun()

    if st.button("Excuse Absence Request", use_container_width=True):
        st.session_state["page"] = "request"
        st.rerun()

if st.session_state["page"] == "dashboard":
    st.title("Excuse Absences")

    st.divider()

    total_count = len(requests)

    pending_count = 0
    for r in requests:
        if r["status"] == "Pending":
            pending_count += 1

    top_left, top_right1, top_right2 = st.columns([3, 1, 1])

    with top_left:
        st.subheader("Excused Absences")
        st.write("Review student submissions and approve or cancel excused absences.")

    with top_right1:
        st.metric("Count", total_count)

    with top_right2:
        st.metric("Pending", pending_count)

    with st.container():
        search_col, filter_col = st.columns([2, 1])

        with search_col:
            search_email = st.text_input("Search by student Email")

        with filter_col:
            selected_status = st.selectbox(
                "Status",
                ["All", "Pending", "Approved", "Cancelled"]
            )

    st.divider()

    filtered_requests = []

    for r in requests:
        email_match = search_email.lower() in r["student_email"].lower()

        if selected_status == "All":
            status_match = True
        else:
            status_match = r["status"] == selected_status

        if email_match and status_match:
            filtered_requests.append(r)

    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("Requests")

        if len(filtered_requests) > 0:
            event = st.dataframe(
                filtered_requests,
                on_select="rerun",
                selection_mode="single-row",
                use_container_width=True
            )

            if event.selection.rows:
                index = event.selection.rows[0]
                st.session_state["selected_request"] = filtered_requests[index]
            else:
                st.session_state["selected_request"] = None
        else:
            st.write("No requests found.")
            st.session_state["selected_request"] = None

    with right_col:
        if st.session_state["selected_request"] is not None:
            r = st.session_state["selected_request"]

            st.subheader("Request Details")

            with st.container():
                st.write("Status:", r["status"])
                st.write("Student Email:", r["student_email"])
                st.write("Course ID:", r["course_id"])
                st.write("Absence Date:", r["absence_date"])
                st.write("Submitted:", r["submitted_timestamp"])
                st.write("Excuse Type:", r["excuse_type"])
                st.write("Explanation:", r["explanation"])
                st.write("Instructor Note:", r["instructor_note"])

elif st.session_state["page"] == "request":
    st.title("Submit Excused Absence")
    st.write("Form is being developed...")