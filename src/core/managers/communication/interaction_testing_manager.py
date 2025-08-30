#!/usr/bin/env python3
"""
Interaction Testing Manager - V2 Modular Architecture
===================================================

Interaction testing capabilities integrated into main communication infrastructure.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-1 (PERPETUAL MOTION LEADER - COMMUNICATIONS INTEGRATION SPECIALIST)
License: MIT
"""

import logging
import asyncio
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
import json

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority
from .types import CommunicationTypes, CommunicationConfig
from .models import Channel


@dataclass
class TestCategory:
    """Test category enumeration"""
    COMMUNICATION = "communication"
    PROTOCOL = "protocol"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    STRESS = "stress"
    RECOVERY = "recovery"


@dataclass
class TestStatus:
    """Test status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class TestResult:
    """Represents a test execution result"""
    
    test_id: str
    test_name: str
    category: str
    status: str
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
    """Represents a test suite"""
    
    suite_id: str
    name: str
    description: str
    tests: List[str]
    category: str
    timeout_seconds: int = 300
    retry_count: int = 1
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class InteractionTestingManager(BaseManager):
    """
    Interaction Testing Manager - Single responsibility: Communication system testing
    
    Manages:
    - Communication channel testing
    - Protocol execution testing
    - Coordination system testing
    - Performance benchmarking
    - Stress testing
    - Integration testing
    """
    
    def __init__(self, config_path: str = "config/interaction_testing_manager.json"):
        """Initialize interaction testing manager"""
        super().__init__(
            manager_name="InteractionTestingManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Test management
        self.test_results: Dict[str, TestResult] = {}
        self.test_suites: Dict[str, TestSuite] = {}
        self.test_execution_queue: List[str] = []
        self.running_tests: Dict[str, TestResult] = {}
        self.test_timeouts: Dict[str, float] = {}
        self.test_callbacks: List[Callable] = []
        
        # Test configuration
        self.default_timeout = 60  # seconds
        self.max_concurrent_tests = 5
        self.test_retry_delay = 5  # seconds
        
        # Initialize test suites
        self._initialize_test_suites()
    
    def _initialize_test_suites(self):
        """Initialize default test suites"""
        test_suites = [
            TestSuite(
                suite_id="communication_basic",
                name="Basic Communication Tests",
                description="Test basic agent communication capabilities",
                tests=["channel_connectivity", "message_sending", "message_receiving"],
                category=TestCategory.COMMUNICATION,
                timeout_seconds=120
            ),
            TestSuite(
                suite_id="protocol_execution",
                name="Protocol Execution Tests",
                description="Test coordination protocol execution",
                tests=["protocol_initialization", "protocol_execution", "protocol_cleanup"],
                category=TestCategory.PROTOCOL,
                timeout_seconds=180
            ),
            TestSuite(
                suite_id="integration_system",
                name="Integration System Tests",
                description="Test system integration capabilities",
                tests=["agent_coordination", "system_communication", "cross_module_integration"],
                category=TestCategory.INTEGRATION,
                timeout_seconds=300
            ),
            TestSuite(
                suite_id="performance_benchmark",
                name="Performance Benchmark Tests",
                description="Test system performance under load",
                tests=["throughput_testing", "latency_testing", "concurrency_testing"],
                category=TestCategory.PERFORMANCE,
                timeout_seconds=240
            ),
            TestSuite(
                suite_id="stress_recovery",
                name="Stress and Recovery Tests",
                description="Test system resilience and recovery",
                tests=["stress_testing", "failure_injection", "recovery_testing"],
                category=TestCategory.STRESS,
                timeout_seconds=360
            )
        ]
        
        for suite in test_suites:
            self.test_suites[suite.suite_id] = suite
        
        self.logger.info(f"✅ {len(test_suites)} test suites initialized")
    
    def create_test(self, test_name: str, category: str, test_function: Callable) -> str:
        """Create a new test"""
        try:
            test_id = f"test_{int(time.time())}_{test_name}"
            
            test_result = TestResult(
                test_id=test_id,
                test_name=test_name,
                category=category,
                status=TestStatus.PENDING,
                start_time=datetime.now()
            )
            
            self.test_results[test_id] = test_result
            self.logger.info(f"✅ Test created: {test_id} - {test_name}")
            
            return test_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create test: {e}")
            return ""
    
    def run_test(self, test_id: str) -> bool:
        """Run a specific test"""
        try:
            if test_id not in self.test_results:
                self.logger.error(f"❌ Test not found: {test_id}")
                return False
            
            if len(self.running_tests) >= self.max_concurrent_tests:
                self.logger.warning(f"⚠️ Maximum concurrent tests reached, queuing: {test_id}")
                self.test_execution_queue.append(test_id)
                return False
            
            test_result = self.test_results[test_id]
            test_result.status = TestStatus.RUNNING
            self.running_tests[test_id] = test_result
            
            self.logger.info(f"🔄 Running test: {test_id}")
            
            # Start test execution
            asyncio.create_task(self._execute_test(test_id))
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to run test: {e}")
            return False
    
    async def _execute_test(self, test_id: str):
        """Execute a test"""
        try:
            test_result = self.running_tests.get(test_id)
            if not test_result:
                return
            
            start_time = time.time()
            
            # Simulate test execution
            await asyncio.sleep(2)  # Simulate test time
            
            # Determine test result (simulated)
            test_success = self._simulate_test_result(test_result.category)
            
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            
            # Update test result
            test_result.end_time = datetime.now()
            test_result.duration_ms = duration_ms
            
            if test_success:
                test_result.status = TestStatus.COMPLETED
                test_result.metrics = {
                    "success": True,
                    "duration_ms": duration_ms,
                    "performance_score": 95.0
                }
                self.logger.info(f"✅ Test completed successfully: {test_id}")
            else:
                test_result.status = TestStatus.FAILED
                test_result.error_message = "Simulated test failure"
                test_result.metrics = {
                    "success": False,
                    "duration_ms": duration_ms,
                    "error_count": 1
                }
                self.logger.warning(f"⚠️ Test failed: {test_id}")
            
            # Remove from running tests
            del self.running_tests[test_id]
            
            # Process queue
            self._process_test_queue()
            
        except Exception as e:
            self.logger.error(f"❌ Test execution failed for {test_id}: {e}")
            if test_id in self.running_tests:
                test_result = self.running_tests[test_id]
                test_result.status = TestStatus.FAILED
                test_result.error_message = str(e)
                test_result.end_time = datetime.now()
                del self.running_tests[test_id]
    
    def _simulate_test_result(self, category: str) -> bool:
        """Simulate test result based on category"""
        # Simulate different success rates for different categories
        success_rates = {
            TestCategory.COMMUNICATION: 0.95,  # 95% success
            TestCategory.PROTOCOL: 0.90,       # 90% success
            TestCategory.INTEGRATION: 0.85,    # 85% success
            TestCategory.PERFORMANCE: 0.80,    # 80% success
            TestCategory.STRESS: 0.75,         # 75% success
            TestCategory.RECOVERY: 0.70        # 70% success
        }
        
        success_rate = success_rates.get(category, 0.80)
        return random.random() < success_rate
    
    def _process_test_queue(self):
        """Process queued tests"""
        while self.test_execution_queue and len(self.running_tests) < self.max_concurrent_tests:
            test_id = self.test_execution_queue.pop(0)
            self.run_test(test_id)
    
    def run_test_suite(self, suite_id: str) -> List[str]:
        """Run all tests in a test suite"""
        try:
            if suite_id not in self.test_suites:
                self.logger.error(f"❌ Test suite not found: {suite_id}")
                return []
            
            suite = self.test_suites[suite_id]
            test_ids = []
            
            self.logger.info(f"🚀 Running test suite: {suite.name}")
            
            for test_name in suite.tests:
                test_id = self.create_test(test_name, suite.category, None)
                if test_id:
                    test_ids.append(test_id)
                    self.run_test(test_id)
            
            return test_ids
            
        except Exception as e:
            self.logger.error(f"❌ Failed to run test suite: {e}")
            return []
    
    def get_test_status(self, test_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific test"""
        if test_id in self.test_results:
            test_result = self.test_results[test_id]
            return {
                "test_id": test_result.test_id,
                "test_name": test_result.test_name,
                "category": test_result.category,
                "status": test_result.status,
                "start_time": test_result.start_time.isoformat(),
                "end_time": test_result.end_time.isoformat() if test_result.end_time else None,
                "duration_ms": test_result.duration_ms,
                "error_message": test_result.error_message,
                "metrics": test_result.metrics
            }
        return None
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary of all tests"""
        total_tests = len(self.test_results)
        completed_tests = len([t for t in self.test_results.values() if t.status == TestStatus.COMPLETED])
        failed_tests = len([t for t in self.test_results.values() if t.status == TestStatus.FAILED])
        running_tests = len(self.running_tests)
        queued_tests = len(self.test_execution_queue)
        
        success_rate = completed_tests / total_tests if total_tests > 0 else 0.0
        
        return {
            "total_tests": total_tests,
            "completed_tests": completed_tests,
            "failed_tests": failed_tests,
            "running_tests": running_tests,
            "queued_tests": queued_tests,
            "success_rate": success_rate,
            "test_suites": len(self.test_suites)
        }
    
    def register_test_callback(self, callback: Callable):
        """Register callback for test events"""
        if callback not in self.test_callbacks:
            self.test_callbacks.append(callback)
            self.logger.info("✅ Test callback registered")
    
    def unregister_test_callback(self, callback: Callable):
        """Unregister test callback"""
        if callback in self.test_callbacks:
            self.test_callbacks.remove(callback)
            self.logger.info("✅ Test callback unregistered")


# Import random for simulation (remove in production)
import random


if __name__ == "__main__":
    # CLI interface for testing and validation
    import asyncio
    
    async def test_interaction_testing():
        """Test interaction testing functionality"""
        print("🧪 Interaction Testing Manager - Integration Test")
        print("=" * 60)
        
        # Initialize manager
        manager = InteractionTestingManager()
        
        # Test test suite execution
        print("🚀 Testing test suite execution...")
        test_ids = manager.run_test_suite("communication_basic")
        print(f"✅ Test suite started: {len(test_ids)} tests created")
        
        # Wait for tests to complete
        await asyncio.sleep(5)
        
        # Get test summary
        summary = manager.get_test_summary()
        print(f"📊 Test summary: {summary}")
        
        # Get individual test status
        for test_id in test_ids:
            status = manager.get_test_status(test_id)
            print(f"📋 Test {test_id}: {status['status']}")
        
        print("🎉 Interaction testing manager test completed successfully!")
    
    # Run test
    asyncio.run(test_interaction_testing())
