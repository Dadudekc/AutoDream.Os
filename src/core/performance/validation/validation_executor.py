"""Execution of performance validation rules."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .rule_management import RuleManager
from .validation_types import ValidationResult, ValidationSeverity


class ValidationExecutor:
    """Execute validation rules against provided metrics."""

    def __init__(self, rule_manager: RuleManager) -> None:
        self.logger = logging.getLogger(f"{__name__}.ValidationExecutor")
        self.rule_manager = rule_manager

    def validate_metrics(self, metrics: Dict[str, Any]) -> List[ValidationResult]:
        """Validate metrics and return results."""
        validation_results: List[ValidationResult] = []
        for metric_name, metric_value in metrics.items():
            validation_results.extend(
                self._check_metric_thresholds(metric_name, metric_value)
            )
            validation_results.extend(
                self._validate_against_rules(metric_name, metric_value)
            )
        return validation_results

    def _check_metric_thresholds(self, metric_name: str, metric_value: Any) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        threshold_config = self.rule_manager.thresholds.get(metric_name)
        if not threshold_config:
            return results
        operator = threshold_config.get("operator", ">=")
        if "warning" in threshold_config:
            warning = threshold_config["warning"]
            if self._evaluate_threshold(metric_value, warning, operator):
                results.append(
                    ValidationResult(
                        metric_name=metric_name,
                        current_value=metric_value,
                        threshold=warning,
                        severity=ValidationSeverity.WARNING,
                        message=f"{metric_name} exceeds warning threshold",
                        passed=False,
                        timestamp=datetime.now().isoformat(),
                    )
                )
        if "critical" in threshold_config:
            critical = threshold_config["critical"]
            if self._evaluate_threshold(metric_value, critical, operator):
                results.append(
                    ValidationResult(
                        metric_name=metric_name,
                        current_value=metric_value,
                        threshold=critical,
                        severity=ValidationSeverity.CRITICAL,
                        message=f"{metric_name} exceeds critical threshold",
                        passed=False,
                        timestamp=datetime.now().isoformat(),
                    )
                )
        return results

    def _validate_against_rules(self, metric_name: str, metric_value: Any) -> List[ValidationResult]:
        results: List[ValidationResult] = []
        for rule in self.rule_manager.validation_rules:
            if self._should_apply_rule(rule, metric_name):
                rule_result = self._apply_validation_rule(
                    rule, metric_name, metric_value
                )
                if rule_result:
                    results.append(rule_result)
        return results

    def _should_apply_rule(self, rule: Dict[str, Any], metric_name: str) -> bool:
        targets = rule.get("target_metrics", [])
        return not targets or metric_name in targets

    def _apply_validation_rule(
        self, rule: Dict[str, Any], metric_name: str, metric_value: Any
    ) -> Optional[ValidationResult]:
        rule_type = rule.get("type", "threshold")
        if rule_type == "threshold":
            return self._apply_threshold_rule(rule, metric_name, metric_value)
        if rule_type == "range":
            return self._apply_range_rule(rule, metric_name, metric_value)
        if rule_type == "trend":
            return self._apply_trend_rule(rule, metric_name, metric_value)
        return None

    def _apply_threshold_rule(
        self, rule: Dict[str, Any], metric_name: str, metric_value: Any
    ) -> Optional[ValidationResult]:
        threshold = rule.get("threshold")
        operator = rule.get("operator", ">=")
        severity = rule.get("severity", ValidationSeverity.WARNING)
        if threshold is None:
            return None
        if self._evaluate_threshold(metric_value, threshold, operator):
            return ValidationResult(
                metric_name=metric_name,
                current_value=metric_value,
                threshold=threshold,
                severity=severity,
                message=rule.get(
                    "message", f"{metric_name} failed threshold validation"
                ),
                passed=False,
                timestamp=datetime.now().isoformat(),
            )
        return None

    def _apply_range_rule(
        self, rule: Dict[str, Any], metric_name: str, metric_value: Any
    ) -> Optional[ValidationResult]:
        min_value = rule.get("min_value")
        max_value = rule.get("max_value")
        severity = rule.get("severity", ValidationSeverity.WARNING)
        if min_value is None and max_value is None:
            return None
        failed = False
        message = ""
        if min_value is not None and metric_value < min_value:
            failed = True
            message = f"{metric_name} below minimum value {min_value}"
        elif max_value is not None and metric_value > max_value:
            failed = True
            message = f"{metric_name} above maximum value {max_value}"
        if failed:
            return ValidationResult(
                metric_name=metric_name,
                current_value=metric_value,
                threshold=f"range({min_value}, {max_value})",
                severity=severity,
                message=message,
                passed=False,
                timestamp=datetime.now().isoformat(),
            )
        return None

    def _apply_trend_rule(
        self, rule: Dict[str, Any], metric_name: str, metric_value: Any
    ) -> Optional[ValidationResult]:
        trend_threshold = rule.get("trend_threshold")
        severity = rule.get("severity", ValidationSeverity.WARNING)
        if trend_threshold is None:
            return None
        if metric_value > trend_threshold:
            return ValidationResult(
                metric_name=metric_name,
                current_value=metric_value,
                threshold=trend_threshold,
                severity=severity,
                message=f"{metric_name} exceeds trend threshold",
                passed=False,
                timestamp=datetime.now().isoformat(),
            )
        return None

    @staticmethod
    def _evaluate_threshold(value: Any, threshold: float, operator: str) -> bool:
        if not isinstance(value, (int, float)):
            return False
        if operator == ">=":
            return value >= threshold
        if operator == ">":
            return value > threshold
        if operator == "<=":
            return value <= threshold
        if operator == "<":
            return value < threshold
        if operator == "==":
            return value == threshold
        if operator == "!=":
            return value != threshold
        return False
