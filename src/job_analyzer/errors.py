class JobAnalyzerError(Exception):
    """All predictable project errors"""

    exit_code: int = 1

class InputError(JobAnalyzerError):
    """User invalid input"""

    exit_code: int = 2

class ConfigurationError(JobAnalyzerError):
    """Project configuration error"""

    exit_code: int = 3

class EmptyInputError(InputError):
    """Occupation description is Null"""

class InputFileNotFoundError(InputError):
    """Occupation SKills file is not found"""

class InputDecodeError(InputError):
    """Occupation skill file cannot be uncoded"""

class InvalidProfileError(ConfigurationError):
    """Profile.json with invalid content"""

class SkillDictionaryError(ConfigurationError):
    """Skill Dictionary content invalid"""
