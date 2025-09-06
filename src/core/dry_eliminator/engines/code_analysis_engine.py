#!/usr/bin/env python3
"""
Code Analysis Engine - KISS Compliant
=====================================

Simple code analysis engine.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class CodeAnalysisEngine:
    """Simple code analysis engine."""

    def __init__(self, config=None):
        """Initialize code analysis engine."""
        self.config = config or {}
        self.logger = logger
        self.analysis_history = []
        self.parsed_files = {}

    def analyze_code(self, code_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code for patterns."""
        try:
            if not code_data:
                return {"error": "No code data provided"}

            # Simple code analysis
            patterns = self._extract_patterns(code_data)
            duplicates = self._find_duplicates(code_data)
            metrics = self._calculate_metrics(code_data)

            result = {
                "patterns": patterns,
                "duplicates": duplicates,
                "metrics": metrics,
                "timestamp": datetime.now().isoformat(),
            }

            # Store in history
            self.analysis_history.append(result)
            if len(self.analysis_history) > 100:  # Keep only last 100
                self.analysis_history.pop(0)

            self.logger.info(f"Code analyzed: {len(patterns)} patterns found")
            return result

        except Exception as e:
            self.logger.error(f"Error analyzing code: {e}")
            return {"error": str(e)}

    def _extract_patterns(self, code_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract patterns from code."""
        try:
            patterns = []

            # Simple pattern extraction
            if "functions" in code_data:
                for func in code_data["functions"]:
                    if isinstance(func, dict) and "name" in func:
                        patterns.append(
                            {
                                "type": "function",
                                "name": func["name"],
                                "pattern": "function_def",
                            }
                        )

            return patterns
        except Exception as e:
            self.logger.error(f"Error extracting patterns: {e}")
            return []

    def _find_duplicates(self, code_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find duplicate code patterns."""
        try:
            duplicates = []

            # Simple duplicate detection
            if "functions" in code_data:
                seen = set()
                for func in code_data["functions"]:
                    if isinstance(func, dict) and "name" in func:
                        name = func["name"]
                        if name in seen:
                            duplicates.append(
                                {
                                    "type": "duplicate_function",
                                    "name": name,
                                    "pattern": "duplicate",
                                }
                            )
                        else:
                            seen.add(name)

            return duplicates
        except Exception as e:
            self.logger.error(f"Error finding duplicates: {e}")
            return []

    def _calculate_metrics(self, code_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate code metrics."""
        try:
            metrics = {
                "total_functions": 0,
                "duplicate_functions": 0,
                "complexity_score": 0,
            }

            if "functions" in code_data:
                metrics["total_functions"] = len(code_data["functions"])

            return metrics
        except Exception as e:
            self.logger.error(f"Error calculating metrics: {e}")
            return {}

    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get analysis summary."""
        try:
            if not self.analysis_history:
                return {"message": "No analysis data available"}

            total_analyses = len(self.analysis_history)
            recent_analysis = self.analysis_history[-1] if self.analysis_history else {}

            return {
                "total_analyses": total_analyses,
                "recent_analysis": recent_analysis,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            self.logger.error(f"Error getting analysis summary: {e}")
            return {"error": str(e)}

    def clear_analysis_history(self) -> None:
        """Clear analysis history."""
        self.analysis_history.clear()
        self.parsed_files.clear()
        self.logger.info("Analysis history cleared")

    def get_status(self) -> Dict[str, Any]:
        """Get engine status."""
        return {
            "active": True,
            "analysis_count": len(self.analysis_history),
            "parsed_files": len(self.parsed_files),
            "timestamp": datetime.now().isoformat(),
        }


# Simple factory function
def create_code_analysis_engine(config=None) -> CodeAnalysisEngine:
    """Create code analysis engine."""
    return CodeAnalysisEngine(config)


__all__ = ["CodeAnalysisEngine", "create_code_analysis_engine"]
