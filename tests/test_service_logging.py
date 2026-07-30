import logging

import job_analyzer.service as service
from job_analyzer.config import AppConfig

def test_logs_do_not_contain_full_job_text(
    tmp_path,
    monkeypatch,
    caplog,
) -> None:
    skills_path = tmp_path / "skills.yaml"
    profile_path = tmp_path / "profile.json"

    skills_path.write_text(
        "skills: []",
        encoding="utf-8",
    )
    profile_path.write_text(
        '{"skills": []}',
        encoding="utf-8",
    )

    config = AppConfig(
        skills_path=skills_path,
        profile_path=profile_path,
    )

    secret_text = (
        "TOP_SECRET_JOB_DESCRIPTION "
        "Python and SQL are required."
    )

    # Isolate subsequent business logic and only verify logs.
    monkeypatch.setattr(
        service,
        "extract_skill",
        lambda text, path: [],
    )
    monkeypatch.setattr(
        service,
        "load_profile",
        lambda path: object(),
    )
    monkeypatch.setattr(
        service,
        "score_skills",
        lambda skills, profile: object(),
    )

    caplog.set_level(
        logging.INFO,
        logger="job_analyzer.service",
    )

    service.analyze_job(
        config=config,
        text=secret_text,
    )

    assert secret_text not in caplog.text
    assert "TOP_SECRET_JOB_DESCRIPTION" not in caplog.text
    assert f"length={len(secret_text)}" in caplog.text
    assert "source=inline-text" in caplog.text