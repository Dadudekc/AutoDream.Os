"""Default code validation rules and standards."""

from typing import Dict, List


CODE_STANDARDS: Dict[str, int] = {
    "max_line_length": 120,
    "max_function_length": 50,
    "max_class_length": 500,
    "max_file_length": 400,
    "max_parameters": 7,
    "max_nesting_depth": 4,
}

PYTHON_KEYWORDS: List[str] = [
    "False",
    "None",
    "True",
    "and",
    "as",
    "assert",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
]


def get_code_standards() -> Dict[str, int]:
    """Return a copy of default code standards."""
    return CODE_STANDARDS.copy()


def get_python_keywords() -> List[str]:
    """Return list of Python keywords used by validations."""
    return list(PYTHON_KEYWORDS)


__all__ = ["get_code_standards", "get_python_keywords", "CODE_STANDARDS", "PYTHON_KEYWORDS"]
