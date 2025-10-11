#!/usr/bin/env python3
"""
Project Scanner - Workers & File Processing Module
==================================================

Handles threading, multibot management, file hashing, and exclusion logic.

V2 Compliance: Extracted from projectscanner.py (1,153 lines → modular)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-10-11
License: MIT
"""

import hashlib
import logging
import queue
import threading
from pathlib import Path

logger = logging.getLogger(__name__)


class BotWorker(threading.Thread):
    """
    A background worker that pulls file tasks from a queue,
    processes them, and appends results to results_list.
    """

    def __init__(self, task_queue: queue.Queue, results_list: list, scanner, status_callback=None):
        super().__init__()
        self.task_queue = task_queue
        self.results_list = results_list
        self.scanner = scanner
        self.status_callback = status_callback
        self.daemon = True
        self.start()

    def run(self):
        while True:
            file_path = self.task_queue.get()
            if file_path is None:
                break
            result = self.scanner._process_file(file_path)
            if result is not None:
                self.results_list.append(result)
            if self.status_callback:
                self.status_callback(file_path, result)
            self.task_queue.task_done()


class MultibotManager:
    """Manages a pool of BotWorker threads."""

    def __init__(self, scanner, num_workers=4, status_callback=None):
        self.task_queue = queue.Queue()
        self.results_list = []
        self.scanner = scanner
        self.status_callback = status_callback
        self.workers = [
            BotWorker(self.task_queue, self.results_list, scanner, status_callback)
            for _ in range(num_workers)
        ]

    def add_task(self, file_path: Path):
        self.task_queue.put(file_path)

    def wait_for_completion(self):
        self.task_queue.join()

    def stop_workers(self):
        for _ in self.workers:
            self.task_queue.put(None)


class FileProcessor:
    """Handles file hashing, ignoring, caching checks, etc."""

    def __init__(
        self,
        project_root: Path,
        cache: dict,
        cache_lock: threading.Lock,
        additional_ignore_dirs: set,
    ):
        self.project_root = project_root
        self.cache = cache
        self.cache_lock = cache_lock
        self.additional_ignore_dirs = additional_ignore_dirs

    def hash_file(self, file_path: Path) -> str:
        try:
            with file_path.open("rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""

    def should_exclude(self, file_path: Path) -> bool:
        """Exclude logic for venvs, node_modules, .git, etc."""
        # Common virtual environment patterns
        venv_patterns = {
            "venv",
            "env",
            ".env",
            ".venv",
            "virtualenv",
            "ENV",
            "VENV",
            ".ENV",
            ".VENV",
            "python-env",
            "python-venv",
            "py-env",
            "py-venv",
            # Common Conda environment locations
            "envs",
            "conda-env",
            ".conda-env",
            # Poetry virtual environments
            ".poetry/venv",
            ".poetry-venv",
        }

        default_exclude_dirs = {
            "__pycache__",
            "node_modules",
            "migrations",
            "build",
            "target",
            ".git",
            "coverage",
            "chrome_profile",
            "framework_disabled",
        } | venv_patterns  # Merge with venv patterns

        file_abs = file_path.resolve()

        # Check if this is the scanner itself
        try:
            if file_abs == Path(__file__).resolve():
                return True
        except NameError:
            pass

        # Check additional ignore directories
        for ignore in self.additional_ignore_dirs:
            ignore_path = Path(ignore)
            if not ignore_path.is_absolute():
                ignore_path = (self.project_root / ignore_path).resolve()
            try:
                file_abs.relative_to(ignore_path)
                return True
            except ValueError:
                continue

        # Check for virtual environment indicators
        try:
            # Look for pyvenv.cfg or similar files that indicate a venv
            if any(p.name == "pyvenv.cfg" for p in file_abs.parents):
                return True

            # Look for bin/activate or Scripts/activate.bat
            for parent in file_abs.parents:
                if (parent / "bin" / "activate").exists() or (
                    parent / "Scripts" / "activate.bat"
                ).exists():
                    return True
        except (OSError, PermissionError):
            # Handle permission errors gracefully
            pass

        # Check for excluded directory names in the path
        if any(excluded in file_path.parts for excluded in default_exclude_dirs):
            return True

        # Check for common virtual environment path patterns
        path_str = str(file_abs).lower()
        if any(f"/{pattern}/" in path_str.replace("\\", "/") for pattern in venv_patterns):
            return True

        return False

    def process_file(self, file_path: Path, language_analyzer) -> tuple | None:
        """Analyzes a file if not in cache or changed, else returns None."""
        file_hash_val = self.hash_file(file_path)
        relative_path = str(file_path.relative_to(self.project_root))
        with self.cache_lock:
            if (
                relative_path in self.cache
                and self.cache[relative_path].get("hash") == file_hash_val
            ):
                return None
        try:
            with file_path.open("r", encoding="utf-8") as f:
                source_code = f.read()
            analysis_result = language_analyzer.analyze_file(file_path, source_code)
            with self.cache_lock:
                self.cache[relative_path] = {"hash": file_hash_val}
            return (relative_path, analysis_result)
        except Exception as e:
            logger.error(f"❌ Error analyzing {file_path}: {e}")
            return None
