from time import time

import streamlit as st

next_assignment_id_number = 3

st.title("Course Management App")
st.header("Assignments")
st.subheader("Assignments Manager")

st.divider()

#load assignments
assignments=[
    {
        "id" : "HW1",
       "title" : "Intoduction to Database",
       "description" : "basics of database design",
       "points" : 100,
       "type" : "homework",
    },
    {
        "id" : "HW2",
        "title" : "Normalization",
        "description" : "Normalize the table designs",
        "points" : 100,
        "type" : "lab"
    }
]

#Add New Assignment
st.markdown("# Add New Assignment")

#input

title = st.text_input("Title",placeholder="ex. Homework", help = "This is the name of the assignment")


description = st.text_area("Description", placeholder="ex. Basics of database design", help="This is a brief description of the assignment")
due_date = st.date_input("Due Date")
assignment_type = st.radio("Type",["Homework", "Lab"])

points = st.number_input("Points")

#assignments_type2 = st.selectbox("Type",["Homework", "Lab","Other"])
#if assignments_type2 == "Other":
#    assignments_type2 = st.text_input("Assignment Type")

#assignments_type3 = st.checkbox("Lab")

with st.expander("Assignment Preview",expanded=True):
    st.markdown("## Live Preview")
    st.markdown(f"Title: {title}")

btn_save = st.button("Save", width="stretch")

import time
import json
from pathlib import Path

json_path = Path("assignments.json")

if btn_save:
    with st.spinner("Saving the Assignment..."):
        time.sleep(5)
        if title == "":
            st.warning("Enter Assignment Title")
        else:
            #Add/Create new assignment
            new_assignment_id = "HW" + str(next_assignment_id_number)
            next_assignment_id_number += 1

            assignments.append(
                {
                 "id" : new_assignment_id,
                 "title" : title,
                 "description" : description,
                 "points" : points,
                 "type" : assignment_type
                }
            )

            with json_path.open("w",encoding="utf-8") as f:
                json.dump(assignments,f,indent=4)

            st.success("Assignment saved successfully!")
            st.dataframe(assignments)
