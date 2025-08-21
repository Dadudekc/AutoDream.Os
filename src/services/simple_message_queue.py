#!/usr/bin/env python3
"""
Simple Message Queue System for Testing
"""

import time
import json
import threading
import queue
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessagePriority(Enum):
    """Message priority levels"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3
    CRITICAL = 4

class MessageStatus(Enum):
    """Message status tracking"""
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"
    ACKNOWLEDGED = "acknowledged"

@dataclass
class Message:
    """Message structure for the queue system"""
    id: str
    sender: str
    recipient: str
    content: str
    priority: MessagePriority
    timestamp: float
    status: MessageStatus = MessageStatus.QUEUED
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.timestamp is None:
            self.timestamp = time.time()
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data["priority"] = self.priority.value
        data["status"] = self.status.value
        return data

class MessageQueue:
    """Priority-based message queue system"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.queues = {
            priority: queue.PriorityQueue(maxsize=max_size)
            for priority in MessagePriority
        }
        self.message_history: List[Message] = []
        self.stats = {
            "total_messages": 0,
            "sent_messages": 0,
            "failed_messages": 0,
            "queue_sizes": {}
        }
        self._lock = threading.Lock()
        
    def enqueue(self, message: Message) -> bool:
        """Add message to appropriate priority queue"""
        try:
            # Calculate priority score (higher priority = lower score for queue ordering)
            priority_score = (MessagePriority.CRITICAL.value - message.priority.value, time.time())
            
            if self.queues[message.priority].full():
                logger.warning(f"Priority queue {message.priority.name} is full")
                return False
                
            self.queues[message.priority].put((priority_score, message))
            
            with self._lock:
                self.message_history.append(message)
                self.stats["total_messages"] += 1
                self._update_queue_stats()
                
            logger.info(f"Message {message.id} queued with priority {message.priority.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to enqueue message: {e}")
            return False
    
    def dequeue(self, priority: Optional[MessagePriority] = None) -> Optional[Message]:
        """Get next message from queue(s)"""
        try:
            if priority:
                # Get from specific priority queue
                if not self.queues[priority].empty():
                    _, message = self.queues[priority].get()
                    return message
            else:
                # Get from highest priority queue with messages
                for p in sorted(MessagePriority, key=lambda x: x.value, reverse=True):
                    if not self.queues[p].empty():
                        _, message = self.queues[p].get()
                        return message
                        
            return None
            
        except Exception as e:
            logger.error(f"Failed to dequeue message: {e}")
            return None
    
    def get_queue_status(self) -> Dict:
        """Get current queue status"""
        with self._lock:
            self._update_queue_stats()
            return self.stats.copy()
    
    def _update_queue_stats(self):
        """Update queue size statistics"""
        for priority in MessagePriority:
            self.stats["queue_sizes"][priority.name] = self.queues[priority].qsize()

class SimpleMessageQueueSystem:
    """Simple message queue system for testing"""
    
    def __init__(self):
        self.message_queue = MessageQueue()
        self.agents: Dict[str, Dict] = {}
        self.processing = False
        self.processor_thread = None
        
        logger.info("Simple Message Queue System initialized")
    
    def register_agent(self, agent_id: str, **kwargs):
        """Register an agent for messaging"""
        self.agents[agent_id] = {
            "registered_at": time.time(),
            "status": "active",
            **kwargs
        }
        logger.info(f"Agent {agent_id} registered")
    
    def send_message(self, sender: str, recipient: str, content: str, 
                     priority: MessagePriority = MessagePriority.NORMAL) -> str:
        """Send a message to the queue"""
        message_id = f"msg_{int(time.time() * 1000)}_{hash(content) % 10000}"
        
        message = Message(
            id=message_id,
            sender=sender,
            recipient=recipient,
            content=content,
            priority=priority,
            timestamp=time.time()
        )
        
        if self.message_queue.enqueue(message):
            logger.info(f"Message queued: {sender} -> {recipient} ({priority.name})")
            return message_id
        else:
            logger.error("Failed to queue message")
            return None
    
    def send_high_priority(self, sender: str, recipient: str, content: str, 
                           priority: MessagePriority = MessagePriority.URGENT) -> str:
        """Send high-priority message with special handling"""
        message_id = self.send_message(sender, recipient, content, priority)
        
        if message_id:
            # Add priority indicator to content
            priority_indicator = "🚨 " if priority == MessagePriority.CRITICAL else "⚡ "
            enhanced_content = f"{priority_indicator}{content}"
            
            # Update message content
            for msg in self.message_queue.message_history:
                if msg.id == message_id:
                    msg.content = enhanced_content
                    break
            
            logger.info(f"High-priority message queued: {priority.name}")
        
        return message_id
    
    def process_queue(self):
        """Process messages from the queue"""
        while self.processing:
            try:
                message = self.message_queue.dequeue()
                if message:
                    self._send_message(message)
                else:
                    time.sleep(0.1)  # Brief pause when queue is empty
            except Exception as e:
                logger.error(f"Queue processing error: {e}")
                time.sleep(1)
    
    def _send_message(self, message: Message):
        """Send a single message (simulated)"""
        try:
            message.status = MessageStatus.SENDING
            
            # Simulate message sending
            time.sleep(0.1)  # Simulate processing time
            
            # Mark as sent
            message.status = MessageStatus.SENT
            with self.message_queue._lock:
                self.message_queue.stats["sent_messages"] += 1
            
            logger.info(f"Message {message.id} sent successfully to {message.recipient}")
            
        except Exception as e:
            logger.error(f"Error sending message {message.id}: {e}")
            message.status = MessageStatus.FAILED
    
    def start_processing(self):
        """Start the message processing thread"""
        if not self.processing:
            self.processing = True
            self.processor_thread = threading.Thread(target=self.process_queue, daemon=True)
            self.processor_thread.start()
            logger.info("Message processing started")
    
    def stop_processing(self):
        """Stop the message processing thread"""
        self.processing = False
        if self.processor_thread:
            self.processor_thread.join(timeout=5)
        logger.info("Message processing stopped")
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        queue_status = self.message_queue.get_queue_status()
        
        return {
            "queue_status": queue_status,
            "agents_registered": len(self.agents),
            "processing_active": self.processing,
            "timestamp": time.time()
        }
    
    def broadcast_message(self, sender: str, content: str, 
                         priority: MessagePriority = MessagePriority.NORMAL) -> List[str]:
        """Send message to all registered agents"""
        message_ids = []
        for agent_id in self.agents.keys():
            msg_id = self.send_message(sender, agent_id, content, priority)
            if msg_id:
                message_ids.append(msg_id)
        
        logger.info(f"Broadcast message sent to {len(message_ids)} agents")
        return message_ids

# Export the classes
__all__ = ["SimpleMessageQueueSystem", "MessagePriority", "MessageStatus", "Message"]
