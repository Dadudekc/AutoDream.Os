from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from typing import TYPE_CHECKING
import asyncio
import logging

    from src.autonomous_development.core import DevelopmentTask
    from src.core.task_manager_refactored import DevelopmentTaskManager as TaskManager
    from src.services import (
from src.autonomous_development.agents.coordinator import AgentCoordinator
from src.autonomous_development.reporting.manager import ReportingManager
from src.autonomous_development.tasks.handler import TaskHandler
from src.core.base_manager import BaseManager, ManagerStatus, ManagerPriority
from src.utils.stability_improvements import stability_manager, safe_import

#!/usr/bin/env python3
"""
Autonomous Development Workflow Manager
======================================

This module handles the core workflow management for autonomous development.
Follows SRP by focusing solely on workflow orchestration.
Now inherits from BaseManager for unified functionality.

V2 Standards: ≤200 LOC, SRP, OOP principles, BaseManager inheritance
"""



if TYPE_CHECKING:
        UnifiedMessagingService as RealAgentCommunicationSystem,
    )


class AutonomousWorkflowManager(BaseManager):
    """
    Manages autonomous overnight development workflow
    
    Now inherits from BaseManager for unified functionality
    """

    def __init__(
        self,
        comm_system: "RealAgentCommunicationSystem",
        task_manager: "TaskManager",
        agent_coordinator: Optional[AgentCoordinator] = None,
        task_handler: Optional[TaskHandler] = None,
        reporting_manager: Optional[ReportingManager] = None,
    ):
        """Initialize autonomous workflow manager with BaseManager"""
        super().__init__(
            manager_id="autonomous_workflow_manager",
            name="Autonomous Workflow Manager",
            description="Manages autonomous overnight development workflow"
        )
        
        self.comm_system = comm_system
        self.task_manager = task_manager
        self.agent_coordinator = agent_coordinator or AgentCoordinator()
        self.task_handler = task_handler or TaskHandler(task_manager)
        self.reporting_manager = reporting_manager or ReportingManager(task_manager)
        
        # Workflow state
        self.workflow_active = False
        self.cycle_duration = 3600  # 1 hour cycles
        
        # Workflow tracking
        self.cycles_completed = 0
        self.total_workflow_time = 0
        self.workflow_start_time: Optional[datetime] = None
        
        self.logger.info("Autonomous Workflow Manager initialized")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize autonomous workflow system"""
        try:
            self.logger.info("Starting Autonomous Workflow Manager...")
            
            # Reset workflow state
            self.workflow_active = False
            self.cycles_completed = 0
            self.total_workflow_time = 0
            self.workflow_start_time = None
            
            self.logger.info("Autonomous Workflow Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start Autonomous Workflow Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup autonomous workflow system"""
        try:
            self.logger.info("Stopping Autonomous Workflow Manager...")
            
            # Stop workflow if active
            if self.workflow_active:
                asyncio.create_task(self.stop_overnight_workflow())
            
            # Clear workflow state
            self.workflow_active = False
            self.cycles_completed = 0
            self.total_workflow_time = 0
            self.workflow_start_time = None
            
            self.logger.info("Autonomous Workflow Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop Autonomous Workflow Manager: {e}")
    
    def _on_heartbeat(self):
        """Autonomous workflow manager heartbeat"""
        try:
            # Check workflow health
            if self.workflow_active:
                self._check_workflow_health()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize autonomous workflow resources"""
        try:
            # Initialize workflow state
            self.workflow_active = False
            self.cycles_completed = 0
            self.total_workflow_time = 0
            self.workflow_start_time = None
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup autonomous workflow resources"""
        try:
            # Clear workflow state
            self.workflow_active = False
            self.cycles_completed = 0
            self.total_workflow_time = 0
            self.workflow_start_time = None
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reset workflow state
            self.workflow_active = False
            self.cycles_completed = 0
            
            # Restart workflow if needed
            if "workflow" in context.lower():
                self.logger.info("Attempting to restart workflow...")
                # Note: This would need to be handled asynchronously
                return True
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # Autonomous Workflow Management Methods
    # ============================================================================
    
    async def start_overnight_workflow(self) -> bool:
        """Start autonomous overnight development workflow"""
        try:
            self.logger.info("🌙 Starting autonomous overnight development workflow...")
            
            # Set workflow state
            self.workflow_active = True
            self.workflow_start_time = datetime.now()
            
            # Record operation
            self.record_operation("start_overnight_workflow", True, 0.0)
            
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
                self.record_operation("start_overnight_workflow", False, 0.0)
                return False

            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start overnight workflow: {e}")
            self.workflow_active = False
            self.record_operation("start_overnight_workflow", False, 0.0)
            return False

    async def _broadcast_workflow_start(self):
        """Broadcast workflow start message"""
        try:
            message = self.reporting_manager.format_workflow_start_message()
            await self.comm_system.send_message_to_all_agents_with_line_breaks(message)

            agent1_message = self.reporting_manager.format_agent1_message()
            await self.comm_system.send_message_to_agent_with_line_breaks(
                "Agent-1", agent1_message, "workspace_box"
            )
            
            # Record operation
            self.record_operation("broadcast_workflow_start", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Failed to broadcast workflow start: {e}")
            self.record_operation("broadcast_workflow_start", False, 0.0)

    async def _execute_workflow_cycle(self):
        """Execute one workflow cycle"""
        try:
            self.logger.info("🔄 Executing workflow cycle...")

            # Update workflow stats
            self.task_manager.workflow_stats["overnight_cycles"] += 1
            self.task_manager.workflow_stats["autonomous_hours"] += 1
            
            # Update local tracking
            self.cycles_completed += 1

            # 1. Task Review and Claiming Phase
            await self._task_review_and_claiming_phase()

            # 2. Work Execution Phase
            await self._work_execution_phase()

            # 3. Progress Reporting Phase
            await self._progress_reporting_phase()

            # 4. Cycle Summary
            await self._cycle_summary_phase()
            
            # Record operation
            self.record_operation("execute_workflow_cycle", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Failed to execute workflow cycle: {e}")
            self.record_operation("execute_workflow_cycle", False, 0.0)

    async def _task_review_and_claiming_phase(self):
        """Phase 1: Agents review and claim tasks"""
        try:
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
            
            # Record operation
            self.record_operation("task_review_claiming_phase", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Failed to execute task review and claiming phase: {e}")
            self.record_operation("task_review_claiming_phase", False, 0.0)

    async def _work_execution_phase(self):
        """Phase 2: Agents work on claimed tasks"""
        try:
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
            
            # Record operation
            self.record_operation("work_execution_phase", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Failed to execute work execution phase: {e}")
            self.record_operation("work_execution_phase", False, 0.0)

    async def _progress_reporting_phase(self):
        """Phase 3: Agents report progress"""
        try:
            self.logger.info("📊 Phase 3: Progress Reporting")

            progress_message = self.reporting_manager.format_progress_summary()
            await self.comm_system.send_message_to_all_agents_with_line_breaks(
                f"📊 PROGRESS SUMMARY:\n\n{progress_message}", "status_box"
            )
            
            # Record operation
            self.record_operation("progress_reporting_phase", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Failed to execute progress reporting phase: {e}")
            self.record_operation("progress_reporting_phase", False, 0.0)

    async def _cycle_summary_phase(self):
        """Phase 4: Cycle summary and next steps"""
        try:
            self.logger.info("📈 Phase 4: Cycle Summary")

            cycle_message = self.reporting_manager.format_cycle_summary()
            await self.comm_system.send_message_to_all_agents_with_line_breaks(
                cycle_message, "workspace_box"
            )
            
            # Record operation
            self.record_operation("cycle_summary_phase", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Failed to execute cycle summary phase: {e}")
            self.record_operation("cycle_summary_phase", False, 0.0)

    async def _simulate_autonomous_task_claiming(
        self, available_tasks: List["DevelopmentTask"]
    ):
        """Simulate agents autonomously claiming tasks"""
        try:
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
            
            # Record operation
            self.record_operation("simulate_autonomous_task_claiming", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Failed to simulate autonomous task claiming: {e}")
            self.record_operation("simulate_autonomous_task_claiming", False, 0.0)

    async def _simulate_work_progress(self, active_tasks: List["DevelopmentTask"]):
        """Simulate agents working on claimed tasks"""
        try:
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
            
            # Record operation
            self.record_operation("simulate_work_progress", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Failed to simulate work progress: {e}")
            self.record_operation("simulate_work_progress", False, 0.0)

    async def _broadcast_no_tasks_available(self):
        """Broadcast when no tasks are available"""
        try:
            message = self.reporting_manager.format_no_tasks_message()
            await self.comm_system.send_message_to_all_agents_with_line_breaks(
                message, "status_box"
            )
            
            # Record operation
            self.record_operation("broadcast_no_tasks_available", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Failed to broadcast no tasks available: {e}")
            self.record_operation("broadcast_no_tasks_available", False, 0.0)

    async def stop_overnight_workflow(self):
        """Stop autonomous overnight workflow"""
        try:
            self.logger.info("🛑 Stopping autonomous overnight workflow...")
            
            # Update workflow state
            self.workflow_active = False
            
            # Calculate total workflow time
            if self.workflow_start_time:
                self.total_workflow_time = (datetime.now() - self.workflow_start_time).total_seconds()

            final_message = self.reporting_manager.format_workflow_complete_message()
            await self.comm_system.send_message_to_all_agents_with_line_breaks(
                final_message, "workspace_box"
            )
            
            # Record operation
            self.record_operation("stop_overnight_workflow", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Failed to stop overnight workflow: {e}")
            self.record_operation("stop_overnight_workflow", False, 0.0)
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _check_workflow_health(self):
        """Check workflow health status"""
        try:
            # Check if workflow is still active
            if not self.workflow_active:
                return
            
            # Check if workflow has been running too long
            if self.workflow_start_time:
                runtime = (datetime.now() - self.workflow_start_time).total_seconds()
                if runtime > 86400:  # 24 hours
                    self.logger.warning("Workflow has been running for over 24 hours")
            
            # Check cycle completion rate
            if self.cycles_completed > 0 and self.workflow_start_time:
                runtime_hours = (datetime.now() - self.workflow_start_time).total_seconds() / 3600
                cycles_per_hour = self.cycles_completed / runtime_hours
                if cycles_per_hour < 0.5:  # Less than 1 cycle per 2 hours
                    self.logger.warning("Workflow cycle completion rate is low")
                    
        except Exception as e:
            self.logger.error(f"Failed to check workflow health: {e}")
    
    def get_workflow_stats(self) -> Dict[str, Any]:
        """Get workflow statistics"""
        try:
            stats = {
                "workflow_active": self.workflow_active,
                "cycles_completed": self.cycles_completed,
                "total_workflow_time": self.total_workflow_time,
                "workflow_start_time": self.workflow_start_time.isoformat() if self.workflow_start_time else None,
                "cycle_duration": self.cycle_duration
            }
            
            # Record operation
            self.record_operation("get_workflow_stats", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get workflow stats: {e}")
            self.record_operation("get_workflow_stats", False, 0.0)
            return {"error": str(e)}
