from job_analyzer.extractor import extract_skill, contains_alias

def test_detect_python_sql_and_ml() -> None:
    text = (
        "We need Python, SQL and machine learning "
        "experience."
    )

    results = extract_skill(
        text=text,
        file_path="data/skills.yaml",
    )

    skill_names = {
        result.skill
        for result in results
    }

    assert "Python" in skill_names
    assert "SQL" in skill_names
    assert "Machine Learning" in skill_names

def test_does_not_match_r_inside_required() -> None:
    assert contains_alias(
        "Communication skills are required.",
        "R",
    ) is False


def test_matches_standalone_r() -> None:
    assert contains_alias(
        "Experience with R is required.",
        "R",
    ) is True


def test_result_contains_evidence() -> None:
    text = "Strong Python experience is required."

    results = extract_skill(
        text=text,
        file_path="data/skills.yaml",
    )

    python_result = next(
        result
        for result in results
        if result.skill == "Python"
    )

    assert python_result.evidence == text