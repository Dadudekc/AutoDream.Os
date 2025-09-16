#!/usr/bin/env python3
"""
Consolidated Automation System - Unified Automation Operations
=============================================================

Consolidated automation system combining:
- Mailbox processing automation
- Task claiming automation
- Process automation coordination

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 compliance modularization - consolidated automation system
License: MIT
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .automation import AutomationMessage, MailboxProcessor, TaskClaimer

logger = logging.getLogger(__name__)


class ConsolidatedAutomationSystem:
    """Unified automation system combining all automation components."""

    def __init__(self, agent_workspace: Path, agent_id: str) -> None:
        """Initialize consolidated automation system."""
        self.agent_workspace = agent_workspace
        self.agent_id = agent_id
        
        # Initialize components
        self.mailbox_processor = MailboxProcessor(agent_workspace)
        self.task_claimer = TaskClaimer(agent_workspace, agent_id)
        
        logger.info(f"Consolidated automation system initialized for {agent_id}")

    def run_automation_cycle(self) -> dict[str, Any]:
        """Run complete automation cycle."""
        results = {
            "mailbox_processing": {},
            "task_claiming": {},
            "overall_status": "success"
        }
        
        try:
            # Step 1: Process mailbox
            logger.info("Starting mailbox processing...")
            mailbox_results = self.mailbox_processor.process_all_messages()
            results["mailbox_processing"] = mailbox_results
            
            # Step 2: Claim tasks if needed
            if self.task_claimer.can_claim_task():
                logger.info("Attempting to claim new task...")
                claimed_task = self.task_claimer.auto_claim_task()
                if claimed_task:
                    results["task_claiming"] = {
                        "status": "task_claimed",
                        "task_id": claimed_task.get("id", "unknown")
                    }
                else:
                    results["task_claiming"] = {"status": "no_suitable_tasks"}
            else:
                results["task_claiming"] = {"status": "already_has_task"}
            
            logger.info("Automation cycle completed successfully")
            
        except Exception as e:
            logger.error(f"Error in automation cycle: {e}")
            results["overall_status"] = "error"
            results["error"] = str(e)
        
        return results

    def get_system_status(self) -> dict[str, Any]:
        """Get comprehensive system status."""
        status = {
            "agent_id": self.agent_id,
            "workspace": str(self.agent_workspace),
            "mailbox_stats": self.mailbox_processor.get_processing_stats(),
            "task_status": {
                "can_claim_task": self.task_claimer.can_claim_task(),
                "available_tasks": len(self.task_claimer.get_available_tasks())
            }
        }
        return status

    def process_single_message(self, message_file: Path) -> str:
        """Process a single message file."""
        try:
            content = message_file.read_text(encoding="utf-8")
            message = AutomationMessage(
                file_path=message_file,
                content=content
            )
            
            if message.validate():
                return self.mailbox_processor.process_message(message)
            else:
                return "invalid_message"
                
        except Exception as e:
            logger.error(f"Error processing single message: {e}")
            return "error"

    def claim_specific_task(self, task_id: str) -> bool:
        """Claim a specific task by ID."""
        try:
            available_tasks = self.task_claimer.get_available_tasks()
            target_task = None
            
            for task in available_tasks:
                if task.get("id") == task_id:
                    target_task = task
                    break
            
            if target_task:
                return self.task_claimer.claim_task(target_task)
            else:
                logger.warning(f"Task {task_id} not found in available tasks")
                return False
                
        except Exception as e:
            logger.error(f"Error claiming specific task: {e}")
            return False

    def complete_current_task(self, result: str = "completed") -> bool:
        """Complete the current task."""
        return self.task_claimer.complete_current_task(result)

    def get_processing_statistics(self) -> dict[str, Any]:
        """Get detailed processing statistics."""
        stats = self.mailbox_processor.get_processing_stats()
        stats.update({
            "agent_id": self.agent_id,
            "can_claim_task": self.task_claimer.can_claim_task(),
            "available_tasks_count": len(self.task_claimer.get_available_tasks())
        })
        return stats