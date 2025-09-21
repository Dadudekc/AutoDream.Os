#!/usr/bin/env python3
"""
Mailbox Manager
================

Manages mailbox checking and message processing.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List

from ...agent_devlog_automation import auto_create_devlog

logger = logging.getLogger(__name__)


class MailboxManager:
    """Manages mailbox operations for autonomous agents."""
    
    def __init__(self, agent_id: str, workspace_dir: Path):
        """Initialize mailbox manager."""
        self.agent_id = agent_id
        self.workspace_dir = workspace_dir
        self.inbox_dir = workspace_dir / "inbox"
        self.processed_dir = workspace_dir / "processed"
        
        # Ensure directories exist
        self.inbox_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)
    
    async def check_mailbox(self) -> int:
        """Check inbox for new messages and process them."""
        messages_processed = 0
        
        if not self.inbox_dir.exists():
            return 0
        
        for message_file in self.inbox_dir.glob("*.json"):
            try:
                with open(message_file, 'r') as f:
                    message = json.load(f)
                
                # Process message
                await self._process_message(message)
                
                # Move to processed
                processed_file = self.processed_dir / message_file.name
                message_file.rename(processed_file)
                messages_processed += 1
                
                # Create devlog for message processing
                await auto_create_devlog(
                    self.agent_id,
                    f"Processed message from {message.get('from', 'unknown')}",
                    "completed",
                    {"message_id": message.get('id'), "subject": message.get('subject', 'No subject')}
                )
                
            except Exception as e:
                logger.error(f"{self.agent_id}: Error processing message {message_file}: {e}")
        
        return messages_processed
    
    async def _process_message(self, message: Dict[str, Any]) -> None:
        """Process a single message."""
        try:
            # Extract message details
            message_id = message.get('id', 'unknown')
            sender = message.get('from', 'unknown')
            subject = message.get('subject', 'No subject')
            content = message.get('content', '')
            priority = message.get('priority', 'normal')
            
            logger.info(f"{self.agent_id}: Processing message {message_id} from {sender}")
            
            # Handle different message types
            if message.get('type') == 'task_assignment':
                await self._handle_task_assignment(message)
            elif message.get('type') == 'coordination':
                await self._handle_coordination_message(message)
            elif message.get('type') == 'status_request':
                await self._handle_status_request(message)
            else:
                await self._handle_general_message(message)
                
        except Exception as e:
            logger.error(f"{self.agent_id}: Error processing message: {e}")
    
    async def _handle_task_assignment(self, message: Dict[str, Any]) -> None:
        """Handle task assignment message."""
        task_data = message.get('task_data', {})
        logger.info(f"{self.agent_id}: Received task assignment: {task_data.get('title', 'Unknown task')}")
        
        # Create devlog for task assignment
        await auto_create_devlog(
            self.agent_id,
            "Task assignment received",
            "completed",
            {"task_title": task_data.get('title'), "priority": task_data.get('priority')}
        )
    
    async def _handle_coordination_message(self, message: Dict[str, Any]) -> None:
        """Handle coordination message."""
        coordination_data = message.get('coordination_data', {})
        logger.info(f"{self.agent_id}: Received coordination message: {coordination_data.get('type', 'Unknown')}")
        
        # Create devlog for coordination
        await auto_create_devlog(
            self.agent_id,
            "Coordination message received",
            "completed",
            {"coordination_type": coordination_data.get('type')}
        )
    
    async def _handle_status_request(self, message: Dict[str, Any]) -> None:
        """Handle status request message."""
        logger.info(f"{self.agent_id}: Received status request")
        
        # Create devlog for status request
        await auto_create_devlog(
            self.agent_id,
            "Status request received",
            "completed",
            {"requestor": message.get('from')}
        )
    
    async def _handle_general_message(self, message: Dict[str, Any]) -> None:
        """Handle general message."""
        logger.info(f"{self.agent_id}: Received general message")
        
        # Create devlog for general message
        await auto_create_devlog(
            self.agent_id,
            "General message received",
            "completed",
            {"sender": message.get('from'), "subject": message.get('subject')}
        )


