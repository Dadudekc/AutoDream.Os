#!/usr/bin/env python3
"""
DRY Elimination Engine Orchestrator
===================================

Main orchestrator for DRY elimination system.
Coordinates all DRY elimination components and provides unified interface.
V2 COMPLIANT: Focused orchestration under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR ORCHESTRATOR
@license MIT
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from ..dry_eliminator_models import (
    DRYEliminatorConfig,
    DRYViolation,
    EliminationResult,
    EliminationStrategy,
    create_default_config,
)
from .file_discovery_engine import FileDiscoveryEngine, create_file_discovery_engine
from .code_analysis_engine import CodeAnalysisEngine, create_code_analysis_engine
from .violation_detection_engine import (
    ViolationDetectionEngine,
    create_violation_detection_engine,
)
from .elimination_strategy_engine import (
    EliminationStrategyEngine,
    create_elimination_strategy_engine,
)
from .metrics_reporting_engine import (
    MetricsReportingEngine,
    create_metrics_reporting_engine,
)


class DRYEliminationEngineOrchestrator:
    """Main orchestrator for DRY elimination system."""

    def __init__(self, config: Optional[DRYEliminatorConfig] = None):
        """Initialize DRY elimination engine orchestrator."""
        self.logger = logging.getLogger(__name__)
        self.config = config or create_default_config()

        # Initialize all engines
        self.file_engine = create_file_discovery_engine(self.config)
        self.analysis_engine = create_code_analysis_engine(self.config)
        self.violation_engine = create_violation_detection_engine()
        self.elimination_engine = create_elimination_strategy_engine()
        self.metrics_engine = create_metrics_reporting_engine()

        # Analysis state
        self.python_files: List[Path] = []
        self.detected_violations: List[DRYViolation] = []
        self.elimination_results: List[EliminationResult] = []

        self.logger.info("DRY Elimination Engine Orchestrator initialized")

    def run_full_analysis(self, project_root: Path) -> Dict[str, Any]:
        """Run complete DRY analysis and elimination."""
        try:
            self.metrics_engine.start_analysis()

            # Step 1: Discover Python files
            self.logger.info("Step 1: Discovering Python files...")
            self.python_files = self.file_engine.discover_python_files(project_root)
            self.metrics_engine.update_file_metrics(
                len(self.python_files), len(self.python_files)
            )

            if not self.python_files:
                return {"error": "No Python files found for analysis"}

            # Step 2: Analyze code patterns
            self.logger.info("Step 2: Analyzing code patterns...")
            analysis_results = self.analysis_engine.analyze_multiple_files(
                self.python_files
            )

            # Step 3: Extract patterns
            self.logger.info("Step 3: Extracting patterns...")
            import_patterns = self.analysis_engine.get_import_patterns(
                self.python_files
            )
            method_patterns = self.analysis_engine.get_function_patterns(
                self.python_files
            )
            constant_patterns = self.analysis_engine.get_constant_patterns(
                self.python_files
            )
            duplicate_blocks = self.analysis_engine.find_duplicate_code_blocks(
                self.python_files
            )

            # Step 4: Detect violations
            self.logger.info("Step 4: Detecting violations...")
            violations = []
            violations.extend(
                self.violation_engine.detect_duplicate_imports(import_patterns)
            )
            violations.extend(
                self.violation_engine.detect_duplicate_methods(method_patterns)
            )
            violations.extend(
                self.violation_engine.detect_duplicate_constants(constant_patterns)
            )
            violations.extend(
                self.violation_engine.detect_unused_imports(self.python_files)
            )
            violations.extend(
                self.violation_engine.detect_duplicate_code_blocks(duplicate_blocks)
            )

            self.detected_violations = violations
            self.violation_engine.detected_violations = violations
            self.metrics_engine.update_violation_metrics(violations)

            # Step 5: Execute eliminations
            self.logger.info("Step 5: Executing eliminations...")
            elimination_results = []

            for violation in violations:
                # Determine strategy based on violation type
                strategy = self._determine_elimination_strategy(violation)
                result = self.elimination_engine.execute_elimination(
                    violation, strategy
                )
                elimination_results.append(result)

            self.elimination_results = elimination_results
            self.metrics_engine.update_elimination_metrics(elimination_results)

            # Step 6: Generate report
            self.logger.info("Step 6: Generating report...")
            self.metrics_engine.end_analysis()

            summary = self.metrics_engine.generate_summary_report(
                violations, elimination_results
            )
            summary["file_statistics"] = self.file_engine.get_file_statistics()
            summary["analysis_summary"] = self.analysis_engine.get_analysis_summary(
                self.python_files
            )

            return summary

        except Exception as e:
            self.logger.error(f"Error during full analysis: {e}")
            return {"error": str(e)}

    def _determine_elimination_strategy(
        self, violation: DRYViolation
    ) -> EliminationStrategy:
        """Determine appropriate elimination strategy for violation."""
        if violation.violation_type.value == "unused_imports":
            return EliminationStrategy.REMOVE
        elif violation.violation_type.value in [
            "duplicate_imports",
            "duplicate_constants",
        ]:
            return EliminationStrategy.CONSOLIDATE
        elif violation.violation_type.value in [
            "duplicate_methods",
            "duplicate_code_blocks",
        ]:
            return EliminationStrategy.REFACTOR
        else:
            return EliminationStrategy.REMOVE  # Default strategy

    def get_violations_summary(self) -> Dict[str, Any]:
        """Get summary of detected violations."""
        if not self.detected_violations:
            return {"total_violations": 0}

        return {
            "total_violations": len(self.detected_violations),
            "violations_by_type": self.violation_engine.get_violations_by_type(),
            "violations_by_severity": (
                self.violation_engine.get_violations_by_severity()
            ),
            "total_potential_savings": (
                self.violation_engine.get_total_potential_savings()
            ),
        }

    def get_elimination_summary(self) -> Dict[str, Any]:
        """Get summary of elimination results."""
        return self.elimination_engine.get_elimination_summary()

    def generate_detailed_report(self) -> str:
        """Generate detailed text report."""
        return self.metrics_engine.generate_detailed_report(
            self.detected_violations, self.elimination_results
        )

    def export_results(self, output_path: Path) -> bool:
        """Export results to file."""
        try:
            # Export metrics
            metrics_file = output_path / "dry_elimination_metrics.txt"
            self.metrics_engine.export_metrics_to_file(metrics_file)

            # Export detailed report
            report_file = output_path / "dry_elimination_report.txt"
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(self.generate_detailed_report())

            # Export elimination results
            results_file = output_path / "elimination_results.txt"
            self.elimination_engine.export_results(results_file)

            return True
        except Exception as e:
            self.logger.error(f"Error exporting results: {e}")
            return False

    def clear_analysis(self):
        """Clear all analysis data."""
        self.python_files.clear()
        self.detected_violations.clear()
        self.elimination_results.clear()

        # Clear engine caches
        self.file_engine.clear_cache()
        self.analysis_engine.clear_cache()
        self.violation_engine.clear_violations()
        self.elimination_engine.clear_results()
        self.metrics_engine.reset_metrics()

    def get_analysis_status(self) -> Dict[str, Any]:
        """Get current analysis status."""
        return {
            "files_discovered": len(self.python_files),
            "violations_detected": len(self.detected_violations),
            "eliminations_executed": len(self.elimination_results),
            "analysis_in_progress": (
                self.metrics_engine.start_time is not None
                and self.metrics_engine.end_time is None
            ),
        }


# Factory function for dependency injection
def create_dry_elimination_engine_orchestrator(
    config: Optional[DRYEliminatorConfig] = None,
) -> DRYEliminationEngineOrchestrator:
    """Factory function to create DRY elimination engine orchestrator with optional
    configuration."""
    return DRYEliminationEngineOrchestrator(config)


# Export for DI
__all__ = [
    "DRYEliminationEngineOrchestrator",
    "create_dry_elimination_engine_orchestrator",
]
