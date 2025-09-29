#!/usr/bin/env python3
"""
Workflow Performance Optimization
=================================

Performance optimization utilities for the workflow system.
V2 Compliance: ≤400 lines, focused optimization functionality.
"""

import asyncio
import logging
import threading
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import psutil

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Performance metrics for workflow execution."""

    execution_time: float
    memory_usage: float
    cpu_usage: float
    steps_completed: int
    steps_failed: int
    parallel_executions: int
    cache_hits: int
    cache_misses: int

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "execution_time": self.execution_time,
            "memory_usage": self.memory_usage,
            "cpu_usage": self.cpu_usage,
            "steps_completed": self.steps_completed,
            "steps_failed": self.steps_failed,
            "parallel_executions": self.parallel_executions,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "success_rate": self.steps_completed / (self.steps_completed + self.steps_failed)
            if (self.steps_completed + self.steps_failed) > 0
            else 0,
        }


class PerformanceMonitor:
    """Monitors workflow performance metrics."""

    def __init__(self):
        self.metrics_history: list[PerformanceMetrics] = []
        self.current_metrics: PerformanceMetrics | None = None
        self.start_time: datetime | None = None
        self.process = psutil.Process()

    def start_monitoring(self):
        """Start performance monitoring."""
        self.start_time = datetime.now()
        self.current_metrics = PerformanceMetrics(
            execution_time=0.0,
            memory_usage=0.0,
            cpu_usage=0.0,
            steps_completed=0,
            steps_failed=0,
            parallel_executions=0,
            cache_hits=0,
            cache_misses=0,
        )
        logger.debug("Performance monitoring started")

    def stop_monitoring(self) -> PerformanceMetrics:
        """Stop monitoring and return final metrics."""
        if not self.start_time or not self.current_metrics:
            raise ValueError("Monitoring not started")

        execution_time = (datetime.now() - self.start_time).total_seconds()
        self.current_metrics.execution_time = execution_time

        # Get final system metrics
        self.current_metrics.memory_usage = self.process.memory_info().rss / 1024 / 1024  # MB
        self.current_metrics.cpu_usage = self.process.cpu_percent()

        # Store metrics
        self.metrics_history.append(self.current_metrics)

        logger.info(f"Performance monitoring completed: {execution_time:.2f}s")
        return self.current_metrics

    def record_step_completion(self, success: bool):
        """Record step completion."""
        if self.current_metrics:
            if success:
                self.current_metrics.steps_completed += 1
            else:
                self.current_metrics.steps_failed += 1

    def record_parallel_execution(self):
        """Record parallel execution."""
        if self.current_metrics:
            self.current_metrics.parallel_executions += 1

    def record_cache_hit(self):
        """Record cache hit."""
        if self.current_metrics:
            self.current_metrics.cache_hits += 1

    def record_cache_miss(self):
        """Record cache miss."""
        if self.current_metrics:
            self.current_metrics.cache_misses += 1

    def get_average_metrics(self) -> dict[str, float] | None:
        """Get average metrics across all executions."""
        if not self.metrics_history:
            return None

        total_executions = len(self.metrics_history)

        return {
            "average_execution_time": sum(m.execution_time for m in self.metrics_history)
            / total_executions,
            "average_memory_usage": sum(m.memory_usage for m in self.metrics_history)
            / total_executions,
            "average_cpu_usage": sum(m.cpu_usage for m in self.metrics_history) / total_executions,
            "average_success_rate": sum(
                m.steps_completed / (m.steps_completed + m.steps_failed)
                for m in self.metrics_history
                if (m.steps_completed + m.steps_failed) > 0
            )
            / total_executions,
            "total_executions": total_executions,
        }


class WorkflowCache:
    """Caching system for workflow optimization."""

    def __init__(self, max_size: int = 1000):
        self.cache: dict[str, Any] = {}
        self.max_size = max_size
        self.access_times: dict[str, datetime] = {}
        self.hit_count = 0
        self.miss_count = 0
        self.lock = threading.RLock()

    def get(self, key: str) -> Any | None:
        """Get value from cache."""
        with self.lock:
            if key in self.cache:
                self.access_times[key] = datetime.now()
                self.hit_count += 1
                logger.debug(f"Cache hit for key: {key}")
                return self.cache[key]

            self.miss_count += 1
            logger.debug(f"Cache miss for key: {key}")
            return None

    def set(self, key: str, value: Any):
        """Set value in cache."""
        with self.lock:
            # Evict oldest entries if cache is full
            if len(self.cache) >= self.max_size:
                self._evict_oldest()

            self.cache[key] = value
            self.access_times[key] = datetime.now()
            logger.debug(f"Cached value for key: {key}")

    def _evict_oldest(self):
        """Evict oldest cache entry."""
        if not self.access_times:
            return

        oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        del self.cache[oldest_key]
        del self.access_times[oldest_key]
        logger.debug(f"Evicted cache entry: {oldest_key}")

    def clear(self):
        """Clear cache."""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
            logger.info("Cache cleared")

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total_requests if total_requests > 0 else 0

        return {
            "cache_size": len(self.cache),
            "max_size": self.max_size,
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate,
            "total_requests": total_requests,
        }


class ParallelExecutor:
    """Parallel execution engine for workflow steps."""

    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or min(32, (psutil.cpu_count() or 1) + 4)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=self.max_workers)
        self.active_tasks: dict[str, Any] = {}
        self.lock = threading.RLock()

    async def execute_parallel(
        self, tasks: list[Callable], use_processes: bool = False
    ) -> list[Any]:
        """Execute tasks in parallel."""
        executor = self.process_pool if use_processes else self.thread_pool

        # Create tasks
        loop = asyncio.get_event_loop()
        futures = []

        for i, task in enumerate(tasks):
            future = loop.run_in_executor(executor, task)
            futures.append(future)

            with self.lock:
                self.active_tasks[f"task_{i}"] = future

        # Wait for completion
        try:
            results = await asyncio.gather(*futures, return_exceptions=True)

            # Clean up active tasks
            with self.lock:
                self.active_tasks.clear()

            return results
        except Exception as e:
            logger.error(f"Parallel execution error: {e}")
            raise

    def get_active_task_count(self) -> int:
        """Get number of active tasks."""
        with self.lock:
            return len(self.active_tasks)

    def shutdown(self):
        """Shutdown executor pools."""
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)
        logger.info("Parallel executor shutdown")


class WorkflowOptimizer:
    """Main workflow optimization engine."""

    def __init__(self):
        self.performance_monitor = PerformanceMonitor()
        self.cache = WorkflowCache()
        self.parallel_executor = ParallelExecutor()
        self.optimization_enabled = True

    def optimize_workflow_execution(
        self, workflow_steps: list[Any], execution_function: Callable
    ) -> dict[str, Any]:
        """Optimize workflow execution with caching and parallel processing."""
        if not self.optimization_enabled:
            return self._execute_sequential(workflow_steps, execution_function)

        # Start performance monitoring
        self.performance_monitor.start_monitoring()

        try:
            # Group steps by dependencies for parallel execution
            parallel_groups = self._group_parallel_steps(workflow_steps)

            results = {}
            for group in parallel_groups:
                group_results = self._execute_group_parallel(group, execution_function)
                results.update(group_results)

            # Stop monitoring and get metrics
            metrics = self.performance_monitor.stop_monitoring()

            return {
                "success": True,
                "results": results,
                "metrics": metrics.to_dict(),
                "optimization_applied": True,
            }

        except Exception as e:
            logger.error(f"Optimized execution failed: {e}")
            return {"success": False, "error": str(e), "optimization_applied": True}

    def _group_parallel_steps(self, steps: list[Any]) -> list[list[Any]]:
        """Group steps that can be executed in parallel."""
        # Simple implementation - group steps with same dependency level
        groups = []
        remaining_steps = steps.copy()

        while remaining_steps:
            # Find steps with no dependencies or all dependencies completed
            current_group = []
            for step in remaining_steps[:]:
                if not hasattr(step, "dependencies") or not step.dependencies:
                    current_group.append(step)
                    remaining_steps.remove(step)
                else:
                    # Check if all dependencies are completed
                    completed_deps = all(
                        dep in [s.step_id for s in current_group] for dep in step.dependencies
                    )
                    if completed_deps:
                        current_group.append(step)
                        remaining_steps.remove(step)

            if current_group:
                groups.append(current_group)
            else:
                # No more steps can be executed (circular dependency or error)
                break

        return groups

    def _execute_group_parallel(
        self, group: list[Any], execution_function: Callable
    ) -> dict[str, Any]:
        """Execute a group of steps in parallel."""
        if len(group) == 1:
            # Single step - execute directly
            step = group[0]
            result = execution_function(step)
            self.performance_monitor.record_step_completion(result.get("success", False))
            return {step.step_id: result}

        # Multiple steps - execute in parallel
        tasks = [lambda s=step: execution_function(s) for step in group]

        try:
            results = asyncio.run(self.parallel_executor.execute_parallel(tasks))

            group_results = {}
            for i, result in enumerate(results):
                step = group[i]
                group_results[step.step_id] = result
                self.performance_monitor.record_step_completion(result.get("success", False))
                self.performance_monitor.record_parallel_execution()

            return group_results

        except Exception as e:
            logger.error(f"Parallel group execution failed: {e}")
            # Fall back to sequential execution
            return self._execute_group_sequential(group, execution_function)

    def _execute_group_sequential(
        self, group: list[Any], execution_function: Callable
    ) -> dict[str, Any]:
        """Execute a group of steps sequentially."""
        results = {}
        for step in group:
            result = execution_function(step)
            results[step.step_id] = result
            self.performance_monitor.record_step_completion(result.get("success", False))

        return results

    def _execute_sequential(self, steps: list[Any], execution_function: Callable) -> dict[str, Any]:
        """Execute steps sequentially without optimization."""
        self.performance_monitor.start_monitoring()

        results = {}
        for step in steps:
            result = execution_function(step)
            results[step.step_id] = result
            self.performance_monitor.record_step_completion(result.get("success", False))

        metrics = self.performance_monitor.stop_monitoring()

        return {
            "success": True,
            "results": results,
            "metrics": metrics.to_dict(),
            "optimization_applied": False,
        }

    def get_optimization_stats(self) -> dict[str, Any]:
        """Get optimization statistics."""
        cache_stats = self.cache.get_stats()
        performance_stats = self.performance_monitor.get_average_metrics()

        return {
            "cache": cache_stats,
            "performance": performance_stats,
            "parallel_executor": {
                "max_workers": self.parallel_executor.max_workers,
                "active_tasks": self.parallel_executor.get_active_task_count(),
            },
            "optimization_enabled": self.optimization_enabled,
        }

    def enable_optimization(self):
        """Enable optimization features."""
        self.optimization_enabled = True
        logger.info("Workflow optimization enabled")

    def disable_optimization(self):
        """Disable optimization features."""
        self.optimization_enabled = False
        logger.info("Workflow optimization disabled")

    def clear_cache(self):
        """Clear optimization cache."""
        self.cache.clear()
        logger.info("Optimization cache cleared")

    def shutdown(self):
        """Shutdown optimization components."""
        self.parallel_executor.shutdown()
        logger.info("Workflow optimizer shutdown")
