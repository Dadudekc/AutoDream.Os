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
from src.autonomous_development.tasks.handler import TaskHandler
from src.autonomous_development.agents.coordinator import AgentCoordinator
from src.autonomous_development.reporting.manager import ReportingManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.task_manager import DevelopmentTaskManager as TaskManager
    from src.autonomous_development.core import DevelopmentTask
    from src.services.messaging import (
        UnifiedMessagingService as RealAgentCommunicationSystem,
    )


class AutonomousWorkflowManager:
    """Manages autonomous overnight development workflow"""

    def __init__(
        self,
        comm_system: "RealAgentCommunicationSystem",
        task_manager: "TaskManager",
        agent_coordinator: Optional[AgentCoordinator] = None,
        task_handler: Optional[TaskHandler] = None,
        reporting_manager: Optional[ReportingManager] = None,
    ):
        self.comm_system = comm_system
        self.task_manager = task_manager
        self.agent_coordinator = agent_coordinator or AgentCoordinator()
        self.task_handler = task_handler or TaskHandler(task_manager)
        self.reporting_manager = reporting_manager or ReportingManager(task_manager)
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
        message = self.reporting_manager.format_workflow_start_message()
        await self.comm_system.send_message_to_all_agents_with_line_breaks(message)

        agent1_message = self.reporting_manager.format_agent1_message()
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

        task_list_message = self.reporting_manager.format_task_list_for_agents(
            available_tasks
        )
        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            f"📋 AVAILABLE TASKS FOR CLAIMING:\n\n{task_list_message}", "workspace_box"
        )

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

        progress_message = self.reporting_manager.format_progress_summary()
        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            f"📊 PROGRESS SUMMARY:\n\n{progress_message}", "status_box"
        )

    async def _cycle_summary_phase(self):
        """Phase 4: Cycle summary and next steps"""
        self.logger.info("📈 Phase 4: Cycle Summary")

        cycle_message = self.reporting_manager.format_cycle_summary()
        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            cycle_message, "workspace_box"
        )

    async def _simulate_autonomous_task_claiming(
        self, available_tasks: List["DevelopmentTask"]
    ):
        """Simulate agents autonomously claiming tasks"""
        self.logger.info("🎯 Simulating autonomous task claiming...")

        for agent_id in [f"Agent-{i}" for i in range(2, 9)]:
            if not available_tasks:
                break

            best_task = self.agent_coordinator.find_best_task_for_agent(
                agent_id, available_tasks
            )
            if best_task and self.task_handler.claim_task(best_task.task_id, agent_id):
                available_tasks.remove(best_task)
                self.agent_coordinator.update_agent_workload(
                    agent_id, best_task.task_id, "claim"
                )
                claim_message = self.reporting_manager.format_task_claimed_message(
                    best_task
                )
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

    async def _simulate_work_progress(self, active_tasks: List["DevelopmentTask"]):
        """Simulate agents working on claimed tasks"""
        self.logger.info("🚀 Simulating work progress...")

        for task in active_tasks:
            if task.status == "claimed":
                self.task_handler.start_task_work(task.task_id)
                self.agent_coordinator.update_agent_workload(
                    task.claimed_by, task.task_id, "start"
                )

            if task.status == "in_progress":
                current_progress = task.progress_percentage
                progress_increment = 20.0
                new_progress = min(100.0, current_progress + progress_increment)

                blockers = []
                if task.progress_percentage > 50:
                    possible_blockers = [
                        "Waiting for dependency update",
                        "Need clarification on requirements",
                        "Technical issue encountered",
                        "Waiting for code review",
                        "Integration testing needed",
                    ]
                    blockers = possible_blockers[:2]

                self.task_handler.update_task_progress(
                    task.task_id, new_progress, blockers
                )

                progress_message = (
                    self.reporting_manager.format_progress_update_message(
                        task, new_progress, blockers
                    )
                )
                await self.comm_system.send_message_to_agent(
                    task.claimed_by, progress_message, "status_box"
                )

                if task.status == "completed":
                    self.agent_coordinator.update_agent_workload(
                        task.claimed_by, task.task_id, "complete"
                    )

    async def _broadcast_no_tasks_available(self):
        """Broadcast when no tasks are available"""
        message = self.reporting_manager.format_no_tasks_message()
        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            message, "status_box"
        )

    async def stop_overnight_workflow(self):
        """Stop autonomous overnight workflow"""
        self.logger.info("🛑 Stopping autonomous overnight workflow...")
        self.workflow_active = False

        final_message = self.reporting_manager.format_workflow_complete_message()
        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            final_message, "workspace_box"
        )
