import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SYSTEM_PROMPT = """
You are a Mini ReAct Agent.

You have access to two tools:

1. calculator(expression)
2. search(query)

Rules:
- If you need a tool, respond ONLY in this format:

Action: calculator
Input: 25*18

or

Action: search
Input: population of Egypt

- If you know the final answer, respond ONLY in this format:

Final Answer: your answer

Never explain your reasoning.
"""


def ask_llm(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{prompt}"
    )

    return response.text.strip()