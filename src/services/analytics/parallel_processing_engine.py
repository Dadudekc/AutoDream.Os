"""
Parallel Processing Engine - V2 Compliant
==========================================

Parallel processing engine for business intelligence optimization.
V2 COMPLIANT: Under 400 lines, single responsibility.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
import threading
import time
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ProcessingTask:
    """Processing task definition."""

    task_id: str
    function: Callable
    args: tuple
    kwargs: dict
    priority: int = 0
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class ProcessingResult:
    """Processing result."""

    task_id: str
    result: Any
    error: Exception | None
    execution_time: float
    completed_at: datetime


class ParallelProcessingEngine:
    """Parallel processing engine with load balancing."""

    def __init__(self, max_workers: int = 4, use_processes: bool = False):
        self.max_workers = max_workers
        self.use_processes = use_processes
        self.executor_class = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
        self.executor = None
        self.task_queue = []
        self.completed_tasks = []
        self.running_tasks = {}
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "total_execution_time": 0.0,
        }
        self.lock = threading.RLock()

    def start(self) -> None:
        """Start the processing engine."""
        if self.executor is None:
            self.executor = self.executor_class(max_workers=self.max_workers)
            logger.info(f"Parallel processing engine started with {self.max_workers} workers")

    def stop(self) -> None:
        """Stop the processing engine."""
        if self.executor:
            self.executor.shutdown(wait=True)
            self.executor = None
            logger.info("Parallel processing engine stopped")

    def submit_task(self, task: ProcessingTask) -> str:
        """Submit a task for processing."""
        with self.lock:
            self.task_queue.append(task)
            self.stats["total_tasks"] += 1
            logger.debug(f"Task submitted: {task.task_id}")
            return task.task_id

    def process_tasks(self, tasks: list[ProcessingTask]) -> list[ProcessingResult]:
        """Process multiple tasks in parallel."""
        if not self.executor:
            self.start()
        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)
        future_to_task = {}
        for task in sorted_tasks:
            future = self.executor.submit(self._execute_task, task)
            future_to_task[future] = task
        results = []
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                result = future.result()
                results.append(result)
                self.stats["completed_tasks"] += 1
            except Exception as e:
                error_result = ProcessingResult(
                    task_id=task.task_id,
                    result=None,
                    error=e,
                    execution_time=0.0,
                    completed_at=datetime.now(),
                )
                results.append(error_result)
                self.stats["failed_tasks"] += 1
                logger.error(f"Task {task.task_id} failed: {e}")
        return results

    def _execute_task(self, task: ProcessingTask) -> ProcessingResult:
        """Execute a single task."""
        start_time = time.time()
        try:
            result = task.function(*task.args, **task.kwargs)
            execution_time = time.time() - start_time
            return ProcessingResult(
                task_id=task.task_id,
                result=result,
                error=None,
                execution_time=execution_time,
                completed_at=datetime.now(),
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ProcessingResult(
                task_id=task.task_id,
                result=None,
                error=e,
                execution_time=execution_time,
                completed_at=datetime.now(),
            )

    def get_stats(self) -> dict[str, Any]:
        """Get processing engine statistics."""
        with self.lock:
            success_rate = 0.0
            if self.stats["total_tasks"] > 0:
                success_rate = self.stats["completed_tasks"] / self.stats["total_tasks"] * 100
            avg_execution_time = 0.0
            if self.stats["completed_tasks"] > 0:
                avg_execution_time = (
                    self.stats["total_execution_time"] / self.stats["completed_tasks"]
                )
            return {
                "max_workers": self.max_workers,
                "use_processes": self.use_processes,
                "total_tasks": self.stats["total_tasks"],
                "completed_tasks": self.stats["completed_tasks"],
                "failed_tasks": self.stats["failed_tasks"],
                "success_rate": round(success_rate, 2),
                "avg_execution_time": round(avg_execution_time, 3),
                "queue_size": len(self.task_queue),
                "running_tasks": len(self.running_tasks),
            }


class DataProcessingPipeline:
    """Data processing pipeline with parallel stages."""

    def __init__(self, processing_engine: ParallelProcessingEngine):
        self.engine = processing_engine
        self.stages = []
        self.pipeline_stats = {
            "total_pipelines": 0,
            "successful_pipelines": 0,
            "failed_pipelines": 0,
        }

    def add_stage(
        self,
        stage_name: str,
        processing_function: Callable,
        parallel: bool = True,
        priority: int = 0,
    ) -> None:
        """Add a processing stage to the pipeline."""
        stage = {
            "name": stage_name,
            "function": processing_function,
            "parallel": parallel,
            "priority": priority,
        }
        self.stages.append(stage)
        logger.debug(f"Added pipeline stage: {stage_name}")

    def process_data(self, data: list[Any], **kwargs) -> list[Any]:
        """Process data through the pipeline."""
        self.pipeline_stats["total_pipelines"] += 1
        current_data = data
        try:
            for stage in self.stages:
                if stage["parallel"]:
                    tasks = []
                    for i, item in enumerate(current_data):
                        task = ProcessingTask(
                            task_id=f"{stage['name']}_{i}",
                            function=stage["function"],
                            args=(item,),
                            kwargs=kwargs,
                            priority=stage["priority"],
                        )
                        tasks.append(task)
                    results = self.engine.process_tasks(tasks)
                    current_data = [r.result for r in results if r.error is None]
                else:
                    processed_data = []
                    for item in current_data:
                        try:
                            result = stage["function"](item, **kwargs)
                            processed_data.append(result)
                        except Exception as e:
                            logger.error(f"Stage {stage['name']} failed: {e}")
                    current_data = processed_data
            self.pipeline_stats["successful_pipelines"] += 1
            return current_data
        except Exception as e:
            self.pipeline_stats["failed_pipelines"] += 1
            logger.error(f"Pipeline processing failed: {e}")
            return []

    def get_pipeline_stats(self) -> dict[str, Any]:
        """Get pipeline statistics."""
        success_rate = 0.0
        if self.pipeline_stats["total_pipelines"] > 0:
            success_rate = (
                self.pipeline_stats["successful_pipelines"]
                / self.pipeline_stats["total_pipelines"]
                * 100
            )
        return {
            "stages_count": len(self.stages),
            "total_pipelines": self.pipeline_stats["total_pipelines"],
            "successful_pipelines": self.pipeline_stats["successful_pipelines"],
            "failed_pipelines": self.pipeline_stats["failed_pipelines"],
            "success_rate": round(success_rate, 2),
        }


class LoadBalancer:
    """Load balancer for parallel processing."""

    def __init__(self, processing_engines: list[ParallelProcessingEngine]):
        self.engines = processing_engines
        self.current_engine = 0
        self.engine_stats = dict.fromkeys(range(len(engines)), 0)
        self.lock = threading.RLock()

    def get_engine(self) -> ParallelProcessingEngine:
        """Get the next available engine using round-robin."""
        with self.lock:
            engine = self.engines[self.current_engine]
            self.engine_stats[self.current_engine] += 1
            self.current_engine = (self.current_engine + 1) % len(self.engines)
            return engine

    def get_least_loaded_engine(self) -> ParallelProcessingEngine:
        """Get the least loaded engine."""
        with self.lock:
            least_loaded = min(self.engines, key=lambda e: len(e.task_queue))
            return least_loaded

    def get_balance_stats(self) -> dict[str, Any]:
        """Get load balancing statistics."""
        with self.lock:
            return {
                "total_engines": len(self.engines),
                "engine_stats": dict(self.engine_stats),
                "current_engine": self.current_engine,
            }


_global_processing_engine = None


def get_parallel_processing_engine() -> ParallelProcessingEngine:
    """Get global parallel processing engine."""
    global _global_processing_engine
    if _global_processing_engine is None:
        _global_processing_engine = ParallelProcessingEngine()
    return _global_processing_engine


def get_data_processing_pipeline() -> DataProcessingPipeline:
    """Get global data processing pipeline."""
    engine = get_parallel_processing_engine()
    return DataProcessingPipeline(engine)


if __name__ == "__main__":
    engine = get_parallel_processing_engine()
    pipeline = get_data_processing_pipeline()

    def stage1(data):
        return f"processed_{data}"

    def stage2(data):
        return f"enhanced_{data}"

    pipeline.add_stage("stage1", stage1, parallel=True, priority=1)
    pipeline.add_stage("stage2", stage2, parallel=True, priority=2)
    test_data = ["item1", "item2", "item3", "item4"]
    results = pipeline.process_data(test_data)
    logger.info(f"Pipeline results: {results}")
    logger.info(f"Engine stats: {engine.get_stats()}")
    logger.info(f"Pipeline stats: {pipeline.get_pipeline_stats()}")
