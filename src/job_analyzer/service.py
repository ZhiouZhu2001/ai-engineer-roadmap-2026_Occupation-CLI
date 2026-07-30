import logging
import time
from pathlib import Path

from job_analyzer.config import AppConfig
from job_analyzer.extractor import extract_skill
from job_analyzer.loader import (
    read_from_file,
    read_text
)
from job_analyzer.models import MatchReport
from job_analyzer.normalizer import normalize_data
from job_analyzer.profile_loader import load_profile
from job_analyzer.scorer import score_skills

logger = logging.getLogger(__name__)

def analyze_job(
    *,
    config: AppConfig,
    file_path: str | Path | None = None,
    text: str | None = None
) -> MatchReport:
    """Execute Occupation read, skills """

    started_at = time.perf_counter()

    source = (
        str(file_path)
        if file_path is not None
        else "inline-text"
    )
    
    try:
        if file_path is not None:
            raw_text = read_from_file(str(file_path))
        else:
            raw_text = read_text(text or "")

        logger.info(
            "input_loaded source=%s length=%d",
            source,
            len(raw_text),
        )

        normalize_text = normalize_data(raw_text)

        job_skills = extract_skill(
            normalize_text, 
            config.skills_path,
        )

        profile = load_profile(config.profile_path)

        report = score_skills(
            job_skills,
            profile,
        )

        duration_ms = (
            time.perf_counter() - started_at
        ) * 1000

        logger.info(
            (
                "analysis_completed "
                "source=%s "
                "skill_count=%d "
                "duration_ms=%.2f"
            ),
            source,
            len(job_skills),
            duration_ms,
        )

        return report
    
    except Exception as error:
        duration_ms = (
            time.perf_counter() - started_at
        ) * 1000

        logger.error(
            (
                "analysis_failed "
                "source=%s "
                "error_type=%s "
                "duration_ms=%.2f"
            ),
            source,
            type(error).__name__,
            duration_ms,
        )

        raise
