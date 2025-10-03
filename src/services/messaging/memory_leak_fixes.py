"""
Memory Leak Fixes for Messaging System
=====================================

Specific fixes for identified memory leaks and sinks in the messaging system.
Implements proper resource management and cleanup.

Author: Agent-5 (Coordinator)
License: MIT
"""

import logging
import threading
import time
import weakref
from contextlib import contextmanager
from typing import Any

logger = logging.getLogger(__name__)


class CoordinationRequestManager:
    """Fixed coordination request manager with proper cleanup"""

    def __init__(self, max_requests: int = 1000, cleanup_interval: int = 3600):
        """Initialize with memory-safe settings"""
        self.coordination_requests = {}
        self.max_requests = max_requests
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = time.time()
        self._lock = threading.Lock()

    def add_request(self, request_id: str, request_data: dict[str, Any]) -> None:
        """Add coordination request with size limits"""
        with self._lock:
            # Cleanup if needed
            if len(self.coordination_requests) >= self.max_requests:
                self._cleanup_old_requests()

            self.coordination_requests[request_id] = {
                **request_data,
                "created_at": time.time(),
                "access_count": 0,
            }

    def get_request(self, request_id: str) -> dict[str, Any] | None:
        """Get request with access tracking"""
        with self._lock:
            if request_id in self.coordination_requests:
                self.coordination_requests[request_id]["access_count"] += 1
                return self.coordination_requests[request_id]
            return None

    def _cleanup_old_requests(self) -> int:
        """Clean up old requests to prevent memory accumulation"""
        current_time = time.time()
        cleaned_count = 0

        # Remove requests older than cleanup interval
        old_requests = []
        for request_id, request in self.coordination_requests.items():
            if current_time - request["created_at"] > self.cleanup_interval:
                old_requests.append(request_id)

        for request_id in old_requests:
            del self.coordination_requests[request_id]
            cleaned_count += 1

        logger.info(f"Cleaned up {cleaned_count} old coordination requests")
        return cleaned_count

    def periodic_cleanup(self) -> None:
        """Periodic cleanup to prevent memory leaks"""
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_requests()
            self.last_cleanup = current_time


class PyAutoGUIResourceManager:
    """Manage PyAutoGUI resources and prevent memory leaks"""

    def __init__(self):
        """Initialize PyAutoGUI resource manager"""
        self.active_sessions = weakref.WeakSet()
        self.session_registry = {}
        self._lock = threading.Lock()

    @contextmanager
    def managed_session(self, session_id: str):
        """Context manager for PyAutoGUI sessions"""
        session = None
        try:
            session = self._create_session(session_id)
            yield session
        finally:
            if session:
                self._cleanup_session(session_id)

    def _create_session(self, session_id: str) -> dict[str, Any]:
        """Create PyAutoGUI session"""
        with self._lock:
            session = {
                "id": session_id,
                "created_at": time.time(),
                "last_activity": time.time(),
                "operations_count": 0,
            }
            self.active_sessions.add(session)
            self.session_registry[session_id] = session
            return session

    def _cleanup_session(self, session_id: str) -> None:
        """Cleanup PyAutoGUI session"""
        with self._lock:
            if session_id in self.session_registry:
                del self.session_registry[session_id]

    def cleanup_stale_sessions(self, max_age_seconds: int = 300) -> int:
        """Clean up stale PyAutoGUI sessions"""
        current_time = time.time()
        cleaned_count = 0

        with self._lock:
            stale_sessions = []
            for session_id, session in self.session_registry.items():
                if current_time - session["last_activity"] > max_age_seconds:
                    stale_sessions.append(session_id)

            for session_id in stale_sessions:
                del self.session_registry[session_id]
                cleaned_count += 1

        return cleaned_count


class FileResourceManager:
    """Manage file resources and prevent file handle leaks"""

    def __init__(self):
        """Initialize file resource manager"""
        self.open_files = weakref.WeakSet()
        self.file_registry = {}
        self._lock = threading.Lock()

    @contextmanager
    def managed_file(self, file_path: str, mode: str = "r"):
        """Context manager for file handles with automatic cleanup"""
        file_handle = None
        file_id = f"{file_path}_{mode}_{int(time.time())}"

        try:
            with open(file_path, mode) as file_handle:
                with self._lock:
                    self.open_files.add(file_handle)
                    self.file_registry[file_id] = {
                        "handle": file_handle,
                        "path": file_path,
                        "mode": mode,
                        "opened_at": time.time(),
                    }

                yield file_handle

        finally:
            if file_handle:
                try:
                    file_handle.close()
                except:
                    pass

                with self._lock:
                    if file_id in self.file_registry:
                        del self.file_registry[file_id]

    def cleanup_stale_files(self, max_age_seconds: int = 60) -> int:
        """Clean up stale file handles"""
        current_time = time.time()
        cleaned_count = 0

        with self._lock:
            stale_files = []
            for file_id, file_info in self.file_registry.items():
                if current_time - file_info["opened_at"] > max_age_seconds:
                    stale_files.append(file_id)

            for file_id in stale_files:
                try:
                    self.file_registry[file_id]["handle"].close()
                except:
                    pass
                del self.file_registry[file_id]
                cleaned_count += 1

        return cleaned_count


class MemoryLeakFixer:
    """Main class to fix memory leaks in messaging system"""

    def __init__(self):
        """Initialize memory leak fixer"""
        self.coordination_manager = CoordinationRequestManager()
        self.pyautogui_manager = PyAutoGUIResourceManager()
        self.file_manager = FileResourceManager()
        self.cleanup_thread = None
        self.running = False

    def start_cleanup_service(self) -> None:
        """Start background cleanup service"""
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            return

        self.running = True
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        logger.info("Memory cleanup service started")

    def stop_cleanup_service(self) -> None:
        """Stop background cleanup service"""
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=5)
        logger.info("Memory cleanup service stopped")

    def _cleanup_loop(self) -> None:
        """Background cleanup loop"""
        while self.running:
            try:
                # Cleanup coordination requests
                self.coordination_manager.periodic_cleanup()

                # Cleanup PyAutoGUI sessions
                stale_sessions = self.pyautogui_manager.cleanup_stale_sessions()
                if stale_sessions > 0:
                    logger.info(f"Cleaned up {stale_sessions} stale PyAutoGUI sessions")

                # Cleanup file handles
                stale_files = self.file_manager.cleanup_stale_files()
                if stale_files > 0:
                    logger.info(f"Cleaned up {stale_files} stale file handles")

                # Sleep for 5 minutes before next cleanup
                time.sleep(300)

            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

    def get_memory_stats(self) -> dict[str, Any]:
        """Get current memory statistics"""
        return {
            "coordination_requests": len(self.coordination_manager.coordination_requests),
            "pyautogui_sessions": len(self.pyautogui_manager.session_registry),
            "open_files": len(self.file_manager.file_registry),
            "cleanup_service_running": self.running,
        }

    def force_cleanup(self) -> dict[str, int]:
        """Force immediate cleanup of all resources"""
        logger.info("Performing forced cleanup of all resources")

        results = {
            "coordination_requests_cleaned": self.coordination_manager._cleanup_old_requests(),
            "pyautogui_sessions_cleaned": self.pyautogui_manager.cleanup_stale_sessions(),
            "file_handles_cleaned": self.file_manager.cleanup_stale_files(),
        }

        logger.info(f"Forced cleanup completed: {results}")
        return results


# Global instance for system-wide memory management
memory_fixer = MemoryLeakFixer()


def initialize_memory_management() -> None:
    """Initialize memory management for messaging system"""
    memory_fixer.start_cleanup_service()
    logger.info("Memory management initialized for messaging system")


def cleanup_memory_resources() -> dict[str, int]:
    """Cleanup memory resources"""
    return memory_fixer.force_cleanup()


def get_memory_status() -> dict[str, Any]:
    """Get current memory status"""
    return memory_fixer.get_memory_stats()
