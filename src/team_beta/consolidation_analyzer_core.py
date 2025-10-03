#!/usr/bin/env python3
"""
Consolidation Analyzer Core
==========================
Core logic for system duplication elimination and SSOT compliance
V2 Compliant: ≤400 lines, focused consolidation logic
"""

import json
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any


class DuplicationSeverity(Enum):
    """Duplication severity levels."""

    CRITICAL = "critical"  # Immediate consolidation required
    HIGH = "high"  # High priority consolidation
    MEDIUM = "medium"  # Medium priority consolidation
    LOW = "low"  # Low priority consolidation


class ConsolidationStatus(Enum):
    """Consolidation status enumeration."""

    IDENTIFIED = "identified"
    ANALYZED = "analyzed"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class DuplicationInstance:
    """Duplication instance structure."""

    name: str
    description: str
    files: list[str]
    severity: DuplicationSeverity
    status: ConsolidationStatus
    impact: str
    consolidation_plan: str
    dependencies: list[str]
    risks: list[str]


@dataclass
class ConsolidationReport:
    """Consolidation report structure."""

    total_duplications: int
    critical_duplications: int
    high_priority_duplications: int
    medium_priority_duplications: int
    low_priority_duplications: int
    ssot_violations: int
    v2_compliance_issues: int
    maintenance_complexity_score: float


class SystemConsolidationAnalyzerCore:
    """Core logic for system consolidation analyzer"""

    def __init__(self):
        """Initialize consolidation analyzer."""
        self.duplications: list[DuplicationInstance] = []
        self.consolidation_report = ConsolidationReport(
            total_duplications=0,
            critical_duplications=0,
            high_priority_duplications=0,
            medium_priority_duplications=0,
            low_priority_duplications=0,
            ssot_violations=0,
            v2_compliance_issues=0,
            maintenance_complexity_score=0.0,
        )
        self._initialize_known_duplications()

    def manage_consolidation_operations(self, action: str, **kwargs) -> Any:
        """Consolidated consolidation operations"""
        if action == "analyze":
            return self.analyze_duplications()
        elif action == "create_plan":
            return self.create_consolidation_plan()
        elif action == "update_status":
            return self.update_duplication_status(kwargs["name"], kwargs["status"])
        elif action == "get_progress":
            return self.get_consolidation_progress()
        elif action == "export":
            return self.export_consolidation_analysis(kwargs["filepath"])
        elif action == "assess_risks":
            return self._assess_consolidation_risks()
        return None

    def _initialize_known_duplications(self):
        """Initialize known system duplications."""
        self.duplications = [
            DuplicationInstance(
                name="Persistent Memory",
                description="Multiple memory management implementations",
                files=["memory/persistent_memory.db", "test_memory.db", "test_performance.db"],
                severity=DuplicationSeverity.CRITICAL,
                status=ConsolidationStatus.IDENTIFIED,
                impact="Inconsistent data persistence, data loss risks, synchronization problems",
                consolidation_plan="Create unified memory management system with single database",
                dependencies=["sqlite3", "database management"],
                risks=["Data migration complexity", "Temporary system downtime"],
            ),
            DuplicationInstance(
                name="Aletheia Prompt Manager",
                description="Duplicate prompt management systems",
                files=["test_aletheia_prompt_manager.py", "aletheia_prompt_manager.py"],
                severity=DuplicationSeverity.HIGH,
                status=ConsolidationStatus.IDENTIFIED,
                impact="Inconsistent prompt handling, version conflicts, management complexity",
                consolidation_plan="Merge both implementations into single prompt manager",
                dependencies=["prompt management", "file operations"],
                risks=["Feature conflicts", "API compatibility"],
            ),
            DuplicationInstance(
                name="Coordinate Loader",
                description="Multiple coordinate loading implementations",
                files=["cursor_agent_coords.json", "config/coordinates.json"],
                severity=DuplicationSeverity.HIGH,
                status=ConsolidationStatus.IDENTIFIED,
                impact="Inconsistent coordinate management, agent positioning conflicts",
                consolidation_plan="Create unified coordinate loading system",
                dependencies=["JSON parsing", "configuration management"],
                risks=["Agent positioning errors", "Configuration conflicts"],
            ),
            DuplicationInstance(
                name="ML Pipeline Core",
                description="Duplicate ML pipeline implementations",
                files=["src/core/ml_pipeline.py", "tools/ml_pipeline_core.py"],
                severity=DuplicationSeverity.HIGH,
                status=ConsolidationStatus.IDENTIFIED,
                impact="Inconsistent ML processing, model training conflicts, pipeline errors",
                consolidation_plan="Merge ML pipeline implementations into single core",
                dependencies=["machine learning", "pipeline management"],
                risks=["Model compatibility", "Training disruption"],
            ),
        ]

    def analyze_duplications(self) -> dict[str, Any]:
        """Analyze all system duplications."""
        analysis = {
            "analysis_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_duplications": len(self.duplications),
            "duplications_by_severity": {},
            "duplications_by_status": {},
            "ssot_violations": 0,
            "v2_compliance_issues": 0,
            "maintenance_complexity_score": 0.0,
            "consolidation_priority_order": [],
            "risk_assessment": {},
        }

        # Count by severity
        severity_counts = {}
        status_counts = {}
        for dup in self.duplications:
            severity_counts[dup.severity.value] = severity_counts.get(dup.severity.value, 0) + 1
            status_counts[dup.status.value] = status_counts.get(dup.status.value, 0) + 1

        analysis["duplications_by_severity"] = severity_counts
        analysis["duplications_by_status"] = status_counts

        # Calculate SSOT violations (multiple files doing same thing)
        analysis["ssot_violations"] = sum(1 for dup in self.duplications if len(dup.files) > 1)

        # Calculate V2 compliance issues (based on file count and complexity)
        analysis["v2_compliance_issues"] = len([d for d in self.duplications if len(d.files) > 2])

        # Calculate maintenance complexity score (0-100)
        total_files = sum(len(d.files) for d in self.duplications)
        unique_files = len(set(f for d in self.duplications for f in d.files))
        duplication_ratio = (total_files - unique_files) / total_files if total_files > 0 else 0
        analysis["maintenance_complexity_score"] = min(100.0, duplication_ratio * 100)

        # Create consolidation priority order
        priority_order = []
        for severity in [
            DuplicationSeverity.CRITICAL,
            DuplicationSeverity.HIGH,
            DuplicationSeverity.MEDIUM,
            DuplicationSeverity.LOW,
        ]:
            for dup in self.duplications:
                if dup.severity == severity:
                    priority_order.append(
                        {
                            "name": dup.name,
                            "severity": dup.severity.value,
                            "file_count": len(dup.files),
                            "impact": dup.impact,
                        }
                    )

        analysis["consolidation_priority_order"] = priority_order

        # Risk assessment
        analysis["risk_assessment"] = self._assess_consolidation_risks()

        return analysis

    def _assess_consolidation_risks(self) -> dict[str, Any]:
        """Assess risks associated with consolidation."""
        risks = {
            "high_risk_consolidations": [],
            "medium_risk_consolidations": [],
            "low_risk_consolidations": [],
            "overall_risk_level": "medium",
        }

        for dup in self.duplications:
            if dup.severity == DuplicationSeverity.CRITICAL:
                risks["high_risk_consolidations"].append(
                    {"name": dup.name, "risks": dup.risks, "impact": dup.impact}
                )
            elif dup.severity == DuplicationSeverity.HIGH:
                risks["medium_risk_consolidations"].append(
                    {"name": dup.name, "risks": dup.risks, "impact": dup.impact}
                )
            else:
                risks["low_risk_consolidations"].append(
                    {"name": dup.name, "risks": dup.risks, "impact": dup.impact}
                )

        # Determine overall risk level
        if len(risks["high_risk_consolidations"]) > 2:
            risks["overall_risk_level"] = "high"
        elif len(risks["high_risk_consolidations"]) == 0:
            risks["overall_risk_level"] = "low"

        return risks

    def create_consolidation_plan(self) -> dict[str, Any]:
        """Create comprehensive consolidation plan."""
        plan = {
            "consolidation_plan": {
                "plan_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_duplications": len(self.duplications),
                "estimated_duration_days": 7,
                "required_agents": ["Agent-5", "Agent-1", "Agent-7", "Agent-8", "Agent-6"],
                "phases": [
                    {
                        "phase": 1,
                        "name": "Analysis and Planning",
                        "duration_days": 1,
                        "tasks": [
                            "Complete system-wide duplication audit",
                            "Map all dependencies and relationships",
                            "Prioritize consolidations by impact",
                            "Create detailed migration strategy",
                            "Assemble consolidation team",
                        ],
                        "responsible_agents": ["Agent-5", "Agent-1"],
                    },
                    {
                        "phase": 2,
                        "name": "Critical Consolidation",
                        "duration_days": 2,
                        "tasks": [
                            "Consolidate persistent memory (3 files)",
                            "Create unified memory management system",
                            "Migrate existing data safely",
                            "Test memory system functionality",
                        ],
                        "responsible_agents": ["Agent-1", "Agent-7"],
                    },
                    {
                        "phase": 3,
                        "name": "High Priority Consolidation",
                        "duration_days": 2,
                        "tasks": [
                            "Consolidate Aletheia prompt manager (2 files)",
                            "Consolidate coordinate loader (2 files)",
                            "Consolidate ML pipeline core (2 files)",
                            "Test all consolidated systems",
                        ],
                        "responsible_agents": ["Agent-1", "Agent-7", "Agent-6"],
                    },
                    {
                        "phase": 4,
                        "name": "Validation and Testing",
                        "duration_days": 1,
                        "tasks": [
                            "V2 compliance validation",
                            "Functionality testing",
                            "Performance validation",
                            "Documentation updates",
                        ],
                        "responsible_agents": ["Agent-8", "Agent-7"],
                    },
                    {
                        "phase": 5,
                        "name": "Cleanup and Documentation",
                        "duration_days": 1,
                        "tasks": [
                            "Remove duplicate files",
                            "Update all references",
                            "Create consolidation documentation",
                            "Archive old implementations",
                        ],
                        "responsible_agents": ["Agent-7", "Agent-8"],
                    },
                ],
                "success_metrics": {
                    "ssot_compliance": "100%",
                    "v2_compliance": "100%",
                    "maintenance_reduction": "60-80%",
                    "bug_reduction": "50-70%",
                    "performance_improvement": "20-40%",
                },
                "risk_mitigation": {
                    "data_backup": "Complete backups before consolidation",
                    "rollback_plan": "Maintain old systems until validation complete",
                    "testing_strategy": "Comprehensive testing at each phase",
                    "coordination_protocol": "Daily progress reporting",
                },
            }
        }

        return plan

    def update_duplication_status(self, name: str, status: ConsolidationStatus):
        """Update status of a duplication."""
        for dup in self.duplications:
            if dup.name == name:
                dup.status = status
                break

    def get_consolidation_progress(self) -> dict[str, Any]:
        """Get current consolidation progress."""
        completed = len([d for d in self.duplications if d.status == ConsolidationStatus.COMPLETED])
        in_progress = len(
            [d for d in self.duplications if d.status == ConsolidationStatus.IN_PROGRESS]
        )
        total = len(self.duplications)

        return {
            "total_duplications": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": total - completed - in_progress,
            "completion_percentage": (completed / total) * 100 if total > 0 else 0,
            "current_phase": "Critical Consolidation"
            if completed == 0
            else "High Priority Consolidation",
        }

    def export_consolidation_analysis(self, filepath: str) -> bool:
        """Export consolidation analysis to JSON file."""
        try:
            analysis = {
                "consolidation_analysis": self.analyze_duplications(),
                "consolidation_plan": self.create_consolidation_plan(),
                "progress_report": self.get_consolidation_progress(),
                "duplication_details": [
                    {
                        "name": dup.name,
                        "description": dup.description,
                        "files": dup.files,
                        "severity": dup.severity.value,
                        "status": dup.status.value,
                        "impact": dup.impact,
                        "consolidation_plan": dup.consolidation_plan,
                        "dependencies": dup.dependencies,
                        "risks": dup.risks,
                    }
                    for dup in self.duplications
                ],
                "export_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

            with open(filepath, "w") as f:
                json.dump(analysis, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting consolidation analysis: {e}")
            return False

