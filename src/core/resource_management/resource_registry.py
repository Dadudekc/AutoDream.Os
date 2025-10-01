"""
Resource Registry for Memory Leak Prevention
============================================

Tracks and manages all resources to prevent leaks.

Author: Captain Agent-4
License: MIT
"""

import logging
import threading
import weakref
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ResourceRegistry:
    """Registry for tracking and cleaning up resources."""
    
    def __init__(self):
        """Initialize resource registry."""
        self.resources = weakref.WeakSet()
        self._lock = threading.Lock()
        self._resource_types: Dict[str, int] = {}
    
    def register(self, resource: Any, resource_type: str = "unknown") -> Any:
        """Register a resource for tracking."""
        with self._lock:
            self.resources.add(resource)
            self._resource_types[resource_type] = (
                self._resource_types.get(resource_type, 0) + 1
            )
        return resource
    
    def cleanup_all(self, timeout: float = 5.0) -> int:
        """Clean up all registered resources."""
        cleaned = 0
        with self._lock:
            for resource in list(self.resources):
                try:
                    if hasattr(resource, 'close'):
                        resource.close()
                    elif hasattr(resource, 'join'):
                        resource.join(timeout=timeout)
                    elif hasattr(resource, 'terminate'):
                        resource.terminate()
                    cleaned += 1
                except Exception as e:
                    logger.warning(f"Cleanup error: {e}")
        return cleaned
    
    def get_stats(self) -> Dict[str, Any]:
        """Get resource statistics."""
        with self._lock:
            return {
                "total_resources": len(self.resources),
                "by_type": dict(self._resource_types)
            }


# Global registry instance
_global_registry = ResourceRegistry()


def get_registry() -> ResourceRegistry:
    """Get global resource registry."""
    return _global_registry

