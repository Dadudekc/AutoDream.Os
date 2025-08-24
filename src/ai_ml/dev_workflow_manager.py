"""Development workflow manager handling execution logic."""
from __future__ import annotations

import subprocess
import time
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class WorkflowStep:
    """A step in the development workflow."""

    name: str
    description: str
    command: str
    dependencies: List[str] = field(default_factory=list)
    timeout: int = 300
    retry_count: int = 3
    required: bool = True
    ai_assisted: bool = False


@dataclass
class WorkflowResult:
    """Result of a workflow step."""

    step_name: str
    success: bool
    output: str
    error: Optional[str] = None
    execution_time: float = 0.0
    ai_suggestions: List[str] = field(default_factory=list)


class DevWorkflowManager:
    """Execute workflow steps and manage results."""

    def __init__(self, project_path: Path, processor, coordinator):
        self.project_path = Path(project_path)
        self.processor = processor
        self.coordinator = coordinator

    def execute_workflow(self, workflow_name: str, **kwargs) -> Dict[str, WorkflowResult]:
        """Execute a named workflow and return step results."""
        steps = self.coordinator.get_workflow(workflow_name)
        results: Dict[str, WorkflowResult] = {}
        for step in steps:
            result = self._execute_step(step, **kwargs)
            results[step.name] = result
            if not result.success and step.required:
                break
        return results

    def _execute_step(self, step: WorkflowStep, **kwargs) -> WorkflowResult:
        start = time.time()
        try:
            if step.ai_assisted:
                output = self.processor.execute_ai_assisted_step(
                    step, self.project_path, **kwargs
                )
            else:
                output = self._execute_command(step.command, step.timeout)
            exec_time = time.time() - start
            suggestions: List[str] = []
            if step.ai_assisted:
                suggestions = self.processor.get_ai_suggestions(step, output)
            return WorkflowResult(
                step_name=step.name,
                success=True,
                output=output,
                execution_time=exec_time,
                ai_suggestions=suggestions,
            )
        except subprocess.TimeoutExpired:
            return WorkflowResult(
                step_name=step.name,
                success=False,
                output="",
                error=f"Step timed out after {step.timeout} seconds",
                execution_time=time.time() - start,
            )
        except Exception as e:  # pragma: no cover - safety catch
            return WorkflowResult(
                step_name=step.name,
                success=False,
                output="",
                error=str(e),
                execution_time=time.time() - start,
            )

    def _execute_command(self, command: str, timeout: int) -> str:
        """Execute shell command safely."""
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=self.project_path,
        )
        if result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode, command, result.stdout, result.stderr
            )
        return result.stdout
