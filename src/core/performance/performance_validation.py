#!/usr/bin/env python3
"""
Performance Validation Manager - Validation Rules and Alerting
===========================================================

Handles performance validation rules, threshold checking, and alert generation.
Follows V2 standards: ≤400 LOC, SRP, OOP design.

Author: Agent-1 (Phase 3 Modularization)
License: MIT
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

from .performance_models import (
    PerformanceMetric, ValidationRule, ValidationThreshold, 
    ValidationSeverity, PerformanceAlert
)


class PerformanceValidationManager:
    """
    Performance Validation Manager - Handles validation rules and alerting
    
    Single Responsibility: Validate performance metrics against defined rules,
    check thresholds, and generate performance alerts.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.PerformanceValidationManager")
        
        # Validation state
        self.validation_active = False
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.thresholds: Dict[str, ValidationThreshold] = {}
        
        # Alert tracking
        self.active_alerts: Dict[str, PerformanceAlert] = {}
        self.alert_history: List[PerformanceAlert] = []
        
        # Validation statistics
        self.total_validations = 0
        self.passed_validations = 0
        self.failed_validations = 0
        self.alerts_generated = 0
        
        # Default validation rules
        self._setup_default_rules()
        
        self.logger.info("Performance Validation Manager initialized")
    
    def _setup_default_rules(self):
        """Setup default validation rules"""
        default_rules = [
            ValidationRule(
                rule_name="response_time_threshold",
                metric_name="response_time_ms",
                threshold=1000.0,
                operator="lte",
                severity=ValidationSeverity.WARNING,
                description="Response time should be under 1 second"
            ),
            ValidationRule(
                rule_name="cpu_usage_threshold",
                metric_name="cpu_usage_percent",
                threshold=80.0,
                operator="lte",
                severity=ValidationSeverity.CRITICAL,
                description="CPU usage should be under 80%"
            ),
            ValidationRule(
                rule_name="memory_usage_threshold",
                metric_name="memory_usage_percent",
                threshold=85.0,
                operator="lte",
                severity=ValidationSeverity.WARNING,
                description="Memory usage should be under 85%"
            ),
            ValidationRule(
                rule_name="disk_usage_threshold",
                metric_name="disk_usage_percent",
                threshold=90.0,
                operator="lte",
                severity=ValidationSeverity.WARNING,
                description="Disk usage should be under 90%"
            )
        ]
        
        for rule in default_rules:
            self.validation_rules[rule.rule_name] = rule
        
        # Default thresholds
        default_thresholds = [
            ValidationThreshold(
                metric_name="response_time_ms",
                warning_threshold=500.0,
                critical_threshold=1000.0,
                unit="ms",
                description="Response time thresholds"
            ),
            ValidationThreshold(
                metric_name="cpu_usage_percent",
                warning_threshold=70.0,
                critical_threshold=80.0,
                unit="%",
                description="CPU usage thresholds"
            ),
            ValidationThreshold(
                metric_name="memory_usage_percent",
                warning_threshold=75.0,
                critical_threshold=85.0,
                unit="%",
                description="Memory usage thresholds"
            ),
            ValidationThreshold(
                metric_name="disk_usage_percent",
                warning_threshold=80.0,
                critical_threshold=90.0,
                unit="%",
                description="Disk usage thresholds"
            )
        ]
        
        for threshold in default_thresholds:
            self.thresholds[threshold.metric_name] = threshold
        
        self.logger.info(f"Setup {len(default_rules)} default validation rules and {len(default_thresholds)} thresholds")
    
    def start_validation(self) -> bool:
        """Start performance validation"""
        try:
            if self.validation_active:
                self.logger.warning("Validation is already active")
                return True
            
            self.validation_active = True
            self.logger.info("✅ Performance validation started")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start validation: {e}")
            return False
    
    def stop_validation(self) -> bool:
        """Stop performance validation"""
        try:
            if not self.validation_active:
                self.logger.warning("Validation is not active")
                return True
            
            self.validation_active = False
            self.logger.info("✅ Performance validation stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop validation: {e}")
            return False
    
    def add_validation_rule(self, rule: ValidationRule) -> bool:
        """Add a new validation rule"""
        try:
            if rule.rule_name in self.validation_rules:
                self.logger.warning(f"Validation rule '{rule.rule_name}' already exists, updating")
            
            self.validation_rules[rule.rule_name] = rule
            self.logger.info(f"Validation rule added: {rule.rule_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add validation rule: {e}")
            return False
    
    def remove_validation_rule(self, rule_name: str) -> bool:
        """Remove a validation rule"""
        try:
            if rule_name in self.validation_rules:
                del self.validation_rules[rule_name]
                self.logger.info(f"Validation rule removed: {rule_name}")
                return True
            else:
                self.logger.warning(f"Validation rule not found: {rule_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to remove validation rule: {e}")
            return False
    
    def add_threshold(self, threshold: ValidationThreshold) -> bool:
        """Add a new performance threshold"""
        try:
            if threshold.metric_name in self.thresholds:
                self.logger.warning(f"Threshold for '{threshold.metric_name}' already exists, updating")
            
            self.thresholds[threshold.metric_name] = threshold
            self.logger.info(f"Threshold added: {threshold.metric_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add threshold: {e}")
            return False
    
    def remove_threshold(self, metric_name: str) -> bool:
        """Remove a performance threshold"""
        try:
            if metric_name in self.thresholds:
                del self.thresholds[metric_name]
                self.logger.info(f"Threshold removed: {metric_name}")
                return True
            else:
                self.logger.warning(f"Threshold not found: {metric_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to remove threshold: {e}")
            return False
    
    def validate_metrics(self, metrics: List[PerformanceMetric]) -> List[Dict[str, Any]]:
        """Validate performance metrics against defined rules"""
        try:
            if not self.validation_active:
                self.logger.warning("Validation is not active")
                return []
            
            validation_results = []
            
            for metric in metrics:
                # Find applicable rules for this metric
                applicable_rules = [
                    rule for rule in self.validation_rules.values()
                    if rule.metric_name == metric.name and rule.enabled
                ]
                
                for rule in applicable_rules:
                    result = self._validate_metric_against_rule(metric, rule)
                    validation_results.append(result)
                    
                    # Update statistics
                    self.total_validations += 1
                    if result["status"] == "pass":
                        self.passed_validations += 1
                    else:
                        self.failed_validations += 1
            
            self.logger.debug(f"Validated {len(metrics)} metrics, {len(validation_results)} rule checks")
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Failed to validate metrics: {e}")
            return []
    
    def _validate_metric_against_rule(self, metric: PerformanceMetric, rule: ValidationRule) -> Dict[str, Any]:
        """Validate a single metric against a validation rule"""
        try:
            # Apply validation rule
            is_valid = self._apply_validation_rule(metric.value, rule)
            
            result = {
                "rule_name": rule.rule_name,
                "metric_name": metric.name,
                "metric_value": metric.value,
                "threshold": rule.threshold,
                "operator": rule.operator,
                "severity": rule.severity.value,
                "description": rule.description,
                "status": "pass" if is_valid else "fail",
                "timestamp": datetime.now().isoformat(),
                "message": f"Metric {metric.name}={metric.value} {'meets' if is_valid else 'fails'} {rule.description}"
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to validate metric against rule: {e}")
            return {
                "rule_name": rule.rule_name,
                "metric_name": metric.name,
                "status": "error",
                "message": f"Validation error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _apply_validation_rule(self, metric_value: float, rule: ValidationRule) -> bool:
        """Apply a single validation rule to a metric value"""
        try:
            if rule.operator == "gt":
                return metric_value > rule.threshold
            elif rule.operator == "lt":
                return metric_value < rule.threshold
            elif rule.operator == "eq":
                return abs(metric_value - rule.threshold) < 0.001  # Small tolerance for float comparison
            elif rule.operator == "gte":
                return metric_value >= rule.threshold
            elif rule.operator == "lte":
                return metric_value <= rule.threshold
            else:
                self.logger.warning(f"Unknown operator: {rule.operator}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to apply validation rule: {e}")
            return False
    
    def check_alerts(self, validation_results: List[Dict[str, Any]]) -> List[str]:
        """Check validation results and generate alerts"""
        try:
            new_alerts = []
            
            for result in validation_results:
                if result.get("status") == "fail":
                    # Check if we should generate an alert
                    severity = result.get("severity", "info")
                    if severity in ["warning", "critical"]:
                        alert = self._create_alert_from_validation(result)
                        if alert:
                            self.active_alerts[alert.alert_id] = alert
                            self.alert_history.append(alert)
                            new_alerts.append(alert.alert_id)
                            self.alerts_generated += 1
            
            if new_alerts:
                self.logger.warning(f"Generated {len(new_alerts)} new performance alerts")
            
            return new_alerts
            
        except Exception as e:
            self.logger.error(f"Failed to check alerts: {e}")
            return []
    
    def _create_alert_from_validation(self, validation_result: Dict[str, Any]) -> Optional[PerformanceAlert]:
        """Create a performance alert from a validation result"""
        try:
            import uuid
            
            alert = PerformanceAlert(
                alert_id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                severity=ValidationSeverity(validation_result.get("severity", "info")),
                metric_name=validation_result.get("metric_name", "unknown"),
                current_value=validation_result.get("metric_value", 0.0),
                threshold_value=validation_result.get("threshold", 0.0),
                message=validation_result.get("message", "Performance threshold exceeded"),
                component="performance_validation"
            )
            
            return alert
            
        except Exception as e:
            self.logger.error(f"Failed to create alert from validation: {e}")
            return None
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge a performance alert"""
        try:
            if alert_id in self.active_alerts:
                alert = self.active_alerts[alert_id]
                alert.acknowledged = True
                alert.acknowledged_by = acknowledged_by
                alert.acknowledged_at = datetime.now()
                
                # Move to history
                del self.active_alerts[alert_id]
                
                self.logger.info(f"Alert acknowledged: {alert_id} by {acknowledged_by}")
                return True
            else:
                self.logger.warning(f"Alert not found: {alert_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to acknowledge alert: {e}")
            return False
    
    def get_validation_status(self) -> Dict[str, Any]:
        """Get validation system status"""
        return {
            "validation_active": self.validation_active,
            "total_rules": len(self.validation_rules),
            "total_thresholds": len(self.thresholds),
            "total_validations": self.total_validations,
            "passed_validations": self.passed_validations,
            "failed_validations": self.failed_validations,
            "active_alerts": len(self.active_alerts),
            "total_alerts_generated": self.alerts_generated
        }
    
    def get_active_alerts(self) -> List[PerformanceAlert]:
        """Get all active performance alerts"""
        return list(self.active_alerts.values())
    
    def get_alert_history(self, limit: Optional[int] = None) -> List[PerformanceAlert]:
        """Get alert history with optional limit"""
        if limit is None:
            return self.alert_history.copy()
        else:
            return self.alert_history[-limit:] if self.alert_history else []
    
    def clear_alert_history(self) -> bool:
        """Clear alert history"""
        try:
            self.alert_history.clear()
            self.logger.info("Alert history cleared")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear alert history: {e}")
            return False
