"""Content rule evaluation logic."""

from typing import Any, Dict, List

from .ast_parser import ASTParser
from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


class ContentRuleEvaluator:
    """Evaluates code content against various rules."""

    def __init__(
        self,
        validator: BaseValidator,
        code_standards: Dict[str, float],
        python_keywords: List[str],
    ) -> None:
        self.validator = validator
        self.code_standards = code_standards
        self.python_keywords = python_keywords
        self.ast_parser = ASTParser(validator, code_standards, python_keywords)

    def validate(self, content: Any, language: str = None) -> List[ValidationResult]:
        """Validate code content."""
        results: List[ValidationResult] = []

        if not isinstance(content, str):
            result = self.validator._create_result(
                rule_id="content_type",
                rule_name="Content Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Code content must be a string",
                field_path="content",
                actual_value=type(content).__name__,
                expected_value="str",
            )
            results.append(result)
            return results

        if len(content) == 0:
            result = self.validator._create_result(
                rule_id="content_empty",
                rule_name="Content Empty Check",
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.WARNING,
                message="Code content is empty",
                field_path="content",
                actual_value=content,
                expected_value="non-empty code content",
            )
            results.append(result)
            return results

        if language and language.lower() in ["python", "py"]:
            results.extend(self.ast_parser.validate(content))

        results.extend(self._validate_line_lengths(content))

        return results

    def _validate_line_lengths(self, content: str) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if len(line) > self.code_standards["max_line_length"]:
                result = self.validator._create_result(
                    rule_id="line_too_long",
                    rule_name="Line Too Long",
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.WARNING,
                    message=f"Line {i} is {len(line)} characters long",
                    field_path="content",
                    actual_value=f"line {i}: {len(line)} chars",
                    expected_value=(
                        f"<= {self.code_standards['max_line_length']} characters"
                    ),
                )
                results.append(result)
        return results
