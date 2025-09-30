"""
Vibe Check Pattern Detectors - Pattern detection logic for vibe check.
"""

from .design_authority import DecisionSeverity
from .vibe_check_models import VibeViolation


class VibePatternDetector:
    """Detects patterns and anti-patterns in code."""

    def check_duplication(self, file_path: str, content: str) -> list[VibeViolation]:
        """Check for code duplication (simplified version)."""
        violations = []
        lines = [line.strip() for line in content.split("\n") if line.strip()]

        line_counts = {}
        for line in lines:
            if len(line) > 20:  # Only check substantial lines
                line_counts[line] = line_counts.get(line, 0) + 1

        for line, count in line_counts.items():
            if count > 3:  # Same line appears more than 3 times
                violations.append(
                    VibeViolation(
                        file_path=file_path,
                        line_number=0,
                        violation_type="duplication",
                        description=f"Line appears {count} times: '{line[:50]}...'",
                        severity=DecisionSeverity.WARNING,
                        suggestion="Extract into a function or constant",
                    )
                )

        return violations

    def check_anti_patterns(self, file_path: str, content: str) -> list[VibeViolation]:
        """Check for common anti-patterns."""
        violations = []
        content_lower = content.lower()

        anti_patterns = {
            "bare_except": ("except:", "Use specific exception types"),
            "global_vars": ("global ", "Avoid global variables"),
            "deep_copy": ("copy.deepcopy", "Consider if deep copy is necessary"),
            "eval_usage": ("eval(", "Avoid eval() for security"),
            "exec_usage": ("exec(", "Avoid exec() for security"),
            "complex_list_comp": ("[", "Simplify nested list comprehensions"),
        }

        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            for pattern_name, (pattern, suggestion) in anti_patterns.items():
                if pattern in line.lower():
                    violations.append(
                        VibeViolation(
                            file_path=file_path,
                            line_number=i,
                            violation_type=f"anti_pattern_{pattern_name}",
                            description=f"Anti-pattern detected: {pattern_name}",
                            severity=DecisionSeverity.WARNING,
                            suggestion=suggestion,
                            code_snippet=line.strip(),
                        )
                    )

        return violations
