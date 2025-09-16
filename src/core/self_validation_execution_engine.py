#!/usr/bin/env python3
"""
Self Validation Execution Engine - Self-Validation Protocol Execution
==================================================================

Execution engine for self-validation protocol with autonomous loop integration.
Part of the self-validation protocol implementation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.self_validation_protocol import (
    FileExistenceRule,
    FileSizeRule,
    SelfValidationProtocol,
    TaskCompletionRule,
)

logger = logging.getLogger(__name__)


class SelfValidationExecutionEngine:
    """Execution engine for self-validation protocol."""

    def __init__(self, agent_id: str = "Agent-2") -> None:
        """Initialize self-validation execution engine."""
        self.agent_id = agent_id
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")
        self.working_tasks_path = self.workspace_path / "working_tasks.json"
        self.future_tasks_path = self.workspace_path / "future_tasks.json"

        # Initialize validation protocol
        self.validation_protocol = SelfValidationProtocol(agent_id)

        # Setup default validation rules
        self._setup_default_rules()

        # Execution metrics
        self.execution_metrics = {
            "total_executions": 0,
            "successful_validations": 0,
            "failed_validations": 0,
            "last_execution": None,
            "execution_history": [],
        }

        logger.info(f"Self-validation execution engine initialized for {agent_id}")

    def _setup_default_rules(self) -> None:
        """Setup default validation rules for the agent."""
        try:
            # File existence rules for critical files
            critical_files = ["working_tasks.json", "future_tasks.json", "status.json"]

            for file_name in critical_files:
                file_path = self.workspace_path / file_name
                rule = FileExistenceRule(file_path)
                self.validation_protocol.add_rule(rule)

            # V2 compliance rules for core modules
            core_modules = [
                "autonomous_loop_integration.py",
                "continuous_autonomy_behavior.py",
                "autonomous_loop_validator.py",
                "autonomous_loop_system_integration.py",
                "production_autonomous_loop.py",
                "self_validation_protocol.py",
                "self_validation_execution_engine.py",
            ]

            core_path = Path("src/core")
            for module_name in core_modules:
                module_path = core_path / module_name
                if module_path.exists():
                    # File existence rule
                    existence_rule = FileExistenceRule(module_path)
                    self.validation_protocol.add_rule(existence_rule)

                    # V2 compliance rule (≤400 lines)
                    size_rule = FileSizeRule(module_path, max_size=400)
                    self.validation_protocol.add_rule(size_rule)

            logger.info("Default validation rules setup completed")

        except Exception as e:
            logger.error(f"Error setting up default rules: {e}")

    def _load_working_tasks(self) -> dict[str, Any] | None:
        """Load working tasks from JSON file."""
        try:
            if self.working_tasks_path.exists():
                with open(self.working_tasks_path) as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Failed to load working tasks: {e}")
            return None

    def _load_future_tasks(self) -> dict[str, Any] | None:
        """Load future tasks from JSON file."""
        try:
            if self.future_tasks_path.exists():
                with open(self.future_tasks_path) as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Failed to load future tasks: {e}")
            return None

    def validate_current_task(self) -> dict[str, Any]:
        """Validate current task completion."""
        try:
            working_tasks = self._load_working_tasks()
            if not working_tasks:
                return {
                    "success": False,
                    "message": "No working tasks data available",
                    "details": {},
                }

            current_task = working_tasks.get("current_task")
            if not current_task:
                return {"success": False, "message": "No current task found", "details": {}}

            task_id = current_task.get("id", "unknown")
            task_status = current_task.get("status", "unknown")

            # Create and execute task completion rule
            task_rule = TaskCompletionRule(task_id, "completed")
            result = task_rule.validate(current_task)

            return {"success": result.success, "message": result.message, "details": result.details}

        except Exception as e:
            logger.error(f"Current task validation error: {e}")
            return {
                "success": False,
                "message": f"Validation error: {e}",
                "details": {"error": str(e)},
            }

    def validate_v2_compliance(self) -> dict[str, Any]:
        """Validate V2 compliance for all core modules."""
        try:
            # Get all V2 compliance rules
            v2_rules = []
            for rule in self.validation_protocol.validation_rules:
                if isinstance(rule, FileSizeRule):
                    v2_rules.append(rule)

            if not v2_rules:
                return {
                    "success": True,
                    "message": "No V2 compliance rules found",
                    "details": {"rules_count": 0},
                }

            # Execute V2 compliance validation
            failed_files = []
            passed_files = []

            for rule in v2_rules:
                result = rule.validate()
                if result.success:
                    passed_files.append(str(rule.file_path))
                else:
                    failed_files.append(
                        {
                            "file": str(rule.file_path),
                            "message": result.message,
                            "details": result.details,
                        }
                    )

            overall_success = len(failed_files) == 0

            return {
                "success": overall_success,
                "message": f"V2 compliance validation: {len(passed_files)} passed, {len(failed_files)} failed",
                "details": {
                    "passed_files": passed_files,
                    "failed_files": failed_files,
                    "total_rules": len(v2_rules),
                },
            }

        except Exception as e:
            logger.error(f"V2 compliance validation error: {e}")
            return {
                "success": False,
                "message": f"V2 compliance validation error: {e}",
                "details": {"error": str(e)},
            }

    def validate_file_system_integrity(self) -> dict[str, Any]:
        """Validate file system integrity."""
        try:
            # Get all file existence rules
            existence_rules = []
            for rule in self.validation_protocol.validation_rules:
                if isinstance(rule, FileExistenceRule):
                    existence_rules.append(rule)

            if not existence_rules:
                return {
                    "success": True,
                    "message": "No file existence rules found",
                    "details": {"rules_count": 0},
                }

            # Execute file system validation
            missing_files = []
            existing_files = []

            for rule in existence_rules:
                result = rule.validate()
                if result.success:
                    existing_files.append(str(rule.file_path))
                else:
                    missing_files.append(
                        {
                            "file": str(rule.file_path),
                            "message": result.message,
                            "details": result.details,
                        }
                    )

            overall_success = len(missing_files) == 0

            return {
                "success": overall_success,
                "message": f"File system validation: {len(existing_files)} existing, {len(missing_files)} missing",
                "details": {
                    "existing_files": existing_files,
                    "missing_files": missing_files,
                    "total_rules": len(existence_rules),
                },
            }

        except Exception as e:
            logger.error(f"File system validation error: {e}")
            return {
                "success": False,
                "message": f"File system validation error: {e}",
                "details": {"error": str(e)},
            }

    def execute_comprehensive_validation(self) -> dict[str, Any]:
        """Execute comprehensive validation across all domains."""
        execution_start = datetime.now()

        try:
            # Execute all validation domains
            current_task_result = self.validate_current_task()
            v2_compliance_result = self.validate_v2_compliance()
            file_system_result = self.validate_file_system_integrity()

            # Run full validation protocol
            protocol_result = self.validation_protocol.validate_all()

            # Calculate overall success
            overall_success = (
                current_task_result["success"]
                and v2_compliance_result["success"]
                and file_system_result["success"]
                and protocol_result["overall_success"]
            )

            # Compile comprehensive results
            comprehensive_result = {
                "overall_success": overall_success,
                "execution_timestamp": execution_start.isoformat(),
                "execution_duration": (datetime.now() - execution_start).total_seconds(),
                "validation_domains": {
                    "current_task": current_task_result,
                    "v2_compliance": v2_compliance_result,
                    "file_system": file_system_result,
                    "protocol": protocol_result,
                },
                "summary": {
                    "total_domains": 4,
                    "successful_domains": sum(
                        [
                            current_task_result["success"],
                            v2_compliance_result["success"],
                            file_system_result["success"],
                            protocol_result["overall_success"],
                        ]
                    ),
                    "failed_domains": 0,
                },
            }

            # Update execution metrics
            self.execution_metrics["total_executions"] += 1
            if overall_success:
                self.execution_metrics["successful_validations"] += 1
            else:
                self.execution_metrics["failed_validations"] += 1
            self.execution_metrics["last_execution"] = execution_start.isoformat()
            self.execution_metrics["execution_history"].append(comprehensive_result)

            # Limit history size
            if len(self.execution_metrics["execution_history"]) > 100:
                self.execution_metrics["execution_history"] = self.execution_metrics[
                    "execution_history"
                ][-100:]

            logger.info(f"Comprehensive validation executed: {overall_success}")
            return comprehensive_result

        except Exception as e:
            logger.error(f"Comprehensive validation error: {e}")
            return {
                "overall_success": False,
                "error": str(e),
                "execution_timestamp": execution_start.isoformat(),
            }

    def generate_execution_report(self) -> str:
        """Generate comprehensive execution report."""
        try:
            latest_execution = None
            if self.execution_metrics["execution_history"]:
                latest_execution = self.execution_metrics["execution_history"][-1]

            report = f"""SELF-VALIDATION EXECUTION ENGINE REPORT - {self.agent_id}
============================================================
📊 Total Executions: {self.execution_metrics["total_executions"]}
✅ Successful Validations: {self.execution_metrics["successful_validations"]}
❌ Failed Validations: {self.execution_metrics["failed_validations"]}
⏰ Last Execution: {self.execution_metrics["last_execution"] or "Never"}
📋 Validation Rules: {len(self.validation_protocol.validation_rules)}
============================================================"""

            if latest_execution:
                summary = latest_execution.get("summary", {})
                report += f"""
🎯 Latest Execution Results:
  - Overall Success: {"YES" if latest_execution["overall_success"] else "NO"}
  - Successful Domains: {summary.get("successful_domains", 0)}/{summary.get("total_domains", 0)}
  - Execution Duration: {latest_execution.get("execution_duration", 0):.3f}s
  - Timestamp: {latest_execution.get("execution_timestamp", "Unknown")}
============================================================"""

            # Add validation protocol report
            protocol_report = self.validation_protocol.generate_report()
            report += f"\n{protocol_report}"

            return report

        except Exception as e:
            logger.error(f"Report generation error: {e}")
            return f"Report generation failed: {e}"

    def get_execution_status(self) -> dict[str, Any]:
        """Get current execution status."""
        return {
            "agent_id": self.agent_id,
            "execution_metrics": self.execution_metrics.copy(),
            "validation_rules_count": len(self.validation_protocol.validation_rules),
            "last_execution": self.execution_metrics["last_execution"],
            "status": "operational",
        }

