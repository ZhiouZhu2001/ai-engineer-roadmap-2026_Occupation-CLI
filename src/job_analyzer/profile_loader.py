import json
from pathlib import Path

from pydantic import ValidationError

from job_analyzer.errors import InvalidProfileError
from job_analyzer.models import UserProfile

def load_profile(
        file_path: str | Path
) -> UserProfile:
    path = Path(file_path)

    try:
        raw_content = path.read_text(encoding="utf-8")
    except OSError as error:
        raise InvalidProfileError(
            f"Cannot read user profile: {path}"
        ) from error
    
    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as error:
        raise InvalidProfileError (
        f"User profile data is not valid JSON {path}"
    ) from error

    try:
        return UserProfile.model_validate(data)
    except ValidationError as error:
        raise InvalidProfileError(
            f"User parameter is not valid: {path}"
        ) from error