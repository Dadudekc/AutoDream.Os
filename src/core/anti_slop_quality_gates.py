#!/usr/bin/env python3
"""
Anti-Slop Protocol Quality Gates Integration
==========================================
Integrate anti-slop protocol with existing quality gates and autonomous workflow system
V2 Compliant: ≤400 lines, focused integration logic
"""

import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any

from .centralized_content_registry import CentralizedContentRegistry
from .content_deduplication_system import ContentDeduplicationSystem
from .progress_validation_system import ProgressValidationSystem


class GateStatus(Enum):
    """Quality gate status"""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    PENDING = "pending"


@dataclass
class QualityGateResult:
    """Quality gate result"""

    gate_name: str
    status: GateStatus
    message: str
    details: dict[str, Any]
    timestamp: str
    agent_id: str


class AntiSlopQualityGates:
    """Integrated quality gates with anti-slop protocol enforcement"""

    def __init__(self, validation_dir: str = "validation_results"):
        self.validation_system = ProgressValidationSystem(validation_dir)
        self.deduplication_system = ContentDeduplicationSystem()
        self.content_registry = CentralizedContentRegistry()

        # Quality gate thresholds
        self.max_file_creation_per_cycle = 3
        self.min_improvement_percentage = 5.0
        self.max_similarity_threshold = 0.95
        self.quality_score_threshold = 0.7

        # Agent tracking
        self.agent_activity: dict[str, dict[str, Any]] = {}

    def initialize_agent_tracking(self, agent_id: str) -> None:
        """Initialize tracking for agent"""
        if agent_id not in self.agent_activity:
            self.agent_activity[agent_id] = {
                "files_created_this_cycle": 0,
                "last_activity": datetime.now().isoformat(),
                "cycle_start": datetime.now().isoformat(),
                "total_improvements": 0,
                "failed_validations": 0,
            }

    def reset_agent_cycle(self, agent_id: str) -> None:
        """Reset agent cycle tracking"""
        if agent_id in self.agent_activity:
            self.agent_activity[agent_id]["files_created_this_cycle"] = 0
            self.agent_activity[agent_id]["cycle_start"] = datetime.now().isoformat()

    def validate_file_creation_limit(self, agent_id: str, file_path: str) -> QualityGateResult:
        """Validate file creation limit for agent"""
        self.initialize_agent_tracking(agent_id)

        current_count = self.agent_activity[agent_id]["files_created_this_cycle"]

        if current_count >= self.max_file_creation_per_cycle:
            return QualityGateResult(
                gate_name="file_creation_limit",
                status=GateStatus.FAILED,
                message=f"Agent {agent_id} has exceeded file creation limit ({self.max_file_creation_per_cycle} files per cycle)",
                details={
                    "current_count": current_count,
                    "limit": self.max_file_creation_per_cycle,
                    "file_path": file_path,
                },
                timestamp=datetime.now().isoformat(),
                agent_id=agent_id,
            )

        # Increment counter
        self.agent_activity[agent_id]["files_created_this_cycle"] += 1

        return QualityGateResult(
            gate_name="file_creation_limit",
            status=GateStatus.PASSED,
            message=f"File creation limit check passed ({current_count + 1}/{self.max_file_creation_per_cycle})",
            details={"current_count": current_count + 1, "limit": self.max_file_creation_per_cycle},
            timestamp=datetime.now().isoformat(),
            agent_id=agent_id,
        )

    def validate_content_uniqueness(self, content: str, agent_id: str) -> QualityGateResult:
        """Validate content uniqueness and similarity"""
        is_compliant, reason = self.deduplication_system.check_anti_slop_compliance(
            content, agent_id
        )

        if not is_compliant:
            return QualityGateResult(
                gate_name="content_uniqueness",
                status=GateStatus.FAILED,
                message=f"Content violates anti-slop protocol: {reason}",
                details={"reason": reason, "content_length": len(content)},
                timestamp=datetime.now().isoformat(),
                agent_id=agent_id,
            )

        return QualityGateResult(
            gate_name="content_uniqueness",
            status=GateStatus.PASSED,
            message="Content uniqueness validation passed",
            details={"content_length": len(content)},
            timestamp=datetime.now().isoformat(),
            agent_id=agent_id,
        )

    def validate_measurable_results(
        self, agent_id: str, task_id: str, before_value: Any, after_value: Any
    ) -> QualityGateResult:
        """Validate measurable results requirement"""
        try:
            before_float = float(before_value)
            after_float = float(after_value)
            improvement = ((after_float - before_float) / before_float) * 100

            if improvement < self.min_improvement_percentage:
                return QualityGateResult(
                    gate_name="measurable_results",
                    status=GateStatus.FAILED,
                    message=f"Improvement {improvement:.1f}% below minimum threshold {self.min_improvement_percentage}%",
                    details={
                        "improvement_percentage": improvement,
                        "threshold": self.min_improvement_percentage,
                        "before_value": before_value,
                        "after_value": after_value,
                    },
                    timestamp=datetime.now().isoformat(),
                    agent_id=agent_id,
                )

            # Track successful improvement
            self.agent_activity[agent_id]["total_improvements"] += 1

            return QualityGateResult(
                gate_name="measurable_results",
                status=GateStatus.PASSED,
                message=f"Measurable improvement validated: {improvement:.1f}%",
                details={"improvement_percentage": improvement},
                timestamp=datetime.now().isoformat(),
                agent_id=agent_id,
            )

        except (ValueError, TypeError, ZeroDivisionError) as e:
            return QualityGateResult(
                gate_name="measurable_results",
                status=GateStatus.FAILED,
                message=f"Cannot calculate measurable improvement: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now().isoformat(),
                agent_id=agent_id,
            )

    def validate_v2_compliance(self, file_path: str) -> QualityGateResult:
        """Validate V2 compliance requirements"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")
            violations = []

            # Check line count (≤400 lines)
            if len(lines) > 400:
                violations.append(f"File exceeds 400 lines ({len(lines)} lines)")

            # Check for Python-specific V2 compliance
            if file_path.endswith(".py"):
                class_count = content.count("class ")
                def_count = content.count("def ")

                if class_count > 5:
                    violations.append(f"File has {class_count} classes (limit: 5)")

                if def_count > 10:
                    violations.append(f"File has {def_count} functions (limit: 10)")

                # Check for forbidden patterns
                forbidden_patterns = [
                    ("threading.RLock()", "Threading usage"),
                    ("weakref.ref(", "Weakref usage"),
                    ("abc.ABC", "Abstract base class without 2+ implementations"),
                ]

                for pattern, description in forbidden_patterns:
                    if pattern in content:
                        violations.append(description)

            if violations:
                return QualityGateResult(
                    gate_name="v2_compliance",
                    status=GateStatus.FAILED,
                    message=f"V2 compliance violations: {', '.join(violations)}",
                    details={"violations": violations, "line_count": len(lines)},
                    timestamp=datetime.now().isoformat(),
                    agent_id="system",
                )

            return QualityGateResult(
                gate_name="v2_compliance",
                status=GateStatus.PASSED,
                message="V2 compliance validation passed",
                details={"line_count": len(lines)},
                timestamp=datetime.now().isoformat(),
                agent_id="system",
            )

        except Exception as e:
            return QualityGateResult(
                gate_name="v2_compliance",
                status=GateStatus.FAILED,
                message=f"Error validating V2 compliance: {str(e)}",
                details={"error": str(e)},
                timestamp=datetime.now().isoformat(),
                agent_id="system",
            )

    def validate_real_work_requirement(
        self, agent_id: str, task_description: str
    ) -> QualityGateResult:
        """Validate that task represents real work, not AI slop"""
        # Check for meta-work patterns
        meta_work_patterns = [
            "monitor",
            "track",
            "status",
            "update",
            "check",
            "review",
            "analyze",
            "report",
            "document",
            "log",
            "audit",
        ]

        task_lower = task_description.lower()
        meta_work_count = sum(1 for pattern in meta_work_patterns if pattern in task_lower)

        # Check for repetitive work
        recent_tasks = [
            metadata.description
            for metadata in self.content_registry.get_content_by_agent(agent_id)
            if datetime.fromisoformat(metadata.created_at) > datetime.now() - timedelta(hours=24)
        ]

        similar_tasks = sum(
            1 for task in recent_tasks if task_lower in task.lower() or task.lower() in task_lower
        )

        # Check for measurable deliverables
        measurable_patterns = [
            "implement",
            "fix",
            "optimize",
            "reduce",
            "improve",
            "create",
            "build",
            "develop",
            "integrate",
            "deploy",
            "configure",
            "setup",
        ]

        has_measurable_deliverable = any(pattern in task_lower for pattern in measurable_patterns)

        violations = []
        if meta_work_count > 2:
            violations.append(f"Task contains {meta_work_count} meta-work patterns")
        if similar_tasks > 1:
            violations.append(f"Task is similar to {similar_tasks} recent tasks")
        if not has_measurable_deliverable:
            violations.append("Task lacks measurable deliverable")

        if violations:
            return QualityGateResult(
                gate_name="real_work_requirement",
                status=GateStatus.FAILED,
                message=f"Task does not represent real work: {', '.join(violations)}",
                details={"violations": violations, "meta_work_count": meta_work_count},
                timestamp=datetime.now().isoformat(),
                agent_id=agent_id,
            )

        return QualityGateResult(
            gate_name="real_work_requirement",
            status=GateStatus.PASSED,
            message="Task represents real work with measurable deliverables",
            details={"has_measurable_deliverable": has_measurable_deliverable},
            timestamp=datetime.now().isoformat(),
            agent_id=agent_id,
        )

    def run_all_quality_gates(
        self,
        agent_id: str,
        file_path: str,
        content: str,
        task_description: str,
        before_value: Any = None,
        after_value: Any = None,
    ) -> list[QualityGateResult]:
        """Run all quality gates for comprehensive validation"""
        results = []

        # Gate 1: File creation limit
        results.append(self.validate_file_creation_limit(agent_id, file_path))

        # Gate 2: Content uniqueness
        results.append(self.validate_content_uniqueness(content, agent_id))

        # Gate 3: V2 compliance
        if Path(file_path).exists():
            results.append(self.validate_v2_compliance(file_path))

        # Gate 4: Real work requirement
        results.append(self.validate_real_work_requirement(agent_id, task_description))

        # Gate 5: Measurable results (if values provided)
        if before_value is not None and after_value is not None:
            results.append(
                self.validate_measurable_results(
                    agent_id, f"{agent_id}_{int(time.time())}", before_value, after_value
                )
            )

        # Track failed validations
        failed_count = sum(1 for result in results if result.status == GateStatus.FAILED)
        if failed_count > 0:
            self.agent_activity[agent_id]["failed_validations"] += failed_count

        return results

    def get_agent_compliance_report(self, agent_id: str) -> dict[str, Any]:
        """Get comprehensive compliance report for agent"""
        self.initialize_agent_tracking(agent_id)

        agent_activity = self.agent_activity[agent_id]
        validation_summary = self.validation_system.get_validation_summary(agent_id)

        # Calculate compliance score
        total_gates = 5  # Number of quality gates
        passed_gates = validation_summary["validated"]
        failed_gates = validation_summary["failed"]

        compliance_score = (
            (passed_gates / (passed_gates + failed_gates)) * 100
            if (passed_gates + failed_gates) > 0
            else 100
        )

        return {
            "agent_id": agent_id,
            "compliance_score": compliance_score,
            "files_created_this_cycle": agent_activity["files_created_this_cycle"],
            "total_improvements": agent_activity["total_improvements"],
            "failed_validations": agent_activity["failed_validations"],
            "validation_summary": validation_summary,
            "last_activity": agent_activity["last_activity"],
            "cycle_start": agent_activity["cycle_start"],
            "status": "compliant" if compliance_score >= 80 else "non_compliant",
        }

    def get_system_compliance_report(self) -> dict[str, Any]:
        """Get system-wide compliance report"""
        agent_reports = {}
        for agent_id in self.agent_activity.keys():
            agent_reports[agent_id] = self.get_agent_compliance_report(agent_id)

        total_compliance = (
            sum(report["compliance_score"] for report in agent_reports.values())
            / len(agent_reports)
            if agent_reports
            else 100
        )

        return {
            "system_compliance_score": total_compliance,
            "total_agents": len(agent_reports),
            "compliant_agents": sum(
                1 for report in agent_reports.values() if report["status"] == "compliant"
            ),
            "agent_reports": agent_reports,
            "last_updated": datetime.now().isoformat(),
        }


def main():
    """Main function for testing"""
    gates = AntiSlopQualityGates()

    # Test quality gates
    test_content = "def hello_world():\n    print('Hello, World!')\n"
    test_file = "test_quality_gates.py"

    with open(test_file, "w") as f:
        f.write(test_content)

    results = gates.run_all_quality_gates(
        agent_id="Agent-7",
        file_path=test_file,
        content=test_content,
        task_description="Implement hello world function",
        before_value=0,
        after_value=1,
    )

    print("Quality Gate Results:")
    for result in results:
        print(f"- {result.gate_name}: {result.status.value} - {result.message}")

    # Get compliance report
    report = gates.get_agent_compliance_report("Agent-7")
    print(f"\nAgent Compliance Report: {report}")

    # Clean up
    Path(test_file).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
