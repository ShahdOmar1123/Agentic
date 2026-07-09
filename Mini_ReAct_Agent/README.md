# Mini ReAct Agent

A simple ReAct (Reason + Act) Agent built in pure Python using the Gemini API.

## Features

- ReAct reasoning loop
- Calculator tool
- Search tool (DuckDuckGo)
- Gemini API integration
- Pure Python implementation
- Environment variables using `.env`

## Project Structure

```
Mini_ReAct_Agent/
│── main.py
│── agent.py
│── llm.py
│── tools.py
│── test_llm.py
│── requirements.txt
│── .env.example
│── README.md
```

## Installation

```bash
git clone https://github.com/your-username/Mini_ReAct_Agent.git

cd Mini_ReAct_Agent

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

## Run

```bash
python main.py
```

## Example

```
Ask a question:
calculate 4*5

LLM Response:

Action: calculator
Input: 4*5

LLM Response:

Final Answer: 20
```

## Tech Stack

- Python
- Gemini API
- DuckDuckGo Search
- Python-dotenv