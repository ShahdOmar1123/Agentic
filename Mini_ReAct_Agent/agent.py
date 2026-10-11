import re

from llm import ask_llm
from tools import calculator, search


def run_agent(question):

    prompt = f"""
Question:
{question}
"""

    while True:

        response = ask_llm(prompt)

        print("\nLLM Response:\n")
        print(response)

        if "Final Answer:" in response:
            return response.split("Final Answer:")[-1].strip()

        action_match = re.search(
            r"Action:\s*(.*)",
            response
        )

        input_match = re.search(
            r"Input:\s*(.*)",
            response
        )

        if not action_match or not input_match:
            return "Couldn't understand LLM response."

        action = action_match.group(1).strip()
        tool_input = input_match.group(1).strip()

        if action == "calculator":
            observation = calculator(tool_input)

        elif action == "search":
            observation = search(tool_input)

        else:
            observation = "Unknown tool."

        prompt += f"""

Action: {action}
Input: {tool_input}

Observation:
{observation}
"""
                