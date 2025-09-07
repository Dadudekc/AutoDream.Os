from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import asyncio
import logging

    from src.autonomous_development.agents.coordinator import AgentCoordinator
    from src.autonomous_development.core import DevelopmentTask
    from src.autonomous_development.reporting.manager import ReportingManager
    from src.autonomous_development.tasks.handler import TaskHandler
    from src.core.task_manager_refactored import DevelopmentTaskManager as TaskManager
    from src.services import UnifiedMessagingService as RealAgentCommunicationSystem
from src.core.base_manager import BaseManager
from src.utils.stability_improvements import stability_manager, safe_import
from src/autonomous_development/workflow/manager.py into a V2-compliant system.

#!/usr/bin/env python3
"""
Extended Workflow Manager - inherits from BaseManager for unified functionality

This manager consolidates autonomous development workflow management functionality
"""



# Safe imports with fallbacks
try:
except ImportError:
    # Fallback classes for compatibility
    class TaskHandler: pass
    class AgentCoordinator: pass
    class ReportingManager: pass
    class TaskManager: pass
    class DevelopmentTask: pass
    class RealAgentCommunicationSystem: pass


class ExtendedWorkflowManager(BaseManager):
    """Extended Workflow Manager - inherits from BaseManager for unified functionality"""
    
    def __init__(self, config_path: str = "config/autonomous_development/workflow_manager.json"):
        super().__init__(
            manager_name="ExtendedWorkflowManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Workflow-specific state
        self.workflow_active = False
        self.cycle_duration = 3600  # 1 hour cycles
        self.current_cycle = 0
        self.total_cycles = 0
        
        # Dependencies (will be injected)
        self.comm_system: Optional[RealAgentCommunicationSystem] = None
        self.task_manager: Optional[TaskManager] = None
        self.agent_coordinator: Optional[AgentCoordinator] = None
        self.task_handler: Optional[TaskHandler] = None
        self.reporting_manager: Optional[ReportingManager] = None
        
        # Workflow statistics
        self.workflow_stats = {
            "overnight_cycles": 0,
            "autonomous_hours": 0,
            "tasks_claimed": 0,
            "tasks_completed": 0,
            "workflow_errors": 0
        }
        
        # Initialize workflow components
        self._initialize_workflow_components()
        
        logger.info(f"ExtendedWorkflowManager initialized successfully")
    
    def _initialize_workflow_components(self):
        """Initialize workflow components with fallbacks"""
        try:
            if not self.agent_coordinator:
                self.agent_coordinator = AgentCoordinator()
            if not self.task_handler and self.task_manager:
                self.task_handler = TaskHandler(self.task_manager)
            if not self.reporting_manager and self.task_manager:
                self.reporting_manager = ReportingManager(self.task_manager)
        except Exception as e:
            self.logger.warning(f"Some workflow components not available: {e}")
    
    def set_dependencies(
        self,
        comm_system: RealAgentCommunicationSystem,
        task_manager: TaskManager,
        agent_coordinator: Optional[AgentCoordinator] = None,
        task_handler: Optional[TaskHandler] = None,
        reporting_manager: Optional[ReportingManager] = None
    ):
        """Set workflow dependencies"""
        self.comm_system = comm_system
        self.task_manager = task_manager
        
        if agent_coordinator:
            self.agent_coordinator = agent_coordinator
        if task_handler:
            self.task_handler = task_handler
        if reporting_manager:
            self.reporting_manager = reporting_manager
        
        # Re-initialize components with new dependencies
        self._initialize_workflow_components()
        
        self.logger.info("Workflow dependencies set successfully")
    
    async def start_overnight_workflow(self) -> bool:
        """Start autonomous overnight development workflow"""
        if not self.comm_system or not self.task_manager:
            self.logger.error("❌ Missing required dependencies for workflow")
            return False
        
        self.logger.info("🌙 Starting autonomous overnight development workflow...")
        self.workflow_active = True
        self.start_time = datetime.now()
        
        # Emit workflow start event
        self.emit_event("workflow_started", {
            "start_time": self.start_time.isoformat(),
            "cycle_duration": self.cycle_duration
        })
        
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
            self.workflow_stats["workflow_errors"] += 1
            
            # Emit error event
            self.emit_event("workflow_error", {
                "error": str(e),
                "cycle": self.current_cycle
            })
            
            return False
        
        return True
    
    async def _broadcast_workflow_start(self):
        """Broadcast workflow start message"""
        if not self.reporting_manager or not self.comm_system:
            return
        
        try:
            message = self.reporting_manager.format_workflow_start_message()
            await self.comm_system.send_message_to_all_agents_with_line_breaks(message)
            
            agent1_message = self.reporting_manager.format_agent1_message()
            await self.comm_system.send_message_to_agent_with_line_breaks(
                "Agent-1", agent1_message, "workspace_box"
            )
            
            self.logger.info("✅ Workflow start broadcast completed")
        except Exception as e:
            self.logger.error(f"❌ Error broadcasting workflow start: {e}")
    
    async def _execute_workflow_cycle(self):
        """Execute one workflow cycle"""
        self.current_cycle += 1
        self.total_cycles += 1
        
        self.logger.info(f"🔄 Executing workflow cycle {self.current_cycle}...")
        
        # Update workflow stats
        if self.task_manager:
            self.task_manager.workflow_stats["overnight_cycles"] += 1
            self.task_manager.workflow_stats["autonomous_hours"] += 1
        
        self.workflow_stats["overnight_cycles"] += 1
        self.workflow_stats["autonomous_hours"] += 1
        
        # Emit cycle start event
        self.emit_event("workflow_cycle_started", {
            "cycle": self.current_cycle,
            "total_cycles": self.total_cycles
        })
        
        try:
            # 1. Task Review and Claiming Phase
            await self._task_review_and_claiming_phase()
            
            # 2. Work Execution Phase
            await self._work_execution_phase()
            
            # 3. Progress Reporting Phase
            await self._progress_reporting_phase()
            
            # 4. Cycle Summary
            await self._cycle_summary_phase()
            
            # Emit cycle completion event
            self.emit_event("workflow_cycle_completed", {
                "cycle": self.current_cycle,
                "duration": self.cycle_duration
            })
            
        except Exception as e:
            self.logger.error(f"❌ Error in workflow cycle {self.current_cycle}: {e}")
            self.emit_event("workflow_cycle_error", {
                "cycle": self.current_cycle,
                "error": str(e)
            })
    
    async def _task_review_and_claiming_phase(self):
        """Phase 1: Agents review and claim tasks"""
        self.logger.info("📋 Phase 1: Task Review and Claiming...")
        
        if not self.task_manager or not self.agent_coordinator:
            return
        
        try:
            # Get available tasks
            available_tasks = self.task_manager.get_available_tasks()
            
            if not available_tasks:
                await self._broadcast_no_tasks_available()
                return
            
            # Simulate autonomous task claiming
            await self._simulate_autonomous_task_claiming(available_tasks)
            
        except Exception as e:
            self.logger.error(f"❌ Error in task review phase: {e}")
    
    async def _work_execution_phase(self):
        """Phase 2: Work execution on claimed tasks"""
        self.logger.info("🚀 Phase 2: Work Execution...")
        
        if not self.task_manager:
            return
        
        try:
            # Get active tasks
            active_tasks = self.task_manager.get_active_tasks()
            
            if active_tasks:
                await self._simulate_work_progress(active_tasks)
            else:
                self.logger.info("📝 No active tasks to process")
                
        except Exception as e:
            self.logger.error(f"❌ Error in work execution phase: {e}")
    
    async def _progress_reporting_phase(self):
        """Phase 3: Progress reporting and status updates"""
        self.logger.info("📊 Phase 3: Progress Reporting...")
        
        if not self.task_manager:
            return
        
        try:
            # Get workflow statistics
            stats = self.task_manager.workflow_stats if self.task_manager else {}
            
            # Emit progress event
            self.emit_event("workflow_progress", {
                "cycle": self.current_cycle,
                "stats": stats
            })
            
        except Exception as e:
            self.logger.error(f"❌ Error in progress reporting phase: {e}")
    
    async def _cycle_summary_phase(self):
        """Phase 4: Cycle summary and next cycle planning"""
        self.logger.info("📈 Phase 4: Cycle Summary...")
        
        try:
            # Format cycle summary message
            cycle_message = f"🔄 Cycle {self.current_cycle} Summary:\n"
            cycle_message += f"📊 Total Cycles: {self.total_cycles}\n"
            cycle_message += f"⏱️ Autonomous Hours: {self.workflow_stats['autonomous_hours']}\n"
            cycle_message += f"🎯 Tasks Claimed: {self.workflow_stats['tasks_claimed']}\n"
            cycle_message += f"✅ Tasks Completed: {self.workflow_stats['tasks_completed']}"
            
            # Broadcast cycle summary
            if self.comm_system:
                await self.comm_system.send_message_to_all_agents_with_line_breaks(
                    cycle_message, "workspace_box"
                )
            
            self.logger.info(f"✅ Cycle {self.current_cycle} summary completed")
            
        except Exception as e:
            self.logger.error(f"❌ Error in cycle summary phase: {e}")
    
    async def _simulate_autonomous_task_claiming(self, available_tasks: List[DevelopmentTask]):
        """Simulate agents autonomously claiming tasks"""
        self.logger.info("🎯 Simulating autonomous task claiming...")
        
        if not self.agent_coordinator or not self.task_handler:
            return
        
        try:
            for agent_id in [f"Agent-{i}" for i in range(2, 9)]:
                if not available_tasks:
                    break
                
                best_task = self.agent_coordinator.find_best_task_for_agent(
                    agent_id, available_tasks
                )
                
                if best_task and self.task_handler.claim_task(best_task.task_id, agent_id):
                    available_tasks.remove(best_task)
                    self.workflow_stats["tasks_claimed"] += 1
                    
                    self.agent_coordinator.update_agent_workload(
                        agent_id, best_task.task_id, "claim"
                    )
                    
                    # Emit task claimed event
                    self.emit_event("task_claimed", {
                        "task_id": best_task.task_id,
                        "agent_id": agent_id,
                        "cycle": self.current_cycle
                    })
                    
                    if self.reporting_manager and self.comm_system:
                        claim_message = self.reporting_manager.format_task_claimed_message(best_task)
                        await self.comm_system.send_message_to_agent_with_line_breaks(
                            agent_id, claim_message, "workspace_box"
                        )
                    
                    self.logger.info(f"✅ {agent_id} claimed task {best_task.task_id}")
            
            # Update remaining available tasks
            remaining_count = len(available_tasks)
            if remaining_count > 0 and self.comm_system:
                await self.comm_system.send_message_to_all_agents_with_line_breaks(
                    f"📋 {remaining_count} tasks still available for claiming in next cycle.",
                    "status_box",
                )
                
        except Exception as e:
            self.logger.error(f"❌ Error in task claiming simulation: {e}")
    
    async def _simulate_work_progress(self, active_tasks: List[DevelopmentTask]):
        """Simulate agents working on claimed tasks"""
        self.logger.info("🚀 Simulating work progress...")
        
        if not self.task_handler or not self.agent_coordinator:
            return
        
        try:
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
                    
                    # Simulate potential blockers
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
                    
                    # Emit progress update event
                    self.emit_event("task_progress", {
                        "task_id": task.task_id,
                        "progress": new_progress,
                        "blockers": blockers,
                        "cycle": self.current_cycle
                    })
                    
                    if self.reporting_manager and self.comm_system:
                        progress_message = self.reporting_manager.format_progress_update_message(
                            task, new_progress, blockers
                        )
                        await self.comm_system.send_message_to_agent(
                            task.claimed_by, progress_message, "status_box"
                        )
                    
                    if task.status == "completed":
                        self.workflow_stats["tasks_completed"] += 1
                        self.agent_coordinator.update_agent_workload(
                            task.claimed_by, task.task_id, "complete"
                        )
                        
                        # Emit task completion event
                        self.emit_event("task_completed", {
                            "task_id": task.task_id,
                            "agent_id": task.claimed_by,
                            "cycle": self.current_cycle
                        })
                        
        except Exception as e:
            self.logger.error(f"❌ Error in work progress simulation: {e}")
    
    async def _broadcast_no_tasks_available(self):
        """Broadcast when no tasks are available"""
        if not self.reporting_manager or not self.comm_system:
            return
        
        try:
            message = self.reporting_manager.format_no_tasks_message()
            await self.comm_system.send_message_to_all_agents_with_line_breaks(
                message, "status_box"
            )
            
            self.logger.info("📝 Broadcasted: No tasks available")
            
        except Exception as e:
            self.logger.error(f"❌ Error broadcasting no tasks message: {e}")
    
    async def stop_overnight_workflow(self):
        """Stop autonomous overnight workflow"""
        self.logger.info("🛑 Stopping autonomous overnight workflow...")
        self.workflow_active = False
        
        # Emit workflow stop event
        self.emit_event("workflow_stopped", {
            "stop_time": datetime.now().isoformat(),
            "total_cycles": self.total_cycles,
            "total_hours": self.workflow_stats["autonomous_hours"]
        })
        
        if self.reporting_manager and self.comm_system:
            try:
                final_message = self.reporting_manager.format_workflow_complete_message()
                await self.comm_system.send_message_to_all_agents_with_line_breaks(
                    final_message, "workspace_box"
                )
            except Exception as e:
                self.logger.error(f"❌ Error sending final workflow message: {e}")
        
        self.logger.info("✅ Workflow stopped successfully")
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status"""
        return {
            "active": self.workflow_active,
            "current_cycle": self.current_cycle,
            "total_cycles": self.total_cycles,
            "cycle_duration": self.cycle_duration,
            "stats": self.workflow_stats.copy(),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "uptime": self.get_uptime()
        }
    
    def reset_workflow_stats(self):
        """Reset workflow statistics"""
        self.workflow_stats = {
            "overnight_cycles": 0,
            "autonomous_hours": 0,
            "tasks_claimed": 0,
            "tasks_completed": 0,
            "workflow_errors": 0
        }
        self.current_cycle = 0
        self.total_cycles = 0
        
        self.logger.info("✅ Workflow statistics reset")
        
        # Emit reset event
        self.emit_event("workflow_stats_reset", {
            "reset_time": datetime.now().isoformat()
        })
    
    def update_cycle_duration(self, new_duration: int):
        """Update workflow cycle duration"""
        if new_duration > 0:
            self.cycle_duration = new_duration
            self.logger.info(f"✅ Cycle duration updated to {new_duration} seconds")
            
            # Emit configuration change event
            self.emit_event("workflow_config_changed", {
                "cycle_duration": new_duration,
                "change_time": datetime.now().isoformat()
            })
        else:
            self.logger.warning("❌ Invalid cycle duration: must be positive")
    
    def get_workflow_metrics(self) -> Dict[str, Any]:
        """Get workflow performance metrics"""
        return {
            "total_cycles": self.total_cycles,
            "total_hours": self.workflow_stats["autonomous_hours"],
            "tasks_claimed": self.workflow_stats["tasks_claimed"],
            "tasks_completed": self.workflow_stats["tasks_completed"],
            "completion_rate": (
                self.workflow_stats["tasks_completed"] / max(self.workflow_stats["tasks_claimed"], 1)
            ),
            "error_rate": (
                self.workflow_stats["workflow_errors"] / max(self.total_cycles, 1)
            ),
            "uptime": self.get_uptime()
        }


