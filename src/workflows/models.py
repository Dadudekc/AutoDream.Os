"""
Workflow Models - V2 Compliant
==============================

Core data models for the Advanced Workflows System.
Defines workflow states, steps, responses, and progress tracking.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive type hints.

Author: Agent-1 - Workflow Orchestration Specialist
License: MIT
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class WorkflowState(Enum):
    """Workflow execution states following V2 cycle-based tracking."""

    INITIALIZED = "initialized"
    RUNNING = "running"
    WAITING_FOR_AI = "waiting_for_ai"
    PROCESSING_RESPONSE = "processing_response"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class ResponseType(Enum):
    """Expected response types for workflow steps."""

    CONVERSATION_PROMPT = "conversation_prompt"
    CONVERSATION_RESPONSE = "conversation_response"
    TASK_EXECUTION = "task_execution"
    DECISION_ANALYSIS = "decision_analysis"
    GOAL_ASSESSMENT = "goal_assessment"
    ACTION_EXECUTION = "action_execution"
    BRANCH_EXECUTION = "branch_execution"


class CoordinationStrategy(Enum):
    """Coordination strategies for multi-agent workflows."""

    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    DECISION_TREE = "decision_tree"
    AUTONOMOUS = "autonomous"


@dataclass
class WorkflowStep:
    """
    Individual step in a workflow.

    Represents a single unit of work that can be executed by an agent.
    Includes dependency management, completion criteria, and retry logic.
    """

    id: str
    name: str
    description: str
    agent_target: str
    prompt_template: str
    expected_response_type: ResponseType
    timeout_seconds: int = 300
    retry_count: int = 0
    max_retries: int = 3
    dependencies: list[str] = field(default_factory=list)
    completion_criteria: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def is_ready(self, completed_steps: set[str]) -> bool:
        """Check if step dependencies are satisfied."""
        return all(dep in completed_steps for dep in self.dependencies)

    def can_retry(self) -> bool:
        """Check if step can be retried."""
        return self.retry_count < self.max_retries

    def increment_retry(self) -> None:
        """Increment retry count."""
        self.retry_count += 1

    def to_dict(self) -> dict[str, Any]:
        """Convert step to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "agent_target": self.agent_target,
            "prompt_template": self.prompt_template,
            "expected_response_type": self.expected_response_type.value,
            "timeout_seconds": self.timeout_seconds,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "dependencies": self.dependencies,
            "completion_criteria": self.completion_criteria,
            "metadata": self.metadata,
        }


@dataclass
class AIResponse:
    """
    Captured AI response from agent communication system.

    Represents a response received from an agent during workflow execution.
    Includes metadata for analysis and workflow progression.
    """

    agent: str
    text: str
    timestamp: float
    message_id: str
    role: str = "assistant"
    metadata: dict[str, Any] = field(default_factory=dict)
    confidence: float | None = None
    response_type: ResponseType | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AIResponse":
        """Create AIResponse from dictionary."""
        return cls(
            agent=data.get("agent", ""),
            text=data.get("text", ""),
            timestamp=data.get("timestamp", time.time()),
            message_id=data.get("message_id", ""),
            role=data.get("role", "assistant"),
            metadata=data.get("metadata", {}),
            confidence=data.get("confidence"),
            response_type=(
                ResponseType(data.get("response_type")) if data.get("response_type") else None
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert response to dictionary for serialization."""
        return {
            "agent": self.agent,
            "text": self.text,
            "timestamp": self.timestamp,
            "message_id": self.message_id,
            "role": self.role,
            "metadata": self.metadata,
            "confidence": self.confidence,
            "response_type": self.response_type.value if self.response_type else None,
        }


@dataclass
class WorkflowProgress:
    """
    Workflow execution progress tracking.

    Provides comprehensive status information about workflow execution
    following V2's cycle-based tracking requirements.
    """

    workflow_name: str
    state: WorkflowState
    total_steps: int
    completed_steps: int
    failed_steps: int
    current_step: str | None = None
    start_time: float = field(default_factory=time.time)
    last_update_time: float = field(default_factory=time.time)
    cycles_completed: int = 0
    workflow_data: dict[str, Any] = field(default_factory=dict)

    @property
    def pending_steps(self) -> int:
        """Calculate number of pending steps."""
        return self.total_steps - self.completed_steps - self.failed_steps

    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.total_steps == 0:
            return 0.0
        return (self.completed_steps / self.total_steps) * 100

    @property
    def execution_time(self) -> float:
        """Calculate total execution time."""
        return time.time() - self.start_time

    @property
    def cycles_per_minute(self) -> float:
        """Calculate cycles per minute (V2 metric)."""
        if self.execution_time == 0:
            return 0.0
        return (self.cycles_completed * 60) / self.execution_time

    def increment_cycle(self) -> None:
        """Increment cycle count (V2 cycle-based tracking)."""
        self.cycles_completed += 1
        self.last_update_time = time.time()

    def update_step(self, step_id: str, status: str) -> None:
        """Update step status."""
        if status == "completed":
            self.completed_steps += 1
        elif status == "failed":
            self.failed_steps += 1

        self.current_step = step_id
        self.last_update_time = time.time()

    def to_dict(self) -> dict[str, Any]:
        """Convert progress to dictionary for serialization."""
        return {
            "workflow_name": self.workflow_name,
            "state": self.state.value,
            "total_steps": self.total_steps,
            "completed_steps": self.completed_steps,
            "failed_steps": self.failed_steps,
            "pending_steps": self.pending_steps,
            "current_step": self.current_step,
            "start_time": self.start_time,
            "last_update_time": self.last_update_time,
            "cycles_completed": self.cycles_completed,
            "completion_percentage": self.completion_percentage,
            "execution_time": self.execution_time,
            "cycles_per_minute": self.cycles_per_minute,
            "workflow_data": self.workflow_data,
        }


@dataclass
class WorkflowConfiguration:
    """
    Workflow configuration settings.

    Centralizes configuration management for workflow execution
    following V2's unified configuration approach.
    """

    max_iterations: int = 10
    default_timeout: int = 300
    retry_count: int = 3
    response_check_interval: float = 1.0
    state_persistence: bool = True
    devlog_enabled: bool = True
    cycle_based_tracking: bool = True

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> "WorkflowConfiguration":
        """Create configuration from config dictionary."""
        return cls(
            max_iterations=config.get("max_iterations", 10),
            default_timeout=config.get("default_timeout", 300),
            retry_count=config.get("retry_count", 3),
            response_check_interval=config.get("response_check_interval", 1.0),
            state_persistence=config.get("state_persistence", True),
            devlog_enabled=config.get("devlog", {}).get("enabled", True),
            cycle_based_tracking=config.get("v2_compliance", {}).get("cycle_based_tracking", True),
        )
