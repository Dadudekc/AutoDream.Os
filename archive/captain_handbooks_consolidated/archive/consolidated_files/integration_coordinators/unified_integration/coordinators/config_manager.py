"""
Config Manager - V2 Compliant Module
===================================

Handles configuration management and export.
Extracted from coordinator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from collections.abc import Callable
from datetime import datetime
from typing import Any

from ..models import IntegrationConfig, IntegrationModels, IntegrationType


class ConfigManager:
    """Handles configuration management and export.

    Manages configuration settings, export functionality, and configuration validation.
    """

    def __init__(self, config: IntegrationConfig):
        """Initialize config manager."""
        self.config = config
        self.config_history: list[dict[str, Any]] = []
        self.export_history: list[dict[str, Any]] = []

    def export_configuration(
        self,
        integration_handlers: dict[IntegrationType, Callable],
        alert_thresholds: dict[str, float],
        optimizer_status: dict[str, Any],
    ) -> dict[str, Any]:
        """Export coordination configuration."""
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "config": self.config.__dict__,
            "alert_thresholds": alert_thresholds,
            "registered_integrations": [t.value for t in integration_handlers.keys()],
            "optimization_status": optimizer_status,
        }

        # Record export
        self.export_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "export_type": "full_configuration",
                "integration_count": len(integration_handlers),
            }
        )

        return export_data

    def validate_configuration(self) -> dict[str, Any]:
        """Validate current configuration."""
        validation_results = {"valid": True, "errors": [], "warnings": []}

        # Validate config object
        if not self.config:
            validation_results["valid"] = False
            validation_results["errors"].append("Configuration is None")
            return validation_results

        # Validate required fields
        required_fields = [
            "max_concurrent_requests",
            "timeout_seconds",
            "retry_attempts",
        ]
        for field in required_fields:
            if not hasattr(self.config, field):
                validation_results["valid"] = False
                validation_results["errors"].append(f"Missing required field: {field}")

        # Validate numeric fields
        numeric_fields = [
            "max_concurrent_requests",
            "timeout_seconds",
            "retry_attempts",
        ]
        for field in numeric_fields:
            if hasattr(self.config, field):
                value = getattr(self.config, field)
                if not isinstance(value, (int, float)) or value <= 0:
                    validation_results["warnings"].append(f"Invalid {field}: {value}")

        return validation_results

    def update_configuration(self, updates: dict[str, Any]) -> dict[str, Any]:
        """Update configuration with new values."""
        update_results = {"success": True, "updated_fields": [], "errors": []}

        try:
            for field, value in updates.items():
                if hasattr(self.config, field):
                    old_value = getattr(self.config, field)
                    setattr(self.config, field, value)
                    update_results["updated_fields"].append(
                        {"field": field, "old_value": old_value, "new_value": value}
                    )
                else:
                    update_results["errors"].append(f"Unknown field: {field}")

            # Record configuration change
            self.config_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "updated_fields": update_results["updated_fields"],
                    "errors": update_results["errors"],
                }
            )

        except Exception as e:
            update_results["success"] = False
            update_results["errors"].append(f"Update failed: {str(e)}")

        return update_results

    def get_configuration_summary(self) -> dict[str, Any]:
        """Get configuration summary."""
        return {
            "config_type": type(self.config).__name__,
            "config_fields": list(self.config.__dict__.keys()),
            "config_history_count": len(self.config_history),
            "export_history_count": len(self.export_history),
            "last_export": (self.export_history[-1]["timestamp"] if self.export_history else None),
            "last_update": (self.config_history[-1]["timestamp"] if self.config_history else None),
        }

    def get_configuration_history(self, hours: int = 24) -> list[dict[str, Any]]:
        """Get configuration history."""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)

        return [
            record
            for record in self.config_history
            if datetime.fromisoformat(record["timestamp"]).timestamp() >= cutoff_time
        ]

    def reset_configuration(self) -> dict[str, Any]:
        """Reset configuration to defaults."""
        try:
            # Create new default config
            self.config = IntegrationModels.create_integration_config()

            # Record reset
            self.config_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "action": "reset_to_defaults",
                    "new_config": self.config.__dict__,
                }
            )

            return {
                "success": True,
                "message": "Configuration reset to defaults",
                "new_config": self.config.__dict__,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_manager_status(self) -> dict[str, Any]:
        """Get config manager status."""
        return {
            "config_history_count": len(self.config_history),
            "export_history_count": len(self.export_history),
            "configuration_valid": self.validate_configuration()["valid"],
        }
