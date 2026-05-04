from openai import OpenAI


class AssignmentAssistantBot:
    def __init__(self, api_key: str, context_data: str):
        self.client = OpenAI(api_key=api_key)
        self.context_data = context_data

    def build_ai_prompt(self) -> str:
        return (
            "You are a helpful assignment assistant.\n"
            "Answer user questions based ONLY on the assignment data provided below.\n"
            "If the answer is not in the assignment data, say you do not have enough information.\n\n"
            f"ASSIGNMENT DATA:\n{self.context_data}"
        )

    def get_ai_response(self, chat_history: list) -> str:
        ai_prompt = self.build_ai_prompt()

        ai_prompt_message = [
            {"role": "system", "content": ai_prompt}
        ]

        messages = ai_prompt_message + chat_history

        response = self.client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages,
            temperature=0.2
        )

        return response.choices[0].message.content