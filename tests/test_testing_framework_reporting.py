#!/usr/bin/env python3
"""
Testing Framework Reporting Tests - TDD Implementation
======================================================

Tests for reporting configuration and output.
"""

from unittest.mock import Mock

import pytest

from src.core.testing_framework import TestOrchestrator, TestingFrameworkCLI


@pytest.fixture
def test_orchestrator():
    """Create a test orchestrator instance."""
    return TestOrchestrator()


@pytest.fixture
def cli():
    """Create a CLI instance."""
    return TestingFrameworkCLI()


@pytest.fixture
def cli_args():
    """Mock CLI arguments for reporting configuration."""
    args = Mock()
    args.retry_failed = True
    args.parallel = True
    args.output = "json"
    return args


class TestReportingFeatures:
    """Tests for reporting configuration options."""

    def test_orchestrator_reporting_config(self, test_orchestrator):
        config = {"auto_retry_failed": False, "generate_reports": False}
        test_orchestrator.configure(config)
        assert test_orchestrator.config["generate_reports"] is False

    def test_cli_reporting_configuration(self, cli, cli_args):
        cli._configure_orchestrator(cli_args)
        assert cli.orchestrator.runner.global_config["report_format"] == "json"
