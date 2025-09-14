"""
DRY Eliminator Orchestrator - V2 Compliant Module
================================================

Main orchestrator for DRY violation elimination system.
Coordinates all elimination components and provides unified interface.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import logging
from pathlib import Path
from typing import Any

from ..dry_eliminator_models import DRYEliminatorConfig, DRYViolationType, create_default_config
from .elimination_coordinator import EliminationCoordinator
from .results_manager import ResultsManager


class AdvancedDRYEliminator:
    """Main orchestrator for advanced DRY violation elimination system.

    Provides unified interface to all DRY elimination capabilities while maintaining V2
    compliance through modular architecture.
    """

    def __init__(self, config: DRYEliminatorConfig | None = None):
        """Initialize advanced DRY eliminator."""
        self.config = config or create_default_config()
        self.logger = logging.getLogger(__name__)
        self.coordinator = EliminationCoordinator(self.config)
        self.results_manager = ResultsManager(self.config)
        self.is_active = False
        self.current_operation = None
        self.project_root = Path.cwd()
        self.logger.info("Advanced DRY Eliminator initialized")

    def eliminate_advanced_dry_violations(self) -> dict[str, Any]:
        """Execute advanced DRY violation elimination."""
        try:
            self.is_active = True
            self.current_operation = "advanced_elimination"
            results = self.coordinator.eliminate_advanced_dry_violations()
            if "elimination_results" in results:
                self.results_manager.update_results(results["elimination_results"])
            return results
        except Exception as e:
            self.logger.error(f"Error in advanced DRY elimination: {e}")
            return {"error": str(e)}
        finally:
            self.is_active = False
            self.current_operation = None

    def analyze_project_violations(self) -> dict[str, Any]:
        """Analyze project for DRY violations without elimination."""
        return self.coordinator.analyze_project_violations()

    def eliminate_specific_violations(
        self, violation_types: list[DRYViolationType]
    ) -> dict[str, Any]:
        """Eliminate specific types of violations."""
        return self.coordinator.eliminate_specific_violations(violation_types)

    def get_system_status(self) -> dict[str, Any]:
        """Get comprehensive system status and metrics."""
        coordinator_status = self.coordinator.get_coordinator_status()
        results_status = self.results_manager.get_results_status()
        return {
            "is_active": self.is_active,
            "current_operation": self.current_operation,
            "project_root": str(self.project_root),
            "configuration": {
                "dry_run_mode": self.config.dry_run_mode,
                "backup_before_modification": self.config.backup_before_modification,
                "max_concurrent_operations": self.config.max_concurrent_operations,
                "enabled_analyses": {
                    "imports": self.config.enable_import_analysis,
                    "methods": self.config.enable_method_analysis,
                    "constants": self.config.enable_constant_analysis,
                    "documentation": self.config.enable_documentation_analysis,
                    "error_handling": self.config.enable_error_handling_analysis,
                    "algorithms": self.config.enable_algorithm_analysis,
                    "interfaces": self.config.enable_interface_analysis,
                    "tests": self.config.enable_test_analysis,
                    "data_structures": self.config.enable_data_structure_analysis,
                },
            },
            "coordinator_status": coordinator_status,
            "results_status": results_status,
        }

    def reset_elimination_state(self):
        """Reset elimination state and clear results."""
        self.coordinator.reset_coordinator_state()
        self.results_manager.reset_results()
        self.logger.info("Elimination state reset")

    def get_performance_report(self) -> dict[str, Any]:
        """Get performance report from results manager."""
        return self.results_manager.generate_summary_report()

    def export_results(self, format: str = "json") -> dict[str, Any]:
        """Export results in specified format."""
        return self.results_manager.export_results(format)


class UnifiedEntryPoint:
    """Unified entry point for backward compatibility."""

    def __init__(self):
        self.eliminator = AdvancedDRYEliminator()

    def run_elimination(self) -> dict[str, Any]:
        """Run elimination process."""
        return self.eliminator.eliminate_advanced_dry_violations()


_global_eliminator = None


def get_advanced_dry_eliminator() -> AdvancedDRYEliminator:
    """Get global advanced DRY eliminator instance."""
    global _global_eliminator
    if _global_eliminator is None:
        _global_eliminator = AdvancedDRYEliminator()
    return _global_eliminator


def eliminate_advanced_dry_violations() -> dict[str, Any]:
    """Eliminate advanced DRY violations (backward compatibility function)."""
    eliminator = get_advanced_dry_eliminator()
    return eliminator.eliminate_advanced_dry_violations()


def main():
    """Main entry point for command line usage."""
    eliminator = AdvancedDRYEliminator()
    results = eliminator.eliminate_advanced_dry_violations()
    logger.info("🎯 Advanced DRY Elimination Results:")
    logger.info(f"Files processed: {results.get('files_processed', 0)}")
    logger.info(f"Violations eliminated: {results.get('total_violations_eliminated', 0)}")
    logger.info(f"Lines reduced: {results.get('net_lines_reduced', 0)}")
    logger.info(f"Success rate: {results.get('success_rate', 0):.1%}")
    return results


if __name__ == "__main__":
    main()
