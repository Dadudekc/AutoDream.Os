from typing import Dict, List, Any, Optional

from .v2_comprehensive_messaging_system import V2Message, V2MessageType, V2MessagePriority, V2MessageStatus
from dataclasses import dataclass


# Use consolidated messaging system instead of duplicate enums


@dataclass
class RoutingRule:
    """Rule describing how a message type should be delivered."""

    rule_id: str
    message_type: V2MessageType
    priority: V2MessagePriority
    routing_strategy: str
    target_agents: List[str]
    fallback_strategy: str = "round_robin"
    max_retries: int = 3
    timeout_seconds: int = 30
    enabled: bool = True


@dataclass
class RoutingResult:
    """Result of a routing operation."""

    success: bool
    routed_to: List[str]
    routing_strategy: str
    timestamp: str
    error_message: Optional[str] = None
    retry_count: int = 0


@dataclass
class AgentRoutingInfo:
    """Information about an agent's routing capabilities."""

    agent_id: str
    supported_message_types: List[V2MessageType]
    max_priority: V2MessagePriority
    current_load: int
    is_available: bool
    last_heartbeat: str
    routing_preferences: Dict[str, Any]
