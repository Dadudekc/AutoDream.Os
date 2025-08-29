"""
Quality Validator - Unified Validation Framework

This module provides code quality validation functionality, inheriting from BaseValidator
and following the unified validation framework patterns.
"""

from typing import Dict, List, Any, Optional
from .base_validator import (
    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)
import time


class QualityValidator(BaseValidator):
    """Validates code quality metrics and standards using unified validation framework"""

    def __init__(self):
        """Initialize quality validator"""
        super().__init__("QualityValidator")
        self.quality_thresholds = {
            "cyclomatic_complexity": 10,
            "maintainability_index": 65,
            "code_duplication": 5.0,
            "test_coverage": 80.0,
            "documentation_coverage": 70.0,
            "max_function_length": 50,
            "max_class_length": 500,
            "max_file_length": 400,
        }

    def validate(
        self, quality_data: Dict[str, Any], **kwargs
    ) -> List[ValidationResult]:
        """Validate quality data and return validation results.

        Returns:
            List[ValidationResult]: Validation results produced during quality
            validation.
        """
        results = []

        try:
            # Validate quality data structure
            structure_results = self._validate_quality_structure(quality_data)
            results.extend(structure_results)

            # Validate required fields
            required_fields = ["file_path", "metrics", "timestamp"]
            field_results = self._validate_required_fields(
                quality_data, required_fields
            )
            results.extend(field_results)

            # Validate quality metrics if present
            if "metrics" in quality_data:
                metrics_results = self._validate_quality_metrics(
                    quality_data["metrics"]
                )
                results.extend(metrics_results)

            # Validate complexity analysis if present
            if "complexity" in quality_data:
                complexity_results = self._validate_complexity_analysis(
                    quality_data["complexity"]
                )
                results.extend(complexity_results)

            # Validate duplication analysis if present
            if "duplication" in quality_data:
                duplication_results = self._validate_duplication_analysis(
                    quality_data["duplication"]
                )
                results.extend(duplication_results)

            # Validate test coverage if present
            if "test_coverage" in quality_data:
                coverage_results = self._validate_test_coverage(
                    quality_data["test_coverage"]
                )
                results.extend(coverage_results)

            # Add overall success result if no critical errors
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                success_result = self._create_result(
                    rule_id="overall_quality_validation",
                    rule_name="Overall Quality Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Quality validation passed successfully",
                    details={"total_checks": len(results)},
                )
                results.append(success_result)

        except Exception as e:
            error_result = self._create_result(
                rule_id="quality_validation_error",
                rule_name="Quality Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Quality validation error: {str(e)}",
                details={"error_type": type(e).__name__},
            )
            results.append(error_result)

        return results

    def _validate_quality_structure(
        self, quality_data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate quality data structure and format"""
        results = []

        if not isinstance(quality_data, dict):
            result = self._create_result(
                rule_id="quality_type",
                rule_name="Quality Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Quality data must be a dictionary",
                actual_value=type(quality_data).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        if len(quality_data) == 0:
            result = self._create_result(
                rule_id="quality_empty",
                rule_name="Quality Empty Check",
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.WARNING,
                message="Quality data is empty",
                actual_value=quality_data,
                expected_value="non-empty quality data",
            )
            results.append(result)

        return results

    def _validate_quality_metrics(self, metrics: Any) -> List[ValidationResult]:
        """Validate quality metrics against thresholds"""
        results = []

        if not isinstance(metrics, dict):
            result = self._create_result(
                rule_id="metrics_type",
                rule_name="Metrics Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Metrics must be a dictionary",
                field_path="metrics",
                actual_value=type(metrics).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        # Validate each metric against thresholds
        for metric_name, metric_value in metrics.items():
            if metric_name in self.quality_thresholds:
                threshold = self.quality_thresholds[metric_name]
                threshold_result = self._validate_metric_threshold(
                    metric_name, metric_value, threshold
                )
                if threshold_result:
                    results.append(threshold_result)

        return results

    def _validate_metric_threshold(
        self, metric_name: str, metric_value: Any, threshold: float
    ) -> Optional[ValidationResult]:
        """Validate a single metric against its threshold"""
        if not isinstance(metric_value, (int, float)):
            return self._create_result(
                rule_id=f"{metric_name}_type",
                rule_name=f"{metric_name} Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Metric '{metric_name}' must be numeric",
                field_path=f"metrics.{metric_name}",
                actual_value=type(metric_value).__name__,
                expected_value="numeric value",
            )

        # Different validation logic based on metric type
        if metric_name in [
            "cyclomatic_complexity",
            "max_function_length",
            "max_class_length",
            "max_file_length",
        ]:
            # These should be <= threshold
            if metric_value > threshold:
                return self._create_result(
                    rule_id=f"{metric_name}_threshold",
                    rule_name=f"{metric_name} Threshold Check",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Metric '{metric_name}' exceeds threshold: {metric_value} > {threshold}",
                    field_path=f"metrics.{metric_name}",
                    actual_value=metric_value,
                    expected_value=f"<= {threshold}",
                )

        elif metric_name in [
            "maintainability_index",
            "test_coverage",
            "documentation_coverage",
        ]:
            # These should be >= threshold
            if metric_value < threshold:
                return self._create_result(
                    rule_id=f"{metric_name}_threshold",
                    rule_name=f"{metric_name} Threshold Check",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Metric '{metric_name}' below threshold: {metric_value} < {threshold}",
                    field_path=f"metrics.{metric_name}",
                    actual_value=metric_value,
                    expected_value=f">= {threshold}",
                )

        elif metric_name == "code_duplication":
            # This should be <= threshold (percentage)
            if metric_value > threshold:
                return self._create_result(
                    rule_id=f"{metric_name}_threshold",
                    rule_name=f"{metric_name} Threshold Check",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Code duplication exceeds threshold: {metric_value}% > {threshold}%",
                    field_path=f"metrics.{metric_name}",
                    actual_value=f"{metric_value}%",
                    expected_value=f"<= {threshold}%",
                )

        return None

    def _validate_complexity_analysis(self, complexity: Any) -> List[ValidationResult]:
        """Validate complexity analysis data"""
        results = []

        if not isinstance(complexity, dict):
            result = self._create_result(
                rule_id="complexity_type",
                rule_name="Complexity Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Complexity data must be a dictionary",
                field_path="complexity",
                actual_value=type(complexity).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        # Validate cyclomatic complexity if present
        if "cyclomatic_complexity" in complexity:
            cc_value = complexity["cyclomatic_complexity"]
            if isinstance(cc_value, (int, float)):
                if cc_value > self.quality_thresholds["cyclomatic_complexity"]:
                    result = self._create_result(
                        rule_id="complexity_cyclomatic",
                        rule_name="Cyclomatic Complexity Check",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Cyclomatic complexity too high: {cc_value}",
                        field_path="complexity.cyclomatic_complexity",
                        actual_value=cc_value,
                        expected_value=f"<= {self.quality_thresholds['cyclomatic_complexity']}",
                    )
                    results.append(result)

        # Validate maintainability index if present
        if "maintainability_index" in complexity:
            mi_value = complexity["maintainability_index"]
            if isinstance(mi_value, (int, float)):
                if mi_value < self.quality_thresholds["maintainability_index"]:
                    result = self._create_result(
                        rule_id="complexity_maintainability",
                        rule_name="Maintainability Index Check",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Maintainability index too low: {mi_value}",
                        field_path="complexity.maintainability_index",
                        actual_value=mi_value,
                        expected_value=f">= {self.quality_thresholds['maintainability_index']}",
                    )
                    results.append(result)

        return results

    def _validate_duplication_analysis(
        self, duplication: Any
    ) -> List[ValidationResult]:
        """Validate duplication analysis data"""
        results = []

        if not isinstance(duplication, dict):
            result = self._create_result(
                rule_id="duplication_type",
                rule_name="Duplication Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Duplication data must be a dictionary",
                field_path="duplication",
                actual_value=type(duplication).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        # Validate duplication percentage if present
        if "percentage" in duplication:
            dup_percentage = duplication["percentage"]
            if isinstance(dup_percentage, (int, float)):
                if dup_percentage > self.quality_thresholds["code_duplication"]:
                    result = self._create_result(
                        rule_id="duplication_percentage",
                        rule_name="Duplication Percentage Check",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Code duplication too high: {dup_percentage}%",
                        field_path="duplication.percentage",
                        actual_value=f"{dup_percentage}%",
                        expected_value=f"<= {self.quality_thresholds['code_duplication']}%",
                    )
                    results.append(result)

        # Validate duplicate blocks if present
        if "duplicate_blocks" in duplication:
            dup_blocks = duplication["duplicate_blocks"]
            if isinstance(dup_blocks, list):
                if len(dup_blocks) > 0:
                    result = self._create_result(
                        rule_id="duplication_blocks",
                        rule_name="Duplicate Blocks Check",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=f"Found {len(dup_blocks)} duplicate code blocks",
                        field_path="duplication.duplicate_blocks",
                        actual_value=len(dup_blocks),
                        expected_value="0 duplicate blocks",
                    )
                    results.append(result)

        return results

    def _validate_test_coverage(self, test_coverage: Any) -> List[ValidationResult]:
        """Validate test coverage data"""
        results = []

        if not isinstance(test_coverage, dict):
            result = self._create_result(
                rule_id="test_coverage_type",
                rule_name="Test Coverage Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Test coverage data must be a dictionary",
                field_path="test_coverage",
                actual_value=type(test_coverage).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        # Validate overall coverage if present
        if "overall" in test_coverage:
            overall_coverage = test_coverage["overall"]
            if isinstance(overall_coverage, (int, float)):
                if overall_coverage < self.quality_thresholds["test_coverage"]:
                    result = self._create_result(
                        rule_id="test_coverage_overall",
                        rule_name="Test Coverage Overall Check",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Test coverage too low: {overall_coverage}%",
                        field_path="test_coverage.overall",
                        actual_value=f"{overall_coverage}%",
                        expected_value=f">= {self.quality_thresholds['test_coverage']}%",
                    )
                    results.append(result)

        # Validate line coverage if present
        if "line_coverage" in test_coverage:
            line_coverage = test_coverage["line_coverage"]
            if isinstance(line_coverage, (int, float)):
                if line_coverage < self.quality_thresholds["test_coverage"]:
                    result = self._create_result(
                        rule_id="test_coverage_line",
                        rule_name="Test Coverage Line Check",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Line coverage too low: {line_coverage}%",
                        field_path="test_coverage.line_coverage",
                        actual_value=f"{line_coverage}%",
                        expected_value=f">= {self.quality_thresholds['test_coverage']}%",
                    )
                    results.append(result)

        return results

    def set_quality_threshold(self, metric_name: str, threshold: float) -> bool:
        """Set a custom quality threshold for a metric"""
        try:
            if metric_name in self.quality_thresholds:
                self.quality_thresholds[metric_name] = threshold
                self.logger.info(
                    f"Quality threshold updated: {metric_name} = {threshold}"
                )
                return True
            else:
                self.logger.warning(f"Unknown metric: {metric_name}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to set quality threshold: {e}")
            return False

    def get_quality_thresholds(self) -> Dict[str, float]:
        """Get current quality thresholds"""
        return self.quality_thresholds.copy()

    # Quality validation functionality integration (from duplicate quality_validator.py)
    def validate_service_quality_legacy(
        self, service_id: str, quality_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Legacy service quality validation method (from duplicate quality_validator.py)"""
        try:
            validation_results = []
            current_time = time.time()

            # Check test coverage
            if "test_coverage" in quality_data:
                test_coverage = quality_data["test_coverage"]
                if isinstance(test_coverage, (int, float)):
                    if test_coverage < 80.0:
                        validation_results.append(
                            {
                                "validation_id": f"validation_{service_id}_test_coverage_{int(current_time)}",
                                "rule_id": "test_coverage_min",
                                "service_id": service_id,
                                "status": "failed",
                                "timestamp": current_time,
                                "actual_value": test_coverage,
                                "expected_value": 80.0,
                                "message": f"Test coverage {test_coverage}% below threshold 80%",
                                "details": {
                                    "rule_name": "Minimum Test Coverage",
                                    "rule_type": "coverage",
                                    "severity": "high",
                                },
                            }
                        )
                    else:
                        validation_results.append(
                            {
                                "validation_id": f"validation_{service_id}_test_coverage_{int(current_time)}",
                                "rule_id": "test_coverage_min",
                                "service_id": service_id,
                                "status": "passed",
                                "timestamp": current_time,
                                "actual_value": test_coverage,
                                "expected_value": 80.0,
                                "message": f"Test coverage {test_coverage}% meets threshold 80%",
                                "details": {
                                    "rule_name": "Minimum Test Coverage",
                                    "rule_type": "coverage",
                                    "severity": "high",
                                },
                            }
                        )

            # Check code quality
            if "code_quality" in quality_data:
                code_quality = quality_data["code_quality"]
                if isinstance(code_quality, (int, float)):
                    if code_quality < 7.0:
                        validation_results.append(
                            {
                                "validation_id": f"validation_{service_id}_code_quality_{int(current_time)}",
                                "rule_id": "code_quality_min",
                                "service_id": service_id,
                                "status": "failed",
                                "timestamp": current_time,
                                "actual_value": code_quality,
                                "expected_value": 7.0,
                                "message": f"Code quality {code_quality} below threshold 7.0",
                                "details": {
                                    "rule_name": "Minimum Code Quality",
                                    "rule_type": "quality",
                                    "severity": "medium",
                                },
                            }
                        )
                    else:
                        validation_results.append(
                            {
                                "validation_id": f"validation_{service_id}_code_quality_{int(current_time)}",
                                "rule_id": "code_quality_min",
                                "service_id": service_id,
                                "status": "passed",
                                "timestamp": current_time,
                                "actual_value": code_quality,
                                "expected_value": 7.0,
                                "message": f"Code quality {code_quality} meets threshold 7.0",
                                "details": {
                                    "rule_name": "Minimum Code Quality",
                                    "rule_type": "quality",
                                    "severity": "medium",
                                },
                            }
                        )

            return validation_results

        except Exception as e:
            self.logger.error(
                f"Failed to validate service quality for {service_id}: {e}"
            )
            return []

    def get_validation_summary_legacy(self, service_id: str = None) -> Dict[str, Any]:
        """Get legacy validation summary statistics"""
        try:
            # This would need to be implemented based on the legacy validation results
            # For now, return a basic structure
            return {
                "total_validations": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0,
                "pending": 0,
                "pass_rate": 0.0,
                "note": "Legacy validation summary - implement based on stored results",
            }

        except Exception as e:
            self.logger.error(f"Failed to get legacy validation summary: {e}")
            return {"error": str(e)}

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime

        return datetime.now().isoformat()
