#!/usr/bin/env python3
"""
Project Analyzer - Core Analysis Module
========================================

Handles core project structure analysis and consolidation opportunity detection.
Part of comprehensive_project_analyzer.py refactoring (623→<400L).

Author: Agent-2 - Architecture & Design Specialist
Pattern: Facade + Module Splitting (CONSOLIDATION_ARCHITECTURE_PATTERNS.md)
"""

import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from project_analyzer_file import FileAnalyzer


class CoreAnalyzer:
    """Core project analysis and consolidation detection."""

    def __init__(self, project_root: Path, chunk_size: int = 50):
        """Initialize core analyzer."""
        self.project_root = project_root
        self.chunk_size = chunk_size
        self.file_analyzer = FileAnalyzer()

    def get_project_structure(self) -> dict[str, Any]:
        """Get comprehensive project structure."""
        structure = {}
        total_files = 0
        total_dirs = 0
        file_types = Counter()

        for root, dirs, files in os.walk(self.project_root):
            rel_path = os.path.relpath(root, self.project_root)
            if rel_path == ".":
                rel_path = ""

            # Skip certain directories
            skip_dirs = ["__pycache__", ".git", "node_modules", "venv", ".venv", "env"]
            dirs[:] = [d for d in dirs if d not in skip_dirs]

            file_counts = Counter(Path(f).suffix.lower() for f in files)

            structure[rel_path or "."] = {
                "files": file_counts,
                "file_count": len(files),
                "subdirs": len(dirs),
                "total_files": len(files),
            }

            total_files += len(files)
            total_dirs += len(dirs)
            file_types.update(file_counts)

        return {
            "structure": structure,
            "total_files": total_files,
            "total_dirs": total_dirs,
            "file_types": dict(file_types),
        }

    def analyze_directory_chunk(self, directory: str, chunk_id: int) -> dict[str, Any]:
        """Analyze a directory chunk for consolidation."""
        if not os.path.exists(directory):
            return {"error": f"Directory not found: {directory}"}

        print(f"🔍 Analyzing directory chunk {chunk_id}: {directory}")

        files_analyzed = []
        total_files = 0
        total_lines = 0
        total_functions = 0
        total_classes = 0
        total_imports = 0
        file_types = Counter()
        complexity_by_type = defaultdict(list)
        imports_by_file = defaultdict(list)
        consolidation_opportunities = []

        for root, dirs, files in os.walk(directory):
            # Skip certain directories
            skip_dirs = ["__pycache__", ".git", "node_modules", "venv", ".venv", "env"]
            dirs[:] = [d for d in dirs if d not in skip_dirs]

            for file in files:
                if total_files >= self.chunk_size:
                    break

                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.project_root)

                print(f"  📄 Analyzing: {rel_path}")
                analysis = self.file_analyzer.analyze_file(file_path)

                files_analyzed.append({"file_path": rel_path, "analysis": analysis})

                # Update totals
                total_files += 1
                total_lines += analysis.get("line_count", 0)
                total_functions += analysis.get("function_count", 0)
                total_classes += analysis.get("class_count", 0)
                total_imports += analysis.get("import_count", 0)

                # Track file types
                file_type = analysis.get("language", "unknown")
                file_types[file_type] += 1

                # Track complexity
                complexity_by_type[file_type].append(analysis.get("complexity", 0))

                # Track imports
                if analysis.get("imports"):
                    imports_by_file[rel_path] = analysis["imports"]

                # Identify consolidation opportunities
                if self.identify_consolidation_opportunity(analysis, rel_path):
                    consolidation_opportunities.append(
                        {
                            "file_path": rel_path,
                            "reason": self.get_consolidation_reason(analysis),
                            "priority": self.get_consolidation_priority(analysis),
                        }
                    )

            if total_files >= self.chunk_size:
                break

        # Calculate averages
        avg_complexity_by_type = {}
        for file_type, complexities in complexity_by_type.items():
            avg_complexity_by_type[file_type] = (
                sum(complexities) / len(complexities) if complexities else 0
            )

        return {
            "chunk_id": chunk_id,
            "directory": directory,
            "files_analyzed": files_analyzed,
            "summary": {
                "total_files": total_files,
                "total_lines": total_lines,
                "total_functions": total_functions,
                "total_classes": total_classes,
                "total_imports": total_imports,
                "file_types": dict(file_types),
                "avg_complexity_by_type": avg_complexity_by_type,
            },
            "consolidation_opportunities": consolidation_opportunities,
            "imports_analysis": dict(imports_by_file),
        }

    def identify_consolidation_opportunity(self, analysis: dict[str, Any], file_path: str) -> bool:
        """Identify if a file is a consolidation opportunity."""
        # Small files with few functions
        if analysis.get("line_count", 0) < 50 and analysis.get("function_count", 0) < 3:
            return True

        # Files with no functions or classes
        if analysis.get("function_count", 0) == 0 and analysis.get("class_count", 0) == 0:
            return True

        # Duplicate patterns
        if "messaging_pyautogui" in file_path or "config" in file_path:
            return True

        # Very small files
        if analysis.get("file_size", 0) < 1000:
            return True

        return False

    def get_consolidation_reason(self, analysis: dict[str, Any]) -> str:
        """Get reason for consolidation."""
        reasons = []

        if analysis.get("line_count", 0) < 50:
            reasons.append("Small file (<50 lines)")
        if analysis.get("function_count", 0) < 3:
            reasons.append("Few functions (<3)")
        if analysis.get("function_count", 0) == 0 and analysis.get("class_count", 0) == 0:
            reasons.append("No functions or classes")
        if analysis.get("file_size", 0) < 1000:
            reasons.append("Small file size (<1KB)")

        return ", ".join(reasons) if reasons else "Potential consolidation candidate"

    def get_consolidation_priority(self, analysis: dict[str, Any]) -> str:
        """Get consolidation priority."""
        line_count = analysis.get("line_count", 0)

        if line_count < 20:
            return "HIGH"
        elif line_count < 50:
            return "MEDIUM"
        else:
            return "LOW"
