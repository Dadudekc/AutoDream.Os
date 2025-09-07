
# MIGRATED: This file has been migrated to the centralized configuration system
"""Single source of truth for data pipeline configuration."""

from typing import Dict

DEFAULT_DB_PATH: str = "agent_responses.db"

RESPONSE_PATTERNS: Dict[str, str] = {
    "code_file": r"\.py$|\.js$|\.ts$|\.java$|\.cpp$|\.h$",
    "documentation": r"\.md$|\.txt$|\.rst$|\.docx?$",
    "data_file": r"\.json$|\.xml$|\.csv$|\.yaml$|\.yml$",
    "image_file": r"\.png$|\.jpg$|\.jpeg$|\.gif$|\.svg$",
    "log_file": r"\.log$|\.out$|\.err$",
}

AGENT_ASSIGNMENTS: Dict[str, str] = {
    "debug": "Agent-4",
    "implementation": "Agent-1",
    "optimization": "Agent-3",
    "testing": "Agent-2",
}
