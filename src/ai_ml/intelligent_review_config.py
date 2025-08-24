"""Configuration for the Intelligent Reviewer modules."""

# Security vulnerability patterns used during analysis
SECURITY_PATTERNS = {
    "sql_injection": [
        r"execute\s*\(\s*[\"'].*\+\s*\w+",
        r"cursor\.execute\s*\(\s*[\"'].*\+\s*\w+",
        r"\.execute\s*\(\s*[\"'].*\+\s*\w+",
    ],
    "xss": [
        r"innerHTML\s*=",
        r"document\.write\s*\(",
        r"eval\s*\(",
        r"setTimeout\s*\(\s*[\"'].*\+\s*\w+",
    ],
    "path_traversal": [
        r"open\s*\(\s*[\"'].*\+\s*\w+",
        r"file\s*\(\s*[\"'].*\+\s*\w+",
        r"Path\s*\(\s*[\"'].*\+\s*\w+",
    ],
    "command_injection": [
        r"os\.system\s*\(",
        r"subprocess\.run\s*\(",
        r"subprocess\.Popen\s*\(",
        r"subprocess\.call\s*\(",
    ],
}

# Generic code quality patterns
QUALITY_PATTERNS = {
    "long_function": r"def\s+\w+\s*\([^)]*\):\s*\n(?:[^\n]*\n){20,}",
    "magic_numbers": r"\b\d{3,}\b",
    "hardcoded_strings": r"[\"'][^\"']{50,}[\"']",
    "nested_loops": r"for\s+.*:\s*\n\s*for\s+.*:",
    "complex_conditionals": r"if\s+.*\sand\s+.*\sand\s+.*:",
}

__all__ = ["SECURITY_PATTERNS", "QUALITY_PATTERNS"]
