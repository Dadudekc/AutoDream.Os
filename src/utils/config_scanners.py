"""
Configuration Scanners - V2 Compliance Module
===========================================

Modular scanners for different configuration patterns following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from .config_consolidator import ConfigPattern


class ConfigurationScanner(ABC):
    """Abstract base class for configuration scanners."""

    @abstractmethod
    def scan_file(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Scan a file for specific configuration patterns."""
        pass

    @property
    @abstractmethod
    def pattern_type(self) -> str:
        """Get the type of patterns this scanner detects."""
        pass


class EnvironmentVariableScanner(ConfigurationScanner):
    """Scans for environment variable usage patterns."""

    @property
    def pattern_type(self) -> str:
        return "environment_variables"

    def scan_file(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Find environment variable usage patterns."""
        patterns = []
        for i, line in enumerate(lines, 1):
            if 'os.getenv' in line:
                match = re.search(r'os\.getenv\(["\']([^"\']+)["\']', line)
                if match:
                    key = match.group(1)
                    patterns.append(ConfigPattern(
                        file_path=file_path,
                        line_number=i,
                        pattern_type=self.pattern_type,
                        key=key,
                        value=None,
                        context=line.strip(),
                        source='environment'
                    ))
        return patterns


class HardcodedValueScanner(ConfigurationScanner):
    """Scans for hardcoded configuration values."""

    @property
    def pattern_type(self) -> str:
        return "hardcoded_values"

    def scan_file(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Find hardcoded configuration values."""
        patterns = []
        config_patterns = [
            (r'(\w+)\s*=\s*["\']([^"\']+)["\']', 'string_value'),
            (r'(\w+)\s*=\s*(\d+)', 'numeric_value'),
            (r'(\w+)\s*=\s*(True|False)', 'boolean_value')
        ]

        for i, line in enumerate(lines, 1):
            for pattern, value_type in config_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    key = match.group(1)
                    value = match.group(2)
                    if self._is_likely_config(key, value):
                        patterns.append(ConfigPattern(
                            file_path=file_path,
                            line_number=i,
                            pattern_type=self.pattern_type,
                            key=key,
                            value=value,
                            context=line.strip(),
                            source='hardcoded'
                        ))
        return patterns

    def _is_likely_config(self, key: str, value: str) -> bool:
        """Check if a key-value pair is likely to be configuration."""
        # Skip common variable names that aren't config
        skip_keys = {'i', 'j', 'k', 'x', 'y', 'temp', 'result', 'data', 'item', 'value'}

        if key.lower() in skip_keys:
            return False

        # Skip if value is too short or generic
        if len(value) < 3:
            return False

        # Check for config-like patterns
        config_indicators = ['config', 'setting', 'param', 'option', 'default', 'path', 'url', 'host', 'port']
        return any(indicator in key.lower() for indicator in config_indicators)


class ConfigConstantScanner(ConfigurationScanner):
    """Scans for configuration constant definitions."""

    @property
    def pattern_type(self) -> str:
        return "config_constants"

    def scan_file(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Find configuration constant definitions."""
        patterns = []
        for i, line in enumerate(lines, 1):
            if re.match(r'^[A-Z_][A-Z0-9_]*\s*=', line):
                match = re.search(r'([A-Z_][A-Z0-9_]*)\s*=\s*(.+)', line)
                if match:
                    key = match.group(1)
                    value_str = match.group(2).strip()
                    if self._is_config_constant(key, value_str):
                        patterns.append(ConfigPattern(
                            file_path=file_path,
                            line_number=i,
                            pattern_type=self.pattern_type,
                            key=key,
                            value=value_str,
                            context=line.strip(),
                            source='constant'
                        ))
        return patterns

    def _is_config_constant(self, key: str, value: str) -> bool:
        """Check if this is a configuration constant."""
        # Constants should be uppercase with underscores
        if not re.match(r'^[A-Z_][A-Z0-9_]*$', key):
            return False

        # Skip simple numeric assignments
        if re.match(r'^\d+$', value):
            return False

        return True


class SettingsPatternScanner(ConfigurationScanner):
    """Scans for settings-related patterns."""

    @property
    def pattern_type(self) -> str:
        return "settings_patterns"

    def scan_file(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Find settings-related patterns."""
        patterns = []
        settings_keywords = ['settings', 'config', 'configuration', 'options']

        for i, line in enumerate(lines, 1):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in settings_keywords):
                # Look for dictionary or object access patterns
                if '.' in line or '[' in line:
                    patterns.append(ConfigPattern(
                        file_path=file_path,
                        line_number=i,
                        pattern_type=self.pattern_type,
                        key="settings_access",
                        value=None,
                        context=line.strip(),
                        source='settings'
                    ))
        return patterns
