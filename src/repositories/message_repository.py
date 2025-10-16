"""
Message Repository - Data Access Layer
=======================================

Handles all message-related data operations including message storage,
history retrieval, and message management.

Author: Agent-7 - Repository Cloning Specialist
Mission: Quarantine Fix Phase 3 (Repository Pattern)
Date: 2025-10-16
Points: 300 pts
V2 Compliant: ≤400 lines, single responsibility

Architecture:
- Follows repository pattern (data access abstraction)
- No business logic (data operations only)
- Type hints for all methods
- Comprehensive error handling

Usage:
    from src.repositories import MessageRepository
    
    repo = MessageRepository()
    repo.save_message(message_dict)
    history = repo.get_message_history("Agent-7")
    recent = repo.get_recent_messages(limit=10)
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MessageRepository:
    """
    Repository for message data operations.
    
    Provides data access methods for message storage, retrieval,
    and history management.
    """
    
    def __init__(
        self, 
        message_queue_dir: str = "message_queue",
        workspace_root: str = "agent_workspaces"
    ):
        """
        Initialize message repository.
        
        Args:
            message_queue_dir: Directory for message queue storage
            workspace_root: Root directory for agent workspaces
        """
        self.message_queue_dir = Path(message_queue_dir)
        self.workspace_root = Path(workspace_root)
    
    def save_message(self, message: Dict[str, Any]) -> bool:
        """
        Save message to storage.
        
        Args:
            message: Message data dictionary with required fields:
                - to: recipient agent ID
                - from: sender agent ID
                - content: message content
                - timestamp: message timestamp
                
        Returns:
            True if successfully saved, False otherwise
        """
        try:
            # Validate required fields
            required_fields = ['to', 'from', 'content']
            if not all(field in message for field in required_fields):
                logger.error(f"Message missing required fields: {required_fields}")
                return False
            
            recipient = message['to']
            timestamp = message.get(
                'timestamp', 
                datetime.now().isoformat()
            )
            message['timestamp'] = timestamp
            
            # Save to recipient inbox
            inbox_dir = self.workspace_root / recipient / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate message filename
            message_id = message.get(
                'message_id',
                f"msg_{timestamp.replace(':', '_').replace('-', '_')}"
            )
            message_file = inbox_dir / f"{message_id}.json"
            
            # Save message
            with open(message_file, 'w', encoding='utf-8') as f:
                json.dump(message, f, indent=2)
            
            logger.info(f"Saved message to {recipient} inbox")
            return True
            
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return False
    
    def get_message_history(
        self, 
        agent_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get message history for agent.
        
        Args:
            agent_id: Agent identifier
            limit: Optional limit on number of messages
            
        Returns:
            List of message data dictionaries
        """
        try:
            inbox_dir = self.workspace_root / agent_id / "inbox"
            
            if not inbox_dir.exists():
                logger.warning(f"Inbox not found for {agent_id}")
                return []
            
            messages = []
            
            # Read all JSON message files
            for message_file in sorted(
                inbox_dir.glob("*.json"),
                key=lambda f: f.stat().st_mtime,
                reverse=True
            ):
                try:
                    with open(message_file, 'r', encoding='utf-8') as f:
                        message_data = json.load(f)
                    
                    messages.append(message_data)
                    
                    if limit and len(messages) >= limit:
                        break
                        
                except Exception as e:
                    logger.warning(f"Error reading message {message_file}: {e}")
            
            return messages
            
        except Exception as e:
            logger.error(f"Error retrieving message history for {agent_id}: {e}")
            return []
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent messages across all agents.
        
        Args:
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of recent message data dictionaries
        """
        all_messages = []
        
        try:
            # Collect messages from all agent inboxes
            for agent_dir in self.workspace_root.iterdir():
                if not agent_dir.is_dir():
                    continue
                
                inbox_dir = agent_dir / "inbox"
                if not inbox_dir.exists():
                    continue
                
                for message_file in inbox_dir.glob("*.json"):
                    try:
                        with open(message_file, 'r', encoding='utf-8') as f:
                            message_data = json.load(f)
                        
                        message_data['_file_path'] = str(message_file)
                        message_data['_modified_time'] = message_file.stat().st_mtime
                        
                        all_messages.append(message_data)
                        
                    except Exception as e:
                        logger.warning(f"Error reading message {message_file}: {e}")
            
            # Sort by modification time (most recent first)
            all_messages.sort(
                key=lambda m: m.get('_modified_time', 0),
                reverse=True
            )
            
            # Return limited results
            return all_messages[:limit]
            
        except Exception as e:
            logger.error(f"Error retrieving recent messages: {e}")
            return []
    
    def get_messages_between(
        self, 
        from_agent: str, 
        to_agent: str
    ) -> List[Dict[str, Any]]:
        """
        Get messages between two agents.
        
        Args:
            from_agent: Sender agent ID
            to_agent: Recipient agent ID
            
        Returns:
            List of message data dictionaries
        """
        all_messages = self.get_message_history(to_agent)
        
        filtered_messages = [
            msg for msg in all_messages
            if msg.get('from') == from_agent
        ]
        
        return filtered_messages
    
    def delete_message(
        self, 
        agent_id: str, 
        message_id: str
    ) -> bool:
        """
        Delete message from agent inbox.
        
        Args:
            agent_id: Agent identifier
            message_id: Message identifier
            
        Returns:
            True if successfully deleted, False otherwise
        """
        try:
            inbox_dir = self.workspace_root / agent_id / "inbox"
            message_file = inbox_dir / f"{message_id}.json"
            
            if not message_file.exists():
                logger.warning(f"Message {message_id} not found")
                return False
            
            message_file.unlink()
            logger.info(f"Deleted message {message_id} from {agent_id} inbox")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting message {message_id}: {e}")
            return False
    
    def get_unread_messages(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get unread messages for agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            List of unread message data dictionaries
        """
        all_messages = self.get_message_history(agent_id)
        
        unread_messages = [
            msg for msg in all_messages
            if not msg.get('read', False)
        ]
        
        return unread_messages
    
    def mark_message_read(
        self, 
        agent_id: str, 
        message_id: str
    ) -> bool:
        """
        Mark message as read.
        
        Args:
            agent_id: Agent identifier
            message_id: Message identifier
            
        Returns:
            True if successfully marked, False otherwise
        """
        try:
            inbox_dir = self.workspace_root / agent_id / "inbox"
            message_file = inbox_dir / f"{message_id}.json"
            
            if not message_file.exists():
                logger.warning(f"Message {message_id} not found")
                return False
            
            with open(message_file, 'r', encoding='utf-8') as f:
                message_data = json.load(f)
            
            message_data['read'] = True
            message_data['read_at'] = datetime.now().isoformat()
            
            with open(message_file, 'w', encoding='utf-8') as f:
                json.dump(message_data, f, indent=2)
            
            logger.info(f"Marked message {message_id} as read")
            return True
            
        except Exception as e:
            logger.error(f"Error marking message {message_id} as read: {e}")
            return False

