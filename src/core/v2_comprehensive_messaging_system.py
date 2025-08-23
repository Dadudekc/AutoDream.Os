#!/usr/bin/env python3
"""
V2 Comprehensive Messaging System - Agent Cellphone V2
======================================================

Clean, production-grade messaging system following V2 standards:
- OOP design with proper abstractions
- Single Responsibility Principle (SRP)
- Clean, maintainable code
- ≤300 LOC per class

Author: V2 Clean Architecture Specialist
License: MIT
"""

import json
import logging
import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set, Callable, Union, Generic, TypeVar
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
from abc import ABC, abstractmethod
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

# Generic type for message content
T = TypeVar('T')


# ============================================================================
# CORE ENUMS - Single Responsibility: Define message types and states
# ============================================================================

class V2MessageType(Enum):
    """Message types for V2 system"""
    TASK_ASSIGNMENT = "task_assignment"
    STATUS_UPDATE = "status_update"
    COORDINATION = "coordination"
    BROADCAST = "broadcast"
    ONBOARDING_PHASE = "onboarding_phase"
    SYSTEM = "system"
    ALERT = "alert"
    WORKFLOW_UPDATE = "workflow_update"
    # Additional types for comprehensive coverage
    TASK = "task"
    RESPONSE = "response"
    VALIDATION = "validation"
    FEEDBACK = "feedback"
    TEXT = "text"
    NOTIFICATION = "notification"
    COMMAND = "command"
    ERROR = "error"
    CONTRACT_ASSIGNMENT = "contract_assignment"
    EMERGENCY = "emergency"
    HEARTBEAT = "heartbeat"
    SYSTEM_COMMAND = "system_command"
    ONBOARDING_START = "onboarding_start"
    ONBOARDING_COMPLETE = "onboarding_complete"
    TASK_CREATED = "task_created"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    AGENT_REGISTRATION = "agent_registration"
    AGENT_STATUS = "agent_status"
    AGENT_HEALTH = "agent_health"
    AGENT_CAPABILITY_UPDATE = "agent_capability_update"
    WORKFLOW_STATUS = "workflow_status"
    WORKFLOW_COMMAND = "workflow_command"
    WORKFLOW_RESPONSE = "workflow_response"
    METRICS_UPDATE = "metrics_update"
    PERFORMANCE_ALERT = "performance_alert"
    SYSTEM_HEALTH = "system_health"
    CAPACITY_ALERT = "capacity_alert"
    TASK_COORDINATION = "task_coordination"
    TASK_DEPENDENCY = "task_dependency"
    TASK_RESOURCE = "task_resource"
    TASK_SCHEDULE = "task_schedule"
    AGENT_COORDINATION = "agent_coordination"
    AGENT_SYNC = "agent_sync"
    AGENT_LOAD_BALANCE = "agent_load_balance"
    AGENT_FAILOVER = "agent_failover"
    SYSTEM_MAINTENANCE = "system_maintenance"
    SYSTEM_UPDATE = "system_update"
    SYSTEM_ROLLBACK = "system_rollback"
    SYSTEM_BACKUP = "system_backup"
    DATA_SYNC = "data_sync"
    DATA_BACKUP = "data_backup"
    DATA_RESTORE = "data_restore"
    DATA_MIGRATION = "data_migration"
    SECURITY_ALERT = "security_alert"
    COMPLIANCE_CHECK = "compliance_check"
    ACCESS_REQUEST = "access_request"
    AUDIT_LOG = "audit_log"
    # Additional types expected by smoke tests
    PERFORMANCE_METRIC = "performance_metric"
    HEALTH_CHECK = "health_check"
    DIRECT = "direct"


class V2MessagePriority(Enum):
    """Message priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


class V2MessageStatus(Enum):
    """Message status states"""
    PENDING = "pending"
    PROCESSING = "processing"
    DELIVERED = "delivered"
    ACKNOWLEDGED = "acknowledged"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    READ = "read"


class V2AgentStatus(Enum):
    """Agent status states"""
    OFFLINE = "offline"
    ONLINE = "online"
    BUSY = "busy"
    IDLE = "idle"
    ERROR = "error"
    RECOVERING = "recovering"
    MAINTENANCE = "maintenance"
    ONBOARDING = "onboarding"
    TRAINING = "training"


class V2TaskStatus(Enum):
    """Task status states"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


class V2WorkflowStatus(Enum):
    """Workflow status states"""
    CREATED = "created"
    PLANNING = "planning"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RECOVERING = "recovering"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    ACTIVE = "active"
    WAITING_FOR_AI = "waiting_for_ai"
    PROCESSING_RESPONSE = "processing_response"
    OPTIMIZING = "optimizing"
    SCALING = "scaling"
    IN_PROGRESS = "in_progress"


class V2WorkflowType(Enum):
    """Workflow types"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    PARALLEL_BATCH = "parallel_batch"
    PIPELINE = "pipeline"


class V2AgentCapability(Enum):
    """Agent capabilities"""
    TASK_EXECUTION = "task_execution"
    DECISION_MAKING = "decision_making"
    COMMUNICATION = "communication"
    DATA_PROCESSING = "data_processing"
    MONITORING = "monitoring"
    REPORTING = "reporting"
    # Additional capabilities for swarm agents
    TESTING = "testing"
    AI_ML = "ai_ml"
    CONTENT_PROCESSING = "content_processing"
    MULTIMEDIA = "multimedia"
    SECURITY = "security"
    INFRASTRUCTURE = "infrastructure"
    BUSINESS_INTELLIGENCE = "business_intelligence"
    TRADING = "trading"
    GAME_DEVELOPMENT = "game_development"
    ENTERTAINMENT = "entertainment"
    WEB_DEVELOPMENT = "web_development"
    UI_FRAMEWORK = "ui_framework"
    INTEGRATION = "integration"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"


# ============================================================================
# DATA STRUCTURES - Single Responsibility: Define message and agent data
# ============================================================================

@dataclass
class V2Message:
    """V2 message structure - clean and focused"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: V2MessageType = V2MessageType.COORDINATION
    priority: V2MessagePriority = V2MessagePriority.NORMAL
    status: V2MessageStatus = V2MessageStatus.PENDING
    sender_id: str = ""
    recipient_id: str = ""
    subject: str = ""
    content: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    delivered_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    ttl: Optional[int] = None
    sequence_number: Optional[int] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    requires_acknowledgment: bool = False
    is_onboarding_message: bool = False
    phase_number: Optional[int] = None
    workflow_id: Optional[str] = None
    task_id: Optional[str] = None
    
    def __post_init__(self):
        """Ensure required fields are set"""
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.now()
        if not self.created_at:
            self.created_at = self.timestamp
        if self.payload is None:
            self.payload = {}
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "status": self.status.value,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "subject": self.subject,
            "content": self.content,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "created_at": self.created_at.isoformat(),
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "ttl": self.ttl,
            "sequence_number": self.sequence_number,
            "dependencies": self.dependencies,
            "tags": self.tags,
            "requires_acknowledgment": self.requires_acknowledgment,
            "is_onboarding_message": self.is_onboarding_message,
            "phase_number": self.phase_number,
            "workflow_id": self.workflow_id,
            "task_id": self.task_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'V2Message':
        """Create message from dictionary"""
        # Convert timestamp strings back to datetime objects
        timestamp_fields = ['timestamp', 'created_at', 'delivered_at', 'acknowledged_at', 'read_at']
        for field in timestamp_fields:
            if field in data and isinstance(data[field], str):
                data[field] = datetime.fromisoformat(data[field])
        
        # Convert enum values back to enum objects
        if 'message_type' in data and isinstance(data['message_type'], str):
            data['message_type'] = V2MessageType(data['message_type'])
        if 'priority' in data and isinstance(data['priority'], (str, int)):
            if isinstance(data['priority'], str):
                data['priority'] = V2MessagePriority[data['priority'].upper()]
            else:
                data['priority'] = V2MessagePriority(data['priority'])
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = V2MessageStatus(data['status'])
        
        return cls(**data)
    
    def is_expired(self) -> bool:
        """Check if message has expired based on TTL"""
        if self.ttl is None:
            return False
        return datetime.now() > self.created_at + timedelta(seconds=self.ttl)
    
    def can_retry(self) -> bool:
        """Check if message can be retried"""
        return self.retry_count < self.max_retries and not self.is_expired()
    
    def mark_delivered(self):
        """Mark message as delivered"""
        self.status = V2MessageStatus.DELIVERED
        self.delivered_at = datetime.now()
    
    def mark_acknowledged(self):
        """Mark message as acknowledged"""
        self.status = V2MessageStatus.ACKNOWLEDGED
        self.acknowledged_at = datetime.now()
    
    def mark_read(self):
        """Mark message as read"""
        self.status = V2MessageStatus.READ
        self.read_at = datetime.now()
    
    def increment_retry(self):
        """Increment retry count"""
        self.retry_count += 1
        if self.retry_count >= self.max_retries:
            self.status = V2MessageStatus.FAILED


@dataclass
class V2AgentInfo:
    """V2 agent information - clean and focused"""
    agent_id: str
    name: str
    capabilities: List[V2AgentCapability]
    status: V2AgentStatus
    last_seen: datetime
    endpoint: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Additional fields for comprehensive coverage
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    current_tasks: List[str] = field(default_factory=list)
    workflow_participation: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Ensure collections are initialized"""
        if self.performance_metrics is None:
            self.performance_metrics = {}
        if self.current_tasks is None:
            self.current_tasks = []
        if self.workflow_participation is None:
            self.workflow_participation = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "capabilities": [cap.value for cap in self.capabilities],
            "status": self.status.value,
            "last_seen": self.last_seen.isoformat(),
            "endpoint": self.endpoint,
            "metadata": self.metadata,
            "performance_metrics": self.performance_metrics,
            "current_tasks": self.current_tasks,
            "workflow_participation": self.workflow_participation
        }


# ============================================================================
# ABSTRACT INTERFACES - Single Responsibility: Define contracts
# ============================================================================

class IMessageStorage(ABC):
    """Interface for message storage - SRP: Store and retrieve messages"""
    
    @abstractmethod
    def store_message(self, message: V2Message) -> bool:
        """Store a message"""
        pass
    
    @abstractmethod
    def get_messages_for_agent(self, agent_id: str, 
                              message_type: Optional[V2MessageType] = None,
                              status: Optional[V2MessageStatus] = None) -> List[V2Message]:
        """Get messages for an agent with optional filtering"""
        pass
    
    @abstractmethod
    def update_message_status(self, message_id: str, status: V2MessageStatus) -> bool:
        """Update message status"""
        pass


class IAgentRegistry(ABC):
    """Interface for agent management - SRP: Manage agent registration"""
    
    @abstractmethod
    def register_agent(self, agent_info: V2AgentInfo) -> bool:
        """Register an agent"""
        pass
    
    @abstractmethod
    def get_agent(self, agent_id: str) -> Optional[V2AgentInfo]:
        """Get agent information"""
        pass
    
    @abstractmethod
    def update_agent_status(self, agent_id: str, status: V2AgentStatus) -> bool:
        """Update agent status"""
        pass


class IMessageQueue(ABC):
    """Interface for message queuing - SRP: Manage message flow"""
    
    @abstractmethod
    def enqueue_message(self, message: V2Message) -> bool:
        """Add message to queue"""
        pass
    
    @abstractmethod
    def dequeue_message(self) -> Optional[V2Message]:
        """Remove and return next message"""
        pass
    
    @abstractmethod
    def get_queue_size(self) -> int:
        """Get current queue size"""
        pass


# ============================================================================
# CONCRETE IMPLEMENTATIONS - Single Responsibility: Implement interfaces
# ============================================================================

class V2MessageStorage(IMessageStorage):
    """Message storage implementation - SRP: Store and retrieve messages"""
    
    def __init__(self):
        self.messages: Dict[str, V2Message] = {}
        self.lock = threading.RLock()
    
    def store_message(self, message: V2Message) -> bool:
        """Store a message"""
        try:
            with self.lock:
                self.messages[message.message_id] = message
                return True
        except Exception as e:
            logger.error(f"Failed to store message: {e}")
            return False
    
    def get_messages_for_agent(self, agent_id: str, 
                              message_type: Optional[V2MessageType] = None,
                              status: Optional[V2MessageStatus] = None) -> List[V2Message]:
        """Get messages for an agent with optional filtering"""
        try:
            messages = []
            for message in self.messages.values():
                # Check if message is for this agent or is a broadcast
                if (message.recipient_id == agent_id or 
                    message.recipient_id == "broadcast"):
                    
                    # Apply filters if specified
                    if message_type and message.message_type != message_type:
                        continue
                    if status and message.status != status:
                        continue
                    
                    messages.append(message)
            
            # Sort by priority (highest first) then by timestamp (oldest first)
            messages.sort(key=lambda m: (m.priority.value, m.timestamp), reverse=True)
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get messages for agent {agent_id}: {e}")
            return []
    
    def update_message_status(self, message_id: str, status: V2MessageStatus) -> bool:
        """Update message status"""
        try:
            with self.lock:
                if message_id in self.messages:
                    self.messages[message_id].status = status
                    return True
                return False
        except Exception as e:
            logger.error(f"Failed to update message status: {e}")
            return False


class V2AgentRegistry(IAgentRegistry):
    """Agent registry implementation - SRP: Manage agent registration"""
    
    def __init__(self):
        self.agents: Dict[str, V2AgentInfo] = {}
        self.lock = threading.RLock()
    
    def register_agent(self, agent_info: V2AgentInfo) -> bool:
        """Register an agent"""
        try:
            with self.lock:
                self.agents[agent_info.agent_id] = agent_info
                logger.info(f"Agent {agent_info.agent_id} registered successfully")
                return True
        except Exception as e:
            logger.error(f"Failed to register agent: {e}")
            return False
    
    def get_agent(self, agent_id: str) -> Optional[V2AgentInfo]:
        """Get agent information"""
        try:
            with self.lock:
                return self.agents.get(agent_id)
        except Exception as e:
            logger.error(f"Failed to get agent {agent_id}: {e}")
            return None
    
    def update_agent_status(self, agent_id: str, status: V2AgentStatus) -> bool:
        """Update agent status"""
        try:
            with self.lock:
                if agent_id in self.agents:
                    self.agents[agent_id].status = status
                    self.agents[agent_id].last_seen = datetime.now()
                    return True
                return False
        except Exception as e:
            logger.error(f"Failed to update agent status: {e}")
            return False


class V2MessageQueue(IMessageQueue):
    """Message queue implementation - SRP: Manage message flow"""
    
    def __init__(self):
        self.queue: deque = deque()
        self.lock = threading.RLock()
        self.metrics = {
            'enqueue_count': 0,
            'dequeue_count': 0,
            'current_size': 0
        }
    
    def enqueue_message(self, message: V2Message) -> bool:
        """Add message to queue"""
        try:
            with self.lock:
                self.queue.append(message)
                self.metrics['enqueue_count'] += 1
                self.metrics['current_size'] = len(self.queue)
                return True
        except Exception as e:
            logger.error(f"Failed to enqueue message: {e}")
            return False
    
    def dequeue_message(self) -> Optional[V2Message]:
        """Remove and return next message"""
        try:
            with self.lock:
                if self.queue:
                    message = self.queue.popleft()
                    self.metrics['dequeue_count'] += 1
                    self.metrics['current_size'] = len(self.queue)
                    return message
                return None
        except Exception as e:
            logger.error(f"Failed to dequeue message: {e}")
            return None
    
    def get_queue_size(self) -> int:
        """Get current queue size"""
        try:
            with self.lock:
                return len(self.queue)
        except Exception as e:
            logger.error(f"Failed to get queue size: {e}")
            return 0
    
    def __len__(self) -> int:
        """Support len() operation for compatibility with existing tests"""
        return self.get_queue_size()


# ============================================================================
# MAIN MESSAGING SYSTEM - Single Responsibility: Orchestrate components
# ============================================================================

class V2ComprehensiveMessagingSystem:
    """
    V2 Comprehensive Messaging System
    
    Single responsibility: Orchestrate messaging components
    Follows V2 standards: OOP, SRP, clean production-grade code
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the messaging system with clean architecture"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize components (dependency injection)
        self.message_storage = V2MessageStorage()
        self.agent_registry = V2AgentRegistry()
        self.message_queue = V2MessageQueue()
        
        # System state
        self.active = False
        self.lock = threading.RLock()
        
        # Callbacks for compatibility with existing tests
        self.message_callbacks: List[Callable] = []
        self.agent_status_callbacks: List[Callable] = []
        
        # Initialize system
        self._initialize_system()
    
    @property
    def communication_active(self) -> bool:
        """Alias for active attribute - compatibility with existing tests"""
        return self.active
    
    @property
    def queue_metrics(self) -> Dict[str, Any]:
        """Alias for queue metrics - compatibility with existing tests"""
        return self.message_queue.metrics.copy()
    
    @property
    def messages(self) -> Dict[str, V2Message]:
        """Access to all messages - compatibility with existing tests"""
        return self.message_storage.messages.copy()
    
    @property
    def registered_agents(self) -> Dict[str, V2AgentInfo]:
        """Access to registered agents - compatibility with existing tests"""
        return self.agent_registry.agents.copy()
    
    @property
    def agent_capabilities(self) -> Dict[str, Set[str]]:
        """Access to agent capabilities index - compatibility with existing tests"""
        capabilities_index = defaultdict(set)
        for agent_id, agent_info in self.registered_agents.items():
            for capability in agent_info.capabilities:
                capabilities_index[capability.value].add(agent_id)
        return dict(capabilities_index)
    
    def _initialize_system(self):
        """Initialize the system"""
        try:
            self.logger.info("Initializing V2 Comprehensive Messaging System...")
            self.active = True
            self.logger.info("✅ V2 Comprehensive Messaging System initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize messaging system: {e}")
            self.active = False
    
    def send_message(self, 
                    sender_id: str,
                    recipient_id: str,
                    message_type: V2MessageType,
                    subject: str = "",
                    content: str = "",
                    payload: Dict[str, Any] = None,
                    priority: V2MessagePriority = V2MessagePriority.NORMAL,
                    requires_acknowledgment: bool = False,
                    **kwargs) -> Optional[str]:
        """Send a message through the system"""
        try:
            if not self.active:
                self.logger.error("Messaging system not active")
                return None
            
            # Create message
            message = V2Message(
                message_type=message_type,
                priority=priority,
                sender_id=sender_id,
                recipient_id=recipient_id,
                subject=subject,
                content=content,
                payload=payload or {},
                requires_acknowledgment=requires_acknowledgment,
                **kwargs
            )
            
            # Store and queue message
            if (self.message_storage.store_message(message) and 
                self.message_queue.enqueue_message(message)):
                
                self.logger.info(f"Message sent: {message.message_id} from {sender_id} to {recipient_id}")
                return message.message_id
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return None
    
    def get_messages_for_agent(self, agent_id: str, 
                              message_type: Optional[V2MessageType] = None,
                              status: Optional[V2MessageStatus] = None) -> List[V2Message]:
        """Get messages for an agent with optional filtering"""
        return self.message_storage.get_messages_for_agent(agent_id, message_type, status)
    
    def acknowledge_message(self, message_id: str, agent_id: str) -> bool:
        """Acknowledge a message"""
        try:
            # Get message from storage
            messages = self.message_storage.get_messages_for_agent(agent_id)
            message = next((m for m in messages if m.message_id == message_id), None)
            
            if message and message.requires_acknowledgment:
                message.mark_acknowledged()
                return self.message_storage.update_message_status(message_id, V2MessageStatus.ACKNOWLEDGED)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to acknowledge message {message_id}: {e}")
            return False
    
    def register_agent(self, agent_id: str, name: str, capabilities: List[V2AgentCapability],
                      endpoint: str, metadata: Dict[str, Any] = None) -> bool:
        """Register a new agent"""
        try:
            agent_info = V2AgentInfo(
                agent_id=agent_id,
                name=name,
                capabilities=capabilities,
                status=V2AgentStatus.ONLINE,
                last_seen=datetime.now(),
                endpoint=endpoint,
                metadata=metadata or {}
            )
            
            return self.agent_registry.register_agent(agent_info)
            
        except Exception as e:
            self.logger.error(f"Failed to register agent {agent_id}: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status information"""
        try:
            # Get all messages from storage
            all_messages = list(self.message_storage.messages.values())
            
            # Count messages by type and priority
            message_types = {}
            priority_counts = {}
            agent_message_counts = defaultdict(int)
            
            for message in all_messages:
                # Count by message type
                msg_type = message.message_type.value
                message_types[msg_type] = message_types.get(msg_type, 0) + 1
                
                # Count by priority
                priority = message.priority.value
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
                
                # Count by sender
                if message.sender_id:
                    agent_message_counts[message.sender_id] += 1
            
            # Get agent statuses
            agent_statuses = {}
            for agent_id, agent_info in self.agent_registry.agents.items():
                agent_statuses[agent_id] = agent_info.status.value
            
            return {
                "system_active": self.active,
                "total_messages": len(all_messages),
                "queued_messages": self.message_queue.get_queue_size(),
                "registered_agents": len(self.agent_registry.agents),
                "agent_message_counts": dict(agent_message_counts),
                "message_types": message_types,
                "priority_counts": priority_counts,
                "queue_metrics": self.message_queue.metrics.copy(),
                "agent_statuses": agent_statuses
            }
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {"error": str(e)}
    
    def shutdown(self):
        """Shutdown the messaging system"""
        try:
            self.logger.info("Shutting down V2 Comprehensive Messaging System...")
            self.active = False
            self.logger.info("✅ V2 Comprehensive Messaging System shutdown complete")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")


# ============================================================================
# CONVENIENCE FUNCTIONS - Single Responsibility: Create common messages
# ============================================================================

def create_onboarding_message(agent_id: str, phase: int, content: str) -> V2Message:
    """Create an onboarding message"""
    return V2Message(
        message_type=V2MessageType.ONBOARDING_PHASE,
        sender_id="SYSTEM",
        recipient_id=agent_id,
        subject=f"V2 Onboarding Phase {phase}",
        content=content,
        priority=V2MessagePriority.CRITICAL,
        requires_acknowledgment=True,
        is_onboarding_message=True,
        phase_number=phase
    )


def create_coordination_message(sender_id: str, recipient_id: str, content: str,
                              priority: V2MessagePriority = V2MessagePriority.NORMAL) -> V2Message:
    """Create a coordination message"""
    return V2Message(
        message_type=V2MessageType.COORDINATION,
        sender_id=sender_id,
        recipient_id=recipient_id,
        subject="Coordination Message",
        content=content,
        priority=priority
    )


def create_broadcast_message(sender_id: str, content: str,
                           priority: V2MessagePriority = V2MessagePriority.NORMAL) -> V2Message:
    """Create a broadcast message"""
    return V2Message(
        message_type=V2MessageType.BROADCAST,
        sender_id=sender_id,
        recipient_id="broadcast",
        subject="Broadcast Message",
        content=content,
        priority=priority
    )


def create_task_message(sender_id: str, recipient_id: str, task_id: str,
                       content: str, priority: V2MessagePriority = V2MessagePriority.NORMAL) -> V2Message:
    """Create a task message"""
    return V2Message(
        message_type=V2MessageType.TASK_ASSIGNMENT,
        sender_id=sender_id,
        recipient_id=recipient_id,
        subject=f"Task Assignment: {task_id}",
        content=content,
        priority=priority,
        task_id=task_id
    )


def create_workflow_message(sender_id: str, recipient_id: str, workflow_id: str,
                           content: str, priority: V2MessagePriority = V2MessagePriority.NORMAL) -> V2Message:
    """Create a workflow message"""
    return V2Message(
        message_type=V2MessageType.COORDINATION,
        sender_id=sender_id,
        recipient_id=recipient_id,
        subject=f"Workflow Update: {workflow_id}",
        content=content,
        priority=priority,
        workflow_id=workflow_id
    )
