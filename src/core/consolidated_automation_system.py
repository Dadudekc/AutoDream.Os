#!/usr/bin/env python3
"""
Consolidated Automation System - Unified Automation Operations
=============================================================

Consolidated automation system combining:
- Mailbox processing automation
- Task claiming automation
- Process automation coordination

Author: Agent-8 (Operations Specialist)
Mission: TASK 1 - Operations consolidation for Phase 2 system integration
License: MIT
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


class AutomationMessage:
    """Represents an automation message."""
    
    def __init__(self, file_path: Path, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Initialize automation message."""
        self.file_path = file_path
        self.content = content
        self.metadata = metadata or {}
        self.processed_at = None
        self.processing_result = None
    
    def mark_processed(self, result: str = "success") -> None:
        """Mark message as processed."""
        self.processed_at = datetime.now()
        self.processing_result = result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "file_path": str(self.file_path),
            "content": self.content,
            "metadata": self.metadata,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "processing_result": self.processing_result
        }


class AutomationTask:
    """Represents an automation task."""
    
    def __init__(self, task_data: Dict[str, Any]) -> None:
        """Initialize task from data dictionary."""
        self.id = task_data.get("id", "")
        self.description = task_data.get("description", "")
        self.status = task_data.get("status", "pending")
        self.assigned_to = task_data.get("assigned_to", "")
        self.priority = task_data.get("priority", "medium")
        self.created_at = task_data.get("created_at", "")
        self.updated_at = task_data.get("updated_at", "")
        self.completed_at = task_data.get("completed_at", "")
        self.phases = task_data.get("phases", [])
        self.dependencies = task_data.get("dependencies", [])
        self.estimated_duration = task_data.get("estimated_duration", "")
        self.created_by = task_data.get("created_by", "")
    
    def is_claimable(self) -> bool:
        """Check if task is claimable."""
        return (
            self.status == "available" or 
            self.status == "pending" and not self.assigned_to
        )
    
    def can_be_claimed_by(self, agent_id: str) -> bool:
        """Check if task can be claimed by specific agent."""
        return (
            self.is_claimable() and
            (not self.assigned_to or self.assigned_to == agent_id)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed_at": self.completed_at,
            "phases": self.phases,
            "dependencies": self.dependencies,
            "estimated_duration": self.estimated_duration,
            "created_by": self.created_by
        }


class ConsolidatedAutomationSystem:
    """Consolidated automation system for mailbox processing and task claiming."""
    
    def __init__(self, agent_id: str = "Agent-8") -> None:
        """Initialize consolidated automation system."""
        self.agent_id = agent_id
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")
        self.inbox_path = self.workspace_path / "inbox"
        self.processed_path = self.workspace_path / "inbox" / "processed"
        self.working_tasks_path = self.workspace_path / "working_tasks.json"
        self.future_tasks_path = self.workspace_path / "future_tasks.json"
        
        # Ensure directories exist
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        # Automation metrics
        self.metrics = {
            "total_messages_processed": 0,
            "successful_message_processing": 0,
            "failed_message_processing": 0,
            "total_claims_attempted": 0,
            "successful_claims": 0,
            "failed_claims": 0,
            "last_processing": None,
            "processing_history": []
        }
        
        logger.info(f"Consolidated automation system initialized for {agent_id}")
    
    # Message Processing Methods
    def scan_inbox(self) -> List[AutomationMessage]:
        """Scan inbox for unprocessed messages."""
        messages = []
        
        try:
            if not self.inbox_path.exists():
                logger.info("Inbox directory does not exist")
                return messages
            
            # Find all message files (not in processed subdirectory)
            for file_path in self.inbox_path.iterdir():
                if file_path.is_file() and file_path.parent.name == "inbox":
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        messages.append(AutomationMessage(file_path, content))
                    except Exception as e:
                        logger.error(f"Failed to read message file {file_path}: {e}")
            
            logger.info(f"Found {len(messages)} unprocessed messages in inbox")
            return messages
            
        except Exception as e:
            logger.error(f"Failed to scan inbox: {e}")
            return []
    
    def process_message(self, message: AutomationMessage) -> bool:
        """Process a single automation message."""
        try:
            # Extract message information
            message_info = self._extract_message_info(message.content)
            
            # Process based on message type
            if message_info["type"] == "A2A":
                result = self._process_a2a_message(message, message_info)
            elif message_info["type"] == "DIRECTIVE":
                result = self._process_directive_message(message, message_info)
            elif message_info["type"] == "COORDINATION":
                result = self._process_coordination_message(message, message_info)
            else:
                result = self._process_generic_message(message, message_info)
            
            # Mark as processed
            message.mark_processed("success" if result else "failed")
            
            # Move to processed directory
            if result:
                self._move_to_processed(message)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to process message {message.file_path}: {e}")
            message.mark_processed("error")
            return False
    
    def _extract_message_info(self, content: str) -> Dict[str, Any]:
        """Extract information from message content."""
        info = {
            "type": "UNKNOWN",
            "from_agent": None,
            "to_agent": None,
            "priority": "NORMAL",
            "tags": [],
            "subject": None,
            "body": content
        }
        
        try:
            lines = content.split('\n')
            
            # Look for A2A message format
            if "[A2A] MESSAGE" in content:
                info["type"] = "A2A"
                
                for line in lines:
                    if line.startswith("FROM:"):
                        info["from_agent"] = line.replace("FROM:", "").strip()
                    elif line.startswith("TO:"):
                        info["to_agent"] = line.replace("TO:", "").strip()
                    elif line.startswith("Priority:"):
                        info["priority"] = line.replace("Priority:", "").strip()
                    elif line.startswith("Tags:"):
                        tags_str = line.replace("Tags:", "").strip()
                        info["tags"] = [tag.strip() for tag in tags_str.split()] if tags_str else []
            
            # Look for directive patterns
            elif any(keyword in content.upper() for keyword in ["DIRECTIVE", "REQUEST", "COMMAND"]):
                info["type"] = "DIRECTIVE"
            
            # Look for coordination patterns
            elif any(keyword in content.upper() for keyword in ["COORDINATION", "COLLABORATION", "SUPPORT"]):
                info["type"] = "COORDINATION"
            
        except Exception as e:
            logger.error(f"Failed to extract message info: {e}")
        
        return info
    
    def _process_a2a_message(self, message: AutomationMessage, info: Dict[str, Any]) -> bool:
        """Process A2A message."""
        try:
            logger.info(f"Processing A2A message from {info['from_agent']} to {info['to_agent']}")
            
            # Log message details
            logger.info(f"Priority: {info['priority']}, Tags: {info['tags']}")
            
            # Extract key information for processing
            content_summary = self._summarize_content(info['body'])
            logger.info(f"Message summary: {content_summary}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to process A2A message: {e}")
            return False
    
    def _process_directive_message(self, message: AutomationMessage, info: Dict[str, Any]) -> bool:
        """Process directive message."""
        try:
            logger.info("Processing directive message")
            
            # Extract directive details
            content_summary = self._summarize_content(info['body'])
            logger.info(f"Directive summary: {content_summary}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to process directive message: {e}")
            return False
    
    def _process_coordination_message(self, message: AutomationMessage, info: Dict[str, Any]) -> bool:
        """Process coordination message."""
        try:
            logger.info("Processing coordination message")
            
            # Extract coordination details
            content_summary = self._summarize_content(info['body'])
            logger.info(f"Coordination summary: {content_summary}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to process coordination message: {e}")
            return False
    
    def _process_generic_message(self, message: AutomationMessage, info: Dict[str, Any]) -> bool:
        """Process generic message."""
        try:
            logger.info("Processing generic message")
            
            # Generic processing for unknown message types
            content_summary = self._summarize_content(info['body'])
            logger.info(f"Generic message summary: {content_summary}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to process generic message: {e}")
            return False
    
    def _summarize_content(self, content: str) -> str:
        """Summarize message content."""
        try:
            # Simple summarization - take first 100 characters
            summary = content.strip()[:100]
            if len(content) > 100:
                summary += "..."
            return summary
        except Exception:
            return "Unable to summarize content"
    
    def _move_to_processed(self, message: AutomationMessage) -> None:
        """Move message to processed directory."""
        try:
            processed_file = self.processed_path / message.file_path.name
            message.file_path.rename(processed_file)
            logger.info(f"Moved {message.file_path.name} to processed directory")
        except Exception as e:
            logger.error(f"Failed to move message to processed: {e}")
    
    # Task Management Methods
    def _load_working_tasks(self) -> Optional[Dict[str, Any]]:
        """Load working tasks from JSON file."""
        try:
            if self.working_tasks_path.exists():
                with open(self.working_tasks_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Failed to load working tasks: {e}")
            return None
    
    def _save_working_tasks(self, data: Dict[str, Any]) -> bool:
        """Save working tasks to JSON file."""
        try:
            with open(self.working_tasks_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save working tasks: {e}")
            return False
    
    def _load_future_tasks(self) -> Optional[Dict[str, Any]]:
        """Load future tasks from JSON file."""
        try:
            if self.future_tasks_path.exists():
                with open(self.future_tasks_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Failed to load future tasks: {e}")
            return None
    
    def _save_future_tasks(self, data: Dict[str, Any]) -> bool:
        """Save future tasks to JSON file."""
        try:
            with open(self.future_tasks_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save future tasks: {e}")
            return False
    
    def get_current_task(self) -> Optional[AutomationTask]:
        """Get current task from working tasks."""
        try:
            working_tasks = self._load_working_tasks()
            if not working_tasks:
                return None
            
            current_task_data = working_tasks.get("current_task")
            if not current_task_data:
                return None
            
            return AutomationTask(current_task_data)
            
        except Exception as e:
            logger.error(f"Failed to get current task: {e}")
            return None
    
    def has_current_task(self) -> bool:
        """Check if agent has a current task."""
        current_task = self.get_current_task()
        return current_task is not None and current_task.status in ["in_progress", "pending"]
    
    def get_available_tasks(self) -> List[AutomationTask]:
        """Get all available tasks from future tasks."""
        try:
            future_tasks = self._load_future_tasks()
            if not future_tasks:
                return []
            
            available_tasks = []
            pending_tasks = future_tasks.get("pending_tasks", [])
            
            for task_data in pending_tasks:
                task = AutomationTask(task_data)
                if task.can_be_claimed_by(self.agent_id):
                    available_tasks.append(task)
            
            return available_tasks
            
        except Exception as e:
            logger.error(f"Failed to get available tasks: {e}")
            return []
    
    def _validate_task_dependencies(self, task: AutomationTask) -> bool:
        """Validate that task dependencies are met."""
        try:
            if not task.dependencies:
                return True
            
            working_tasks = self._load_working_tasks()
            if not working_tasks:
                return False
            
            completed_task_ids = {t.get("id", "") for t in working_tasks.get("completed_tasks", [])}
            return all(dep in completed_task_ids for dep in task.dependencies)
            
        except Exception as e:
            logger.error(f"Failed to validate task dependencies: {e}")
            return False
    
    def _select_best_task(self, available_tasks: List[AutomationTask]) -> Optional[AutomationTask]:
        """Select the best task from available tasks based on priority and other factors."""
        try:
            if not available_tasks:
                return None
            
            # Filter tasks with met dependencies
            valid_tasks = [task for task in available_tasks if self._validate_task_dependencies(task)]
            
            if not valid_tasks:
                logger.info("No tasks with met dependencies available")
                return None
            
            # Sort by priority (high > medium > low)
            priority_order = {"high": 3, "medium": 2, "low": 1}
            
            def task_score(task: AutomationTask) -> tuple:
                priority_score = priority_order.get(task.priority.lower(), 1)
                # Prefer tasks created by self
                creator_bonus = 2 if task.created_by == self.agent_id else 1
                return (priority_score, creator_bonus, task.id)
            
            best_task = max(valid_tasks, key=task_score)
            logger.info(f"Selected best task: {best_task.id} (priority: {best_task.priority})")
            
            return best_task
            
        except Exception as e:
            logger.error(f"Failed to select best task: {e}")
            return None
    
    def claim_task(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Claim a task from available tasks."""
        claim_start = datetime.now()
        
        try:
            # Check if already has a current task
            if self.has_current_task():
                current_task = self.get_current_task()
                return {
                    "success": False,
                    "message": f"Already has current task: {current_task.id if current_task else 'unknown'}",
                    "task_id": None,
                    "timestamp": claim_start.isoformat()
                }
            
            # Get available tasks
            available_tasks = self.get_available_tasks()
            
            if not available_tasks:
                return {
                    "success": False,
                    "message": "No available tasks to claim",
                    "task_id": None,
                    "timestamp": claim_start.isoformat()
                }
            
            # Select task to claim
            if task_id:
                # Claim specific task
                selected_task = None
                for task in available_tasks:
                    if task.id == task_id:
                        selected_task = task
                        break
                
                if not selected_task:
                    return {
                        "success": False,
                        "message": f"Task {task_id} not available for claiming",
                        "task_id": None,
                        "timestamp": claim_start.isoformat()
                    }
            else:
                # Auto-select best task
                selected_task = self._select_best_task(available_tasks)
                if not selected_task:
                    return {
                        "success": False,
                        "message": "No suitable task found for auto-claiming",
                        "task_id": None,
                        "timestamp": claim_start.isoformat()
                    }
            
            # Validate dependencies
            if not self._validate_task_dependencies(selected_task):
                return {
                    "success": False,
                    "message": f"Task {selected_task.id} dependencies not met",
                    "task_id": selected_task.id,
                    "timestamp": claim_start.isoformat()
                }
            
            # Claim the task
            success = self._execute_task_claim(selected_task)
            
            # Update metrics
            self.metrics["total_claims_attempted"] += 1
            if success:
                self.metrics["successful_claims"] += 1
            else:
                self.metrics["failed_claims"] += 1
            
            self.metrics["last_processing"] = claim_start.isoformat()
            
            result = {
                "success": success,
                "message": f"Task {selected_task.id} {'claimed' if success else 'claim failed'}",
                "task_id": selected_task.id,
                "task_description": selected_task.description,
                "timestamp": claim_start.isoformat()
            }
            
            # Store in history
            self.metrics["processing_history"].append(result)
            
            # Limit history size
            if len(self.metrics["processing_history"]) > 100:
                self.metrics["processing_history"] = self.metrics["processing_history"][-100:]
            
            return result
            
        except Exception as e:
            logger.error(f"Task claiming failed: {e}")
            self.metrics["total_claims_attempted"] += 1
            self.metrics["failed_claims"] += 1
            
            return {
                "success": False,
                "message": f"Task claiming error: {e}",
                "task_id": None,
                "timestamp": claim_start.isoformat()
            }
    
    def _execute_task_claim(self, task: AutomationTask) -> bool:
        """Execute the actual task claiming process."""
        try:
            # Load current working tasks
            working_tasks = self._load_working_tasks()
            if not working_tasks:
                return False
            
            # Load future tasks
            future_tasks = self._load_future_tasks()
            if not future_tasks:
                return False
            
            # Update task status
            task.status = "in_progress"
            task.assigned_to = self.agent_id
            task.updated_at = datetime.now().isoformat()
            
            # Add phases if not present
            if not task.phases:
                task.phases = [
                    {"phase": 1, "description": f"Phase 1: {task.description}", "status": "in_progress"},
                    {"phase": 2, "description": f"Phase 2: {task.description}", "status": "pending"},
                    {"phase": 3, "description": f"Phase 3: {task.description}", "status": "pending"}
                ]
            
            # Move current task to previous task if exists
            current_task = working_tasks.get("current_task")
            if current_task:
                working_tasks["previous_task"] = current_task
            
            # Set new current task
            working_tasks["current_task"] = task.to_dict()
            
            # Remove task from future tasks
            pending_tasks = future_tasks.get("pending_tasks", [])
            future_tasks["pending_tasks"] = [
                t for t in pending_tasks if t.get("id") != task.id
            ]
            
            # Save both files
            working_saved = self._save_working_tasks(working_tasks)
            future_saved = self._save_future_tasks(future_tasks)
            
            if working_saved and future_saved:
                logger.info(f"Successfully claimed task: {task.id}")
                return True
            else:
                logger.error("Failed to save task claiming changes")
                return False
            
        except Exception as e:
            logger.error(f"Failed to execute task claim: {e}")
            return False
    
    # Combined Processing Methods
    def process_all_messages(self) -> Dict[str, Any]:
        """Process all messages in inbox."""
        processing_start = datetime.now()
        
        try:
            # Scan for messages
            messages = self.scan_inbox()
            
            if not messages:
                logger.info("No messages to process")
                return {
                    "success": True,
                    "messages_processed": 0,
                    "processing_duration": 0,
                    "timestamp": processing_start.isoformat()
                }
            
            # Process each message
            processed_count = 0
            failed_count = 0
            
            for message in messages:
                success = self.process_message(message)
                if success:
                    processed_count += 1
                else:
                    failed_count += 1
            
            # Update metrics
            self.metrics["total_messages_processed"] += processed_count + failed_count
            self.metrics["successful_message_processing"] += processed_count
            self.metrics["failed_message_processing"] += failed_count
            self.metrics["last_processing"] = processing_start.isoformat()
            
            # Calculate duration
            processing_duration = (datetime.now() - processing_start).total_seconds()
            
            result = {
                "success": True,
                "messages_processed": processed_count,
                "messages_failed": failed_count,
                "total_messages": len(messages),
                "processing_duration": processing_duration,
                "timestamp": processing_start.isoformat()
            }
            
            # Store in history
            self.metrics["processing_history"].append(result)
            
            # Limit history size
            if len(self.metrics["processing_history"]) > 100:
                self.metrics["processing_history"] = self.metrics["processing_history"][-100:]
            
            logger.info(f"Processing complete: {processed_count} processed, {failed_count} failed")
            return result
            
        except Exception as e:
            logger.error(f"Failed to process messages: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": processing_start.isoformat()
            }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get automation metrics."""
        return self.metrics.copy()
    
    def generate_report(self) -> str:
        """Generate automation report."""
        report = f"""CONSOLIDATED AUTOMATION SYSTEM REPORT - {self.agent_id}
============================================================
📊 MESSAGE PROCESSING:
   Total Processed: {self.metrics['total_messages_processed']}
   ✅ Successful: {self.metrics['successful_message_processing']}
   ❌ Failed: {self.metrics['failed_message_processing']}

📊 TASK CLAIMING:
   Total Claims Attempted: {self.metrics['total_claims_attempted']}
   ✅ Successful Claims: {self.metrics['successful_claims']}
   ❌ Failed Claims: {self.metrics['failed_claims']}

⏰ Last Processing: {self.metrics['last_processing'] or 'Never'}
📁 Inbox Path: {self.inbox_path}
📁 Processed Path: {self.processed_path}
📁 Working Tasks: {self.working_tasks_path}
📁 Future Tasks: {self.future_tasks_path}
============================================================"""
        
        return report


# Global instance for convenience
_global_automation_system = None


def get_consolidated_automation_system(agent_id: str = "Agent-8") -> ConsolidatedAutomationSystem:
    """Get global consolidated automation system."""
    global _global_automation_system
    if _global_automation_system is None:
        _global_automation_system = ConsolidatedAutomationSystem(agent_id)
    return _global_automation_system


if __name__ == '__main__':
    # Test the consolidated automation system
    automation = get_consolidated_automation_system("Agent-8")
    
    # Process messages
    message_result = automation.process_all_messages()
    logger.info(f"Message processing result: {message_result}")
    
    # Try to claim a task
    claim_result = automation.claim_task()
    logger.info(f"Task claiming result: {claim_result}")
    
    # Generate report
    report = automation.generate_report()
    logger.info(f"Automation report:\n{report}")
