#!/usr/bin/env python3
"""
Enhanced Language Analyzer Core - V2 Compliant
==============================================

Core enhanced language analyzer functionality.
V2 Compliance: ≤200 lines, single responsibility, KISS principle.
"""

import logging
from pathlib import Path
from typing import Any

from .caching_system import EnhancedCachingSystem
from .language_analyzer import EnhancedLanguageAnalyzer
from .report_generator import EnhancedReportGenerator

logger = logging.getLogger(__name__)


class EnhancedAnalyzerCore:
    """Core enhanced analyzer coordinator."""

    def __init__(self, project_root: Path | None = None):
        """Initialize enhanced analyzer components."""
        self.project_root = project_root or Path(".")
        self.analysis: dict[str, dict[str, Any]] = {}

        # Initialize modular components
        self.language_analyzer = EnhancedLanguageAnalyzer()
        self.caching_system = EnhancedCachingSystem()
        self.report_generator = None  # Will be initialized with analysis data

        logger.info("🔍 Enhanced Analyzer Core initialized")

    def analyze_file(self, file_path: Path, source_code: str) -> dict[str, Any]:
        """Analyze a file using enhanced language analysis."""
        try:
            # Check cache first
            relative_path = str(file_path.relative_to(self.project_root))
            if self.caching_system.is_file_cached(file_path, relative_path):
                cached_result = self.caching_system.get_cached_analysis(file_path, relative_path)
                if cached_result:
                    logger.debug(f"📋 Using cached analysis for {relative_path}")
                    return cached_result

            # Perform fresh analysis
            analysis_result = self.language_analyzer.analyze_file(file_path, source_code)

            # Cache the result
            self.caching_system.update_file_cache(file_path, relative_path, analysis_result)

            # Store in analysis
            self.analysis[relative_path] = analysis_result

            logger.debug(f"✅ Analyzed {relative_path}")
            return analysis_result

        except Exception as e:
            logger.error(f"❌ Error analyzing {file_path}: {e}")
            return {
                "language": file_path.suffix,
                "functions": [],
                "classes": {},
                "routes": [],
                "complexity": 0,
                "maturity": "Unknown",
                "agent_type": "Unknown",
                "error": str(e),
            }

    def detect_moved_files(self, current_files: set) -> dict[str, str]:
        """Detect moved files using caching system."""
        return self.caching_system.detect_moved_files(current_files, self.project_root)

    def cleanup_missing_files(self, current_files: set):
        """Cleanup cache for missing files."""
        self.caching_system.cleanup_missing_files(current_files, self.project_root)

    def generate_reports(self):
        """Generate enhanced reports."""
        if not self.report_generator:
            self.report_generator = EnhancedReportGenerator(self.project_root, self.analysis)

        self.report_generator.generate_enhanced_reports()

    def export_chatgpt_context(self):
        """Export ChatGPT context."""
        if self.report_generator:
            self.report_generator.export_chatgpt_context()

    def get_analysis_summary(self) -> dict[str, Any]:
        """Get comprehensive analysis summary."""
        if not self.analysis:
            return {"total_files": 0, "languages": {}, "complexity": 0}

        languages = {}
        total_complexity = 0

        for file_path, analysis in self.analysis.items():
            lang = analysis.get("language", "unknown")
            languages[lang] = languages.get(lang, 0) + 1
            total_complexity += analysis.get("complexity", 0)

        return {
            "total_files": len(self.analysis),
            "languages": languages,
            "total_complexity": total_complexity,
            "average_complexity": total_complexity / len(self.analysis) if self.analysis else 0,
            "analysis": self.analysis,
        }

    def save_cache(self):
        """Save analysis cache."""
        self.caching_system.save_cache()

    def load_cache(self):
        """Load analysis cache."""
        self.caching_system.load_cache()
