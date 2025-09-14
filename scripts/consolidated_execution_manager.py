#!/usr/bin/env python3
"""
Consolidated Execution Manager
==============================

Unified execution system for running various system components and integrations.
Consolidates functionality from multiple execution-related scripts.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import argparse
import json
import logging
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class ExecutionTarget:
    """Represents an execution target."""

    name: str
    script_path: str
    description: str
    dependencies: List[str]
    timeout: int = 300
    required: bool = True


class ExecutionManager:
    """Unified execution manager for system components."""

    def __init__(self):
        """Initialize the execution manager."""
        self.targets = [
            ExecutionTarget(
                name="admin_commander",
                script_path="scripts/execution/run_admin_commander.py",
                description="Admin command interface",
                dependencies=["src/core/"]
            ),
            ExecutionTarget(
                name="discord_bot",
                script_path="scripts/execution/run_discord_bot.py",
                description="Discord bot interface",
                dependencies=["src/web/discord_bot.py", "config/discord.json"]
            ),
            ExecutionTarget(
                name="discord_agent_bot",
                script_path="src/discord_commander/discord_agent_bot.py",
                description="Discord agent bot interface",
                dependencies=["src/discord_commander/discord_agent_bot.py", "config/discord_bot_config.json"]
            ),
            ExecutionTarget(
                name="ssot_integration",
                script_path="scripts/execution/execute_ssot_integration.py",
                description="Single Source of Truth integration",
                dependencies=["src/core/unified_config.py"]
            )
        ]

    def list_targets(self) -> List[ExecutionTarget]:
        """List all available execution targets."""
        return self.targets

    def validate_target(self, target: ExecutionTarget) -> Dict[str, Any]:
        """Validate an execution target."""
        result = {
            "valid": True,
            "script_exists": False,
            "dependencies_met": True,
            "issues": []
        }

        # Check script existence
        script_path = Path(target.script_path)
        if script_path.exists():
            result["script_exists"] = True
        else:
            result["valid"] = False
            result["issues"].append(f"Script not found: {target.script_path}")

        # Check dependencies
        missing_deps = []
        for dep in target.dependencies:
            if not Path(dep).exists():
                missing_deps.append(dep)

        if missing_deps:
            result["dependencies_met"] = False
            result["issues"].append(f"Missing dependencies: {missing_deps}")
            if target.required:
                result["valid"] = False

        return result

    def execute_target(self, target_name: str, args: List[str] = None) -> Dict[str, Any]:
        """Execute a specific target."""
        target = None
        for t in self.targets:
            if t.name == target_name:
                target = t
                break

        if not target:
            return {
                "success": False,
                "error": f"Target '{target_name}' not found",
                "output": "",
                "duration": 0
            }

        # Validate target
        validation = self.validate_target(target)
        if not validation["valid"]:
            return {
                "success": False,
                "error": f"Target validation failed: {validation['issues']}",
                "output": "",
                "duration": 0
            }

        # Execute target
        start_time = time.time()
        try:
            cmd = [sys.executable, target.script_path]
            if args:
                cmd.extend(args)

            logger.info(f"Executing {target.name}: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=target.timeout
            )

            duration = time.time() - start_time

            return {
                "success": result.returncode == 0,
                "error": result.stderr if result.returncode != 0 else "",
                "output": result.stdout,
                "duration": duration,
                "return_code": result.returncode
            }

        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            return {
                "success": False,
                "error": f"Execution timed out after {target.timeout} seconds",
                "output": "",
                "duration": duration
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                "success": False,
                "error": f"Execution failed: {str(e)}",
                "output": "",
                "duration": duration
            }

    def run_admin_commander(self, command: str = None) -> Dict[str, Any]:
        """Run admin commander with optional command."""
        args = []
        if command:
            args.append("--command")
            args.append(command)

        return self.execute_target("admin_commander", args)

    def run_discord_bot(self, bot_type: str = "standard") -> Dict[str, Any]:
        """Run Discord bot."""
        if bot_type == "agent":
            return self.execute_target("discord_agent_bot")
        else:
            return self.execute_target("discord_bot")

    def execute_ssot_integration(self) -> Dict[str, Any]:
        """Execute SSOT integration."""
        return self.execute_target("ssot_integration")

    def run_all_targets(self, parallel: bool = False) -> Dict[str, Any]:
        """Run all available targets."""
        results = {}

        if parallel:
            # Run targets in parallel (simplified - would need threading for real parallel execution)
            logger.info("Running all targets in parallel...")
            for target in self.targets:
                validation = self.validate_target(target)
                if validation["valid"]:
                    results[target.name] = self.execute_target(target.name)
                else:
                    results[target.name] = {
                        "success": False,
                        "error": f"Validation failed: {validation['issues']}",
                        "output": "",
                        "duration": 0
                    }
        else:
            # Run targets sequentially
            logger.info("Running all targets sequentially...")
            for target in self.targets:
                validation = self.validate_target(target)
                if validation["valid"]:
                    logger.info(f"Executing {target.name}...")
                    results[target.name] = self.execute_target(target.name)
                else:
                    logger.warning(f"Skipping {target.name}: {validation['issues']}")
                    results[target.name] = {
                        "success": False,
                        "error": f"Validation failed: {validation['issues']}",
                        "output": "",
                        "duration": 0
                    }

        return results

    def get_status(self) -> Dict[str, Any]:
        """Get execution manager status."""
        status = {
            "total_targets": len(self.targets),
            "valid_targets": 0,
            "targets": {}
        }

        for target in self.targets:
            validation = self.validate_target(target)
            status["targets"][target.name] = {
                "valid": validation["valid"],
                "script_exists": validation["script_exists"],
                "dependencies_met": validation["dependencies_met"],
                "issues": validation["issues"]
            }

            if validation["valid"]:
                status["valid_targets"] += 1

        return status


def main():
    """Main entry point for the execution manager."""
    parser = argparse.ArgumentParser(description="Consolidated Execution Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List execution targets")

    # Execute command
    execute_parser = subparsers.add_parser("execute", help="Execute a specific target")
    execute_parser.add_argument("target", help="Target name to execute")
    execute_parser.add_argument("--args", nargs="*", help="Additional arguments")

    # Admin commander command
    admin_parser = subparsers.add_parser("admin", help="Run admin commander")
    admin_parser.add_argument("--command", help="Admin command to execute")

    # Discord bot command
    discord_parser = subparsers.add_parser("discord", help="Run Discord bot")
    discord_parser.add_argument("--type", choices=["standard", "agent"], default="standard", help="Bot type")

    # SSOT integration command
    ssot_parser = subparsers.add_parser("ssot", help="Execute SSOT integration")

    # Run all command
    runall_parser = subparsers.add_parser("run-all", help="Run all targets")
    runall_parser.add_argument("--parallel", action="store_true", help="Run in parallel")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get execution manager status")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    manager = ExecutionManager()

    try:
        if args.command == "list":
            targets = manager.list_targets()
            print(f"Available execution targets ({len(targets)}):")
            for target in targets:
                validation = manager.validate_target(target)
                status = "✅" if validation["valid"] else "❌"
                print(f"  {status} {target.name}: {target.description}")
                if not validation["valid"]:
                    for issue in validation["issues"]:
                        print(f"    - {issue}")

        elif args.command == "execute":
            result = manager.execute_target(args.target, args.args)
            if result["success"]:
                print(f"✅ {args.target} executed successfully")
                if result["output"]:
                    print("Output:")
                    print(result["output"])
            else:
                print(f"❌ {args.target} execution failed: {result['error']}")
                return 1

        elif args.command == "admin":
            result = manager.run_admin_commander(args.command)
            if result["success"]:
                print("✅ Admin commander executed successfully")
                if result["output"]:
                    print("Output:")
                    print(result["output"])
            else:
                print(f"❌ Admin commander failed: {result['error']}")
                return 1

        elif args.command == "discord":
            result = manager.run_discord_bot(args.type)
            if result["success"]:
                print(f"✅ {args.type} Discord bot executed successfully")
                if result["output"]:
                    print("Output:")
                    print(result["output"])
            else:
                print(f"❌ {args.type} Discord bot failed: {result['error']}")
                return 1

        elif args.command == "ssot":
            result = manager.execute_ssot_integration()
            if result["success"]:
                print("✅ SSOT integration executed successfully")
                if result["output"]:
                    print("Output:")
                    print(result["output"])
            else:
                print(f"❌ SSOT integration failed: {result['error']}")
                return 1

        elif args.command == "run-all":
            results = manager.run_all_targets(args.parallel)
            successful = sum(1 for r in results.values() if r["success"])
            total = len(results)
            print(f"Execution completed: {successful}/{total} targets successful")

            for target_name, result in results.items():
                status = "✅" if result["success"] else "❌"
                print(f"  {status} {target_name}: {result.get('error', 'Success')}")

        elif args.command == "status":
            status = manager.get_status()
            print(f"Execution Manager Status:")
            print(f"  Total Targets: {status['total_targets']}")
            print(f"  Valid Targets: {status['valid_targets']}")
            print(f"  Success Rate: {status['valid_targets']/status['total_targets']*100:.1f}%")

            print("\nTarget Details:")
            for target_name, target_status in status["targets"].items():
                status_icon = "✅" if target_status["valid"] else "❌"
                print(f"  {status_icon} {target_name}")
                if target_status["issues"]:
                    for issue in target_status["issues"]:
                        print(f"    - {issue}")

        return 0

    except Exception as e:
        logger.error(f"Command failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
