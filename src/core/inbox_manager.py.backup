#!/usr/bin/env python3
"""
Inbox Manager - Agent Cellphone V2
=================================

Manages message routing and storage with strict OOP design.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class MessageStatus(Enum):
    """Message status states."""
    PENDING = "pending"
    READ = "read"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Message:
    """Message data structure."""
    message_id: str
    sender: str
    recipient: str
    subject: str
    content: str
    priority: MessagePriority
    status: MessageStatus
    created_at: str
    read_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class InboxManager:
    """
    Inbox Manager - Single responsibility: Message routing and storage.
    
    This service manages:
    - Message storage and retrieval
    - Message routing between agents
    - Message status tracking
    - Priority-based message handling
    """
    
    def __init__(self, workspace_manager):
        """Initialize Inbox Manager with workspace manager."""
        self.workspace_manager = workspace_manager
        self.logger = self._setup_logging()
        self.messages: Dict[str, Message] = {}
        self.status = "initialized"
        
        # Load existing messages
        self._load_messages()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("InboxManager")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_messages(self):
        """Load existing messages from all inboxes."""
        try:
            for workspace in self.workspace_manager.get_all_workspaces():
                inbox_path = Path(workspace.inbox_path)
                if inbox_path.exists():
                    for message_file in inbox_path.glob("*.json"):
                        try:
                            with open(message_file, 'r') as f:
                                message_data = json.load(f)
                                
                                # Convert string values back to enums
                                if 'priority' in message_data:
                                    message_data['priority'] = MessagePriority(message_data['priority'])
                                if 'status' in message_data:
                                    message_data['status'] = MessageStatus(message_data['status'])
                                
                                message = Message(**message_data)
                                self.messages[message.message_id] = message
                        except Exception as e:
                            self.logger.error(f"Failed to load message from {message_file}: {e}")
            
            self.logger.info(f"Loaded {len(self.messages)} existing messages")
        except Exception as e:
            self.logger.error(f"Failed to load messages: {e}")
    
    def _generate_message_id(self, sender: str, recipient: str) -> str:
        """Generate unique message ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"{sender}_{recipient}_{timestamp}"
    
    def send_message(self, sender: str, recipient: str, subject: str, 
                    content: str, priority: MessagePriority = MessagePriority.NORMAL,
                    metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Send a message to a recipient."""
        try:
            # Generate message ID
            message_id = self._generate_message_id(sender, recipient)
            
            # Create message
            message = Message(
                message_id=message_id,
                sender=sender,
                recipient=recipient,
                subject=subject,
                content=content,
                priority=priority,
                status=MessageStatus.PENDING,
                created_at=datetime.now().isoformat(),
                metadata=metadata or {}
            )
            
            # Store message
            self.messages[message_id] = message
            
            # Save to recipient's inbox
            recipient_workspace = self.workspace_manager.get_workspace_info(recipient)
            if recipient_workspace:
                inbox_path = Path(recipient_workspace.inbox_path)
                message_file = inbox_path / f"{message_id}.json"
                
                with open(message_file, 'w') as f:
                    # Convert enums to strings for JSON serialization
                    message_dict = message.__dict__.copy()
                    message_dict['priority'] = message.priority.value
                    message_dict['status'] = message.status.value
                    json.dump(message_dict, f, indent=2, default=str)
                
                self.logger.info(f"Message sent from {sender} to {recipient}: {message_id}")
                return message_id
            else:
                self.logger.error(f"Recipient workspace not found: {recipient}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return None
    
    def get_messages(self, agent_id: str, status: Optional[MessageStatus] = None,
                    priority: Optional[MessagePriority] = None) -> List[Message]:
        """Get messages for an agent with optional filtering."""
        try:
            messages = []
            for message in self.messages.values():
                if message.recipient == agent_id:
                    if status and message.status != status:
                        continue
                    if priority and message.priority != priority:
                        continue
                    messages.append(message)
            
            # Sort by priority and creation time
            priority_order = {MessagePriority.URGENT: 0, MessagePriority.HIGH: 1,
                            MessagePriority.NORMAL: 2, MessagePriority.LOW: 3}
            
            messages.sort(key=lambda m: (priority_order[m.priority], m.created_at))
            return messages
            
        except Exception as e:
            self.logger.error(f"Failed to get messages for {agent_id}: {e}")
            return []
    
    def get_message(self, message_id: str) -> Optional[Message]:
        """Get a specific message by ID."""
        return self.messages.get(message_id)
    
    def mark_message_read(self, message_id: str) -> bool:
        """Mark a message as read."""
        try:
            if message_id in self.messages:
                message = self.messages[message_id]
                message.status = MessageStatus.READ
                message.read_at = datetime.now().isoformat()
                
                # Update file
                recipient_workspace = self.workspace_manager.get_workspace_info(message.recipient)
                if recipient_workspace:
                    inbox_path = Path(recipient_workspace.inbox_path)
                    message_file = inbox_path / f"{message_id}.json"
                    
                    with open(message_file, 'w') as f:
                        # Convert enums to strings for JSON serialization
                        message_dict = message.__dict__.copy()
                        message_dict['priority'] = message.priority.value
                        message_dict['status'] = message.status.value
                        json.dump(message_dict, f, indent=2, default=str)
                    
                    self.logger.info(f"Message marked as read: {message_id}")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to mark message as read: {e}")
            return False
    
    def update_message_status(self, message_id: str, status: MessageStatus) -> bool:
        """Update message status."""
        try:
            if message_id in self.messages:
                message = self.messages[message_id]
                message.status = status
                
                # Update file
                recipient_workspace = self.workspace_manager.get_workspace_info(message.recipient)
                if recipient_workspace:
                    inbox_path = Path(recipient_workspace.inbox_path)
                    message_file = inbox_path / f"{message_id}.json"
                    
                    with open(message_file, 'w') as f:
                        # Convert enums to strings for JSON serialization
                        message_dict = message.__dict__.copy()
                        message_dict['priority'] = message.priority.value
                        message_dict['status'] = message.status.value
                        json.dump(message_dict, f, indent=2, default=str)
                    
                    self.logger.info(f"Message status updated: {message_id} -> {status.value}")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update message status: {e}")
            return False
    
    def delete_message(self, message_id: str) -> bool:
        """Delete a message."""
        try:
            if message_id in self.messages:
                message = self.messages[message_id]
                
                # Remove from file system
                recipient_workspace = self.workspace_manager.get_workspace_info(message.recipient)
                if recipient_workspace:
                    inbox_path = Path(recipient_workspace.inbox_path)
                    message_file = inbox_path / f"{message_id}.json"
                    
                    if message_file.exists():
                        message_file.unlink()
                
                # Remove from memory
                del self.messages[message_id]
                
                self.logger.info(f"Message deleted: {message_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to delete message: {e}")
            return False
    
    def get_inbox_status(self, agent_id: str) -> Dict[str, Any]:
        """Get inbox status for an agent."""
        try:
            messages = self.get_messages(agent_id)
            
            status_counts = {}
            for status in MessageStatus:
                status_counts[status.value] = len([m for m in messages if m.status == status])
            
            priority_counts = {}
            for priority in MessagePriority:
                priority_counts[priority.value] = len([m for m in messages if m.priority == priority])
            
            return {
                "agent_id": agent_id,
                "total_messages": len(messages),
                "status_counts": status_counts,
                "priority_counts": priority_counts,
                "unread_count": status_counts.get("pending", 0),
                "urgent_count": priority_counts.get("urgent", 0)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get inbox status for {agent_id}: {e}")
            return {"agent_id": agent_id, "error": str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall inbox system status."""
        try:
            total_messages = len(self.messages)
            pending_messages = len([m for m in self.messages.values() if m.status == MessageStatus.PENDING])
            urgent_messages = len([m for m in self.messages.values() if m.priority == MessagePriority.URGENT])
            
            return {
                "status": self.status,
                "total_messages": total_messages,
                "pending_messages": pending_messages,
                "urgent_messages": urgent_messages,
                "active_agents": len(set(m.recipient for m in self.messages.values()))
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {"status": "error", "error": str(e)}


def main():
    """CLI interface for Inbox Manager testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Inbox Manager Testing Interface")
    parser.add_argument("--init", action="store_true", help="Initialize inbox manager")
    parser.add_argument("--send", nargs=4, metavar=("SENDER", "RECIPIENT", "SUBJECT", "CONTENT"), help="Send message")
    parser.add_argument("--status", metavar="AGENT_ID", help="Show inbox status for agent")
    parser.add_argument("--messages", metavar="AGENT_ID", help="Show messages for agent")
    parser.add_argument("--test", action="store_true", help="Run inbox manager tests")
    
    args = parser.parse_args()
    
    # Create workspace manager first
    from workspace_manager import WorkspaceManager
    workspace_manager = WorkspaceManager()
    
    # Create inbox manager
    inbox_manager = InboxManager(workspace_manager)
    
    if args.init or not any([args.init, args.send, args.status, args.messages, args.test]):
        print("📬 Inbox Manager - Agent Cellphone V2")
        print("Manager initialized successfully")
    
    if args.send:
        sender, recipient, subject, content = args.send
        message_id = inbox_manager.send_message(sender, recipient, subject, content)
        if message_id:
            print(f"✅ Message sent successfully: {message_id}")
        else:
            print("❌ Failed to send message")
    
    if args.status:
        status = inbox_manager.get_inbox_status(args.status)
        print(f"📊 Inbox Status for {args.status}:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    if args.messages:
        messages = inbox_manager.get_messages(args.messages)
        print(f"📨 Messages for {args.messages}:")
        for message in messages:
            print(f"  {message.message_id}: {message.subject} (Priority: {message.priority.value})")
    
    if args.test:
        print("🧪 Running inbox manager tests...")
        try:
            # Test message sending
            message_id = inbox_manager.send_message("TestAgent", "Agent-1", "Test", "Test message")
            print(f"Message sending test: {'✅ Success' if message_id else '❌ Failed'}")
            
            # Test message retrieval
            messages = inbox_manager.get_messages("Agent-1")
            print(f"Message retrieval test: {'✅ Success' if messages else '❌ Failed'}")
            
            # Test status update
            if message_id:
                success = inbox_manager.mark_message_read(message_id)
                print(f"Status update test: {'✅ Success' if success else '❌ Failed'}")
            
        except Exception as e:
            print(f"❌ Inbox manager test failed: {e}")


if __name__ == "__main__":
    main()
