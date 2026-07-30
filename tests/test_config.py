import pytest

from job_analyzer.config import build_config
from job_analyzer.errors import ConfigurationError

def test_build_valid_config(tmp_path) -> None:
    skills_path = tmp_path / "skills.yaml"
    profile_path = tmp_path / "profile.json"

    skills_path.write_text(
        "skills: []",
        encoding="utf-8"
    )

    profile_path.write_text(
        '{"skills": []}',
        encoding="utf-8"
    )

    config = build_config(
        skills_path=skills_path,
        profile_path=profile_path,
        log_level="info"
    )

    assert config.skills_path == skills_path
    assert config.profile_path == profile_path
    assert config.log_level == "INFO"

def test_skills_path_can_be_replaced(tmp_path) -> None:
    custome_skills_path = tmp_path / "custom-skills.yaml"
    profile_path = tmp_path / "profile.json"

    custome_skills_path.write_text(
        "skills: []",
        encoding="utf-8"
    )

    profile_path.write_text(
        '{"skills": []}'
    )

    config = build_config(
        skills_path=custome_skills_path,
        profile_path=profile_path
    )

    assert config.skills_path == custome_skills_path

def test_missing_skills_file_raises_config_error(tmp_path) -> None:
    profile_path = tmp_path / "profile.json"

    profile_path.write_text(
        '{"skills": []}'
    )

    with pytest.raises(
        ConfigurationError,
        match="Cannot find skill dictionary"
    ):
        build_config(
            skills_path= tmp_path / "missing.yaml",
            profile_path=profile_path
        )

def test_invalid_log_level_raises_config_error(
    tmp_path,
) -> None:
    skills_path = tmp_path / "skills.yaml"
    profile_path = tmp_path / "profile.json"

    skills_path.write_text("skills: []", encoding="utf-8")
    profile_path.write_text('{"skills": []}', encoding="utf-8")

    with pytest.raises(ConfigurationError):
        build_config(
            skills_path=skills_path,
            profile_path=profile_path,
            log_level="wrong-level",
        )