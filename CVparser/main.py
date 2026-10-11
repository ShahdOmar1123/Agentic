import os
import re
import sys
from datetime import date
from pathlib import Path

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_ai import Agent

MODEL = os.getenv("MODEL", "gemini-2.5-flashen")


class Experience(BaseModel):
    company: str
    title: str
    start_date: date = Field(
        description="Start date. If only the month is given, use the first day of that month."
    )
    end_date: date | None = Field(
        default=None, description="None if the person still works there."
    )
    summary: str = Field(description="Short summary of the responsibilities in 1-2 sentences.")

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must not be before start_date")
        return self


class Education(BaseModel):
    institution: str
    degree: str
    graduation_year: int | None = Field(default=None, ge=1950, le=date.today().year + 6)


class CandidateCV(BaseModel):
    full_name: str
    email: str | None = None
    phone: str | None = None
    summary: str = Field(description="A 2-3 sentence overview of the candidate.")
    skills: list[str] = Field(description="Technical and soft skills, without duplicates.")
    experiences: list[Experience]
    education: list[Education]
    languages: list[str] = Field(default_factory=list)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str | None):
        if v is None:
            return v
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", v):
            raise ValueError(f"Invalid email format: {v}")
        return v.lower()

    @field_validator("skills")
    @classmethod
    def dedupe_skills(cls, v: list[str]):
        seen, out = set(), []
        for s in v:
            key = s.strip().lower()
            if key and key not in seen:
                seen.add(key)
                out.append(s.strip())
        return out



agent = Agent(
    MODEL,
    output_type=CandidateCV,
    instructions=(
        "You are an expert CV analyst. Extract the data from the CV text accurately. "
        "Do not invent information that is not present; if a field is missing, leave it as None. "
        "Use the YYYY-MM-DD format for dates. The CV may be in Arabic or English; "
        "keep values as they are written in the CV."
    ),

    retries=2,
)




def read_cv(path: Path) -> str:
    """Read a CV from a .txt or .pdf file and return its text."""
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return path.read_text(encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python main.py <cv.txt | cv.pdf>")

    text = read_cv(Path(sys.argv[1]))
    result = agent.run_sync(text)
    cv = result.output  

    print(cv.model_dump_json(indent=2, ensure_ascii=False))
    print("\n--- Token usage ---")
    print(result.usage)


if __name__ == "__main__":
    main()






     
        

