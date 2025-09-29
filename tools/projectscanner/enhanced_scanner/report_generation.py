#!/usr/bin/env python3
"""
Report Generation Handler - V2 Compliant
========================================

Handles report generation for enhanced project scanner.
V2 Compliance: ≤150 lines, single responsibility, KISS principle.
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ReportGenerationHandler:
    """Handles report generation for enhanced project scanner."""

    def __init__(self, core):
        """Initialize report generation handler."""
        self.core = core
        self.report_generator = None

    def generate_enhanced_reports(self) -> None:
        """Generate enhanced analysis reports."""

        logger.info("📊 Generating enhanced reports")

        # Initialize report generator
        if not self.report_generator:
            from ..enhanced_analyzer import EnhancedReportGenerator

            self.report_generator = EnhancedReportGenerator()

        # Generate main analysis report
        analysis_report = self.report_generator.generate_analysis_report(self.core.analysis)

        # Save to file
        report_path = self.core.project_root / "project_analysis.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(analysis_report, f, indent=2, ensure_ascii=False)

        logger.info(f"💾 Analysis report saved to: {report_path}")

        # Generate summary report
        summary_report = self.report_generator.generate_summary_report(self.core.analysis)

        # Save summary
        summary_path = self.core.project_root / "analysis_summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary_report, f, indent=2, ensure_ascii=False)

        logger.info(f"📋 Summary report saved to: {summary_path}")

    def export_chatgpt_context(self, template_path: str | None = None) -> None:
        """Export ChatGPT context for project analysis."""

        logger.info("🤖 Exporting ChatGPT context")

        # Generate ChatGPT context
        chatgpt_context = self.report_generator.generate_chatgpt_context(
            self.core.analysis, self.core.project_root
        )

        # Save context
        context_path = self.core.project_root / "chatgpt_project_context.json"
        with open(context_path, "w", encoding="utf-8") as f:
            json.dump(chatgpt_context, f, indent=2, ensure_ascii=False)

        logger.info(f"💬 ChatGPT context saved to: {context_path}")

    def generate_init_files(self, overwrite: bool = True) -> None:
        """Generate __init__.py files for Python packages."""

        logger.info("🐍 Generating __init__.py files")

        init_count = 0

        for file_path, analysis in self.core.analysis.items():
            if analysis.get("language") == "Python":
                dir_path = Path(file_path).parent
                init_path = dir_path / "__init__.py"

                if not init_path.exists() or overwrite:
                    try:
                        with open(init_path, "w", encoding="utf-8") as f:
                            f.write('"""Package initialization."""\n')
                        init_count += 1
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to create {init_path}: {e}")

        logger.info(f"✅ Generated {init_count} __init__.py files")
