"""
Code Validator - Unified Validation Framework

This module provides code validation functionality, inheriting from BaseValidator
and following the unified validation framework patterns.
"""

from typing import Dict, List, Any
from .base_validator import (
    BaseValidator,
    ValidationRule,
    ValidationResult,
    ValidationSeverity,
)
from .code_rule_evaluator import CodeRuleEvaluator
from .code_reporter import ValidationReporter


class CodeValidator(BaseValidator):
    """Validates code structure, syntax, and quality using unified validation framework"""

    def __init__(self):
        """Initialize code validator"""
        super().__init__("CodeValidator")
        self.code_standards = {
            "max_line_length": 120,
            "max_function_length": 50,
            "max_class_length": 500,
            "max_file_length": 400,
            "max_parameters": 7,
            "max_nesting_depth": 4,
        }

        self.python_keywords = [
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

        self.rule_evaluator = CodeRuleEvaluator(
            self, self.code_standards, self.python_keywords
        )
        self.reporter = ValidationReporter(self)

    def _setup_default_rules(self) -> None:
        """Setup default code validation rules"""
        default_rules = [
            ValidationRule(
                rule_id="code_structure",
                rule_name="Code Structure",
                rule_type="code",
                description="Validate code structure and syntax",
                severity=ValidationSeverity.ERROR,
            ),
            ValidationRule(
                rule_id="code_quality_validation",
                rule_name="Code Quality Validation",
                rule_type="code",
                description="Validate code quality and standards",
                severity=ValidationSeverity.WARNING,
            ),
            ValidationRule(
                rule_id="naming_convention_validation",
                rule_name="Naming Convention Validation",
                rule_type="code",
                description="Validate naming conventions and standards",
                severity=ValidationSeverity.WARNING,
            ),
            ValidationRule(
                rule_id="complexity_validation",
                rule_name="Complexity Validation",
                rule_type="code",
                description="Validate code complexity and maintainability",
                severity=ValidationSeverity.WARNING,
            ),
        ]

        for rule in default_rules:
            self.add_validation_rule(rule)

    def validate(self, code_data: Dict[str, Any], **kwargs) -> List[ValidationResult]:
        """Validate code data and return validation results.

        Returns:
            List[ValidationResult]: Validation results produced during code
            validation.
        """
        results: List[ValidationResult] = []

        try:
            structure_results = self.rule_evaluator.validate_code_structure(code_data)
            results.extend(structure_results)

            required_fields = ["file_path", "content", "language"]
            field_results = self._validate_required_fields(code_data, required_fields)
            results.extend(field_results)

            if "content" in code_data:
                results.extend(
                    self.rule_evaluator.validate_code_content(
                        code_data["content"], code_data.get("language")
                    )
                )

            if "metrics" in code_data:
                results.extend(
                    self.rule_evaluator.validate_code_metrics(code_data["metrics"])
                )

            if "naming" in code_data:
                results.extend(
                    self.rule_evaluator.validate_naming_conventions(
                        code_data["naming"]
                    )
                )

            if "complexity" in code_data:
                results.extend(
                    self.rule_evaluator.validate_code_complexity(
                        code_data["complexity"]
                    )
                )

            self.reporter.finalize(results)

        except Exception as e:
            results.append(self.reporter.report_error(e))

        return results


    def set_code_standard(self, standard_name: str, value: float) -> bool:
        """Set a custom code standard threshold"""
        try:
            if standard_name in self.code_standards:
                self.code_standards[standard_name] = value
                self.logger.info(f"Code standard updated: {standard_name} = {value}")
                return True
            else:
                self.logger.warning(f"Unknown code standard: {standard_name}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to set code standard: {e}")
            return False

    def get_code_standards(self) -> Dict[str, float]:
        """Get current code standards"""
        return self.code_standards.copy()

    # Code validation functionality integration (from duplicate ai_ml/validation.py)
    def validate_code_legacy(self, code: str) -> None:
        """Legacy code validation method (from duplicate ai_ml/validation.py)"""
        try:
            # Ensure the generated code looks plausible
            # The checks are intentionally lightweight: at the moment we only verify
            # that the code contains at least one function definition
            if "def " not in code:
                raise ValueError("Generated code must contain a function definition")

            # Additional lightweight checks can be added here without touching the orchestrating engine
            if len(code.strip()) == 0:
                raise ValueError("Generated code cannot be empty")

            # Check for basic Python syntax indicators
            if not any(
                keyword in code for keyword in ["def ", "class ", "import ", "from "]
            ):
                raise ValueError(
                    "Generated code should contain basic Python syntax elements"
                )

        except Exception as e:
            self.logger.error(f"Legacy code validation failed: {e}")
            raise

    def validate_code_with_legacy_fallback(self, code: str) -> Dict[str, Any]:
        """Validate code using both unified and legacy methods"""
        try:
            # Use unified validation first
            unified_results = self.validate({"code": code})

            # Use legacy validation as fallback
            legacy_valid = True
            legacy_message = "Code validation passed"
            try:
                self.validate_code_legacy(code)
            except Exception as e:
                legacy_valid = False
                legacy_message = str(e)

            return {
                "unified_validation": {
                    "total": len(unified_results),
                    "passed": len(
                        [r for r in unified_results if r.status.value == "passed"]
                    ),
                    "failed": len(
                        [r for r in unified_results if r.status.value == "failed"]
                    ),
                    "warnings": len(
                        [r for r in unified_results if r.severity.value == "warning"]
                    ),
                    "results": unified_results,
                },
                "legacy_validation": {"valid": legacy_valid, "message": legacy_message},
                "overall_valid": legacy_valid
                and len([r for r in unified_results if r.status.value == "failed"])
                == 0,
                "timestamp": self._get_current_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Code validation failed: {e}")
            return {
                "error": str(e),
                "overall_valid": False,
                "timestamp": self._get_current_timestamp(),
            }

    def get_code_validation_summary(self, code: str) -> Dict[str, Any]:
        """Get comprehensive code validation summary"""
        try:
            validation_result = self.validate_code_with_legacy_fallback(code)

            # Add code statistics
            code_stats = {
                "total_lines": len(code.split("\n")),
                "total_characters": len(code),
                "function_count": code.count("def "),
                "class_count": code.count("class "),
                "import_count": code.count("import ") + code.count("from "),
                "comment_lines": len(
                    [line for line in code.split("\n") if line.strip().startswith("#")]
                ),
                "empty_lines": len(
                    [line for line in code.split("\n") if line.strip() == ""]
                ),
            }

            validation_result["code_statistics"] = code_stats

            return validation_result

        except Exception as e:
            self.logger.error(f"Failed to get code validation summary: {e}")
            return {"error": str(e)}

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime

        return datetime.now().isoformat()
