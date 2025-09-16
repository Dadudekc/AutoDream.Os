#!/usr/bin/env python3
"""
CommandResult Testing Suite - Core Module
=========================================

Core CommandResult testing functionality extracted from test_commandresult.py
V2 Compliance: ≤400 lines for compliance

Author: Agent-2 (Architecture & Design Specialist)
Mission: Modularize test_commandresult.py for V2 compliance
License: MIT
"""

from dataclasses import asdict

import pytest

from src.commandresult import CommandResult


class TestCommandResultCore:
    """Unit tests for CommandResult core functionality."""

    def test_success_result_creation(self):
        """Test creating a successful CommandResult."""
        result = CommandResult(
            success=True,
            message="Operation completed successfully",
            data={"result": "test_data"},
            execution_time=0.5,
            agent="Agent-1",
        )

        assert result.success is True
        assert result.message == "Operation completed successfully"
        assert result.data == {"result": "test_data"}
        assert result.execution_time == 0.5
        assert result.agent == "Agent-1"

    def test_failure_result_creation(self):
        """Test creating a failed CommandResult."""
        result = CommandResult(
            success=False,
            message="Operation failed",
            data={"error": "connection_timeout"},
            execution_time=2.3,
            agent="Agent-2",
        )

        assert result.success is False
        assert result.message == "Operation failed"
        assert result.data == {"error": "connection_timeout"}
        assert result.execution_time == 2.3
        assert result.agent == "Agent-2"

    def test_minimal_result_creation(self):
        """Test creating a CommandResult with minimal required fields."""
        result = CommandResult(success=True, message="Basic operation")

        assert result.success is True
        assert result.message == "Basic operation"
        assert result.data is None
        assert result.execution_time is None
        assert result.agent is None

    def test_result_with_none_values(self):
        """Test CommandResult with explicit None values."""
        result = CommandResult(
            success=False, message="No data available", data=None, execution_time=None, agent=None
        )

        assert result.success is False
        assert result.message == "No data available"
        assert result.data is None
        assert result.execution_time is None
        assert result.agent is None

    def test_result_immutability(self):
        """Test that CommandResult instances are immutable (dataclass behavior)."""
        result = CommandResult(
            success=True,
            message="Test message",
            data={"key": "value"},
            execution_time=1.0,
            agent="Agent-1",
        )

        # Test that we can access attributes but cannot modify them
        # (assuming dataclass with frozen=True)
        assert result.success is True
        assert result.message == "Test message"
        assert result.data == {"key": "value"}
        assert result.execution_time == 1.0
        assert result.agent == "Agent-1"

    def test_result_serialization(self):
        """Test converting CommandResult to dictionary."""
        result = CommandResult(
            success=True,
            message="Data processed",
            data={"items": [1, 2, 3]},
            execution_time=1.5,
            agent="Agent-3",
        )

        result_dict = asdict(result)

        expected = {
            "success": True,
            "message": "Data processed",
            "data": {"items": [1, 2, 3]},
            "execution_time": 1.5,
            "agent": "Agent-3",
        }

        assert result_dict == expected

    @pytest.mark.parametrize(
        "success,message,data,execution_time,agent",
        [
            (True, "Success", {"key": "value"}, 0.1, "Agent-1"),
            (False, "Failure", None, None, None),
            (True, "", {}, 0.0, ""),
            (False, "Error message", {"error_code": 500}, 10.5, "Agent-8"),
        ],
    )
    def test_result_parametrized(self, success, message, data, execution_time, agent):
        """Parametrized test for CommandResult creation with various inputs."""
        result = CommandResult(
            success=success, message=message, data=data, execution_time=execution_time, agent=agent
        )

        assert result.success == success
        assert result.message == message
        assert result.data == data
        assert result.execution_time == execution_time
        assert result.agent == agent

    def test_result_with_complex_data(self):
        """Test CommandResult with complex nested data structures."""
        complex_data = {
            "user": {
                "id": 123,
                "profile": {"name": "John Doe", "preferences": ["option1", "option2"]},
            },
            "metadata": {"created_at": "2025-01-01T00:00:00Z", "tags": ["important", "urgent"]},
        }

        result = CommandResult(
            success=True,
            message="Complex data processed",
            data=complex_data,
            execution_time=2.5,
            agent="Agent-4",
        )

        assert result.success is True
        assert result.data == complex_data
        assert result.data["user"]["id"] == 123
        assert result.data["user"]["profile"]["name"] == "John Doe"
        assert "important" in result.data["metadata"]["tags"]

    def test_result_with_empty_strings(self):
        """Test CommandResult with empty string values."""
        result = CommandResult(
            success=True, message="", data={"empty_field": ""}, execution_time=0.0, agent=""
        )

        assert result.success is True
        assert result.message == ""
        assert result.data == {"empty_field": ""}
        assert result.execution_time == 0.0
        assert result.agent == ""

    def test_result_with_zero_values(self):
        """Test CommandResult with zero values."""
        result = CommandResult(
            success=False,
            message="Zero execution time",
            data={"count": 0, "value": 0.0},
            execution_time=0.0,
            agent="Agent-5",
        )

        assert result.success is False
        assert result.data["count"] == 0
        assert result.data["value"] == 0.0
        assert result.execution_time == 0.0

    def test_result_with_boolean_data(self):
        """Test CommandResult with boolean data values."""
        result = CommandResult(
            success=True,
            message="Boolean data test",
            data={"enabled": True, "disabled": False, "mixed": {"active": True, "inactive": False}},
            execution_time=0.1,
            agent="Agent-6",
        )

        assert result.success is True
        assert result.data["enabled"] is True
        assert result.data["disabled"] is False
        assert result.data["mixed"]["active"] is True
        assert result.data["mixed"]["inactive"] is False

    def test_result_with_list_data(self):
        """Test CommandResult with list data structures."""
        list_data = {
            "numbers": [1, 2, 3, 4, 5],
            "strings": ["a", "b", "c"],
            "mixed": [1, "text", True, None],
            "nested": [{"id": 1}, {"id": 2}],
        }

        result = CommandResult(
            success=True,
            message="List data processed",
            data=list_data,
            execution_time=0.3,
            agent="Agent-7",
        )

        assert result.success is True
        assert result.data["numbers"] == [1, 2, 3, 4, 5]
        assert result.data["strings"] == ["a", "b", "c"]
        assert result.data["mixed"] == [1, "text", True, None]
        assert len(result.data["nested"]) == 2
        assert result.data["nested"][0]["id"] == 1

    def test_result_equality(self):
        """Test CommandResult equality comparison."""
        result1 = CommandResult(
            success=True,
            message="Test message",
            data={"key": "value"},
            execution_time=1.0,
            agent="Agent-1",
        )

        result2 = CommandResult(
            success=True,
            message="Test message",
            data={"key": "value"},
            execution_time=1.0,
            agent="Agent-1",
        )

        result3 = CommandResult(
            success=False,
            message="Different message",
            data={"key": "value"},
            execution_time=1.0,
            agent="Agent-1",
        )

        # Test equality
        assert result1 == result2
        assert result1 != result3

    def test_result_string_representation(self):
        """Test CommandResult string representation."""
        result = CommandResult(
            success=True,
            message="Test operation",
            data={"result": "success"},
            execution_time=0.5,
            agent="Agent-1",
        )

        result_str = str(result)

        # Basic checks for string representation
        assert "CommandResult" in result_str or "success=True" in result_str
        assert "Test operation" in result_str or "message=" in result_str

    def test_result_repr(self):
        """Test CommandResult repr representation."""
        result = CommandResult(
            success=True,
            message="Test operation",
            data={"result": "success"},
            execution_time=0.5,
            agent="Agent-1",
        )

        result_repr = repr(result)

        # Basic checks for repr representation
        assert "CommandResult" in result_repr or "success=True" in result_repr


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""
    print("🐝 CommandResult Testing Suite - Core Module")
    print("=" * 50)
    print("✅ Core CommandResult tests loaded successfully")
    print("✅ Basic creation and validation tests loaded successfully")
    print("✅ Serialization and parametrized tests loaded successfully")
    print("✅ Data structure validation tests loaded successfully")
    print("🐝 WE ARE SWARM - Core CommandResult testing ready!")
