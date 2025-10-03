"""
Integration Workflow Optimizer Models - V2 Compliant
==================================================

Data models and enums for integration workflow optimization.
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions, KISS principle
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class IntegrationPattern(Enum):
    """Integration pattern enumeration."""

    SERVICE_TO_SERVICE = "service_to_service"
    DATA_PIPELINE = "data_pipeline"
    EVENT_DRIVEN = "event_driven"
    API_GATEWAY = "api_gateway"
    MESSAGE_QUEUE = "message_queue"


class AutomationLevel(Enum):
    """Automation level enumeration."""

    MANUAL = "manual"
    SEMI_AUTOMATED = "semi_automated"
    FULL = "full"
    SCHEDULED = "scheduled"


class ConnectionStatus(Enum):
    """Connection status enumeration."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


@dataclass
class IntegrationWorkflow:
    """Integration workflow configuration."""

    workflow_id: str
    pattern: IntegrationPattern
    source_service: str
    target_service: str
    connection_type: str
    automation_level: str
    status: str = "active"


@dataclass
class SeamlessConnection:
    """Seamless connection configuration."""

    connection_id: str
    source: str
    destination: str
    protocol: str
    authentication: str
    retry_policy: str
    timeout: int = 30


@dataclass
class AutomationTool:
    """Automation tool configuration."""

    tool_id: str
    tool_name: str
    tool_type: str
    configuration: dict[str, Any]
    status: str = "active"


@dataclass
class WorkflowMetrics:
    """Workflow performance metrics."""

    workflow_id: str
    execution_time: float
    success_rate: float
    error_count: int
    last_execution: str


@dataclass
class IntegrationReport:
    """Integration analysis report."""

    report_id: str
    total_workflows: int
    active_connections: int
    automation_coverage: float
    performance_score: float
    recommendations: list[str]
