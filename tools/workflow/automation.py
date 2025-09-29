#!/usr/bin/env python3
"""
Agent Workflow Automation
=========================

Automated workflow execution and task management for agents.
V2 Compliance: ≤400 lines, focused automation functionality.
"""

import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.consolidated_messaging_service import ConsolidatedMessagingService
from tools.workflow.core import WorkflowStep

logger = logging.getLogger(__name__)


class ModuleFixer:
    """Handles fixing missing imports and module issues."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.logger = logging.getLogger(f"{__name__}.ModuleFixer")

    def fix_missing_imports(self, module_path: str) -> bool:
        """Fix missing imports by creating necessary __init__.py files."""
        try:
            module_path = Path(module_path)
            if not module_path.exists():
                self.logger.error(f"Module path {module_path} does not exist")
                return False

            # Create __init__.py files for all directories in the path
            current_path = self.project_root
            for part in module_path.parts:
                current_path = current_path / part
                if current_path.is_dir() and not (current_path / "__init__.py").exists():
                    init_file = current_path / "__init__.py"
                    init_file.write_text('"""Auto-generated __init__.py file."""\n')
                    self.logger.info(f"Created {init_file}")

            return True
        except Exception as e:
            self.logger.error(f"Error fixing imports for {module_path}: {e}")
            return False

    def validate_module_structure(self, module_path: str) -> list[str]:
        """Validate module structure and return list of issues."""
        issues = []
        module_path = Path(module_path)

        if not module_path.exists():
            issues.append(f"Module path does not exist: {module_path}")
            return issues

        # Check for __init__.py files
        for root, dirs, files in module_path.rglob("*"):
            if Path(root).is_dir() and "__init__.py" not in files:
                issues.append(f"Missing __init__.py in: {root}")

        return issues


class TestRunner:
    """Handles running tests and validation."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.logger = logging.getLogger(f"{__name__}.TestRunner")

    def run_pytest(self, test_path: str = "tests/") -> dict[str, Any]:
        """Run pytest on specified test path."""
        try:
            cmd = [sys.executable, "-m", "pytest", test_path, "-v", "--tb=short"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except Exception as e:
            self.logger.error(f"Error running pytest: {e}")
            return {"success": False, "error": str(e), "returncode": -1}

    def run_syntax_check(self, file_path: str) -> bool:
        """Run syntax check on a Python file."""
        try:
            cmd = [sys.executable, "-m", "py_compile", file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Error checking syntax for {file_path}: {e}")
            return False


class ProjectManager:
    """Handles project management tasks."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.logger = logging.getLogger(f"{__name__}.ProjectManager")

    def get_project_status(self) -> dict[str, Any]:
        """Get overall project status."""
        status = {
            "project_root": str(self.project_root),
            "python_files": 0,
            "test_files": 0,
            "total_files": 0,
            "last_modified": None,
        }

        try:
            for file_path in self.project_root.rglob("*.py"):
                status["total_files"] += 1
                if file_path.name.endswith(".py"):
                    status["python_files"] += 1
                if "test" in file_path.name.lower():
                    status["test_files"] += 1

                # Track last modified
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if status["last_modified"] is None or mtime > status["last_modified"]:
                    status["last_modified"] = mtime

            if status["last_modified"]:
                status["last_modified"] = status["last_modified"].isoformat()

        except Exception as e:
            self.logger.error(f"Error getting project status: {e}")
            status["error"] = str(e)

        return status

    def cleanup_temp_files(self) -> int:
        """Clean up temporary files and return count of files removed."""
        temp_patterns = ["*.pyc", "__pycache__", "*.tmp", ".pytest_cache"]
        removed_count = 0

        try:
            for pattern in temp_patterns:
                for file_path in self.project_root.rglob(pattern):
                    if file_path.is_file():
                        file_path.unlink()
                        removed_count += 1
                    elif file_path.is_dir():
                        import shutil

                        shutil.rmtree(file_path)
                        removed_count += 1
        except Exception as e:
            self.logger.error(f"Error cleaning up temp files: {e}")

        return removed_count


class WorkflowAutomation:
    """Main automation class for agent workflows."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.project_root = project_root
        self.messaging_service = ConsolidatedMessagingService()

        # Initialize components
        self.module_fixer = ModuleFixer(self.project_root)
        self.test_runner = TestRunner(self.project_root)
        self.project_manager = ProjectManager(self.project_root)

    def execute_workflow_step(self, step: WorkflowStep) -> dict[str, Any]:
        """Execute a single workflow step."""
        self.logger.info(f"Executing step: {step.step_id} - {step.task}")

        step.started_at = datetime.now()
        step.status = "in_progress"

        try:
            result = self._execute_task(step.task, step.agent_id)
            step.result = result
            step.status = "completed"
            step.completed_at = datetime.now()

            self.logger.info(f"Completed step: {step.step_id}")
            return {"success": True, "result": result}

        except Exception as e:
            step.error = str(e)
            step.status = "failed"
            step.completed_at = datetime.now()

            self.logger.error(f"Failed step: {step.step_id} - {e}")
            return {"success": False, "error": str(e)}

    def _execute_task(self, task: str, agent_id: str) -> Any:
        """Execute a specific task based on task description."""
        task_lower = task.lower()

        if "fix imports" in task_lower or "missing imports" in task_lower:
            # Extract module path from task
            module_path = self._extract_module_path(task)
            return self.module_fixer.fix_missing_imports(module_path)

        elif "run tests" in task_lower or "test" in task_lower:
            test_path = self._extract_test_path(task)
            return self.test_runner.run_pytest(test_path)

        elif "syntax check" in task_lower:
            file_path = self._extract_file_path(task)
            return self.test_runner.run_syntax_check(file_path)

        elif "project status" in task_lower:
            return self.project_manager.get_project_status()

        elif "cleanup" in task_lower:
            return self.project_manager.cleanup_temp_files()

        else:
            raise ValueError(f"Unknown task: {task}")

    def _extract_module_path(self, task: str) -> str:
        """Extract module path from task description."""
        # Simple extraction - look for paths in the task
        words = task.split()
        for word in words:
            if "/" in word or "\\" in word:
                return word
        return "src"  # Default fallback

    def _extract_test_path(self, task: str) -> str:
        """Extract test path from task description."""
        words = task.split()
        for word in words:
            if "test" in word.lower():
                return word
        return "tests/"  # Default fallback

    def _extract_file_path(self, task: str) -> str:
        """Extract file path from task description."""
        words = task.split()
        for word in words:
            if word.endswith(".py"):
                return word
        return ""  # No file found
