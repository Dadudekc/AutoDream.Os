#!/usr/bin/env python3
"""
Inbox Delivery Service - V2 Compliant File-Based Messaging
=========================================================

V2 compliant inbox delivery service for file-based message delivery.
Provides reliable fallback messaging when PyAutoGUI is not available.

V2 Compliance: <300 lines, single responsibility for inbox delivery
Enterprise Ready: High availability, reliability, monitoring, error handling

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Dict, List, Optional

from ..models import UnifiedMessage, DeliveryMethod, MessageStatus
from ..interfaces import BaseMessageDelivery

logger = logging.getLogger(__name__)

class InboxDeliveryService(BaseMessageDelivery):
    """V2 compliant inbox delivery service for file-based messaging."""

    def __init__(self, base_path: str = "agent_workspaces"):
        """Initialize inbox delivery service."""
        super().__init__(DeliveryMethod.INBOX)
        self.base_path = Path(base_path)
        self.logger = logging.getLogger(__name__)
        
        # Ensure base path exists
        self.base_path.mkdir(parents=True, exist_ok=True)

    def send_message(self, message: UnifiedMessage) -> bool:
        """Send message to agent inbox."""
        try:
            # Create inbox directory for recipient
            inbox_dir = self.base_path / message.recipient / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)

            # Create timestamped filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"CAPTAIN_MESSAGE_{timestamp}_{message.message_id[:8]}.md"
            filepath = inbox_dir / filename

            # Write message to file
            success = self._write_message_to_file(message, filepath)
            
            if success:
                # Update message status
                message.status = MessageStatus.DELIVERED
                message.delivery_method = DeliveryMethod.INBOX
                self.logger.info(f"Message delivered to inbox: {message.recipient}")
            else:
                message.status = MessageStatus.FAILED
                self.logger.error(f"Failed to deliver message to inbox: {message.recipient}")
            
            # Record metrics
            self._record_metrics(message, success)
            
            return success

        except Exception as e:
            self.logger.error(f"Error sending message to inbox: {e}")
            message.status = MessageStatus.FAILED
            self._record_metrics(message, False)
            return False

    def can_deliver(self, message: UnifiedMessage) -> bool:
        """Check if inbox can deliver this message."""
        # Inbox can deliver any message to any agent
        return True

    def _write_message_to_file(self, message: UnifiedMessage, filepath: Path) -> bool:
        """Write message to file in markdown format."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                # Write message header
                f.write(f'# 🚨 CAPTAIN MESSAGE - {message.message_type.value.upper()}\n\n')
                f.write(f'**From**: {message.sender}\n')
                f.write(f'**To**: {message.recipient}\n')
                f.write(f'**Priority**: {message.priority.value}\n')
                f.write(f'**Message ID**: {message.message_id}\n')
                f.write(f'**Timestamp**: {message.timestamp.isoformat()}\n')
                
                if message.tags:
                    f.write(f'**Tags**: {", ".join(tag.value for tag in message.tags)}\n')
                
                if message.metadata:
                    f.write(f'**Metadata**: {message.metadata}\n')
                
                f.write('\n---\n\n')
                
                # Write message content
                f.write(f'{message.content}\n')
                f.write('\n---\n')
                f.write('*Message delivered via Unified Messaging Service*\n')
                
                # Add delivery info
                f.write(f'\n**Delivery Method**: {self.delivery_method.value}\n')
                f.write(f'**Delivery Time**: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')

            return True

        except Exception as e:
            self.logger.error(f"Error writing message to file {filepath}: {e}")
            return False

    def get_inbox_status(self, agent_id: str) -> Dict[str, any]:
        """Get inbox status for specific agent."""
        try:
            inbox_dir = self.base_path / agent_id / "inbox"
            
            if not inbox_dir.exists():
                return {
                    "agent_id": agent_id,
                    "inbox_exists": False,
                    "message_count": 0,
                    "latest_message": None
                }
            
            # Count messages
            message_files = list(inbox_dir.glob("CAPTAIN_MESSAGE_*.md"))
            message_count = len(message_files)
            
            # Get latest message
            latest_message = None
            if message_files:
                latest_file = max(message_files, key=lambda f: f.stat().st_mtime)
                latest_message = {
                    "filename": latest_file.name,
                    "modified_time": time.ctime(latest_file.stat().st_mtime),
                    "size_bytes": latest_file.stat().st_size
                }
            
            return {
                "agent_id": agent_id,
                "inbox_exists": True,
                "message_count": message_count,
                "latest_message": latest_message,
                "inbox_path": str(inbox_dir)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting inbox status for {agent_id}: {e}")
            return {
                "agent_id": agent_id,
                "inbox_exists": False,
                "message_count": 0,
                "latest_message": None,
                "error": str(e)
            }

    def get_all_inbox_status(self) -> Dict[str, Dict[str, any]]:
        """Get inbox status for all agents."""
        try:
            status = {}
            
            # Get all agent directories
            agent_dirs = [d for d in self.base_path.iterdir() if d.is_dir()]
            
            for agent_dir in agent_dirs:
                agent_id = agent_dir.name
                status[agent_id] = self.get_inbox_status(agent_id)
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting all inbox status: {e}")
            return {}

    def cleanup_old_messages(self, agent_id: str, days_old: int = 30) -> int:
        """Clean up old messages from agent inbox."""
        try:
            inbox_dir = self.base_path / agent_id / "inbox"
            
            if not inbox_dir.exists():
                return 0
            
            # Calculate cutoff time
            cutoff_time = time.time() - (days_old * 24 * 60 * 60)
            
            # Find old message files
            message_files = list(inbox_dir.glob("CAPTAIN_MESSAGE_*.md"))
            old_files = [f for f in message_files if f.stat().st_mtime < cutoff_time]
            
            # Remove old files
            removed_count = 0
            for old_file in old_files:
                try:
                    old_file.unlink()
                    removed_count += 1
                except Exception as e:
                    self.logger.warning(f"Failed to remove old message {old_file}: {e}")
            
            if removed_count > 0:
                self.logger.info(f"Cleaned up {removed_count} old messages from {agent_id}")
            
            return removed_count
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old messages for {agent_id}: {e}")
            return 0

    def get_system_status(self) -> Dict[str, any]:
        """Get inbox delivery system status."""
        try:
            # Check base path
            base_exists = self.base_path.exists()
            
            # Count total agents with inboxes
            agent_count = 0
            total_messages = 0
            
            if base_exists:
                agent_dirs = [d for d in self.base_path.iterdir() if d.is_dir()]
                agent_count = len(agent_dirs)
                
                for agent_dir in agent_dirs:
                    inbox_dir = agent_dir / "inbox"
                    if inbox_dir.exists():
                        message_files = list(inbox_dir.glob("CAPTAIN_MESSAGE_*.md"))
                        total_messages += len(message_files)
            
            return {
                "base_path": str(self.base_path),
                "base_path_exists": base_exists,
                "agent_count": agent_count,
                "total_messages": total_messages,
                "delivery_method": self.delivery_method.value,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            self.logger.error(f"Error getting inbox system status: {e}")
            return {
                "error": str(e),
                "delivery_method": self.delivery_method.value,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

# Global instance
inbox_delivery_service = InboxDeliveryService()

# Public API functions
def get_inbox_delivery_service() -> InboxDeliveryService:
    """Get the inbox delivery service instance."""
    return inbox_delivery_service

def send_message_to_inbox(message: UnifiedMessage) -> bool:
    """Send message to inbox using inbox delivery service."""
    return inbox_delivery_service.send_message(message)

def get_inbox_status(agent_id: str) -> Dict[str, any]:
    """Get inbox status for agent."""
    return inbox_delivery_service.get_inbox_status(agent_id)

def get_all_inbox_status() -> Dict[str, Dict[str, any]]:
    """Get inbox status for all agents."""
    return inbox_delivery_service.get_all_inbox_status()

def cleanup_old_messages(agent_id: str, days_old: int = 30) -> int:
    """Clean up old messages from agent inbox."""
    return inbox_delivery_service.cleanup_old_messages(agent_id, days_old)

# EXPORTS
__all__ = [
    # Main class
    "InboxDeliveryService",
    
    # Global instance
    "inbox_delivery_service",
    
    # Public API functions
    "get_inbox_delivery_service",
    "send_message_to_inbox",
    "get_inbox_status",
    "get_all_inbox_status",
    "cleanup_old_messages",
]