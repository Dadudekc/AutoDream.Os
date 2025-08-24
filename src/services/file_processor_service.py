#!/usr/bin/env python3
"""
File Processor Service - Agent Cellphone V2
===========================================

TDD-compliant file processing service for multiple file types.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import logging
import time

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, Any, List

from .language_analyzer_service import LanguageAnalyzerService
from .file_analysis_utils import FileAnalysisUtils

logger = logging.getLogger(__name__)


class FileProcessorService:
    """
    Processes files to extract metadata, statistics, and analysis results.
    Handles multiple file types and provides comprehensive file information.
    """

    def __init__(self):
        """Initialize file processor with language analyzer."""
        self.language_analyzer = LanguageAnalyzerService()
        self.cache = {}

    def process_file(self, file_path: Path, use_cache: bool = False) -> Dict[str, Any]:
        """
        Process a single file and extract comprehensive information.

        Args:
            file_path: Path to the file to process
            use_cache: Whether to use cached results

        Returns:
            Dict containing file analysis results
        """
        start_time = time.time()
        file_key = str(file_path.absolute())

        if use_cache and file_key in self.cache:
            result = self.cache[file_key].copy()
            result["from_cache"] = True
            return result

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            # Basic file information
            stat = file_path.stat()
            content = file_path.read_text(encoding="utf-8")

            result = {
                "file_path": str(file_path),
                "file_type": self._get_file_type(file_path),
                "size_bytes": stat.st_size,
                "lines_count": len(content.splitlines()) if content else 0,
                "encoding": "utf-8",
                "has_syntax_errors": False,
                "from_cache": False,
            }

            # Language-specific analysis
            if content and file_path.suffix in [".py", ".js", ".ts", ".rs"]:
                try:
                    lang_result = self.language_analyzer.analyze_file(
                        file_path, content
                    )
                    result.update(
                        {
                            "functions_count": len(lang_result.get("functions", [])),
                            "classes_count": len(lang_result.get("classes", {})),
                            "structs_count": lang_result.get("structs_count", 0),
                            "complexity_score": lang_result.get("complexity", 0),
                        }
                    )

                    # Set complexity level
                    complexity = result["complexity_score"]
                    if complexity <= 5:
                        result["complexity_level"] = "low"
                    elif complexity <= 10:
                        result["complexity_level"] = "medium"
                    elif complexity <= 20:
                        result["complexity_level"] = "high"
                    else:
                        result["complexity_level"] = "very_high"

                except Exception as e:
                    result["has_syntax_errors"] = True
                    result["error_details"] = str(e)
                    result.update(
                        {
                            "functions_count": 0,
                            "classes_count": 0,
                            "structs_count": 0,
                            "complexity_score": 0,
                            "complexity_level": "unknown",
                        }
                    )
            else:
                result.update(
                    {
                        "functions_count": 0,
                        "classes_count": 0,
                        "structs_count": 0,
                        "complexity_score": 0,
                        "complexity_level": "unknown",
                    }
                )

            # Extract imports (Python only for now)
            if file_path.suffix == ".py" and content:
                result["imports"] = FileAnalysisUtils.extract_python_imports(content)

            # Extract TODO/FIXME comments
            result["work_items"] = FileAnalysisUtils.extract_work_items(content)

            # Performance metrics
            processing_time = (time.time() - start_time) * 1000
            result["processing_time_ms"] = round(processing_time, 2)
            result["memory_usage_bytes"] = len(content)

            # Cache result
            if use_cache:
                self.cache[file_key] = result.copy()

            return result

        except UnicodeDecodeError:
            # Try different encodings
            for encoding in ["latin-1", "cp1252", "ascii"]:
                try:
                    content = file_path.read_text(encoding=encoding)
                    result["encoding"] = encoding
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise Exception(f"Could not decode file {file_path}")

    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type from extension."""
        return FileAnalysisUtils.get_file_type(file_path)

    def process_files_batch(self, file_paths: List[Path]) -> List[Dict[str, Any]]:
        """Process multiple files in batch."""
        results = []
        for file_path in file_paths:
            try:
                result = self.process_file(file_path)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
                results.append(
                    {"file_path": str(file_path), "error": str(e), "processed": False}
                )
        return results

    def get_file_stats(self, file_paths: List[Path]) -> Dict[str, Any]:
        """Get comprehensive statistics for multiple files."""
        results = self.process_files_batch(file_paths)
        return FileAnalysisUtils.get_file_stats_summary(results)
