from job_analyzer.errors import (
    EmptyInputError,
    InputFileNotFoundError,
    InputDecodeError,
    InputError
)


from pathlib import Path
from typing import Any
import yaml

def read_text(text: str) -> str:
    """Read user input text"""
    if not text or not text.strip():
        raise EmptyInputError("input text cannot be blank")
    return text

def read_from_file(file_path:str) -> str:
    """Read user input file"""
    path = Path(file_path)

    if not path.exists():
        raise InputFileNotFoundError(f"No file has been detected in path {file_path}")
    
    if not path.is_file():
        raise InputFileNotFoundError(f"Input path has no file detected {file_path}")

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise InputDecodeError(
            f"cannot read file with decode utf-8: {file_path}"
        ) from error

    if not text.strip():
        raise EmptyInputError(
            f"File dosen't containt content {file_path}"
        )
    
    return text


