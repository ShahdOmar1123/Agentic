from ddgs import DDGS
import math


def calculator(expression):
    """
    Evaluate a mathematical expression safely.
    """

    try:
        allowed = {
            "__builtins__": {},
            "sqrt": math.sqrt,
            "pow": pow,
            "abs": abs,
            "round": round,
            "pi": math.pi,
            "e": math.e,
        }

        result = eval(expression, allowed)
        return str(result)

    except Exception as e:
        return f"Calculator Error: {e}"


def search(query):
    """
    Search the web using DuckDuckGo.
    """

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return "No results found."

        output = ""

        for i, item in enumerate(results, start=1):
            output += f"{i}. {item['title']}\n"
            output += f"{item['body']}\n"
            output += f"{item['href']}\n\n"

        return output

    except Exception as e:
        return f"Search Error: {e}"

          


       
    