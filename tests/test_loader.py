import pytest

from job_analyzer.loader import (
    EmptyInputError,
    InputFileNotFoundError,
    read_from_file,
    read_text,
)


def test_load_from_text() -> None:
    result = read_text("Python and SQL")

    assert result == "Python and SQL"


def test_empty_text_fails() -> None:
    with pytest.raises(EmptyInputError):
        read_text("")


def test_load_from_file(tmp_path) -> None:
    file_path = tmp_path / "job.txt"
    file_path.write_text(
        "Python and SQL",
        encoding="utf-8",
    )

    result = read_from_file(str(file_path))

    assert result == "Python and SQL"


def test_missing_file_fails() -> None:
    with pytest.raises(InputFileNotFoundError):
        read_from_file("missing-job.txt")


def test_empty_file_fails(tmp_path) -> None:
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(EmptyInputError):
        read_from_file(str(file_path))