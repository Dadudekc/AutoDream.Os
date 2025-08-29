"""Content rule evaluation logic."""

import ast
import re
from typing import Any, Dict, List

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)
from .code_parser import CodeParser


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
        self.parser = CodeParser()

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
            results.extend(self._validate_python_content(content))

        results.extend(self._validate_line_lengths(content))

        return results

    # ---------------------------- python specific ---------------------------
    def _validate_python_content(self, content: str) -> List[ValidationResult]:
        """Validate Python code by parsing and applying AST based checks."""
        results: List[ValidationResult] = []
        try:
            tree = self.parser.parse_python(content)
            results.extend(self._validate_python_imports(tree))
            results.extend(self._validate_python_functions(tree))
            results.extend(self._validate_python_classes(tree))
            results.extend(self._validate_python_naming(tree))
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
        except Exception as e:
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

    def _validate_python_imports(self, tree: ast.AST) -> List[ValidationResult]:
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

    def _validate_python_functions(self, tree: ast.AST) -> List[ValidationResult]:
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

    def _validate_python_classes(self, tree: ast.AST) -> List[ValidationResult]:
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
                            f"Class name '{node.name}' should follow PascalCase convention"
                        ),
                        field_path="classes",
                        actual_value=node.name,
                        expected_value="PascalCase naming",
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
                            message=f"Class '{node.name}' is {class_length} lines long",
                            field_path="classes",
                            actual_value=class_length,
                            expected_value=(
                                f"<= {self.code_standards['max_class_length']} lines"
                            ),
                        )
                        results.append(result)
        return results

    def _validate_python_naming(self, tree: ast.AST) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if not re.match(r"^[a-z_][a-z0-9_]*$", node.id):
                    if node.id not in self.python_keywords and not node.id.startswith(
                        "__"
                    ):
                        result = self.validator._create_result(
                            rule_id="variable_naming_convention",
                            rule_name="Variable Naming Convention",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=(
                                f"Variable name '{node.id}' should follow snake_case convention"
                            ),
                            field_path="naming",
                            actual_value=node.id,
                            expected_value="snake_case naming",
                        )
                        results.append(result)
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
