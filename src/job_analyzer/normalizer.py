import re
import unicodedata


def normalize_data(text: str) -> str:
    """Make all text have same and stable format"""

    normalized = unicodedata.normalize("NFKC", text)

    # Uppercase and Lowercase unified
    normalized = normalized.casefold()

    # Consecutive spaces, newlines, and tabs are merged into a single space.
    normalized = re.sub(r"\s+", " ", normalized).strip()


    return normalized


