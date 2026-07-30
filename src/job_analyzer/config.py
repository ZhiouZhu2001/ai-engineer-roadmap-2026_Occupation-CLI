from dataclasses import dataclass
from pathlib import Path

from job_analyzer.errors import ConfigurationError

@dataclass(frozen=True, slots=True)
class AppConfig:
    skills_path: Path
    profile_path: Path
    log_level: str = "INFO"

def build_config(
        *,
        skills_path: Path,
        profile_path: Path,
        log_level: str = "INFO"
) -> AppConfig:
    """test and create application configuration"""

    resolved_skills_path = Path(skills_path)
    resolved_profile_path = Path(profile_path)
    normalized_log_level = log_level.upper()

    valid_log_levels = {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL"
    }

    if normalized_log_level not in valid_log_levels:
        raise ConfigurationError(
            f"Abnormal log level: {log_level}"
        )

    if not resolved_skills_path.is_file():
        raise ConfigurationError(
            f"Cannot find skill dictionary: {resolved_skills_path}"
        )
    
    if not resolved_profile_path.is_file():
        raise ConfigurationError(
            f"Cannot find user data: {resolved_profile_path}"
        )
    
    return AppConfig(
        skills_path=resolved_skills_path,
        profile_path=resolved_profile_path,
        log_level=normalized_log_level
    )