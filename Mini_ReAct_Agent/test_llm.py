from llm import ask_llm
question = """
Question:
What is 25 * 18?
"""
import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("GEMINI_API_KEY")[:10])
response=ask_llm(question)
print(response)