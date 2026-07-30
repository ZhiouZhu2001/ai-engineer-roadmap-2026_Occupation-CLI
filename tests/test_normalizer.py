from job_analyzer.normalizer import normalize_data

def test_normalize_case() -> None:
    assert normalize_data("PYTHON") == "python"

def test_normalize_whitespace() -> None:
    text = "  Python \n\n and \t SQL"

    assert normalize_data(text) == "python and sql"

def test_normalize_full_width_characters() -> None:
    assert normalize_data("ＰＹＴＨＯＮ") == "python"