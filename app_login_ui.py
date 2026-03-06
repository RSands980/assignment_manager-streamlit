import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Course Manager",
    layout="centered"
)

st.title("Course Manager")

# -------------------------
# Data Loading Logic
# -------------------------

json_file = Path("users.json")

if json_file.exists():
    with json_file.open("r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = [
        {
            "id": "1",
            "email": "admin@school.edu",
            "full_name": "System Admin",
            "password": "123ssag@43AE",
            "role": "Admin",
            "registered_at": str(datetime.now())
        }
    ]

# -------------------------
# Navigation
# -------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    ["Register", "Login"]
)

# -------------------------
# REGISTER PAGE
# -------------------------

if page == "Register":

    st.header("New Instructor Account")

    with st.container():

        email = st.text_input("Email Address")
        full_name = st.text_input("Full Name")
        password = st.text_input("Password", type="password", key="register_password")

        role = st.selectbox(
            "Role",
            ["Instructor"]
        )

        btn_create = st.button("Create Account")

        if btn_create:

            with st.spinner("Creating your account..."):
                time.sleep(5)

                new_user = {
                    "id": str(uuid.uuid4()),
                    "email": email,
                    "full_name": full_name,
                    "password": password,
                    "role": role,
                    "registered_at": str(datetime.now())
                }

                users.append(new_user)

                with json_file.open("w", encoding="utf-8") as f:
                    json.dump(users, f, indent=4)

                st.success("Account created successfully!")

# -------------------------
# LOGIN PAGE
# -------------------------

if page == "Login":

    st.header("Login")

    with st.container():

        email = st.text_input("Email")
        password = st.text_input("Password", type="password", key="login_password")

        btn_login = st.button("Log In")

        if btn_login:

            with st.spinner("Verifying credentials..."):
                time.sleep(5)

                user_found = None

                for user in users:
                    if user["email"] == email and user["password"] == password:
                        user_found = user
                        break

                if user_found:
                    st.success(f"Welcome back, {user_found['full_name']}!")
                else:
                    st.error("Invalid email or password.")

    # -------------------------
    # Display User Database
    # -------------------------

    st.subheader("Current Users")

    st.dataframe(users)