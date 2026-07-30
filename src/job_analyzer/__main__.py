import argparse
import logging
import os
import sys
from collections.abc import Sequence

from job_analyzer.config import build_config
from job_analyzer.errors import JobAnalyzerError
from job_analyzer.logging_config import configure_logging
from job_analyzer.service import analyze_job

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze a job description"
    )

    input_group = parser.add_mutually_exclusive_group(
        required=True
    )

    input_group.add_argument(
        "--file",
        help="Introduce path of file"
    )

    input_group.add_argument(
        "--text",
        help="Write input of occupation"
    )

    parser.add_argument(
        "--skills",
        default=os.getenv(
            "JOB_ANALYZER_SKILLS_PATH",
            "data/skills.yaml",
        ),
        help="Skill yaml file path",
    )

    parser.add_argument(
        "--profile",
        default=os.getenv(
            "JOB_ANALYZER_PROFILE_PATH",
            "data/profile.json",
        ),
        help="self skill json file path",
    )

    parser.add_argument(
        "--log-level",
        default=os.getenv(
            "JOB_ANALYZER_LOG_LEVEL",
            "INFO",
        ),
        help="DEBUG, INFO, WARNING, ERROR, or CRITICAL",
    )

    return parser


def run(
    argv: Sequence[str] | None = None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = build_config(
            skills_path=args.skills,
            profile_path=args.profile,
            log_level=args.log_level,
        )

        configure_logging(config.log_level)

        report = analyze_job(
            config=config,
            file_path=args.file,
            text=args.text,
        )

        print(report.model_dump_json(indent=2))

        return 0

    except JobAnalyzerError as error:
        logger.warning(
            "request_failed error_type=%s",
            type(error).__name__,
        )

        print(
            f"Error: {error}",
            file=sys.stderr,
        )

        return error.exit_code

    except Exception as error:
        logger.error(
            "request_failed error_type=%s",
            type(error).__name__,
        )

        print(
            "Error: Program got internal error",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(run())
