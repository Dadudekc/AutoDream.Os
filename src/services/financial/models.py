from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Any


@dataclass
class AgentRegistration:
    """Agent registration information"""
    agent_id: str
    agent_name: str
    agent_type: str
    required_services: List[str]
    registration_time: datetime
    last_heartbeat: datetime
    status: str  # ACTIVE, INACTIVE, ERROR
    performance_metrics: Dict[str, Any] = None

    def __post_init__(self):
        if self.performance_metrics is None:
            self.performance_metrics = {}


@dataclass
class CrossAgentRequest:
    """Cross-agent service request"""
    request_id: str
    source_agent: str
    target_service: str
    request_type: str
    request_data: Dict[str, Any]
    timestamp: datetime
    priority: str  # HIGH, MEDIUM, LOW
    status: str  # PENDING, PROCESSING, COMPLETED, ERROR

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class CrossAgentResponse:
    """Cross-agent service response"""
    request_id: str
    response_data: Any
    response_time: float
    status: str
    error_message: str = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SystemHealthMetrics:
    """Overall system health metrics"""
    total_agents: int
    active_agents: int
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    system_uptime: float
    last_updated: datetime

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()
