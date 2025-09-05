"""
Messaging Status Models
======================

Data models for messaging status tracking.
V2 Compliance: < 300 lines, single responsibility, data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class StatusType(Enum):
    """Status tracking types."""
    MESSAGE_SENT = "message_sent"
    MESSAGE_DELIVERED = "message_delivered"
    MESSAGE_FAILED = "message_failed"
    SYSTEM_ERROR = "system_error"
    PERFORMANCE_METRIC = "performance_metric"


@dataclass
class StatusEntry:
    """Individual status entry."""
    timestamp: datetime
    status_type: StatusType
    message_id: str
    agent_id: str
    details: Dict[str, Any]
    success: bool


@dataclass
class StatusSummary:
    """Status summary data."""
    total_messages: int
    successful_messages: int
    failed_messages: int
    success_rate: float
    average_response_time: float
    last_updated: datetime


@dataclass
class AgentStatus:
    """Agent-specific status data."""
    agent_id: str
    total_messages: int
    successful_messages: int
    failed_messages: int
    success_rate: float
    last_activity: datetime
    is_online: bool


@dataclass
class PerformanceMetrics:
    """Performance metrics data."""
    average_response_time: float
    max_response_time: float
    min_response_time: float
    total_requests: int
    error_count: int
    error_rate: float


class StatusTrackerModels:
    """Status tracker models and validation."""
    
    @staticmethod
    def create_status_entry(
        status_type: StatusType,
        message_id: str,
        agent_id: str,
        details: Dict[str, Any],
        success: bool
    ) -> StatusEntry:
        """Create a new status entry."""
        return StatusEntry(
            timestamp=datetime.now(),
            status_type=status_type,
            message_id=message_id,
            agent_id=agent_id,
            details=details,
            success=success
        )
    
    @staticmethod
    def create_status_summary(
        total_messages: int,
        successful_messages: int,
        failed_messages: int,
        average_response_time: float
    ) -> StatusSummary:
        """Create status summary."""
        success_rate = (successful_messages / total_messages * 100) if total_messages > 0 else 0.0
        
        return StatusSummary(
            total_messages=total_messages,
            successful_messages=successful_messages,
            failed_messages=failed_messages,
            success_rate=success_rate,
            average_response_time=average_response_time,
            last_updated=datetime.now()
        )
    
    @staticmethod
    def create_agent_status(
        agent_id: str,
        total_messages: int,
        successful_messages: int,
        failed_messages: int,
        last_activity: datetime,
        is_online: bool = True
    ) -> AgentStatus:
        """Create agent status."""
        success_rate = (successful_messages / total_messages * 100) if total_messages > 0 else 0.0
        
        return AgentStatus(
            agent_id=agent_id,
            total_messages=total_messages,
            successful_messages=successful_messages,
            failed_messages=failed_messages,
            success_rate=success_rate,
            last_activity=last_activity,
            is_online=is_online
        )
    
    @staticmethod
    def create_performance_metrics(
        response_times: List[float],
        total_requests: int,
        error_count: int
    ) -> PerformanceMetrics:
        """Create performance metrics."""
        if not response_times:
            return PerformanceMetrics(
                average_response_time=0.0,
                max_response_time=0.0,
                min_response_time=0.0,
                total_requests=total_requests,
                error_count=error_count,
                error_rate=(error_count / total_requests * 100) if total_requests > 0 else 0.0
            )
        
        return PerformanceMetrics(
            average_response_time=sum(response_times) / len(response_times),
            max_response_time=max(response_times),
            min_response_time=min(response_times),
            total_requests=total_requests,
            error_count=error_count,
            error_rate=(error_count / total_requests * 100) if total_requests > 0 else 0.0
        )
