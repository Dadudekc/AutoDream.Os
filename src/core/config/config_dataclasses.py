#!/usr/bin/env python3
"""
Configuration Dataclasses - V2 Compliance Module
================================================

Dataclass configuration models for unified configuration system.
Extracted from config_ssot.py for better modularity.

V2 Compliance: Single Responsibility Principle, <400 lines
SOLID Principles: Open-Closed Principle, Interface Segregation

Author: Agent-2 (Architecture & Design Specialist) - ROI 32.26 Task
Extracted from: Agent-7's config_ssot.py consolidation
Created: 2025-10-13
License: MIT
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config_enums import ReportFormat

logger = logging.getLogger(__name__)


@dataclass
class TimeoutConfig:
    """Centralized timeout configurations."""

    # Browser/UI timeouts
    scrape_timeout: float = 30.0
    response_wait_timeout: float = 120.0
    browser_timeout: float = 30.0
    page_load_timeout: float = 60.0

    # Quality monitoring timeouts
    quality_check_interval: float = 30.0
    performance_check_interval: float = 60.0
    health_check_timeout: float = 10.0

    # Metrics collection
    metrics_collection_interval: float = 60.0

    # Test timeouts
    smoke_test_timeout: int = 60
    unit_test_timeout: int = 120
    integration_test_timeout: int = 300
    performance_test_timeout: int = 600
    security_test_timeout: int = 180
    api_test_timeout: int = 240
    coordination_test_timeout: int = 180
    learning_test_timeout: int = 180
    test_timeout: float = 300.0

    # FSM timeouts
    fsm_state_timeout: float = 300.0
    fsm_transition_timeout: float = 30.0

    # Messaging timeouts
    message_timeout: float = 30.0


@dataclass
class AgentConfig:
    """Centralized agent configuration."""

    agent_count: int = 8
    captain_id: str = "Agent-4"
    default_mode: str = "pyautogui"
    coordinate_mode: str = "8-agent"

    @property
    def agent_ids(self) -> list[str]:
        """Get list of all agent IDs."""
        return [f"Agent-{i}" for i in range(1, self.agent_count + 1)]


@dataclass
class BrowserConfig:
    """Unified browser configuration (ChatGPT + Driver management)."""

    # ChatGPT URLs
    gpt_url: str = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
    conversation_url: str = "https://chatgpt.com/c/68bf1b1b-37b8-8324-be55-e3ccf20af737"

    # ChatGPT Selectors
    input_selector: str = "textarea[data-testid='prompt-textarea']"
    send_button_selector: str = "button[data-testid='send-button']"
    response_selector: str = "[data-testid='conversation-turn']:last-child .markdown"
    thinking_indicator: str = "[data-testid='thinking-indicator']"

    # Fallback selectors
    input_fallback_selectors: list[str] = field(
        default_factory=lambda: [
            "textarea#prompt-textarea",
            "textarea[placeholder*='Message']",
            "div[contenteditable='true']",
        ]
    )
    send_fallback_selectors: list[str] = field(
        default_factory=lambda: [
            "button[aria-label='Send']",
            "button:has(svg[data-testid='send-button-icon'])",
            "button.absolute.bottom-0",
        ]
    )
    response_fallback_selectors: list[str] = field(
        default_factory=lambda: [
            ".markdown.prose",
            "[data-message-author-role='assistant']",
            ".agent-turn",
        ]
    )

    # Driver paths & settings
    template_dir: Path = field(default_factory=lambda: Path("templates"))
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    log_dir: Path = field(default_factory=lambda: Path("logs"))
    profile_dir: Path = field(default_factory=lambda: Path("runtime/browser/profiles"))
    cookie_file: Path = field(default_factory=lambda: Path("runtime/browser/cookies.json"))

    # Driver configuration
    driver_type: str = "chrome"
    undetected_mode: bool = True
    headless: bool = False
    page_load_timeout: int = 30
    implicit_wait: int = 10
    max_instances: int = 3
    max_scrape_retries: int = 3

    # Mobile emulation
    mobile_emulation_enabled: bool = False
    mobile_device: str = "iphone_12"


@dataclass
class ThresholdConfig:
    """Centralized threshold and alert configurations."""

    # Quality monitoring
    test_failure_threshold: int = 0
    performance_degradation_threshold: float = 100.0
    coverage_threshold: float = 85.0
    alert_threshold: float = 0.8

    # Performance benchmarks
    response_time_target: float = 100.0  # ms
    throughput_target: float = 1000.0  # ops/sec
    scalability_target: int = 100  # concurrent users
    reliability_target: float = 99.9  # %
    latency_target: float = 50.0  # ms

    # Messaging performance
    single_message_timeout: float = 1.0
    bulk_message_timeout: float = 10.0
    concurrent_message_timeout: float = 5.0
    min_throughput: float = 10.0
    max_memory_per_message: int = 1024

    # System thresholds
    memory_threshold: float = 80.0
    cpu_threshold: float = 70.0

    @property
    def alert_rules(self) -> dict[str, dict[str, Any]]:
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
    def benchmark_targets(self) -> dict[str, dict[str, Any]]:
        """Get performance benchmark targets."""
        return {
            "response_time": {"target": self.response_time_target, "unit": "ms"},
            "throughput": {"target": self.throughput_target, "unit": "ops/sec"},
            "scalability": {"target": self.scalability_target, "unit": "concurrent_users"},
            "reliability": {"target": self.reliability_target, "unit": "%"},
            "latency": {"target": self.latency_target, "unit": "ms"},
        }


@dataclass
class FilePatternConfig:
    """Centralized file pattern configurations."""

    test_file_pattern: str = "test_*.py"
    architecture_files: str = r"\.(py|js|ts|java|cpp|h|md)$"
    config_files: str = r"(config|settings|env|yml|yaml|json|toml|ini)$"
    test_files: str = r"(test|spec)\.(py|js|ts|java)$"
    docs_files: str = r"(README|CHANGELOG|CONTRIBUTING|docs?)\.md$"
    build_files: str = (
        r"(Dockerfile|docker-compose|\.gitlab-ci|\.github|Makefile|build\.gradle|pom\.xml)$"
    )

    @property
    def project_patterns(self) -> dict[str, str]:
        """Get all project file patterns."""
        return {
            "architecture_files": self.architecture_files,
            "config_files": self.config_files,
            "test_files": self.test_files,
            "docs_files": self.docs_files,
            "build_files": self.build_files,
        }


@dataclass
class TestConfig:
    """Centralized test configuration."""

    # Coverage configuration
    coverage_report_precision: int = 2
    history_window: int = 100

    @property
    def test_categories(self) -> dict[str, dict[str, Any]]:
        """Get test category definitions (lazy loaded)."""
        try:
            from .test_categories_config import get_test_categories

            return get_test_categories()
        except ImportError:
            logger.warning("test_categories_config not available, using defaults")
            return {}


@dataclass
class ReportConfig:
    """Centralized reporting configuration."""

    # Default settings
    reports_dir: Path = field(default_factory=lambda: Path("reports"))
    default_format: ReportFormat = ReportFormat.JSON
    include_metadata: bool = True
    include_recommendations: bool = True

    # Templates
    html_template: str = """<!DOCTYPE html>
<html>
<head><title>Error Analytics Report</title></head>
<body>{content}</body>
</html>
"""

    markdown_template: str = """# Error Analytics Report\n\n{content}\n"""


__all__ = [
    "TimeoutConfig",
    "AgentConfig",
    "BrowserConfig",
    "ThresholdConfig",
    "FilePatternConfig",
    "TestConfig",
    "ReportConfig",
]
