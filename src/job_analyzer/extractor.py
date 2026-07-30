import re
from pathlib import Path
from typing import Any
import yaml
from job_analyzer.models import ExtractedSkill

# Read skills from yaml
def load_skill_directory(file_path: str | Path) -> list[dict[str,Any]]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Did not detected skill file {file_path}")
    
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict) or "skills" not in data:
        raise ValueError("Skill Dict must have skills parameter")
    
    if not isinstance(data["skills"], list):
        raise ValueError("Skills must be a list")
    
    return data["skills"]

# Secure confution of alias
def contains_alias(text: str, alias: str) -> bool:
    pattern = re.compile(
        rf"(?<!\w){re.escape(alias)}(?!\w)",
        flags=re.IGNORECASE,
    )

    return pattern.search(text) is not None

# Return Evidence
def split_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?。！？])\s+|\n+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


# Extract skills
def extract_skill(
    text: str,
    file_path: str | Path
) -> list[ExtractedSkill]:
    skill_definitions = load_skill_directory(file_path)

    sentences = split_sentences(text)

    results: list[ExtractedSkill] = []

    for skill_definition in skill_definitions:
        canonical_name = skill_definition["canonical_name"]
        category = skill_definition["category"]
        aliases = skill_definition["aliases"]
        weight = skill_definition.get("weight", 1)

        skill_found = False

        for sentence in sentences:
            for alias in aliases:
                if contains_alias(sentence,alias):
                    results.append(
                        ExtractedSkill(
                            skill=canonical_name,
                            category=category,
                            matched_alias=alias,
                            evidence=sentence,
                            weight=weight,
                        )
                    )

                    skill_found = True
                    break
            if skill_found:
                break
    return results
