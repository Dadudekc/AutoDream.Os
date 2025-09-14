"""
Results Manager - V2 Compliant Module
====================================

Manages DRY elimination results and reporting.
Extracted from dry_eliminator_orchestrator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import logging
from typing import Any

from ..dry_eliminator_models import (
    DRYEliminatorConfig,
    DRYViolationType,
    EliminationResult,
    create_default_config,
)


class ResultsManager:
    """Manages DRY elimination results and reporting.

    Handles result tracking, reporting, and status management for DRY elimination
    operations.
    """

    def __init__(self, config: DRYEliminatorConfig | None = None):
        """Initialize results manager."""
        self.config = config or create_default_config()
        self.logger = logging.getLogger(__name__)

        # Results tracking
        self.elimination_results = {
            "files_processed": 0,
            "imports_consolidated": 0,
            "methods_consolidated": 0,
            "documentation_consolidated": 0,
            "classes_consolidated": 0,
            "constants_consolidated": 0,
            "error_handling_consolidated": 0,
            "algorithms_consolidated": 0,
            "interfaces_consolidated": 0,
            "tests_consolidated": 0,
            "data_structures_consolidated": 0,
            "unused_imports_removed": 0,
            "errors": [],
        }

        # Performance tracking
        self.performance_metrics = {
            "total_elimination_time": 0.0,
            "average_file_processing_time": 0.0,
            "elimination_operations_count": 0,
            "success_rate": 0.0,
        }

    def update_results(self, elimination_results: list[EliminationResult]):
        """Update results from elimination operations."""
        try:
            for result in elimination_results:
                if result.success:
                    self._increment_result_counter(result.violation_type)
                else:
                    self.elimination_results["errors"].append(result.error_message)

            self._update_performance_metrics(elimination_results)

        except Exception as e:
            self.logger.error(f"Error updating results: {e}")
            self.elimination_results["errors"].append(str(e))

    def _increment_result_counter(self, violation_type: DRYViolationType):
        """Increment appropriate result counter based on violation type."""
        type_mapping = {
            DRYViolationType.IMPORT: "imports_consolidated",
            DRYViolationType.METHOD: "methods_consolidated",
            DRYViolationType.CONSTANT: "constants_consolidated",
            DRYViolationType.DOCUMENTATION: "documentation_consolidated",
            DRYViolationType.ERROR_HANDLING: "error_handling_consolidated",
            DRYViolationType.ALGORITHM: "algorithms_consolidated",
            DRYViolationType.INTERFACE: "interfaces_consolidated",
            DRYViolationType.TEST: "tests_consolidated",
            DRYViolationType.DATA_STRUCTURE: "data_structures_consolidated",
            DRYViolationType.CLASS: "classes_consolidated",
            DRYViolationType.UNUSED_IMPORT: "unused_imports_removed",
        }

        counter_name = type_mapping.get(violation_type)
        if counter_name:
            self.elimination_results[counter_name] += 1

    def _update_performance_metrics(self, elimination_results: list[EliminationResult]):
        """Update performance metrics from elimination results."""
        try:
            successful_results = [r for r in elimination_results if r.success]
            total_results = len(elimination_results)

            if total_results > 0:
                self.performance_metrics["success_rate"] = len(successful_results) / total_results
                self.performance_metrics["elimination_operations_count"] += total_results

                # Update average processing time
                if successful_results:
                    total_time = sum(
                        r.processing_time
                        for r in successful_results
                        if hasattr(r, "processing_time")
                    )
                    if total_time > 0:
                        self.performance_metrics["total_elimination_time"] += total_time
                        self.performance_metrics["average_file_processing_time"] = (
                            self.performance_metrics["total_elimination_time"]
                            / self.performance_metrics["elimination_operations_count"]
                        )

        except Exception as e:
            self.logger.error(f"Error updating performance metrics: {e}")

    def generate_summary_report(self, elimination_time: float = 0.0) -> dict[str, Any]:
        """Generate comprehensive summary report."""
        try:
            total_consolidations = sum(
                [
                    self.elimination_results["imports_consolidated"],
                    self.elimination_results["methods_consolidated"],
                    self.elimination_results["constants_consolidated"],
                    self.elimination_results["documentation_consolidated"],
                    self.elimination_results["classes_consolidated"],
                    self.elimination_results["error_handling_consolidated"],
                    self.elimination_results["algorithms_consolidated"],
                    self.elimination_results["interfaces_consolidated"],
                    self.elimination_results["tests_consolidated"],
                    self.elimination_results["data_structures_consolidated"],
                ]
            )

            total_removals = self.elimination_results["unused_imports_removed"]
            total_errors = len(self.elimination_results["errors"])

            return {
                **self.elimination_results,
                "elimination_time_seconds": elimination_time,
                "total_consolidations": total_consolidations,
                "total_removals": total_removals,
                "total_operations": total_consolidations + total_removals,
                "error_count": total_errors,
                "success_rate": self.performance_metrics["success_rate"],
                "performance_metrics": self.performance_metrics,
                "summary": self._generate_summary_text(
                    total_consolidations, total_removals, total_errors, elimination_time
                ),
            }

        except Exception as e:
            self.logger.error(f"Error generating summary report: {e}")
            return {"error": str(e)}

    def _generate_summary_text(
        self, consolidations: int, removals: int, errors: int, time: float
    ) -> str:
        """Generate human-readable summary text."""
        try:
            parts = []

            if consolidations > 0:
                parts.append(f"consolidated {consolidations} violations")

            if removals > 0:
                parts.append(f"removed {removals} unused imports")

            if errors > 0:
                parts.append(f"encountered {errors} errors")

            if time > 0:
                parts.append(f"in {time:.2f} seconds")

            if not parts:
                return "No operations performed"

            return f"Processed {self.elimination_results['files_processed']} files, " + ", ".join(
                parts
            )

        except Exception as e:
            self.logger.error(f"Error generating summary text: {e}")
            return "Error generating summary"

    def get_results_status(self) -> dict[str, Any]:
        """Get current results status."""
        return {
            "elimination_results": self.elimination_results.copy(),
            "performance_metrics": self.performance_metrics.copy(),
            "has_errors": len(self.elimination_results["errors"]) > 0,
            "total_operations": sum(
                [
                    self.elimination_results["imports_consolidated"],
                    self.elimination_results["methods_consolidated"],
                    self.elimination_results["constants_consolidated"],
                    self.elimination_results["documentation_consolidated"],
                    self.elimination_results["classes_consolidated"],
                    self.elimination_results["error_handling_consolidated"],
                    self.elimination_results["algorithms_consolidated"],
                    self.elimination_results["interfaces_consolidated"],
                    self.elimination_results["tests_consolidated"],
                    self.elimination_results["data_structures_consolidated"],
                    self.elimination_results["unused_imports_removed"],
                ]
            ),
        }

    def reset_results(self):
        """Reset all results and metrics."""
        self.elimination_results = {
            "files_processed": 0,
            "imports_consolidated": 0,
            "methods_consolidated": 0,
            "documentation_consolidated": 0,
            "classes_consolidated": 0,
            "constants_consolidated": 0,
            "error_handling_consolidated": 0,
            "algorithms_consolidated": 0,
            "interfaces_consolidated": 0,
            "tests_consolidated": 0,
            "data_structures_consolidated": 0,
            "unused_imports_removed": 0,
            "errors": [],
        }

        self.performance_metrics = {
            "total_elimination_time": 0.0,
            "average_file_processing_time": 0.0,
            "elimination_operations_count": 0,
            "success_rate": 0.0,
        }

        self.logger.info("Results manager reset")

    def export_results(self, format: str = "json") -> dict[str, Any]:
        """Export results in specified format."""
        try:
            if format.lower() == "json":
                return self.get_results_status()
            else:
                return {"error": f"Unsupported format: {format}"}

        except Exception as e:
            self.logger.error(f"Error exporting results: {e}")
            return {"error": str(e)}
