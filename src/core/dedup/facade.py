"""High level facade for deduplication workflow."""
from __future__ import annotations

import logging
from typing import Any, Dict, List

from .algorithms.detector import DuplicationDetector
from .models import DuplicationGroup
from .remediation import ConsolidationEngine
from .reporting import ReportGenerator


class DeduplicationFacade:
    """Facade that orchestrates detection, remediation and reporting."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.detector = DuplicationDetector()
        self.remediator = ConsolidationEngine()
        self.reporter = ReportGenerator()
        self.duplication_groups: List[DuplicationGroup] = []
        self.consolidation_plan: Dict[str, Any] = {}

    def analyze_codebase(self, codebase_path: str) -> Dict[str, Any]:
        self.logger.info("Starting codebase analysis: %s", codebase_path)
        self.duplication_groups = self.detector.detect_duplications(codebase_path)
        self.consolidation_plan = self.remediator.generate_consolidation_plan(
            self.duplication_groups
        )
        return {
            "duplication_groups": len(self.duplication_groups),
            "total_duplications": self.consolidation_plan.get("total_duplications", 0),
            "estimated_effort": self.consolidation_plan.get(
                "estimated_effort", "Unknown"
            ),
            "consolidation_plan": self.consolidation_plan,
        }

    def generate_report(self) -> Dict[str, Any]:
        return self.reporter.build_report(
            self.duplication_groups, self.consolidation_plan
        )

    def export_report(self, output_path: str, format_type: str = "json") -> bool:
        report = self.generate_report()
        return self.reporter.export_report(report, output_path, format_type)
