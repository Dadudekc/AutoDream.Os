
# MIGRATED: This file has been migrated to the centralized configuration system
"""
Config Validator - Unified Validation Framework

This module provides configuration validation functionality, inheriting from BaseValidator
and following the unified validation framework patterns.
"""

from typing import Dict, List, Any, Callable
from .base_validator import (
    BaseValidator,
    ValidationRule,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class ConfigValidator(BaseValidator):
    """Validates configuration data using unified validation framework"""

    def __init__(self, validators: Dict[str, Callable[[Dict[str, Any]], bool]] = None):
        """Initialize config validator with optional custom validators"""
        super().__init__("ConfigValidator")
        self.custom_validators = validators or {}

    def validate(
        self, configs: Dict[str, Dict[str, Any]], **kwargs
    ) -> List[ValidationResult]:
        """Validate configuration data and return validation results.

        Returns:
            List[ValidationResult]: Validation results produced during
            configuration validation.
        """
        results = []

        try:
            # Validate configuration structure
            structure_results = self._validate_config_structure(configs)
            results.extend(structure_results)

            # Validate required sections if specified
            required_sections = kwargs.get("required_sections", [])
            if required_sections:
                section_results = self._validate_required_sections(
                    configs, required_sections
                )
                results.extend(section_results)

            # Run section-specific validators
            validator_results = self._run_section_validators(configs)
            results.extend(validator_results)

            # Check configuration consistency
            consistency_results = self._validate_config_consistency(configs)
            results.extend(consistency_results)

            # Add overall success result if no critical errors
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                success_result = self._create_result(
                    rule_id="overall_config_validation",
                    rule_name="Overall Configuration Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Configuration validation passed successfully",
                    details={
                        "total_sections": len(configs),
                        "total_checks": len(results),
                    },
                )
                results.append(success_result)

        except Exception as e:
            error_result = self._create_result(
                rule_id="config_validation_error",
                rule_name="Configuration Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Configuration validation error: {str(e)}",
                details={"error_type": type(e).__name__},
            )
            results.append(error_result)

        return results

    def _validate_config_structure(
        self, configs: Dict[str, Dict[str, Any]]
    ) -> List[ValidationResult]:
        """Validate configuration structure and format"""
        results = []

        if not isinstance(configs, dict):
            result = self._create_result(
                rule_id="config_type",
                rule_name="Configuration Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Configuration must be a dictionary",
                actual_value=type(configs).__name__,
                expected_value="dict",
            )
            results.append(result)
            return results

        if len(configs) == 0:
            result = self._create_result(
                rule_id="config_empty",
                rule_name="Configuration Empty Check",
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.WARNING,
                message="Configuration is empty",
                actual_value=configs,
                expected_value="non-empty configuration",
            )
            results.append(result)
            return results

        # Validate each section is a dictionary
        for section_name, section_data in configs.items():
            if not isinstance(section_data, dict):
                result = self._create_result(
                    rule_id=f"section_{section_name}_type",
                    rule_name=f"Section {section_name} Type Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Section '{section_name}' must be a dictionary",
                    field_path=section_name,
                    actual_value=type(section_data).__name__,
                    expected_value="dict",
                )
                results.append(result)

        return results

    def _validate_required_sections(
        self, configs: Dict[str, Dict[str, Any]], required_sections: List[str]
    ) -> List[ValidationResult]:
        """Validate that all required sections are present"""
        results = []

        for section_name in required_sections:
            if section_name not in configs:
                result = self._create_result(
                    rule_id=f"required_section_{section_name}",
                    rule_name=f"Required Section: {section_name}",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Required configuration section '{section_name}' is missing",
                    field_path=section_name,
                    actual_value="missing",
                    expected_value="present",
                )
                results.append(result)

        return results

    def _run_section_validators(
        self, configs: Dict[str, Dict[str, Any]]
    ) -> List[ValidationResult]:
        """Run section-specific validation functions"""
        results = []

        for section_name, section_data in configs.items():
            validator = self.custom_validators.get(section_name)
            if validator and callable(validator):
                try:
                    is_valid = validator(section_data)
                    if not is_valid:
                        result = self._create_result(
                            rule_id=f"section_validator_{section_name}",
                            rule_name=f"Section Validator: {section_name}",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Section '{section_name}' failed custom validation",
                            field_path=section_name,
                            actual_value=section_data,
                            expected_value="valid configuration",
                        )
                        results.append(result)
                except Exception as e:
                    result = self._create_result(
                        rule_id=f"section_validator_error_{section_name}",
                        rule_name=f"Section Validator Error: {section_name}",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Section '{section_name}' validator error: {str(e)}",
                        field_path=section_name,
                        details={"error_type": type(e).__name__},
                    )
                    results.append(result)

        return results

    def _validate_config_consistency(
        self, configs: Dict[str, Dict[str, Any]]
    ) -> List[ValidationResult]:
        """Check for configuration consistency across sections"""
        results = []

        # Check for duplicate keys across sections
        all_keys = set()
        duplicate_keys = set()

        for section_name, section_data in configs.items():
            if isinstance(section_data, dict):
                for key in section_data.keys():
                    if key in all_keys:
                        duplicate_keys.add(key)
                    all_keys.add(key)

        if duplicate_keys:
            result = self._create_result(
                rule_id="duplicate_keys",
                rule_name="Duplicate Keys Check",
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.WARNING,
                message=f"Duplicate keys found across sections: {list(duplicate_keys)}",
                details={"duplicate_keys": list(duplicate_keys)},
            )
            results.append(result)

        # Check for conflicting values (basic check)
        # This could be extended with more sophisticated conflict detection
        for key in all_keys:
            values = []
            for section_data in configs.values():
                if isinstance(section_data, dict) and key in section_data:
                    values.append(section_data[key])

            if len(set(values)) > 1:
                result = self._create_result(
                    rule_id=f"conflicting_values_{key}",
                    rule_name=f"Conflicting Values: {key}",
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.WARNING,
                    message=f"Conflicting values for key '{key}' across sections",
                    details={"key": key, "values": values},
                )
                results.append(result)

        return results

    def add_section_validator(
        self, section_name: str, validator: Callable[[Dict[str, Any]], bool]
    ) -> bool:
        """Add a custom validator for a specific configuration section"""
        try:
            self.custom_validators[section_name] = validator
            self.logger.info(f"Section validator added for: {section_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add section validator: {e}")
            return False

    def remove_section_validator(self, section_name: str) -> bool:
        """Remove a custom validator for a specific configuration section"""
        try:
            if section_name in self.custom_validators:
                del self.custom_validators[section_name]
                self.logger.info(f"Section validator removed for: {section_name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove section validator: {e}")
            return False

    # ConfigManagerValidator functionality integration
    def validate_config_sections(
        self, configs: Dict[str, Dict[str, Any]]
    ) -> Dict[str, bool]:
        """Validate configuration sections using custom validators (from ConfigManagerValidator)"""
        results: Dict[str, bool] = {}

        try:
            for name, data in configs.items():
                validator = self.custom_validators.get(name)
                if validator is None:
                    # No validator specified, assume valid
                    results[name] = True
                    continue

                try:
                    results[name] = bool(validator(data))
                except Exception:
                    # Any exception during validation means invalid
                    results[name] = False

        except Exception as e:
            self.logger.error(f"Config section validation failed: {e}")
            # Return empty results on error
            results = {}

        return results

    def get_validation_summary(
        self, configs: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Get validation summary for configuration sections"""
        try:
            section_results = self.validate_config_sections(configs)

            total_sections = len(section_results)
            valid_sections = sum(1 for valid in section_results.values() if valid)
            invalid_sections = total_sections - valid_sections

            return {
                "total_sections": total_sections,
                "valid_sections": valid_sections,
                "invalid_sections": invalid_sections,
                "pass_rate": (valid_sections / total_sections * 100)
                if total_sections > 0
                else 0,
                "section_results": section_results,
                "timestamp": self._get_current_timestamp(),
            }

        except Exception as e:
            self.logger.error(f"Failed to get validation summary: {e}")
            return {"error": str(e)}

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime

        return datetime.now().isoformat()
