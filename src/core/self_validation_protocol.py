#!/usr/bin/env python3
"""
Self Validation Protocol - Self-Validation Protocol Framework
===========================================================

Self-validation protocol framework for task completion verification and quality assurance.
Part of the self-validation protocol implementation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


class ValidationResult:
    """Validation result container."""

    def __init__(self, success: bool, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize validation result."""
        self.success = success
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }


class ValidationRule:
    """Base validation rule class."""

    def __init__(self, name: str, description: str, priority: int = 1) -> None:
        """Initialize validation rule."""
        self.name = name
        self.description = description
        self.priority = priority
        self.enabled = True

    def validate(self, target: Any) -> ValidationResult:
        """Validate target object."""
        raise NotImplementedError("Subclasses must implement validate method")

    def __str__(self) -> str:
        """String representation."""
        return f"{self.name}: {self.description}"


class FileExistenceRule(ValidationRule):
    """Validation rule for file existence."""

    def __init__(self, file_path: str | Path) -> None:
        """Initialize file existence rule."""
        super().__init__(
            name=f"FileExists_{Path(file_path).name}",
            description=f"Verify file exists: {file_path}",
            priority=1,
        )
        self.file_path = Path(file_path)

    def validate(self, target: Any = None) -> ValidationResult:
        """Validate file existence."""
        try:
            if self.file_path.exists():
                return ValidationResult(
                    success=True,
                    message=f"File exists: {self.file_path}",
                    details={
                        "file_path": str(self.file_path),
                        "size": self.file_path.stat().st_size,
                    },
                )
            else:
                return ValidationResult(
                    success=False,
                    message=f"File does not exist: {self.file_path}",
                    details={"file_path": str(self.file_path)},
                )
        except Exception as e:
            return ValidationResult(
                success=False,
                message=f"File validation error: {e}",
                details={"file_path": str(self.file_path), "error": str(e)},
            )


class FileSizeRule(ValidationRule):
    """Validation rule for file size limits."""

    def __init__(self, file_path: str | Path, max_size: int = 400) -> None:
        """Initialize file size rule."""
        super().__init__(
            name=f"FileSize_{Path(file_path).name}",
            description=f"Verify file size ≤ {max_size} lines: {file_path}",
            priority=2,
        )
        self.file_path = Path(file_path)
        self.max_size = max_size

    def validate(self, target: Any = None) -> ValidationResult:
        """Validate file size."""
        try:
            if not self.file_path.exists():
                return ValidationResult(
                    success=False,
                    message=f"File does not exist: {self.file_path}",
                    details={"file_path": str(self.file_path)},
                )

            # Count lines in file
            with open(self.file_path, encoding="utf-8") as f:
                line_count = sum(1 for _ in f)

            if line_count <= self.max_size:
                return ValidationResult(
                    success=True,
                    message=f"File size compliant: {line_count} ≤ {self.max_size} lines",
                    details={
                        "file_path": str(self.file_path),
                        "line_count": line_count,
                        "max_size": self.max_size,
                    },
                )
            else:
                return ValidationResult(
                    success=False,
                    message=f"File size violation: {line_count} > {self.max_size} lines",
                    details={
                        "file_path": str(self.file_path),
                        "line_count": line_count,
                        "max_size": self.max_size,
                    },
                )
        except Exception as e:
            return ValidationResult(
                success=False,
                message=f"File size validation error: {e}",
                details={"file_path": str(self.file_path), "error": str(e)},
            )


class TaskCompletionRule(ValidationRule):
    """Validation rule for task completion."""

    def __init__(self, task_id: str, required_status: str = "completed") -> None:
        """Initialize task completion rule."""
        super().__init__(
            name=f"TaskCompletion_{task_id}",
            description=f"Verify task {task_id} is {required_status}",
            priority=1,
        )
        self.task_id = task_id
        self.required_status = required_status

    def validate(self, target: dict[str, Any]) -> ValidationResult:
        """Validate task completion."""
        try:
            if not target:
                return ValidationResult(
                    success=False,
                    message="No task data provided",
                    details={"task_id": self.task_id},
                )

            task_status = target.get("status", "unknown")
            task_id = target.get("id", "unknown")

            if task_id != self.task_id:
                return ValidationResult(
                    success=False,
                    message=f"Task ID mismatch: expected {self.task_id}, got {task_id}",
                    details={"expected_id": self.task_id, "actual_id": task_id},
                )

            if task_status == self.required_status:
                return ValidationResult(
                    success=True,
                    message=f"Task {task_id} is {task_status}",
                    details={
                        "task_id": task_id,
                        "status": task_status,
                        "required_status": self.required_status,
                    },
                )
            else:
                return ValidationResult(
                    success=False,
                    message=f"Task {task_id} status is {task_status}, expected {self.required_status}",
                    details={
                        "task_id": task_id,
                        "status": task_status,
                        "required_status": self.required_status,
                    },
                )
        except Exception as e:
            return ValidationResult(
                success=False,
                message=f"Task completion validation error: {e}",
                details={"task_id": self.task_id, "error": str(e)},
            )


class SelfValidationProtocol:
    """Self-validation protocol framework."""

    def __init__(self, agent_id: str = "Agent-2") -> None:
        """Initialize self-validation protocol."""
        self.agent_id = agent_id
        self.validation_rules: list[ValidationRule] = []
        self.validation_history: list[dict[str, Any]] = []
        self.workspace_path = Path(f"agent_workspaces/{agent_id}")

        logger.info(f"Self-validation protocol initialized for {agent_id}")

    def add_rule(self, rule: ValidationRule) -> None:
        """Add validation rule."""
        self.validation_rules.append(rule)
        logger.info(f"Added validation rule: {rule.name}")

    def remove_rule(self, rule_name: str) -> bool:
        """Remove validation rule by name."""
        for i, rule in enumerate(self.validation_rules):
            if rule.name == rule_name:
                removed_rule = self.validation_rules.pop(i)
                logger.info(f"Removed validation rule: {removed_rule.name}")
                return True
        logger.warning(f"Validation rule not found: {rule_name}")
        return False

    def get_rule(self, rule_name: str) -> ValidationRule | None:
        """Get validation rule by name."""
        for rule in self.validation_rules:
            if rule.name == rule_name:
                return rule
        return None

    def list_rules(self) -> list[str]:
        """List all validation rule names."""
        return [rule.name for rule in self.validation_rules]

    def validate_all(self, target: Any = None) -> dict[str, Any]:
        """Run all validation rules."""
        validation_start = datetime.now()
        results = {
            "overall_success": True,
            "rule_results": {},
            "summary": {
                "total_rules": len(self.validation_rules),
                "passed": 0,
                "failed": 0,
                "errors": 0,
            },
            "validation_duration": 0,
            "timestamp": validation_start.isoformat(),
        }

        try:
            # Sort rules by priority (lower number = higher priority)
            sorted_rules = sorted(self.validation_rules, key=lambda r: r.priority)

            for rule in sorted_rules:
                if not rule.enabled:
                    continue

                try:
                    rule_result = rule.validate(target)
                    results["rule_results"][rule.name] = rule_result.to_dict()

                    if rule_result.success:
                        results["summary"]["passed"] += 1
                    else:
                        results["summary"]["failed"] += 1
                        results["overall_success"] = False

                except Exception as e:
                    error_result = ValidationResult(
                        success=False,
                        message=f"Validation rule error: {e}",
                        details={"rule_name": rule.name, "error": str(e)},
                    )
                    results["rule_results"][rule.name] = error_result.to_dict()
                    results["summary"]["errors"] += 1
                    results["overall_success"] = False

            # Calculate validation duration
            validation_end = datetime.now()
            results["validation_duration"] = (validation_end - validation_start).total_seconds()

            # Store in history
            self.validation_history.append(results)

            logger.info(f"Validation completed: {results['summary']}")
            return results

        except Exception as e:
            logger.error(f"Validation error: {e}")
            results["overall_success"] = False
            results["error"] = str(e)
            return results

    def validate_rule(self, rule_name: str, target: Any = None) -> ValidationResult | None:
        """Run specific validation rule."""
        rule = self.get_rule(rule_name)
        if not rule:
            logger.error(f"Validation rule not found: {rule_name}")
            return None

        try:
            result = rule.validate(target)
            logger.info(f"Rule {rule_name} validation: {result.success}")
            return result
        except Exception as e:
            logger.error(f"Rule {rule_name} validation error: {e}")
            return ValidationResult(
                success=False,
                message=f"Validation error: {e}",
                details={"rule_name": rule_name, "error": str(e)},
            )

    def get_validation_history(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get validation history."""
        return self.validation_history[-limit:]

    def clear_history(self) -> None:
        """Clear validation history."""
        self.validation_history.clear()
        logger.info("Validation history cleared")

    def generate_report(self) -> str:
        """Generate validation report."""
        if not self.validation_history:
            return "No validation history available"

        latest_validation = self.validation_history[-1]
        summary = latest_validation["summary"]

        report = f"""SELF-VALIDATION PROTOCOL REPORT - {self.agent_id}
============================================================
📊 Total Rules: {summary["total_rules"]}
✅ Passed: {summary["passed"]}
❌ Failed: {summary["failed"]}
⚠️ Errors: {summary["errors"]}
🎯 Overall Success: {"YES" if latest_validation["overall_success"] else "NO"}
⏱️ Validation Duration: {latest_validation["validation_duration"]:.3f}s
📅 Timestamp: {latest_validation["timestamp"]}
============================================================"""

        return report

