"""Rule management for performance validation."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List

from .validation_constants import DEFAULT_THRESHOLDS


class RuleManager:
    """Manage validation rules and metric thresholds."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.RuleManager")
        self.validation_rules: List[Dict[str, Any]] = []
        self.thresholds: Dict[str, Dict[str, Any]] = DEFAULT_THRESHOLDS.copy()

    def add_validation_rule(self, rule: Dict[str, Any]) -> None:
        """Add a new validation rule.

        Parameters
        ----------
        rule: Dict[str, Any]
            Rule configuration to add.
        """
        rule["id"] = f"rule_{len(self.validation_rules) + 1}"
        rule["created_at"] = datetime.now().isoformat()
        self.validation_rules.append(rule)
        self.logger.info("✅ Added validation rule: %s", rule["id"])

    def set_threshold(self, metric_name: str, severity: str, value: float, operator: str = ">=") -> None:
        """Configure a threshold for a metric."""
        if metric_name not in self.thresholds:
            self.thresholds[metric_name] = {}
        self.thresholds[metric_name][severity] = value
        self.thresholds[metric_name]["operator"] = operator
        self.logger.info("✅ Set %s threshold for %s: %s", severity, metric_name, value)

    def get_thresholds(self) -> Dict[str, Dict[str, Any]]:
        """Return current threshold configuration."""
        return self.thresholds.copy()

    def remove_threshold(self, metric_name: str) -> bool:
        """Remove threshold configuration for a metric."""
        if metric_name in self.thresholds:
            del self.thresholds[metric_name]
            self.logger.info("✅ Removed threshold for %s", metric_name)
            return True
        return False

    def export_validation_config(self) -> Dict[str, Any]:
        """Export current validation configuration for persistence."""
        return {
            "export_timestamp": datetime.now().isoformat(),
            "thresholds": self.thresholds,
            "validation_rules": self.validation_rules,
            "total_rules": len(self.validation_rules),
            "total_thresholds": len(self.thresholds),
        }

    def reset(self) -> None:
        """Reset rules and thresholds to defaults."""
        self.validation_rules.clear()
        self.thresholds = DEFAULT_THRESHOLDS.copy()
        self.logger.info("✅ RuleManager reset to defaults")
