#!/usr/bin/env python3
"""
Performance Validation Engine - V2 Modular Architecture
======================================================

Handles all performance validation operations.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from .validation_types import ValidationStatus, ValidationSeverity, ValidationContext, ValidationResult, ValidationSummary


logger = logging.getLogger(__name__)


class ValidationEngine:
    """
    Validation Engine - Single responsibility: Validate performance metrics
    
    Handles all validation operations including:
    - Metric validation against rules
    - Threshold checking
    - Performance classification
    - Validation result management
    """

    def __init__(self):
        """Initialize validation engine"""
        self.logger = logging.getLogger(f"{__name__}.ValidationEngine")
        
        # Validation rules
        self.validation_rules: List[Dict[str, Any]] = []
        
        # Thresholds
        self.thresholds: Dict[str, Dict[str, Any]] = {}
        
        # Validation history
        self.validation_history: List[ValidationResult] = []
        
        # Default thresholds
        self._setup_default_thresholds()
        
        self.logger.info("✅ Validation Engine initialized successfully")

    def _setup_default_thresholds(self) -> None:
        """Setup default validation thresholds"""
        self.thresholds = {
            "cpu_usage_percent": {
                "warning": 80.0,
                "critical": 95.0,
                "operator": ">="
            },
            "memory_usage_percent": {
                "warning": 85.0,
                "critical": 95.0,
                "operator": ">="
            },
            "disk_usage_percent": {
                "warning": 90.0,
                "critical": 98.0,
                "operator": ">="
            },
            "response_time_ms": {
                "warning": 500.0,
                "critical": 1000.0,
                "operator": ">="
            },
            "network_latency_ms": {
                "warning": 100.0,
                "critical": 200.0,
                "operator": ">="
            }
        }

    def add_validation_rule(self, rule: Dict[str, Any]) -> None:
        """Add a new validation rule"""
        try:
            rule["id"] = f"rule_{len(self.validation_rules) + 1}"
            rule["created_at"] = datetime.now().isoformat()
            self.validation_rules.append(rule)
            self.logger.info(f"✅ Added validation rule: {rule['id']}")
            
        except Exception as e:
            self.logger.error(f"Failed to add validation rule: {e}")

    def set_threshold(self, metric_name: str, severity: str, value: float, operator: str = ">=") -> None:
        """Set threshold for a metric"""
        try:
            if metric_name not in self.thresholds:
                self.thresholds[metric_name] = {}
            
            self.thresholds[metric_name][severity] = value
            self.thresholds[metric_name]["operator"] = operator
            
            self.logger.info(f"✅ Set {severity} threshold for {metric_name}: {value}")
            
        except Exception as e:
            self.logger.error(f"Failed to set threshold for {metric_name}: {e}")

    def validate_metrics(self, metrics: Dict[str, Any]) -> List[ValidationResult]:
        """Validate metrics against validation rules"""
        try:
            validation_results = []
            
            for metric_name, metric_value in metrics.items():
                # Validate against thresholds
                threshold_results = self._check_metric_thresholds(metric_name, metric_value)
                validation_results.extend(threshold_results)
                
                # Validate against custom rules
                rule_results = self._validate_against_rules(metric_name, metric_value)
                validation_results.extend(rule_results)
            
            # Store validation results
            self.validation_history.extend(validation_results)
            
            # Limit history size
            if len(self.validation_history) > 10000:
                self.validation_history = self.validation_history[-5000:]
            
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Failed to validate metrics: {e}")
            return []

    def _check_metric_thresholds(self, metric_name: str, metric_value: Any) -> List[ValidationResult]:
        """Check metric against configured thresholds"""
        results = []
        
        try:
            if metric_name not in self.thresholds:
                return results
            
            threshold_config = self.thresholds[metric_name]
            operator = threshold_config.get("operator", ">=")
            
            # Check warning threshold
            if "warning" in threshold_config:
                warning_threshold = threshold_config["warning"]
                if self._evaluate_threshold(metric_value, warning_threshold, operator):
                    results.append(ValidationResult(
                        metric_name=metric_name,
                        current_value=metric_value,
                        threshold=warning_threshold,
                        severity=ValidationSeverity.WARNING,
                        message=f"{metric_name} exceeds warning threshold",
                        passed=False,
                        timestamp=datetime.now().isoformat()
                    ))
            
            # Check critical threshold
            if "critical" in threshold_config:
                critical_threshold = threshold_config["critical"]
                if self._evaluate_threshold(metric_value, critical_threshold, operator):
                    results.append(ValidationResult(
                        metric_name=metric_name,
                        current_value=metric_value,
                        threshold=critical_threshold,
                        severity=ValidationSeverity.CRITICAL,
                        message=f"{metric_name} exceeds critical threshold",
                        passed=False,
                        timestamp=datetime.now().isoformat()
                    ))
            
        except Exception as e:
            self.logger.error(f"Failed to check thresholds for {metric_name}: {e}")
        
        return results

    def _evaluate_threshold(self, value: Any, threshold: float, operator: str) -> bool:
        """Evaluate if a value meets a threshold condition"""
        try:
            if not isinstance(value, (int, float)):
                return False
            
            if operator == ">=":
                return value >= threshold
            elif operator == ">":
                return value > threshold
            elif operator == "<=":
                return value <= threshold
            elif operator == "<":
                return value < threshold
            elif operator == "==":
                return value == threshold
            elif operator == "!=":
                return value != threshold
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to evaluate threshold: {e}")
            return False

    def _validate_against_rules(self, metric_name: str, metric_value: Any) -> List[ValidationResult]:
        """Validate metric against custom validation rules"""
        results = []
        
        try:
            for rule in self.validation_rules:
                if self._should_apply_rule(rule, metric_name):
                    rule_result = self._apply_validation_rule(rule, metric_name, metric_value)
                    if rule_result:
                        results.append(rule_result)
                        
        except Exception as e:
            self.logger.error(f"Failed to validate against rules for {metric_name}: {e}")
        
        return results

    def _should_apply_rule(self, rule: Dict[str, Any], metric_name: str) -> bool:
        """Check if a rule should be applied to a metric"""
        try:
            target_metrics = rule.get("target_metrics", [])
            if not target_metrics:
                return True  # Apply to all metrics if no specific targets
            
            return metric_name in target_metrics
            
        except Exception as e:
            self.logger.error(f"Failed to check rule applicability: {e}")
            return False

    def _apply_validation_rule(self, rule: Dict[str, Any], metric_name: str, metric_value: Any) -> Optional[ValidationResult]:
        """Apply a validation rule to a metric"""
        try:
            rule_type = rule.get("type", "threshold")
            
            if rule_type == "threshold":
                return self._apply_threshold_rule(rule, metric_name, metric_value)
            elif rule_type == "range":
                return self._apply_range_rule(rule, metric_name, metric_value)
            elif rule_type == "trend":
                return self._apply_trend_rule(rule, metric_name, metric_value)
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to apply validation rule: {e}")
            return None

    def _apply_threshold_rule(self, rule: Dict[str, Any], metric_name: str, metric_value: Any) -> Optional[ValidationResult]:
        """Apply a threshold-based validation rule"""
        try:
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
                    message=rule.get("message", f"{metric_name} failed threshold validation"),
                    passed=False,
                    timestamp=datetime.now().isoformat()
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to apply threshold rule: {e}")
            return None

    def _apply_range_rule(self, rule: Dict[str, Any], metric_name: str, metric_value: Any) -> Optional[ValidationResult]:
        """Apply a range-based validation rule"""
        try:
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
                    timestamp=datetime.now().isoformat()
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to apply range rule: {e}")
            return None

    def _apply_trend_rule(self, rule: Dict[str, Any], metric_name: str, metric_value: Any) -> Optional[ValidationResult]:
        """Apply a trend-based validation rule"""
        try:
            # This is a simplified trend rule - in practice, you'd need historical data
            trend_threshold = rule.get("trend_threshold")
            severity = rule.get("severity", ValidationSeverity.WARNING)
            
            if trend_threshold is None:
                return None
            
            # For now, just check if value is above trend threshold
            if metric_value > trend_threshold:
                return ValidationResult(
                    metric_name=metric_name,
                    current_value=metric_value,
                    threshold=trend_threshold,
                    severity=severity,
                    message=f"{metric_name} exceeds trend threshold",
                    passed=False,
                    timestamp=datetime.now().isoformat()
                )
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to apply trend rule: {e}")
            return None

    def check_thresholds(self, metrics: Dict[str, Any]) -> List[ValidationResult]:
        """Check metrics against configured thresholds"""
        return self.validate_metrics(metrics)

    def get_validation_summary(self) -> ValidationSummary:
        """Get validation summary"""
        try:
            total_validations = len(self.validation_history)
            passed_validations = len([r for r in self.validation_history if r.passed])
            failed_validations = total_validations - passed_validations
            
            # Count by severity
            severity_counts = {}
            for result in self.validation_history:
                severity = result.severity.value
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            return ValidationSummary(
                total_validations=total_validations,
                passed_validations=passed_validations,
                failed_validations=failed_validations,
                success_rate=round(passed_validations / max(total_validations, 1), 3),
                severity_distribution=severity_counts,
                last_validation=datetime.now().isoformat()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get validation summary: {e}")
            return ValidationSummary(
                total_validations=0,
                passed_validations=0,
                failed_validations=0,
                success_rate=0.0,
                severity_distribution={},
                last_validation=datetime.now().isoformat()
            )

    def get_recent_validations(self, count: int = 100) -> List[ValidationResult]:
        """Get recent validation results"""
        return self.validation_history[-count:] if self.validation_history else []

    def clear_validation_history(self) -> None:
        """Clear validation history"""
        self.validation_history.clear()
        self.logger.info("✅ Validation history cleared")

    def get_thresholds(self) -> Dict[str, Dict[str, Any]]:
        """Get all configured thresholds"""
        return self.thresholds.copy()

    def remove_threshold(self, metric_name: str) -> bool:
        """Remove threshold for a metric"""
        try:
            if metric_name in self.thresholds:
                del self.thresholds[metric_name]
                self.logger.info(f"✅ Removed threshold for {metric_name}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to remove threshold for {metric_name}: {e}")
            return False

    def export_validation_config(self) -> Dict[str, Any]:
        """Export validation configuration"""
        try:
            return {
                "export_timestamp": datetime.now().isoformat(),
                "thresholds": self.thresholds,
                "validation_rules": self.validation_rules,
                "total_rules": len(self.validation_rules),
                "total_thresholds": len(self.thresholds)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to export validation config: {e}")
            return {"error": str(e)}

    def reset(self) -> None:
        """Reset validation engine to initial state"""
        try:
            self.clear_validation_history()
            self.validation_rules.clear()
            self._setup_default_thresholds()
            self.logger.info("✅ Validation Engine reset to initial state")
            
        except Exception as e:
            self.logger.error(f"Failed to reset validation engine: {e}")
