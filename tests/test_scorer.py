from job_analyzer.scorer import score_skills
from job_analyzer.models import ExtractedSkill, UserProfile


def make_job_skill(
    skill: str,
    weight: int = 1,
    category: str = "programming_language",
) -> ExtractedSkill:
    return ExtractedSkill(
        skill=skill,
        category=category,
        matched_alias=skill.casefold(),
        evidence=f"{skill} is required.",
        weight=weight,
    )


def test_all_skills_matched_returns_full_score() -> None:
    job_skills = [
        make_job_skill("Python", weight=2),
        make_job_skill("SQL", weight=1, category="database"),
    ]
    profile = UserProfile(skills=["Python", "SQL"])

    report = score_skills(job_skills, profile)

    assert report.score == 100
    assert len(report.matched_skills) == 2
    assert report.missing_skills == []
    assert all(skill.matched for skill in report.matched_skills)


def test_all_skills_mismatched_returns_zero_score() -> None:
    job_skills = [
        make_job_skill("Python", weight=2),
        make_job_skill("SQL", weight=1, category="database"),
    ]
    profile = UserProfile(skills=["JavaScript", "HTML"])

    report = score_skills(job_skills, profile)

    assert report.score == 0
    assert report.matched_skills == []
    assert len(report.missing_skills) == 2
    assert all(not skill.matched for skill in report.missing_skills)


def test_repeated_skills_are_counted_once() -> None:
    job_skills = [
        make_job_skill("Python", weight=1),
        make_job_skill("Python", weight=3),
        make_job_skill("SQL", weight=1, category="database"),
    ]
    profile = UserProfile(skills=["Python"])

    report = score_skills(job_skills, profile)

    assert report.score == 75
    assert [skill.skill for skill in report.matched_skills] == ["Python"]
    assert [skill.skill for skill in report.missing_skills] == ["SQL"]
    assert report.matched_skills[0].weight == 3


def test_same_input_has_same_score() -> None:
    job_skills = [
        make_job_skill("Python", weight=2),
        make_job_skill("SQL", weight=1, category="database"),
    ]
    profile = UserProfile(skills=["Python"])

    first_report = score_skills(job_skills, profile)
    second_report = score_skills(job_skills, profile)

    assert first_report.score == second_report.score
