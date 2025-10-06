#!/usr/bin/env python3
"""
Unified Configuration System - V2 Compliance
============================================

Centralized configuration management consolidating all config.py files.
Provides Single Source of Truth (SSOT) for all system configurations.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

# Consolidated into src/core/config_core.py - Single Source of Truth
from .config_core import get_config, get_agent_config, get_timeout_config, get_threshold_config, get_test_config


# Enums moved to config_core.py - Single Source of Truth


@dataclass
class TimeoutConfig:
    """Centralized timeout configurations."""
    # Browser/UI timeouts
    scrape_timeout: float = get_config("SCRAPE_TIMEOUT", 30.0)
    response_wait_timeout: float = get_config("RESPONSE_WAIT_TIMEOUT", 120.0)

    # Quality monitoring timeouts
    quality_check_interval: float = get_config("QUALITY_CHECK_INTERVAL", 30.0)

    # Performance monitoring timeouts
    metrics_collection_interval: float = get_config("METRICS_COLLECTION_INTERVAL", 60.0)

    # Test timeouts
    smoke_test_timeout: int = get_config("SMOKE_TEST_TIMEOUT", 60)
    unit_test_timeout: int = get_config("UNIT_TEST_TIMEOUT", 120)
    integration_test_timeout: int = get_config("INTEGRATION_TEST_TIMEOUT", 300)
    performance_test_timeout: int = get_config("PERFORMANCE_TEST_TIMEOUT", 600)
    security_test_timeout: int = get_config("SECURITY_TEST_TIMEOUT", 180)
    api_test_timeout: int = get_config("API_TEST_TIMEOUT", 240)
    coordination_test_timeout: int = get_config("COORDINATION_TEST_TIMEOUT", 180)
    learning_test_timeout: int = get_config("LEARNING_TEST_TIMEOUT", 180)


@dataclass
class AgentConfig:
    """Centralized agent configuration."""
    agent_count: int = get_config("AGENT_COUNT", 8)
    captain_id: str = get_config("CAPTAIN_ID", "Agent-4")
    default_mode: str = get_config("DEFAULT_MODE", "pyautogui")
    coordinate_mode: str = get_config("COORDINATE_MODE", "8-agent")

    @property
    def agent_ids(self) -> List[str]:
        """Get list of all agent IDs."""
        return [f"Agent-{i}" for i in range(1, self.agent_count + 1)]


@dataclass
class FilePatternConfig:
    """Centralized file pattern configurations."""
    # Test file patterns
    test_file_pattern: str = get_config("TEST_FILE_PATTERN", "test_*.py")

    # Project file patterns
    architecture_files: str = get_config("ARCHITECTURE_FILES", r'\.(py|js|ts|java|cpp|h|md)$')
    config_files: str = get_config("CONFIG_FILES", r'(config|settings|env|yml|yaml|json|toml|ini)$')
    test_files: str = get_config("TEST_FILES", r'(test|spec)\.(py|js|ts|java)$')
    docs_files: str = get_config("DOCS_FILES", r'(README|CHANGELOG|CONTRIBUTING|docs?)\.md$')
    build_files: str = get_config("BUILD_FILES", r'(Dockerfile|docker-compose|\.gitlab-ci|\.github|Makefile|build\.gradle|pom\.xml)$')

    @property
    def project_patterns(self) -> Dict[str, str]:
        """Get all project file patterns."""
        return {
            'architecture_files': self.architecture_files,
            'config_files': self.config_files,
            'test_files': self.test_files,
            'docs_files': self.docs_files,
            'build_files': self.build_files
        }


@dataclass
class ThresholdConfig:
    """Centralized threshold and alert configurations."""
    # Quality monitoring thresholds
    test_failure_threshold: int = get_config("TEST_FAILURE_THRESHOLD", 0)
    performance_degradation_threshold: float = get_config("PERFORMANCE_DEGRADATION_THRESHOLD", 100.0)
    coverage_threshold: float = get_config("COVERAGE_THRESHOLD", 80.0)

    # Performance benchmark targets
    response_time_target: float = get_config("RESPONSE_TIME_TARGET", 100.0)  # ms
    throughput_target: float = get_config("THROUGHPUT_TARGET", 1000.0)  # ops/sec
    scalability_target: int = get_config("SCALABILITY_TARGET", 100)  # concurrent users
    reliability_target: float = get_config("RELIABILITY_TARGET", 99.9)  # %
    latency_target: float = get_config("LATENCY_TARGET", 50.0)  # ms

    # Messaging performance thresholds
    single_message_timeout: float = get_config("SINGLE_MESSAGE_TIMEOUT", 1.0)
    bulk_message_timeout: float = get_config("BULK_MESSAGE_TIMEOUT", 10.0)
    concurrent_message_timeout: float = get_config("CONCURRENT_MESSAGE_TIMEOUT", 5.0)
    min_throughput: float = get_config("MIN_THROUGHPUT", 10.0)
    max_memory_per_message: int = get_config("MAX_MEMORY_PER_MESSAGE", 1024)

    @property
    def alert_rules(self) -> Dict[str, Dict[str, Any]]:
        """Get quality alert rules."""
        return {
            "test_failure": {
                "threshold": self.test_failure_threshold,
                "severity": "high",
                "message": "Test failures detected",
            },
            "performance_degradation": {
                "threshold": self.performance_degradation_threshold,
                "severity": "medium",
                "message": "Performance degradation detected",
            },
            "low_coverage": {
                "threshold": self.coverage_threshold,
                "severity": "medium",
                "message": "Test coverage below threshold",
            },
        }

    @property
    def benchmark_targets(self) -> Dict[str, Dict[str, Any]]:
        """Get performance benchmark targets."""
        return {
            "response_time": {"target": self.response_time_target, "unit": "ms"},
            "throughput": {"target": self.throughput_target, "unit": "ops/sec"},
            "scalability": {"target": self.scalability_target, "unit": "concurrent_users"},
            "reliability": {"target": self.reliability_target, "unit": "%"},
            "latency": {"target": self.latency_target, "unit": "ms"},
        }


@dataclass
class BrowserConfig:
    """Centralized browser interaction configuration."""
    # URLs
    gpt_url: str = get_config("GPT_URL", 'https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager')
    conversation_url: str = get_config("CONVERSATION_URL", 'https://chatgpt.com/c/68bf1b1b-37b8-8324-be55-e3ccf20af737')

    # Primary selectors
    input_selector: str = get_config("INPUT_SELECTOR", "textarea[data-testid='prompt-textarea']")
    send_button_selector: str = get_config("SEND_BUTTON_SELECTOR", "button[data-testid='send-button']")
    response_selector: str = get_config("RESPONSE_SELECTOR", "[data-testid='conversation-turn']:last-child .markdown")
    thinking_indicator: str = get_config("THINKING_INDICATOR", "[data-testid='thinking-indicator']")

    # Fallback selectors
    input_fallback_selectors: List[str] = field(default_factory=lambda: [
        "textarea[placeholder*='Message']", "textarea[placeholder*='Ask']",
        'textarea', '#prompt-textarea', "[contenteditable='true']",
        "div[contenteditable='true']", 'p[data-placeholder]',
        "[data-placeholder='Ask anything']"
    ])

    send_fallback_selectors: List[str] = field(default_factory=lambda: [
        "button[data-testid='send-button']", "button[type='submit']",
        "button:has-text('Send')"
    ])

    response_fallback_selectors: List[str] = field(default_factory=lambda: [
        "[data-testid='conversation-turn']:last-child .markdown",
        '.message-content:last-child', '.markdown:last-child',
        '[data-message-id]:last-child'
    ])

    # Retry configuration
    max_scrape_retries: int = get_config("MAX_SCRAPE_RETRIES", 3)


@dataclass
class TestConfig:
    """Centralized test configuration."""
    # Test categories
    test_categories: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "smoke": {
            "description": "Smoke tests for basic functionality validation",
            "marker": "smoke",
            "timeout": 60,
            "critical": True,
            "directory": "smoke",
        },
        "unit": {
            "description": "Unit tests for individual components",
            "marker": "unit",
            "timeout": 120,
            "critical": True,
            "directory": "unit",
        },
        "integration": {
            "description": "Integration tests for component interaction",
            "marker": "integration",
            "timeout": 300,
            "critical": False,
            "directory": "integration",
        },
        "performance": {
            "description": "Performance and load testing",
            "marker": "performance",
            "timeout": 600,
            "critical": False,
            "directory": "performance",
        },
        "security": {
            "description": "Security and vulnerability testing",
            "marker": "security",
            "timeout": 180,
            "critical": True,
            "directory": "security",
        },
        "api": {
            "description": "API endpoint testing",
            "marker": "api",
            "timeout": 240,
            "critical": False,
            "directory": "api",
        },
        "behavior": {
            "description": "Behavior tree tests",
            "marker": "behavior",
            "timeout": 120,
            "critical": False,
            "directory": "behavior_trees",
        },
        "decision": {
            "description": "Decision engine tests",
            "marker": "decision",
            "timeout": 120,
            "critical": False,
            "directory": "decision_engines",
        },
        "coordination": {
            "description": "Multi-agent coordination tests",
            "marker": "coordination",
            "timeout": 180,
            "critical": False,
            "directory": "multi_agent",
        },
        "learning": {
            "description": "Learning component tests",
            "marker": "learning",
            "timeout": 180,
            "critical": False,
            "directory": "learning",
        },
    })

    # Coverage configuration
    coverage_report_precision: int = get_config("COVERAGE_REPORT_PRECISION", 2)
    history_window: int = get_config("HISTORY_WINDOW", 100)


@dataclass
class ReportConfig:
    """Centralized reporting configuration."""
    # Report formats
    class ReportFormat(str, Enum):
        JSON = "json"
        MARKDOWN = "markdown"
        HTML = "html"
        CSV = "csv"
        CONSOLE = "console"

    # Default settings
    reports_dir: Path = Path(get_config("REPORTS_DIR", "reports"))
    default_format: ReportFormat = ReportFormat.JSON
    include_metadata: bool = get_config("INCLUDE_METADATA", True)
    include_recommendations: bool = get_config("INCLUDE_RECOMMENDATIONS", True)

    # Templates
    html_template: str = """<!DOCTYPE html>
<html>
<head><title>Error Analytics Report</title></head>
<body>{content}</body>
</html>
"""

    markdown_template: str = """# Error Analytics Report\n\n{content}\n"""


@dataclass
class UnifiedConfig:
    """Unified configuration system consolidating all config.py files."""

    timeouts: TimeoutConfig = field(default_factory=TimeoutConfig)
    agents: AgentConfig = field(default_factory=AgentConfig)
    file_patterns: FilePatternConfig = field(default_factory=FilePatternConfig)
    thresholds: ThresholdConfig = field(default_factory=ThresholdConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    tests: TestConfig = field(default_factory=TestConfig)
    reports: ReportConfig = field(default_factory=ReportConfig)

    def __post_init__(self):
        """Initialize configuration after creation."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Unified configuration system initialized")

    def validate(self) -> List[str]:
        """Validate all configurations and return any issues."""
        issues = []

        # Validate timeouts
        if self.timeouts.scrape_timeout <= 0:
            issues.append("Scrape timeout must be positive")
        if self.timeouts.response_wait_timeout <= 0:
            issues.append("Response wait timeout must be positive")
        if self.timeouts.quality_check_interval <= 0:
            issues.append("Quality check interval must be positive")
        if self.timeouts.metrics_collection_interval <= 0:
            issues.append("Metrics collection interval must be positive")

        # Validate agent configuration
        if self.agents.agent_count <= 0 or self.agents.agent_count > 20:
            issues.append("Agent count must be between 1 and 20")
        if not self.agents.captain_id:
            issues.append("Captain ID cannot be empty")
        if not self.agents.captain_id.startswith('Agent-'):
            issues.append("Captain ID must start with 'Agent-'")
        if self.agents.default_mode not in ['pyautogui', 'selenium', 'manual']:
            issues.append("Default mode must be one of: pyautogui, selenium, manual")

        # Validate browser configuration
        if not self.browser.gpt_url.startswith('https://'):
            issues.append("GPT URL must be HTTPS")
        if not self.browser.conversation_url.startswith('https://'):
            issues.append("Conversation URL must be HTTPS")
        if not self.browser.input_selector.strip():
            issues.append("Input selector cannot be empty")
        if not self.browser.send_button_selector.strip():
            issues.append("Send button selector cannot be empty")
        if self.browser.max_scrape_retries < 0:
            issues.append("Max scrape retries must be non-negative")

        # Validate thresholds
        if self.thresholds.coverage_threshold < 0 or self.thresholds.coverage_threshold > 100:
            issues.append("Coverage threshold must be between 0 and 100")
        if self.thresholds.reliability_target < 0 or self.thresholds.reliability_target > 100:
            issues.append("Reliability target must be between 0 and 100")
        if self.thresholds.response_time_target <= 0:
            issues.append("Response time target must be positive")
        if self.thresholds.throughput_target <= 0:
            issues.append("Throughput target must be positive")
        if self.thresholds.scalability_target <= 0:
            issues.append("Scalability target must be positive")
        if self.thresholds.latency_target <= 0:
            issues.append("Latency target must be positive")

        # Validate file patterns
        if not self.file_patterns.test_file_pattern.strip():
            issues.append("Test file pattern cannot be empty")
        if not self.file_patterns.architecture_files.strip():
            issues.append("Architecture files pattern cannot be empty")

        # Validate test configuration
        if self.tests.coverage_report_precision < 0 or self.tests.coverage_report_precision > 10:
            issues.append("Coverage report precision must be between 0 and 10")
        if self.tests.history_window <= 0:
            issues.append("History window must be positive")

        # Validate report configuration
        if not self.reports.reports_dir.exists() and not self.reports.reports_dir.parent.exists():
            issues.append("Reports directory parent must exist")

        return issues

    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of all configurations."""
        return {
            "timeouts": {
                "scrape_timeout": self.timeouts.scrape_timeout,
                "response_wait_timeout": self.timeouts.response_wait_timeout,
                "quality_check_interval": self.timeouts.quality_check_interval,
                "metrics_collection_interval": self.timeouts.metrics_collection_interval,
            },
            "agents": {
                "agent_count": self.agents.agent_count,
                "captain_id": self.agents.captain_id,
                "agent_ids": self.agents.agent_ids,
            },
            "thresholds": {
                "coverage_threshold": self.thresholds.coverage_threshold,
                "response_time_target": self.thresholds.response_time_target,
                "throughput_target": self.thresholds.throughput_target,
            },
            "browser": {
                "gpt_url": self.browser.gpt_url,
                "input_selector": self.browser.input_selector,
                "max_retries": self.browser.max_scrape_retries,
            },
            "tests": {
                "test_categories_count": len(self.tests.test_categories),
                "coverage_precision": self.tests.coverage_report_precision,
            },
        }


# Global unified configuration instance
unified_config = UnifiedConfig()


def get_unified_config() -> UnifiedConfig:
    """Get the global unified configuration instance."""
    return unified_config


def reload_config() -> UnifiedConfig:
    """Reload configuration from sources."""
    global unified_config
    unified_config = UnifiedConfig()
    return unified_config


# Convenience functions for backward compatibility
def get_timeout_config() -> TimeoutConfig:
    """Get timeout configuration."""
    return unified_config.timeouts


def get_agent_config() -> AgentConfig:
    """Get agent configuration."""
    return unified_config.agents


def get_threshold_config() -> ThresholdConfig:
    """Get threshold configuration."""
    return unified_config.thresholds


def get_browser_config() -> BrowserConfig:
    """Get browser configuration."""
    return unified_config.browser


def get_test_config() -> TestConfig:
    """Get test configuration."""
    return unified_config.tests


def get_file_pattern_config() -> FilePatternConfig:
    """Get file pattern configuration."""
    return unified_config.file_patterns


def get_report_config() -> ReportConfig:
    """Get report configuration."""
    return unified_config.reports
