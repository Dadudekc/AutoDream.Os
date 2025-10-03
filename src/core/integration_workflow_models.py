"""
Integration Workflow Models - V2 Compliant
==========================================

Data models for integration workflow optimization.
V2 Compliance: ≤400 lines, ≤5 classes, simple data structures
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class IntegrationPattern(Enum):
    """Integration pattern enumeration."""
    
    SERVICE_TO_SERVICE = "service_to_service"
    DATA_PIPELINE = "data_pipeline"
    EVENT_DRIVEN = "event_driven"
    API_GATEWAY = "api_gateway"
    MESSAGE_QUEUE = "message_queue"


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
    encryption: bool = True
    timeout: int = 30


@dataclass
class OptimizationResult:
    """Optimization result data."""
    
    workflow_id: str
    optimization_type: str
    performance_gain: float
    resource_savings: float
    implementation_time: float
    success: bool = True


@dataclass
class IntegrationMetrics:
    """Integration performance metrics."""
    
    connection_count: int
    average_latency: float
    success_rate: float
    error_rate: float
    throughput: float
