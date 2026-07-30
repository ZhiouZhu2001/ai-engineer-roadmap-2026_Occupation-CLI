from pydantic import BaseModel, Field, field_validator
from typing import Literal

class JobDescription(BaseModel):
    title: str | None = None
    company: str | None = None
    raw_text: str = Field(min_length=1)
    source: str | None = None

    @field_validator("raw_text")
    @classmethod
    def text_must_not_be_blank(cls, value:str) -> str:
        if not value.strip():
            raise ValueError("Job Description cannot be blank")
        return value


class SkillMatch(BaseModel):
    skill: str = Field(min_length=1)
    category: str = Field(min_length=1)
    weight: int
    matched: bool
    evidence: list[str] = []
    priority: Literal["high","medium","low"] | None = None

class ExtractedSkill(BaseModel):
    skill: str = Field(min_length=1)
    category: str = Field(min_length=1)
    matched_alias: str = Field(min_length=1)
    evidence: str = Field(min_length=1)
    weight: int = Field(ge=1, le=3)

class UserProfile(BaseModel):
    name: str | None = None
    skills: list[str]

class MatchReport(BaseModel):
    score: float | None
    matched_skills: list[SkillMatch]
    missing_skills: list[SkillMatch]
