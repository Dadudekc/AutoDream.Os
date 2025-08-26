"""Cleanup Manager - Removes generated test files and other artifacts with BaseManager inheritance."""
import os
import logging
from typing import Iterable, Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

from ...core.persistent_data_storage import PersistentDataStorage

from ...core.base_manager import BaseManager, ManagerStatus, ManagerPriority


class CleanupManager(BaseManager):
    """
    Remove generated test files and other artifacts

    Now inherits from BaseManager for unified functionality
    """

    def __init__(self, storage: Optional[PersistentDataStorage] = None):
        """Initialize cleanup manager with BaseManager"""
        super().__init__(
            manager_id="cleanup_manager",
            name="Cleanup Manager",
            description="Removes generated test files and other artifacts",
        )
        self.storage = storage or PersistentDataStorage()

        # Cleanup tracking
        self.cleanup_history: List[Dict[str, Any]] = []
        self.removed_files_count = 0
        self.removed_directories_count = 0
        self.failed_cleanups: List[Dict[str, Any]] = []

        self.logger.info("Cleanup Manager initialized")

    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================

    def _on_start(self) -> bool:
        """Initialize cleanup system"""
        try:
            self.logger.info("Starting Cleanup Manager...")

            # Clear cleanup data
            self.cleanup_history.clear()
            self.removed_files_count = 0
            self.removed_directories_count = 0
            self.failed_cleanups.clear()

            self.logger.info("Cleanup Manager started successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start Cleanup Manager: {e}")
            return False

    def _on_stop(self):
        """Cleanup cleanup system"""
        try:
            self.logger.info("Stopping Cleanup Manager...")

            # Save cleanup history
            self._save_cleanup_history()

            # Clear data
            self.cleanup_history.clear()
            self.failed_cleanups.clear()

            self.logger.info("Cleanup Manager stopped successfully")

        except Exception as e:
            self.logger.error(f"Failed to stop Cleanup Manager: {e}")

    def _on_heartbeat(self):
        """Cleanup manager heartbeat"""
        try:
            # Check cleanup health
            self._check_cleanup_health()

            # Update metrics
            self.record_operation("heartbeat", True, 0.0)

        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)

    def _on_initialize_resources(self) -> bool:
        """Initialize cleanup resources"""
        try:
            # Initialize data structures
            self.cleanup_history = []
            self.removed_files_count = 0
            self.removed_directories_count = 0
            self.failed_cleanups = []

            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False

    def _on_cleanup_resources(self):
        """Cleanup cleanup resources"""
        try:
            # Clear data
            self.cleanup_history.clear()
            self.failed_cleanups.clear()

        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")

            # Reset cleanup state
            self.removed_files_count = 0
            self.removed_directories_count = 0

            # Clear failed cleanups
            self.failed_cleanups.clear()

            self.logger.info("Recovery successful")
            return True

        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False

    # ============================================================================
    # Cleanup Management Methods
    # ============================================================================

    def cleanup(self, paths: Iterable[str]) -> int:
        """Remove generated test files and other artifacts"""
        try:
            removed = 0
            cleanup_start = datetime.now()

            for path in paths:
                try:
                    path_obj = Path(path)

                    if path_obj.is_file():
                        os.remove(path)
                        removed += 1
                        self.removed_files_count += 1
                        self.logger.debug(f"Removed file: {path}")

                    elif path_obj.is_dir():
                        # Remove directory and contents
                        import shutil

                        shutil.rmtree(path)
                        removed += 1
                        self.removed_directories_count += 1
                        self.logger.debug(f"Removed directory: {path}")

                    else:
                        self.logger.warning(f"Path not found: {path}")

                except FileNotFoundError:
                    continue
                except PermissionError:
                    self.logger.warning(f"Permission denied: {path}")
                    self._record_failed_cleanup(path, "Permission denied")
                except Exception as e:
                    self.logger.error(f"Failed to remove {path}: {e}")
                    self._record_failed_cleanup(path, str(e))

            # Record cleanup operation
            cleanup_time = (datetime.now() - cleanup_start).total_seconds()
            self._record_cleanup_operation(removed, cleanup_time)

            # Record operation
            self.record_operation("cleanup", True, cleanup_time)

            self.logger.info(f"Cleanup completed: {removed} items removed")
            return removed

        except Exception as e:
            self.logger.error(f"Cleanup operation failed: {e}")
            self.record_operation("cleanup", False, 0.0)
            return 0

    def cleanup_files_by_pattern(self, directory: str, pattern: str) -> int:
        """Clean up files matching a pattern in a directory"""
        try:
            import glob

            pattern_path = os.path.join(directory, pattern)
            matching_files = glob.glob(pattern_path)

            if not matching_files:
                self.logger.debug(f"No files found matching pattern: {pattern}")
                return 0

            removed = self.cleanup(matching_files)

            # Record operation
            self.record_operation("cleanup_files_by_pattern", True, 0.0)

            return removed

        except Exception as e:
            self.logger.error(f"Failed to cleanup files by pattern: {e}")
            self.record_operation("cleanup_files_by_pattern", False, 0.0)
            return 0

    def cleanup_test_artifacts(self, test_directory: str) -> int:
        """Clean up common test artifacts"""
        try:
            test_path = Path(test_directory)
            if not test_path.exists():
                self.logger.warning(f"Test directory not found: {test_directory}")
                return 0

            # Common test artifact patterns
            patterns = [
                "*.pyc",
                "*.pyo",
                "__pycache__",
                "*.log",
                "*.tmp",
                "*.cache",
                ".pytest_cache",
                "htmlcov",
                ".coverage",
                "*.egg-info",
                "build",
                "dist",
            ]

            total_removed = 0

            for pattern in patterns:
                if pattern in [
                    "__pycache__",
                    "build",
                    "dist",
                    "htmlcov",
                    ".pytest_cache",
                    "*.egg-info",
                ]:
                    # These are directories
                    dir_pattern = os.path.join(test_directory, pattern)
                    if os.path.exists(dir_pattern):
                        import shutil

                        shutil.rmtree(dir_pattern)
                        total_removed += 1
                        self.removed_directories_count += 1
                        self.logger.debug(
                            f"Removed test artifact directory: {dir_pattern}"
                        )
                else:
                    # These are file patterns
                    removed = self.cleanup_files_by_pattern(test_directory, pattern)
                    total_removed += removed

            # Record operation
            self.record_operation("cleanup_test_artifacts", True, 0.0)

            self.logger.info(
                f"Test artifacts cleanup completed: {total_removed} items removed"
            )
            return total_removed

        except Exception as e:
            self.logger.error(f"Failed to cleanup test artifacts: {e}")
            self.record_operation("cleanup_test_artifacts", False, 0.0)
            return 0

    def cleanup_old_files(self, directory: str, max_age_days: int = 7) -> int:
        """Clean up files older than specified days"""
        try:
            import time

            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 3600
            removed = 0

            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_age = current_time - os.path.getmtime(file_path)
                        if file_age > max_age_seconds:
                            os.remove(file_path)
                            removed += 1
                            self.removed_files_count += 1
                            self.logger.debug(f"Removed old file: {file_path}")
                    except (OSError, PermissionError) as e:
                        self.logger.warning(
                            f"Failed to remove old file {file_path}: {e}"
                        )
                        self._record_failed_cleanup(file_path, str(e))

            # Record operation
            self.record_operation("cleanup_old_files", True, 0.0)

            self.logger.info(f"Old files cleanup completed: {removed} files removed")
            return removed

        except Exception as e:
            self.logger.error(f"Failed to cleanup old files: {e}")
            self.record_operation("cleanup_old_files", False, 0.0)
            return 0

    def get_cleanup_stats(self) -> Dict[str, Any]:
        """Get cleanup statistics"""
        try:
            stats = {
                "total_files_removed": self.removed_files_count,
                "total_directories_removed": self.removed_directories_count,
                "total_items_removed": self.removed_files_count
                + self.removed_directories_count,
                "cleanup_history_size": len(self.cleanup_history),
                "failed_cleanups_count": len(self.failed_cleanups),
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds,
            }

            # Record operation
            self.record_operation("get_cleanup_stats", True, 0.0)

            return stats

        except Exception as e:
            self.logger.error(f"Failed to get cleanup stats: {e}")
            self.record_operation("get_cleanup_stats", False, 0.0)
            return {"error": str(e)}

    # ============================================================================
    # Private Helper Methods
    # ============================================================================

    def _record_cleanup_operation(self, items_removed: int, cleanup_time: float):
        """Record cleanup operation in history"""
        try:
            cleanup_record = {
                "timestamp": datetime.now().isoformat(),
                "items_removed": items_removed,
                "cleanup_time": cleanup_time,
                "files_removed": self.removed_files_count,
                "directories_removed": self.removed_directories_count,
            }

            self.cleanup_history.append(cleanup_record)

            # Keep history manageable
            if len(self.cleanup_history) > 1000:
                self.cleanup_history = self.cleanup_history[-500:]

        except Exception as e:
            self.logger.error(f"Failed to record cleanup operation: {e}")

    def _record_failed_cleanup(self, path: str, error: str):
        """Record failed cleanup attempt"""
        try:
            failed_record = {
                "timestamp": datetime.now().isoformat(),
                "path": path,
                "error": error,
            }

            self.failed_cleanups.append(failed_record)

            # Keep failed cleanups manageable
            if len(self.failed_cleanups) > 100:
                self.failed_cleanups = self.failed_cleanups[-50:]

        except Exception as e:
            self.logger.error(f"Failed to record failed cleanup: {e}")

    def _save_cleanup_history(self):
        """Save cleanup history to persistent storage"""
        try:
            existing = self.storage.retrieve_data("cleanup_history") or []
            existing.extend(self.cleanup_history)
            if len(existing) > 1000:
                existing = existing[-1000:]
            self.storage.store_data("cleanup_history", existing, "cleanup")
            self.logger.debug("Cleanup history saved")

        except Exception as e:
            self.logger.error(f"Failed to save cleanup history: {e}")

    def _check_cleanup_health(self):
        """Check cleanup health status"""
        try:
            # Check for excessive failed cleanups
            if len(self.failed_cleanups) > 50:
                self.logger.warning(
                    f"High number of failed cleanups: {len(self.failed_cleanups)}"
                )

            # Check cleanup history size
            if len(self.cleanup_history) > 500:
                self.logger.info(
                    f"Large cleanup history: {len(self.cleanup_history)} records"
                )

        except Exception as e:
            self.logger.error(f"Failed to check cleanup health: {e}")

    def get_cleanup_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent cleanup history"""
        try:
            history = (
                self.cleanup_history[-limit:]
                if limit > 0
                else self.cleanup_history.copy()
            )

            # Record operation
            self.record_operation("get_cleanup_history", True, 0.0)

            return history

        except Exception as e:
            self.logger.error(f"Failed to get cleanup history: {e}")
            self.record_operation("get_cleanup_history", False, 0.0)
            return []

    def load_cleanup_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Load cleanup history from persistent storage"""
        try:
            history = self.storage.retrieve_data("cleanup_history") or []
            history = history[-limit:] if limit > 0 else history

            self.record_operation("load_cleanup_history", True, 0.0)

            return history

        except Exception as e:
            self.logger.error(f"Failed to load cleanup history: {e}")
            self.record_operation("load_cleanup_history", False, 0.0)
            return []

    def get_failed_cleanups(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent failed cleanup attempts"""
        try:
            failed = (
                self.failed_cleanups[-limit:]
                if limit > 0
                else self.failed_cleanups.copy()
            )

            # Record operation
            self.record_operation("get_failed_cleanups", True, 0.0)

            return failed

        except Exception as e:
            self.logger.error(f"Failed to get failed cleanups: {e}")
            self.record_operation("get_failed_cleanups", False, 0.0)
            return []
