"""
Communication System Compatibility Layer

This module provides backward compatibility for the old communication system
while using the new V2 Comprehensive Messaging System under the hood.

Purpose: Enable gradual migration without breaking existing code.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import logging
import threading
import time
from datetime import datetime

from .v2_comprehensive_messaging_system import (
    V2ComprehensiveMessagingSystem,
    V2Message, V2MessageType, V2MessagePriority, V2MessageStatus,
    V2AgentStatus, V2AgentCapability, V2TaskStatus, V2WorkflowStatus
)

logger = logging.getLogger(__name__)


# ============================================================================
# COMPATIBILITY ENUMS - Maintain old interface names
# ============================================================================

class MessageType(Enum):
    """Compatibility: Old MessageType enum mapped to V2MessageType"""
    # Map old values to V2 values
    COORDINATION = V2MessageType.COORDINATION
    TASK_ASSIGNMENT = V2MessageType.TASK_ASSIGNMENT
    STATUS_UPDATE = V2MessageType.STATUS_UPDATE
    BROADCAST = V2MessageType.BROADCAST
    SYSTEM = V2MessageType.SYSTEM
    ERROR = V2MessageType.ERROR
    ALERT = V2MessageType.ALERT
    INFO = V2MessageType.NOTIFICATION
    SUCCESS = V2MessageType.RESPONSE
    TASK = V2MessageType.TASK
    RESPONSE = V2MessageType.RESPONSE
    NOTIFICATION = V2MessageType.NOTIFICATION
    COMMAND = V2MessageType.COMMAND
    HEARTBEAT = V2MessageType.HEARTBEAT
    SYSTEM_COMMAND = V2MessageType.SYSTEM_COMMAND


class MessagePriority(Enum):
    """Compatibility: Old MessagePriority enum mapped to V2MessagePriority"""
    LOW = V2MessagePriority.LOW
    NORMAL = V2MessagePriority.NORMAL
    HIGH = V2MessagePriority.HIGH
    URGENT = V2MessagePriority.URGENT
    CRITICAL = V2MessagePriority.CRITICAL


class MessageStatus(Enum):
    """Compatibility: Old MessageStatus enum mapped to V2MessageStatus"""
    PENDING = V2MessageStatus.PENDING
    PROCESSING = V2MessageStatus.PROCESSING
    DELIVERED = V2MessageStatus.DELIVERED
    ACKNOWLEDGED = V2MessageStatus.ACKNOWLEDGED
    COMPLETED = V2MessageStatus.COMPLETED
    FAILED = V2MessageStatus.FAILED
    EXPIRED = V2MessageStatus.EXPIRED
    CANCELLED = V2MessageStatus.CANCELLED
    READ = V2MessageStatus.READ


class AgentStatus(Enum):
    """Compatibility: Old AgentStatus enum mapped to V2AgentStatus"""
    OFFLINE = V2AgentStatus.OFFLINE
    ONLINE = V2AgentStatus.ONLINE
    BUSY = V2AgentStatus.BUSY
    IDLE = V2AgentStatus.IDLE
    ERROR = V2AgentStatus.ERROR
    RECOVERING = V2AgentStatus.RECOVERING
    MAINTENANCE = V2AgentStatus.MAINTENANCE
    ONBOARDING = V2AgentStatus.ONBOARDING
    TRAINING = V2AgentStatus.TRAINING


class AgentCapability(Enum):
    """Compatibility: Old AgentCapability enum mapped to V2AgentCapability"""
    TASK_EXECUTION = V2AgentCapability.TASK_EXECUTION
    MONITORING = V2AgentCapability.MONITORING
    COMMUNICATION = V2AgentCapability.COMMUNICATION
    REPORTING = V2AgentCapability.REPORTING
    INTEGRATION = V2AgentCapability.INTEGRATION
    DECISION_MAKING = V2AgentCapability.DECISION_MAKING
    DATA_PROCESSING = V2AgentCapability.DATA_PROCESSING


# ============================================================================
# COMPATIBILITY DATACLASSES - Maintain old interface names
# ============================================================================

@dataclass
class Message:
    """Compatibility: Old Message class mapped to V2Message"""
    message_type: MessageType
    sender_id: str
    recipient_id: str
    content: str
    priority: MessagePriority = MessagePriority.NORMAL
    status: MessageStatus = MessageStatus.PENDING
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}
    
    def to_v2_message(self) -> V2Message:
        """Convert to V2Message for internal use"""
        return V2Message(
            message_type=V2MessageType(self.message_type.value),
            sender_id=self.sender_id,
            recipient_id=self.recipient_id,
            subject=f"Message from {self.sender_id}",
            content=self.content,
            priority=V2MessagePriority(self.priority.value),
            status=V2MessageStatus(self.status.value),
            timestamp=self.timestamp,
            metadata=self.metadata
        )


@dataclass
class AgentInfo:
    """Compatibility: Old AgentInfo class mapped to V2AgentStatus"""
    agent_id: str
    status: AgentStatus
    capabilities: List[AgentCapability]
    last_seen: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.last_seen is None:
            self.last_seen = datetime.now()
        if self.metadata is None:
            self.metadata = {}


# ============================================================================
# COMPATIBILITY CLASSES - Maintain old interface names
# ============================================================================

class AgentCommunicationProtocol:
    """Compatibility: Old AgentCommunicationProtocol using V2 system"""
    
    def __init__(self):
        """Initialize the compatibility protocol"""
        self.v2_system = V2ComprehensiveMessagingSystem()
        self.active = False
        self._lock = threading.Lock()
        
    def initialize(self) -> bool:
        """Initialize the communication protocol"""
        try:
            with self._lock:
                if not self.active:
                    self.v2_system.initialize()
                    self.active = True
                    logger.info("AgentCommunicationProtocol compatibility layer initialized")
                return True
        except Exception as e:
            logger.error(f"Failed to initialize compatibility protocol: {e}")
            return False
    
    def send_message(self, from_agent: str, to_agent: str, message: str,
                    message_type: MessageType = MessageType.COORDINATION,
                    priority: MessagePriority = MessagePriority.NORMAL) -> bool:
        """Send a message using V2 system"""
        try:
            if not self.active:
                self.initialize()
            
            v2_message = V2Message(
                message_type=V2MessageType(message_type.value),
                sender_id=from_agent,
                recipient_id=to_agent,
                subject=f"Message from {from_agent}",
                content=message,
                priority=V2MessagePriority(priority.value)
            )
            
            return self.v2_system.send_message(v2_message)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def broadcast_message(self, from_agent: str, message: str,
                        message_type: MessageType = MessageType.BROADCAST,
                        priority: MessagePriority = MessagePriority.NORMAL) -> bool:
        """Broadcast a message using V2 system"""
        try:
            if not self.active:
                self.initialize()
            
            v2_message = V2Message(
                message_type=V2MessageType(message_type.value),
                sender_id=from_agent,
                recipient_id="broadcast",
                subject=f"Broadcast from {from_agent}",
                content=message,
                priority=V2MessagePriority(priority.value)
            )
            
            return self.v2_system.broadcast_message(v2_message)
        except Exception as e:
            logger.error(f"Failed to broadcast message: {e}")
            return False
    
    def get_agent_status(self, agent_id: str) -> Optional[AgentStatus]:
        """Get agent status using V2 system"""
        try:
            if not self.active:
                self.initialize()
            
            agent_info = self.v2_system.agent_registry.get_agent(agent_id)
            if agent_info:
                return AgentStatus(agent_info.status.value)
            return None
        except Exception as e:
            logger.error(f"Failed to get agent status: {e}")
            return None
    
    def shutdown(self):
        """Shutdown the compatibility protocol"""
        try:
            with self._lock:
                if self.active:
                    self.v2_system.shutdown()
                    self.active = False
                    logger.info("AgentCommunicationProtocol compatibility layer shutdown")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


class InboxManager:
    """Compatibility: Old InboxManager using V2 system"""
    
    def __init__(self):
        """Initialize the compatibility inbox manager"""
        self.v2_system = V2ComprehensiveMessagingSystem()
        self.active = False
        self._lock = threading.Lock()
        
    def initialize(self) -> bool:
        """Initialize the inbox manager"""
        try:
            with self._lock:
                if not self.active:
                    self.v2_system.initialize()
                    self.active = True
                    logger.info("InboxManager compatibility layer initialized")
                return True
        except Exception as e:
            logger.error(f"Failed to initialize inbox manager: {e}")
            return False
    
    def get_messages(self, agent_id: str, status: Optional[MessageStatus] = None) -> List[Message]:
        """Get messages for an agent using V2 system"""
        try:
            if not self.active:
                self.initialize()
            
            v2_messages = self.v2_system.get_messages_for_agent(agent_id)
            
            # Convert V2 messages to compatibility format
            messages = []
            for v2_msg in v2_messages:
                if status is None or v2_msg.status.value == status.value:
                    msg = Message(
                        message_type=MessageType(v2_msg.message_type.value),
                        sender_id=v2_msg.sender_id,
                        recipient_id=v2_msg.recipient_id,
                        content=v2_msg.content,
                        priority=MessagePriority(v2_msg.priority.value),
                        status=MessageStatus(v2_msg.status.value),
                        timestamp=v2_msg.timestamp,
                        metadata=v2_msg.metadata
                    )
                    messages.append(msg)
            
            return messages
        except Exception as e:
            logger.error(f"Failed to get messages: {e}")
            return []
    
    def mark_message_read(self, message_id: str) -> bool:
        """Mark a message as read using V2 system"""
        try:
            if not self.active:
                self.initialize()
            
            # Note: V2 system doesn't have individual message IDs in the same way
            # This is a compatibility limitation
            logger.warning("mark_message_read not fully implemented in V2 compatibility layer")
            return True
        except Exception as e:
            logger.error(f"Failed to mark message read: {e}")
            return False
    
    def shutdown(self):
        """Shutdown the inbox manager"""
        try:
            with self._lock:
                if self.active:
                    self.v2_system.shutdown()
                    self.active = False
                    logger.info("InboxManager compatibility layer shutdown")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


# ============================================================================
# COMPATIBILITY FUNCTIONS - Maintain old interface names
# ============================================================================

def create_message(message_type: MessageType, sender_id: str, recipient_id: str,
                  content: str, priority: MessagePriority = MessagePriority.NORMAL) -> Message:
    """Compatibility: Create a message using old interface"""
    return Message(
        message_type=message_type,
        sender_id=sender_id,
        recipient_id=recipient_id,
        content=content,
        priority=priority
    )


def create_agent_info(agent_id: str, status: AgentStatus,
                     capabilities: List[AgentCapability]) -> AgentInfo:
    """Compatibility: Create agent info using old interface"""
    return AgentInfo(
        agent_id=agent_id,
        status=status,
        capabilities=capabilities
    )
