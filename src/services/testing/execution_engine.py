"""
Test Execution Engine
=====================

Unified test execution engine for V2 services.
Consolidates test execution from integration framework.
Target: ≤300 LOC for V2 standards compliance.
"""

import os
import sys
import json
import time
import logging
import threading
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Callable, Coroutine, Type
from pathlib import Path
from datetime import datetime, timedelta
import traceback
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExecutionStatus(Enum):
    """Test execution status values."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class ExecutionMode(Enum):
    """Test execution modes."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    DISTRIBUTED = "distributed"


@dataclass
class TestExecutionConfig:
    """Configuration for test execution."""
    execution_mode: ExecutionMode = ExecutionMode.SEQUENTIAL
    max_workers: int = 4
    timeout: float = 300.0  # seconds
    retry_count: int = 3
    retry_delay: float = 2.0  # seconds
    enable_logging: bool = True
    log_level: str = "INFO"
    enable_metrics: bool = True
    enable_reporting: bool = True


@dataclass
class TestExecutionResult:
    """Result of test execution."""
    execution_id: str
    test_name: str
    status: ExecutionStatus
    start_time: float
    end_time: float
    duration: float
    worker_id: Optional[int] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    metrics: Dict[str, Any] = field(default_factory=dict)


class TestScheduler:
    """Schedules test execution."""
    
    def __init__(self, config: TestExecutionConfig):
        self.config = config
        self.test_queue: List[Callable] = []
        self.execution_history: List[TestExecutionResult] = []
        self._lock = threading.Lock()
    
    def add_test(self, test_function: Callable) -> bool:
        """Add a test to the execution queue."""
        try:
            with self._lock:
                self.test_queue.append(test_function)
                logger.info(f"Added test to queue: {test_function.__name__}")
                return True
        except Exception as e:
            logger.error(f"Failed to add test: {e}")
            return False
    
    def add_tests(self, test_functions: List[Callable]) -> bool:
        """Add multiple tests to the execution queue."""
        try:
            with self._lock:
                self.test_queue.extend(test_functions)
                logger.info(f"Added {len(test_functions)} tests to queue")
                return True
        except Exception as e:
            logger.error(f"Failed to add tests: {e}")
            return False
    
    def get_next_test(self) -> Optional[Callable]:
        """Get the next test from the queue."""
        with self._lock:
            if self.test_queue:
                return self.test_queue.pop(0)
            return None
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status."""
        with self._lock:
            return {
                "queue_length": len(self.test_queue),
                "executed_tests": len(self.execution_history),
                "pending_tests": len(self.test_queue)
            }
    
    def clear_queue(self):
        """Clear the test queue."""
        with self._lock:
            self.test_queue.clear()
            logger.info("Test queue cleared")
    
    def add_execution_result(self, result: TestExecutionResult):
        """Add execution result to history."""
        with self._lock:
            self.execution_history.append(result)


class ResultCollector:
    """Collects and manages test execution results."""
    
    def __init__(self):
        self.results: List[TestExecutionResult] = []
        self._lock = threading.Lock()
    
    def add_result(self, result: TestExecutionResult):
        """Add a test execution result."""
        with self._lock:
            self.results.append(result)
    
    def get_results_by_status(self, status: ExecutionStatus) -> List[TestExecutionResult]:
        """Get results by execution status."""
        with self._lock:
            return [r for r in self.results if r.status == status]
    
    def get_all_results(self) -> List[TestExecutionResult]:
        """Get all execution results."""
        with self._lock:
            return list(self.results)
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of execution results."""
        with self._lock:
            if not self.results:
                return {"error": "No execution results available"}
            
            total_tests = len(self.results)
            completed_tests = len([r for r in self.results if r.status == ExecutionStatus.COMPLETED])
            failed_tests = len([r for r in self.results if r.status == ExecutionStatus.FAILED])
            timeout_tests = len([r for r in self.results if r.status == ExecutionStatus.TIMEOUT])
            cancelled_tests = len([r for r in self.results if r.status == ExecutionStatus.CANCELLED])
            
            total_duration = sum(r.duration for r in self.results)
            avg_duration = total_duration / total_tests if total_tests > 0 else 0
            
            return {
                "total_tests": total_tests,
                "completed": completed_tests,
                "failed": failed_tests,
                "timeout": timeout_tests,
                "cancelled": cancelled_tests,
                "success_rate": (completed_tests / total_tests * 100) if total_tests > 0 else 0,
                "total_duration": total_duration,
                "average_duration": avg_duration
            }
    
    def clear_results(self):
        """Clear all execution results."""
        with self._lock:
            self.results.clear()
    
    def export_results(self, file_path: str) -> bool:
        """Export results to JSON file."""
        try:
            results_data = [result.__dict__ for result in self.results]
            with open(file_path, 'w') as f:
                json.dump(results_data, f, default=str, indent=2)
            logger.info(f"Results exported to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export results: {e}")
            return False


class TestOrchestrator:
    """Orchestrates test execution."""
    
    def __init__(self, config: TestExecutionConfig):
        self.config = config
        self.scheduler = TestScheduler(config)
        self.result_collector = ResultCollector()
        self.is_running = False
        self.workers: List[threading.Thread] = []
        self._lock = threading.Lock()
    
    def start_execution(self) -> bool:
        """Start test execution."""
        try:
            with self._lock:
                if self.is_running:
                    logger.warning("Test execution already running")
                    return False
                
                self.is_running = True
                
                if self.config.execution_mode == ExecutionMode.SEQUENTIAL:
                    self._start_sequential_execution()
                elif self.config.execution_mode == ExecutionMode.PARALLEL:
                    self._start_parallel_execution()
                else:
                    logger.error(f"Unsupported execution mode: {self.config.execution_mode}")
                    self.is_running = False
                    return False
                
                logger.info(f"Test execution started in {self.config.execution_mode.value} mode")
                return True
                
        except Exception as e:
            logger.error(f"Failed to start execution: {e}")
            self.is_running = False
            return False
    
    def stop_execution(self) -> bool:
        """Stop test execution."""
        try:
            with self._lock:
                if not self.is_running:
                    return True
                
                self.is_running = False
                
                # Wait for workers to complete
                for worker in self.workers:
                    worker.join(timeout=5.0)
                
                self.workers.clear()
                logger.info("Test execution stopped")
                return True
                
        except Exception as e:
            logger.error(f"Failed to stop execution: {e}")
            return False
    
    def _start_sequential_execution(self):
        """Start sequential test execution."""
        execution_thread = threading.Thread(target=self._sequential_execution_worker)
        execution_thread.daemon = True
        execution_thread.start()
        self.workers.append(execution_thread)
    
    def _start_parallel_execution(self):
        """Start parallel test execution."""
        for i in range(self.config.max_workers):
            worker = threading.Thread(target=self._parallel_execution_worker, args=(i,))
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
    
    def _sequential_execution_worker(self):
        """Worker for sequential execution."""
        while self.is_running:
            test_function = self.scheduler.get_next_test()
            if not test_function:
                break
            
            self._execute_single_test(test_function, 0)
        
        self.is_running = False
    
    def _parallel_execution_worker(self, worker_id: int):
        """Worker for parallel execution."""
        while self.is_running:
            test_function = self.scheduler.get_next_test()
            if not test_function:
                time.sleep(0.1)  # Small delay to prevent busy waiting
                continue
            
            self._execute_single_test(test_function, worker_id)
    
    def _execute_single_test(self, test_function: Callable, worker_id: int):
        """Execute a single test."""
        execution_id = f"exec_{int(time.time())}_{worker_id}"
        start_time = time.time()
        
        try:
            # Create execution result
            result = TestExecutionResult(
                execution_id=execution_id,
                test_name=test_function.__name__,
                status=ExecutionStatus.RUNNING,
                start_time=start_time,
                end_time=0,
                duration=0,
                worker_id=worker_id
            )
            
            # Execute test with timeout
            test_result = self._execute_with_timeout(test_function)
            
            # Update result
            end_time = time.time()
            result.end_time = end_time
            result.duration = end_time - start_time
            
            if test_result["success"]:
                result.status = ExecutionStatus.COMPLETED
                result.metrics = test_result.get("metrics", {})
                logger.info(f"Test completed: {test_function.__name__} (Worker {worker_id})")
            else:
                result.status = ExecutionStatus.FAILED
                result.error_message = test_result.get("error", "Unknown error")
                logger.error(f"Test failed: {test_function.__name__} (Worker {worker_id})")
            
        except Exception as e:
            end_time = time.time()
            result.end_time = end_time
            result.duration = end_time - start_time
            result.status = ExecutionStatus.FAILED
            result.error_message = str(e)
            logger.error(f"Test execution error: {test_function.__name__} (Worker {worker_id}) - {e}")
        
        # Add result to collector
        self.result_collector.add_result(result)
        self.scheduler.add_execution_result(result)
    
    def _execute_with_timeout(self, test_function: Callable) -> Dict[str, Any]:
        """Execute test function with timeout."""
        try:
            # Simple timeout implementation
            start_time = time.time()
            result = test_function()
            
            execution_time = time.time() - start_time
            if execution_time > self.config.timeout:
                return {
                    "success": False,
                    "error": f"Test execution timeout after {execution_time:.2f}s",
                    "metrics": {"execution_time": execution_time}
                }
            
            return {
                "success": True,
                "result": result,
                "metrics": {"execution_time": execution_time}
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metrics": {}
            }
    
    def get_execution_status(self) -> Dict[str, Any]:
        """Get current execution status."""
        queue_status = self.scheduler.get_queue_status()
        execution_summary = self.result_collector.get_execution_summary()
        
        return {
            "is_running": self.is_running,
            "execution_mode": self.config.execution_mode.value,
            "active_workers": len(self.workers),
            "queue_status": queue_status,
            "execution_summary": execution_summary
        }


class TestExecutor:
    """Main test execution class."""
    
    def __init__(self, config: Optional[TestExecutionConfig] = None):
        self.config = config or TestExecutionConfig()
        self.orchestrator = TestOrchestrator(self.config)
    
    def add_test(self, test_function: Callable) -> bool:
        """Add a test to the execution queue."""
        return self.orchestrator.scheduler.add_test(test_function)
    
    def add_tests(self, test_functions: List[Callable]) -> bool:
        """Add multiple tests to the execution queue."""
        return self.orchestrator.scheduler.add_tests(test_functions)
    
    def start_execution(self) -> bool:
        """Start test execution."""
        return self.orchestrator.start_execution()
    
    def stop_execution(self) -> bool:
        """Stop test execution."""
        return self.orchestrator.stop_execution()
    
    def get_status(self) -> Dict[str, Any]:
        """Get execution status."""
        return self.orchestrator.get_execution_status()
    
    def get_results(self) -> List[TestExecutionResult]:
        """Get execution results."""
        return self.result_collector.get_all_results()
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get results summary."""
        return self.result_collector.get_execution_summary()
    
    def export_results(self, file_path: str) -> bool:
        """Export results to file."""
        return self.result_collector.export_results(file_path)
    
    def clear_results(self):
        """Clear all results."""
        self.result_collector.clear_results()
    
    def clear_queue(self):
        """Clear test queue."""
        self.orchestrator.scheduler.clear_queue()
