"""
Autonomous Workflow Strategy - V2 Compliant
==========================================

Autonomous execution strategy with adaptive behavior.
Separated from strategies.py for V2 compliance (file size limit).

V2 Compliance: ≤400 lines, SOLID principles, comprehensive type hints.

Author: Agent-1 - Workflow Orchestration Specialist
License: MIT
"""

import asyncio
import logging
from typing import Any

from .models import ResponseType, WorkflowStep
from .strategies import WorkflowStrategy


class AutonomousStrategy(WorkflowStrategy):
    """
    Autonomous execution strategy.

    Executes steps with adaptive behavior based on responses.
    Supports goal-oriented iteration and self-correction.
    """

    def __init__(self, max_iterations: int = 10):
        super().__init__("Autonomous")
        self.max_iterations = max_iterations

    async def execute_workflow(
        self,
        steps: list[WorkflowStep],
        workflow_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute workflow autonomously with adaptation."""
        completed_steps: set[str] = set()
        failed_steps: set[str] = set()
        results = {}
        iterations = 0

        self.logger.info(f"Starting autonomous execution of {len(steps)} steps")

        # Autonomous loop with adaptation
        while iterations < self.max_iterations and len(completed_steps) + len(failed_steps) < len(
            steps
        ):
            iterations += 1
            self.logger.info(f"Autonomous iteration {iterations}")

            # Find executable steps
            executable_steps = [
                step for step in steps if self.can_execute_step(step, completed_steps, failed_steps)
            ]

            if not executable_steps:
                self.logger.info("No executable steps found, autonomous workflow complete")
                break

            # Execute steps with adaptive behavior
            for step in executable_steps:
                try:
                    result = await self._execute_step_autonomously(step, workflow_data, iterations)
                    completed_steps.add(step.id)
                    results[step.id] = {"status": "completed", "result": result}
                except Exception as e:
                    self.logger.error(f"Autonomous step {step.id} failed: {e}")
                    failed_steps.add(step.id)
                    results[step.id] = {"status": "failed", "error": str(e)}

        return {
            "strategy": self.name,
            "completed_steps": list(completed_steps),
            "failed_steps": list(failed_steps),
            "results": results,
            "iterations": iterations,
        }

    def can_execute_step(
        self,
        step: WorkflowStep,
        completed_steps: set[str],
        failed_steps: set[str],
    ) -> bool:
        """Check if step can be executed (dependencies satisfied)."""
        return step.is_ready(completed_steps)

    async def _execute_step_autonomously(
        self,
        step: WorkflowStep,
        workflow_data: dict[str, Any],
        iteration: int,
    ) -> Any:
        """Execute step with autonomous behavior."""
        self.logger.info(
            f"Autonomous execution of step {step.id}: {step.name} (iteration {iteration})"
        )

        # Adaptive behavior based on step type and iteration
        if step.expected_response_type == ResponseType.GOAL_ASSESSMENT:
            # Goal assessment gets more context with each iteration
            workflow_data["iteration"] = iteration
            workflow_data["previous_results"] = workflow_data.get("results", {})

        # Simulate adaptive execution
        await asyncio.sleep(0.1)
        return f"Autonomous result of {step.name} (iteration {iteration})"

