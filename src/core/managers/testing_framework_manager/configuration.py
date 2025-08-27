#!/usr/bin/env python3
"""Configuration data structure for TestingFrameworkManager."""

from dataclasses import dataclass


@dataclass
class TestConfiguration:
    """Represents testing framework configuration."""

    framework_type: str  # "unittest", "pytest", "custom"
    parallel_execution: bool = False
    max_workers: int = 4
    timeout_seconds: int = 300
    verbose_output: bool = True
    generate_reports: bool = True
    coverage_enabled: bool = False
    retry_failed_tests: bool = False
    max_retries: int = 3
