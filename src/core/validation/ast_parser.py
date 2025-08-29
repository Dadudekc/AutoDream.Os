"""AST parsing and inspection utilities for code validation."""

from __future__ import annotations

import ast
import re
from typing import Dict, List

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


class ASTParser:
    """Parse source code and apply AST-based validations."""

    def __init__(
        self,
        validator: BaseValidator,
        code_standards: Dict[str, float],
        python_keywords: List[str],
    ) -> None:
        self.validator = validator
        self.code_standards = code_standards
        self.python_keywords = python_keywords

    # ------------------------------------------------------------------
    def validate(self, content: str) -> List[ValidationResult]:
        """Validate Python code by parsing and applying AST based checks."""
        results: List[ValidationResult] = []
        try:
            tree = ast.parse(content)
            results.extend(self._validate_imports(tree))
            results.extend(self._validate_functions(tree))
            results.extend(self._validate_classes(tree))
            results.extend(self._validate_naming(tree))
        except SyntaxError as e:
            result = self.validator._create_result(
                rule_id="python_syntax_error",
                rule_name="Python Syntax Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Python syntax error: {str(e)}",
                field_path="content",
                actual_value=f"line {e.lineno}: {e.text}",
                expected_value="valid Python syntax",
            )
            results.append(result)
        except Exception as e:  # pragma: no cover - safety net
            result = self.validator._create_result(
                rule_id="python_parsing_error",
                rule_name="Python Parsing Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Python parsing error: {str(e)}",
                field_path="content",
                actual_value=str(e),
                expected_value="parseable Python code",
            )
            results.append(result)
        return results

    # ------------------------------------------------------------------
    def _validate_imports(self, tree: ast.AST) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in self.python_keywords:
                        result = self.validator._create_result(
                            rule_id="import_keyword_conflict",
                            rule_name="Import Keyword Conflict",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=(
                                f"Import name '{alias.name}' conflicts with Python keyword"
                            ),
                            field_path="imports",
                            actual_value=alias.name,
                            expected_value="non-keyword import name",
                        )
                        results.append(result)
            elif isinstance(node, ast.ImportFrom):
                if node.module in self.python_keywords:
                    result = self.validator._create_result(
                        rule_id="from_import_keyword_conflict",
                        rule_name="From Import Keyword Conflict",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=(
                            f"From import module '{node.module}' conflicts with Python keyword"
                        ),
                        field_path="imports",
                        actual_value=node.module,
                        expected_value="non-keyword module name",
                    )
                    results.append(result)
        return results

    # ------------------------------------------------------------------
    def _validate_functions(self, tree: ast.AST) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r"^[a-z_][a-z0-9_]*$", node.name):
                    result = self.validator._create_result(
                        rule_id="function_naming_convention",
                        rule_name="Function Naming Convention",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=(
                            f"Function name '{node.name}' should follow snake_case convention"
                        ),
                        field_path="functions",
                        actual_value=node.name,
                        expected_value="snake_case naming",
                    )
                    results.append(result)
                if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
                    function_length = node.end_lineno - node.lineno + 1
                    if function_length > self.code_standards["max_function_length"]:
                        result = self.validator._create_result(
                            rule_id="function_too_long",
                            rule_name="Function Too Long",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=(
                                f"Function '{node.name}' is {function_length} lines long"
                            ),
                            field_path="functions",
                            actual_value=function_length,
                            expected_value=(
                                f"<= {self.code_standards['max_function_length']} lines"
                            ),
                        )
                        results.append(result)
                if len(node.args.args) > self.code_standards["max_parameters"]:
                    result = self.validator._create_result(
                        rule_id="function_too_many_parameters",
                        rule_name="Function Too Many Parameters",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=(
                            f"Function '{node.name}' has {len(node.args.args)} parameters"
                        ),
                        field_path="functions",
                        actual_value=len(node.args.args),
                        expected_value=(
                            f"<= {self.code_standards['max_parameters']} parameters"
                        ),
                    )
                    results.append(result)
        return results

    # ------------------------------------------------------------------
    def _validate_classes(self, tree: ast.AST) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not re.match(r"^[A-Z][a-zA-Z0-9]*$", node.name):
                    result = self.validator._create_result(
                        rule_id="class_naming_convention",
                        rule_name="Class Naming Convention",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=(
                            f"Class name '{node.name}' should use CapWords convention"
                        ),
                        field_path="classes",
                        actual_value=node.name,
                        expected_value="CapWords naming",
                    )
                    results.append(result)
                if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
                    class_length = node.end_lineno - node.lineno + 1
                    if class_length > self.code_standards["max_class_length"]:
                        result = self.validator._create_result(
                            rule_id="class_too_long",
                            rule_name="Class Too Long",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=(
                                f"Class '{node.name}' is {class_length} lines long"
                            ),
                            field_path="classes",
                            actual_value=class_length,
                            expected_value=(
                                f"<= {self.code_standards['max_class_length']} lines"
                            ),
                        )
                        results.append(result)
        return results

    # ------------------------------------------------------------------
    def _validate_naming(self, tree: ast.AST) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if node.id in self.python_keywords:
                    result = self.validator._create_result(
                        rule_id="variable_keyword_conflict",
                        rule_name="Variable Keyword Conflict",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=(
                            f"Variable name '{node.id}' conflicts with Python keyword"
                        ),
                        field_path="variables",
                        actual_value=node.id,
                        expected_value="non-keyword variable name",
                    )
                    results.append(result)
        return results


__all__ = ["ASTParser"]
