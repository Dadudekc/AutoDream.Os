"""
Orchestrator Execution Logic
=============================

Cycle and task execution for overnight orchestrator.

Author: Agent-6 (Quality Gates & VSCode Forking Specialist)
Refactored from: orchestrator.py (OvernightOrchestrator class split)
License: MIT
"""

import asyncio
import time
from typing import Any


class OrchestratorExecution:
    """Handles cycle and task execution."""

    def __init__(self, logger, config, scheduler, monitor, send_message_func):
        """Initialize execution handler."""
        self.logger = logger
        self.config = config
        self.scheduler = scheduler
        self.monitor = monitor
        self.send_message = send_message_func

        overnight_config = config.get("overnight", {})
        self.messaging_integration = overnight_config.get("integration", {}).get(
            "messaging_system", True
        )

    async def execute_cycle(self, cycle_number: int) -> None:
        """Execute a single cycle of autonomous operations."""
        try:
            tasks = await self.scheduler.get_cycle_tasks(cycle_number)

            if not tasks:
                self.logger.info(f"No tasks scheduled for cycle {cycle_number}")
                return

            self.logger.info(f"Executing {len(tasks)} tasks in cycle {cycle_number}")

            for task in tasks:
                await self.distribute_task(task, cycle_number)

            self.monitor.update_tasks(tasks)

        except Exception as e:
            self.logger.error(f"Cycle execution failed: {e}")
            raise

    async def distribute_task(self, task: dict[str, Any], cycle_number: int) -> None:
        """Distribute a task to an agent."""
        try:
            agent_id = task.get("agent_id")
            task_type = task.get("type")
            task_data = task.get("data", {})

            if not agent_id:
                self.logger.warning("Task missing agent_id, skipping")
                return

            message = self._create_task_message(task_type, task_data, cycle_number)

            if self.messaging_integration:
                success = await asyncio.get_event_loop().run_in_executor(
                    None, self.send_message, agent_id, message
                )

                if success:
                    self.logger.info(f"Task distributed to {agent_id}: {task_type}")
                else:
                    self.logger.error(f"Failed to distribute task to {agent_id}")

        except Exception as e:
            self.logger.error(f"Task distribution failed: {e}")

    @staticmethod
    def _create_task_message(task_type: str, task_data: dict[str, Any], cycle_number: int) -> str:
        """Create task message for agent."""
        return f"""
[OVERNIGHT TASK] Cycle {cycle_number}
Type: {task_type}
Data: {task_data}
Timestamp: {time.time()}

Execute this task autonomously. Report completion or issues.
"""
