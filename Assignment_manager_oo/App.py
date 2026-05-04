import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from Data.assignment_store import AssignmentStore
from Data.chat_logger_store import ChatLoggerStore

from Services.assignment_manager import AssignmentManager
from Services.assignment_assistant_bot import AssignmentAssistantBot

from UI.assignment_dashboard import AssignmentDashboard

load_dotenv(Path(__file__).parent / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY was not found. Check your .env file.")
    st.stop()


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True

if "role" not in st.session_state:
    st.session_state["role"] = "instructor"

if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"


if st.session_state["logged_in"]:

    if st.session_state["role"] == "instructor":
        store = AssignmentStore(Path("Data/assignments.json"))
        manager = AssignmentManager(store.load())

        st.title("Course Management")

        st.divider()
        st.subheader("AI Assignment Assistant")
        st.write("Ask me anything about the assignment data.")

        logger = ChatLoggerStore(Path("Data/chat_logs.json"))
        assignments_context = store.get_assignments_as_string()
        bot = AssignmentAssistantBot(api_key, assignments_context)

        if "messages" not in st.session_state:
            st.session_state.messages = []

            logs = logger.load_logs()

            for log in logs:
                st.session_state.messages.append({
                    "role": "user",
                    "content": log["user_message"]
                })

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": log["assistant_message"]
                })

            if len(st.session_state.messages) == 0:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Hi! Ask me a question about the assignment data."
                })

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Type your question here...")

        if user_input:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })

            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response_text = bot.get_ai_response(
                        st.session_state.messages
                    )

                st.markdown(response_text)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text
            })

            logs = logger.load_logs()

            logs.append({
                "user_message": user_input,
                "assistant_message": response_text
            })

            logger.save_logs(logs)

        st.divider()

        dashboard = AssignmentDashboard(manager, store)
        dashboard.main()

    elif st.session_state["role"] == "student":
        pass

else:
    # Later development: login / register flow
    pass