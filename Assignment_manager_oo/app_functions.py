import os
import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(Path(__file__).parent / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY was not found. Check your .env file.")
    st.stop()

client = OpenAI(api_key=api_key)


def get_assignments_data(filepath: str) -> str:
    path = Path(filepath)

    if not path.exists():
        return "[]"

    with open(path, "r") as f:
        data = json.load(f)
        return json.dumps(data, indent=2)


assignments_context = get_assignments_data("Data/assignments.json")


def load_logs(filepath: str) -> list:
    json_path = Path(filepath)

    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)

    return []


def save_logs(filepath: str, logs: list) -> None:
    json_path = Path(filepath)

    with open(json_path, "w") as f:
        json.dump(logs, f, indent=2)


def build_ai_prompt(assignments_context: str) -> str:
    return (
        "You are a helpful assignment assistant.\n"
        "Answer user questions based ONLY on the assignment data provided below.\n"
        "If the answer is not in the assignment data, say you do not have enough information.\n\n"
        f"ASSIGNMENT DATA:\n{assignments_context}"
    )


def get_ai_response(client: OpenAI, assignments_context: str, chat_history: list) -> str:
    ai_prompt = build_ai_prompt(assignments_context)

    ai_prompt_message = [
        {
            "role": "system",
            "content": ai_prompt
        }
    ]

    messages = ai_prompt_message + chat_history

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2
    )

    return response.choices[0].message.content

from app_functions import client, assignments_context, get_ai_response, load_logs, save_logs

st.divider()
st.subheader("AI Assignment Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

    logs = load_logs("chat_logs.json")

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


chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


user_input = st.chat_input("Type your question...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with chat_container.chat_message("user"):
        st.markdown(user_input)

    with chat_container.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = get_ai_response(
                client,
                assignments_context,
                st.session_state.messages
            )

        st.markdown(response_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })

    logs = load_logs("chat_logs.json")

    logs.append({
        "user_message": user_input,
        "assistant_message": response_text
    })

    save_logs("chat_logs.json", logs)