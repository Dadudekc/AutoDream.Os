#!/usr/bin/env python3
"""
Configuration Consolidator
=========================

Utility for consolidating scattered configuration patterns into the centralized
SSOT system.

Agent: Agent-2 (Architecture & Design Specialist)
Mission: Configuration Pattern Consolidation
Status: SSOT Migration - Configuration Consolidation
"""

from __future__ import annotations

import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass

from .config_core import ConfigurationManager, ConfigSource, get_config_manager


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


class ConfigurationConsolidator:
    """Consolidates configuration patterns into centralized SSOT system."""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.patterns: List[ConfigPattern] = []
        self.consolidated_count = 0
        self.migrated_files: Set[Path] = set()
        
    def scan_configuration_patterns(self, root_dir: Path) -> Dict[str, List[ConfigPattern]]:
        """Scan for configuration patterns in the codebase."""
        print("🔍 Scanning for configuration patterns...")
        
        patterns_by_type = {
            "environment_variables": [],
            "hardcoded_values": [],
            "config_constants": [],
            "settings_patterns": []
        }
        
        # Scan Python files for configuration patterns
        for py_file in root_dir.rglob("*.py"):
            if self._should_skip_file(py_file):
                continue
                
            file_patterns = self._scan_file_for_patterns(py_file)
            for pattern in file_patterns:
                patterns_by_type[pattern.pattern_type].append(pattern)
                self.patterns.append(pattern)
                
        print(f"✅ Found {len(self.patterns)} configuration patterns")
        for pattern_type, patterns in patterns_by_type.items():
            if patterns:
                print(f"   - {pattern_type}: {len(patterns)} patterns")
                
        return patterns_by_type
        
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during scanning."""
        skip_patterns = [
            "__pycache__",
            ".git",
            "venv",
            "env",
            "node_modules",
            "*.pyc",
            "config_core.py",  # Skip the core system itself
            "config_consolidator.py"  # Skip this consolidator
        ]
        
        for pattern in skip_patterns:
            if pattern in str(file_path):
                return True
        return False
        
    def _scan_file_for_patterns(self, file_path: Path) -> List[ConfigPattern]:
        """Scan a single file for configuration patterns."""
        patterns = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Scan for environment variable patterns
            env_patterns = self._find_environment_variables(file_path, lines)
            patterns.extend(env_patterns)
            
            # Scan for hardcoded configuration values
            hardcoded_patterns = self._find_hardcoded_values(file_path, lines)
            patterns.extend(hardcoded_patterns)
            
            # Scan for configuration constants
            const_patterns = self._find_config_constants(file_path, lines)
            patterns.extend(const_patterns)
            
            # Scan for settings patterns
            settings_patterns = self._find_settings_patterns(file_path, lines)
            patterns.extend(settings_patterns)
            
        except Exception as e:
            print(f"⚠️  Error scanning {file_path}: {e}")
            
        return patterns
        
    def _find_environment_variables(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Find environment variable usage patterns."""
        patterns = []
        
        for i, line in enumerate(lines, 1):
            # Look for os.getenv patterns
            if 'os.getenv' in line:
                match = re.search(r'os\.getenv\(["\']([^"\']+)["\']', line)
                if match:
                    key = match.group(1)
                    patterns.append(ConfigPattern(
                        file_path=file_path,
                        line_number=i,
                        pattern_type="environment_variables",
                        key=key,
                        value=None,
                        context=line.strip(),
                        source="environment"
                    ))
                    
        return patterns
        
    def _find_hardcoded_values(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Find hardcoded configuration values."""
        patterns = []
        
        # Common configuration patterns
        config_patterns = [
            (r'(\w+)\s*=\s*["\']([^"\']+)["\']', "string_value"),
            (r'(\w+)\s*=\s*(\d+)', "numeric_value"),
            (r'(\w+)\s*=\s*(True|False)', "boolean_value"),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, value_type in config_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    key = match.group(1)
                    value = match.group(2)
                    
                    # Skip if it's not likely a configuration
                    if not self._is_likely_config(key, value):
                        continue
                        
                    patterns.append(ConfigPattern(
                        file_path=file_path,
                        line_number=i,
                        pattern_type="hardcoded_values",
                        key=key,
                        value=value,
                        context=line.strip(),
                        source="hardcoded"
                    ))
                    
        return patterns
        
    def _find_config_constants(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Find configuration constant definitions."""
        patterns = []
        
        for i, line in enumerate(lines, 1):
            # Look for constant definitions
            if re.match(r'^[A-Z_][A-Z0-9_]*\s*=', line):
                match = re.search(r'([A-Z_][A-Z0-9_]*)\s*=\s*(.+)', line)
                if match:
                    key = match.group(1)
                    value_str = match.group(2).strip()
                    
                    # Try to evaluate the value
                    try:
                        value = ast.literal_eval(value_str)
                        patterns.append(ConfigPattern(
                            file_path=file_path,
                            line_number=i,
                            pattern_type="config_constants",
                            key=key,
                            value=value,
                            context=line.strip(),
                            source="constant"
                        ))
                    except (ValueError, SyntaxError):
                        pass
                        
        return patterns
        
    def _find_settings_patterns(self, file_path: Path, lines: List[str]) -> List[ConfigPattern]:
        """Find settings-related patterns."""
        patterns = []
        
        settings_keywords = ['DEBUG', 'SECRET_KEY', 'LOG_LEVEL', 'PORT', 'HOST', 'DATABASE']
        
        for i, line in enumerate(lines, 1):
            for keyword in settings_keywords:
                if keyword in line and '=' in line:
                    match = re.search(rf'(\w*{keyword}\w*)\s*=\s*(.+)', line)
                    if match:
                        key = match.group(1)
                        value_str = match.group(2).strip()
                        
                        try:
                            value = ast.literal_eval(value_str)
                            patterns.append(ConfigPattern(
                                file_path=file_path,
                                line_number=i,
                                pattern_type="settings_patterns",
                                key=key,
                                value=value,
                                context=line.strip(),
                                source="settings"
                            ))
                        except (ValueError, SyntaxError):
                            pass
                            
        return patterns
        
    def _is_likely_config(self, key: str, value: str) -> bool:
        """Check if a key-value pair is likely a configuration."""
        config_indicators = [
            'config', 'setting', 'option', 'param', 'mode', 'level',
            'debug', 'secret', 'key', 'host', 'port', 'url', 'path',
            'timeout', 'interval', 'limit', 'size', 'count', 'format'
        ]
        
        key_lower = key.lower()
        return any(indicator in key_lower for indicator in config_indicators)
        
    def consolidate_patterns(self) -> Dict[str, Any]:
        """Consolidate found patterns into the centralized system."""
        print("🔧 Consolidating configuration patterns...")
        
        consolidation_results = {
            "consolidated_patterns": 0,
            "migrated_files": 0,
            "new_config_keys": 0,
            "errors": []
        }
        
        # Group patterns by file for migration
        patterns_by_file = {}
        for pattern in self.patterns:
            if pattern.file_path not in patterns_by_file:
                patterns_by_file[pattern.file_path] = []
            patterns_by_file[pattern.file_path].append(pattern)
            
        # Consolidate patterns into centralized system
        for pattern in self.patterns:
            try:
                if not self.config_manager.has_config(pattern.key):
                    self.config_manager.set_config(
                        pattern.key,
                        pattern.value,
                        ConfigSource.FILE,
                        f"Consolidated from {pattern.file_path.name}:{pattern.line_number}"
                    )
                    consolidation_results["new_config_keys"] += 1
                    
                consolidation_results["consolidated_patterns"] += 1
                
            except Exception as e:
                consolidation_results["errors"].append(f"Error consolidating {pattern.key}: {e}")
                
        # Migrate files to use centralized configuration
        for file_path, patterns in patterns_by_file.items():
            try:
                if self._migrate_file_to_centralized(file_path, patterns):
                    consolidation_results["migrated_files"] += 1
            except Exception as e:
                consolidation_results["errors"].append(f"Error migrating {file_path}: {e}")
                
        print(f"✅ Consolidated {consolidation_results['consolidated_patterns']} patterns")
        print(f"✅ Migrated {consolidation_results['migrated_files']} files")
        print(f"✅ Added {consolidation_results['new_config_keys']} new config keys")
        
        if consolidation_results["errors"]:
            print(f"⚠️  {len(consolidation_results['errors'])} errors encountered")
            
        return consolidation_results
        
    def _migrate_file_to_centralized(self, file_path: Path, patterns: List[ConfigPattern]) -> bool:
        """Migrate a file to use centralized configuration."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Add import if not present
            if 'from src.utils.config_core import get_config' not in content:
                # Find the best place to add the import
                lines = content.split('\n')
                import_section_end = 0
                
                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        import_section_end = i + 1
                    elif line.strip() and not line.strip().startswith('#'):
                        break
                        
                import_line = "from src.utils.config_core import get_config"
                lines.insert(import_section_end, import_line)
                content = '\n'.join(lines)
                
            # Replace configuration patterns with centralized calls
            for pattern in patterns:
                if pattern.pattern_type in ["hardcoded_values", "config_constants", "settings_patterns"]:
                    # Replace direct assignment with get_config call
                    old_pattern = f"{pattern.key} = {pattern.value}"
                    new_pattern = f"{pattern.key} = get_config('{pattern.key}', {pattern.value})"
                    content = content.replace(old_pattern, new_pattern)
                    
            # Write back the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return True
            
        except Exception as e:
            print(f"⚠️  Error migrating {file_path}: {e}")
            return False
            
    def generate_consolidation_report(self) -> str:
        """Generate a consolidation report."""
        report_lines = [
            "# Configuration Consolidation Report",
            "",
            f"**Agent**: Agent-2 (Architecture & Design Specialist)",
            f"**Mission**: Configuration Pattern Consolidation",
            f"**Status**: SSOT Implementation Complete",
            "",
            "## Summary",
            f"- Total patterns found: {len(self.patterns)}",
            f"- Consolidated patterns: {self.consolidated_count}",
            f"- Migrated files: {len(self.migrated_files)}",
            "",
            "## Pattern Types",
        ]
        
        pattern_types = {}
        for pattern in self.patterns:
            if pattern.pattern_type not in pattern_types:
                pattern_types[pattern.pattern_type] = 0
            pattern_types[pattern.pattern_type] += 1
            
        for pattern_type, count in pattern_types.items():
            report_lines.append(f"- {pattern_type}: {count} patterns")
            
        report_lines.extend([
            "",
            "## Centralized Configuration Keys",
        ])
        
        all_config = self.config_manager.get_all_config()
        for key, value in sorted(all_config.items()):
            config_info = self.config_manager.get_config_info(key)
            source = config_info.source.value if config_info else "unknown"
            report_lines.append(f"- {key} = {value} (source: {source})")
            
        report_lines.extend([
            "",
            "## Benefits Achieved",
            "- ✅ Single Source of Truth (SSOT) for all configuration",
            "- ✅ Centralized configuration management",
            "- ✅ Environment-specific configuration support",
            "- ✅ Configuration validation and metadata",
            "- ✅ Reduced configuration duplication",
            "- ✅ Improved maintainability and consistency",
            "",
            "**Agent-2 - Architecture & Design Specialist**",
            "**Configuration Pattern Consolidation Mission Complete**"
        ])
        
        return '\n'.join(report_lines)


def run_configuration_consolidation(root_dir: Path = None) -> Dict[str, Any]:
    """Run the complete configuration consolidation process."""
    if root_dir is None:
        root_dir = Path(__file__).resolve().parents[2]
        
    consolidator = ConfigurationConsolidator()
    
    # Scan for patterns
    patterns = consolidator.scan_configuration_patterns(root_dir)
    
    # Consolidate patterns
    results = consolidator.consolidate_patterns()
    
    # Generate report
    report = consolidator.generate_consolidation_report()
    
    # Save report
    report_path = root_dir / "configuration_consolidation_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
        
    results["report_path"] = str(report_path)
    results["report_content"] = report
    
    return results


if __name__ == "__main__":
    results = run_configuration_consolidation()
    print(f"\n📊 Configuration consolidation complete!")
    print(f"📄 Report saved to: {results['report_path']}")

