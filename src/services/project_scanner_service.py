#!/usr/bin/env python3
"""
Project Scanner Service - Agent Cellphone V2
===========================================

Scans entire projects for comprehensive analysis.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import os
import time

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from .language_analyzer_service import LanguageAnalyzerService
from .file_processor_service import FileProcessorService


class ProjectScannerService:
    """
    Scans entire projects for comprehensive analysis.

    Responsibilities:
    - Scan project directories recursively
    - Analyze project structure and dependencies
    - Coordinate file analysis across multiple workers
    - Generate project-wide insights
    """

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.language_analyzer = LanguageAnalyzerService()
        self.file_processor = FileProcessorService()
        self.scanned_files: Set[Path] = set()
        self.analysis_cache: Dict[Path, Dict[str, Any]] = {}

    def scan_project(
        self, project_path: Path, include_hidden: bool = False
    ) -> Dict[str, Any]:
        """Scan entire project for comprehensive analysis"""
        try:
            start_time = time.time()

            # Discover all files in project
            all_files = self._discover_project_files(project_path, include_hidden)
            supported_files = self._filter_supported_files(all_files)

            # Analyze files in parallel
            analysis_results = self._analyze_files_parallel(supported_files)

            # Generate project summary
            project_summary = self._generate_project_summary(
                project_path, analysis_results, time.time() - start_time
            )

            return project_summary

        except Exception as e:
            return {"error": str(e), "status": "failed", "timestamp": time.time()}

    def scan_directory(
        self, directory_path: Path, recursive: bool = True
    ) -> List[Dict[str, Any]]:
        """Scan specific directory for files"""
        try:
            files = []

            if recursive:
                for file_path in directory_path.rglob("*"):
                    if file_path.is_file():
                        files.append(self._analyze_single_file(file_path))
            else:
                for file_path in directory_path.iterdir():
                    if file_path.is_file():
                        files.append(self._analyze_single_file(file_path))

            return files

        except Exception as e:
            return [{"error": str(e), "status": "failed"}]

    def get_project_structure(self, project_path: Path) -> Dict[str, Any]:
        """Get hierarchical project structure"""
        try:
            structure = {
                "name": project_path.name,
                "type": "directory",
                "path": str(project_path),
                "children": [],
            }

            for item in project_path.iterdir():
                if item.is_dir():
                    structure["children"].append(self._get_directory_structure(item))
                else:
                    structure["children"].append(
                        {
                            "name": item.name,
                            "type": "file",
                            "path": str(item),
                            "size": item.stat().st_size,
                        }
                    )

            return structure

        except Exception as e:
            return {"error": str(e), "status": "failed"}

    def _discover_project_files(
        self, project_path: Path, include_hidden: bool
    ) -> List[Path]:
        """Discover all files in project directory"""
        files = []

        try:
            for file_path in project_path.rglob("*"):
                if file_path.is_file():
                    # Skip hidden files unless explicitly included
                    if not include_hidden and any(
                        part.startswith(".") for part in file_path.parts
                    ):
                        continue

                    # Skip common directories to ignore
                    if self._should_skip_directory(file_path):
                        continue

                    files.append(file_path)
        except Exception as e:
            # Handle permission errors gracefully
            pass

        return files

    def _filter_supported_files(self, files: List[Path]) -> List[Path]:
        """Filter files to only include supported types"""
        supported_extensions = {
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".rs",
            ".java",
            ".cpp",
            ".c",
            ".h",
            ".hpp",
            ".cs",
            ".go",
            ".rb",
            ".php",
            ".swift",
            ".kt",
        }

        return [f for f in files if f.suffix.lower() in supported_extensions]

    def _should_skip_directory(self, file_path: Path) -> bool:
        """Check if directory should be skipped during scanning"""
        skip_dirs = {
            "__pycache__",
            "node_modules",
            ".git",
            ".svn",
            ".hg",
            "build",
            "dist",
            "target",
            "bin",
            "obj",
            ".vs",
        }

        return any(part in skip_dirs for part in file_path.parts)

    def _analyze_files_parallel(self, files: List[Path]) -> List[Dict[str, Any]]:
        """Analyze multiple files in parallel using thread pool"""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all file analysis tasks
            future_to_file = {
                executor.submit(self._analyze_single_file, file_path): file_path
                for file_path in files
            }

            # Collect results as they complete
            for future in as_completed(future_to_file):
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    file_path = future_to_file[future]
                    results.append(
                        {
                            "name": file_path.name,
                            "path": str(file_path),
                            "error": str(e),
                            "status": "failed",
                        }
                    )

        return results

    def _analyze_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file for comprehensive insights"""
        try:
            # Check cache first
            if file_path in self.analysis_cache:
                return self.analysis_cache[file_path]

            # Basic file information
            file_info = {
                "name": file_path.name,
                "path": str(file_path),
                "size": file_path.stat().st_size,
                "modified": file_path.stat().st_mtime,
                "status": "analyzed",
            }

            # Language analysis
            language_info = self.language_analyzer.analyze_file(file_path)
            file_info.update(language_info)

            # File processing
            file_data = self.file_processor.process_file(file_path)
            file_info.update(file_data)

            # Cache the result
            self.analysis_cache[file_path] = file_info
            self.scanned_files.add(file_path)

            return file_info

        except Exception as e:
            return {
                "name": file_path.name,
                "path": str(file_path),
                "error": str(e),
                "status": "failed",
            }

    def _generate_project_summary(
        self,
        project_path: Path,
        analysis_results: List[Dict[str, Any]],
        scan_time: float,
    ) -> Dict[str, Any]:
        """Generate comprehensive project summary"""
        try:
            # Filter successful analyses
            successful_analyses = [
                r for r in analysis_results if r.get("status") == "analyzed"
            ]
            failed_analyses = [
                r for r in analysis_results if r.get("status") == "failed"
            ]

            # Calculate statistics
            total_files = len(analysis_results)
            total_lines = sum(r.get("line_count", 0) for r in successful_analyses)
            total_complexity = sum(r.get("complexity", 0) for r in successful_analyses)

            # Language distribution
            language_stats = self._calculate_language_distribution(successful_analyses)

            # File size distribution
            size_stats = self._calculate_size_distribution(successful_analyses)

            summary = {
                "project_name": project_path.name,
                "project_path": str(project_path),
                "scan_timestamp": time.time(),
                "scan_duration": round(scan_time, 2),
                "summary": {
                    "total_files": total_files,
                    "successful_analyses": len(successful_analyses),
                    "failed_analyses": len(failed_analyses),
                    "total_lines": total_lines,
                    "average_complexity": round(
                        total_complexity / len(successful_analyses), 2
                    )
                    if successful_analyses
                    else 0.0,
                },
                "language_breakdown": language_stats,
                "size_analysis": size_stats,
                "files": successful_analyses,
                "errors": failed_analyses,
            }

            return summary

        except Exception as e:
            return {"error": str(e), "status": "failed", "timestamp": time.time()}

    def _calculate_language_distribution(
        self, analyses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate language distribution statistics"""
        language_counts = {}
        language_lines = {}

        for analysis in analyses:
            lang = analysis.get("language", "unknown")
            lines = analysis.get("line_count", 0)

            language_counts[lang] = language_counts.get(lang, 0) + 1
            language_lines[lang] = language_lines.get(lang, 0) + lines

        return {
            "file_counts": language_counts,
            "line_counts": language_lines,
            "primary_language": max(language_counts.items(), key=lambda x: x[1])[0]
            if language_counts
            else "unknown",
        }

    def _calculate_size_distribution(
        self, analyses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate file size distribution statistics"""
        sizes = [a.get("line_count", 0) for a in analyses]

        if not sizes:
            return {"small": 0, "medium": 0, "large": 0, "oversized": 0}

        distribution = {"small": 0, "medium": 0, "large": 0, "oversized": 0}

        for size in sizes:
            if size <= 50:
                distribution["small"] += 1
            elif size <= 200:
                distribution["medium"] += 1
            elif size <= 500:
                distribution["large"] += 1
            else:
                distribution["oversized"] += 1

        return distribution

    def _get_directory_structure(self, directory_path: Path) -> Dict[str, Any]:
        """Recursively get directory structure"""
        try:
            structure = {
                "name": directory_path.name,
                "type": "directory",
                "path": str(directory_path),
                "children": [],
            }

            for item in directory_path.iterdir():
                if item.is_dir():
                    structure["children"].append(self._get_directory_structure(item))
                else:
                    structure["children"].append(
                        {
                            "name": item.name,
                            "type": "file",
                            "path": str(item),
                            "size": item.stat().st_size,
                        }
                    )

            return structure

        except Exception:
            return {
                "name": directory_path.name,
                "type": "directory",
                "path": str(directory_path),
                "error": "Access denied",
                "children": [],
            }
