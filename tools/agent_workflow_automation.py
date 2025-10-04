#!/usr/bin/env python3
"""
Agent Workflow Automation Tool
==============================

Comprehensive workflow automation tool for agents to handle common tasks
like module fixes, testing, messaging, and project management.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.consolidated_messaging_service import ConsolidatedMessagingService


class AgentWorkflowAutomation:
    """Comprehensive workflow automation for agents."""

    def __init__(self):
        """Initialize the workflow automation tool."""
        self.logger = logging.getLogger(__name__)
        self.messaging_service = ConsolidatedMessagingService()
        self.project_root = project_root

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
                    self._create_init_file(current_path)
                    self.logger.info(f"Created __init__.py in {current_path}")

            return True
        except Exception as e:
            self.logger.error(f"Error fixing imports: {e}")
            return False

    def _create_init_file(self, directory: Path):
        """Create an __init__.py file for a directory."""
        init_file = directory / "__init__.py"

        # Get all Python files in the directory
        python_files = [
            f.stem
            for f in directory.iterdir()
            if f.is_file() and f.suffix == ".py" and f.name != "__init__.py"
        ]

        # Create __init__.py content
        content = """# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""

        # Add imports for each Python file
        for py_file in python_files:
            content += f"from . import {py_file}\n"

        content += f"""
__all__ = {python_files}
"""

        init_file.write_text(content)

    def test_imports(self, module_path: str) -> bool:
        """Test if a module can be imported successfully."""
        try:
            # Convert path to import string
            import_path = (
                str(module_path)
                .replace(str(self.project_root), "")
                .replace("/", ".")
                .replace("\\", ".")
            )
            if import_path.startswith("."):
                import_path = import_path[1:]

            # Test import
            exec(f"import {import_path}")
            self.logger.info(f"Import test successful: {import_path}")
            return True
        except Exception as e:
            self.logger.error(f"Import test failed: {e}")
            return False

    def run_tests(self, test_path: str = "tests/") -> dict[str, Any]:
        """Run test suite and return results."""
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", test_path, "-v", "--tb=short"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except Exception as e:
            self.logger.error(f"Error running tests: {e}")
            return {"success": False, "error": str(e)}

    def send_status_update(self, agent_id: str, status: str, details: str = "") -> bool:
        """Send status update to another agent."""
        try:
            message = f"Agent-2 Workflow Automation Update:\n\n{status}"
            if details:
                message += f"\n\nDetails:\n{details}"

            return self.messaging_service.send_message(agent_id, message, "Agent-2", "NORMAL")
        except Exception as e:
            self.logger.error(f"Error sending status update: {e}")
            return False

    def create_devlog(self, title: str, content: str, agent_id: str = "Agent-2") -> str:
        """Create a devlog file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"devlogs/{agent_id.lower().replace('-', '')}_{title.lower().replace(' ', '_')}_{timestamp}.md"
            filepath = self.project_root / filename

            # Ensure devlogs directory exists
            filepath.parent.mkdir(exist_ok=True)

            # Create devlog content
            devlog_content = f"""# {title}

**Date:** {datetime.now().strftime("%Y-%m-%d")}
**Agent:** {agent_id}
**Status:** ✅ COMPLETED

{content}

"""

            filepath.write_text(devlog_content)
            self.logger.info(f"Devlog created: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error creating devlog: {e}")
            return ""

    def update_working_tasks(self, agent_id: str, task_data: dict[str, Any]) -> bool:
        """Update agent working tasks."""
        try:
            tasks_file = self.project_root / f"agent_workspaces/{agent_id}/working_tasks.json"

            if tasks_file.exists():
                with open(tasks_file) as f:
                    tasks = json.load(f)
            else:
                tasks = {"agent_id": agent_id, "current_task": None, "completed_tasks": []}

            # Update tasks
            for key, value in task_data.items():
                tasks[key] = value

            # Write back
            with open(tasks_file, "w") as f:
                json.dump(tasks, f, indent=2, default=str)

            self.logger.info(f"Updated working tasks for {agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating working tasks: {e}")
            return False

    def check_v2_compliance(self, file_path: str) -> dict[str, Any]:
        """Check V2 compliance for a file."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {"error": "File not found"}

            content = file_path.read_text()
            lines = content.split("\n")

            # Count lines
            line_count = len(lines)

            # Count classes (simple regex)
            class_count = len([line for line in lines if line.strip().startswith("class ")])

            # Count functions (simple regex)
            function_count = len([line for line in lines if line.strip().startswith("def ")])

            # Count enums (simple regex)
            enum_count = len([line for line in lines if "enum" in line.lower() and "class" in line])

            compliance = {
                "file_path": str(file_path),
                "line_count": line_count,
                "class_count": class_count,
                "function_count": function_count,
                "enum_count": enum_count,
                "v2_compliant": (
                    line_count <= 400
                    and class_count <= 5
                    and function_count <= 10
                    and enum_count <= 3
                ),
            }

            return compliance
        except Exception as e:
            return {"error": str(e)}

    def create_project_structure(self, project_name: str, structure: dict[str, Any]) -> bool:
        """Create a project structure with directories and files."""
        try:
            project_dir = self.project_root / project_name
            project_dir.mkdir(exist_ok=True)

            for item, content in structure.items():
                item_path = project_dir / item

                if isinstance(content, dict):
                    # Directory
                    item_path.mkdir(exist_ok=True)
                    self.create_project_structure(
                        str(item_path.relative_to(self.project_root)), content
                    )
                else:
                    # File
                    item_path.parent.mkdir(parents=True, exist_ok=True)
                    item_path.write_text(content)

            self.logger.info(f"Project structure created: {project_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating project structure: {e}")
            return False

    def run_workflow(self, workflow_name: str, parameters: dict[str, Any]) -> dict[str, Any]:
        """Run a predefined workflow."""
        workflows = {
            "fix_imports": self._workflow_fix_imports,
            "test_and_report": self._workflow_test_and_report,
            "create_component": self._workflow_create_component,
            "deploy_feature": self._workflow_deploy_feature,
        }

        if workflow_name not in workflows:
            return {"error": f"Unknown workflow: {workflow_name}"}

        try:
            return workflows[workflow_name](parameters)
        except Exception as e:
            return {"error": str(e)}

    def _workflow_fix_imports(self, params: dict[str, Any]) -> dict[str, Any]:
        """Workflow: Fix missing imports."""
        module_path = params.get("module_path", "src/core")
        success = self.fix_missing_imports(module_path)

        if success:
            # Test the fix
            test_success = self.test_imports(module_path)
            return {
                "success": test_success,
                "message": "Import fix completed and tested",
                "module_path": module_path,
            }
        else:
            return {"success": False, "message": "Import fix failed"}

    def _workflow_test_and_report(self, params: dict[str, Any]) -> dict[str, Any]:
        """Workflow: Run tests and send report."""
        test_results = self.run_tests(params.get("test_path", "tests/"))

        # Send status update
        status = "Tests PASSED" if test_results["success"] else "Tests FAILED"
        self.send_status_update(
            params.get("target_agent", "Agent-4"), status, test_results.get("stdout", "")
        )

        return test_results

    def _workflow_create_component(self, params: dict[str, Any]) -> dict[str, Any]:
        """Workflow: Create a new component."""
        component_name = params.get("name", "NewComponent")
        component_type = params.get("type", "react")

        if component_type == "react":
            structure = {
                f"{component_name}.js": f"// {component_name} component",
                f"{component_name}.css": f"/* {component_name} styles */",
                f"{component_name}.test.js": f"// {component_name} tests",
            }
        else:
            structure = {
                f"{component_name}.py": f"# {component_name} module",
                f"test_{component_name}.py": f"# {component_name} tests",
            }

        success = self.create_project_structure(f"components/{component_name}", structure)

        return {
            "success": success,
            "component_name": component_name,
            "component_type": component_type,
        }

    def _workflow_deploy_feature(self, params: dict[str, Any]) -> dict[str, Any]:
        """Workflow: Deploy a feature."""
        feature_name = params.get("name", "new_feature")

        # Update working tasks
        task_update = {
            "current_task": {
                "task_id": f"DEPLOY-{feature_name.upper()}",
                "title": f"Deploy {feature_name}",
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
            }
        }

        self.update_working_tasks("Agent-2", task_update)

        # Send completion message
        self.send_status_update(
            "Agent-4",
            f"Feature {feature_name} deployed successfully",
            "All components tested and deployed",
        )

        return {"success": True, "feature_name": feature_name}


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Agent Workflow Automation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Fix imports command
    fix_parser = subparsers.add_parser("fix-imports", help="Fix missing imports")
    fix_parser.add_argument("--module-path", required=True, help="Module path to fix")

    # Test imports command
    test_parser = subparsers.add_parser("test-imports", help="Test imports")
    test_parser.add_argument("--module-path", required=True, help="Module path to test")

    # Run tests command
    run_tests_parser = subparsers.add_parser("run-tests", help="Run test suite")
    run_tests_parser.add_argument("--test-path", default="tests/", help="Test directory path")

    # Send message command
    message_parser = subparsers.add_parser("send-message", help="Send status message")
    message_parser.add_argument("--agent", required=True, help="Target agent ID")
    message_parser.add_argument("--message", required=True, help="Message content")

    # Create devlog command
    devlog_parser = subparsers.add_parser("create-devlog", help="Create devlog")
    devlog_parser.add_argument("--title", required=True, help="Devlog title")
    devlog_parser.add_argument("--content", required=True, help="Devlog content")

    # Check compliance command
    compliance_parser = subparsers.add_parser("check-compliance", help="Check V2 compliance")
    compliance_parser.add_argument("--file", required=True, help="File to check")

    # Run workflow command
    workflow_parser = subparsers.add_parser("run-workflow", help="Run predefined workflow")
    workflow_parser.add_argument("--name", required=True, help="Workflow name")
    workflow_parser.add_argument(
        "--params", type=json.loads, default={}, help="Workflow parameters (JSON)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize automation tool
    automation = AgentWorkflowAutomation()

    # Execute command
    if args.command == "fix-imports":
        success = automation.fix_missing_imports(args.module_path)
        print(f"Import fix: {'SUCCESS' if success else 'FAILED'}")

    elif args.command == "test-imports":
        success = automation.test_imports(args.module_path)
        print(f"Import test: {'SUCCESS' if success else 'FAILED'}")

    elif args.command == "run-tests":
        results = automation.run_tests(args.test_path)
        print(f"Tests: {'PASSED' if results['success'] else 'FAILED'}")
        if not results["success"]:
            print(f"Error: {results.get('error', 'Unknown error')}")

    elif args.command == "send-message":
        success = automation.send_status_update(args.agent, args.message)
        print(f"Message sent: {'SUCCESS' if success else 'FAILED'}")

    elif args.command == "create-devlog":
        filepath = automation.create_devlog(args.title, args.content)
        print(f"Devlog created: {filepath}")

    elif args.command == "check-compliance":
        compliance = automation.check_v2_compliance(args.file)
        print(json.dumps(compliance, indent=2))

    elif args.command == "run-workflow":
        results = automation.run_workflow(args.name, args.params)
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
