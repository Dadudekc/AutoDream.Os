#!/usr/bin/env python3
"""AIDebuggerAssistant module.

Provides basic debugging suggestions and error pattern recognition.
This lightweight implementation is enough for unit tests and serves as
an example of how intelligent debugging helpers could be structured.
"""

from typing import List


class AIDebuggerAssistant:
    """Simple rule-based debugging assistant."""

    _PATTERNS = {
        "NameError": "undefined_variable",
        "TypeError": "type_mismatch",
        "SyntaxError": "syntax_error",
    }

    _SUGGESTIONS = {
        "undefined_variable": [
            "Check for misspelled variable names",
            "Ensure variables are defined before use",
        ],
        "type_mismatch": [
            "Verify variable types and conversions",
            "Use type casting where appropriate",
        ],
        "syntax_error": [
            "Review Python syntax near the reported line",
            "Ensure brackets and quotes are balanced",
        ],
        "unknown": [
            "Review the stack trace for more details",
        ],
    }

    def analyze_error(self, error_message: str) -> str:
        """Return a simple classification for a given error message."""
        for key, label in self._PATTERNS.items():
            if key in error_message:
                return label
        return "unknown"

    def suggest_fixes(self, error_message: str) -> List[str]:
        """Provide debugging suggestions based on the error message."""
        pattern = self.analyze_error(error_message)
        return self._SUGGESTIONS.get(pattern, self._SUGGESTIONS["unknown"])


__all__ = ["AIDebuggerAssistant"]
