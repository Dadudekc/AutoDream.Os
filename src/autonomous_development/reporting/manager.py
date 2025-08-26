#!/usr/bin/env python3
"""
Autonomous Development Reporting Manager
=======================================

This module handles reporting and status management for autonomous development.
Follows SRP by focusing solely on reporting and status formatting.
Now inherits from BaseManager for unified functionality.

V2 Standards: ≤200 LOC, SRP, OOP principles, BaseManager inheritance
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.utils.stability_improvements import stability_manager, safe_import
from src.core.base_manager import BaseManager, ManagerStatus, ManagerPriority

# Use type hints with strings to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.autonomous_development.core import DevelopmentTask
    from src.core.task_manager import DevelopmentTaskManager as TaskManager


class ReportingManager(BaseManager):
    """
    Manages reporting and status formatting for autonomous development
    
    Now inherits from BaseManager for unified functionality
    """

    def __init__(self, task_manager: "TaskManager"):
        """Initialize reporting manager with BaseManager"""
        super().__init__(
            manager_id="reporting_manager",
            name="Reporting Manager",
            description="Manages reporting and status formatting for autonomous development"
        )
        
        self.task_manager = task_manager
        
        # Reporting tracking
        self.reports_generated: int = 0
        self.last_report_time: Optional[datetime] = None
        self.report_history: List[Dict[str, Any]] = []
        
        self.logger.info("Reporting Manager initialized")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize reporting system"""
        try:
            self.logger.info("Starting Reporting Manager...")
            
            # Clear reporting data
            self.reports_generated = 0
            self.last_report_time = None
            self.report_history.clear()
            
            self.logger.info("Reporting Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Reporting Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup reporting system"""
        try:
            self.logger.info("Stopping Reporting Manager...")
            
            # Save report history
            self._save_report_history()
            
            # Clear data
            self.report_history.clear()
            
            self.logger.info("Reporting Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Reporting Manager: {e}")
    
    def _on_heartbeat(self):
        """Reporting manager heartbeat"""
        try:
            # Check for new reports needed
            self._check_reporting_needs()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize reporting resources"""
        try:
            # Initialize data structures
            self.reports_generated = 0
            self.last_report_time = None
            self.report_history = []
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup reporting resources"""
        try:
            # Clear data
            self.report_history.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reset reporting state
            self.reports_generated = 0
            self.last_report_time = None
            
            # Clear report history
            self.report_history.clear()
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Reporting Management Methods
    # ============================================================================
    
    def format_task_list_for_agents(self, tasks: List["DevelopmentTask"]) -> str:
        """Format task list for agent review with proper formatting"""
        try:
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

            # Record operation
            self.record_operation("format_task_list", True, 0.0)
            
            return "\n".join(task_lines)
            
        except Exception as e:
            self.logger.error(f"Failed to format task list: {e}")
            self.record_operation("format_task_list", False, 0.0)
            return "Error formatting task list"

    def format_progress_summary(self) -> str:
        """Format progress summary for all agents"""
        try:
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

            # Record operation
            self.record_operation("format_progress_summary", True, 0.0)
            
            return "\n".join(progress_lines)
            
        except Exception as e:
            self.logger.error(f"Failed to format progress summary: {e}")
            self.record_operation("format_progress_summary", False, 0.0)
            return "Error formatting progress summary"

    def format_cycle_summary(self) -> str:
        """Format cycle summary with comprehensive statistics"""
        try:
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

            # Record operation
            self.record_operation("format_cycle_summary", True, 0.0)
            
            return cycle_message
            
        except Exception as e:
            self.logger.error(f"Failed to format cycle summary: {e}")
            self.record_operation("format_cycle_summary", False, 0.0)
            return "Error formatting cycle summary"

    def format_workflow_start_message(self) -> str:
        """Format workflow start message"""
        try:
            message = """🚀 AUTONOMOUS OVERNIGHT DEVELOPMENT WORKFLOW STARTED!

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

            # Record operation
            self.record_operation("format_workflow_start", True, 0.0)
            
            return message
            
        except Exception as e:
            self.logger.error(f"Failed to format workflow start message: {e}")
            self.record_operation("format_workflow_start", False, 0.0)
            return "Error formatting workflow start message"

    def format_agent1_message(self) -> str:
        """Format special message for Agent-1"""
        try:
            message = """🎯 AGENT-1: You are now the Task Manager!

Your responsibilities:
1. 📋 Monitor task list and create new tasks as needed
2. 📊 Track progress and identify bottlenecks
3. 🔄 Coordinate workflow and resolve conflicts
4. 📈 Optimize task distribution and priorities
5. 🚨 Handle emergencies and blocked tasks

Start by reviewing the current task list and identifying areas for improvement!"""

            # Record operation
            self.record_operation("format_agent1_message", True, 0.0)
            
            return message
            
        except Exception as e:
            self.logger.error(f"Failed to format Agent-1 message: {e}")
            self.record_operation("format_agent1_message", False, 0.0)
            return "Error formatting Agent-1 message"

    def format_no_tasks_message(self) -> str:
        """Format message when no tasks are available"""
        try:
            message = """📋 NO TASKS AVAILABLE

🎯 All current tasks have been claimed or completed!
⏰ Waiting for Agent-1 to create new tasks...

🔄 Next cycle will focus on:
   • Progress monitoring
   • Task completion
   • New task creation by Agent-1

Stay ready for new development opportunities! 🚀"""

            # Record operation
            self.record_operation("format_no_tasks_message", True, 0.0)
            
            return message
            
        except Exception as e:
            self.logger.error(f"Failed to format no tasks message: {e}")
            self.record_operation("format_no_tasks_message", False, 0.0)
            return "Error formatting no tasks message"

    def format_task_claimed_message(self, task: "DevelopmentTask") -> str:
        """Format message when a task is claimed"""
        try:
            message = f"""🎯 TASK CLAIMED: {task.title}

📋 Task Details:
   • ID: {task.task_id}
   • Priority: {task.priority}
   • Complexity: {task.complexity}
   • Estimated Time: {task.estimated_hours}h
   • Required Skills: {', '.join(task.required_skills)}

🚀 Status: Ready to start work
⏰ Next: Begin task execution in next cycle

Good luck with your autonomous development! 🚀"""

            # Record operation
            self.record_operation("format_task_claimed", True, 0.0)
            
            return message
            
        except Exception as e:
            self.logger.error(f"Failed to format task claimed message: {e}")
            self.record_operation("format_task_claimed", False, 0.0)
            return "Error formatting task claimed message"

    def format_progress_update_message(self, task: "DevelopmentTask", new_progress: float, blockers: List[str] = None) -> str:
        """Format progress update message for an agent"""
        try:
            if blockers:
                message = f"""⚠️ PROGRESS UPDATE - BLOCKERS DETECTED

📊 Task: {task.title}
📈 Progress: {new_progress:.1f}%
🚫 Blockers: {', '.join(blockers)}

🔧 Action Required: Address blockers before continuing
⏰ Next Update: In next cycle"""
            else:
                message = f"""📊 PROGRESS UPDATE

📋 Task: {task.title}
📈 Progress: {new_progress:.1f}%
✅ Status: Making good progress

🚀 Continue autonomous development!
⏰ Next Update: In next cycle"""

            # Record operation
            self.record_operation("format_progress_update", True, 0.0)
            
            return message
            
        except Exception as e:
            self.logger.error(f"Failed to format progress update message: {e}")
            self.record_operation("format_progress_update", False, 0.0)
            return "Error formatting progress update message"

    def format_workflow_complete_message(self) -> str:
        """Format final workflow completion message"""
        try:
            summary = self.task_manager.get_task_summary()
            stats = summary["workflow_stats"]
            
            message = f"""🌅 OVERNIGHT WORKFLOW COMPLETE

📊 Final Summary:
   • Total Cycles: {stats['overnight_cycles']}
   • Autonomous Hours: {stats['autonomous_hours']}
   • Tasks Completed: {stats['total_tasks_completed']}

🎯 Great work on autonomous development!
🔄 System ready for next overnight session

Good morning! ☀️"""

            # Record operation
            self.record_operation("format_workflow_complete", True, 0.0)
            
            return message
            
        except Exception as e:
            self.logger.error(f"Failed to format workflow complete message: {e}")
            self.record_operation("format_workflow_complete", False, 0.0)
            return "Error formatting workflow complete message"

    def format_remaining_tasks_message(self, remaining_count: int) -> str:
        """Format message about remaining available tasks"""
        try:
            message = f"📋 {remaining_count} tasks still available for claiming in next cycle."
            
            # Record operation
            self.record_operation("format_remaining_tasks", True, 0.0)
            
            return message
            
        except Exception as e:
            self.logger.error(f"Failed to format remaining tasks message: {e}")
            self.record_operation("format_remaining_tasks", False, 0.0)
            return "Error formatting remaining tasks message"

    def format_detailed_task_status(self) -> str:
        """Format detailed task status for CLI display"""
        try:
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

            # Record operation
            self.record_operation("format_detailed_task_status", True, 0.0)
            
            return "\n".join(status_lines)
            
        except Exception as e:
            self.logger.error(f"Failed to format detailed task status: {e}")
            self.record_operation("format_detailed_task_status", False, 0.0)
            return "Error formatting detailed task status"

    def format_workflow_statistics(self) -> str:
        """Format workflow statistics for CLI display"""
        try:
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

            # Record operation
            self.record_operation("format_workflow_statistics", True, 0.0)
            
            return "\n".join(status_lines)
            
        except Exception as e:
            self.logger.error(f"Failed to format workflow statistics: {e}")
            self.record_operation("format_workflow_statistics", False, 0.0)
            return "Error formatting workflow statistics"

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
            
            report = {
                "summary": summary,
                "workflow_stats": stats,
                "performance_metrics": {
                    "efficiency_score": efficiency_score,
                    "avg_cycle_efficiency": avg_cycle_efficiency,
                    "task_completion_rate": summary["completion_rate"],
                    "autonomous_productivity": completed_tasks / max(stats["autonomous_hours"], 1),
                }
            }
            
            # Track report generation
            self.reports_generated += 1
            self.last_report_time = datetime.now()
            self.report_history.append({
                "timestamp": self.last_report_time.isoformat(),
                "report_type": "performance",
                "success": True
            })
            
            # Record operation
            self.record_operation("generate_performance_report", True, 0.0)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate performance report: {e}")
            
            # Track failed report
            self.report_history.append({
                "timestamp": datetime.now().isoformat(),
                "report_type": "performance",
                "success": False,
                "error": str(e)
            })
            
            self.record_operation("generate_performance_report", False, 0.0)
            return {}
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_report_history(self):
        """Save report history (placeholder for future persistence)"""
        try:
            # TODO: Implement persistence to database/file
            self.logger.debug("Report history saved")
            
        except Exception as e:
            self.logger.error(f"Failed to save report history: {e}")
    
    def _check_reporting_needs(self):
        """Check if new reports are needed"""
        try:
            # Check if it's time for a new report
            if self.last_report_time:
                time_since_last = (datetime.now() - self.last_report_time).total_seconds()
                if time_since_last > 3600:  # 1 hour
                    self.logger.info("Time for new performance report")
                    
        except Exception as e:
            self.logger.error(f"Failed to check reporting needs: {e}")
    
    def get_reporting_stats(self) -> Dict[str, Any]:
        """Get reporting statistics"""
        try:
            stats = {
                "reports_generated": self.reports_generated,
                "last_report_time": self.last_report_time.isoformat() if self.last_report_time else None,
                "report_history_size": len(self.report_history),
                "successful_reports": len([r for r in self.report_history if r.get("success", False)]),
                "failed_reports": len([r for r in self.report_history if not r.get("success", False)])
            }
            
            # Record operation
            self.record_operation("get_reporting_stats", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get reporting stats: {e}")
            self.record_operation("get_reporting_stats", False, 0.0)
            return {"error": str(e)}
