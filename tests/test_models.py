import pytest
from pydantic import ValidationError
from job_analyzer.models import JobDescription, SkillMatch
from job_analyzer.loader import read_from_file, read_text

def test_create_valid_job_description() -> None:
    job = JobDescription(
        title="AI engineer",
        raw_text="Python and SQL are required"
    )

    assert job.title == "AI engineer"

def test_job_description_rejects_blank_text() -> None:
    with pytest.raises(ValidationError):
        JobDescription(raw_text="   ")


def test_create_valid_skill_match() -> None:
    result = SkillMatch(
        skill="Python",
        category="programming",
        weight=1,
        matched=True,
        evidence=["Python experience required"]
    )

    assert result.matched is True


def test_skill_match_reject_empty_skill() -> None:
    with pytest.raises(ValidationError):
        SkillMatch(
            skill="",
            category="Programming",
            weight=1,
            matched=False)
        
