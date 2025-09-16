#!/usr/bin/env python3
"""
Mailbox Processor - Automated mailbox processing
===============================================

Handles automated processing of agent mailboxes including message scanning,
processing, and cleanup operations.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 compliance modularization
License: MIT
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Generator

from .automation_message import AutomationMessage

logger = logging.getLogger(__name__)


class MailboxProcessor:
    """Handles automated mailbox processing."""

    def __init__(self, agent_workspace: Path) -> None:
        """Initialize mailbox processor."""
        self.agent_workspace = agent_workspace
        self.inbox_path = agent_workspace / "inbox"
        self.processed_path = agent_workspace / "processed"
        self.working_tasks_path = agent_workspace / "working_tasks.json"
        self.future_tasks_path = agent_workspace / "future_tasks.json"

    def scan_mailbox(self) -> Generator[AutomationMessage, None, None]:
        """Scan mailbox for new messages."""
        if not self.inbox_path.exists():
            logger.warning(f"Inbox path does not exist: {self.inbox_path}")
            return

        for message_file in self.inbox_path.glob("*.md"):
            try:
                content = message_file.read_text(encoding="utf-8")
                metadata = self._extract_metadata(content)
                
                message = AutomationMessage(
                    file_path=message_file,
                    content=content,
                    metadata=metadata
                )
                
                if message.validate():
                    yield message
                else:
                    logger.warning(f"Invalid message: {message_file}")
                    
            except Exception as e:
                logger.error(f"Error processing message {message_file}: {e}")

    def process_message(self, message: AutomationMessage) -> str:
        """Process a single message."""
        try:
            # Extract task information from message
            task_info = self._extract_task_info(message.content)
            
            if task_info:
                # Update working tasks
                self._update_working_tasks(task_info)
                
                # Mark message as processed
                message.mark_processed("success")
                
                # Move to processed folder
                self._move_to_processed(message)
                
                return "success"
            else:
                message.mark_processed("no_task_found")
                return "no_task_found"
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            message.mark_processed("error")
            return "error"

    def process_all_messages(self) -> dict[str, int]:
        """Process all messages in mailbox."""
        results = {"success": 0, "error": 0, "no_task_found": 0}
        
        for message in self.scan_mailbox():
            result = self.process_message(message)
            results[result] += 1
            
        logger.info(f"Processed {sum(results.values())} messages: {results}")
        return results

    def _extract_metadata(self, content: str) -> dict[str, Any]:
        """Extract metadata from message content."""
        metadata = {}
        
        # Extract timestamp
        if "Timestamp:" in content:
            try:
                timestamp_line = [line for line in content.split('\n') if 'Timestamp:' in line][0]
                timestamp_str = timestamp_line.split('Timestamp:')[1].strip()
                metadata['timestamp'] = timestamp_str
            except (IndexError, ValueError):
                pass
        
        # Extract priority
        if "Priority:" in content:
            try:
                priority_line = [line for line in content.split('\n') if 'Priority:' in line][0]
                priority = priority_line.split('Priority:')[1].strip()
                metadata['priority'] = priority
            except (IndexError, ValueError):
                pass
        
        # Extract tags
        if "Tags:" in content:
            try:
                tags_line = [line for line in content.split('\n') if 'Tags:' in line][0]
                tags = tags_line.split('Tags:')[1].strip()
                metadata['tags'] = tags
            except (IndexError, ValueError):
                pass
        
        return metadata

    def _extract_task_info(self, content: str) -> dict[str, Any] | None:
        """Extract task information from message content."""
        # Look for task patterns in content
        if "MISSION:" in content or "TASK:" in content:
            return {
                "type": "mission",
                "content": content,
                "extracted_at": datetime.now().isoformat()
            }
        return None

    def _update_working_tasks(self, task_info: dict[str, Any]) -> None:
        """Update working tasks file."""
        try:
            if self.working_tasks_path.exists():
                with open(self.working_tasks_path, 'r', encoding='utf-8') as f:
                    tasks = json.load(f)
            else:
                tasks = {"current_task": None, "completed_tasks": []}
            
            # Add new task
            if not tasks.get("current_task"):
                tasks["current_task"] = task_info
            
            with open(self.working_tasks_path, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error updating working tasks: {e}")

    def _move_to_processed(self, message: AutomationMessage) -> None:
        """Move processed message to processed folder."""
        try:
            if not self.processed_path.exists():
                self.processed_path.mkdir(parents=True, exist_ok=True)
            
            processed_file = self.processed_path / message.file_path.name
            message.file_path.rename(processed_file)
            
        except Exception as e:
            logger.error(f"Error moving message to processed: {e}")

    def get_processing_stats(self) -> dict[str, Any]:
        """Get processing statistics."""
        stats = {
            "inbox_count": len(list(self.inbox_path.glob("*.md"))) if self.inbox_path.exists() else 0,
            "processed_count": len(list(self.processed_path.glob("*.md"))) if self.processed_path.exists() else 0,
            "has_working_task": self.working_tasks_path.exists(),
            "has_future_tasks": self.future_tasks_path.exists()
        }
        return stats
