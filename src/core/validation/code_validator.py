"""
Code Validator - Unified Validation Framework

This module provides code validation functionality, inheriting from BaseValidator
and following the unified validation framework patterns.
"""

import ast
import re
from typing import Dict, List, Any, Optional
from .base_validator import (
    BaseValidator,
    ValidationRule,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


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
        results = []

        try:
            # Validate code data structure
            structure_results = self._validate_code_structure(code_data)
            results.extend(structure_results)

            # Validate required fields
            required_fields = ["file_path", "content", "language"]
            field_results = self._validate_required_fields(code_data, required_fields)
            results.extend(field_results)

            # Validate code content if present
            if "content" in code_data:
                content_results = self._validate_code_content(
                    code_data["content"], code_data.get("language")
                )
                results.extend(content_results)

            # Validate code metrics if present
            if "metrics" in code_data:
                metrics_results = self._validate_code_metrics(code_data["metrics"])
                results.extend(metrics_results)

            # Validate naming conventions if present
            if "naming" in code_data:
                naming_results = self._validate_naming_conventions(code_data["naming"])
                results.extend(naming_results)

            # Validate complexity if present
            if "complexity" in code_data:
                complexity_results = self._validate_code_complexity(
                    code_data["complexity"]
                )
                results.extend(complexity_results)

            # Add overall success result if no critical errors
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                success_result = self._create_result(
                    rule_id="overall_code_validation",
                    rule_name="Overall Code Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Code validation passed successfully",
                    details={"total_checks": len(results)},
                )
                results.append(success_result)

        except Exception as e:
            error_result = self._create_result(
                rule_id="code_validation_error",
                rule_name="Code Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Code validation error: {str(e)}",
                details={"error_type": type(e).__name__},
            )
            results.append(error_result)

        return results

    def _validate_code_structure(
        self, code_data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate code data structure and format"""
        results = []

        if not isinstance(code_data, dict):
            result = self._create_result(
                rule_id="code_type",
                rule_name="Code Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Code data must be a dictionary",
                actual_value=type(code_data).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        if len(code_data) == 0:
            result = self._create_result(
                rule_id="code_empty",
                rule_name="Code Empty Check",
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.WARNING,
                message="Code data is empty",
                actual_value=code_data,
                expected_value="non-empty code data",
            )
            results.append(result)

        return results

    def _validate_code_content(
        self, content: Any, language: str = None
    ) -> List[ValidationResult]:
        """Validate code content"""
        results = []

        if not isinstance(content, str):
            result = self._create_result(
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
            result = self._create_result(
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

        # Validate Python code if language is Python
        if language and language.lower() in ["python", "py"]:
            python_results = self._validate_python_code(content)
            results.extend(python_results)

        # Validate line length
        line_length_results = self._validate_line_lengths(content)
        results.extend(line_length_results)

        return results

    def _validate_python_code(self, content: str) -> List[ValidationResult]:
        """Validate Python code syntax and structure"""
        results = []

        try:
            # Parse Python code
            tree = ast.parse(content)

            # Validate imports
            import_results = self._validate_python_imports(tree)
            results.extend(import_results)

            # Validate functions
            function_results = self._validate_python_functions(tree)
            results.extend(function_results)

            # Validate classes
            class_results = self._validate_python_classes(tree)
            results.extend(class_results)

            # Validate naming conventions
            naming_results = self._validate_python_naming(tree)
            results.extend(naming_results)

        except SyntaxError as e:
            result = self._create_result(
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
            result = self._create_result(
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
        """Validate Python imports"""
        results = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                # Check import names
                for alias in node.names:
                    if alias.name in self.python_keywords:
                        result = self._create_result(
                            rule_id="import_keyword_conflict",
                            rule_name="Import Keyword Conflict",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=f"Import name '{alias.name}' conflicts with Python keyword",
                            field_path="imports",
                            actual_value=alias.name,
                            expected_value="non-keyword import name",
                        )
                        results.append(result)

            elif isinstance(node, ast.ImportFrom):
                # Check from imports
                if node.module in self.python_keywords:
                    result = self._create_result(
                        rule_id="from_import_keyword_conflict",
                        rule_name="From Import Keyword Conflict",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=f"From import module '{node.module}' conflicts with Python keyword",
                        field_path="imports",
                        actual_value=node.module,
                        expected_value="non-keyword module name",
                    )
                    results.append(result)

        return results

    def _validate_python_functions(self, tree: ast.AST) -> List[ValidationResult]:
        """Validate Python functions"""
        results = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check function name
                if not re.match(r"^[a-z_][a-z0-9_]*$", node.name):
                    result = self._create_result(
                        rule_id="function_naming_convention",
                        rule_name="Function Naming Convention",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=f"Function name '{node.name}' should follow snake_case convention",
                        field_path="functions",
                        actual_value=node.name,
                        expected_value="snake_case naming",
                    )
                    results.append(result)

                # Check function length
                if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
                    function_length = node.end_lineno - node.lineno + 1
                    if function_length > self.code_standards["max_function_length"]:
                        result = self._create_result(
                            rule_id="function_too_long",
                            rule_name="Function Too Long",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=f"Function '{node.name}' is {function_length} lines long",
                            field_path="functions",
                            actual_value=function_length,
                            expected_value=f"<= {self.code_standards['max_function_length']} lines",
                        )
                        results.append(result)

                # Check number of parameters
                if len(node.args.args) > self.code_standards["max_parameters"]:
                    result = self._create_result(
                        rule_id="function_too_many_parameters",
                        rule_name="Function Too Many Parameters",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=f"Function '{node.name}' has {len(node.args.args)} parameters",
                        field_path="functions",
                        actual_value=len(node.args.args),
                        expected_value=f"<= {self.code_standards['max_parameters']} parameters",
                    )
                    results.append(result)

        return results

    def _validate_python_classes(self, tree: ast.AST) -> List[ValidationResult]:
        """Validate Python classes"""
        results = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check class name
                if not re.match(r"^[A-Z][a-zA-Z0-9]*$", node.name):
                    result = self._create_result(
                        rule_id="class_naming_convention",
                        rule_name="Class Naming Convention",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=f"Class name '{node.name}' should follow PascalCase convention",
                        field_path="classes",
                        actual_value=node.name,
                        expected_value="PascalCase naming",
                    )
                    results.append(result)

                # Check class length
                if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
                    class_length = node.end_lineno - node.lineno + 1
                    if class_length > self.code_standards["max_class_length"]:
                        result = self._create_result(
                            rule_id="class_too_long",
                            rule_name="Class Too Long",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=f"Class '{node.name}' is {class_length} lines long",
                            field_path="classes",
                            actual_value=class_length,
                            expected_value=f"<= {self.code_standards['max_class_length']} lines",
                        )
                        results.append(result)

        return results

    def _validate_python_naming(self, tree: ast.AST) -> List[ValidationResult]:
        """Validate Python naming conventions"""
        results = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                # Check variable naming
                if not re.match(r"^[a-z_][a-z0-9_]*$", node.id):
                    # Skip if it's a built-in or imported name
                    if node.id not in self.python_keywords and not node.id.startswith(
                        "__"
                    ):
                        result = self._create_result(
                            rule_id="variable_naming_convention",
                            rule_name="Variable Naming Convention",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=f"Variable name '{node.id}' should follow snake_case convention",
                            field_path="naming",
                            actual_value=node.id,
                            expected_value="snake_case naming",
                        )
                        results.append(result)

        return results

    def _validate_line_lengths(self, content: str) -> List[ValidationResult]:
        """Validate line lengths"""
        results = []

        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if len(line) > self.code_standards["max_line_length"]:
                result = self._create_result(
                    rule_id="line_too_long",
                    rule_name="Line Too Long",
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.WARNING,
                    message=f"Line {i} is {len(line)} characters long",
                    field_path="content",
                    actual_value=f"line {i}: {len(line)} chars",
                    expected_value=f"<= {self.code_standards['max_line_length']} characters",
                )
                results.append(result)

        return results

    def _validate_code_metrics(self, metrics: Any) -> List[ValidationResult]:
        """Validate code metrics"""
        results = []

        if not isinstance(metrics, dict):
            result = self._create_result(
                rule_id="metrics_type",
                rule_name="Metrics Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Code metrics must be a dictionary",
                field_path="metrics",
                actual_value=type(metrics).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        # Validate each metric against standards
        for metric_name, metric_value in metrics.items():
            if metric_name in self.code_standards:
                threshold = self.code_standards[metric_name]
                if isinstance(metric_value, (int, float)):
                    if metric_value > threshold:
                        result = self._create_result(
                            rule_id=f"{metric_name}_exceeded",
                            rule_name=f"{metric_name.title()} Exceeded",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=f"Code metric '{metric_name}' exceeds threshold: {metric_value} > {threshold}",
                            field_path=f"metrics.{metric_name}",
                            actual_value=metric_value,
                            expected_value=f"<= {threshold}",
                        )
                        results.append(result)

        return results

    def _validate_naming_conventions(self, naming: Any) -> List[ValidationResult]:
        """Validate naming conventions"""
        results = []

        if not isinstance(naming, dict):
            result = self._create_result(
                rule_id="naming_type",
                rule_name="Naming Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Naming conventions must be a dictionary",
                field_path="naming",
                actual_value=type(naming).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        # Validate naming patterns if present
        if "patterns" in naming:
            patterns = naming["patterns"]
            if isinstance(patterns, dict):
                for pattern_name, pattern in patterns.items():
                    if isinstance(pattern, str):
                        try:
                            re.compile(pattern)
                        except re.error:
                            result = self._create_result(
                                rule_id=f"naming_pattern_invalid",
                                rule_name="Naming Pattern Invalid",
                                status=ValidationStatus.FAILED,
                                severity=ValidationSeverity.ERROR,
                                message=f"Invalid naming pattern '{pattern_name}': {pattern}",
                                field_path=f"naming.patterns.{pattern_name}",
                                actual_value=pattern,
                                expected_value="valid regex pattern",
                            )
                            results.append(result)

        return results

    def _validate_code_complexity(self, complexity: Any) -> List[ValidationResult]:
        """Validate code complexity"""
        results = []

        if not isinstance(complexity, dict):
            result = self._create_result(
                rule_id="complexity_type",
                rule_name="Complexity Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Code complexity must be a dictionary",
                field_path="complexity",
                actual_value=type(complexity).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        # Validate cyclomatic complexity if present
        if "cyclomatic_complexity" in complexity:
            cc = complexity["cyclomatic_complexity"]
            if isinstance(cc, (int, float)):
                if cc > 10:  # High complexity threshold
                    result = self._create_result(
                        rule_id="cyclomatic_complexity_high",
                        rule_name="Cyclomatic Complexity High",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=f"Cyclomatic complexity is high: {cc}",
                        field_path="complexity.cyclomatic_complexity",
                        actual_value=cc,
                        expected_value="<= 10",
                    )
                    results.append(result)

        # Validate nesting depth if present
        if "nesting_depth" in complexity:
            depth = complexity["nesting_depth"]
            if isinstance(depth, (int, float)):
                if depth > self.code_standards["max_nesting_depth"]:
                    result = self._create_result(
                        rule_id="nesting_depth_exceeded",
                        rule_name="Nesting Depth Exceeded",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=f"Nesting depth exceeds threshold: {depth} > {self.code_standards['max_nesting_depth']}",
                        field_path="complexity.nesting_depth",
                        actual_value=depth,
                        expected_value=f"<= {self.code_standards['max_nesting_depth']}",
                    )
                    results.append(result)

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
