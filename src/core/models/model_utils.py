"""Utility enums and shared constants for model classes."""
from __future__ import annotations

from enum import Enum


class ModelType(str, Enum):
    """AI model categories."""

    LLM = "llm"
    EMBEDDING = "embedding"
    VISION = "vision"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"
    CODE = "code"
    REASONING = "reasoning"


class Provider(str, Enum):
    """AI service providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    META = "meta"
    LOCAL = "local"
    CUSTOM = "custom"


class AgentType(str, Enum):
    """Supported AI agent roles."""

    COORDINATOR = "coordinator"
    LEARNER = "learner"
    OPTIMIZER = "optimizer"
    PERFORMANCE_TUNER = "performance_tuner"
    KNOWLEDGE_MANAGER = "knowledge_manager"
    TASK_EXECUTOR = "task_executor"
    WORKFLOW_MANAGER = "workflow_manager"


class WorkflowType(str, Enum):
    """System workflow categories."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"
    OPTIMIZATION = "optimization"
    MAINTENANCE = "maintenance"


class TaskStatus(str, Enum):
    """Task execution states."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class TaskPriority(int, Enum):
    """Task priority levels."""

    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5
