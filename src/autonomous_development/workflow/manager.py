#!/usr/bin/env python3
"""
Autonomous Development Workflow Manager
======================================

This module handles the core workflow management for autonomous development.
Follows SRP by focusing solely on workflow orchestration.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from src.utils.stability_improvements import stability_manager, safe_import
# Use type hints with strings to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.task_manager import DevelopmentTaskManager as TaskManager
    from src.autonomous_development.core import DevelopmentTask
    from src.services.messaging import UnifiedMessagingService as RealAgentCommunicationSystem


class AutonomousWorkflowManager:
    """Manages autonomous overnight development workflow"""

    def __init__(
        self, comm_system: "RealAgentCommunicationSystem", task_manager: "TaskManager"
    ):
        self.comm_system = comm_system
        self.task_manager = task_manager
        self.logger = logging.getLogger(__name__)
        self.workflow_active = False
        self.cycle_duration = 3600  # 1 hour cycles

    async def start_overnight_workflow(self) -> bool:
        """Start autonomous overnight development workflow"""
        self.logger.info("🌙 Starting autonomous overnight development workflow...")
        self.workflow_active = True

        # Initial broadcast to all agents
        await self._broadcast_workflow_start()

        # Start continuous workflow cycle
        try:
            while self.workflow_active:
                await self._execute_workflow_cycle()
                await asyncio.sleep(self.cycle_duration)
        except Exception as e:
            self.logger.error(f"❌ Workflow error: {e}")
            self.workflow_active = False
            return False

        return True

    async def _broadcast_workflow_start(self):
        """Broadcast workflow start message"""
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

        # Send to all agents with line breaks
        await self.comm_system.send_message_to_all_agents_with_line_breaks(message)

        # Special message to Agent-1 with line breaks
        agent1_message = """🎯 AGENT-1: You are now the Task Manager!

Your responsibilities:
1. 📋 Monitor task list and create new tasks as needed
2. 📊 Track progress and identify bottlenecks
3. 🔄 Coordinate workflow and resolve conflicts
4. 📈 Optimize task distribution and priorities
5. 🚨 Handle emergencies and blocked tasks

Start by reviewing the current task list and identifying areas for improvement!"""

        await self.comm_system.send_message_to_agent_with_line_breaks(
            "Agent-1", agent1_message, "workspace_box"
        )

    async def _execute_workflow_cycle(self):
        """Execute one workflow cycle"""
        self.logger.info("🔄 Executing workflow cycle...")

        # Update workflow stats
        self.task_manager.workflow_stats["overnight_cycles"] += 1
        self.task_manager.workflow_stats["autonomous_hours"] += 1

        # 1. Task Review and Claiming Phase
        await self._task_review_and_claiming_phase()

        # 2. Work Execution Phase
        await self._work_execution_phase()

        # 3. Progress Reporting Phase
        await self._progress_reporting_phase()

        # 4. Cycle Summary
        await self._cycle_summary_phase()

    async def _task_review_and_claiming_phase(self):
        """Phase 1: Agents review and claim tasks"""
        self.logger.info("📋 Phase 1: Task Review and Claiming")

        available_tasks = self.task_manager.get_available_tasks()
        if not available_tasks:
            await self._broadcast_no_tasks_available()
            return

        # Broadcast available tasks to Agents 2-8 with line breaks
        task_list_message = self._format_task_list_for_agents(available_tasks)
        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            f"📋 AVAILABLE TASKS FOR CLAIMING:\n\n{task_list_message}", "workspace_box"
        )

        # Simulate autonomous task claiming
        await self._simulate_autonomous_task_claiming(available_tasks)

    async def _work_execution_phase(self):
        """Phase 2: Agents work on claimed tasks"""
        self.logger.info("🚀 Phase 2: Work Execution")

        # Get all claimed and in-progress tasks
        active_tasks = [
            t
            for t in self.task_manager.tasks.values()
            if t.status in ["claimed", "in_progress"]
        ]

        if not active_tasks:
            await self.comm_system.send_message_to_all_agents_with_line_breaks(
                "⏸️ No active tasks to work on. Waiting for new tasks...", "status_box"
            )
            return

        # Simulate work progress
        await self._simulate_work_progress(active_tasks)

    async def _progress_reporting_phase(self):
        """Phase 3: Agents report progress"""
        self.logger.info("📊 Phase 3: Progress Reporting")

        # Get progress updates from all active tasks
        progress_message = self._format_progress_summary()
        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            f"📊 PROGRESS SUMMARY:\n\n{progress_message}", "status_box"
        )

    async def _cycle_summary_phase(self):
        """Phase 4: Cycle summary and next steps"""
        self.logger.info("📈 Phase 4: Cycle Summary")

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

        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            cycle_message, "workspace_box"
        )

    def _format_task_list_for_agents(self, tasks: List["DevelopmentTask"]) -> str:
        """Format task list for agent review"""
        if not tasks:
            return "No tasks available for claiming."

        task_lines = []
        for task in sorted(tasks, key=lambda t: t.priority, reverse=True):
            priority_icon = (
                "🔴" if task.priority >= 8 else "🟡" if task.priority >= 5 else "🟢"
            )
            complexity_icon = (
                "🔥"
                if task.complexity == "high"
                else "⚡"
                if task.complexity == "medium"
                else "💡"
            )

            task_lines.append(
                f"{priority_icon} **{task.title}** (Priority: {task.priority})\n"
                f"   {complexity_icon} Complexity: {task.complexity.title()}\n"
                f"   ⏱️ Estimated: {task.estimated_hours}h\n"
                f"   🎯 Skills: {', '.join(task.required_skills)}\n"
                f"   📝 {task.description}\n"
                f"   🆔 Task ID: {task.task_id}\n"
            )

        return "\n".join(task_lines)

    async def _simulate_autonomous_task_claiming(
        self, available_tasks: List["DevelopmentTask"]
    ):
        """Simulate agents autonomously claiming tasks"""
        self.logger.info("🎯 Simulating autonomous task claiming...")

        # Simulate Agents 2-8 claiming tasks based on skills
        for agent_id in [f"Agent-{i}" for i in range(2, 9)]:
            if not available_tasks:
                break

            # Find best matching task for this agent
            best_task = self._find_best_task_for_agent(agent_id, available_tasks)
            if best_task:
                # Claim the task
                if self.task_manager.claim_task(best_task.task_id, agent_id):
                    available_tasks.remove(best_task)

                    # Notify agent of claimed task with proper line breaks
                    claim_message = f"""🎯 TASK CLAIMED: {best_task.title}

📋 Task Details:
   • ID: {best_task.task_id}
   • Priority: {best_task.priority}
   • Complexity: {best_task.complexity}
   • Estimated Time: {best_task.estimated_hours}h
   • Required Skills: {', '.join(best_task.required_skills)}

🚀 Status: Ready to start work
⏰ Next: Begin task execution in next cycle

Good luck with your autonomous development! 🚀"""

                    # Send with line break handling
                    await self.comm_system.send_message_to_agent_with_line_breaks(
                        agent_id, claim_message, "workspace_box"
                    )

                    self.logger.info(f"✅ {agent_id} claimed task {best_task.task_id}")

        # Update remaining available tasks
        remaining_count = len(available_tasks)
        if remaining_count > 0:
            await self.comm_system.send_message_to_all_agents_with_line_breaks(
                f"📋 {remaining_count} tasks still available for claiming in next cycle.",
                "status_box",
            )

    def _find_best_task_for_agent(
        self, agent_id: str, available_tasks: List["DevelopmentTask"]
    ) -> Optional["DevelopmentTask"]:
        """Find the best matching task for an agent based on skills and preferences"""
        # This method will be implemented by the agent coordinator
        # For now, return None to maintain compatibility
        return None

    async def _simulate_work_progress(self, active_tasks: List["DevelopmentTask"]):
        """Simulate agents working on claimed tasks"""
        self.logger.info("🚀 Simulating work progress...")

        for task in active_tasks:
            if task.status == "claimed":
                # Start work on claimed task
                self.task_manager.start_task_work(task.task_id)

            if task.status == "in_progress":
                # Simulate progress
                current_progress = task.progress_percentage
                progress_increment = 20.0  # 20% progress per cycle
                new_progress = min(100.0, current_progress + progress_increment)

                # Random blockers
                blockers = []
                if task.progress_percentage > 50:  # 50% chance of blocker after 50% progress
                    possible_blockers = [
                        "Waiting for dependency update",
                        "Need clarification on requirements",
                        "Technical issue encountered",
                        "Waiting for code review",
                        "Integration testing needed",
                    ]
                    blockers = possible_blockers[:2]

                self.task_manager.update_task_progress(
                    task.task_id, new_progress, blockers
                )

                # Notify agent of progress
                if blockers:
                    progress_message = f"""⚠️ PROGRESS UPDATE - BLOCKERS DETECTED

📊 Task: {task.title}
📈 Progress: {new_progress:.1f}%
🚫 Blockers: {', '.join(blockers)}

🔧 Action Required: Address blockers before continuing
⏰ Next Update: In next cycle"""
                else:
                    progress_message = f"""📊 PROGRESS UPDATE

📋 Task: {task.title}
📈 Progress: {new_progress:.1f}%
✅ Status: Making good progress

🚀 Continue autonomous development!
⏰ Next Update: In next cycle"""

                await self.comm_system.send_message_to_agent(
                    task.claimed_by, progress_message, "status_box"
                )

    def _format_progress_summary(self) -> str:
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
            status_icon = "🔄" if task.status == "in_progress" else "⏳"
            progress_lines.append(
                f"{status_icon} **{task.title}** (Agent: {task.claimed_by})\n"
                f"   📊 Progress: {task.progress_percentage:.1f}%\n"
                f"   🚫 Blockers: {', '.join(task.blockers) if task.blockers else 'None'}\n"
            )

        return "\n".join(progress_lines)

    async def _broadcast_no_tasks_available(self):
        """Broadcast when no tasks are available"""
        message = """📋 NO TASKS AVAILABLE

🎯 All current tasks have been claimed or completed!
⏰ Waiting for Agent-1 to create new tasks...

🔄 Next cycle will focus on:
   • Progress monitoring
   • Task completion
   • New task creation by Agent-1

Stay ready for new development opportunities! 🚀"""

        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            message, "status_box"
        )

    async def stop_overnight_workflow(self):
        """Stop autonomous overnight workflow"""
        self.logger.info("🛑 Stopping autonomous overnight workflow...")
        self.workflow_active = False

        # Final broadcast
        final_message = f"""🌅 OVERNIGHT WORKFLOW COMPLETE

📊 Final Summary:
   • Total Cycles: {self.task_manager.workflow_stats['overnight_cycles']}
   • Autonomous Hours: {self.task_manager.workflow_stats['autonomous_hours']}
   • Tasks Completed: {self.task_manager.workflow_stats['total_tasks_completed']}

🎯 Great work on autonomous development!
🔄 System ready for next overnight session

Good morning! ☀️"""

        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            final_message, "workspace_box"
        )
