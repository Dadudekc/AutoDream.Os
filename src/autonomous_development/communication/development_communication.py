#!/usr/bin/env python3
"""
Development Communication - Agent Cellphone V2
============================================

Communication system for autonomous development coordination.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from ..core.enums import TaskStatus, WorkflowState
from ..core.models import DevelopmentTask


@dataclass
class CommunicationMessage:
    """Communication message structure"""
    message_id: str
    sender_id: str
    recipient_id: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime
    priority: str = "normal"
    requires_ack: bool = False
    acknowledged: bool = False
    acknowledged_at: Optional[datetime] = None


class DevelopmentCommunication:
    """Communication system for autonomous development coordination"""
    
    def __init__(self):
        self.messages: Dict[str, CommunicationMessage] = {}
        self.message_counter = 0
        self.logger = logging.getLogger(__name__)
        self.communication_stats = {
            "total_messages_sent": 0,
            "total_messages_received": 0,
            "messages_acknowledged": 0,
            "messages_pending_ack": 0,
            "communication_errors": 0
        }
        self.message_handlers: Dict[str, callable] = {}
        self._initialize_message_handlers()
    
    def _initialize_message_handlers(self):
        """Initialize message type handlers"""
        self.message_handlers = {
            "task_assignment": self._handle_task_assignment,
            "task_update": self._handle_task_update,
            "workflow_status": self._handle_workflow_status,
            "agent_heartbeat": self._handle_agent_heartbeat,
            "task_completion": self._handle_task_completion,
            "error_report": self._handle_error_report,
            "coordination_request": self._handle_coordination_request
        }
    
    def send_message(self, sender_id: str, recipient_id: str, message_type: str,
                    content: Dict[str, Any], priority: str = "normal", 
                    requires_ack: bool = False) -> str:
        """Send a communication message"""
        self.message_counter += 1
        message_id = f"msg_{self.message_counter:06d}"
        
        message = CommunicationMessage(
            message_id=message_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_type=message_type,
            content=content,
            timestamp=datetime.now(),
            priority=priority,
            requires_ack=requires_ack
        )
        
        self.messages[message_id] = message
        self.communication_stats["total_messages_sent"] += 1
        
        if requires_ack:
            self.communication_stats["messages_pending_ack"] += 1
        
        self.logger.info(f"📤 Sent message {message_id}: {message_type} from {sender_id} to {recipient_id}")
        return message_id
    
    def receive_message(self, message_id: str) -> Optional[CommunicationMessage]:
        """Receive a communication message"""
        message = self.messages.get(message_id)
        if message:
            self.communication_stats["total_messages_received"] += 1
            self.logger.info(f"📥 Received message {message_id}: {message.message_type}")
        return message
    
    def acknowledge_message(self, message_id: str, acknowledger_id: str) -> bool:
        """Acknowledge a message"""
        message = self.messages.get(message_id)
        if not message or not message.requires_ack:
            return False
        
        if message.acknowledged:
            return False
        
        message.acknowledged = True
        message.acknowledged_at = datetime.now()
        self.communication_stats["messages_acknowledged"] += 1
        self.communication_stats["messages_pending_ack"] -= 1
        
        self.logger.info(f"✅ Message {message_id} acknowledged by {acknowledger_id}")
        return True
    
    def get_messages_for_agent(self, agent_id: str, message_type: Optional[str] = None) -> List[CommunicationMessage]:
        """Get messages for a specific agent"""
        messages = []
        for message in self.messages.values():
            if message.recipient_id == agent_id:
                if message_type is None or message.message_type == message_type:
                    messages.append(message)
        
        # Sort by timestamp (oldest first)
        messages.sort(key=lambda x: x.timestamp)
        return messages
    
    def get_pending_acknowledgments(self, agent_id: str) -> List[CommunicationMessage]:
        """Get messages pending acknowledgment from an agent"""
        return [
            message for message in self.messages.values()
            if (message.recipient_id == agent_id and 
                message.requires_ack and not message.acknowledged)
        ]
    
    def process_message(self, message_id: str) -> bool:
        """Process a received message"""
        message = self.messages.get(message_id)
        if not message:
            return False
        
        try:
            # Get handler for message type
            handler = self.message_handlers.get(message.message_type)
            if handler:
                handler(message)
                return True
            else:
                self.logger.warning(f"No handler for message type: {message.message_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error processing message {message_id}: {e}")
            self.communication_stats["communication_errors"] += 1
            return False
    
    def _handle_task_assignment(self, message: CommunicationMessage):
        """Handle task assignment message"""
        task_id = message.content.get("task_id")
        agent_id = message.content.get("assigned_agent")
        
        self.logger.info(f"📋 Task assignment: {task_id} -> {agent_id}")
        
        # In real system, would update task manager and agent coordinator
        # For now, just log the assignment
    
    def _handle_task_update(self, message: CommunicationMessage):
        """Handle task update message"""
        task_id = message.content.get("task_id")
        status = message.content.get("status")
        progress = message.content.get("progress")
        
        self.logger.info(f"📊 Task update: {task_id} - {status} ({progress}%)")
        
        # In real system, would update task manager
        # For now, just log the update
    
    def _handle_workflow_status(self, message: CommunicationMessage):
        """Handle workflow status message"""
        workflow_state = message.content.get("state")
        cycle_count = message.content.get("cycle_count")
        
        self.logger.info(f"🔄 Workflow status: {workflow_state} (Cycle {cycle_count})")
        
        # In real system, would update workflow engine
        # For now, just log the status
    
    def _handle_agent_heartbeat(self, message: CommunicationMessage):
        """Handle agent heartbeat message"""
        agent_id = message.content.get("agent_id")
        status = message.content.get("status")
        
        self.logger.debug(f"💓 Agent heartbeat: {agent_id} - {status}")
        
        # In real system, would update agent coordinator
        # For now, just log the heartbeat
    
    def _handle_task_completion(self, message: CommunicationMessage):
        """Handle task completion message"""
        task_id = message.content.get("task_id")
        agent_id = message.content.get("completed_by")
        completion_time = message.content.get("completion_time")
        
        self.logger.info(f"🎉 Task completed: {task_id} by {agent_id} in {completion_time}h")
        
        # In real system, would update task manager and agent coordinator
        # For now, just log the completion
    
    def _handle_error_report(self, message: CommunicationMessage):
        """Handle error report message"""
        error_type = message.content.get("error_type")
        error_message = message.content.get("error_message")
        agent_id = message.content.get("reported_by")
        
        self.logger.error(f"❌ Error report from {agent_id}: {error_type} - {error_message}")
        
        # In real system, would handle error appropriately
        # For now, just log the error
    
    def _handle_coordination_request(self, message: CommunicationMessage):
        """Handle coordination request message"""
        request_type = message.content.get("request_type")
        requesting_agent = message.content.get("requesting_agent")
        details = message.content.get("details")
        
        self.logger.info(f"🤝 Coordination request from {requesting_agent}: {request_type}")
        
        # In real system, would handle coordination request
        # For now, just log the request
    
    def broadcast_message(self, sender_id: str, message_type: str, content: Dict[str, Any],
                         priority: str = "normal") -> List[str]:
        """Broadcast message to all agents"""
        message_ids = []
        
        # In real system, would get list of all agent IDs
        # For now, use sample agent IDs
        all_agents = ["agent_1", "agent_2", "agent_3", "agent_4", "agent_5"]
        
        for agent_id in all_agents:
            if agent_id != sender_id:  # Don't send to self
                message_id = self.send_message(
                    sender_id=sender_id,
                    recipient_id=agent_id,
                    message_type=message_type,
                    content=content,
                    priority=priority
                )
                message_ids.append(message_id)
        
        self.logger.info(f"📢 Broadcasted {message_type} to {len(message_ids)} agents")
        return message_ids
    
    def get_communication_statistics(self) -> Dict[str, any]:
        """Get communication statistics"""
        return {
            "total_messages": len(self.messages),
            "messages_by_type": self._get_message_type_distribution(),
            "communication_stats": self.communication_stats.copy(),
            "pending_acknowledgments": self.communication_stats["messages_pending_ack"]
        }
    
    def _get_message_type_distribution(self) -> Dict[str, int]:
        """Get distribution of messages by type"""
        distribution = {}
        for message in self.messages.values():
            msg_type = message.message_type
            distribution[msg_type] = distribution.get(msg_type, 0) + 1
        return distribution
    
    def cleanup_old_messages(self, days_old: int = 7) -> int:
        """Remove old messages"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        removed_count = 0
        
        message_ids_to_remove = []
        for message_id, message in self.messages.items():
            if message.timestamp < cutoff_date:
                message_ids_to_remove.append(message_id)
        
        for message_id in message_ids_to_remove:
            del self.messages[message_id]
            removed_count += 1
        
        self.logger.info(f"🧹 Cleaned up {removed_count} old messages")
        return removed_count
    
    def export_messages(self) -> List[Dict[str, any]]:
        """Export messages to dictionary format"""
        return [asdict(message) for message in self.messages.values()]
    
    def import_messages(self, messages_data: List[Dict[str, any]]) -> int:
        """Import messages from dictionary format"""
        imported_count = 0
        
        for message_data in messages_data:
            try:
                # Convert timestamp string back to datetime
                if message_data.get("timestamp"):
                    message_data["timestamp"] = datetime.fromisoformat(message_data["timestamp"])
                if message_data.get("acknowledged_at"):
                    message_data["acknowledged_at"] = datetime.fromisoformat(message_data["acknowledged_at"])
                
                message = CommunicationMessage(**message_data)
                self.messages[message.message_id] = message
                imported_count += 1
                
            except Exception as e:
                self.logger.error(f"Failed to import message: {e}")
        
        self.logger.info(f"Imported {imported_count} messages")
        return imported_count
