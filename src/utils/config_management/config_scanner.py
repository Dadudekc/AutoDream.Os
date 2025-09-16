#!/usr/bin/env python3
"""
Configuration Scanner Module - V2 Compliant
==========================================

Configuration scanning functionality extracted from consolidated_config_management.py
for V2 compliance (≤400 lines).

Provides:
- Configuration pattern scanning
- Environment variable detection
- JSON/YAML configuration scanning
- Pattern detection and analysis

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import json
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

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
    metadata: dict[str, Any] = field(default_factory=dict)


class ConfigurationScanner(ABC):
    """Abstract base class for configuration scanners."""

    @abstractmethod
    def scan_file(self, file_path: Path, lines: list[str]) -> list[ConfigPattern]:
        """Scan a file for configuration patterns."""
        pass

    @abstractmethod
    def get_pattern_types(self) -> list[str]:
        """Get the types of patterns this scanner detects."""
        pass


class EnvironmentVariableScanner(ConfigurationScanner):
    """Scans for environment variable usage patterns."""

    def get_pattern_types(self) -> list[str]:
        return ["env_var", "getenv", "environ"]

    def scan_file(self, file_path: Path, lines: list[str]) -> list[ConfigPattern]:
        """Scan for environment variable patterns."""
        patterns = []
        env_patterns = [
            (r'os\.getenv\(["\']([^"\']+)["\']', "getenv"),
            (r'os\.environ\.get\(["\']([^"\']+)["\']', "environ_get"),
            (r'os\.environ\["([^"]+)"\]', "environ_direct"),
            (r"os\.environ\[\'([^\']+)\'\]", "environ_direct"),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, pattern_type in env_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    key = match.group(1)
                    patterns.append(ConfigPattern(
                        file_path=file_path,
                        line_number=i,
                        pattern_type=pattern_type,
                        key=key,
                        value=None,
                        context=line.strip(),
                        source="environment_variable"
                    ))

        return patterns


class JSONConfigScanner(ConfigurationScanner):
    """Scans for JSON configuration patterns."""

    def get_pattern_types(self) -> list[str]:
        return ["json_config", "json_file", "json_data"]

    def scan_file(self, file_path: Path, lines: list[str]) -> list[ConfigPattern]:
        """Scan for JSON configuration patterns."""
        patterns = []
        
        # Look for JSON file loading patterns
        json_patterns = [
            (r'json\.load\(open\(["\']([^"\']+)["\']', "json_load_file"),
            (r'json\.loads\(([^)]+)\)', "json_loads_string"),
            (r'\.json["\']', "json_file_extension"),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, pattern_type in json_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    key = match.group(1) if match.groups() else "json_data"
                    patterns.append(ConfigPattern(
                        file_path=file_path,
                        line_number=i,
                        pattern_type=pattern_type,
                        key=key,
                        value=None,
                        context=line.strip(),
                        source="json_configuration"
                    ))

        return patterns


class YAMLConfigScanner(ConfigurationScanner):
    """Scans for YAML configuration patterns."""

    def get_pattern_types(self) -> list[str]:
        return ["yaml_config", "yaml_file", "yaml_data"]

    def scan_file(self, file_path: Path, lines: list[str]) -> list[ConfigPattern]:
        """Scan for YAML configuration patterns."""
        patterns = []
        
        # Look for YAML file loading patterns
        yaml_patterns = [
            (r'yaml\.load\(open\(["\']([^"\']+)["\']', "yaml_load_file"),
            (r'yaml\.safe_load\(([^)]+)\)', "yaml_safe_load"),
            (r'\.yaml["\']', "yaml_file_extension"),
            (r'\.yml["\']', "yml_file_extension"),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, pattern_type in yaml_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    key = match.group(1) if match.groups() else "yaml_data"
                    patterns.append(ConfigPattern(
                        file_path=file_path,
                        line_number=i,
                        pattern_type=pattern_type,
                        key=key,
                        value=None,
                        context=line.strip(),
                        source="yaml_configuration"
                    ))

        return patterns


class ConfigFileScanner(ConfigurationScanner):
    """Scans for configuration file patterns."""

    def get_pattern_types(self) -> list[str]:
        return ["config_file", "settings_file", "ini_file"]

    def scan_file(self, file_path: Path, lines: list[str]) -> list[ConfigPattern]:
        """Scan for configuration file patterns."""
        patterns = []
        
        # Look for configuration file patterns
        config_patterns = [
            (r'configparser\.ConfigParser\(\)', "config_parser"),
            (r'\.ini["\']', "ini_file_extension"),
            (r'\.conf["\']', "conf_file_extension"),
            (r'\.cfg["\']', "cfg_file_extension"),
            (r'config\[["\']([^"\']+)["\']', "config_access"),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, pattern_type in config_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    key = match.group(1) if match.groups() else "config_data"
                    patterns.append(ConfigPattern(
                        file_path=file_path,
                        line_number=i,
                        pattern_type=pattern_type,
                        key=key,
                        value=None,
                        context=line.strip(),
                        source="configuration_file"
                    ))

        return patterns


class ConfigurationScannerRegistry:
    """Registry for configuration scanners."""

    def __init__(self):
        self.scanners = {
            "environment": EnvironmentVariableScanner(),
            "json": JSONConfigScanner(),
            "yaml": YAMLConfigScanner(),
            "config_file": ConfigFileScanner(),
        }

    def get_scanner(self, scanner_type: str) -> ConfigurationScanner:
        """Get a scanner by type."""
        return self.scanners.get(scanner_type)

    def get_all_scanners(self) -> list[ConfigurationScanner]:
        """Get all available scanners."""
        return list(self.scanners.values())

    def scan_file(self, file_path: Path, lines: list[str]) -> list[ConfigPattern]:
        """Scan a file with all available scanners."""
        all_patterns = []
        
        for scanner in self.scanners.values():
            try:
                patterns = scanner.scan_file(file_path, lines)
                all_patterns.extend(patterns)
            except Exception as e:
                logger.error(f"Scanner {scanner.__class__.__name__} failed for {file_path}: {e}")
        
        return all_patterns

    def get_pattern_summary(self, patterns: list[ConfigPattern]) -> dict[str, int]:
        """Get a summary of pattern types found."""
        summary = {}
        for pattern in patterns:
            pattern_type = pattern.pattern_type
            summary[pattern_type] = summary.get(pattern_type, 0) + 1
        return summary


if __name__ == "__main__":
    # Example usage
    registry = ConfigurationScannerRegistry()
    
    # Test with sample lines
    sample_lines = [
        'import os',
        'api_key = os.getenv("API_KEY")',
        'config = json.load(open("config.json"))',
        'settings = yaml.safe_load(file)',
        'parser = configparser.ConfigParser()'
    ]
    
    patterns = registry.scan_file(Path("test.py"), sample_lines)
    summary = registry.get_pattern_summary(patterns)
    
    print(f"Found {len(patterns)} configuration patterns:")
    for pattern_type, count in summary.items():
        print(f"  {pattern_type}: {count}")
