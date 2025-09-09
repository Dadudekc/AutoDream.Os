#!/usr/bin/env python3
"""
Environment Variable Loader - V2 Compliance
===========================================

Loads environment variables and integrates them with the unified configuration system.
Provides type conversion, validation, and fallback mechanisms.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .unified_config import get_unified_config


class EnvironmentLoader:
    """Loads and validates environment variables for unified configuration."""
    
    def __init__(self, env_file: Optional[Path] = None):
        """Initialize environment loader."""
        self.env_file = env_file or Path(".env")
        self.logger = logging.getLogger(__name__)
        self._loaded_vars: Dict[str, Any] = {}
        
    def load_env_file(self) -> bool:
        """Load environment variables from .env file if it exists."""
        if not self.env_file.exists():
            self.logger.warning(f"Environment file {self.env_file} not found")
            return False
            
        try:
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                        
                    # Parse key=value pairs
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                            
                        os.environ[key] = value
                        self._loaded_vars[key] = value
                        
            self.logger.info(f"Loaded {len(self._loaded_vars)} environment variables from {self.env_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading environment file {self.env_file}: {e}")
            return False
    
    def get_env_var(self, key: str, default: Any = None, var_type: type = str) -> Any:
        """Get environment variable with type conversion and validation."""
        value = os.environ.get(key, default)
        
        if value is None:
            return default
            
        try:
            # Type conversion
            if var_type == bool:
                return value.lower() in ('true', '1', 'yes', 'on')
            elif var_type == int:
                return int(value)
            elif var_type == float:
                return float(value)
            elif var_type == list:
                return [item.strip() for item in value.split(',')]
            elif var_type == Path:
                return Path(value)
            else:
                return str(value)
                
        except (ValueError, TypeError) as e:
            self.logger.warning(f"Invalid value for {key}: {value} (expected {var_type.__name__})")
            return default
    
    def validate_critical_settings(self) -> List[str]:
        """Validate critical environment settings."""
        issues = []
        
        # Validate required settings
        required_settings = [
            'AGENT_COUNT',
            'CAPTAIN_ID',
            'DEFAULT_MODE',
            'COORDINATE_MODE'
        ]
        
        for setting in required_settings:
            if not os.environ.get(setting):
                issues.append(f"Required setting {setting} is not set")
        
        # Validate numeric settings
        numeric_settings = {
            'AGENT_COUNT': (int, 1, 20),
            'SCRAPE_TIMEOUT': (float, 1.0, 300.0),
            'RESPONSE_WAIT_TIMEOUT': (float, 10.0, 600.0),
            'COVERAGE_THRESHOLD': (float, 0.0, 100.0)
        }
        
        for setting, (var_type, min_val, max_val) in numeric_settings.items():
            value = self.get_env_var(setting, var_type=var_type)
            if value is not None and not (min_val <= value <= max_val):
                issues.append(f"{setting} must be between {min_val} and {max_val}")
        
        # Validate URL settings
        url_settings = ['GPT_URL', 'CONVERSATION_URL']
        for setting in url_settings:
            value = os.environ.get(setting, '')
            if value and not value.startswith('https://'):
                issues.append(f"{setting} must be a valid HTTPS URL")
        
        return issues
    
    def load_unified_config_from_env(self) -> bool:
        """Load unified configuration from environment variables."""
        try:
            # Load .env file first
            self.load_env_file()
            
            # Validate critical settings
            issues = self.validate_critical_settings()
            if issues:
                self.logger.error("Environment validation failed:")
                for issue in issues:
                    self.logger.error(f"  - {issue}")
                return False
            
            # Update unified config with environment values
            config = get_unified_config()
            
            # Update timeout config
            config.timeouts.scrape_timeout = self.get_env_var('SCRAPE_TIMEOUT', 30.0, float)
            config.timeouts.response_wait_timeout = self.get_env_var('RESPONSE_WAIT_TIMEOUT', 120.0, float)
            config.timeouts.quality_check_interval = self.get_env_var('QUALITY_CHECK_INTERVAL', 30.0, float)
            config.timeouts.metrics_collection_interval = self.get_env_var('METRICS_COLLECTION_INTERVAL', 60.0, float)
            
            # Update agent config
            config.agents.agent_count = self.get_env_var('AGENT_COUNT', 8, int)
            config.agents.captain_id = self.get_env_var('CAPTAIN_ID', 'Agent-4', str)
            config.agents.default_mode = self.get_env_var('DEFAULT_MODE', 'pyautogui', str)
            config.agents.coordinate_mode = self.get_env_var('COORDINATE_MODE', '8-agent', str)
            
            # Update file pattern config
            config.file_patterns.test_file_pattern = self.get_env_var('TEST_FILE_PATTERN', 'test_*.py', str)
            config.file_patterns.architecture_files = self.get_env_var('ARCHITECTURE_FILES', r'\.(py|js|ts|java|cpp|h|md)$', str)
            config.file_patterns.config_files = self.get_env_var('CONFIG_FILES', r'(config|settings|env|yml|yaml|json|toml|ini)$', str)
            config.file_patterns.test_files = self.get_env_var('TEST_FILES', r'(test|spec)\.(py|js|ts|java)$', str)
            config.file_patterns.docs_files = self.get_env_var('DOCS_FILES', r'(README|CHANGELOG|CONTRIBUTING|docs?)\.md$', str)
            config.file_patterns.build_files = self.get_env_var('BUILD_FILES', r'(Dockerfile|docker-compose|\.gitlab-ci|\.github|Makefile|build\.gradle|pom\.xml)$', str)
            
            # Update threshold config
            config.thresholds.test_failure_threshold = self.get_env_var('TEST_FAILURE_THRESHOLD', 0, int)
            config.thresholds.performance_degradation_threshold = self.get_env_var('PERFORMANCE_DEGRADATION_THRESHOLD', 100.0, float)
            config.thresholds.coverage_threshold = self.get_env_var('COVERAGE_THRESHOLD', 80.0, float)
            config.thresholds.response_time_target = self.get_env_var('RESPONSE_TIME_TARGET', 100.0, float)
            config.thresholds.throughput_target = self.get_env_var('THROUGHPUT_TARGET', 1000.0, float)
            config.thresholds.scalability_target = self.get_env_var('SCALABILITY_TARGET', 100, int)
            config.thresholds.reliability_target = self.get_env_var('RELIABILITY_TARGET', 99.9, float)
            config.thresholds.latency_target = self.get_env_var('LATENCY_TARGET', 50.0, float)
            config.thresholds.single_message_timeout = self.get_env_var('SINGLE_MESSAGE_TIMEOUT', 1.0, float)
            config.thresholds.bulk_message_timeout = self.get_env_var('BULK_MESSAGE_TIMEOUT', 10.0, float)
            config.thresholds.concurrent_message_timeout = self.get_env_var('CONCURRENT_MESSAGE_TIMEOUT', 5.0, float)
            config.thresholds.min_throughput = self.get_env_var('MIN_THROUGHPUT', 10.0, float)
            config.thresholds.max_memory_per_message = self.get_env_var('MAX_MEMORY_PER_MESSAGE', 1024, int)
            
            # Update browser config
            config.browser.gpt_url = self.get_env_var('GPT_URL', 'https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager', str)
            config.browser.conversation_url = self.get_env_var('CONVERSATION_URL', 'https://chatgpt.com/c/68bf1b1b-37b8-8324-be55-e3ccf20af737', str)
            config.browser.input_selector = self.get_env_var('INPUT_SELECTOR', "textarea[data-testid='prompt-textarea']", str)
            config.browser.send_button_selector = self.get_env_var('SEND_BUTTON_SELECTOR', "button[data-testid='send-button']", str)
            config.browser.response_selector = self.get_env_var('RESPONSE_SELECTOR', "[data-testid='conversation-turn']:last-child .markdown", str)
            config.browser.thinking_indicator = self.get_env_var('THINKING_INDICATOR', "[data-testid='thinking-indicator']", str)
            config.browser.max_scrape_retries = self.get_env_var('MAX_SCRAPE_RETRIES', 3, int)
            
            # Update test config
            config.tests.coverage_report_precision = self.get_env_var('COVERAGE_REPORT_PRECISION', 2, int)
            config.tests.history_window = self.get_env_var('HISTORY_WINDOW', 100, int)
            
            # Update report config
            config.reports.reports_dir = self.get_env_var('REPORTS_DIR', Path('reports'), Path)
            config.reports.include_metadata = self.get_env_var('INCLUDE_METADATA', True, bool)
            config.reports.include_recommendations = self.get_env_var('INCLUDE_RECOMMENDATIONS', True, bool)
            
            self.logger.info("Successfully loaded unified configuration from environment variables")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading unified config from environment: {e}")
            return False
    
    def get_environment_summary(self) -> Dict[str, Any]:
        """Get a summary of loaded environment variables."""
        return {
            "loaded_vars": len(self._loaded_vars),
            "env_file": str(self.env_file),
            "env_file_exists": self.env_file.exists(),
            "critical_settings_valid": len(self.validate_critical_settings()) == 0
        }


# Global environment loader instance
env_loader = EnvironmentLoader()


def load_environment_config() -> bool:
    """Load environment configuration into unified config system."""
    return env_loader.load_unified_config_from_env()


def get_env_summary() -> Dict[str, Any]:
    """Get environment configuration summary."""
    return env_loader.get_environment_summary()
