import streamlit as st
import time
import json
from pathlib import Path, path

st.title("Course Management App")
st.divider()

next_assignment_id_number = 3

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

json_path = Path("assignments.json")

if json_path.exists():
    with json_path.open("r",encoding="utf-8") as f:
        assignments = json.load(f)



tab1, tab2, tab3, = st.tabs(["View Assignments", "Add New Assignment", "Update An Assignment"])

with tab1:
    #st.info("This tab is is under development!")
    option = st.radio("View/Search", ["View", "Search"], horizontal= True)
    if option == "View":
        st.dataframe(assignments)

with tab2:
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
