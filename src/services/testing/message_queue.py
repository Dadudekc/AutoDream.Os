"""
Message Queue System
===================

Unified messaging system for V2 services.
Consolidates message queuing functionality from V1-V2 system.
Target: ≤300 LOC for V2 standards compliance.
"""

import os
import sys
import json
import time
import logging
import threading
import queue
import hashlib
from typing import Dict, List, Any, Optional, Callable, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class MessageStatus(Enum):
    """Message status values."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class MessageType(Enum):
    """Message type values."""
    TEXT = "text"
    COMMAND = "command"
    STATUS = "status"
    DATA = "data"
    NOTIFICATION = "notification"
    ERROR = "error"


@dataclass
class Message:
    """Message data structure."""
    message_id: str
    sender_agent: str
    target_agent: str
    content: str
    priority: MessagePriority
    message_type: MessageType
    timestamp: float = field(default_factory=time.time)
    status: MessageStatus = MessageStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class AgentInfo:
    """Agent information structure."""
    agent_id: str
    name: str
    status: str = "unknown"
    capabilities: List[str] = field(default_factory=list)
    window_title: str = "Unknown"
    coordinates: Dict[str, int] = field(default_factory=dict)
    last_seen: float = field(default_factory=time.time)


class PriorityManager:
    """Manages message priority handling."""
    def __init__(self):
        self.priority_weights = {MessagePriority.LOW: 1, MessagePriority.NORMAL: 2, MessagePriority.HIGH: 3, MessagePriority.CRITICAL: 4}
    def get_priority_weight(self, priority: MessagePriority) -> int:
        return self.priority_weights.get(priority, 1)
    def is_high_priority(self, priority: MessagePriority) -> bool:
        return priority in [MessagePriority.HIGH, MessagePriority.CRITICAL]


class MessageHandler:
    """Handles message processing and routing."""
    
    def __init__(self):
        self.processors: Dict[MessageType, Callable] = {}
        self._setup_default_processors()
    
    def _setup_default_processors(self):
        """Setup default message processors."""
        self.processors[MessageType.TEXT] = self._process_text_message
        self.processors[MessageType.COMMAND] = self._process_command_message
        self.processors[MessageType.STATUS] = self._process_status_message
        self.processors[MessageType.DATA] = self._process_data_message
        self.processors[MessageType.NOTIFICATION] = self._process_notification_message
        self.processors[MessageType.ERROR] = self._process_error_message
    
    def process_message(self, message: Message) -> bool:
        """Process a message based on its type."""
        try:
            processor = self.processors.get(message.message_type)
            if processor:
                return processor(message)
            else:
                logger.warning(f"No processor for message type: {message.message_type}")
                return False
        except Exception as e:
            logger.error(f"Error processing message {message.message_id}: {e}")
            return False
    
    def _process_text_message(self, message: Message) -> bool:
        """Process text message."""
        logger.info(f"Processing text message: {message.content[:50]}...")
        return True
    
    def _process_command_message(self, message: Message) -> bool:
        """Process command message."""
        logger.info(f"Processing command: {message.content}")
        return True
    
    def _process_status_message(self, message: Message) -> bool:
        """Process status message."""
        logger.info(f"Processing status update: {message.content}")
        return True
    
    def _process_data_message(self, message: Message) -> bool:
        """Process data message."""
        logger.info(f"Processing data message: {len(message.content)} bytes")
        return True
    
    def _process_notification_message(self, message: Message) -> bool:
        """Process notification message."""
        logger.info(f"Processing notification: {message.content}")
        return True
    
    def _process_error_message(self, message: Message) -> bool:
        """Process error message."""
        logger.error(f"Processing error: {message.content}")
        return True


class AgentRegistry:
    """Manages agent registration and information."""
    
    def __init__(self):
        self.agents: Dict[str, AgentInfo] = {}
        self._lock = threading.Lock()
    
    def register_agent(self, agent_info: AgentInfo) -> bool:
        """Register a new agent."""
        try:
            with self._lock:
                self.agents[agent_info.agent_id] = agent_info
                logger.info(f"Registered agent: {agent_info.name} ({agent_info.agent_id})")
                return True
        except Exception as e:
            logger.error(f"Failed to register agent: {e}")
            return False
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        try:
            with self._lock:
                if agent_id in self.agents:
                    agent_name = self.agents[agent_id].name
                    del self.agents[agent_id]
                    logger.info(f"Unregistered agent: {agent_name} ({agent_id})")
                    return True
                return False
        except Exception as e:
            logger.error(f"Failed to unregister agent: {e}")
            return False
    
    def get_agent(self, agent_id: str) -> Optional[AgentInfo]:
        """Get agent information."""
        with self._lock:
            return self.agents.get(agent_id)
    
    def get_all_agents(self) -> List[AgentInfo]:
        """Get all registered agents."""
        with self._lock:
            return list(self.agents.values())
    
    def update_agent_status(self, agent_id: str, status: str) -> bool:
        """Update agent status."""
        try:
            with self._lock:
                if agent_id in self.agents:
                    self.agents[agent_id].status = status
                    self.agents[agent_id].last_seen = time.time()
                    return True
                return False
        except Exception as e:
            logger.error(f"Failed to update agent status: {e}")
            return False


class UnifiedMessageQueue:
    """Unified message queue system."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        self.is_running = False
        self.message_queue = queue.Queue()
        self.high_priority_queue = queue.PriorityQueue()
        self.agent_registry = AgentRegistry()
        self.message_handler = MessageHandler()
        self.priority_manager = PriorityManager()
        self.message_history: List[Message] = []
        self.processing_thread = None
        self._lock = threading.Lock()
        
        logger.info("🚀 Unified Message Queue System initialized")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration."""
        return {
            "max_queue_size": 1000,
            "high_priority_timeout": 5.0,
            "message_retry_attempts": 3,
            "retry_delay": 2.0,
            "enable_persistence": True,
            "persistence_file": "message_history.json"
        }
    
    def start_system(self) -> bool:
        """Start the message queue system."""
        try:
            with self._lock:
                if self.is_running:
                    logger.warning("System already running")
                    return True
                
                self.is_running = True
                self.processing_thread = threading.Thread(target=self._process_messages)
                self.processing_thread.daemon = True
                self.processing_thread.start()
                
                logger.info("✅ Message queue system started")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to start system: {e}")
            return False
    
    def stop_system(self) -> bool:
        """Stop the message queue system."""
        try:
            with self._lock:
                if not self.is_running:
                    return True
                
                self.is_running = False
                if self.processing_thread:
                    self.processing_thread.join(timeout=5.0)
                
                logger.info("🛑 Message queue system stopped")
                return True
        except Exception as e:
            logger.error(f"❌ Failed to stop system: {e}")
            return False
    
    def send_message(self, sender_agent: str, target_agent: str, content: str,
                    priority: MessagePriority = MessagePriority.NORMAL,
                    message_type: MessageType = MessageType.TEXT,
                    metadata: Optional[Dict[str, Any]] = None) -> str:
        """Send a message."""
        try:
            message = Message(
                message_id=self._generate_message_id(),
                sender_agent=sender_agent,
                target_agent=target_agent,
                content=content,
                priority=priority,
                message_type=message_type,
                metadata=metadata or {}
            )
            
            if self.priority_manager.is_high_priority(priority):
                weight = self.priority_manager.get_priority_weight(priority)
                self.high_priority_queue.put((weight, message))
            else:
                self.message_queue.put(message)
            
            self.message_history.append(message)
            logger.info(f"📤 Message sent: {message.message_id}")
            return message.message_id
            
        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return ""
    
    def _generate_message_id(self) -> str:
        timestamp = str(int(time.time() * 1000))
        random_part = str(hash(str(threading.current_thread().ident))[-6:]
        return f"msg_{timestamp}_{random_part}"
    
    def _process_messages(self):
        """Process messages in background thread."""
        while self.is_running:
            try:
                # Process high priority messages first
                try:
                    while not self.high_priority_queue.empty():
                        _, message = self.high_priority_queue.get_nowait()
                        self._process_single_message(message)
                except queue.Empty:
                    pass
                
                # Process normal priority messages
                try:
                    message = self.message_queue.get(timeout=1.0)
                    self._process_single_message(message)
                except queue.Empty:
                    continue
                    
            except Exception as e:
                logger.error(f"Error in message processing: {e}")
                time.sleep(0.1)
    
    def _process_single_message(self, message: Message):
        try:
            message.status = MessageStatus.PROCESSING
            success = self.message_handler.process_message(message)
            if success:
                message.status = MessageStatus.COMPLETED
                logger.info(f"✅ Message processed: {message.message_id}")
            else:
                message.status = MessageStatus.FAILED
                logger.error(f"❌ Message failed: {message.message_id}")
        except Exception as e:
            message.status = MessageStatus.ERROR
            logger.error(f"❌ Message error: {message.message_id} - {e}")
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status."""
        return {
            "normal_queue_size": self.message_queue.qsize(),
            "high_priority_queue_size": self.high_priority_queue.qsize(),
            "total_messages": len(self.message_history),
            "system_running": self.is_running
        }
