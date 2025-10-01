"""
Thread Manager for Safe Threading
=================================

Manages thread lifecycle to prevent leaks.

Author: Captain Agent-4
License: MIT
"""

import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class ThreadManager:
    """Manage threads with proper cleanup."""
    
    def __init__(self, max_workers: int = 10):
        """Initialize thread manager."""
        self.threads: List[threading.Thread] = []
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
    
    def start_thread(
        self,
        target: Callable,
        name: Optional[str] = None,
        daemon: bool = True,
        **kwargs
    ) -> threading.Thread:
        """Start a managed thread."""
        thread = threading.Thread(
            target=target,
            name=name,
            daemon=daemon,
            **kwargs
        )
        with self._lock:
            self.threads.append(thread)
        thread.start()
        return thread
    
    def submit_task(self, func: Callable, *args, **kwargs):
        """Submit task to thread pool."""
        return self.executor.submit(func, *args, **kwargs)
    
    def stop_all(self, timeout: float = 5.0) -> int:
        """Stop all threads gracefully."""
        self._stop_event.set()
        stopped = 0
        
        with self._lock:
            for thread in self.threads:
                try:
                    thread.join(timeout=timeout)
                    stopped += 1
                except Exception as e:
                    logger.warning(f"Thread stop error: {e}")
            self.threads.clear()
        
        self.executor.shutdown(wait=True, cancel_futures=True)
        return stopped
    
    def get_stats(self) -> Dict[str, Any]:
        """Get thread statistics."""
        with self._lock:
            return {
                "active_threads": len([t for t in self.threads if t.is_alive()]),
                "total_threads": len(self.threads),
                "stop_requested": self._stop_event.is_set()
            }


# Global thread manager
_global_thread_manager = ThreadManager()


def get_thread_manager() -> ThreadManager:
    """Get global thread manager."""
    return _global_thread_manager

