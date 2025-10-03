#!/usr/bin/env python3
"""
Progress Tracking Validation System
==================================
Anti-Slop Protocol: Measurable, verifiable results requirement
V2 Compliant: ≤400 lines, focused validation logic
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any


class ValidationStatus(Enum):
    """Validation status enumeration"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VALIDATED = "validated"
    FAILED = "failed"
    SKIPPED = "skipped"


class ResultType(Enum):
    """Result type enumeration"""

    FEATURE_IMPLEMENTED = "feature_implemented"
    BUG_FIXED = "bug_fixed"
    PERFORMANCE_IMPROVED = "performance_improved"
    FILE_CREATED = "file_created"
    FILE_MODIFIED = "file_modified"
    FILE_DELETED = "file_deleted"
    SYSTEM_OPTIMIZED = "system_optimized"


@dataclass
class ValidationResult:
    """Validation result data structure"""

    agent_id: str
    task_id: str
    result_type: ResultType
    description: str
    measurable_metric: str
    before_value: Any | None = None
    after_value: Any | None = None
    improvement_percentage: float | None = None
    timestamp: str = ""
    status: ValidationStatus = ValidationStatus.PENDING
    evidence_files: list[str] = None
    verification_commands: list[str] = None

    def __post_init__(self):
        if self.timestamp == "":
            self.timestamp = datetime.now().isoformat()
        if self.evidence_files is None:
            self.evidence_files = []
        if self.verification_commands is None:
            self.verification_commands = []


class ProgressValidationSystem:
    """Progress tracking validation system with measurable results requirement"""

    def __init__(self, validation_dir: str = "validation_results"):
        self.validation_dir = Path(validation_dir)
        self.validation_dir.mkdir(exist_ok=True)

        # Track validation results
        self.results: dict[str, ValidationResult] = {}
        self.load_existing_results()

        # Anti-slop validation rules
        self.min_improvement_threshold = 5.0  # Minimum 5% improvement required
        self.max_file_creation_per_cycle = 3  # Anti-slop limit

    def load_existing_results(self) -> None:
        """Load existing validation results from disk"""
        results_file = self.validation_dir / "validation_results.json"
        if results_file.exists():
            try:
                with open(results_file) as f:
                    data = json.load(f)
                    for task_id, result_data in data.items():
                        result_data["result_type"] = ResultType(result_data["result_type"])
                        result_data["status"] = ValidationStatus(result_data["status"])
                        self.results[task_id] = ValidationResult(**result_data)
            except Exception as e:
                print(f"Warning: Failed to load validation results: {e}")

    def save_results(self) -> None:
        """Save validation results to disk"""
        results_file = self.validation_dir / "validation_results.json"
        try:
            data = {}
            for task_id, result in self.results.items():
                data[task_id] = asdict(result)
                data[task_id]["result_type"] = result.result_type.value
                data[task_id]["status"] = result.status.value

            with open(results_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving validation results: {e}")

    def register_task(
        self,
        agent_id: str,
        task_id: str,
        result_type: ResultType,
        description: str,
        measurable_metric: str,
    ) -> ValidationResult:
        """Register a new task for validation"""
        result = ValidationResult(
            agent_id=agent_id,
            task_id=task_id,
            result_type=result_type,
            description=description,
            measurable_metric=measurable_metric,
            status=ValidationStatus.PENDING,
        )

        self.results[task_id] = result
        self.save_results()

        return result

    def set_baseline(self, task_id: str, baseline_value: Any) -> bool:
        """Set baseline value for comparison"""
        if task_id not in self.results:
            return False

        self.results[task_id].before_value = baseline_value
        self.results[task_id].status = ValidationStatus.IN_PROGRESS
        self.save_results()

        return True

    def submit_result(
        self,
        task_id: str,
        final_value: Any,
        evidence_files: list[str] = None,
        verification_commands: list[str] = None,
    ) -> bool:
        """Submit final result for validation"""
        if task_id not in self.results:
            return False

        result = self.results[task_id]
        result.after_value = final_value
        result.status = ValidationStatus.IN_PROGRESS

        # Calculate improvement percentage
        if result.before_value is not None and result.after_value is not None:
            try:
                before = float(result.before_value)
                after = float(result.after_value)
                result.improvement_percentage = ((after - before) / before) * 100
            except (ValueError, TypeError, ZeroDivisionError):
                result.improvement_percentage = None

        # Add evidence and verification
        if evidence_files:
            result.evidence_files.extend(evidence_files)
        if verification_commands:
            result.verification_commands.extend(verification_commands)

        self.save_results()

        return True

    def validate_result(self, task_id: str) -> bool:
        """Validate a submitted result"""
        if task_id not in self.results:
            return False

        result = self.results[task_id]

        # Check if result meets minimum requirements
        validation_passed = True
        validation_reasons = []

        # Check measurable improvement
        if result.improvement_percentage is not None:
            if result.improvement_percentage < self.min_improvement_threshold:
                validation_passed = False
                validation_reasons.append(
                    f"Improvement {result.improvement_percentage:.1f}% below threshold {self.min_improvement_threshold}%"
                )

        # Check for evidence
        if not result.evidence_files:
            validation_passed = False
            validation_reasons.append("No evidence files provided")

        # Check for verification commands
        if not result.verification_commands:
            validation_passed = False
            validation_reasons.append("No verification commands provided")

        # Update status
        result.status = ValidationStatus.VALIDATED if validation_passed else ValidationStatus.FAILED

        # Save validation result
        self.save_results()

        return validation_passed

    def get_validation_summary(self, agent_id: str = None) -> dict[str, Any]:
        """Get validation summary for agent or all agents"""
        summary = {
            "total_tasks": 0,
            "validated": 0,
            "failed": 0,
            "pending": 0,
            "in_progress": 0,
            "average_improvement": 0.0,
            "tasks": [],
        }

        improvements = []
        for task_id, result in self.results.items():
            if agent_id and result.agent_id != agent_id:
                continue

            summary["total_tasks"] += 1
            summary["tasks"].append(
                {
                    "task_id": task_id,
                    "agent_id": result.agent_id,
                    "status": result.status.value,
                    "improvement": result.improvement_percentage,
                    "description": result.description,
                }
            )

            if result.status == ValidationStatus.VALIDATED:
                summary["validated"] += 1
                if result.improvement_percentage is not None:
                    improvements.append(result.improvement_percentage)
            elif result.status == ValidationStatus.FAILED:
                summary["failed"] += 1
            elif result.status == ValidationStatus.PENDING:
                summary["pending"] += 1
            elif result.status == ValidationStatus.IN_PROGRESS:
                summary["in_progress"] += 1

        if improvements:
            summary["average_improvement"] = sum(improvements) / len(improvements)

        return summary

    def check_anti_slop_compliance(self, agent_id: str, files_created: int) -> bool:
        """Check if agent is compliant with anti-slop protocol"""
        if files_created > self.max_file_creation_per_cycle:
            return False

        # Check for duplicate content
        recent_results = [
            r
            for r in self.results.values()
            if r.agent_id == agent_id
            and r.timestamp > (datetime.now() - timedelta(hours=24)).isoformat()
        ]

        # Check for repetitive tasks
        task_descriptions = [r.description for r in recent_results]
        if len(set(task_descriptions)) < len(task_descriptions) * 0.8:  # 80% uniqueness required
            return False

        return True

    def generate_validation_report(self, agent_id: str = None) -> str:
        """Generate comprehensive validation report"""
        summary = self.get_validation_summary(agent_id)

        report = []
        report.append("# 📊 Progress Validation Report")
        report.append(f"## Agent: {agent_id or 'All Agents'}")
        report.append(f"## Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        report.append("## 📈 Summary")
        report.append(f"- **Total Tasks**: {summary['total_tasks']}")
        report.append(f"- **Validated**: {summary['validated']}")
        report.append(f"- **Failed**: {summary['failed']}")
        report.append(f"- **Pending**: {summary['pending']}")
        report.append(f"- **In Progress**: {summary['in_progress']}")
        report.append(f"- **Average Improvement**: {summary['average_improvement']:.1f}%")
        report.append("")

        if summary["tasks"]:
            report.append("## 📋 Task Details")
            for task in summary["tasks"]:
                status_emoji = {"validated": "✅", "failed": "❌", "pending": "⏳", "in_progress": "🔄"}

                emoji = status_emoji.get(task["status"], "❓")
                improvement = f" ({task['improvement']:.1f}%)" if task["improvement"] else ""

                report.append(
                    f"- {emoji} **{task['task_id']}**: {task['description']}{improvement}"
                )

        return "\n".join(report)


def main():
    """Main function for testing"""
    validator = ProgressValidationSystem()

    # Example usage
    task_id = "test_task_001"
    result = validator.register_task(
        agent_id="Agent-7",
        task_id=task_id,
        result_type=ResultType.PERFORMANCE_IMPROVED,
        description="Optimize database query performance",
        measurable_metric="Query execution time (ms)",
    )

    validator.set_baseline(task_id, 1000.0)  # 1000ms baseline
    validator.submit_result(
        task_id=task_id,
        final_value=800.0,  # 800ms final
        evidence_files=["performance_test_results.json"],
        verification_commands=["python -m pytest tests/test_performance.py"],
    )

    is_valid = validator.validate_result(task_id)
    print(f"Validation result: {is_valid}")

    report = validator.generate_validation_report("Agent-7")
    print(report)


if __name__ == "__main__":
    main()
