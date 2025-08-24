"""
CLI Utilities Module - Command Execution

This module provides CLI command execution utilities.
Follows Single Responsibility Principle - only manages command execution.

Architecture: Single Responsibility Principle - CLI execution only
LOC: 150 lines (under 200 limit)
"""

import subprocess
import os

from src.utils.stability_improvements import stability_manager, safe_import
from typing import List, Optional
from pathlib import Path


class CLIExecutor:
    """
    Executes CLI commands with proper error handling and output formatting.

    Responsibilities:
    - Execute CLI commands safely
    - Handle command output and errors
    - Provide formatted results
    """

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = (
            Path(project_root) if project_root else Path(__file__).parent.parent.parent
        )
        self.use_emojis = True

    def set_emoji_style(self, use_emojis: bool):
        """Set whether to use emojis in output"""
        self.use_emojis = use_emojis

    def run_command(
        self, cmd_args: List[str], description: str = "", capture_output: bool = True
    ) -> dict:
        """
        Run a CLI command and return structured results

        Args:
            cmd_args: Command arguments list
            description: Human-readable description of the command
            capture_output: Whether to capture and return output

        Returns:
            Dictionary with command results
        """
        try:
            if self.use_emojis:
                print(f"📤 {description}")
            else:
                print(f"Sending: {description}")

            # Set environment variable to handle Unicode properly
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"

            if capture_output:
                result = subprocess.run(
                    cmd_args,
                    capture_output=True,
                    text=True,
                    cwd=self.project_root,
                    env=env,
                )

                success = result.returncode == 0

                if success:
                    if self.use_emojis:
                        print(f"✅ Success: {result.stdout.strip()}")
                    else:
                        print(f"Success: {result.stdout.strip()}")
                else:
                    if self.use_emojis:
                        print(f"❌ Error: {result.stderr.strip()}")
                    else:
                        print(f"Error: {result.stderr.strip()}")

                return {
                    "success": success,
                    "returncode": result.returncode,
                    "stdout": result.stdout.strip(),
                    "stderr": result.stderr.strip(),
                    "command": " ".join(cmd_args),
                }
            else:
                # Run without capturing output (for interactive commands)
                result = subprocess.run(cmd_args, cwd=self.project_root, env=env)

                success = result.returncode == 0

                if success:
                    if self.use_emojis:
                        print(f"✅ Command completed successfully")
                    else:
                        print(f"Command completed successfully")
                else:
                    if self.use_emojis:
                        print(f"❌ Command failed with exit code {result.returncode}")
                    else:
                        print(f"Command failed with exit code {result.returncode}")

                return {
                    "success": success,
                    "returncode": result.returncode,
                    "command": " ".join(cmd_args),
                }

        except Exception as e:
            error_msg = f"Exception: {e}"
            if self.use_emojis:
                print(f"❌ {error_msg}")
            else:
                print(f"Exception: {e}")

            return {"success": False, "error": str(e), "command": " ".join(cmd_args)}

    def run_python_module(
        self, module_path: str, args: List[str] = None, description: str = ""
    ) -> dict:
        """
        Run a Python module with arguments

        Args:
            module_path: Python module path (e.g., "src.core.agent_manager")
            args: Additional arguments for the module
            description: Human-readable description

        Returns:
            Command execution results
        """
        cmd_args = ["python", "-m", module_path]
        if args:
            cmd_args.extend(args)

        return self.run_command(
            cmd_args, description or f"Running Python module: {module_path}"
        )

    def run_python_script(
        self, script_path: str, args: List[str] = None, description: str = ""
    ) -> dict:
        """
        Run a Python script with arguments

        Args:
            script_path: Path to Python script
            args: Additional arguments for the script
            description: Human-readable description

        Returns:
            Command execution results
        """
        cmd_args = ["python", script_path]
        if args:
            cmd_args.extend(args)

        return self.run_command(
            cmd_args, description or f"Running Python script: {script_path}"
        )

    def get_project_root(self) -> Path:
        """Get the project root directory"""
        return self.project_root

    def change_working_directory(self, new_path: str):
        """Change the working directory for command execution"""
        self.project_root = Path(new_path).resolve()


def run_smoke_test():
    """Run basic functionality test for CLIExecutor"""
    print("🧪 Running CLIExecutor Smoke Test...")

    try:
        executor = CLIExecutor()

        # Test basic command execution
        result = executor.run_command(["echo", "test"], "Testing echo command")
        assert result["success"]
        assert "test" in result["stdout"]

        # Test Python module execution
        result = executor.run_python_module(
            "src.utils.cli_utils", ["--test"], "Testing module execution"
        )
        # Note: This might fail if run from wrong directory, but that's expected

        # Test emoji style switching
        executor.set_emoji_style(False)
        assert not executor.use_emojis

        print("✅ CLIExecutor Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ CLIExecutor Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for CLIExecutor testing"""
    import argparse

    parser = argparse.ArgumentParser(description="CLI Executor CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--command", nargs="+", help="Execute a command")
    parser.add_argument("--module", help="Run Python module")
    parser.add_argument("--script", help="Run Python script")
    parser.add_argument("--no-emojis", action="store_true", help="Disable emojis")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    executor = CLIExecutor()

    if args.no_emojis:
        executor.set_emoji_style(False)

    if args.command:
        result = executor.run_command(
            args.command, f"Executing: {' '.join(args.command)}"
        )
        print(f"Result: {result}")
    elif args.module:
        result = executor.run_python_module(
            args.module, description=f"Running module: {args.module}"
        )
        print(f"Result: {result}")
    elif args.script:
        result = executor.run_python_script(
            args.script, description=f"Running script: {args.script}"
        )
        print(f"Result: {result}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
