"""
Standard SSOT Validator
=======================

Handles standard field validation for SSOT components.
Extracted from validator.py for improved modularity.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from datetime import datetime
from typing import Any

from ..models import SSOTComponent, SSOTComponentType


class StandardValidator:
    """Handles standard SSOT component validation."""

    def __init__(self):
        """Initialize the standard validator."""
        self.logger = logging.getLogger(__name__)


def get_example_usage():
    """
    Example usage for StandardValidator.
    
    # Import the core component
    from src.core.ssot.unified_ssot.validators.standard_validator import StandardValidator

# Import the core component
from src.core.ssot.unified_ssot.validators.standard_validator import Standard_Validator

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Standard_Validator(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

        """Initialize standard validator."""
        self.validation_rules = {
            "valid_priorities": ["low", "medium", "high", "critical"],
            "valid_statuses": ["active", "inactive", "deprecated", "maintenance"],
            "max_age_days": (365),  # Components shouldn't be older than 1 year without updates
            "min_update_frequency_days": 30,
        }

    def validate_standard_fields(self, component: SSOTComponent) -> list[str]:
        """Validate standard component fields."""
        issues = []

        try:
            # Check priority if present
            if hasattr(component, "priority") and component.priority:
                if component.priority.lower() not in self.validation_rules["valid_priorities"]:
                    issues.append(f"Invalid priority: {component.priority}")

            # Check status if present
            if hasattr(component, "status") and component.status:
                if component.status.lower() not in self.validation_rules["valid_statuses"]:
                    issues.append(f"Invalid status: {component.status}")

            # Check component age
            if hasattr(component, "created_at") and component.created_at:
                age = datetime.now() - component.created_at
                if age.days > self.validation_rules["max_age_days"]:
                    issues.append(f"Component is too old ({age.days} days)")

            # Check update frequency
            if hasattr(component, "updated_at") and component.updated_at:
                days_since_update = (datetime.now() - component.updated_at).days
                if days_since_update > self.validation_rules["min_update_frequency_days"]:
                    issues.append(f"Component not updated recently ({days_since_update} days)")

            # Check configuration if present
            if hasattr(component, "configuration") and component.configuration:
                config_issues = self._validate_configuration(component.configuration)
                issues.extend(config_issues)

        except Exception as e:
            issues.append(f"Standard validation error: {str(e)}")

        return issues

    def validate_component_relationships(self, component: SSOTComponent) -> list[str]:
        """Validate component relationships."""
        issues = []

        try:
            # Check parent-child relationships
            if hasattr(component, "parent_id") and hasattr(component, "children"):
                if component.parent_id and component.children:
                    issues.append("Component cannot have both parent and children")

            # Check circular dependencies
            if hasattr(component, "dependencies") and component.dependencies:
                if (
                    hasattr(component, "component_id")
                    and component.component_id in component.dependencies
                ):
                    issues.append("Component cannot depend on itself")

            # Check component type consistency
            if hasattr(component, "component_type") and hasattr(component, "parent_id"):
                if component.component_type == SSOTComponentType.ROOT and component.parent_id:
                    issues.append("Root component cannot have a parent")

        except Exception as e:
            issues.append(f"Relationship validation error: {str(e)}")

        return issues

    def _validate_configuration(self, configuration: dict[str, Any]) -> list[str]:
        """Validate component configuration."""
        issues = []

        try:
            if not isinstance(configuration, dict):
                issues.append("Configuration must be a dictionary")
                return issues

            # Check for required configuration keys based on component type
            required_keys = ["enabled", "settings"]
            for key in required_keys:
                if key not in configuration:
                    issues.append(f"Missing required configuration key: {key}")

            # Validate settings if present
            if "settings" in configuration:
                settings = configuration["settings"]
                if not isinstance(settings, dict):
                    issues.append("Configuration settings must be a dictionary")
                else:
                    # Check for circular references in settings
                    if self._has_circular_reference(settings):
                        issues.append("Configuration has circular references")

        except Exception as e:
            issues.append(f"Configuration validation error: {str(e)}")

        return issues

    def _has_circular_reference(self, data: Any, visited: set = None) -> bool:
        """Check for circular references in configuration data."""
        if visited is None:
            visited = set()

        try:
            if isinstance(data, dict):
                for key, value in data.items():
                    if id(value) in visited:
                        return True
                    visited.add(id(value))
                    if self._has_circular_reference(value, visited):
                        return True
                    visited.remove(id(value))
            elif isinstance(data, list):
                for item in data:
                    if id(item) in visited:
                        return True
                    visited.add(id(item))
                    if self._has_circular_reference(item, visited):
                        return True
                    visited.remove(id(item))

            return False

        except Exception:
            return False

    def get_validation_score(self, issues: list[str]) -> float:
        """Calculate validation score based on issues."""
        try:
            base_score = 100.0
            # Deduct 5 points per standard issue
            score = base_score - (len(issues) * 5)
            return max(0.0, score)  # Ensure score doesn't go below 0
        except Exception:
            return 0.0
