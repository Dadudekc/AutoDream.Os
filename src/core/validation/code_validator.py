"""
Code Validator - Unified Validation Framework

Thin coordinator that delegates rule evaluation,
AST parsing and reporting to dedicated modules.
"""

from typing import Any, Dict, List

from .base_validator import BaseValidator, ValidationResult
from .code_reporter import CodeReporter
from .code_rule_evaluator import CodeRuleEvaluator
from .code_rules import get_code_standards, get_python_keywords


class CodeValidator(BaseValidator):
    """Validate source code using modular rule evaluators."""

    def __init__(self) -> None:
        super().__init__("CodeValidator")
        self.code_standards = get_code_standards()
        self.python_keywords = get_python_keywords()
        self.rules = CodeRuleEvaluator(
            self, self.code_standards, self.python_keywords
        )
        self.reporter = CodeReporter(self)

    def validate(self, code_data: Dict[str, Any], **kwargs) -> List[ValidationResult]:
        """Coordinate validation of provided code data."""
        results: List[ValidationResult] = []
        try:
            results.extend(self.rules.validate_code_structure(code_data))

            if "content" in code_data:
                results.extend(
                    self.rules.validate_code_content(
                        code_data["content"], code_data.get("language")
                    )
                )

            if "metrics" in code_data:
                results.extend(self.rules.validate_code_metrics(code_data["metrics"]))

            if "naming" in code_data:
                results.extend(
                    self.rules.validate_naming_conventions(code_data["naming"])
                )

            if "complexity" in code_data:
                results.extend(
                    self.rules.validate_code_complexity(code_data["complexity"])
                )

            self.reporter.finalize(results)
        except Exception as exc:  # pragma: no cover - safety net
            results.append(self.reporter.report_error(exc))
        return results

    # ------------------------------------------------------------------
    # Legacy compatibility helpers
    def validate_code_legacy(self, *args, **kwargs) -> List[ValidationResult]:
        return self.validate(*args, **kwargs)

    def validate_code_with_legacy_fallback(
        self, *args, **kwargs
    ) -> List[ValidationResult]:
        return self.validate(*args, **kwargs)


__all__ = ["CodeValidator"]
