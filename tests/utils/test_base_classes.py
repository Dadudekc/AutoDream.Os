#!/usr/bin/env python3
"""
Test Base Classes - Common Test Patterns
========================================

Base classes and common test patterns for the test suite.
Provides reusable test structures and common functionality.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import threading
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest

from .test_fixtures import MockFactory, TestDataFactory


class BaseTestClass(ABC):
    """Base class for all test classes."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_start_time = time.time()
        self._setup_test_data()
        self._setup_mocks()

    def teardown_method(self):
        """Clean up after test."""
        self._cleanup_test_data()
        self._cleanup_mocks()

    @abstractmethod
    def _setup_test_data(self):
        """Set up test-specific data."""
        pass

    def _setup_mocks(self):
        """Set up common mocks."""
        self.mock_pyautogui = MockFactory.create_pyautogui_mock()
        self.mock_pyperclip = MockFactory.create_pyperclip_mock()
        self.mock_discord = MockFactory.create_discord_mock()

    def _cleanup_test_data(self):
        """Clean up test-specific data."""
        pass

    def _cleanup_mocks(self):
        """Clean up mocks."""
        pass

    def assert_performance(self, operation: Callable, max_duration: float, iterations: int = 1):
        """Assert operation performance."""
        start_time = time.time()
        for _ in range(iterations):
            operation()
        duration = time.time() - start_time
        assert duration < max_duration, f"Operation took {duration}s, expected < {max_duration}s"

    def assert_thread_safety(self, operation: Callable, thread_count: int = 10):
        """Assert operation thread safety."""
        results = []

        def thread_operation():
            try:
                result = operation()
                results.append(result)
            except Exception as e:
                results.append(e)

        threads = []
        for _ in range(thread_count):
            thread = threading.Thread(target=thread_operation)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Check that all operations completed without exceptions
        exceptions = [r for r in results if isinstance(r, Exception)]
        assert len(exceptions) == 0, f"Thread safety test failed with exceptions: {exceptions}"


class MessagingServiceTestBase(BaseTestClass):
    """Base class for messaging service tests."""

    def _setup_test_data(self):
        """Set up messaging service test data."""
        self.coordinates_data = TestDataFactory.create_coordinates_data()
        self.test_agents = list(self.coordinates_data["agents"].keys())
        self.expected_coordinates = {
            agent_id: tuple(data["chat_input_coordinates"])
            for agent_id, data in self.coordinates_data["agents"].items()
        }

    def assert_message_sent_successfully(self, result: bool, agent_id: str):
        """Assert message was sent successfully."""
        assert result is True, f"Failed to send message to {agent_id}"

    def assert_message_send_failed(self, result: bool, agent_id: str):
        """Assert message send failed."""
        assert result is False, f"Message send should have failed for {agent_id}"

    def assert_broadcast_results(self, results: dict[str, bool], expected_count: int):
        """Assert broadcast results."""
        assert (
            len(results) == expected_count
        ), f"Expected {expected_count} results, got {len(results)}"
        for agent_id in self.test_agents:
            assert agent_id in results, f"Missing result for {agent_id}"

    def assert_message_formatting(
        self,
        formatted_message: str,
        sender: str,
        recipient: str,
        content: str,
        priority: str = "NORMAL",
    ):
        """Assert message formatting is correct."""
        assert f"FROM: {sender}" in formatted_message
        assert f"TO: {recipient}" in formatted_message
        assert f"Priority: {priority}" in formatted_message
        assert content in formatted_message
        assert "[A2A] MESSAGE" in formatted_message
        assert "DISCORD DEVLOG REMINDER" in formatted_message


class DiscordBotTestBase(BaseTestClass):
    """Base class for Discord bot tests."""

    def _setup_test_data(self):
        """Set up Discord bot test data."""
        self.discord_message_data = TestDataFactory.create_discord_message_data()
        self.test_agents = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]

    def assert_discord_bot_initialization(self, bot):
        """Assert Discord bot initialization."""
        assert bot is not None
        assert hasattr(bot, "command_prefix")
        assert hasattr(bot, "intents")

    def assert_slash_command_registration(self, bot, command_name: str):
        """Assert slash command registration."""
        assert hasattr(bot, "tree")
        # Note: Actual command validation would require more complex setup

    def assert_discord_embed_creation(self, embed):
        """Assert Discord embed creation."""
        assert embed is not None
        assert hasattr(embed, "title")
        assert hasattr(embed, "description")
        assert hasattr(embed, "color")

    def assert_interaction_response(self, interaction_mock, expected_content: str):
        """Assert interaction response."""
        interaction_mock.response.send_message.assert_called()
        # Note: Actual content validation would require more complex setup


class DatabaseTestBase(BaseTestClass):
    """Base class for database tests."""

    def _setup_test_data(self):
        """Set up database test data."""
        self.agent_status_data = TestDataFactory.create_agent_status_data()
        self.working_tasks_data = TestDataFactory.create_working_tasks_data()
        self.future_tasks_data = TestDataFactory.create_future_tasks_data()

    def assert_database_connection(self, connection):
        """Assert database connection."""
        assert connection is not None
        assert hasattr(connection, "execute")
        assert hasattr(connection, "commit")
        assert hasattr(connection, "close")

    def assert_table_exists(self, connection, table_name: str):
        """Assert table exists in database."""
        cursor = connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
        )
        result = cursor.fetchone()
        assert result is not None, f"Table {table_name} does not exist"

    def assert_data_insertion(self, connection, table_name: str, expected_count: int):
        """Assert data insertion."""
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        assert count == expected_count, f"Expected {expected_count} rows, got {count}"

    def assert_backup_creation(self, backup_path: str):
        """Assert backup creation."""
        import os

        assert os.path.exists(backup_path), f"Backup file {backup_path} does not exist"
        assert os.path.getsize(backup_path) > 0, f"Backup file {backup_path} is empty"


class IntegrationTestBase(BaseTestClass):
    """Base class for integration tests."""

    def _setup_test_data(self):
        """Set up integration test data."""
        self.coordinates_data = TestDataFactory.create_coordinates_data()
        self.discord_message_data = TestDataFactory.create_discord_message_data()

    def assert_system_integration(self, components: list[Any]):
        """Assert system integration."""
        for component in components:
            assert component is not None, "Component should not be None"
            assert hasattr(component, "__class__"), "Component should have a class"

    def assert_data_flow(self, input_data: Any, output_data: Any, transformation_func: Callable):
        """Assert data flow through transformation."""
        result = transformation_func(input_data)
        assert result == output_data, f"Data transformation failed: {input_data} -> {result}"

    def assert_error_handling(self, operation: Callable, expected_exception: type):
        """Assert error handling."""
        with pytest.raises(expected_exception):
            operation()


class PerformanceTestBase(BaseTestClass):
    """Base class for performance tests."""

    def _setup_test_data(self):
        """Set up performance test data."""
        self.performance_thresholds = {
            "message_formatting": 0.001,  # 1ms per message
            "agent_validation": 0.0001,  # 0.1ms per validation
            "coordinate_loading": 0.01,  # 10ms for loading
            "database_query": 0.1,  # 100ms for query
        }

    def assert_performance_threshold(
        self, operation: Callable, threshold_name: str, iterations: int = 1000
    ):
        """Assert performance meets threshold."""
        threshold = self.performance_thresholds.get(threshold_name, 1.0)
        self.assert_performance(operation, threshold, iterations)

    def measure_operation_time(self, operation: Callable, iterations: int = 1) -> float:
        """Measure operation execution time."""
        start_time = time.time()
        for _ in range(iterations):
            operation()
        return time.time() - start_time

    def assert_memory_usage(self, operation: Callable, max_memory_mb: float):
        """Assert memory usage is within limits."""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        operation()

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        assert (
            memory_increase < max_memory_mb
        ), f"Memory usage increased by {memory_increase:.2f}MB, expected < {max_memory_mb}MB"


class MockTestBase(BaseTestClass):
    """Base class for tests using extensive mocking."""

    def _setup_mocks(self):
        """Set up comprehensive mocks."""
        super()._setup_mocks()
        self.mock_database = MockFactory.create_database_mock()
        self.mock_file_system = MagicMock()
        self.mock_network = MagicMock()

    def patch_external_dependencies(self, *patches):
        """Patch external dependencies."""
        self.patches = []
        for patch_target in patches:
            patch_obj = patch(patch_target)
            self.patches.append(patch_obj)
            patch_obj.start()

    def _cleanup_mocks(self):
        """Clean up patches."""
        if hasattr(self, "patches"):
            for patch_obj in self.patches:
                patch_obj.stop()
        super()._cleanup_mocks()

    def assert_mock_calls(self, mock_obj: Mock, expected_calls: int):
        """Assert mock was called expected number of times."""
        assert (
            mock_obj.call_count == expected_calls
        ), f"Expected {expected_calls} calls, got {mock_obj.call_count}"

    def assert_mock_call_with(self, mock_obj: Mock, *args, **kwargs):
        """Assert mock was called with specific arguments."""
        mock_obj.assert_called_with(*args, **kwargs)


# Test Mixins for specific functionality
class ValidationMixin:
    """Mixin for validation tests."""

    def assert_validation_success(self, validator: Callable, valid_data: Any):
        """Assert validation succeeds."""
        result = validator(valid_data)
        assert result is True, f"Validation should succeed for {valid_data}"

    def assert_validation_failure(self, validator: Callable, invalid_data: Any):
        """Assert validation fails."""
        result = validator(invalid_data)
        assert result is False, f"Validation should fail for {invalid_data}"


class ErrorHandlingMixin:
    """Mixin for error handling tests."""

    def assert_graceful_error_handling(
        self, operation: Callable, error_data: Any, expected_result: Any
    ):
        """Assert graceful error handling."""
        result = operation(error_data)
        assert result == expected_result, f"Expected {expected_result}, got {result}"

    def assert_exception_handling(
        self, operation: Callable, exception_data: Any, expected_exception: type
    ):
        """Assert exception handling."""
        with pytest.raises(expected_exception):
            operation(exception_data)


class DataTransformationMixin:
    """Mixin for data transformation tests."""

    def assert_data_transformation(
        self, transformer: Callable, input_data: Any, expected_output: Any
    ):
        """Assert data transformation."""
        result = transformer(input_data)
        assert result == expected_output, f"Transformation failed: {input_data} -> {result}"

    def assert_batch_transformation(
        self, transformer: Callable, input_batch: list[Any], expected_batch: list[Any]
    ):
        """Assert batch data transformation."""
        results = [transformer(data) for data in input_batch]
        assert results == expected_batch, f"Batch transformation failed: {input_batch} -> {results}"
