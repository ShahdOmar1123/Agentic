# CV Parser (Pydantic AI)

Extracts structured data from a CV (`.txt` or `.pdf`) using an LLM and returns a validated Pydantic object: name, contact info, skills, work experience, education and languages.

## Features

- Structured output with Pydantic models (`CandidateCV`, `Experience`, `Education`)
- Built-in validation: email format, end date after start date, graduation year range, duplicate skills removed
- Automatic retries: if validation fails, Pydantic AI sends the error back to the model and tries again
- Works with Arabic and English CVs
- Model-agnostic: switch providers with one environment variable

## Project structure

```
cv_parser/
├── main.py          # models, agent and CLI
├── sample_cv.txt    # example CV for testing
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- An API key (a free Google Gemini key works)

## Installation

```bash
python -m pip install -U "pydantic-ai-slim[google]" pypdf
```

## Get a free API key

1. Go to https://aistudio.google.com/apikey
2. Sign in with a Google account
3. Click **Create API key** and copy it

## Configuration

Set two environment variables in the terminal you will run from.

**Windows (CMD)**

```cmd
set GOOGLE_API_KEY=your-key-here
set MODEL=google:gemini-2.5-flash
```

**Windows (PowerShell)**

```powershell
$env:GOOGLE_API_KEY="your-key-here"
$env:MODEL="google:gemini-2.5-flash"
```

**macOS / Linux**

```bash
export GOOGLE_API_KEY="your-key-here"
export MODEL="google:gemini-2.5-flash"
```

Never commit your API key or share it publicly.

## Usage

```bash
python main.py sample_cv.txt
python main.py path/to/your_cv.pdf
```

Example output:

```json
{
  "full_name": "Ahmed Hassan",
  "email": "ahmed.hassan@example.com",
  "skills": ["Python", "FastAPI", "PostgreSQL"],
  "experiences": [
    {
      "company": "Vodafone Egypt",
      "title": "Senior Backend Developer",
      "start_date": "2022-03-01",
      "end_date": null,
      "summary": "Built REST APIs with FastAPI..."
    }
  ],
  "education": [
    { "institution": "Assiut University", "degree": "B.Sc. Computer Science", "graduation_year": 2020 }
  ],
  "languages": ["Arabic", "English"]
}
```

## Using other models

| Provider | Install | MODEL | Key variable |
|----------|---------|-------|--------------|
| Google Gemini | `pydantic-ai-slim[google]` | `google:gemini-2.5-flash` | `GOOGLE_API_KEY` |
| Anthropic | `pydantic-ai-slim[anthropic]` | `anthropic:claude-sonnet-4-6` | `ANTHROPIC_API_KEY` |
| OpenAI | `pydantic-ai-slim[openai]` | `openai:gpt-4o` | `OPENAI_API_KEY` |

## How it works

1. `CandidateCV` defines the shape of the output.
2. The `Agent` receives the CV text and must return a `CandidateCV`.
3. If any validator fails, Pydantic AI sends the error back to the model and retries (`retries=2`).
4. `result.output` is a validated Python object.

The core Pydantic AI code is only this:

```python
agent = Agent(MODEL, output_type=CandidateCV, instructions="...", retries=2)
result = agent.run_sync(text)
cv = result.output
```

## Privacy note

Free-tier requests to Gemini may be used by Google to improve its products. Do not send real CVs containing personal data while using the free tier.

## Ideas for next steps

- [ ] Compute years of experience with `computed_field`
- [ ] Process a folder of CVs and export to CSV
- [ ] Wrap it in a FastAPI endpoint for file upload
- [ ] Add Logfire tracing
- [ ] Write tests with `TestModel` (no real API calls)
