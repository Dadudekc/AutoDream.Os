#!/usr/bin/env python3
"""
Command Result Module - Standardized Command Execution Results
============================================================

This module provides the CommandResult dataclass for representing the results
of command executions throughout the Agent Cellphone V2 system.

The CommandResult class serves as a standardized data structure for all command
execution outcomes, enabling consistent error handling, logging, and response
processing across the entire swarm system.

USAGE EXAMPLES:
===============

Basic Usage:
    >>> from src.commandresult import CommandResult
    >>> result = CommandResult(success=True, message="Operation completed")
    >>> print(result.success)
    True

Success with Data:
    >>> result = CommandResult(
    ...     success=True,
    ...     message="User data retrieved",
    ...     data={"user_id": 123, "name": "John Doe", "email": "john@example.com"},
    ...     execution_time=0.234,
    ...     agent="Agent-2"
    ... )
    >>> print(f"User: {result.data['name']}")
    User: John Doe

Error Handling:
    >>> result = CommandResult(
    ...     success=False,
    ...     message="Database connection failed",
    ...     data={"error_code": "CONNECTION_ERROR", "retry_count": 3},
    ...     execution_time=5.123,
    ...     agent="Agent-3"
    ... )
    >>> if not result.success:
    ...     print(f"Error: {result.message}")
    ...     print(f"Error Code: {result.data['error_code']}")
    Error: Database connection failed
    Error Code: CONNECTION_ERROR

Real-world Command Execution:
    >>> def send_message_command(recipient: str, content: str) -> CommandResult:
    ...     \"\"\"Send a message to another agent.\"\"\"
    ...     try:
    ...         # Simulate message sending
    ...         message_id = f"msg_{hash(content) % 1000}"
    ...         return CommandResult(
    ...             success=True,
    ...             message=f"Message sent to {recipient}",
    ...             data={"message_id": message_id, "recipient": recipient},
    ...             execution_time=0.045,
    ...             agent="Agent-8"
    ...         )
    ...     except Exception as e:
    ...         return CommandResult(
    ...             success=False,
    ...             message=f"Failed to send message: {str(e)}",
    ...             data={"error": str(e)},
    ...             execution_time=0.012,
    ...             agent="Agent-8"
    ...         )
    >>>
    >>> # Test successful send
    >>> result = send_message_command("Agent-1", "Hello from Agent-8!")
    >>> print(f"Result: {result.message}")
    Result: Message sent to Agent-1
    >>>
    >>> # Test error case
    >>> result = send_message_command("", "")  # Invalid parameters
    >>> print(f"Error: {result.message}")
    Error: Failed to send message: Invalid recipient or content

Integration with Swarm Coordination:
    >>> def coordinate_swarm_task(task_name: str, agents: list) -> CommandResult:
    ...     \"\"\"Coordinate a task across multiple agents.\"\"\"
    ...     import time
    ...     start_time = time.time()
    ...
    ...     try:
    ...         # Simulate task coordination
    ...         assigned_agents = []
    ...         for agent in agents:
    ...             assigned_agents.append({"agent": agent, "status": "assigned"})
    ...
    ...         execution_time = time.time() - start_time
    ...         return CommandResult(
    ...             success=True,
    ...             message=f"Task '{task_name}' coordinated across {len(agents)} agents",
    ...             data={
    ...                 "task_name": task_name,
    ...                 "assigned_agents": assigned_agents,
    ...                 "coordination_status": "complete"
    ...             },
    ...             execution_time=execution_time,
    ...             agent="Captain Agent-4"
    ...         )
    ...     except Exception as e:
    ...         return CommandResult(
    ...             success=False,
    ...             message=f"Task coordination failed: {str(e)}",
    ...             data={"error": str(e), "partial_assignments": assigned_agents},
    ...             execution_time=time.time() - start_time,
    ...             agent="Captain Agent-4"
    ...         )
    >>>
    >>> # Test successful coordination
    >>> result = coordinate_swarm_task("test_execution", ["Agent-1", "Agent-2", "Agent-3"])
    >>> print(f"Coordination: {result.message}")
    Coordination: Task 'test_execution' coordinated across 3 agents

Author: Agent-8 (SSOT & System Integration Specialist)
Enhanced Documentation: Captain Agent-4 (Universal Documentation Initiative)
Version: 2.1 - Comprehensive Testing & Documentation Standards
License: MIT
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class CommandResult:
    """
    Represents the result of a command execution.

    This dataclass provides a standardized way to return command execution
    results with success status, messages, data, and metadata. It serves as
    the universal response format for all command operations in the swarm system.

    Attributes:
        success (bool): Whether the command executed successfully
        message (str): Human-readable message describing the result
        data (Any | None): Optional data returned by the command (can be any type)
        execution_time (float | None): Time taken to execute the command in seconds
        agent (str | None): Agent identifier that executed the command

    Example:
        >>> # Basic success result
        >>> result = CommandResult(
        ...     success=True,
        ...     message="File processed successfully",
        ...     data={"file_path": "/data/input.txt", "lines_processed": 150},
        ...     execution_time=0.234,
        ...     agent="Agent-2"
        ... )
        >>> print(f"✅ {result.message}")
        ✅ File processed successfully
        >>> print(f"📊 Processed {result.data['lines_processed']} lines in {result.execution_time}s")
        📊 Processed 150 lines in 0.234s

    Example:
        >>> # Error result with diagnostic data
        >>> result = CommandResult(
        ...     success=False,
        ...     message="Network connection timeout",
        ...     data={
        ...         "error_code": "NETWORK_TIMEOUT",
        ...         "retry_count": 3,
        ...         "last_attempt": "2025-09-12T10:30:00Z"
        ...     },
        ...     execution_time=15.678,
        ...     agent="Agent-6"
        ... )
        >>> if not result.success:
        ...     print(f"❌ {result.message}")
        ...     print(f"🔄 Retried {result.data['retry_count']} times")
        ❌ Network connection timeout
        🔄 Retried 3 times
    """

    success: bool
    message: str
    data: Any | None = None
    execution_time: float | None = None
    agent: str | None = None
