from collections.abc import Sequence
import logging
import sys
from job_analyzer.__main__ import build_parser
from job_analyzer.config import build_config
from job_analyzer.errors import JobAnalyzerError
from job_analyzer.logging_config import configure_logging
from job_analyzer.service import analyze_job

logger = logging.getLogger(__name__)

def run(
    argv: Sequence[str] | None = None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    configure_logging(args.log_level.upper())

    try:
        config = build_config(
            skills_path=args.skills,
            profile_path=args.profile,
            log_level=args.log_level,
        )

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
            "Error: 程序发生内部错误",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(run())