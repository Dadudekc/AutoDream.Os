"""
Workflow Strategies - V2 Compliant
=================================

Coordination strategies for multi-agent workflow execution.
Implements different approaches to agent coordination and task distribution.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive type hints.

Author: Agent-1 - Workflow Orchestration Specialist
License: MIT
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any

from .models import ResponseType, WorkflowStep


class WorkflowStrategy(ABC):
    """
    Abstract base class for workflow coordination strategies.

    Defines the interface for different approaches to coordinating
    multi-agent workflow execution.
    """

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")

    @abstractmethod
    async def execute_workflow(
        self,
        steps: list[WorkflowStep],
        workflow_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute workflow using this strategy.

        Args:
            steps: List of workflow steps to execute
            workflow_data: Shared data for workflow execution

        Returns:
            Dictionary containing execution results
        """
        pass

    @abstractmethod
    def can_execute_step(
        self,
        step: WorkflowStep,
        completed_steps: set[str],
        failed_steps: set[str],
    ) -> bool:
        """
        Check if a step can be executed with this strategy.

        Args:
            step: Step to check
            completed_steps: Set of completed step IDs
            failed_steps: Set of failed step IDs

        Returns:
            True if step can be executed
        """
        pass


class ParallelStrategy(WorkflowStrategy):
    """
    Parallel execution strategy.

    Executes all available steps simultaneously when their
    dependencies are satisfied. Maximizes concurrency.
    """

    def __init__(self):
        super().__init__("Parallel")

    async def execute_workflow(
        self,
        steps: list[WorkflowStep],
        workflow_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute workflow in parallel."""
        completed_steps: set[str] = set()
        failed_steps: set[str] = set()
        results = {}

        self.logger.info(f"Starting parallel execution of {len(steps)} steps")

        # Continue until all steps are completed or failed
        while len(completed_steps) + len(failed_steps) < len(steps):
            # Find all steps that can be executed
            executable_steps = [
                step for step in steps if self.can_execute_step(step, completed_steps, failed_steps)
            ]

            if not executable_steps:
                self.logger.warning("No executable steps found, workflow may be deadlocked")
                break

            # Execute all executable steps in parallel
            tasks = [self._execute_step(step, workflow_data) for step in executable_steps]

            step_results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for step, result in zip(executable_steps, step_results, strict=False):
                if isinstance(result, Exception):
                    self.logger.error(f"Step {step.id} failed: {result}")
                    failed_steps.add(step.id)
                    results[step.id] = {"status": "failed", "error": str(result)}
                else:
                    completed_steps.add(step.id)
                    results[step.id] = {"status": "completed", "result": result}

        return {
            "strategy": self.name,
            "completed_steps": list(completed_steps),
            "failed_steps": list(failed_steps),
            "results": results,
        }

    def can_execute_step(
        self,
        step: WorkflowStep,
        completed_steps: set[str],
        failed_steps: set[str],
    ) -> bool:
        """Check if step can be executed (dependencies satisfied)."""
        return step.is_ready(completed_steps)

    async def _execute_step(
        self,
        step: WorkflowStep,
        workflow_data: dict[str, Any],
    ) -> Any:
        """Execute a single step (simplified for demonstration)."""
        self.logger.info(f"Executing step {step.id}: {step.name}")
        # Simulate step execution
        await asyncio.sleep(0.1)
        return f"Result of {step.name}"


class SequentialStrategy(WorkflowStrategy):
    """
    Sequential execution strategy.

    Executes steps one at a time in dependency order.
    Ensures proper sequencing but may be slower.
    """

    def __init__(self):
        super().__init__("Sequential")

    async def execute_workflow(
        self,
        steps: list[WorkflowStep],
        workflow_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute workflow sequentially."""
        completed_steps: set[str] = set()
        failed_steps: set[str] = set()
        results = {}

        self.logger.info(f"Starting sequential execution of {len(steps)} steps")

        # Continue until all steps are completed or failed
        while len(completed_steps) + len(failed_steps) < len(steps):
            # Find next executable step
            next_step = None
            for step in steps:
                if self.can_execute_step(step, completed_steps, failed_steps):
                    next_step = step
                    break

            if not next_step:
                self.logger.warning("No executable steps found, workflow may be deadlocked")
                break

            # Execute the step
            try:
                result = await self._execute_step(next_step, workflow_data)
                completed_steps.add(next_step.id)
                results[next_step.id] = {"status": "completed", "result": result}
                self.logger.info(f"Completed step {next_step.id}: {next_step.name}")
            except Exception as e:
                self.logger.error(f"Step {next_step.id} failed: {e}")
                failed_steps.add(next_step.id)
                results[next_step.id] = {"status": "failed", "error": str(e)}

        return {
            "strategy": self.name,
            "completed_steps": list(completed_steps),
            "failed_steps": list(failed_steps),
            "results": results,
        }

    def can_execute_step(
        self,
        step: WorkflowStep,
        completed_steps: set[str],
        failed_steps: set[str],
    ) -> bool:
        """Check if step can be executed (dependencies satisfied)."""
        return step.is_ready(completed_steps)

    async def _execute_step(
        self,
        step: WorkflowStep,
        workflow_data: dict[str, Any],
    ) -> Any:
        """Execute a single step (simplified for demonstration)."""
        self.logger.info(f"Executing step {step.id}: {step.name}")
        # Simulate step execution
        await asyncio.sleep(0.1)
        return f"Result of {step.name}"


class DecisionTreeStrategy(WorkflowStrategy):
    """
    Decision tree execution strategy.

    Executes decision points first, then branches based on
    the decision results. Supports conditional workflow paths.
    """

    def __init__(self):
        super().__init__("DecisionTree")

    async def execute_workflow(
        self,
        steps: list[WorkflowStep],
        workflow_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute workflow using decision tree strategy."""
        completed_steps: set[str] = set()
        failed_steps: set[str] = set()
        results = {}

        self.logger.info(f"Starting decision tree execution of {len(steps)} steps")

        # Group steps by type
        decision_steps = [
            s for s in steps if s.expected_response_type == ResponseType.DECISION_ANALYSIS
        ]
        branch_steps = [
            s for s in steps if s.expected_response_type == ResponseType.BRANCH_EXECUTION
        ]
        other_steps = [
            s
            for s in steps
            if s.expected_response_type
            not in [ResponseType.DECISION_ANALYSIS, ResponseType.BRANCH_EXECUTION]
        ]

        # Execute decision steps first
        for decision_step in decision_steps:
            if self.can_execute_step(decision_step, completed_steps, failed_steps):
                try:
                    result = await self._execute_step(decision_step, workflow_data)
                    completed_steps.add(decision_step.id)
                    results[decision_step.id] = {"status": "completed", "result": result}

                    # Execute branches based on decision
                    await self._execute_branches(
                        decision_step,
                        branch_steps,
                        workflow_data,
                        completed_steps,
                        failed_steps,
                        results,
                    )
                except Exception as e:
                    self.logger.error(f"Decision step {decision_step.id} failed: {e}")
                    failed_steps.add(decision_step.id)
                    results[decision_step.id] = {"status": "failed", "error": str(e)}

        # Execute remaining steps
        for step in other_steps:
            if self.can_execute_step(step, completed_steps, failed_steps):
                try:
                    result = await self._execute_step(step, workflow_data)
                    completed_steps.add(step.id)
                    results[step.id] = {"status": "completed", "result": result}
                except Exception as e:
                    self.logger.error(f"Step {step.id} failed: {e}")
                    failed_steps.add(step.id)
                    results[step.id] = {"status": "failed", "error": str(e)}

        return {
            "strategy": self.name,
            "completed_steps": list(completed_steps),
            "failed_steps": list(failed_steps),
            "results": results,
        }

    def can_execute_step(
        self,
        step: WorkflowStep,
        completed_steps: set[str],
        failed_steps: set[str],
    ) -> bool:
        """Check if step can be executed (dependencies satisfied)."""
        return step.is_ready(completed_steps)

    async def _execute_step(
        self,
        step: WorkflowStep,
        workflow_data: dict[str, Any],
    ) -> Any:
        """Execute a single step (simplified for demonstration)."""
        self.logger.info(f"Executing step {step.id}: {step.name}")
        # Simulate step execution
        await asyncio.sleep(0.1)
        return f"Result of {step.name}"

    async def _execute_branches(
        self,
        decision_step: WorkflowStep,
        branch_steps: list[WorkflowStep],
        workflow_data: dict[str, Any],
        completed_steps: set[str],
        failed_steps: set[str],
        results: dict[str, Any],
    ) -> None:
        """Execute branches based on decision result."""
        # Find branches that depend on this decision
        dependent_branches = [
            step for step in branch_steps if decision_step.id in step.dependencies
        ]

        # Execute branches in parallel
        if dependent_branches:
            tasks = [self._execute_step(step, workflow_data) for step in dependent_branches]

            branch_results = await asyncio.gather(*tasks, return_exceptions=True)

            for step, result in zip(dependent_branches, branch_results, strict=False):
                if isinstance(result, Exception):
                    self.logger.error(f"Branch step {step.id} failed: {result}")
                    failed_steps.add(step.id)
                    results[step.id] = {"status": "failed", "error": str(result)}
                else:
                    completed_steps.add(step.id)
                    results[step.id] = {"status": "completed", "result": result}


# Note: AutonomousStrategy moved to autonomous_strategy.py for V2 compliance
