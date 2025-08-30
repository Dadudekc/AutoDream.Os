
# MIGRATED: This file has been migrated to the centralized configuration system
"""
Configuration Validator - SSOT Violation Detection and Validation

This module validates configuration files for SSOT violations and ensures
consistency across the entire configuration system.

Author: Agent-6
Contract: SSOT-VALUE_ZEROVALUE_ZEROVALUE_THREE: Configuration Management Consolidation
Date: VALUE_TWOVALUE_ZEROVALUE_TWO5-VALUE_ZERO8-VALUE_TWO8
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Tuple, Set
from collections import defaultdict
import logging

from .constants import (
    DEFAULT_TIMEOUT, SHORT_TIMEOUT, LONG_TIMEOUT, CRITICAL_TIMEOUT,
    DEFAULT_RETRY_ATTEMPTS, DEFAULT_RETRY_DELAY, MAX_RETRY_ATTEMPTS,
    DEFAULT_COLLECTION_INTERVAL, LONG_COLLECTION_INTERVAL, SHORT_COLLECTION_INTERVAL,
    SYSTEM_ENABLED, SYSTEM_DISABLED,
    REQUIRED_SYSTEM_KEYS, REQUIRED_COMMUNICATION_KEYS, REQUIRED_AGENT_KEYS
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigurationValidator:
    """Validates configuration files for SSOT violations and consistency."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.violations = []
        self.duplicates = defaultdict(list)
        self.consistency_issues = []
        
    def validate_all_configs(self) -> Dict[str, Any]:
        """Validate all configuration files in the config directory."""
        logger.info("Starting comprehensive configuration validation...")
        
        # Reset validation state
        self.violations = []
        self.duplicates = defaultdict(list)
        self.consistency_issues = []
        
        # Find all configuration files
        config_files = self._find_config_files()
        logger.info(f"Found {len(config_files)} configuration files to validate")
        
        # Load and validate each file
        all_configs = {}
        for file_path in config_files:
            try:
                config_data = self._load_config_file(file_path)
                if config_data:
                    all_configs[str(file_path)] = config_data
                    self._validate_single_config(file_path, config_data)
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
                self.violations.append({
                    "type": "LOAD_ERROR",
                    "file": str(file_path),
                    "error": str(e)
                })
        
        # Cross-file validation
        self._validate_cross_file_consistency(all_configs)
        
        # Generate validation report
        report = self._generate_validation_report()
        
        logger.info(f"Validation complete. Found {len(self.violations)} violations")
        return report
    
    def _find_config_files(self) -> List[Path]:
        """Find all configuration files in the config directory."""
        config_files = []
        
        # Supported file extensions
        extensions = {'.json', '.yaml', '.yml', '.py'}
        
        for file_path in self.config_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                # Skip backup and cache directories
                if not any(part.startswith('.') or part.startswith('__') 
                          for part in file_path.parts):
                    config_files.append(file_path)
        
        return sorted(config_files)
    
    def _load_config_file(self, file_path: Path) -> Dict[str, Any]:
        """Load configuration file based on its extension."""
        if file_path.suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif file_path.suffix in ('.yaml', '.yml'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        elif file_path.suffix == '.py':
            # For Python files, we'll just check for constants
            return self._extract_python_constants(file_path)
        return {}
    
    def _extract_python_constants(self, file_path: Path) -> Dict[str, Any]:
        """Extract constant definitions from Python files."""
        constants = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Simple regex-like extraction for common patterns
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    parts = line.split('=', VALUE_ONE)
                    if len(parts) == VALUE_TWO:
                        key = parts[VALUE_ZERO].strip()
                        value = parts[VALUE_ONE].strip().rstrip(',')
                        constants[key] = value
        except Exception as e:
            logger.warning(f"Could not extract constants from {file_path}: {e}")
        
        return constants
    
    def _validate_single_config(self, file_path: Path, config_data: Dict[str, Any]):
        """Validate a single configuration file."""
        file_str = str(file_path)
        
        # Check for required keys based on file type
        if 'system' in file_path.parts:
            if not self._validate_required_keys(config_data, REQUIRED_SYSTEM_KEYS, file_str):
                self.violations.append({
                    "type": "MISSING_REQUIRED_KEYS",
                    "file": file_str,
                    "missing_keys": [k for k in REQUIRED_SYSTEM_KEYS if k not in config_data]
                })
        
        # Check for duplicate values within the file
        self._check_internal_duplicates(config_data, file_str)
        
        # Check for specific SSOT violations
        self._check_timeout_violations(config_data, file_str)
        self._check_retry_violations(config_data, file_str)
        self._check_collection_interval_violations(config_data, file_str)
        self._check_enable_flag_violations(config_data, file_str)
    
    def _validate_required_keys(self, config: Dict[str, Any], required_keys: List[str], file_path: str) -> bool:
        """Validate that required keys are present in configuration."""
        return all(key in config for key in required_keys)
    
    def _check_internal_duplicates(self, config: Dict[str, Any], file_path: str):
        """Check for duplicate values within a single configuration file."""
        value_locations = defaultdict(list)
        
        def extract_values(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if isinstance(value, (str, int, float, bool)):
                        value_locations[str(value)].append(current_path)
                    else:
                        extract_values(value, current_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{path}[{i}]"
                    extract_values(item, current_path)
        
        extract_values(config)
        
        # Report duplicates
        for value, locations in value_locations.items():
            if len(locations) > VALUE_ONE:
                self.duplicates[value].extend([f"{file_path}:{loc}" for loc in locations])
    
    def _check_timeout_violations(self, config: Dict[str, Any], file_path: str):
        """Check for timeout-related SSOT violations."""
        timeout_values = self._extract_numeric_values(config, ['timeout', 'timeout_ms', 'cdp_timeout'])
        
        for timeout_value in timeout_values:
            if timeout_value not in [DEFAULT_TIMEOUT, SHORT_TIMEOUT, LONG_TIMEOUT, CRITICAL_TIMEOUT]:
                self.violations.append({
                    "type": "NON_STANDARD_TIMEOUT",
                    "file": file_path,
                    "value": timeout_value,
                    "standard_values": [DEFAULT_TIMEOUT, SHORT_TIMEOUT, LONG_TIMEOUT, CRITICAL_TIMEOUT]
                })
    
    def _check_retry_violations(self, config: Dict[str, Any], file_path: str):
        """Check for retry-related SSOT violations."""
        retry_attempts = self._extract_numeric_values(config, ['retry_attempts', 'max_retry_attempts'])
        retry_delays = self._extract_numeric_values(config, ['retry_delay'])
        
        for attempts in retry_attempts:
            if attempts not in [DEFAULT_RETRY_ATTEMPTS, MAX_RETRY_ATTEMPTS]:
                self.violations.append({
                    "type": "NON_STANDARD_RETRY_ATTEMPTS",
                    "file": file_path,
                    "value": attempts,
                    "standard_values": [DEFAULT_RETRY_ATTEMPTS, MAX_RETRY_ATTEMPTS]
                })
        
        for delay in retry_delays:
            if delay not in [DEFAULT_RETRY_DELAY]:
                self.violations.append({
                    "type": "NON_STANDARD_RETRY_DELAY",
                    "file": file_path,
                    "value": delay,
                    "standard_values": [DEFAULT_RETRY_DELAY]
                })
    
    def _check_collection_interval_violations(self, config: Dict[str, Any], file_path: str):
        """Check for collection interval SSOT violations."""
        intervals = self._extract_numeric_values(config, ['collection_interval'])
        
        for interval in intervals:
            if interval not in [DEFAULT_COLLECTION_INTERVAL, LONG_COLLECTION_INTERVAL, SHORT_COLLECTION_INTERVAL]:
                self.violations.append({
                    "type": "NON_STANDARD_COLLECTION_INTERVAL",
                    "file": file_path,
                    "value": interval,
                    "standard_values": [DEFAULT_COLLECTION_INTERVAL, LONG_COLLECTION_INTERVAL, SHORT_COLLECTION_INTERVAL]
                })
    
    def _check_enable_flag_violations(self, config: Dict[str, Any], file_path: str):
        """Check for enable/disable flag SSOT violations."""
        enable_values = self._extract_boolean_values(config, ['enabled', 'enable'])
        
        for value in enable_values:
            if value not in [SYSTEM_ENABLED, SYSTEM_DISABLED]:
                self.violations.append({
                    "type": "NON_STANDARD_ENABLE_FLAG",
                    "file": file_path,
                    "value": value,
                    "standard_values": [SYSTEM_ENABLED, SYSTEM_DISABLED]
                })
    
    def _extract_numeric_values(self, config: Dict[str, Any], key_patterns: List[str]) -> List[float]:
        """Extract numeric values from configuration based on key patterns."""
        values = []
        
        def extract_from_obj(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if any(pattern in key.lower() for pattern in key_patterns):
                        if isinstance(value, (int, float)):
                            values.append(float(value))
                    extract_from_obj(value, current_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{path}[{i}]"
                    extract_from_obj(item, current_path)
        
        extract_from_obj(config)
        return values
    
    def _extract_boolean_values(self, config: Dict[str, Any], key_patterns: List[str]) -> List[bool]:
        """Extract boolean values from configuration based on key patterns."""
        values = []
        
        def extract_from_obj(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if any(pattern in key.lower() for pattern in key_patterns):
                        if isinstance(value, bool):
                            values.append(value)
                    extract_from_obj(value, current_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    current_path = f"{path}[{i}]"
                    extract_from_obj(item, current_path)
        
        extract_from_obj(config)
        return values
    
    def _validate_cross_file_consistency(self, all_configs: Dict[str, Dict[str, Any]]):
        """Validate consistency across multiple configuration files."""
        # Check for duplicate values across files
        for value, locations in self.duplicates.items():
            if len(locations) > VALUE_ONE:
                self.violations.append({
                    "type": "CROSS_FILE_DUPLICATE",
                    "value": value,
                    "locations": locations,
                    "recommendation": "Consolidate into unified constants"
                })
    
    def _generate_validation_report(self) -> Dict[str, Any]:
        """Generate a comprehensive validation report."""
        report = {
            "validation_summary": {
                "total_files_checked": len(self._find_config_files()),
                "total_violations": len(self.violations),
                "duplicate_values": len(self.duplicates),
                "consistency_issues": len(self.consistency_issues)
            },
            "violations": self.violations,
            "duplicates": dict(self.duplicates),
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        
        if self.violations:
            recommendations.append("Implement unified configuration constants to eliminate SSOT violations")
            recommendations.append("Use config.constants module for all configuration values")
            recommendations.append("Establish configuration inheritance hierarchy")
        
        if self.duplicates:
            recommendations.append("Consolidate duplicate values into centralized constants")
            recommendations.append("Implement configuration validation in CI/CD pipeline")
        
        if not recommendations:
            recommendations.append("Configuration system is well-structured and follows SSOT principles")
        
        return recommendations

def validate_configuration(config_dir: str = "config") -> Dict[str, Any]:
    """Convenience function to validate configuration directory."""
    validator = ConfigurationValidator(config_dir)
    return validator.validate_all_configs()

def check_ssot_violations(config_dir: str = "config") -> List[Dict[str, Any]]:
    """Check specifically for SSOT violations."""
    validator = ConfigurationValidator(config_dir)
    validator.validate_all_configs()
    return [v for v in validator.violations if "SSOT" in v.get("type", "")]

if __name__ == "__main__":
    # Run validation when script is executed directly
    report = validate_configuration()
    print(json.dumps(report, indent=VALUE_TWO))
