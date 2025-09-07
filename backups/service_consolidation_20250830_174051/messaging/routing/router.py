"""
Message Router - Extracted from v2_comprehensive_messaging_system.py

This module handles message routing logic including:
- Message routing based on type and priority
- Agent coordination and load balancing
- Workflow routing and task assignment

Original file: src/core/v2_comprehensive_messaging_system.py
Extraction date: 2024-12-19
"""

import logging
import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
from abc import ABC, abstractmethod

# Configure logging
logger = logging.getLogger(__name__)

# Import enums and data structures from consolidated modules
from ..types.v2_message_enums import V2MessageType, V2MessagePriority, V2MessageStatus
from ..models.v2_message import V2Message

# Define missing enums and classes for compatibility

class V2AgentStatus(Enum):
    """Agent status values"""
    OFFLINE = "offline"
    ONLINE = "online"
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"

class V2TaskStatus(Enum):
    """Task status values"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class V2WorkflowStatus(Enum):
    """Workflow status values"""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

class V2AgentCapability(Enum):
    """Agent capability values"""
    TASK_EXECUTION = "task_execution"
    DECISION_MAKING = "decision_making"
    COMMUNICATION = "communication"

@dataclass
class V2AgentInfo:
    """Agent information for routing"""
    agent_id: str
    status: V2AgentStatus
    capabilities: Set[V2AgentCapability] = field(default_factory=set)

@dataclass
class V2TaskInfo:
    """Task information for routing"""
    task_id: str
    status: V2TaskStatus

@dataclass
class V2WorkflowInfo:
    """Workflow information for routing"""
    workflow_id: str
    status: V2WorkflowStatus


class V2MessageRouter:
    """Message routing implementation - SRP: Route messages to appropriate agents"""
    
    def __init__(self):
        self.routing_rules: Dict[V2MessageType, List[str]] = defaultdict(list)
        self.agent_capabilities: Dict[str, Set[V2AgentCapability]] = defaultdict(set)
        self.workflow_routes: Dict[str, List[str]] = defaultdict(list)
        self.task_routes: Dict[str, List[str]] = defaultdict(list)
        self.lock = threading.RLock()
        
    def add_routing_rule(self, message_type: V2MessageType, agent_ids: List[str]) -> None:
        """Add routing rule for message type"""
        with self.lock:
            self.routing_rules[message_type].extend(agent_ids)
            
    def set_agent_capabilities(self, agent_id: str, capabilities: Set[V2AgentCapability]) -> None:
        """Set agent capabilities for routing decisions"""
        with self.lock:
            self.agent_capabilities[agent_id] = capabilities.copy()
            
    def add_workflow_route(self, workflow_id: str, agent_ids: List[str]) -> None:
        """Add workflow routing configuration"""
        with self.lock:
            self.workflow_routes[workflow_id] = agent_ids.copy()
            
    def add_task_route(self, task_id: str, agent_ids: List[str]) -> None:
        """Add task routing configuration"""
        with self.lock:
            self.task_routes[task_id] = agent_ids.copy()
            
    def route_message(self, message: V2Message, available_agents: List[V2AgentInfo]) -> Optional[str]:
        """Route message to appropriate agent based on type and priority"""
        try:
            with self.lock:
                # Check for specific routing rules
                if message.message_type in self.routing_rules:
                    for agent_id in self.routing_rules[message.message_type]:
                        if any(agent.agent_id == agent_id for agent in available_agents):
                            return agent_id
                
                # Check for workflow-specific routing
                if message.workflow_id and message.workflow_id in self.workflow_routes:
                    for agent_id in self.workflow_routes[message.workflow_id]:
                        if any(agent.agent_id == agent_id for agent in available_agents):
                            return agent_id
                
                # Check for task-specific routing
                if message.task_id and message.task_id in self.task_routes:
                    for agent_id in self.task_routes[message.task_id]:
                        if any(agent.agent_id == agent_id for agent in available_agents):
                            return agent_id
                
                # Default routing based on message type and agent capabilities
                return self._route_by_capabilities(message, available_agents)
                
        except Exception as e:
            logger.error(f"Failed to route message {message.message_id}: {e}")
            return None
            
    def _route_by_capabilities(self, message: V2Message, available_agents: List[V2AgentInfo]) -> Optional[str]:
        """Route message based on agent capabilities and availability"""
        try:
            # Filter agents by status (only online and idle agents)
            available_agents = [
                agent for agent in available_agents 
                if agent.status in [V2AgentStatus.ONLINE, V2AgentStatus.IDLE]
            ]
            
            if not available_agents:
                return None
                
            # Score agents based on capabilities and current load
            agent_scores = []
            for agent in available_agents:
                score = 0
                
                # Base score for capability match
                if message.message_type == V2MessageType.TASK_ASSIGNMENT:
                    if V2AgentCapability.TASK_EXECUTION in self.agent_capabilities[agent.agent_id]:
                        score += 10
                elif message.message_type == V2MessageType.DECISION_MAKING:
                    if V2AgentCapability.DECISION_MAKING in self.agent_capabilities[agent.agent_id]:
                        score += 10
                elif message.message_type == V2MessageType.COORDINATION:
                    if V2AgentCapability.COMMUNICATION in self.agent_capabilities[agent.agent_id]:
                        score += 10
                        
                # Bonus for idle agents
                if agent.status == V2AgentStatus.IDLE:
                    score += 5
                    
                # Bonus for agents with matching workflow experience
                if message.workflow_id and message.workflow_id in agent.workflow_history:
                    score += 3
                    
                agent_scores.append((agent.agent_id, score))
                
            # Return agent with highest score
            if agent_scores:
                agent_scores.sort(key=lambda x: x[1], reverse=True)
                return agent_scores[0][0]
                
            return None
            
        except Exception as e:
            logger.error(f"Failed to route by capabilities: {e}")
            return None
            
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing statistics for monitoring"""
        with self.lock:
            return {
                "routing_rules_count": len(self.routing_rules),
                "agent_capabilities_count": len(self.agent_capabilities),
                "workflow_routes_count": len(self.workflow_routes),
                "task_routes_count": len(self.task_routes)
            }
