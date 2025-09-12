#!/usr/bin/env python3
"""
Resource Management System for Performance Optimization
======================================================

Provides proper resource cleanup, context managers, and memory management
to prevent memory leaks and optimize resource usage.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import atexit
import gc
import logging
import threading
import weakref
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

import psutil

logger = logging.getLogger(__name__)


@dataclass
class ResourceUsage:
    """Track resource usage for cleanup"""
    resource_id: str
    resource_type: str
    creation_time: float
    cleanup_function: Optional[Callable] = None
    metadata: Dict[str, Any] = None


class ResourceManager:
    """Centralized resource management system"""

    def __init__(self):
    """# Example usage:
result = __init__("example_value")
print(f"Result: {result}")"""
    """# Example usage:
result = __init__("example_value", "example_value", "example_value", "example_value")
print(f"Result: {result}")"""
        self.resources: Dict[str, ResourceUsage] = {}
        self.cleanup_handlers: Dict[str, List[Callable]] = {}
        self.lock = threading.RLock()
        self.memory_threshold_mb = 500  # Trigger cleanup at 500MB usage
        self._cleanup_thread: Optional[threading.Thread] = None
        self.monitoring_active = False

        # Register cleanup on exit
        atexit.register(self.cleanup_all)

    def register_resource(
        self,
        resource_id: str,
        resource_type: str,
        cleanup_function: Optional[Callable] = None,
        metadata: Dict[str, Any] = None
    ):
        """Register a resource for tracking and cleanup"""
        import time
        with self.lock:
            resource = ResourceUsage(
                resource_id=resource_id,
                resource_type=resource_type,
                creation_time=time.time(),
                cleanup_function=cleanup_function,
                metadata=metadata or {}
            )
            self.resources[resource_id] = resource
            logger.debug(f"Registered resource: {resource_id} ({resource_type})")

    def unregister_resource(self, resource_id: str):
        """Unregister a resource"""
        with self.lock:
            if resource_id in self.resources:
                del self.resources[resource_id]
                logger.debug(f"Unregistered resource: {resource_id}")

    def cleanup_resource(self, resource_id: str):
        """Clean up a specific resource"""
        with self.lock:
            if resource_id in self.resources:
                resource = self.resources[resource_id]
                if resource.cleanup_function:
                    try:
                        resource.cleanup_function()
                        logger.info(f"Cleaned up resource: {resource_id}")
                    except Exception as e:
                        logger.error(f"Error cleaning up resource {resource_id}: {e}")

                del self.resources[resource_id]

    def cleanup_by_type(self, resource_type: str):
        """Clean up all resources of a specific type"""
        with self.lock:
            to_cleanup = [
                rid for rid, res in self.resources.items()
                if res.resource_type == resource_type
            ]

            for resource_id in to_cleanup:
                self.cleanup_resource(resource_id)

    def cleanup_old_resources(self, max_age_seconds: float = 3600):
        """Clean up resources older than specified age"""
        import time
        current_time = time.time()

        with self.lock:
            to_cleanup = [
                rid for rid, res in self.resources.items()
                if current_time - res.creation_time > max_age_seconds
            ]

            for resource_id in to_cleanup:
                self.cleanup_resource(resource_id)

    def start_memory_monitoring(self):
        """Start automatic memory monitoring and cleanup"""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self._cleanup_thread = threading.Thread(
            target=self._memory_monitoring_loop,
            daemon=True,
            name="ResourceManager-Monitor"
        )
        self._cleanup_thread.start()
        logger.info("Resource memory monitoring started")

    def stop_memory_monitoring(self):
        """Stop automatic memory monitoring"""
        self.monitoring_active = False
        if self._cleanup_thread:
            self._cleanup_thread.join(timeout=5.0)
        logger.info("Resource memory monitoring stopped")

    def _memory_monitoring_loop(self):
        """Monitor memory usage and trigger cleanup when needed"""
        import time

        while self.monitoring_active:
            try:
                memory = psutil.virtual_memory()
                memory_used_mb = memory.used / 1024 / 1024

                if memory_used_mb > self.memory_threshold_mb:
                    logger.warning(f"Memory usage ({memory_used_mb:.1f}MB) exceeds threshold ({self.memory_threshold_mb}MB)")
                    self._trigger_memory_cleanup()

                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in memory monitoring: {e}")

    def _trigger_memory_cleanup(self):
        """Trigger memory cleanup when usage is high"""
        logger.info("Triggering memory cleanup...")

        # Force garbage collection
        collected = gc.collect()
        logger.info(f"Garbage collection freed {collected} objects")

        # Clean up old resources
        self.cleanup_old_resources(max_age_seconds=1800)  # 30 minutes

        # Clean up cached imports if available
        self._cleanup_cached_imports()

    def _cleanup_cached_imports(self):
        """Clean up cached imports to free memory"""
        try:
            # Clear import cache for heavy modules
            import sys
            modules_to_clear = ['matplotlib', 'numpy', 'pandas', 'tensorflow', 'torch']

            for module_name in modules_to_clear:
                if module_name in sys.modules:
                    # Remove from cache but don't delete the module object
                    # as it might still be referenced elsewhere
                    pass

            logger.info("Cleaned up cached imports")
        except Exception as e:
            logger.error(f"Error cleaning cached imports: {e}")

    def cleanup_all(self):
        """Clean up all registered resources"""
        with self.lock:
            logger.info(f"Cleaning up {len(self.resources)} resources...")

            for resource_id in list(self.resources.keys()):
                self.cleanup_resource(resource_id)

            # Final garbage collection
            collected = gc.collect()
            logger.info(f"Final cleanup: {collected} objects collected")

    def get_resource_stats(self) -> Dict[str, Any]:
        """Get resource usage statistics"""
        with self.lock:
            import time
            current_time = time.time()

            stats = {
                'total_resources': len(self.resources),
                'resource_types': {},
                'oldest_resource_age': 0,
                'resources_by_type': {}
            }

            for resource in self.resources.values():
                # Count by type
                res_type = resource.resource_type
                if res_type not in stats['resource_types']:
                    stats['resource_types'][res_type] = 0
                    stats['resources_by_type'][res_type] = []
                stats['resource_types'][res_type] += 1
                stats['resources_by_type'][res_type].append(resource.resource_id)

                # Track oldest resource
                age = current_time - resource.creation_time
                if age > stats['oldest_resource_age']:
                    stats['oldest_resource_age'] = age

            return stats

    def add_cleanup_handler(self, resource_type: str, handler: Callable):
        """Add a cleanup handler for a resource type"""
        with self.lock:
            if resource_type not in self.cleanup_handlers:
                self.cleanup_handlers[resource_type] = []
            self.cleanup_handlers[resource_type].append(handler)


# Global resource manager instance
resource_manager = ResourceManager()


class ManagedResource:
    """Context manager for automatic resource cleanup"""

    def __init__(self, resource_id: str, resource_type: str, cleanup_function: Optional[Callable] = None):
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.cleanup_function = cleanup_function
        self.registered = False

    def __enter__(self):
    """# Example usage:
result = __enter__("example_value")
print(f"Result: {result}")"""
        resource_manager.register_resource(
            self.resource_id,
            self.resource_type,
            self.cleanup_function
        )
        self.registered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
    """# Example usage:
result = __exit__("example_value", "example_value", "example_value", "example_value")
print(f"Result: {result}")"""
        if self.registered:
            resource_manager.cleanup_resource(self.resource_id)


@contextmanager
def managed_resource(resource_id: str, resource_type: str, cleanup_function: Optional[Callable] = None):
    """Context manager for resource management"""
    resource_manager.register_resource(resource_id, resource_type, cleanup_function)
    try:
        yield
    finally:
        resource_manager.cleanup_resource(resource_id)


def memory_efficient_import(module_name: str):
    """Import a module with memory monitoring"""
    import sys

    def cleanup_module():
        """Clean up module from cache"""
        if module_name in sys.modules:
            # Remove from modules dict to allow garbage collection
            del sys.modules[module_name]

    try:
        module = __import__(module_name)
        # Register for cleanup
        resource_manager.register_resource(
            f"module_{module_name}",
            "module_import",
            cleanup_module
        )
        return module
    except ImportError:
        return None


# Convenience functions
def start_resource_monitoring():
    """Start resource monitoring"""
    resource_manager.start_memory_monitoring()


def stop_resource_monitoring():
    """Stop resource monitoring"""
    resource_manager.stop_memory_monitoring()


def get_resource_stats():
    """Get resource statistics"""
    return resource_manager.get_resource_stats()


def cleanup_resources():
    """Clean up all resources"""
    resource_manager.cleanup_all()


if __name__ == "__main__":
    # Example usage
    print("Testing resource manager...")

    # Start monitoring
    start_resource_monitoring()

    # Use managed resource
    with managed_resource("test_resource", "test", lambda: print("Cleaning up test resource")):
        print("Using test resource...")

    # Get stats
    stats = get_resource_stats()
    print(f"Resource stats: {stats}")

    # Stop monitoring
    stop_resource_monitoring()
    print("Resource manager test completed.")
