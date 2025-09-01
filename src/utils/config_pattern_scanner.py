#!/usr/bin/env python3
"""
Configuration Pattern Scanner - Agent Cellphone V2
================================================

Scans for configuration patterns in the codebase.

Author: Agent-8 (SSOT Maintenance & System Integration Specialist)
License: MIT
"""

import ast
import re
from pathlib import Path
from typing import List

from .config_consolidator import ConfigPattern


class ConfigurationPatternScanner:
    """Scans for configuration patterns in the codebase."""
    
    def __init__(self):
        self.patterns: List[ConfigPattern] = []
        
    def scan_file_for_patterns(self, file_path: Path) -> List[ConfigPattern]:
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
