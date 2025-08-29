from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import logging

    from .performance_core import ValidationThreshold
from .performance_core import (
from __future__ import annotations

#!/usr/bin/env python3
"""
Performance Validator - Performance Validation Logic

Extracted from unified_performance_system.py to achieve V2 compliance.
Contains validation rules, thresholds, and validation logic.

Author: Agent-8 (Technical Debt Specialist)
License: MIT
"""



    PerformanceMetric, ValidationRule, ValidationThreshold,
    ValidationSeverity, PerformanceLevel
)


class PerformanceValidator:
    """
    Performance validation engine.
    
    Validates performance metrics against defined rules and thresholds,
    generating alerts and recommendations for performance optimization.
    """
    
    def __init__(self):
        """Initialize the performance validator."""
        self.logger = logging.getLogger(__name__)
        
        # Validation components
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.thresholds: Dict[str, ValidationThreshold] = {}
        self.validation_history: List[Dict[str, Any]] = []
        
        # Alert tracking
        self.active_alerts: List[Dict[str, Any]] = []
        self.alert_history: List[Dict[str, Any]] = []
        
        self.logger.info("Performance Validator initialized")
    
    def add_validation_rule(self, rule: ValidationRule) -> bool:
        """Add a validation rule."""
        try:
            self.validation_rules[rule.rule_name] = rule
            self.logger.info(f"Validation rule added: {rule.rule_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add validation rule: {e}")
            return False
    
    def add_threshold(self, threshold: ValidationThreshold) -> bool:
        """Add a performance threshold."""
        try:
            self.thresholds[threshold.metric_name] = threshold
            self.logger.info(f"Threshold added: {threshold.metric_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add threshold: {e}")
            return False
    
    def validate_metric(self, metric: PerformanceMetric) -> Dict[str, Any]:
        """Validate a single performance metric."""
        try:
            validation_result = {
                "metric_name": metric.name,
                "timestamp": metric.timestamp,
                "value": metric.value,
                "unit": metric.unit,
                "validations": [],
                "overall_status": "pass"
            }
            
            # Check thresholds
            threshold_result = self._check_thresholds(metric)
            if threshold_result:
                validation_result["validations"].append(threshold_result)
                if threshold_result["severity"] == ValidationSeverity.CRITICAL:
                    validation_result["overall_status"] = "fail"
                elif threshold_result["severity"] == ValidationSeverity.WARNING:
                    validation_result["overall_status"] = "warn"
            
            # Check validation rules
            rule_results = self._check_validation_rules(metric)
            validation_result["validations"].extend(rule_results)
            
            # Update overall status based on rule results
            for rule_result in rule_results:
                if rule_result["severity"] == ValidationSeverity.CRITICAL:
                    validation_result["overall_status"] = "fail"
                elif rule_result["severity"] == ValidationSeverity.WARNING and validation_result["overall_status"] != "fail":
                    validation_result["overall_status"] = "warn"
            
            # Store validation result
            self.validation_history.append(validation_result)
            
            # Check for alerts
            self._check_alerts(validation_result)
            
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Failed to validate metric {metric.name}: {e}")
            return {
                "metric_name": metric.name,
                "error": str(e),
                "overall_status": "error"
            }
    
    def validate_metrics(self, metrics: List[PerformanceMetric]) -> List[Dict[str, Any]]:
        """Validate multiple performance metrics."""
        results = []
        for metric in metrics:
            result = self.validate_metric(metric)
            results.append(result)
        return results
    
    def _check_thresholds(self, metric: PerformanceMetric) -> Optional[Dict[str, Any]]:
        """Check metric against defined thresholds."""
        if metric.name not in self.thresholds:
            return None
        
        threshold = self.thresholds[metric.name]
        value = metric.value
        
        # Check warning threshold
        if value > threshold.warning_threshold:
            if value > threshold.critical_threshold:
                return {
                    "type": "threshold",
                    "severity": ValidationSeverity.CRITICAL,
                    "message": f"Critical threshold exceeded: {value} > {threshold.critical_threshold}",
                    "threshold": threshold.critical_threshold
                }
            else:
                return {
                    "type": "threshold",
                    "severity": ValidationSeverity.WARNING,
                    "message": f"Warning threshold exceeded: {value} > {threshold.warning_threshold}",
                    "threshold": threshold.warning_threshold
                }
        
        return None
    
    def _check_validation_rules(self, metric: PerformanceMetric) -> List[Dict[str, Any]]:
        """Check metric against validation rules."""
        results = []
        
        for rule in self.validation_rules.values():
            if not rule.enabled or rule.metric_name != metric.name:
                continue
            
            # Apply rule logic
            rule_result = self._apply_validation_rule(rule, metric)
            if rule_result:
                results.append(rule_result)
        
        return results
    
    def _apply_validation_rule(self, rule: ValidationRule, metric: PerformanceMetric) -> Optional[Dict[str, Any]]:
        """Apply a single validation rule to a metric."""
        try:
            value = metric.value
            threshold = rule.threshold
            operator = rule.operator
            
            # Evaluate rule condition
            condition_met = False
            if operator == "gt":
                condition_met = value > threshold
            elif operator == "lt":
                condition_met = value < threshold
            elif operator == "eq":
                condition_met = value == threshold
            elif operator == "gte":
                condition_met = value >= threshold
            elif operator == "lte":
                condition_met = value <= threshold
            
            if condition_met:
                return {
                    "type": "rule",
                    "rule_name": rule.rule_name,
                    "severity": rule.severity,
                    "message": rule.description,
                    "threshold": threshold,
                    "operator": operator
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to apply validation rule {rule.rule_name}: {e}")
            return None
    
    def _check_alerts(self, validation_result: Dict[str, Any]):
        """Check if validation result triggers alerts."""
        for validation in validation_result.get("validations", []):
            if validation.get("severity") in [ValidationSeverity.WARNING, ValidationSeverity.CRITICAL]:
                alert = {
                    "timestamp": datetime.now(),
                    "metric_name": validation_result["metric_name"],
                    "severity": validation["severity"],
                    "message": validation["message"],
                    "validation_type": validation["type"]
                }
                
                self.active_alerts.append(alert)
                self.alert_history.append(alert)
                
                self.logger.warning(f"Performance alert: {alert['message']}")
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get currently active performance alerts."""
        return self.active_alerts.copy()
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary statistics."""
        total_validations = len(self.validation_history)
        if total_validations == 0:
            return {
                "total_validations": 0,
                "pass_count": 0,
                "warn_count": 0,
                "fail_count": 0,
                "active_alerts": len(self.active_alerts)
            }
        
        pass_count = len([r for r in self.validation_history if r.get("overall_status") == "pass"])
        warn_count = len([r for r in self.validation_history if r.get("overall_status") == "warn"])
        fail_count = len([r for r in self.validation_history if r.get("overall_status") == "fail"])
        
        return {
            "total_validations": total_validations,
            "pass_count": pass_count,
            "warn_count": warn_count,
            "fail_count": fail_count,
            "pass_rate": (pass_count / total_validations) * 100,
            "active_alerts": len(self.active_alerts)
        }
    
    def clear_alerts(self):
        """Clear all active alerts."""
        self.active_alerts.clear()
        self.logger.info("All active alerts cleared")
    
    def get_validation_history(self) -> List[Dict[str, Any]]:
        """Get validation history."""
        return self.validation_history.copy()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    
    # Create and test performance validator
    validator = PerformanceValidator()
    
    # Add sample threshold
    threshold = ValidationThreshold(
        metric_name="cpu_usage",
        warning_threshold=80.0,
        critical_threshold=95.0
    )
    validator.add_threshold(threshold)
    
    # Add sample validation rule
    rule = ValidationRule(
        rule_name="cpu_high_usage",
        metric_name="cpu_usage",
        threshold=90.0,
        operator="gt",
        severity=ValidationSeverity.WARNING,
        description="CPU usage is high"
    )
    validator.add_validation_rule(rule)
    
    print("✅ Performance validator initialized successfully")
    print(f"📊 Thresholds: {len(validator.thresholds)}")
    print(f"🔍 Validation Rules: {len(validator.validation_rules)}")
