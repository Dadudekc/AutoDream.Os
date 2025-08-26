#!/usr/bin/env python3
"""
Extended Reporting Manager - Agent Cellphone V2
==============================================

Consolidated ReportingManager inheriting from BaseManager.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.core.base_manager import BaseManager


class ExtendedReportingManager(BaseManager):
    """Extended Reporting Manager - inherits from BaseManager for unified functionality"""
    
    def __init__(self, config_path: str = "config/reporting_manager.json"):
        super().__init__(
            manager_name="ExtendedReportingManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Initialize reporting-specific functionality
        self.task_manager = None
        self.reporting_templates = {}
        self.formatting_options = {}
        
        # Load reporting configuration
        self._load_reporting_config()
        
        logger.info("ExtendedReportingManager initialized successfully")
    
    def _load_reporting_config(self):
        """Load reporting-specific configuration"""
        try:
            if self.config:
                self.formatting_options = self.config.get("formatting", {})
                self.reporting_templates = self.config.get("templates", {})
        except Exception as e:
            logger.error(f"Error loading reporting config: {e}")
    
    def set_task_manager(self, task_manager):
        """Set the task manager reference"""
        self.task_manager = task_manager
        logger.info("Task manager reference set")
    
    def format_task_list_for_agents(self, tasks: List[Any]) -> str:
        """Format task list for agent review with proper formatting"""
        if not tasks:
            return "No tasks available for claiming."

        task_lines = []
        for task in sorted(tasks, key=lambda t: getattr(t, 'priority', 0), reverse=True):
            priority_icon = self._get_priority_icon(getattr(task, 'priority', 'normal'))
            complexity_icon = self._get_complexity_icon(getattr(task, 'complexity', 'medium'))

            task_lines.append(
                f"{priority_icon} **{getattr(task, 'title', 'Untitled')}** "
                f"(Priority: {getattr(task, 'priority', 'normal')})\n"
                f"   {complexity_icon} Complexity: {getattr(task, 'complexity', 'medium').title()}\n"
                f"   ⏱️ Estimated: {getattr(task, 'estimated_hours', 0)}h\n"
                f"   🎯 Skills: {', '.join(getattr(task, 'required_skills', []))}\n"
                f"   📝 {getattr(task, 'description', 'No description')}\n"
                f"   🆔 Task ID: {getattr(task, 'task_id', 'unknown')}\n"
            )

        return "\n".join(task_lines)
    
    def format_progress_summary(self) -> str:
        """Format progress summary for all agents"""
        if not self.task_manager:
            return "Task manager not available for progress summary."

        try:
            active_tasks = [
                t for t in self.task_manager.tasks.values()
                if getattr(t, 'status', '') in ["claimed", "in_progress"]
            ]

            if not active_tasks:
                return "No active tasks to report progress on."

            progress_lines = []
            for task in active_tasks:
                status_icon = self._get_status_icon(getattr(task, 'status', 'unknown'))
                progress_lines.append(
                    f"{status_icon} **{getattr(task, 'title', 'Untitled')}** "
                    f"(Agent: {getattr(task, 'claimed_by', 'Unknown')})\n"
                    f"   📊 Progress: {getattr(task, 'progress_percentage', 0):.1f}%\n"
                    f"   🚫 Blockers: {', '.join(getattr(task, 'blockers', [])) if getattr(task, 'blockers', []) else 'None'}\n"
                )

            return "\n".join(progress_lines)
        except Exception as e:
            logger.error(f"Error formatting progress summary: {e}")
            return f"Error generating progress summary: {e}"
    
    def format_cycle_summary(self) -> str:
        """Format cycle summary with comprehensive statistics"""
        if not self.task_manager:
            return "Task manager not available for cycle summary."

        try:
            summary = self.task_manager.get_task_summary()
            
            cycle_message = f"""🔄 CYCLE COMPLETE - SUMMARY:

📊 Task Status:
   • Total Tasks: {summary.get('total_tasks', 0)}
   • Available: {summary.get('available_tasks', 0)}
   • Claimed: {summary.get('claimed_tasks', 0)}
   • In Progress: {summary.get('in_progress_tasks', 0)}
   • Completed: {summary.get('completed_tasks', 0)}
   • Completion Rate: {summary.get('completion_rate', 0):.1f}%

⏰ Overnight Progress:
   • Cycles Completed: {summary.get('workflow_stats', {}).get('overnight_cycles', 0)}
   • Autonomous Hours: {summary.get('workflow_stats', {}).get('autonomous_hours', 0)}
   • Total Tasks Completed: {summary.get('workflow_stats', {}).get('total_tasks_completed', 0)}

🎯 Next Cycle: Task review and claiming phase begins..."""

            return cycle_message
        except Exception as e:
            logger.error(f"Error formatting cycle summary: {e}")
            return f"Error generating cycle summary: {e}"
    
    def format_workflow_start_message(self) -> str:
        """Format workflow start message"""
        return """🚀 AUTONOMOUS OVERNIGHT DEVELOPMENT WORKFLOW STARTED!

📋 AGENT-1: Task Manager Role
   - Building and updating task list
   - Managing task lifecycle and status
   - Coordinating with other agents

🎯 AGENT-2: Development Role  
   - Executing assigned development tasks
   - Code review and quality assurance
   - Progress reporting and updates

🔧 AGENT-3: Infrastructure Role
   - System health monitoring
   - Performance optimization
   - Technical debt management

📊 AGENT-4: Coordination Role
   - Workflow orchestration
   - Progress tracking and reporting
   - Agent communication management

🔄 Workflow Status: ACTIVE - All agents operational and ready for task assignment."""
    
    def _get_priority_icon(self, priority: str) -> str:
        """Get priority icon based on priority level"""
        priority_icons = {
            'critical': '🚨',
            'high': '🔴',
            'medium': '🟡',
            'normal': '🟢',
            'low': '🔵'
        }
        return priority_icons.get(priority.lower(), '⚪')
    
    def _get_complexity_icon(self, complexity: str) -> str:
        """Get complexity icon based on complexity level"""
        complexity_icons = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }
        return complexity_icons.get(complexity.lower(), '⚪')
    
    def _get_status_icon(self, status: str) -> str:
        """Get status icon based on status"""
        status_icons = {
            'claimed': '📋',
            'in_progress': '🔄',
            'completed': '✅',
            'failed': '❌',
            'blocked': '🚫'
        }
        return status_icons.get(status, '❓')
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get extended manager status including reporting metrics"""
        base_status = super().get_manager_status()
        
        # Add reporting-specific status
        reporting_status = {
            "task_manager_available": self.task_manager is not None,
            "formatting_options": len(self.formatting_options),
            "reporting_templates": len(self.reporting_templates),
            "last_report_generated": self.last_activity.isoformat()
        }
        
        base_status.update(reporting_status)
        return base_status
