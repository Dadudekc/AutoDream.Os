"""
Clone Automation Scripts for Team Beta Mission
Agent-7 Repository Cloning Specialist - Automated Repository Cloning

V2 Compliance: ≤400 lines, type hints, KISS principle
"""

import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class CloneTask:
    """Clone task structure."""

    name: str
    url: str
    local_path: str
    priority: int
    dependencies: list[str]
    status: str
    progress: float
    errors: list[str]


@dataclass
class CloneResult:
    """Clone operation result."""

    task: CloneTask
    success: bool
    duration: float
    files_cloned: int
    errors: list[str]
    warnings: list[str]


class CloneAutomation:
    """
    Clone automation system for Team Beta mission.

    Provides automated repository cloning with error handling,
    dependency management, and progress tracking.
    """

    def __init__(self, base_path: str = "./repositories"):
        """Initialize clone automation system."""
        self.base_path = Path(base_path)
        self.tasks: list[CloneTask] = []
        self.results: list[CloneResult] = []
        self._initialize_clone_tasks()

    def _initialize_clone_tasks(self):
        """Initialize clone tasks for Team Beta mission."""
        self.tasks = [
            CloneTask(
                name="vscode",
                url="https://github.com/microsoft/vscode.git",
                local_path=str(self.base_path / "vscode"),
                priority=1,
                dependencies=["nodejs", "npm", "typescript"],
                status="pending",
                progress=0.0,
                errors=[],
            ),
            CloneTask(
                name="autodream-os",
                url="https://github.com/Dadudekc/AutoDream.Os.git",
                local_path=str(self.base_path / "autodream-os"),
                priority=1,
                dependencies=["python", "pip", "pytest"],
                status="pending",
                progress=0.0,
                errors=[],
            ),
            CloneTask(
                name="agent-cellphone-v2",
                url="https://github.com/Dadudekc/Agent_Cellphone_V2_Repository.git",
                local_path=str(self.base_path / "agent-cellphone-v2"),
                priority=1,
                dependencies=["python", "pip", "pytest"],
                status="pending",
                progress=0.0,
                errors=[],
            ),
            CloneTask(
                name="vscode-extensions",
                url="https://github.com/microsoft/vscode-extensions.git",
                local_path=str(self.base_path / "vscode-extensions"),
                priority=2,
                dependencies=["nodejs", "npm"],
                status="pending",
                progress=0.0,
                errors=[],
            ),
        ]

    def check_dependencies(self, task: CloneTask) -> tuple[bool, list[str]]:
        """Check if all dependencies are available."""
        missing = []

        for dep in task.dependencies:
            if dep == "nodejs":
                if not self._check_command("node --version"):
                    missing.append("Node.js")
            elif dep == "python":
                if not self._check_command("python --version"):
                    missing.append("Python")
            elif dep == "npm":
                if not self._check_command("npm --version"):
                    missing.append("npm")
            elif dep == "pip":
                if not self._check_command("pip --version"):
                    missing.append("pip")
            elif dep == "typescript":
                if not self._check_command("tsc --version"):
                    missing.append("TypeScript")
            elif dep == "pytest":
                if not self._check_command("pytest --version"):
                    missing.append("pytest")

        return len(missing) == 0, missing

    def _check_command(self, command: str) -> bool:
        """Check if a command is available."""
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def clone_repository(self, task: CloneTask) -> CloneResult:
        """Clone a single repository with progress tracking."""
        start_time = time.time()
        errors = []
        warnings = []
        files_cloned = 0

        try:
            # Update task status
            task.status = "cloning"
            task.progress = 10.0

            # Check dependencies
            deps_ok, missing_deps = self.check_dependencies(task)
            if not deps_ok:
                errors.append(f"Missing dependencies: {', '.join(missing_deps)}")
                task.status = "failed"
                task.progress = 0.0
            else:
                task.progress = 20.0

                # Ensure base path exists
                self.base_path.mkdir(parents=True, exist_ok=True)
                task.progress = 30.0

                # Clone repository
                clone_cmd = ["git", "clone", task.url, task.local_path]
                result = subprocess.run(clone_cmd, capture_output=True, text=True)
                task.progress = 80.0

                if result.returncode == 0:
                    task.status = "completed"
                    task.progress = 100.0
                    files_cloned = self._count_files(task.local_path)
                    warnings.append("Repository cloned successfully")
                else:
                    task.status = "failed"
                    task.progress = 0.0
                    errors.append(f"Clone failed: {result.stderr}")

        except Exception as e:
            task.status = "failed"
            task.progress = 0.0
            errors.append(f"Clone exception: {str(e)}")

        duration = time.time() - start_time

        clone_result = CloneResult(
            task=task,
            success=task.status == "completed",
            duration=duration,
            files_cloned=files_cloned,
            errors=errors,
            warnings=warnings,
        )

        self.results.append(clone_result)
        return clone_result

    def _count_files(self, path: str) -> int:
        """Count files in cloned repository."""
        try:
            return sum(1 for _ in Path(path).rglob("*") if _.is_file())
        except Exception:
            return 0

    def run_all_clones(self) -> dict[str, Any]:
        """Run all clone operations in priority order."""
        print("🚀 Starting Team Beta Repository Cloning Operations...")

        # Sort tasks by priority
        sorted_tasks = sorted(self.tasks, key=lambda t: t.priority)

        results_summary = {
            "total_tasks": len(sorted_tasks),
            "completed": 0,
            "failed": 0,
            "total_duration": 0.0,
            "total_files": 0,
            "errors": [],
            "warnings": [],
        }

        for i, task in enumerate(sorted_tasks, 1):
            print(f"\n📋 Task {i}/{len(sorted_tasks)}: Cloning {task.name}")
            print(f"   URL: {task.url}")
            print(f"   Path: {task.local_path}")
            print(f"   Dependencies: {', '.join(task.dependencies)}")

            result = self.clone_repository(task)

            if result.success:
                results_summary["completed"] += 1
                print(f"   ✅ SUCCESS: {result.files_cloned} files cloned in {result.duration:.2f}s")
                results_summary["total_files"] += result.files_cloned
            else:
                results_summary["failed"] += 1
                print(f"   ❌ FAILED: {', '.join(result.errors)}")
                results_summary["errors"].extend(result.errors)

            results_summary["total_duration"] += result.duration
            results_summary["warnings"].extend(result.warnings)

        return results_summary

    def get_task_by_name(self, name: str) -> CloneTask | None:
        """Get clone task by name."""
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def get_tasks_by_status(self, status: str) -> list[CloneTask]:
        """Get tasks by status."""
        return [task for task in self.tasks if task.status == status]

    def get_failed_tasks(self) -> list[CloneTask]:
        """Get failed clone tasks."""
        return [task for task in self.tasks if task.status == "failed"]

    def create_progress_report(self) -> dict[str, Any]:
        """Create comprehensive progress report."""
        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_tasks": len(self.tasks),
            "tasks_by_status": {
                "pending": len(self.get_tasks_by_status("pending")),
                "cloning": len(self.get_tasks_by_status("cloning")),
                "completed": len(self.get_tasks_by_status("completed")),
                "failed": len(self.get_tasks_by_status("failed")),
            },
            "results_summary": {
                "total_attempts": len(self.results),
                "successful": len([r for r in self.results if r.success]),
                "failed": len([r for r in self.results if not r.success]),
                "total_files_cloned": sum(r.files_cloned for r in self.results),
                "total_duration": sum(r.duration for r in self.results),
            },
            "tasks": [
                {
                    "name": task.name,
                    "status": task.status,
                    "progress": task.progress,
                    "errors": task.errors,
                    "dependencies": task.dependencies,
                }
                for task in self.tasks
            ],
        }

    def export_progress_report(self, filepath: str) -> bool:
        """Export progress report to JSON file."""
        try:
            report = self.create_progress_report()
            with open(filepath, "w") as f:
                json.dump(report, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting progress report: {e}")
            return False


def main():
    """Main execution function for clone automation."""
    print("🎯 Agent-7 Repository Cloning Specialist - Clone Automation")
    print("=" * 60)

    # Create clone automation instance
    automation = CloneAutomation()

    # Run all clone operations
    results = automation.run_all_clones()

    # Print summary
    print("\n" + "=" * 60)
    print("📊 CLONE OPERATION SUMMARY")
    print("=" * 60)
    print(f"Total Tasks: {results['total_tasks']}")
    print(f"Completed: {results['completed']}")
    print(f"Failed: {results['failed']}")
    print(f"Total Files: {results['total_files']}")
    print(f"Total Duration: {results['total_duration']:.2f}s")

    if results["errors"]:
        print(f"\n❌ Errors: {len(results['errors'])}")
        for error in results["errors"]:
            print(f"  - {error}")

    if results["warnings"]:
        print(f"\n⚠️ Warnings: {len(results['warnings'])}")
        for warning in results["warnings"]:
            print(f"  - {warning}")

    # Export progress report
    success = automation.export_progress_report("clone_progress_report.json")
    if success:
        print("\n✅ Progress report exported to clone_progress_report.json")
    else:
        print("\n❌ Failed to export progress report")

    return results["failed"] == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
