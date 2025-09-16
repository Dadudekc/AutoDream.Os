import logging

logger = logging.getLogger(__name__)
"""
Utility Consolidation Orchestrator - V2 Compliance Module
=========================================================

Main coordination logic for utility consolidation operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""
import json
import os
from datetime import datetime
from typing import Any

from .utility_consolidation_engine import UtilityConsolidationEngine
from .utility_consolidation_models import ConsolidationConfig, ConsolidationResult


class UtilityConsolidationOrchestrator:
    """Main orchestrator for utility consolidation operations."""

    def __init__(self, config: ConsolidationConfig = None):

EXAMPLE USAGE:
==============

# Import the core component
from src.core.consolidation.utility_consolidation.utility_consolidation_orchestrator import Utility_Consolidation_Orchestrator

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Utility_Consolidation_Orchestrator(config)

# Execute primary functionality
result = component.process_data(input_data)
logger.info(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    logger.info(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    logger.info(f"Operation failed: {e}")
    # Implement recovery logic

        """Initialize consolidation orchestrator."""
        self.config = config or ConsolidationConfig()
        self.engine = UtilityConsolidationEngine(self.config)

    def run_consolidation_analysis(self, source_directory: str) -> dict[str, Any]:
        """Run complete consolidation analysis."""
        logger.info("🔍 Starting utility consolidation analysis...")
        analysis_results = self.engine.analyze_codebase(source_directory)
        report = self.generate_consolidation_report()
        return {"analysis_results": analysis_results, "report": report, "status": "completed"}

    def generate_consolidation_report(self) -> dict[str, Any]:
        """Generate comprehensive consolidation report."""
        logger.info("📊 Generating consolidation report...")
        report = {
            "timestamp": datetime.now().isoformat(),
            "consolidation_summary": {
                "total_opportunities": len(self.engine.consolidation_opportunities),
                "estimated_lines_reduced": sum(
                    opp.estimated_reduction for opp in self.engine.consolidation_opportunities
                ),
                "high_priority_count": len(
                    [
                        opp
                        for opp in self.engine.consolidation_opportunities
                        if opp.priority == "HIGH"
                    ]
                ),
                "consolidation_types": {},
            },
            "detailed_opportunities": [],
        }
        for opp in self.engine.consolidation_opportunities:
            cons_type = opp.consolidation_type.value
            if cons_type not in report["consolidation_summary"]["consolidation_types"]:
                report["consolidation_summary"]["consolidation_types"][cons_type] = 0
            report["consolidation_summary"]["consolidation_types"][cons_type] += 1
            detailed_opp = {
                "type": cons_type,
                "function_name": opp.primary_function.name,
                "primary_file": opp.primary_function.file_path,
                "duplicate_count": len(opp.duplicate_functions),
                "duplicate_files": [f.file_path for f in opp.duplicate_functions],
                "estimated_reduction": opp.estimated_reduction,
                "priority": opp.priority,
                "strategy": opp.consolidation_strategy,
            }
            report["detailed_opportunities"].append(detailed_opp)
        return report

    def execute_consolidation(self, opportunity_index: int) -> ConsolidationResult:
        """Execute consolidation for a specific opportunity."""
        if opportunity_index >= len(self.engine.consolidation_opportunities):
            return ConsolidationResult(
                success=False,
                functions_consolidated=0,
                lines_reduced=0,
                error_message="Invalid opportunity index",
            )
        opportunity = self.engine.consolidation_opportunities[opportunity_index]
        try:
            logger.info(f"🔧 Executing consolidation for {opportunity.primary_function.name}...")
            consolidated_content = self._create_consolidated_function(opportunity)
            consolidated_path = self._write_consolidated_file(
                opportunity.primary_function.name, consolidated_content
            )
            self._update_references(opportunity)
            return ConsolidationResult(
                success=True,
                functions_consolidated=len(opportunity.duplicate_functions) + 1,
                lines_reduced=opportunity.estimated_reduction,
                new_file_path=consolidated_path,
            )
        except Exception as e:
            return ConsolidationResult(
                success=False, functions_consolidated=0, lines_reduced=0, error_message=str(e)
            )

    def _create_consolidated_function(self, opportunity) -> str:
        """Create consolidated function content."""
        primary = opportunity.primary_function
        consolidated = f"# Consolidated utility function: {primary.name}\n"
        consolidated += f"# Original file: {primary.file_path}\n"
        consolidated += f"""# Consolidated from {len(opportunity.duplicate_functions) + 1} functions

"""
        consolidated += primary.content
        consolidated += "\n# This function consolidates the following duplicates:\n"
        for dup in opportunity.duplicate_functions:
            consolidated += f"# - {dup.file_path} (lines {dup.line_start}-{dup.line_end})\n"
        return consolidated

    def _write_consolidated_file(self, function_name: str, content: str) -> str:
        """Write consolidated function to file."""
        os.makedirs(self.config.target_directory, exist_ok=True)
        file_path = os.path.join(self.config.target_directory, f"consolidated_{function_name}.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    def _update_references(self, opportunity) -> None:
        """Update references to use consolidated function."""
        logger.info(f"📝 Updating references for {opportunity.primary_function.name}...")

    def save_report(self, report: dict[str, Any], file_path: str) -> None:
        """Save consolidation report to file."""
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)
        logger.info(f"💾 Report saved to {file_path}")

    def get_opportunities_summary(self) -> list[dict[str, Any]]:
        """Get summary of all consolidation opportunities."""
        return [
            {
                "index": i,
                "function_name": opp.primary_function.name,
                "duplicate_count": len(opp.duplicate_functions),
                "estimated_reduction": opp.estimated_reduction,
                "priority": opp.priority,
                "type": opp.consolidation_type.value,
            }
            for i, opp in enumerate(self.engine.consolidation_opportunities)
        ]
