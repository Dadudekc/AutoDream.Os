#!/usr/bin/env python3
"""
Project Scanner - Core Orchestrator
===================================

Main ProjectScanner class that orchestrates the entire scanning process.

V2 Compliance: Extracted from projectscanner.py (1,153 lines → modular)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-10-11
License: MIT
"""

import json
import logging
import os
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

from projectscanner_language_analyzer import LanguageAnalyzer
from projectscanner_legacy_reports import ReportGenerator
from projectscanner_modular_reports import ModularReportGenerator
from projectscanner_workers import FileProcessor, MultibotManager

logger = logging.getLogger(__name__)

# Cache file for incremental scanning
CACHE_FILE = "dependency_cache.json"


class ProjectScanner:
    """
    A universal project scanner that:
      - Identifies Python, Rust, JS, TS files.
      - Extracts functions, classes, routes, complexity.
      - Caches file hashes to skip unchanged files.
      - Detects moved files by matching file hashes.
      - Merges new analysis into existing project_analysis.json (preserving old entries).
      - Exports a merged ChatGPT context if requested (preserving old context data).
      - Processes files asynchronously with BotWorker threads.
      - Auto-generates __init__.py files for Python packages.
    """

    def __init__(self, project_root: str | Path = "."):
        self.project_root = Path(project_root).resolve()
        self.analysis: dict[str, dict] = {}
        self.cache = self.load_cache()
        self.cache_lock = threading.Lock()
        self.additional_ignore_dirs = set()
        self.language_analyzer = LanguageAnalyzer()
        self.file_processor = FileProcessor(
            self.project_root, self.cache, self.cache_lock, self.additional_ignore_dirs
        )
        self.report_generator = ReportGenerator(self.project_root, self.analysis)
        self.modular_report_generator = ModularReportGenerator(self.project_root, self.analysis)

    def load_cache(self) -> dict:
        """Loads JSON cache from disk if present. Otherwise returns empty."""
        cache_path = Path(CACHE_FILE)
        if cache_path.exists():
            try:
                with cache_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_cache(self):
        """Writes the updated cache to disk."""
        cache_path = Path(CACHE_FILE)
        with cache_path.open("w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=4)

    def scan_project(self, progress_callback: Callable | None = None):
        """
        Orchestrates the project scan:
        - Finds Python, Rust, JS, TS files with os.walk()
        - Excludes certain directories
        - Detects moved files by comparing cached hashes
        - Spawns multibot workers for concurrency
        - Merges new analysis with old project_analysis.json (preserving old data)
        - Writes/updates 'project_analysis.json' without overwriting unscanned files
        - Reports progress via progress_callback(percent)
        """
        logger.info(f"🔍 Scanning project: {self.project_root} ...")

        file_extensions = {".py", ".rs", ".js", ".ts"}
        valid_files = []
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            if self.file_processor.should_exclude(root_path):
                continue
            for file in files:
                file_path = root_path / file
                if (
                    file_path.suffix.lower() in file_extensions
                    and not self.file_processor.should_exclude(file_path)
                ):
                    valid_files.append(file_path)

        total_files = len(valid_files)
        logger.info(f"📝 Found {total_files} valid files for analysis.")

        # Progress reporting: update every file processed
        processed_count = 0

        previous_files = set(self.cache.keys())
        current_files = {str(f.relative_to(self.project_root)) for f in valid_files}
        moved_files = {}
        missing_files = previous_files - current_files

        # Detect moved files by matching file hashes
        for old_path in previous_files:
            old_hash = self.cache.get(old_path, {}).get("hash")
            if not old_hash:
                continue
            for new_path in current_files:
                new_file = self.project_root / new_path
                if self.file_processor.hash_file(new_file) == old_hash:
                    moved_files[old_path] = new_path
                    break

        # Remove truly missing files from cache
        for missing_file in missing_files:
            if missing_file not in moved_files:
                with self.cache_lock:
                    if missing_file in self.cache:
                        del self.cache[missing_file]

        # Update cache for moved files
        for old_path, new_path in moved_files.items():
            with self.cache_lock:
                self.cache[new_path] = self.cache.pop(old_path)

        # Asynchronous processing
        logger.info("⏱️  Processing files asynchronously...")
        num_workers = os.cpu_count() or 4
        manager = MultibotManager(
            scanner=self,
            num_workers=num_workers,
            status_callback=lambda fp, res: logger.info(f"Processed: {fp}"),
        )
        for file_path in valid_files:
            manager.add_task(file_path)
        manager.wait_for_completion()
        manager.stop_workers()

        # Update progress for each processed file
        for result in manager.results_list:
            processed_count += 1
            if progress_callback:
                percent = int((processed_count / total_files) * 100)
                progress_callback(percent)
            if result is not None:
                file_path, analysis_result = result
                self.analysis[file_path] = analysis_result

        # Merge & write final report + save updated cache
        self.report_generator.save_report()
        self.save_cache()
        logger.info(
            f"✅ Scan complete. Results merged into {self.project_root / 'project_analysis.json'} (preserving existing file data)"
        )

    def _process_file(self, file_path: Path):
        """Processes a file via FileProcessor, returning (relative_path, analysis_result)."""
        return self.file_processor.process_file(file_path, self.language_analyzer)

    def generate_init_files(self, overwrite: bool = True):
        """Generate __init__.py for python packages."""
        self.report_generator.generate_init_files(overwrite)

    def export_chatgpt_context(
        self, template_path: str | None = None, output_path: str | None = None
    ):
        """Merges new analysis into old chatgpt_project_context.json or uses a Jinja template, preserving existing data."""
        self.report_generator.export_chatgpt_context(template_path, output_path)

    def generate_modular_reports(self):
        """Generate multiple smaller, agent-digestible analysis files."""
        self.modular_report_generator.generate_modular_reports()

    # ----- Agent Categorization -----
    def categorize_agents(self):
        """
        Loops over analyzed Python classes, assigning maturity & agent_type.
        """
        for file_path, result in self.analysis.items():
            if file_path.endswith(".py"):
                for class_name, class_data in result.get("classes", {}).items():
                    class_data["maturity"] = self._maturity_level(class_name, class_data)
                    class_data["agent_type"] = self._agent_type(class_name, class_data)

    def _maturity_level(self, class_name: str, class_data: dict[str, Any]) -> str:
        score = 0
        if class_data.get("docstring"):
            score += 1
        if len(class_data.get("methods", [])) > 3:
            score += 1
        if any(base for base in class_data.get("base_classes", []) if base not in ("object", None)):
            score += 1
        if class_name and class_name[0].isupper():
            score += 1
        levels = ["Kiddie Script", "Prototype", "Core Asset", "Core Asset"]
        return levels[min(score, 3)]

    def _agent_type(self, class_name: str, class_data: dict[str, Any]) -> str:
        doc = (class_data.get("docstring") or "").lower()
        methods = class_data.get("methods", [])
        if "run" in methods:
            return "ActionAgent"
        if "transform" in doc or "parse" in doc:
            return "DataAgent"
        if any(m in methods for m in ["predict", "analyze"]):
            return "SignalAgent"
        return "Utility"
