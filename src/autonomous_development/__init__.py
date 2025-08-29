"""
Autonomous Development Package

This package provides autonomous development capabilities including:
- Workflow management and orchestration
- Task scheduling and execution
- Code generation and analysis
- Testing orchestration and reporting

Extracted from src/core/autonomous_development.py to follow SRP.
"""

# Import the extracted modules
from .workflow.engine import WorkflowEngine
from .tasks.manager import TaskManager, Task, TaskStatus, TaskPriority
from .code.generator import CodeGenerator, CodeImprovement, CursorAgentPrompt
from .testing.orchestrator import TestingOrchestrator
from .testing.testing_utils import TestResult
from .testing.result_collation import TestSuite

__all__ = [
    # Workflow management
    'WorkflowEngine',

    # Task management
    'TaskManager',
    'Task',
    'TaskStatus',
    'TaskPriority',

    # Code generation and analysis
    'CodeGenerator',
    'CodeImprovement',
    'CursorAgentPrompt',

    # Testing orchestration
    'TestingOrchestrator',
    'TestResult',
    'TestSuite'
]
