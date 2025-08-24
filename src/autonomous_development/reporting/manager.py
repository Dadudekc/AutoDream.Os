#!/usr/bin/env python3
"""
Autonomous Development Reporting Manager
=======================================

This module handles reporting and status management for autonomous development.
Follows SRP by focusing solely on reporting and status formatting.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.utils.stability_improvements import stability_manager, safe_import
# Use type hints with strings to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.autonomous_development.core import DevelopmentTask
    from src.core.task_manager import DevelopmentTaskManager as TaskManager


class ReportingManager:
    """Manages reporting and status formatting for autonomous development"""

    def __init__(self, task_manager: "TaskManager"):
        self.task_manager = task_manager
        self.logger = logging.getLogger(__name__)

    def format_task_list_for_agents(self, tasks: List["DevelopmentTask"]) -> str:
        """Format task list for agent review with proper formatting"""
        if not tasks:
            return "No tasks available for claiming."

        task_lines = []
        for task in sorted(tasks, key=lambda t: t.priority, reverse=True):
            priority_icon = self._get_priority_icon(task.priority)
            complexity_icon = self._get_complexity_icon(task.complexity)

            task_lines.append(
                f"{priority_icon} **{task.title}** (Priority: {task.priority})\n"
                f"   {complexity_icon} Complexity: {task.complexity.title()}\n"
                f"   ⏱️ Estimated: {task.estimated_hours}h\n"
                f"   🎯 Skills: {', '.join(task.required_skills)}\n"
                f"   📝 {task.description}\n"
                f"   🆔 Task ID: {task.task_id}\n"
            )

        return "\n".join(task_lines)

    def format_progress_summary(self) -> str:
        """Format progress summary for all agents"""
        active_tasks = [
            t
            for t in self.task_manager.tasks.values()
            if t.status in ["claimed", "in_progress"]
        ]

        if not active_tasks:
            return "No active tasks to report progress on."

        progress_lines = []
        for task in active_tasks:
            status_icon = self._get_status_icon(task.status)
            progress_lines.append(
                f"{status_icon} **{task.title}** (Agent: {task.claimed_by})\n"
                f"   📊 Progress: {task.progress_percentage:.1f}%\n"
                f"   🚫 Blockers: {', '.join(task.blockers) if task.blockers else 'None'}\n"
            )

        return "\n".join(progress_lines)

    def format_cycle_summary(self) -> str:
        """Format cycle summary with comprehensive statistics"""
        summary = self.task_manager.get_task_summary()
        
        cycle_message = f"""🔄 CYCLE COMPLETE - SUMMARY:

📊 Task Status:
   • Total Tasks: {summary['total_tasks']}
   • Available: {summary['available_tasks']}
   • Claimed: {summary['claimed_tasks']}
   • In Progress: {summary['in_progress_tasks']}
   • Completed: {summary['completed_tasks']}
   • Completion Rate: {summary['completion_rate']:.1f}%

⏰ Overnight Progress:
   • Cycles Completed: {summary['workflow_stats']['overnight_cycles']}
   • Autonomous Hours: {summary['workflow_stats']['autonomous_hours']}
   • Total Tasks Completed: {summary['workflow_stats']['total_tasks_completed']}

🎯 Next Cycle: Task review and claiming phase begins..."""

        return cycle_message

    def format_workflow_start_message(self) -> str:
        """Format workflow start message"""
        return """🚀 AUTONOMOUS OVERNIGHT DEVELOPMENT WORKFLOW STARTED!

📋 AGENT-1: Task Manager Role
   - Building and updating task list
   - Monitoring progress and coordination
   - Managing task priorities

🔍 AGENTS 2-8: Autonomous Workforce
   - Review available tasks
   - Claim tasks based on skills and availability
   - Work autonomously and report progress
   - Complete tasks and claim new ones

🔄 WORKFLOW CYCLE:
   1. Task review and claiming
   2. Autonomous work execution
   3. Progress reporting
   4. Task completion and new task claiming
   5. Repeat cycle

⏰ CYCLE DURATION: 1 hour
🌙 OPERATION: Continuous overnight
🎯 GOAL: Maximize autonomous development progress

Ready to begin autonomous development! 🚀"""

    def format_agent1_message(self) -> str:
        """Format special message for Agent-1"""
        return """🎯 AGENT-1: You are now the Task Manager!

Your responsibilities:
1. 📋 Monitor task list and create new tasks as needed
2. 📊 Track progress and identify bottlenecks
3. 🔄 Coordinate workflow and resolve conflicts
4. 📈 Optimize task distribution and priorities
5. 🚨 Handle emergencies and blocked tasks

Start by reviewing the current task list and identifying areas for improvement!"""

    def format_no_tasks_message(self) -> str:
        """Format message when no tasks are available"""
        return """📋 NO TASKS AVAILABLE

🎯 All current tasks have been claimed or completed!
⏰ Waiting for Agent-1 to create new tasks...

🔄 Next cycle will focus on:
   • Progress monitoring
   • Task completion
   • New task creation by Agent-1

Stay ready for new development opportunities! 🚀"""

    def format_task_claimed_message(self, task: "DevelopmentTask") -> str:
        """Format message when a task is claimed"""
        return f"""🎯 TASK CLAIMED: {task.title}

📋 Task Details:
   • ID: {task.task_id}
   • Priority: {task.priority}
   • Complexity: {task.complexity}
   • Estimated Time: {task.estimated_hours}h
   • Required Skills: {', '.join(task.required_skills)}

🚀 Status: Ready to start work
⏰ Next: Begin task execution in next cycle

Good luck with your autonomous development! 🚀"""

    def format_progress_update_message(self, task: "DevelopmentTask", new_progress: float, blockers: List[str] = None) -> str:
        """Format progress update message for an agent"""
        if blockers:
            return f"""⚠️ PROGRESS UPDATE - BLOCKERS DETECTED

📊 Task: {task.title}
📈 Progress: {new_progress:.1f}%
🚫 Blockers: {', '.join(blockers)}

🔧 Action Required: Address blockers before continuing
⏰ Next Update: In next cycle"""
        else:
            return f"""📊 PROGRESS UPDATE

📋 Task: {task.title}
📈 Progress: {new_progress:.1f}%
✅ Status: Making good progress

🚀 Continue autonomous development!
⏰ Next Update: In next cycle"""

    def format_workflow_complete_message(self) -> str:
        """Format final workflow completion message"""
        summary = self.task_manager.get_task_summary()
        stats = summary["workflow_stats"]
        
        return f"""🌅 OVERNIGHT WORKFLOW COMPLETE

📊 Final Summary:
   • Total Cycles: {stats['overnight_cycles']}
   • Autonomous Hours: {stats['autonomous_hours']}
   • Tasks Completed: {stats['total_tasks_completed']}

🎯 Great work on autonomous development!
🔄 System ready for next overnight session

Good morning! ☀️"""

    def format_remaining_tasks_message(self, remaining_count: int) -> str:
        """Format message about remaining available tasks"""
        return f"📋 {remaining_count} tasks still available for claiming in next cycle."

    def format_detailed_task_status(self) -> str:
        """Format detailed task status for CLI display"""
        summary = self.task_manager.get_task_summary()
        
        status_lines = [
            "📋 Current Development Task Status:",
            "=" * 60,
            f"Total Tasks: {summary['total_tasks']}",
            f"Available: {summary['available_tasks']}",
            f"Claimed: {summary['claimed_tasks']}",
            f"In Progress: {summary['in_progress_tasks']}",
            f"Completed: {summary['completed_tasks']}",
            f"Completion Rate: {summary['completion_rate']:.1f}%",
            "",
            "📊 Detailed Task List:"
        ]

        # Add individual task details
        for task in self.task_manager.tasks.values():
            status_icon = self._get_status_icon(task.status)
            status_lines.append(f"{status_icon} {task.task_id}: {task.title}")
            status_lines.append(f"   Status: {task.status}")
            if task.claimed_by:
                status_lines.append(f"   Agent: {task.claimed_by}")
            if task.progress_percentage > 0:
                status_lines.append(f"   Progress: {task.progress_percentage:.1f}%")
            status_lines.append("")

        return "\n".join(status_lines)

    def format_workflow_statistics(self) -> str:
        """Format workflow statistics for CLI display"""
        summary = self.task_manager.get_task_summary()
        stats = summary["workflow_stats"]
        
        status_lines = [
            "📊 Autonomous Development Workflow Statistics:",
            "=" * 60,
            "📋 Task Statistics:",
            f"   Total Tasks Created: {stats['total_tasks_created']}",
            f"   Total Tasks Completed: {stats['total_tasks_completed']}",
            f"   Total Tasks Claimed: {stats['total_tasks_claimed']}",
            "",
            "🌙 Overnight Statistics:",
            f"   Overnight Cycles: {stats['overnight_cycles']}",
            f"   Autonomous Hours: {stats['autonomous_hours']}"
        ]

        if stats["total_tasks_created"] > 0:
            completion_rate = (
                stats["total_tasks_completed"] / stats["total_tasks_created"]
            ) * 100
            status_lines.append(f"   Overall Completion Rate: {completion_rate:.1f}%")

        return "\n".join(status_lines)

    def _get_priority_icon(self, priority: int) -> str:
        """Get appropriate icon for task priority"""
        if priority >= 8:
            return "🔴"
        elif priority >= 5:
            return "🟡"
        else:
            return "🟢"

    def _get_complexity_icon(self, complexity: str) -> str:
        """Get appropriate icon for task complexity"""
        if complexity == "high":
            return "🔥"
        elif complexity == "medium":
            return "⚡"
        else:
            return "💡"

    def _get_status_icon(self, status: str) -> str:
        """Get appropriate icon for task status"""
        status_icons = {
            "available": "🟢",
            "claimed": "🟡",
            "in_progress": "🔄",
            "completed": "✅",
            "blocked": "🚫",
        }
        return status_icons.get(status, "❓")

    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        try:
            summary = self.task_manager.get_task_summary()
            stats = summary["workflow_stats"]
            
            # Calculate additional metrics
            total_tasks = summary["total_tasks"]
            completed_tasks = summary["completed_tasks"]
            
            efficiency_score = 0.0
            if total_tasks > 0:
                efficiency_score = (completed_tasks / total_tasks) * 100
            
            avg_cycle_efficiency = 0.0
            if stats["overnight_cycles"] > 0:
                avg_cycle_efficiency = completed_tasks / stats["overnight_cycles"]
            
            return {
                "summary": summary,
                "workflow_stats": stats,
                "performance_metrics": {
                    "efficiency_score": efficiency_score,
                    "avg_cycle_efficiency": avg_cycle_efficiency,
                    "task_completion_rate": summary["completion_rate"],
                    "autonomous_productivity": completed_tasks / max(stats["autonomous_hours"], 1),
                }
            }
        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            return {}
