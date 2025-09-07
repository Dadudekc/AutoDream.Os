"""Performance Validation Engine orchestrating rule management, execution, and reporting."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from .rule_management import RuleManager
from .validation_executor import ValidationExecutor
from .validation_reporting import ValidationReporter
from .validation_types import ValidationResult, ValidationSummary


class ValidationEngine:
    """Validate performance metrics using modular components."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.ValidationEngine")
        self.rule_manager = RuleManager()
        self.executor = ValidationExecutor(self.rule_manager)
        self.reporter = ValidationReporter()
        self.logger.info("✅ Validation Engine initialized successfully")

    # Rule management -------------------------------------------------
    def add_validation_rule(self, rule: Dict[str, Any]) -> None:
        """Add a new validation rule."""
        self.rule_manager.add_validation_rule(rule)

    def set_threshold(self, metric_name: str, severity: str, value: float, operator: str = ">=") -> None:
        """Set a threshold for a metric."""
        self.rule_manager.set_threshold(metric_name, severity, value, operator)

    def get_thresholds(self) -> Dict[str, Dict[str, Any]]:
        """Return configured thresholds."""
        return self.rule_manager.get_thresholds()

    def remove_threshold(self, metric_name: str) -> bool:
        """Remove threshold for a metric."""
        return self.rule_manager.remove_threshold(metric_name)

    def export_validation_config(self) -> Dict[str, Any]:
        """Export current validation configuration."""
        return self.rule_manager.export_validation_config()

    # Validation execution -------------------------------------------
    def validate_metrics(self, metrics: Dict[str, Any]) -> List[ValidationResult]:
        """Validate metrics against thresholds and rules."""
        results = self.executor.validate_metrics(metrics)
        self.reporter.record_results(results)
        return results

    # Reporting -------------------------------------------------------
    def get_validation_summary(self) -> ValidationSummary:
        """Return a summary of validation results."""
        return self.reporter.get_validation_summary()

    def get_recent_validations(self, count: int = 100) -> List[ValidationResult]:
        """Return recent validation results."""
        return self.reporter.get_recent_validations(count)

    def clear_validation_history(self) -> None:
        """Clear stored validation results."""
        self.reporter.clear_validation_history()

    # Maintenance -----------------------------------------------------
    def reset(self) -> None:
        """Reset engine to initial state."""
        self.clear_validation_history()
        self.rule_manager.reset()
        self.logger.info("✅ Validation Engine reset to initial state")
