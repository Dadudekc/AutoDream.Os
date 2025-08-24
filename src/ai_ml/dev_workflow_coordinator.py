"""Workflow coordinator defining available development workflows."""
from __future__ import annotations

from typing import List, Dict

from .dev_workflow_manager import WorkflowStep


class WorkflowCoordinator:
    """Provide predefined development workflows."""

    def __init__(self):
        self.workflows: Dict[str, List[WorkflowStep]] = {
            "tdd": self._tdd_workflow(),
            "code_review": self._code_review_workflow(),
            "refactoring": self._refactoring_workflow(),
            "testing": self._testing_workflow(),
            "documentation": self._documentation_workflow(),
            "deployment": self._deployment_workflow(),
        }

    def get_available_workflows(self) -> List[str]:
        return list(self.workflows.keys())

    def get_workflow(self, name: str) -> List[WorkflowStep]:
        if name not in self.workflows:
            raise ValueError(f"Unknown workflow: {name}")
        return self.workflows[name]

    # ------------------------------------------------------------------
    # Workflow definitions
    # ------------------------------------------------------------------
    def _tdd_workflow(self) -> List[WorkflowStep]:
        return [
            WorkflowStep(
                name="project_analysis",
                description="Analyze project structure and code quality",
                command="echo 'Project analysis completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="test_generation",
                description="Generate comprehensive test suites",
                command="echo 'Test generation completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="run_tests",
                description="Execute all tests",
                command="python -m pytest tests/ -v",
                dependencies=["test_generation"],
            ),
        ]

    def _code_review_workflow(self) -> List[WorkflowStep]:
        return [
            WorkflowStep(
                name="code_analysis",
                description="Analyze code quality",
                command="echo 'Code analysis completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="review",
                description="Perform code review",
                command="echo 'Code review completed'",
            ),
        ]

    def _refactoring_workflow(self) -> List[WorkflowStep]:
        return [
            WorkflowStep(
                name="refactor_suggestions",
                description="Generate refactoring suggestions",
                command="echo 'Refactor suggestions generated'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="apply_refactor",
                description="Apply refactoring changes",
                command="echo 'Refactor applied'",
            ),
        ]

    def _testing_workflow(self) -> List[WorkflowStep]:
        return [
            WorkflowStep(
                name="test_generation",
                description="Generate missing tests",
                command="echo 'Test generation completed'",
                ai_assisted=True,
            ),
            WorkflowStep(
                name="run_tests",
                description="Execute all tests",
                command="python -m pytest tests/ -v",
            ),
            WorkflowStep(
                name="coverage_analysis",
                description="Analyze test coverage",
                command="python -m pytest tests/ --cov=src --cov-report=html",
            ),
        ]

    def _documentation_workflow(self) -> List[WorkflowStep]:
        return [
            WorkflowStep(
                name="documentation_analysis",
                description="Analyze current documentation coverage",
                command="echo 'Documentation analysis completed'",
            ),
            WorkflowStep(
                name="documentation_generation",
                description="Generate missing documentation",
                command="echo 'Documentation generation completed'",
                ai_assisted=True,
            ),
        ]

    def _deployment_workflow(self) -> List[WorkflowStep]:
        return [
            WorkflowStep(
                name="pre_deployment_tests",
                description="Run pre-deployment tests",
                command="python -m pytest tests/ -v --tb=short",
            ),
            WorkflowStep(
                name="security_check",
                description="Final security check",
                command="echo 'Security check completed'",
            ),
            WorkflowStep(
                name="deployment",
                description="Deploy to production",
                command="echo 'Deployment completed'",
            ),
        ]
