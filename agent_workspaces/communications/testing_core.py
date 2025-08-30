#!/usr/bin/env python3
"""
Testing Core Module
==================

Core functionality for interaction system testing.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import random


class TestStatus(Enum):
    """Test execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class TestCategory(Enum):
    """Test categories."""
    COMMUNICATION = "communication"
    PROTOCOL = "protocol"
    COORDINATION = "coordination"
    PERFORMANCE = "performance"
    INTEGRATION = "integration"
    STRESS = "stress"


@dataclass
class TestResult:
    """Represents a test execution result."""
    test_id: str
    test_name: str
    category: TestCategory
    status: TestStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    error_message: str = ""
    details: Dict[str, Any] = None
    metrics: Dict[str, float] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}
        if self.metrics is None:
            self.metrics = {}


@dataclass
class TestSuite:
    """Represents a test suite."""
    suite_id: str
    name: str
    description: str
    tests: List[str]
    category: TestCategory
    timeout_seconds: int = 300
    retry_count: int = 1
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class TestingCore:
    """Core testing functionality for interaction systems"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.test_results: Dict[str, TestResult] = {}
        self.test_suites: Dict[str, TestSuite] = {}
        self.test_execution_queue: List[str] = []
        self.execution_lock = threading.Lock()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for testing operations"""
        logger = logging.getLogger("TestingCore")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[TESTING] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def register_test_suite(self, suite: TestSuite) -> bool:
        """Register a test suite for execution"""
        try:
            if suite.suite_id in self.test_suites:
                self.logger.warning(f"Test suite {suite.suite_id} already registered")
                return False
            
            self.test_suites[suite.suite_id] = suite
            self.logger.info(f"Registered test suite: {suite.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error registering test suite: {e}")
            return False
    
    def add_test_result(self, result: TestResult) -> None:
        """Add a test result to the collection"""
        try:
            with self.execution_lock:
                self.test_results[result.test_id] = result
                
        except Exception as e:
            self.logger.error(f"Error adding test result: {e}")
    
    def get_test_result(self, test_id: str) -> Optional[TestResult]:
        """Get a test result by ID"""
        return self.test_results.get(test_id)
    
    def get_test_suite(self, suite_id: str) -> Optional[TestSuite]:
        """Get a test suite by ID"""
        return self.test_suites.get(suite_id)
    
    def calculate_test_metrics(self, test_id: str) -> Dict[str, float]:
        """Calculate metrics for a specific test"""
        try:
            result = self.get_test_result(test_id)
            if not result:
                return {}
            
            metrics = {
                "duration_seconds": result.duration_ms / 1000.0 if result.duration_ms else 0.0,
                "status_score": self._calculate_status_score(result.status),
                "error_count": 1 if result.error_message else 0
            }
            
            # Add custom metrics if available
            if result.metrics:
                metrics.update(result.metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating test metrics: {e}")
            return {}
    
    def _calculate_status_score(self, status: TestStatus) -> float:
        """Calculate numerical score for test status"""
        status_scores = {
            TestStatus.PASSED: 1.0,
            TestStatus.SKIPPED: 0.5,
            TestStatus.FAILED: 0.0,
            TestStatus.TIMEOUT: 0.0,
            TestStatus.PENDING: 0.0,
            TestStatus.RUNNING: 0.0
        }
        return status_scores.get(status, 0.0)
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of all test results"""
        try:
            total_tests = len(self.test_results)
            if total_tests == 0:
                return {
                    "total_tests": 0,
                    "passed": 0,
                    "failed": 0,
                    "skipped": 0,
                    "success_rate": 0.0,
                    "average_duration": 0.0
                }
            
            passed = sum(1 for r in self.test_results.values() if r.status == TestStatus.PASSED)
            failed = sum(1 for r in self.test_results.values() if r.status == TestStatus.FAILED)
            skipped = sum(1 for r in self.test_results.values() if r.status == TestStatus.SKIPPED)
            
            success_rate = passed / total_tests if total_tests > 0 else 0.0
            
            # Calculate average duration
            durations = [r.duration_ms for r in self.test_results.values() if r.duration_ms is not None]
            average_duration = sum(durations) / len(durations) if durations else 0.0
            
            return {
                "total_tests": total_tests,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "success_rate": success_rate,
                "average_duration_ms": average_duration,
                "average_duration_seconds": average_duration / 1000.0
            }
            
        except Exception as e:
            self.logger.error(f"Error getting test summary: {e}")
            return {"error": str(e)}
    
    def get_tests_by_category(self, category: TestCategory) -> List[TestResult]:
        """Get all test results for a specific category"""
        try:
            return [r for r in self.test_results.values() if r.category == category]
        except Exception as e:
            self.logger.error(f"Error getting tests by category: {e}")
            return []
    
    def get_tests_by_status(self, status: TestStatus) -> List[TestResult]:
        """Get all test results for a specific status"""
        try:
            return [r for r in self.test_results.values() if r.status == status]
        except Exception as e:
            self.logger.error(f"Error getting tests by status: {e}")
            return []
    
    def clear_test_results(self) -> None:
        """Clear all test results"""
        try:
            with self.execution_lock:
                self.test_results.clear()
            self.logger.info("All test results cleared")
            
        except Exception as e:
            self.logger.error(f"Error clearing test results: {e}")
    
    def export_test_results(self, filepath: str) -> bool:
        """Export test results to JSON file"""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "test_summary": self.get_test_summary(),
                "test_results": [asdict(r) for r in self.test_results.values()],
                "test_suites": [asdict(s) for s in self.test_suites.values()]
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            self.logger.info(f"Test results exported to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting test results: {e}")
            return False
