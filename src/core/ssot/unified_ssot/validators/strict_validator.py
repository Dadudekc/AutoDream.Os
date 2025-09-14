"""
Strict SSOT Validator
=====================

Handles strict validation for SSOT components.
Extracted from validator.py for improved modularity.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from typing import Any

from ..models import SSOTComponent, SSOTExecutionPhase


class StrictValidator:
    """Handles strict SSOT component validation."""

    def __init__(self):
        """Initialize the strict validator."""
        self.logger = logging.getLogger(__name__)


def get_example_usage():
    """
    Example usage for StrictValidator.
    
    # Import the core component
    from src.core.ssot.unified_ssot.validators.strict_validator import StrictValidator

# Import the core component
from src.core.ssot.unified_ssot.validators.strict_validator import Strict_Validator

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Strict_Validator(config)

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

        """Initialize strict validator."""
        self.validation_rules = {
            "required_documentation": ["description", "usage_examples"],
            "min_description_length": 50,
            "required_metadata": ["author", "created_at", "version"],
            "performance_thresholds": {
                "max_execution_time": 30.0,  # seconds
                "max_memory_usage": 512,  # MB
            },
        }

    def validate_strict_requirements(self, component: SSOTComponent) -> list[str]:
        """Validate strict component requirements."""
        issues = []

        try:
            # Check required documentation
            for doc_field in self.validation_rules["required_documentation"]:
                if not hasattr(component, doc_field) or not getattr(component, doc_field):
                    issues.append(f"Missing required documentation: {doc_field}")
                elif doc_field == "description":
                    desc = getattr(component, doc_field)
                    if len(desc) < self.validation_rules["min_description_length"]:
                        issues.append(
                            f"Description too short (minimum {self.validation_rules['min_description_length']} characters)"
                        )

            # Check required metadata
            for meta_field in self.validation_rules["required_metadata"]:
                if not hasattr(component, meta_field) or not getattr(component, meta_field):
                    issues.append(f"Missing required metadata: {meta_field}")

            # Check performance metrics if available
            if hasattr(component, "performance_metrics") and component.performance_metrics:
                perf_issues = self._validate_performance_metrics(component.performance_metrics)
                issues.extend(perf_issues)

            # Check security requirements
            security_issues = self._validate_security_requirements(component)
            issues.extend(security_issues)

        except Exception as e:
            issues.append(f"Strict validation error: {str(e)}")

        return issues

    def validate_component_integrity(self, component: SSOTComponent) -> list[str]:
        """Validate component integrity and consistency."""
        issues = []

        try:
            # Check data consistency
            if hasattr(component, "created_at") and hasattr(component, "updated_at"):
                if component.created_at and component.updated_at:
                    if component.updated_at < component.created_at:
                        issues.append("Updated timestamp cannot be before created timestamp")

            # Check component completeness
            if hasattr(component, "execution_phases") and component.execution_phases:
                phase_issues = self._validate_execution_phases(component.execution_phases)
                issues.extend(phase_issues)

            # Check resource allocations
            if hasattr(component, "resource_requirements") and component.resource_requirements:
                resource_issues = self._validate_resource_requirements(
                    component.resource_requirements
                )
                issues.extend(resource_issues)

        except Exception as e:
            issues.append(f"Integrity validation error: {str(e)}")

        return issues

    def _validate_performance_metrics(self, metrics: dict[str, Any]) -> list[str]:
        """Validate performance metrics."""
        issues = []

        try:
            thresholds = self.validation_rules["performance_thresholds"]

            # Check execution time
            if "execution_time" in metrics:
                exec_time = metrics["execution_time"]
                if (
                    isinstance(exec_time, (int, float))
                    and exec_time > thresholds["max_execution_time"]
                ):
                    issues.append(
                        f"Execution time exceeds threshold ({exec_time}s > {thresholds['max_execution_time']}s)"
                    )

            # Check memory usage
            if "memory_usage" in metrics:
                memory = metrics["memory_usage"]
                if isinstance(memory, (int, float)) and memory > thresholds["max_memory_usage"]:
                    issues.append(
                        f"Memory usage exceeds threshold ({memory}MB > {thresholds['max_memory_usage']}MB)"
                    )

        except Exception as e:
            issues.append(f"Performance metrics validation error: {str(e)}")

        return issues

    def _validate_security_requirements(self, component: SSOTComponent) -> list[str]:
        """Validate security requirements."""
        issues = []

        try:
            # Check for sensitive data exposure
            if hasattr(component, "configuration") and component.configuration:
                config = component.configuration
                sensitive_keys = ["password", "token", "key", "secret", "credential"]

                for key, value in config.items():
                    if any(sensitive in key.lower() for sensitive in sensitive_keys):
                        if isinstance(value, str) and len(value) > 0:
                            issues.append(
                                f"Potential sensitive data exposure in configuration key: {key}"
                            )

            # Check access controls
            if hasattr(component, "access_controls") and component.access_controls:
                if not isinstance(component.access_controls, dict):
                    issues.append("Access controls must be a dictionary")
                elif not component.access_controls:
                    issues.append("Access controls cannot be empty")

        except Exception as e:
            issues.append(f"Security validation error: {str(e)}")

        return issues

    def _validate_execution_phases(self, phases: list[SSOTExecutionPhase]) -> list[str]:
        """Validate execution phases."""
        issues = []

        try:
            if not isinstance(phases, list):
                issues.append("Execution phases must be a list")
                return issues

            phase_names = set()
            for i, phase in enumerate(phases):
                if not hasattr(phase, "name") or not phase.name:
                    issues.append(f"Phase {i} missing name")
                elif phase.name in phase_names:
                    issues.append(f"Duplicate phase name: {phase.name}")
                else:
                    phase_names.add(phase.name)

        except Exception as e:
            issues.append(f"Execution phases validation error: {str(e)}")

        return issues

    def _validate_resource_requirements(self, requirements: dict[str, Any]) -> list[str]:
        """Validate resource requirements."""
        issues = []

        try:
            required_resources = ["cpu", "memory", "storage"]

            for resource in required_resources:
                if resource not in requirements:
                    issues.append(f"Missing resource requirement: {resource}")
                else:
                    value = requirements[resource]
                    if not isinstance(value, (int, float)) or value <= 0:
                        issues.append(f"Invalid {resource} requirement: {value}")

        except Exception as e:
            issues.append(f"Resource requirements validation error: {str(e)}")

        return issues

    def get_validation_score(self, issues: list[str]) -> float:
        """Calculate validation score based on issues."""
        try:
            base_score = 100.0
            # Deduct 3 points per strict issue
            score = base_score - (len(issues) * 3)
            return max(0.0, score)  # Ensure score doesn't go below 0
        except Exception:
            return 0.0
