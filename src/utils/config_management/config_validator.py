#!/usr/bin/env python3
"""
Configuration Validator Module - V2 Compliant
============================================

Configuration validation functionality extracted from consolidated_config_management.py
for V2 compliance (≤400 lines).

Provides:
- Configuration validation and verification
- Pattern validation and analysis
- Environment variable validation
- Configuration consistency checking

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config_scanner import ConfigPattern

logger = logging.getLogger(__name__)


@dataclass
class ConfigValidationResult:
    """Result of configuration validation."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


class ConfigurationValidator:
    """Validates configuration patterns and settings."""

    def __init__(self):
        self.required_env_vars = set()
        self.optional_env_vars = set()
        self.config_rules = {}

    def validate_patterns(self, patterns: list[ConfigPattern]) -> ConfigValidationResult:
        """Validate a list of configuration patterns."""
        result = ConfigValidationResult(is_valid=True)
        
        # Group patterns by type
        pattern_groups = {}
        for pattern in patterns:
            pattern_type = pattern.pattern_type
            if pattern_type not in pattern_groups:
                pattern_groups[pattern_type] = []
            pattern_groups[pattern_type].append(pattern)
        
        # Validate each pattern type
        for pattern_type, type_patterns in pattern_groups.items():
            validation_result = self._validate_pattern_type(pattern_type, type_patterns)
            
            if not validation_result.is_valid:
                result.is_valid = False
                result.errors.extend(validation_result.errors)
            
            result.warnings.extend(validation_result.warnings)
            result.suggestions.extend(validation_result.suggestions)
        
        return result

    def _validate_pattern_type(self, pattern_type: str, patterns: list[ConfigPattern]) -> ConfigValidationResult:
        """Validate patterns of a specific type."""
        result = ConfigValidationResult(is_valid=True)
        
        if pattern_type in ["getenv", "environ_get", "environ_direct"]:
            return self._validate_environment_patterns(patterns)
        elif pattern_type in ["json_load_file", "json_loads_string"]:
            return self._validate_json_patterns(patterns)
        elif pattern_type in ["yaml_load_file", "yaml_safe_load"]:
            return self._validate_yaml_patterns(patterns)
        elif pattern_type in ["config_parser", "ini_file_extension"]:
            return self._validate_config_file_patterns(patterns)
        else:
            result.warnings.append(f"Unknown pattern type: {pattern_type}")
        
        return result

    def _validate_environment_patterns(self, patterns: list[ConfigPattern]) -> ConfigValidationResult:
        """Validate environment variable patterns."""
        result = ConfigValidationResult(is_valid=True)
        env_vars = set()
        
        for pattern in patterns:
            env_var = pattern.key
            env_vars.add(env_var)
            
            # Check if environment variable is set
            if env_var not in os.environ:
                if env_var in self.required_env_vars:
                    result.errors.append(f"Required environment variable '{env_var}' is not set")
                    result.is_valid = False
                else:
                    result.warnings.append(f"Environment variable '{env_var}' is not set")
        
        # Check for unused required environment variables
        for required_var in self.required_env_vars:
            if required_var not in env_vars:
                result.warnings.append(f"Required environment variable '{required_var}' is not used in code")
        
        return result

    def _validate_json_patterns(self, patterns: list[ConfigPattern]) -> ConfigValidationResult:
        """Validate JSON configuration patterns."""
        result = ConfigValidationResult(is_valid=True)
        
        for pattern in patterns:
            if pattern.pattern_type == "json_load_file":
                file_path = pattern.key
                if not Path(file_path).exists():
                    result.errors.append(f"JSON configuration file '{file_path}' does not exist")
                    result.is_valid = False
                else:
                    # Validate JSON file content
                    try:
                        import json
                        with open(file_path, 'r') as f:
                            json.load(f)
                    except json.JSONDecodeError as e:
                        result.errors.append(f"Invalid JSON in file '{file_path}': {e}")
                        result.is_valid = False
                    except Exception as e:
                        result.warnings.append(f"Could not validate JSON file '{file_path}': {e}")
        
        return result

    def _validate_yaml_patterns(self, patterns: list[ConfigPattern]) -> ConfigValidationResult:
        """Validate YAML configuration patterns."""
        result = ConfigValidationResult(is_valid=True)
        
        for pattern in patterns:
            if pattern.pattern_type == "yaml_load_file":
                file_path = pattern.key
                if not Path(file_path).exists():
                    result.errors.append(f"YAML configuration file '{file_path}' does not exist")
                    result.is_valid = False
                else:
                    # Validate YAML file content
                    try:
                        import yaml
                        with open(file_path, 'r') as f:
                            yaml.safe_load(f)
                    except yaml.YAMLError as e:
                        result.errors.append(f"Invalid YAML in file '{file_path}': {e}")
                        result.is_valid = False
                    except Exception as e:
                        result.warnings.append(f"Could not validate YAML file '{file_path}': {e}")
        
        return result

    def _validate_config_file_patterns(self, patterns: list[ConfigPattern]) -> ConfigValidationResult:
        """Validate configuration file patterns."""
        result = ConfigValidationResult(is_valid=True)
        
        for pattern in patterns:
            if pattern.pattern_type in ["ini_file_extension", "conf_file_extension", "cfg_file_extension"]:
                file_path = pattern.key
                if not Path(file_path).exists():
                    result.warnings.append(f"Configuration file '{file_path}' referenced but not found")
        
        return result

    def set_required_env_vars(self, env_vars: list[str]):
        """Set required environment variables."""
        self.required_env_vars = set(env_vars)

    def set_optional_env_vars(self, env_vars: list[str]):
        """Set optional environment variables."""
        self.optional_env_vars = set(env_vars)

    def add_config_rule(self, rule_name: str, rule_function: callable):
        """Add a custom configuration validation rule."""
        self.config_rules[rule_name] = rule_function

    def validate_custom_rules(self, patterns: list[ConfigPattern]) -> ConfigValidationResult:
        """Validate patterns against custom rules."""
        result = ConfigValidationResult(is_valid=True)
        
        for rule_name, rule_function in self.config_rules.items():
            try:
                rule_result = rule_function(patterns)
                if not rule_result.is_valid:
                    result.is_valid = False
                    result.errors.extend([f"Rule '{rule_name}': {error}" for error in rule_result.errors])
                result.warnings.extend([f"Rule '{rule_name}': {warning}" for warning in rule_result.warnings])
                result.suggestions.extend([f"Rule '{rule_name}': {suggestion}" for suggestion in rule_result.suggestions])
            except Exception as e:
                result.errors.append(f"Custom rule '{rule_name}' failed: {e}")
                result.is_valid = False
        
        return result

    def generate_validation_report(self, patterns: list[ConfigPattern]) -> str:
        """Generate a detailed validation report."""
        validation_result = self.validate_patterns(patterns)
        
        report = []
        report.append("=== Configuration Validation Report ===")
        report.append(f"Overall Status: {'✅ VALID' if validation_result.is_valid else '❌ INVALID'}")
        report.append(f"Patterns Analyzed: {len(patterns)}")
        report.append("")
        
        if validation_result.errors:
            report.append("🚨 ERRORS:")
            for error in validation_result.errors:
                report.append(f"  - {error}")
            report.append("")
        
        if validation_result.warnings:
            report.append("⚠️  WARNINGS:")
            for warning in validation_result.warnings:
                report.append(f"  - {warning}")
            report.append("")
        
        if validation_result.suggestions:
            report.append("💡 SUGGESTIONS:")
            for suggestion in validation_result.suggestions:
                report.append(f"  - {suggestion}")
            report.append("")
        
        # Pattern summary
        pattern_summary = {}
        for pattern in patterns:
            pattern_type = pattern.pattern_type
            pattern_summary[pattern_type] = pattern_summary.get(pattern_type, 0) + 1
        
        report.append("📊 Pattern Summary:")
        for pattern_type, count in sorted(pattern_summary.items()):
            report.append(f"  - {pattern_type}: {count}")
        
        return "\n".join(report)


if __name__ == "__main__":
    # Example usage
    validator = ConfigurationValidator()
    
    # Set required environment variables
    validator.set_required_env_vars(["API_KEY", "DATABASE_URL"])
    
    # Create sample patterns
    from .config_scanner import ConfigPattern
    sample_patterns = [
        ConfigPattern(
            file_path=Path("test.py"),
            line_number=1,
            pattern_type="getenv",
            key="API_KEY",
            value=None,
            context="api_key = os.getenv('API_KEY')",
            source="environment_variable"
        ),
        ConfigPattern(
            file_path=Path("test.py"),
            line_number=2,
            pattern_type="getenv",
            key="OPTIONAL_VAR",
            value=None,
            context="optional = os.getenv('OPTIONAL_VAR')",
            source="environment_variable"
        )
    ]
    
    # Validate patterns
    result = validator.validate_patterns(sample_patterns)
    report = validator.generate_validation_report(sample_patterns)
    
    print(report)
