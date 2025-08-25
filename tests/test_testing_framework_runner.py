#!/usr/bin/env python3
"""
Testing Framework Runner Tests - TDD Implementation
===================================================

Tests for runner, executor, orchestrator and CLI components.
"""

import asyncio
from unittest.mock import Mock, patch

import pytest

from src.core.testing_framework.testing_types import TestStatus, TestPriority
from src.core.testing_framework.integration_tests import (
    CrossSystemCommunicationTest,
    ServiceIntegrationTest,
)
from src.core.testing_framework.testing_orchestration_core import IntegrationTestSuite
from src.core.testing_framework.testing_orchestration_runner import IntegrationTestRunner
from src.core.testing_framework.testing_orchestration_executor import TestExecutor
from src.core.testing_framework.testing_orchestration_orchestrator import TestOrchestrator
from src.core.testing_framework.testing_cli import TestingFrameworkCLI


@pytest.fixture
def test_runner():
    """Create a test runner instance."""
    return IntegrationTestRunner()


@pytest.fixture
def runner_sample_suite():
    """Create a sample test suite for runner tests."""
    suite = IntegrationTestSuite("Sample Suite", "Sample description")
    suite.add_test(CrossSystemCommunicationTest("Test 1", TestPriority.NORMAL))
    return suite


@pytest.fixture
def test_executor():
    """Create a test executor instance."""
    return TestExecutor()


@pytest.fixture
def sample_test():
    """Create a sample test instance."""
    return CrossSystemCommunicationTest("Executor Test", TestPriority.NORMAL)


@pytest.fixture
def test_orchestrator():
    """Create a test orchestrator instance."""
    return TestOrchestrator()


@pytest.fixture
def orchestrator_sample_suite():
    """Create a sample test suite for orchestrator tests."""
    suite = IntegrationTestSuite("Orchestrator Suite", "Orchestrator description")
    suite.add_test(CrossSystemCommunicationTest("Orchestrator Test", TestPriority.NORMAL))
    return suite


@pytest.fixture
def cli():
    """Create a CLI instance."""
    return TestingFrameworkCLI()


class TestIntegrationTestRunner:
    """Tests for IntegrationTestRunner."""

    @pytest.mark.unit
    def test_runner_initialization(self, test_runner):
        assert len(test_runner.test_suites) == 0
        assert test_runner.global_config["parallel_suites"] is False
        assert test_runner.global_config["max_parallel_suites"] == 3

    @pytest.mark.unit
    def test_add_test_suite(self, test_runner, runner_sample_suite):
        test_runner.add_test_suite(runner_sample_suite)
        assert len(test_runner.test_suites) == 1
        assert test_runner.test_suites[0] == runner_sample_suite

    @pytest.mark.unit
    def test_add_invalid_suite(self, test_runner):
        with pytest.raises(ValueError, match="Suite must be an instance of IntegrationTestSuite"):
            test_runner.add_test_suite("invalid_suite")

    @pytest.mark.unit
    def test_remove_test_suite(self, test_runner, runner_sample_suite):
        test_runner.add_test_suite(runner_sample_suite)
        assert len(test_runner.test_suites) == 1
        result = test_runner.remove_test_suite("Sample Suite")
        assert result is True
        assert len(test_runner.test_suites) == 0

    @pytest.mark.unit
    def test_remove_nonexistent_suite(self, test_runner):
        result = test_runner.remove_test_suite("Nonexistent Suite")
        assert result is False

    @pytest.mark.unit
    def test_set_global_config(self, test_runner):
        config = {"parallel_suites": True, "max_parallel_suites": 5}
        test_runner.set_global_config(config)
        assert test_runner.global_config["parallel_suites"] is True
        assert test_runner.global_config["max_parallel_suites"] == 5

    @pytest.mark.asyncio
    async def test_run_empty_runner(self, test_runner):
        results = await test_runner.run_all_suites()
        assert results == {}

    @pytest.mark.asyncio
    async def test_run_runner_with_suites(self, test_runner, runner_sample_suite):
        test_runner.add_test_suite(runner_sample_suite)
        results = await test_runner.run_all_suites()
        assert "Sample Suite" in results
        assert len(results["Sample Suite"]) > 0

    @pytest.mark.unit
    def test_get_global_summary_empty_runner(self, test_runner):
        summary = test_runner.get_global_summary()
        assert summary["total_suites"] == 0
        assert summary["total_tests"] == 0
        assert summary["overall_success_rate"] == 0.0


class TestTestExecutor:
    """Tests for TestExecutor."""

    @pytest.mark.unit
    def test_executor_initialization(self, test_executor):
        assert len(test_executor.execution_history) == 0

    @pytest.mark.asyncio
    async def test_execute_test_success(self, test_executor, sample_test):
        result = await test_executor.execute_test(sample_test, timeout=60.0)
        assert result.test_name == "Executor Test"
        assert result.status in [TestStatus.PASSED, TestStatus.FAILED]
        assert len(test_executor.execution_history) == 1

    @pytest.mark.asyncio
    async def test_execute_test_timeout(self, test_executor, sample_test):
        async def slow_run(*args, **kwargs):
            await asyncio.sleep(2)

        with patch.object(sample_test, "run", new=slow_run):
            result = await test_executor.execute_test(sample_test, timeout=0.1)
        assert result.status == TestStatus.TIMEOUT
        assert "timed out" in result.error_message

    @pytest.mark.unit
    def test_get_execution_history(self, test_executor):
        history = test_executor.get_execution_history()
        assert isinstance(history, list)
        assert len(history) == 0

    @pytest.mark.unit
    def test_clear_history(self, test_executor):
        test_executor.execution_history = [Mock(), Mock()]
        assert len(test_executor.execution_history) == 2
        test_executor.clear_history()
        assert len(test_executor.execution_history) == 0


class TestTestOrchestrator:
    """Tests for TestOrchestrator."""

    @pytest.mark.unit
    def test_orchestrator_initialization(self, test_orchestrator):
        assert test_orchestrator.runner is not None
        assert test_orchestrator.executor is not None
        assert test_orchestrator.config["auto_retry_failed"] is True

    @pytest.mark.asyncio
    async def test_run_test_suite(self, test_orchestrator, orchestrator_sample_suite):
        summary = await test_orchestrator.run_test_suite(orchestrator_sample_suite)
        assert "overall_success_rate" in summary
        assert summary["total_suites"] >= 0
        assert summary["total_tests"] >= 0

    @pytest.mark.asyncio
    async def test_run_multiple_suites(self, test_orchestrator, orchestrator_sample_suite):
        suite2 = IntegrationTestSuite("Suite 2", "Second suite")
        suite2.add_test(ServiceIntegrationTest("Service Test", TestPriority.NORMAL))
        suites = [orchestrator_sample_suite, suite2]
        summary = await test_orchestrator.run_multiple_suites(suites)
        assert "overall_success_rate" in summary
        assert summary["total_suites"] >= 0
        assert summary["total_tests"] >= 0


class TestTestingFrameworkCLI:
    """Tests for TestingFrameworkCLI."""

    @pytest.mark.unit
    def test_cli_initialization(self, cli):
        assert cli.parser is not None
        assert cli.orchestrator is not None

    @pytest.mark.unit
    def test_parser_creation(self, cli):
        parser = cli._create_parser()
        assert parser is not None

    @pytest.mark.unit
    def test_demo_suite_creation(self, cli):
        suite = cli._create_demo_suite_internal("Test Demo Suite")
        assert suite.name == "Test Demo Suite"
        assert len(suite.tests) == 3
        assert suite.description == "Demo test suite: Test Demo Suite"

    @pytest.mark.unit
    def test_suite_by_name_creation(self, cli):
        comm_suite = cli._create_suite_by_name("communication")
        assert comm_suite is not None
        assert comm_suite.name == "Communication Tests"
        assert len(comm_suite.tests) == 3

        service_suite = cli._create_suite_by_name("service")
        assert service_suite is not None
        assert service_suite.name == "Service Tests"
        assert len(service_suite.tests) == 3

        db_suite = cli._create_suite_by_name("database")
        assert db_suite is not None
        assert db_suite.name == "Database Tests"
        assert len(db_suite.tests) == 3

        comp_suite = cli._create_suite_by_name("comprehensive")
        assert comp_suite is not None
        assert comp_suite.name == "Comprehensive Tests"
        assert len(comp_suite.tests) == 3

    @pytest.mark.unit
    def test_unknown_suite_creation(self, cli):
        unknown_suite = cli._create_suite_by_name("unknown")
        assert unknown_suite is None


class TestIntegrationScenarios:
    """Integration tests for complete testing workflows."""

    @pytest.mark.integration
    def test_complete_testing_workflow_tdd(self):
        suite = IntegrationTestSuite("Integration Suite", "Integration test suite")
        suite.add_test(CrossSystemCommunicationTest("Integration Test", TestPriority.HIGH))
        assert suite.name == "Integration Suite"
        assert len(suite.tests) == 1
        assert suite.tests[0].test_name == "Integration Test"
        assert suite.tests[0].priority == TestPriority.HIGH

    @pytest.mark.integration
    def test_test_suite_management_tdd(self):
        runner = IntegrationTestRunner()
        suite1 = IntegrationTestSuite("Suite 1", "First suite")
        suite2 = IntegrationTestSuite("Suite 2", "Second suite")
        runner.add_test_suite(suite1)
        runner.add_test_suite(suite2)
        assert len(runner.test_suites) == 2
        assert runner.test_suites[0].name == "Suite 1"
        assert runner.test_suites[1].name == "Suite 2"
        runner.remove_test_suite("Suite 1")
        assert len(runner.test_suites) == 1
        assert runner.test_suites[0].name == "Suite 2"

    @pytest.mark.integration
    def test_cli_integration_workflow_tdd(self):
        cli = TestingFrameworkCLI()
        suite = cli._create_demo_suite_internal("CLI Test Suite")
        assert suite.name == "CLI Test Suite"
        assert len(suite.tests) == 3
        assert suite.description == "Demo test suite: CLI Test Suite"
