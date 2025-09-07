#!/usr/bin/env python3
"""
Message Processor - V2 Modular Architecture
=========================================

Handles message processing, creation, and lifecycle management.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4H - Communication Manager Modularization
License: MIT
"""

import logging
import json
import asyncio
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import asdict
from pathlib import Path

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority
from ...services.messaging import V2Message, UnifiedMessageType, UnifiedMessageStatus
from .models import Channel
from .types import CommunicationTypes, CommunicationConfig

logger = logging.getLogger(__name__)


class MessageProcessor(BaseManager):
    """
    Message Processor - Single responsibility: Message processing and lifecycle
    
    Manages:
    - Message creation and parsing
    - Message routing and delivery
    - Message status tracking
    - Message handlers and callbacks
    """

    def __init__(self, config_path: str = "config/message_processor.json"):
        """Initialize message processor"""
        super().__init__(
            manager_name="MessageProcessor",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        self.messages: Dict[str, V2Message] = {}
        self.message_handlers: Dict[str, Callable] = {}
        self.message_metrics: Dict[str, Dict[str, Any]] = {}
        
        # Message processing settings
        self.enable_message_tracking = True
        self.message_retention_hours = CommunicationConfig.MESSAGE_RETENTION_HOURS
        self.max_messages = CommunicationConfig.MAX_MESSAGES
        
        # Initialize message system
        self._load_manager_config()
    
    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.enable_message_tracking = config.get('enable_message_tracking', True)
                    self.message_retention_hours = config.get('message_retention_hours', 
                                                           CommunicationConfig.MESSAGE_RETENTION_HOURS)
                    self.max_messages = config.get('max_messages', CommunicationConfig.MAX_MESSAGES)
            else:
                logger.warning(f"Message processor config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load message processor config: {e}")
    
    async def process_incoming_message(self, channel_id: str, message_data: Any, 
                                     channel: Channel) -> str:
        """Process incoming message from channel"""
        try:
            # Parse message
            if isinstance(message_data, str):
                try:
                    message_content = json.loads(message_data)
                except json.JSONDecodeError:
                    message_content = message_data
            else:
                message_content = message_data
            
            # Create message record
            message_id = f"incoming_{channel_id}_{int(datetime.now().timestamp())}"
            
            message = V2Message(
                message_id=message_id,
                message_type=UnifiedMessageType.EVENT,
                sender_id="external",
                recipient_id="system",
                content=message_content,
                payload={"direction": CommunicationTypes.MessageDirection.INCOMING.value, 
                        "channel": channel_id},
                timestamp=datetime.now(),
                status=UnifiedMessageStatus.DELIVERED,
                retry_count=0,
                max_retries=0
            )
            
            self.messages[message_id] = message
            
            # Update channel statistics
            channel.message_count += 1
            channel.last_used = datetime.now().isoformat()
            
            # Initialize message metrics
            self.message_metrics[message_id] = {
                "processing_start": datetime.now().isoformat(),
                "processing_end": None,
                "processing_time": 0.0,
                "handler_called": False,
                "handler_success": False
            }
            
            # Emit event
            self._emit_event("message_received", {
                "message_id": message_id,
                "channel_id": channel_id,
                "content": message_content
            })
            
            # Call message handler if registered
            if channel_id in self.message_handlers:
                try:
                    await self.message_handlers[channel_id](message)
                    self.message_metrics[message_id]["handler_called"] = True
                    self.message_metrics[message_id]["handler_success"] = True
                except Exception as e:
                    logger.error(f"Message handler error for channel {channel_id}: {e}")
                    self.message_metrics[message_id]["handler_called"] = True
                    self.message_metrics[message_id]["handler_success"] = False
            
            # Update processing metrics
            self.message_metrics[message_id]["processing_end"] = datetime.now().isoformat()
            
            logger.info(f"Incoming message processed: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to process incoming message from channel {channel_id}: {e}")
            return ""
    
    async def create_outgoing_message(self, channel_id: str, content: Any, 
                                    message_type: UnifiedMessageType = UnifiedMessageType.TASK,
                                    recipient: str = "all", 
                                    metadata: Optional[Dict[str, Any]] = None) -> V2Message:
        """Create outgoing message"""
        try:
            message_id = f"outgoing_{channel_id}_{int(datetime.now().timestamp())}"
            
            message = V2Message(
                message_id=message_id,
                message_type=message_type,
                sender_id="system",
                recipient_id=recipient,
                content=content,
                payload=metadata or {},
                timestamp=datetime.now(),
                status=UnifiedMessageStatus.PENDING,
                retry_count=0,
                max_retries=CommunicationConfig.DEFAULT_RETRY_COUNT
            )
            
            self.messages[message_id] = message
            
            # Initialize message metrics
            self.message_metrics[message_id] = {
                "processing_start": datetime.now().isoformat(),
                "processing_end": None,
                "processing_time": 0.0,
                "delivery_attempts": 0,
                "delivery_success": False
            }
            
            self._emit_event("message_created", {
                "message_id": message_id,
                "channel_id": channel_id,
                "type": message_type.value
            })
            
            logger.info(f"Outgoing message created: {message_id}")
            return message
            
        except Exception as e:
            logger.error(f"Failed to create outgoing message: {e}")
            raise
    
    def register_message_handler(self, channel_id: str, handler: Callable):
        """Register message handler for a channel"""
        try:
            self.message_handlers[channel_id] = handler
            logger.info(f"Message handler registered for channel {channel_id}")
        except Exception as e:
            logger.error(f"Failed to register message handler for channel {channel_id}: {e}")
    
    def get_message_info(self, message_id: str) -> Optional[V2Message]:
        """Get message information"""
        try:
            return self.messages.get(message_id)
        except Exception as e:
            logger.error(f"Failed to get message info for {message_id}: {e}")
            return None
    
    def update_message_status(self, message_id: str, status: UnifiedMessageStatus) -> bool:
        """Update message status"""
        try:
            if message_id in self.messages:
                self.messages[message_id].status = status
                
                # Update metrics
                if message_id in self.message_metrics:
                    self.message_metrics[message_id]["processing_end"] = datetime.now().isoformat()
                
                self._emit_event("message_status_updated", {
                    "message_id": message_id,
                    "status": status.value
                })
                
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to update message status: {e}")
            return False
    
    def get_message_metrics(self) -> Dict[str, Any]:
        """Get message processing metrics"""
        try:
            total_messages = len(self.messages)
            successful_messages = len([m for m in self.messages.values() 
                                    if m.status == UnifiedMessageStatus.DELIVERED])
            failed_messages = len([m for m in self.messages.values() 
                                 if m.status == UnifiedMessageStatus.FAILED])
            
            # Calculate average processing time
            processing_times = []
            for metrics in self.message_metrics.values():
                if metrics.get("processing_end") and metrics.get("processing_start"):
                    start = datetime.fromisoformat(metrics["processing_start"])
                    end = datetime.fromisoformat(metrics["processing_end"])
                    processing_times.append((end - start).total_seconds())
            
            avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0.0
            
            return {
                "total_messages": total_messages,
                "successful_messages": successful_messages,
                "failed_messages": failed_messages,
                "success_rate": (successful_messages / total_messages * 100) if total_messages > 0 else 0,
                "average_processing_time": avg_processing_time,
                "message_metrics": self.message_metrics
            }
            
        except Exception as e:
            logger.error(f"Failed to get message metrics: {e}")
            return {}
    
    def cleanup_old_messages(self) -> int:
        """Clean up old messages based on retention policy"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=self.message_retention_hours)
            old_messages = [
                msg_id for msg_id, msg in self.messages.items()
                if msg.timestamp < cutoff_time
            ]
            
            for msg_id in old_messages:
                del self.messages[msg_id]
                if msg_id in self.message_metrics:
                    del self.message_metrics[msg_id]
            
            logger.info(f"Cleaned up {len(old_messages)} old messages")
            return len(old_messages)
            
        except Exception as e:
            logger.error(f"Failed to cleanup old messages: {e}")
            return 0

