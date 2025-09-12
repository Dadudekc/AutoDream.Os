#!/usr/bin/env python3
"""
🐝 CONSOLIDATED CONFIGURATION MANAGEMENT SYSTEM
Phase 2 Batch 2A: Unified Configuration Infrastructure

This module consolidates all configuration management functionality from:
- config_consolidator.py (orchestration)
- config_scanners.py (scanning)
- config_core.py (core config)
- unified_config_utils.py (utilities)

Provides:
- Unified configuration scanning and analysis
- Pattern detection and consolidation
- Environment variable management
- Configuration validation and consolidation
- Single source of truth for configuration management
"""

from __future__ import annotations

import json
import logging
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

logger = logging.getLogger(__name__)


@dataclass
class ConfigPattern:
    """Represents a configuration pattern found in code."""
    file_path: Path
    line_number: int
    pattern_type: str
    key: str
    value: Any
    context: str
    source: str
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfigValidationResult:
    """Result of configuration validation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class ConfigConsolidationResult:
    """Result of configuration consolidation."""
    patterns_found: int
    files_scanned: int
    consolidation_suggestions: List[str]
    validation_results: ConfigValidationResult
    consolidated_config: Dict[str, Any] = field(default_factory=dict)


class ConfigurationScanner(ABC):
    """Abstract base class for configuration scanners."""

    @abstractmethod
    def scan_file(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Scan a file for configuration patterns."""
        pass

    @abstractmethod
    def get_pattern_types(self) -> List[str]:
        """Get the types of patterns this scanner detects."""
        pass


class EnvironmentVariableScanner(ConfigurationScanner):
    """Scans for environment variable usage patterns."""

    def get_pattern_types(self) -> List[str]:
        return ["env_var", "getenv", "environ"]

    def scan_file(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Scan for environment variable patterns."""
        patterns = []
        env_patterns = [
            (r'os\.getenv\(["\']([^"\']+)["\']', "getenv"),
            (r'os\.environ\.get\(["\']([^"\']+)["\']', "environ_get"),
            (r'os\.environ\["([^"]+)"\]', "environ_direct"),
            (r'os\.environ\[\'([^\']+)\'\]', "environ_direct"),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, pattern_type in env_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    var_name = match.group(1)
                    patterns.append(ConfigPattern(
                        file_path=file_path,
                        line_number=i,
                        pattern_type=pattern_type,
                        key=var_name,
                        value=f"os.getenv('{var_name}')",
                        context=line.strip(),
                        source="environment_variable",
                        confidence=0.9
                    ))

        return patterns


class HardcodedValueScanner(ConfigurationScanner):
    """Scans for hardcoded configuration values."""

    def get_pattern_types(self) -> List[str]:
        return ["hardcoded_string", "hardcoded_number", "hardcoded_bool"]

    def scan_file(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Scan for hardcoded values that might be configuration."""
        patterns = []

        # Skip certain file types
        if file_path.suffix in ['.pyc', '.pyo', '.pyd']:
            return patterns
        if 'test' in file_path.name.lower():
            return patterns

        # Look for potential config patterns
        config_indicators = [
            'host', 'port', 'url', 'path', 'dir', 'file', 'timeout', 'retry',
            'max', 'min', 'default', 'config', 'setting'
        ]

        for i, line in enumerate(lines, 1):
            line_lower = line.lower()

            # Check for config-like variable assignments
            if '=' in line and any(indicator in line_lower for indicator in config_indicators):
                # Extract variable name and value
                parts = line.split('=', 1)
                if len(parts) == 2:
                    var_name = parts[0].strip()
                    var_value = parts[1].strip()

                    # Skip imports, function calls, etc.
                    if not any(skip in var_name.lower() for skip in ['import', 'from', 'def ', 'class ']):
                        patterns.append(ConfigPattern(
                            file_path=file_path,
                            line_number=i,
                            pattern_type="hardcoded_value",
                            key=var_name,
                            value=var_value,
                            context=line.strip(),
                            source="hardcoded_assignment",
                            confidence=0.6
                        ))

        return patterns


class ConfigConstantScanner(ConfigurationScanner):
    """Scans for configuration constants."""

    def get_pattern_types(self) -> List[str]:
        return ["constant", "config_constant"]

    def scan_file(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Scan for configuration constants."""
        patterns = []

        # Look for ALL_CAPS variable assignments (potential constants)
        constant_pattern = re.compile(r'^([A-Z][A-Z0-9_]*)\s*=\s*(.+)')

        for i, line in enumerate(lines, 1):
            match = constant_pattern.match(line.strip())
            if match:
                const_name = match.group(1)
                const_value = match.group(2).strip()

                # Check if it looks like configuration
                config_keywords = ['host', 'port', 'url', 'path', 'timeout', 'max', 'min', 'default']
                if any(keyword in const_name.lower() for keyword in config_keywords):
                    patterns.append(ConfigPattern(
                        file_path=file_path,
                        line_number=i,
                        pattern_type="config_constant",
                        key=const_name,
                        value=const_value,
                        context=line.strip(),
                        source="constant_definition",
                        confidence=0.8
                    ))

        return patterns


class SettingsPatternScanner(ConfigurationScanner):
    """Scans for settings.py style configuration patterns."""

    def get_pattern_types(self) -> List[str]:
        return ["django_settings", "flask_config", "app_config"]

    def scan_file(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Scan for application configuration patterns."""
        patterns = []

        # Look for common config patterns
        config_patterns = [
            (r'DEBUG\s*=\s*(True|False)', "debug_setting"),
            (r'SECRET_KEY\s*=\s*["\'][^"\']+["\']', "secret_key"),
            (r'DATABASE_URL\s*=\s*["\'][^"\']+["\']', "database_url"),
            (r'ALLOWED_HOSTS\s*=\s*\[.*\]', "allowed_hosts"),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, pattern_type in config_patterns:
                if re.search(pattern, line):
                    patterns.append(ConfigPattern(
                        file_path=file_path,
                        line_number=i,
                        pattern_type=pattern_type,
                        key=pattern_type.upper(),
                        value=line.strip(),
                        context=line.strip(),
                        source="settings_pattern",
                        confidence=0.7
                    ))

        return patterns


class UnifiedConfigurationManager:
    """
    Unified configuration management system.

    Consolidates all configuration-related functionality into a single,
    cohesive system for managing application configuration.
    """

    def __init__(self, scan_directories: Optional[List[str]] = None):
        self.scan_directories = scan_directories or ["src"]
        self.scanners: List[ConfigurationScanner] = []
        self.scan_results: Dict[str, List[ConfigPattern]] = {}
        self.consolidated_config: Dict[str, Any] = {}

        # Initialize default scanners
        self._initialize_scanners()

    def _initialize_scanners(self) -> None:
        """Initialize all available configuration scanners."""
        self.scanners = [
            EnvironmentVariableScanner(),
            HardcodedValueScanner(),
            ConfigConstantScanner(),
            SettingsPatternScanner(),
        ]

    def add_scanner(self, scanner: ConfigurationScanner) -> None:
        """Add a custom configuration scanner."""
        self.scanners.append(scanner)

    def scan_configurations(self, directories: Optional[List[str]] = None) -> Dict[str, List[ConfigPattern]]:
        """Scan specified directories for configuration patterns."""
        scan_dirs = directories or self.scan_directories
        self.scan_results = {}

        for dir_path in scan_dirs:
            directory = Path(dir_path)
            if directory.exists():
                self._scan_directory(directory)

        return self.scan_results

    def _scan_directory(self, directory: Path) -> None:
        """Recursively scan a directory for configuration patterns."""
        for file_path in directory.rglob("*.py"):
            if file_path.is_file():
                self._scan_file(file_path)

    def _scan_file(self, file_path: Path) -> None:
        """Scan a single file for configuration patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            all_patterns = []
            for scanner in self.scanners:
                try:
                    patterns = scanner.scan_file(file_path, lines)
                    all_patterns.extend(patterns)
                except Exception as e:
                    logger.warning(f"Scanner {scanner.__class__.__name__} failed on {file_path}: {e}")

            if all_patterns:
                self.scan_results[str(file_path)] = all_patterns

        except Exception as e:
            logger.warning(f"Failed to scan file {file_path}: {e}")

    def consolidate_configurations(self) -> ConfigConsolidationResult:
        """Consolidate found configuration patterns into recommendations."""
        total_patterns = sum(len(patterns) for patterns in self.scan_results.values())
        total_files = len(self.scan_results)

        # Analyze patterns for consolidation opportunities
        consolidation_suggestions = self._analyze_consolidation_opportunities()

        # Validate current configuration
        validation_result = self._validate_configuration()

        return ConfigConsolidationResult(
            patterns_found=total_patterns,
            files_scanned=total_files,
            consolidation_suggestions=consolidation_suggestions,
            validation_results=validation_result,
            consolidated_config=self.consolidated_config
        )

    def _analyze_consolidation_opportunities(self) -> List[str]:
        """Analyze scan results for consolidation opportunities."""
        suggestions = []

        # Count pattern types
        pattern_counts: Dict[str, int] = {}
        env_vars: Set[str] = set()
        hardcoded_values: List[ConfigPattern] = []

        for patterns in self.scan_results.values():
            for pattern in patterns:
                pattern_counts[pattern.pattern_type] = pattern_counts.get(pattern.pattern_type, 0) + 1

                if pattern.pattern_type in ["getenv", "environ_get", "environ_direct"]:
                    env_vars.add(pattern.key)
                elif pattern.pattern_type == "hardcoded_value":
                    hardcoded_values.append(pattern)

        # Generate suggestions
        if len(env_vars) > 0:
            suggestions.append(f"Found {len(env_vars)} environment variables that could be centralized in a config file")

        if len(hardcoded_values) > 10:
            suggestions.append(f"Found {len(hardcoded_values)} potential hardcoded configuration values that should be externalized")

        if pattern_counts.get("config_constant", 0) > 5:
            suggestions.append(f"Found {pattern_counts['config_constant']} configuration constants that could be consolidated")

        # Suggest centralization
        if len(self.scan_results) > 5:
            suggestions.append(f"Configuration scattered across {len(self.scan_results)} files - consider centralizing")

        return suggestions

    def _validate_configuration(self) -> ConfigValidationResult:
        """Validate current configuration setup."""
        errors = []
        warnings = []
        suggestions = []

        # Check for common issues
        env_vars = set()
        for patterns in self.scan_results.values():
            for pattern in patterns:
                if pattern.pattern_type in ["getenv", "environ_get", "environ_direct"]:
                    env_vars.add(pattern.key)

        # Check for missing environment variables
        for env_var in env_vars:
            if env_var not in os.environ:
                warnings.append(f"Environment variable '{env_var}' used but not set")

        # Check for hardcoded sensitive data
        sensitive_patterns = ["password", "secret", "key", "token"]
        for patterns in self.scan_results.values():
            for pattern in patterns:
                if pattern.pattern_type == "hardcoded_value":
                    value_lower = str(pattern.value).lower()
                    if any(sensitive in value_lower for sensitive in sensitive_patterns):
                        errors.append(f"Potential hardcoded sensitive data in {pattern.file_path}:{pattern.line_number}")

        if not errors and not warnings:
            suggestions.append("Configuration validation passed - no issues found")

        return ConfigValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions
        )

    def generate_config_file(self, output_path: str = "config/consolidated_config.json") -> str:
        """Generate a consolidated configuration file."""
        config_data = {
            "metadata": {
                "generated_by": "UnifiedConfigurationManager",
                "timestamp": str(Path(output_path).stat().st_mtime) if Path(output_path).exists() else None,
                "scan_directories": self.scan_directories,
                "patterns_found": sum(len(patterns) for patterns in self.scan_results.values())
            },
            "environment_variables": {},
            "constants": {},
            "settings": {},
            "validation": {}
        }

        # Extract environment variables
        env_vars = set()
        for patterns in self.scan_results.values():
            for pattern in patterns:
                if pattern.pattern_type in ["getenv", "environ_get", "environ_direct"]:
                    env_vars.add(pattern.key)

        config_data["environment_variables"] = {
            var: {
                "required": True,
                "description": f"Used in {len([p for patterns in self.scan_results.values() for p in patterns if p.key == var])} locations"
            } for var in sorted(env_vars)
        }

        # Extract constants
        constants = {}
        for patterns in self.scan_results.values():
            for pattern in patterns:
                if pattern.pattern_type == "config_constant":
                    constants[pattern.key] = pattern.value

        config_data["constants"] = constants

        # Write config file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(config_data, f, indent=2)

        logger.info(f"✅ Consolidated configuration generated: {output_path}")
        return str(output_file)

    def export_scan_results(self, output_path: str = "reports/config_scan_results.json") -> str:
        """Export detailed scan results."""
        results_data = {
            "scan_timestamp": str(Path(output_path).stat().st_mtime) if Path(output_path).exists() else None,
            "scan_directories": self.scan_directories,
            "total_files_scanned": len(self.scan_results),
            "total_patterns_found": sum(len(patterns) for patterns in self.scan_results.values()),
            "results_by_file": {}
        }

        # Convert patterns to serializable format
        for file_path, patterns in self.scan_results.items():
            results_data["results_by_file"][file_path] = [
                {
                    "line_number": p.line_number,
                    "pattern_type": p.pattern_type,
                    "key": p.key,
                    "value": str(p.value),
                    "context": p.context,
                    "source": p.source,
                    "confidence": p.confidence
                } for p in patterns
            ]

        # Write results file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(results_data, f, indent=2)

        logger.info(f"✅ Scan results exported: {output_path}")
        return str(output_file)


# Convenience functions
def scan_and_consolidate_config(directories: Optional[List[str]] = None) -> ConfigConsolidationResult:
    """Convenience function to scan and consolidate configurations."""
    manager = UnifiedConfigurationManager(directories)
    manager.scan_configurations()
    return manager.consolidate_configurations()


def validate_configuration_setup(directories: Optional[List[str]] = None) -> ConfigValidationResult:
    """Validate current configuration setup."""
    manager = UnifiedConfigurationManager(directories)
    manager.scan_configurations()
    result = manager.consolidate_configurations()
    return result.validation_results


# Backwards compatibility
ConfigurationConsolidator = UnifiedConfigurationManager
