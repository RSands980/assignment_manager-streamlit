import streamlit as st
import time
import json
from pathlib import Path
import uuid

st.set_page_config(
    page_title="Course Management",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("Course Management App")
st.divider()

# Load default data
assignments = [
    {
        "id": "HW1",
        "title": "Intro to Database",
        "description": "basics of database design",
        "points": 100,
        "type": "homework"
    },
    {
        "id": "HW2",
        "title": "Normalization",
        "description": "normalizing",
        "points": 100,
        "type": "homework"
    }
]

json_path = Path("assignments.json")

def load_data():
    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)
        

# Session State Initialization
if "page" not in st.session_state:
    st.session_state["page"] = "Assignment Dashboard"

if "draft" not in st.session_state:
    st.session_state["draft"] = {}

# Assignment Dashboard Page
if st.session_state["page"] == "Assignment Dashboard":
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Assignments")

    with col2:
        if st.button("Add New Assignment", key="add_new_assignment_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "Add New Assignment"
            st.rerun()

    st.dataframe(assignments, use_container_width=True)

# Add New Assignment Page
elif st.session_state["page"] == "Add New Assignment":
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Add New Assignment")

    with col2:
        if st.button("Back", key="back_btn", use_container_width=True):
            st.session_state["page"] = "Assignment Dashboard"
            st.rerun()

    st.session_state["draft"]["title"] = st.text_input(
        "Title",
        value=st.session_state["draft"]["title"],
        key="title_input"
    )

    st.session_state["draft"]["description"] = st.text_area(
        "Description",
        value=st.session_state["draft"]["description"],
        key="description_input",
        placeholder="normalization is covered here",
        help="Here you are entering the assignment details"
    )

    st.session_state["draft"]["points"] = st.number_input(
        "Points",
        min_value=0.0,
        value=float(st.session_state["draft"]["points"]),
        key="points_input"
    )

    st.session_state["draft"]["type"] = st.selectbox(
        "Type",
        options=["homework", "project", "exam"],
        index=["homework", "project", "exam"].index(st.session_state["draft"]["type"]),
        key="type_input"
    )

    if st.button("Save Assignment", key="save_assignment_btn", use_container_width=True):
        with st.spinner("Saving Assignment..."):
            
            # ADD new assignment to the assignments
            assignments.append(
                {
                    "id": str(uuid.uuid4()),
                    "title": st.session_state["draft"]["title"],
                    "description": st.session_state["draft"]["description"],
                    "points": st.session_state["draft"]["points"],
                    "type": st.session_state["draft"]["type"]
                }
            )

            with open(json_path, "w") as f:
                json.dump(assignments, f, indent=4)

            st.success("Assignment Saved!")
            time.sleep(2)

            st.session_state["draft"] = {
                "title": "",
                "description": "",
                "points": 0,
                "type": "homework"
            }

            st.session_state["page"] = "Assignment Dashboard"
            st.rerun()

elif st.session_state["page"] == "Edit Assignment":
    pass