#!/usr/bin/env python3
"""
Unified Configuration Utilities - V2 Compliance Module
=====================================================

Consolidated configuration management following SOLID principles.
Combines functionality from:
- config_consolidator.py
- config_scanners.py
- config_core.py
- config_core/fsm_config.py

SOLID Implementation:
- SRP: Each class has single responsibility
- OCP: Extensible scanner system
- DIP: Dependencies injected via constructor

Author: Agent-3 (DevOps Specialist)
License: MIT
"""

import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ConfigPattern:
    """Configuration pattern found in code."""

    file_path: Path
    line_number: int
    pattern_type: str
    key: str
    value: Any
    context: str
    source: str


class ConfigurationScanner(ABC):
    """Abstract base class for configuration scanners."""

    @abstractmethod
    def scan_file(self, file_path: Path, lines: list[str]) -> list[ConfigPattern]:
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

    def scan_file(self, file_path: Path, lines: list[str]) -> list[ConfigPattern]:
        """Find environment variable usage patterns."""
        patterns = []
        for i, line in enumerate(lines, 1):
            if "os.getenv" in line:
                match = re.search(r'os\.getenv\(["\']([^"\']+)["\']', line)
                if match:
                    key = match.group(1)
                    patterns.append(
                        ConfigPattern(
                            file_path=file_path,
                            line_number=i,
                            pattern_type=self.pattern_type,
                            key=key,
                            value=None,
                            context=line.strip(),
                            source="environment",
                        )
                    )
        return patterns


class HardcodedValueScanner(ConfigurationScanner):
    """Scans for hardcoded configuration values."""

    @property
    def pattern_type(self) -> str:
        return "hardcoded_values"

    def scan_file(self, file_path: Path, lines: list[str]) -> list[ConfigPattern]:
        """Find hardcoded configuration values."""
        patterns = []
        config_patterns = [
            (r'(\w+)\s*=\s*["\']([^"\']+)["\']', "string_value"),
            (r"(\w+)\s*=\s*(\d+)", "numeric_value"),
            (r"(\w+)\s*=\s*(True|False)", "boolean_value"),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, value_type in config_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    key = match.group(1)
                    value = match.group(2)
                    if self._is_likely_config(key, value):
                        patterns.append(
                            ConfigPattern(
                                file_path=file_path,
                                line_number=i,
                                pattern_type=self.pattern_type,
                                key=key,
                                value=value,
                                context=line.strip(),
                                source="hardcoded",
                            )
                        )
        return patterns

    def _is_likely_config(self, key: str, value: str) -> bool:
        """Check if a key-value pair is likely to be configuration."""
        # Skip common variable names that aren't config
        skip_keys = {"i", "j", "k", "x", "y", "temp", "result", "data", "item", "value"}

        if key.lower() in skip_keys:
            return False

        # Skip if value is too short or generic
        if len(value) < 3:
            return False

        # Check for config-like patterns
        config_indicators = [
            "config",
            "setting",
            "param",
            "option",
            "default",
            "path",
            "url",
            "host",
            "port",
        ]
        return any(indicator in key.lower() for indicator in config_indicators)


class ConfigConstantScanner(ConfigurationScanner):
    """Scans for configuration constant definitions."""

    @property
    def pattern_type(self) -> str:
        return "config_constants"

    def scan_file(self, file_path: Path, lines: list[str]) -> list[ConfigPattern]:
        """Find configuration constant definitions."""
        patterns = []
        for i, line in enumerate(lines, 1):
            if re.match(r"^[A-Z_][A-Z0-9_]*\s*=", line):
                match = re.search(r"([A-Z_][A-Z0-9_]*)\s*=\s*(.+)", line)
                if match:
                    key = match.group(1)
                    value_str = match.group(2).strip()
                    if self._is_config_constant(key, value_str):
                        patterns.append(
                            ConfigPattern(
                                file_path=file_path,
                                line_number=i,
                                pattern_type=self.pattern_type,
                                key=key,
                                value=value_str,
                                context=line.strip(),
                                source="constant",
                            )
                        )
        return patterns

    def _is_config_constant(self, key: str, value: str) -> bool:
        """Check if this is a configuration constant."""
        # Constants should be uppercase with underscores
        if not re.match(r"^[A-Z_][A-Z0-9_]*$", key):
            return False

        # Skip simple numeric assignments
        if re.match(r"^\d+$", value):
            return False

        return True


class SettingsPatternScanner(ConfigurationScanner):
    """Scans for settings-related patterns."""

    @property
    def pattern_type(self) -> str:
        return "settings_patterns"

    def scan_file(self, file_path: Path, lines: list[str]) -> list[ConfigPattern]:
        """Find settings-related patterns."""
        patterns = []
        settings_keywords = ["settings", "config", "configuration", "options"]

        for i, line in enumerate(lines, 1):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in settings_keywords):
                # Look for dictionary or object access patterns
                if "." in line or "[" in line:
                    patterns.append(
                        ConfigPattern(
                            file_path=file_path,
                            line_number=i,
                            pattern_type=self.pattern_type,
                            key="settings_access",
                            value=None,
                            context=line.strip(),
                            source="settings",
                        )
                    )
        return patterns


class FileScanner:
    """Handles file scanning operations for configuration patterns."""

    def __init__(self, scanners: list[ConfigurationScanner]):
        """Initialize file scanner with available scanners."""
        self.scanners = scanners
        self.skip_patterns = self._get_skip_patterns()

    def _get_skip_patterns(self) -> set[str]:
        """Get patterns for files that should be skipped."""
        return {
            "__pycache__",
            ".git",
            "venv",
            "env",
            "node_modules",
            "*.pyc",
            "unified_config_utils.py",
        }

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during scanning."""
        file_str = str(file_path)
        return any(pattern in file_str for pattern in self.skip_patterns)

    def scan_file(self, file_path: Path) -> list[ConfigPattern]:
        """Scan a single file for configuration patterns."""
        if self.should_skip_file(file_path):
            return []

        patterns = []
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            # Use all registered scanners
            for scanner in self.scanners:
                file_patterns = scanner.scan_file(file_path, lines)
                patterns.extend(file_patterns)

        except Exception as e:
            logger.warning(f"Error scanning {file_path}: {e}")

        return patterns

    def scan_directory(self, root_dir: Path) -> list[ConfigPattern]:
        """Scan all Python files in a directory."""
        all_patterns = []

        for py_file in root_dir.rglob("*.py"):
            file_patterns = self.scan_file(py_file)
            all_patterns.extend(file_patterns)

        logger.info(
            f"Scanned {len(all_patterns)} patterns from {len(list(root_dir.rglob('*.py')))} files"
        )
        return all_patterns


class UnifiedConfigurationConsolidator:
    """Unified configuration consolidator combining all config utilities."""

    def __init__(self, config_manager=None, file_scanner: FileScanner | None = None):
        """Initialize consolidator with dependency injection."""
        self.config_manager = config_manager
        self.file_scanner = file_scanner or FileScanner(self._create_default_scanners())
        self.consolidated_count = 0
        self.migrated_files: set[Path] = set()

    def _create_default_scanners(self) -> list[ConfigurationScanner]:
        """Create default set of configuration scanners."""
        return [
            EnvironmentVariableScanner(),
            HardcodedValueScanner(),
            ConfigConstantScanner(),
            SettingsPatternScanner(),
        ]

    def scan_configuration_patterns(self, root_dir: Path) -> dict[str, list[ConfigPattern]]:
        """Scan for configuration patterns in the codebase."""
        logger.info("🔍 Scanning for configuration patterns...")

        # Use the file scanner to get all patterns
        all_patterns = self.file_scanner.scan_directory(root_dir)

        # Group patterns by type
        patterns_by_type = {}
        for pattern in all_patterns:
            if pattern.pattern_type not in patterns_by_type:
                patterns_by_type[pattern.pattern_type] = []
            patterns_by_type[pattern.pattern_type].append(pattern)

        # Update statistics
        total_patterns = len(all_patterns)
        logger.info(f"✅ Found {total_patterns} configuration patterns")

        for pattern_type, patterns in patterns_by_type.items():
            if patterns:
                logger.info(f"   - {pattern_type}: {len(patterns)} patterns")

        return patterns_by_type

    def consolidate_patterns(
        self, patterns_by_type: dict[str, list[ConfigPattern]]
    ) -> dict[str, Any]:
        """Consolidate found patterns into actionable insights."""
        statistics = {}
        unique_keys = set()

        for pattern_type, patterns in patterns_by_type.items():
            statistics[pattern_type] = len(patterns)
            for pattern in patterns:
                if pattern.key:
                    unique_keys.add(pattern.key)

        results = {
            "total_patterns": sum(statistics.values()),
            "patterns_by_type": statistics,
            "unique_keys": list(unique_keys),
            "consolidated_count": self.consolidated_count,
            "migrated_files": len(self.migrated_files),
        }

        logger.info(f"📊 Consolidated {results['total_patterns']} patterns")
        return results

    def generate_consolidation_report(self, results: dict[str, Any]) -> str:
        """Generate a comprehensive consolidation report."""
        report = f"""
# 🔧 Configuration Consolidation Report

## 📈 Summary Statistics
- **Total Patterns Found:** {results["total_patterns"]}
- **Pattern Types:** {len(results["patterns_by_type"])}
- **Unique Keys:** {len(results["unique_keys"])}
- **Consolidated:** {results["consolidated_count"]}
- **Files Migrated:** {results["migrated_files"]}

## 🔍 Pattern Analysis
"""

        for pattern_type, count in results["patterns_by_type"].items():
            if count > 0:
                report += f"- **{pattern_type}:** {count} patterns\n"

        report += """

## 🎯 Recommended Actions
1. **Review hardcoded values** for centralization
2. **Migrate environment variables** to config files
3. **Consolidate duplicate configuration keys**
4. **Update import statements** for new config locations

## ✅ SOLID Compliance Maintained
- **Single Responsibility:** Each scanner handles one pattern type
- **Open/Closed:** Easy to add new scanners
- **Dependency Inversion:** Configurable scanner injection

**Agent-3 - DevOps Specialist**
**Unified Configuration Utilities Mission Complete**
"""

        return report


def run_configuration_consolidation(root_dir: Path = None) -> dict[str, Any]:
    """Run the complete configuration consolidation process."""
    if root_dir is None:
        root_dir = Path(__file__).resolve().parents[2]

    consolidator = UnifiedConfigurationConsolidator()
    patterns = consolidator.scan_configuration_patterns(root_dir)
    results = consolidator.consolidate_patterns(patterns)
    report = consolidator.generate_consolidation_report(results)

    report_path = root_dir / "unified_configuration_consolidation_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    results["report_path"] = str(report_path)
    results["report_content"] = report
    return results


if __name__ == "__main__":
    results = run_configuration_consolidation()
    logger.info("\n📊 Unified configuration consolidation complete!")
    logger.info(f"📄 Report saved to: {results['report_path']}")
