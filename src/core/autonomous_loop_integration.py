#!/usr/bin/env python3
"""
Autonomous Loop Integration - Autonomous Agent Loop System
=========================================================

Integration module for autonomous loop mode with continuous autonomy behavior.
Part of the autonomous loop integration implementation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class AutonomousLoopIntegration:
    """Autonomous loop integration system for continuous agent autonomy."""
    
    def __init__(self, agent_id: str = "Agent-2") -> None:
        """Initialize autonomous loop integration."""
        self.agent_id = agent_id
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")
        self.inbox_path = self.workspace_path / "inbox"
        self.processed_path = self.inbox_path / "processed"
        self.working_tasks_path = self.workspace_path / "working_tasks.json"
        self.future_tasks_path = self.workspace_path / "future_tasks.json"
        
        # Ensure directories exist
        self.inbox_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        # Load current state
        self._load_working_tasks()
        self._load_future_tasks()
        
        logger.info(f"Autonomous loop integration initialized for {agent_id}")
    
    def _load_working_tasks(self) -> Dict[str, Any]:
        """Load working tasks from JSON file."""
        try:
            if self.working_tasks_path.exists():
                with open(self.working_tasks_path, 'r') as f:
                    self.working_tasks = json.load(f)
            else:
                self.working_tasks = {
                    "current_task": None,
                    "completed_tasks": [],
                    "available_tasks": []
                }
        except Exception as e:
            logger.error(f"Failed to load working tasks: {e}")
            self.working_tasks = {
                "current_task": None,
                "completed_tasks": [],
                "available_tasks": []
            }
        return self.working_tasks
    
    def _load_future_tasks(self) -> Dict[str, Any]:
        """Load future tasks from JSON file."""
        try:
            if self.future_tasks_path.exists():
                with open(self.future_tasks_path, 'r') as f:
                    self.future_tasks = json.load(f)
            else:
                self.future_tasks = {
                    "pending_tasks": [],
                    "completed_future_tasks": []
                }
        except Exception as e:
            logger.error(f"Failed to load future tasks: {e}")
            self.future_tasks = {
                "pending_tasks": [],
                "completed_future_tasks": []
            }
        return self.future_tasks
    
    def _save_working_tasks(self) -> bool:
        """Save working tasks to JSON file."""
        try:
            with open(self.working_tasks_path, 'w') as f:
                json.dump(self.working_tasks, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save working tasks: {e}")
            return False
    
    def _save_future_tasks(self) -> bool:
        """Save future tasks to JSON file."""
        try:
            with open(self.future_tasks_path, 'w') as f:
                json.dump(self.future_tasks, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save future tasks: {e}")
            return False
    
    def check_mailbox(self) -> List[Path]:
        """Check mailbox for unprocessed messages."""
        try:
            if not self.inbox_path.exists():
                return []
            
            messages = []
            for file_path in self.inbox_path.iterdir():
                if file_path.is_file() and file_path.suffix == '.md':
                    messages.append(file_path)
            
            logger.info(f"Found {len(messages)} unprocessed messages")
            return messages
        except Exception as e:
            logger.error(f"Failed to check mailbox: {e}")
            return []
    
    def process_message(self, message_path: Path) -> bool:
        """Process a single message and move it to processed folder."""
        try:
            # Read message content
            with open(message_path, 'r') as f:
                content = f.read()
            
            # Log message processing
            logger.info(f"Processing message: {message_path.name}")
            
            # Move to processed folder
            processed_path = self.processed_path / message_path.name
            message_path.rename(processed_path)
            
            logger.info(f"Message processed and moved to: {processed_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to process message {message_path}: {e}")
            return False
    
    def process_all_messages(self) -> Tuple[int, int]:
        """Process all unprocessed messages in mailbox."""
        messages = self.check_mailbox()
        processed_count = 0
        failed_count = 0
        
        for message_path in messages:
            if self.process_message(message_path):
                processed_count += 1
            else:
                failed_count += 1
        
        logger.info(f"Processed {processed_count} messages, {failed_count} failed")
        return processed_count, failed_count
    
    def get_current_task(self) -> Optional[Dict[str, Any]]:
        """Get current working task."""
        return self.working_tasks.get("current_task")
    
    def get_available_tasks(self) -> List[Dict[str, Any]]:
        """Get available tasks from working_tasks.json."""
        return self.working_tasks.get("available_tasks", [])
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get pending tasks from future_tasks.json."""
        return self.future_tasks.get("pending_tasks", [])
    
    def claim_task(self, task_id: str, source: str = "available") -> bool:
        """Claim a task and set it as current task."""
        try:
            task = None
            
            if source == "available":
                available_tasks = self.get_available_tasks()
                task = next((t for t in available_tasks if t["id"] == task_id), None)
                if task:
                    # Remove from available tasks
                    self.working_tasks["available_tasks"] = [
                        t for t in available_tasks if t["id"] != task_id
                    ]
            elif source == "pending":
                pending_tasks = self.get_pending_tasks()
                task = next((t for t in pending_tasks if t["id"] == task_id), None)
                if task:
                    # Remove from pending tasks
                    self.future_tasks["pending_tasks"] = [
                        t for t in pending_tasks if t["id"] != task_id
                    ]
            
            if not task:
                logger.error(f"Task {task_id} not found in {source} tasks")
                return False
            
            # Set as current task
            task["status"] = "in_progress"
            task["assigned_to"] = self.agent_id
            task["created_at"] = datetime.now().isoformat()
            task["updated_at"] = datetime.now().isoformat()
            
            # Move previous task to completed if exists
            if self.working_tasks.get("current_task"):
                if "completed_tasks" not in self.working_tasks:
                    self.working_tasks["completed_tasks"] = []
                self.working_tasks["completed_tasks"].append(self.working_tasks["current_task"])
            
            self.working_tasks["current_task"] = task
            
            # Save changes
            self._save_working_tasks()
            if source == "pending":
                self._save_future_tasks()
            
            logger.info(f"Successfully claimed task: {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to claim task {task_id}: {e}")
            return False
    
    def complete_task(self, task_id: str) -> bool:
        """Mark current task as completed."""
        try:
            current_task = self.get_current_task()
            if not current_task or current_task["id"] != task_id:
                logger.error(f"Task {task_id} is not the current task")
                return False
            
            # Update task status
            current_task["status"] = "completed"
            current_task["completed_at"] = datetime.now().isoformat()
            current_task["updated_at"] = datetime.now().isoformat()
            
            # Move to completed tasks
            if "completed_tasks" not in self.working_tasks:
                self.working_tasks["completed_tasks"] = []
            self.working_tasks["completed_tasks"].append(current_task)
            
            # Clear current task
            self.working_tasks["current_task"] = None
            
            # Save changes
            self._save_working_tasks()
            
            logger.info(f"Successfully completed task: {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to complete task {task_id}: {e}")
            return False
    
    def update_task_progress(self, task_id: str, phase: int, status: str) -> bool:
        """Update task progress for a specific phase."""
        try:
            current_task = self.get_current_task()
            if not current_task or current_task["id"] != task_id:
                logger.error(f"Task {task_id} is not the current task")
                return False
            
            # Update phase status
            if "phases" in current_task:
                for phase_obj in current_task["phases"]:
                    if phase_obj["phase"] == phase:
                        phase_obj["status"] = status
                        break
            
            current_task["updated_at"] = datetime.now().isoformat()
            
            # Save changes
            self._save_working_tasks()
            
            logger.info(f"Updated task {task_id} phase {phase} to {status}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update task progress: {e}")
            return False
    
    def autonomous_loop_cycle(self) -> Dict[str, Any]:
        """Execute one autonomous loop cycle."""
        cycle_start = datetime.now()
        cycle_results = {
            "messages_processed": 0,
            "messages_failed": 0,
            "current_task": None,
            "task_claimed": False,
            "task_completed": False,
            "cycle_duration": 0
        }
        
        try:
            # 1. Check and process mailbox
            processed, failed = self.process_all_messages()
            cycle_results["messages_processed"] = processed
            cycle_results["messages_failed"] = failed
            
            # 2. Check current task
            current_task = self.get_current_task()
            cycle_results["current_task"] = current_task
            
            # 3. If no current task, try to claim one
            if not current_task:
                # Try available tasks first
                available_tasks = self.get_available_tasks()
                if available_tasks:
                    task_to_claim = available_tasks[0]
                    if self.claim_task(task_to_claim["id"], "available"):
                        cycle_results["task_claimed"] = True
                        cycle_results["current_task"] = self.get_current_task()
                
                # If still no task, try pending tasks
                if not cycle_results["current_task"]:
                    pending_tasks = self.get_pending_tasks()
                    if pending_tasks:
                        task_to_claim = pending_tasks[0]
                        if self.claim_task(task_to_claim["id"], "pending"):
                            cycle_results["task_claimed"] = True
                            cycle_results["current_task"] = self.get_current_task()
            
            # 4. Calculate cycle duration
            cycle_end = datetime.now()
            cycle_results["cycle_duration"] = (cycle_end - cycle_start).total_seconds()
            
            logger.info(f"Autonomous loop cycle completed: {cycle_results}")
            return cycle_results
            
        except Exception as e:
            logger.error(f"Autonomous loop cycle failed: {e}")
            cycle_results["error"] = str(e)
            return cycle_results
