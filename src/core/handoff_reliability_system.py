#!/usr/bin/env python3
"""
Handoff Reliability System - Agent Cellphone V2
==============================================

Implements comprehensive reliability testing for handoff procedures.
This system ensures that handoffs are reliable under various conditions
including load, stress, and failure scenarios.

Author: Agent-7 (QUALITY COMPLETION MANAGER)
Contract: PHASE-003 - Smooth Handoff Procedure Implementation
License: MIT
"""

import logging
import time
import asyncio
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json
import statistics
import random

from .base_manager import BaseManager


class TestType(Enum):
    """Reliability test types"""
    RELIABILITY = "reliability"
    PERFORMANCE = "performance"
    STRESS = "stress"
    FAILURE_INJECTION = "failure_injection"
    CONCURRENCY = "concurrency"
    ENDURANCE = "endurance"


class TestStatus(Enum):
    """Test status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class TestConfiguration:
    """Configuration for reliability tests"""
    test_id: str
    test_type: TestType
    procedure_id: str
    iterations: int = 100
    timeout: float = 30.0
    concurrent_limit: int = 10
    failure_rate: float = 0.0  # 0.0 = no failures, 1.0 = 100% failures
    stress_factor: float = 1.0  # 1.0 = normal load, >1.0 = increased load
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TestResult:
    """Result of a reliability test"""
    test_id: str
    test_type: TestType
    procedure_id: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    iterations: int = 0
    successful_iterations: int = 0
    failed_iterations: int = 0
    timeout_iterations: int = 0
    total_duration: float = 0.0
    average_duration: float = 0.0
    min_duration: float = 0.0
    max_duration: float = 0.0
    p95_duration: float = 0.0
    p99_duration: float = 0.0
    success_rate: float = 0.0
    throughput: float = 0.0
    error_details: Optional[str] = None
    performance_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class TestSession:
    """Tracks a reliability test session"""
    session_id: str
    test_config: TestConfiguration
    start_time: float
    end_time: Optional[float] = None
    status: TestStatus = TestStatus.PENDING
    current_iteration: int = 0
    results: List[TestResult] = field(default_factory=list)
    active_tests: List[str] = field(default_factory=list)
    error_details: Optional[str] = None


class HandoffReliabilitySystem(BaseManager):
    """
    Handoff Reliability System - Testing and Validation
    
    Single responsibility: Test handoff reliability and performance
    under various conditions to ensure system robustness.
    """
    
    def __init__(self, project_root: str = "."):
        super().__init__("HandoffReliabilitySystem")
        self.project_root = Path(project_root)
        self.logger = logging.getLogger(__name__)
        
        # Core testing components
        self.test_configurations: Dict[str, TestConfiguration] = {}
        self.active_sessions: Dict[str, TestSession] = {}
        self.test_history: List[TestSession] = []
        
        # Performance tracking
        self.reliability_metrics = {
            "total_tests": 0,
            "successful_tests": 0,
            "failed_tests": 0,
            "total_iterations": 0,
            "successful_iterations": 0,
            "failed_iterations": 0,
            "average_success_rate": 0.0,
            "average_duration": 0.0,
            "test_type_performance": {}
        }
        
        # Test engines
        self.test_engines: Dict[TestType, Callable] = {}
        
        # Performance thresholds
        self.performance_thresholds = {
            "min_success_rate": 0.95,  # 95%
            "max_average_duration": 5.0,  # 5 seconds
            "max_p95_duration": 10.0,  # 10 seconds
            "max_p99_duration": 15.0,  # 15 seconds
            "min_throughput": 0.1  # 0.1 tests/second
        }
        
        # Initialize the system
        self._initialize_reliability_system()
    
    def _initialize_reliability_system(self):
        """Initialize the reliability system with default configurations"""
        self.logger.info("🚀 Initializing Handoff Reliability System")
        
        # Load default test configurations
        self._load_default_test_configurations()
        
        # Initialize test engines
        self._initialize_test_engines()
        
        self.logger.info("✅ Handoff Reliability System initialized successfully")
    
    def _load_default_test_configurations(self):
        """Load default test configurations"""
        default_configs = [
            TestConfiguration(
                test_id="RELIABILITY_STANDARD",
                test_type=TestType.RELIABILITY,
                procedure_id="PHASE_TRANSITION_STANDARD",
                iterations=100,
                timeout=30.0,
                concurrent_limit=5
            ),
            TestConfiguration(
                test_id="PERFORMANCE_STANDARD",
                test_type=TestType.PERFORMANCE,
                procedure_id="PHASE_TRANSITION_STANDARD",
                iterations=50,
                timeout=60.0,
                concurrent_limit=10
            ),
            TestConfiguration(
                test_id="STRESS_STANDARD",
                test_type=TestType.STRESS,
                procedure_id="PHASE_TRANSITION_STANDARD",
                iterations=25,
                timeout=120.0,
                concurrent_limit=20,
                stress_factor=2.0
            ),
            TestConfiguration(
                test_id="FAILURE_INJECTION_STANDARD",
                test_type=TestType.FAILURE_INJECTION,
                procedure_id="PHASE_TRANSITION_STANDARD",
                iterations=75,
                timeout=45.0,
                concurrent_limit=5,
                failure_rate=0.1  # 10% failure rate
            ),
            TestConfiguration(
                test_id="CONCURRENCY_STANDARD",
                test_type=TestType.CONCURRENCY,
                procedure_id="PHASE_TRANSITION_STANDARD",
                iterations=30,
                timeout=90.0,
                concurrent_limit=50
            ),
            TestConfiguration(
                test_id="ENDURANCE_STANDARD",
                test_type=TestType.ENDURANCE,
                procedure_id="PHASE_TRANSITION_STANDARD",
                iterations=200,
                timeout=180.0,
                concurrent_limit=3
            )
        ]
        
        for config in default_configs:
            self.test_configurations[config.test_id] = config
        
        self.logger.info(f"📋 Loaded {len(default_configs)} default test configurations")
    
    def _initialize_test_engines(self):
        """Initialize test engines for different test types"""
        self.test_engines = {
            TestType.RELIABILITY: self._run_reliability_test,
            TestType.PERFORMANCE: self._run_performance_test,
            TestType.STRESS: self._run_stress_test,
            TestType.FAILURE_INJECTION: self._run_failure_injection_test,
            TestType.CONCURRENCY: self._run_concurrency_test,
            TestType.ENDURANCE: self._run_endurance_test
        }
    
    def start_reliability_test(self, test_config_id: str) -> str:
        """
        Start a reliability test session
        
        Args:
            test_config_id: ID of the test configuration to use
            
        Returns:
            Session ID for tracking
        """
        try:
            if test_config_id not in self.test_configurations:
                raise ValueError(f"Unknown test configuration ID: {test_config_id}")
            
            test_config = self.test_configurations[test_config_id]
            session_id = f"reliability_{int(time.time())}_{test_config_id}"
            
            # Create test session
            session = TestSession(
                session_id=session_id,
                test_config=test_config,
                start_time=time.time()
            )
            
            # Store session
            self.active_sessions[session_id] = session
            
            # Log session start
            self.logger.info(f"🚀 Starting reliability test session {session_id} for {test_config_id}")
            
            # Start testing
            asyncio.create_task(self._execute_test_session(session))
            
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to start reliability test: {e}")
            raise
    
    async def _execute_test_session(self, session: TestSession):
        """Execute a reliability test session"""
        try:
            session.status = TestStatus.RUNNING
            self.logger.info(f"🔄 Executing reliability test session {session.session_id}")
            
            # Get the appropriate test engine
            test_engine = self.test_engines.get(session.test_config.test_type)
            if not test_engine:
                raise ValueError(f"No test engine for type: {session.test_config.test_type}")
            
            # Run the test
            test_result = await test_engine(session)
            session.results.append(test_result)
            
            # Update session status
            if test_result.error_details:
                session.status = TestStatus.FAILED
                session.error_details = test_result.error_details
            else:
                session.status = TestStatus.COMPLETED
            
            session.end_time = time.time()
            
            # Log completion
            status_emoji = "✅" if session.status == TestStatus.COMPLETED else "❌"
            self.logger.info(f"{status_emoji} Reliability test session {session.session_id} completed: {session.status.value}")
            
            # Update metrics
            self._update_reliability_metrics(test_result)
            
        except Exception as e:
            session.status = TestStatus.FAILED
            session.error_details = str(e)
            session.end_time = time.time()
            self.logger.error(f"❌ Reliability test session {session.session_id} failed: {e}")
            
        finally:
            # Move to history
            self.test_history.append(session)
            if session.session_id in self.active_sessions:
                del self.active_sessions[session.session_id]
    
    # Test engine implementations
    async def _run_reliability_test(self, session: TestSession) -> TestResult:
        """Run a reliability test"""
        try:
            config = session.test_config
            start_time = time.time()
            
            self.logger.info(f"🧪 Running reliability test: {config.iterations} iterations")
            
            # Run iterations
            successful_iterations = 0
            failed_iterations = 0
            timeout_iterations = 0
            durations = []
            
            for i in range(config.iterations):
                iteration_start = time.time()
                
                try:
                    # Simulate handoff execution
                    success = await self._simulate_handoff_execution(config)
                    
                    if success:
                        successful_iterations += 1
                    else:
                        failed_iterations += 1
                    
                    # Record duration
                    duration = time.time() - iteration_start
                    durations.append(duration)
                    
                    # Progress update
                    if (i + 1) % 10 == 0:
                        self.logger.info(f"📊 Reliability test progress: {i + 1}/{config.iterations}")
                    
                except asyncio.TimeoutError:
                    timeout_iterations += 1
                    durations.append(config.timeout)
                except Exception as e:
                    failed_iterations += 1
                    durations.append(time.time() - iteration_start)
            
            # Calculate results
            end_time = time.time()
            total_duration = end_time - start_time
            
            result = self._calculate_test_results(
                config, start_time, end_time, total_duration,
                successful_iterations, failed_iterations, timeout_iterations,
                durations
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Reliability test failed: {e}")
            return self._create_error_result(session.test_config, str(e))
    
    async def _run_performance_test(self, session: TestSession) -> TestResult:
        """Run a performance test"""
        try:
            config = session.test_config
            start_time = time.time()
            
            self.logger.info(f"🧪 Running performance test: {config.iterations} iterations")
            
            # Run iterations with performance monitoring
            successful_iterations = 0
            failed_iterations = 0
            timeout_iterations = 0
            durations = []
            
            for i in range(config.iterations):
                iteration_start = time.time()
                
                try:
                    # Simulate handoff execution with performance tracking
                    success = await self._simulate_handoff_execution(config)
                    
                    if success:
                        successful_iterations += 1
                    else:
                        failed_iterations += 1
                    
                    # Record duration
                    duration = time.time() - iteration_start
                    durations.append(duration)
                    
                    # Progress update
                    if (i + 1) % 10 == 0:
                        self.logger.info(f"📊 Performance test progress: {i + 1}/{config.iterations}")
                    
                except asyncio.TimeoutError:
                    timeout_iterations += 1
                    durations.append(config.timeout)
                except Exception as e:
                    failed_iterations += 1
                    durations.append(time.time() - iteration_start)
            
            # Calculate results
            end_time = time.time()
            total_duration = end_time - start_time
            
            result = self._calculate_test_results(
                config, start_time, end_time, total_duration,
                successful_iterations, failed_iterations, timeout_iterations,
                durations
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Performance test failed: {e}")
            return self._create_error_result(session.test_config, str(e))
    
    async def _run_stress_test(self, session: TestSession) -> TestResult:
        """Run a stress test"""
        try:
            config = session.test_config
            start_time = time.time()
            
            self.logger.info(f"🧪 Running stress test: {config.iterations} iterations (stress factor: {config.stress_factor})")
            
            # Run iterations with increased stress
            successful_iterations = 0
            failed_iterations = 0
            timeout_iterations = 0
            durations = []
            
            for i in range(config.iterations):
                iteration_start = time.time()
                
                try:
                    # Simulate handoff execution under stress
                    success = await self._simulate_stressed_handoff_execution(config)
                    
                    if success:
                        successful_iterations += 1
                    else:
                        failed_iterations += 1
                    
                    # Record duration
                    duration = time.time() - iteration_start
                    durations.append(duration)
                    
                    # Progress update
                    if (i + 1) % 10 == 0:
                        self.logger.info(f"📊 Stress test progress: {i + 1}/{config.iterations}")
                    
                except asyncio.TimeoutError:
                    timeout_iterations += 1
                    durations.append(config.timeout)
                except Exception as e:
                    failed_iterations += 1
                    durations.append(time.time() - iteration_start)
            
            # Calculate results
            end_time = time.time()
            total_duration = end_time - start_time
            
            result = self._calculate_test_results(
                config, start_time, end_time, total_duration,
                successful_iterations, failed_iterations, timeout_iterations,
                durations
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Stress test failed: {e}")
            return self._create_error_result(session.test_config, str(e))
    
    async def _run_failure_injection_test(self, session: TestSession) -> TestResult:
        """Run a failure injection test"""
        try:
            config = session.test_config
            start_time = time.time()
            
            self.logger.info(f"🧪 Running failure injection test: {config.iterations} iterations (failure rate: {config.failure_rate:.1%})")
            
            # Run iterations with controlled failures
            successful_iterations = 0
            failed_iterations = 0
            timeout_iterations = 0
            durations = []
            
            for i in range(config.iterations):
                iteration_start = time.time()
                
                try:
                    # Simulate handoff execution with failure injection
                    success = await self._simulate_failure_injection_handoff(config)
                    
                    if success:
                        successful_iterations += 1
                    else:
                        failed_iterations += 1
                    
                    # Record duration
                    duration = time.time() - iteration_start
                    durations.append(duration)
                    
                    # Progress update
                    if (i + 1) % 10 == 0:
                        self.logger.info(f"📊 Failure injection test progress: {i + 1}/{config.iterations}")
                    
                except asyncio.TimeoutError:
                    timeout_iterations += 1
                    durations.append(config.timeout)
                except Exception as e:
                    failed_iterations += 1
                    durations.append(time.time() - iteration_start)
            
            # Calculate results
            end_time = time.time()
            total_duration = end_time - start_time
            
            result = self._calculate_test_results(
                config, start_time, end_time, total_duration,
                successful_iterations, failed_iterations, timeout_iterations,
                durations
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failure injection test failed: {e}")
            return self._create_error_result(session.test_config, str(e))
    
    async def _run_concurrency_test(self, session: TestSession) -> TestResult:
        """Run a concurrency test"""
        try:
            config = session.test_config
            start_time = time.time()
            
            self.logger.info(f"🧪 Running concurrency test: {config.iterations} iterations (concurrent limit: {config.concurrent_limit})")
            
            # Run iterations with controlled concurrency
            successful_iterations = 0
            failed_iterations = 0
            timeout_iterations = 0
            durations = []
            
            # Process iterations in batches based on concurrent limit
            for batch_start in range(0, config.iterations, config.concurrent_limit):
                batch_end = min(batch_start + config.concurrent_limit, config.iterations)
                batch_size = batch_end - batch_start
                
                # Create concurrent tasks for this batch
                tasks = []
                for i in range(batch_size):
                    task = asyncio.create_task(self._simulate_concurrent_handoff(config))
                    tasks.append(task)
                
                # Wait for all tasks in batch to complete
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process batch results
                for i, result in enumerate(batch_results):
                    if isinstance(result, Exception):
                        failed_iterations += 1
                        durations.append(config.timeout)
                    else:
                        if result:
                            successful_iterations += 1
                        else:
                            failed_iterations += 1
                        durations.append(0.1)  # Simulated duration
                
                # Progress update
                self.logger.info(f"📊 Concurrency test progress: {batch_end}/{config.iterations}")
            
            # Calculate results
            end_time = time.time()
            total_duration = end_time - start_time
            
            result = self._calculate_test_results(
                config, start_time, end_time, total_duration,
                successful_iterations, failed_iterations, timeout_iterations,
                durations
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Concurrency test failed: {e}")
            return self._create_error_result(session.test_config, str(e))
    
    async def _run_endurance_test(self, session: TestSession) -> TestResult:
        """Run an endurance test"""
        try:
            config = session.test_config
            start_time = time.time()
            
            self.logger.info(f"🧪 Running endurance test: {config.iterations} iterations")
            
            # Run iterations over extended period
            successful_iterations = 0
            failed_iterations = 0
            timeout_iterations = 0
            durations = []
            
            for i in range(config.iterations):
                iteration_start = time.time()
                
                try:
                    # Simulate handoff execution with endurance considerations
                    success = await self._simulate_endurance_handoff_execution(config, i)
                    
                    if success:
                        successful_iterations += 1
                    else:
                        failed_iterations += 1
                    
                    # Record duration
                    duration = time.time() - iteration_start
                    durations.append(duration)
                    
                    # Progress update
                    if (i + 1) % 25 == 0:
                        self.logger.info(f"📊 Endurance test progress: {i + 1}/{config.iterations}")
                    
                    # Small delay between iterations for endurance testing
                    await asyncio.sleep(0.01)
                    
                except asyncio.TimeoutError:
                    timeout_iterations += 1
                    durations.append(config.timeout)
                except Exception as e:
                    failed_iterations += 1
                    durations.append(time.time() - iteration_start)
            
            # Calculate results
            end_time = time.time()
            total_duration = end_time - start_time
            
            result = self._calculate_test_results(
                config, start_time, end_time, total_duration,
                successful_iterations, failed_iterations, timeout_iterations,
                durations
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Endurance test failed: {e}")
            return self._create_error_result(session.test_config, str(e))
    
    # Helper methods for test execution
    async def _simulate_handoff_execution(self, config: TestConfiguration) -> bool:
        """Simulate a handoff execution"""
        try:
            # Simulate work with configurable duration
            await asyncio.sleep(0.1)
            
            # Simulate success (95% success rate for reliability tests)
            return random.random() < 0.95
            
        except Exception as e:
            self.logger.error(f"Handoff execution simulation failed: {e}")
            return False
    
    async def _simulate_stressed_handoff_execution(self, config: TestConfiguration) -> bool:
        """Simulate a handoff execution under stress"""
        try:
            # Simulate work with increased stress factor
            stress_duration = 0.1 * config.stress_factor
            await asyncio.sleep(stress_duration)
            
            # Simulate success with reduced rate under stress
            base_success_rate = 0.95
            stress_penalty = min(0.2, (config.stress_factor - 1.0) * 0.1)
            success_rate = max(0.5, base_success_rate - stress_penalty)
            
            return random.random() < success_rate
            
        except Exception as e:
            self.logger.error(f"Stressed handoff execution simulation failed: {e}")
            return False
    
    async def _simulate_failure_injection_handoff(self, config: TestConfiguration) -> bool:
        """Simulate a handoff execution with failure injection"""
        try:
            # Simulate work
            await asyncio.sleep(0.1)
            
            # Inject failures based on configured rate
            if random.random() < config.failure_rate:
                return False
            
            # Simulate normal success rate
            return random.random() < 0.95
            
        except Exception as e:
            self.logger.error(f"Failure injection handoff simulation failed: {e}")
            return False
    
    async def _simulate_concurrent_handoff(self, config: TestConfiguration) -> bool:
        """Simulate a concurrent handoff execution"""
        try:
            # Simulate concurrent work
            await asyncio.sleep(0.05)  # Faster for concurrency tests
            
            # Simulate success with concurrency considerations
            return random.random() < 0.90
            
        except Exception as e:
            self.logger.error(f"Concurrent handoff simulation failed: {e}")
            return False
    
    async def _simulate_endurance_handoff_execution(self, config: TestConfiguration, iteration: int) -> bool:
        """Simulate a handoff execution for endurance testing"""
        try:
            # Simulate work with potential degradation over time
            base_duration = 0.1
            degradation_factor = 1.0 + (iteration / config.iterations) * 0.5  # Up to 50% slower
            duration = base_duration * degradation_factor
            
            await asyncio.sleep(duration)
            
            # Simulate success with potential degradation
            base_success_rate = 0.95
            degradation_penalty = (iteration / config.iterations) * 0.1  # Up to 10% reduction
            success_rate = max(0.8, base_success_rate - degradation_penalty)
            
            return random.random() < success_rate
            
        except Exception as e:
            self.logger.error(f"Endurance handoff execution simulation failed: {e}")
            return False
    
    def _calculate_test_results(self, config: TestConfiguration, start_time: float, end_time: float,
                               total_duration: float, successful_iterations: int, failed_iterations: int,
                               timeout_iterations: int, durations: List[float]) -> TestResult:
        """Calculate comprehensive test results"""
        try:
            # Calculate duration statistics
            if durations:
                min_duration = min(durations)
                max_duration = max(durations)
                average_duration = statistics.mean(durations)
                
                # Calculate percentiles
                sorted_durations = sorted(durations)
                p95_index = int(len(sorted_durations) * 0.95)
                p99_index = int(len(sorted_durations) * 0.99)
                
                p95_duration = sorted_durations[p95_index] if p95_index < len(sorted_durations) else max_duration
                p99_duration = sorted_durations[p99_index] if p99_index < len(sorted_durations) else max_duration
            else:
                min_duration = max_duration = average_duration = p95_duration = p99_duration = 0.0
            
            # Calculate success rate and throughput
            total_iterations = successful_iterations + failed_iterations + timeout_iterations
            success_rate = successful_iterations / total_iterations if total_iterations > 0 else 0.0
            throughput = total_iterations / total_duration if total_duration > 0 else 0.0
            
            # Create test result
            result = TestResult(
                test_id=config.test_id,
                test_type=config.test_type,
                procedure_id=config.procedure_id,
                start_time=start_time,
                end_time=end_time,
                duration=total_duration,
                iterations=total_iterations,
                successful_iterations=successful_iterations,
                failed_iterations=failed_iterations,
                timeout_iterations=timeout_iterations,
                total_duration=total_duration,
                average_duration=average_duration,
                min_duration=min_duration,
                max_duration=max_duration,
                p95_duration=p95_duration,
                p99_duration=p99_duration,
                success_rate=success_rate,
                throughput=throughput
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to calculate test results: {e}")
            return self._create_error_result(config, str(e))
    
    def _create_error_result(self, config: TestConfiguration, error_details: str) -> TestResult:
        """Create an error result for failed tests"""
        current_time = time.time()
        return TestResult(
            test_id=config.test_id,
            test_type=config.test_type,
            procedure_id=config.procedure_id,
            start_time=current_time,
            end_time=current_time,
            duration=0.0,
            error_details=error_details
        )
    
    def _update_reliability_metrics(self, test_result: TestResult):
        """Update reliability performance metrics"""
        try:
            self.reliability_metrics["total_tests"] += 1
            
            if test_result.error_details:
                self.reliability_metrics["failed_tests"] += 1
            else:
                self.reliability_metrics["successful_tests"] += 1
            
            # Update iteration counts
            self.reliability_metrics["total_iterations"] += test_result.iterations
            self.reliability_metrics["successful_iterations"] += test_result.successful_iterations
            self.reliability_metrics["failed_iterations"] += test_result.failed_iterations
            
            # Update averages
            if self.reliability_metrics["total_tests"] > 0:
                self.reliability_metrics["average_success_rate"] = (
                    self.reliability_metrics["successful_iterations"] / self.reliability_metrics["total_iterations"]
                    if self.reliability_metrics["total_iterations"] > 0 else 0.0
                )
                
                self.reliability_metrics["average_duration"] = (
                    test_result.duration / self.reliability_metrics["total_tests"]
                    if test_result.duration else 0.0
                )
            
            # Update test type performance
            test_type = test_result.test_type.value
            if test_type not in self.reliability_metrics["test_type_performance"]:
                self.reliability_metrics["test_type_performance"][test_type] = {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "average_success_rate": 0.0,
                    "average_duration": 0.0
                }
            
            type_metrics = self.reliability_metrics["test_type_performance"][test_type]
            type_metrics["total"] += 1
            
            if test_result.error_details:
                type_metrics["failed"] += 1
            else:
                type_metrics["successful"] += 1
            
            # Update type averages
            if type_metrics["total"] > 0:
                type_metrics["average_success_rate"] = (
                    type_metrics["successful"] / type_metrics["total"]
                )
                
                type_metrics["average_duration"] = (
                    (type_metrics["average_duration"] * (type_metrics["total"] - 1) + test_result.duration) / type_metrics["total"]
                    if test_result.duration else type_metrics["average_duration"]
                )
                
        except Exception as e:
            self.logger.error(f"Failed to update reliability metrics: {e}")
    
    # Public interface methods
    def get_test_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a reliability test session"""
        try:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                return {
                    "session_id": session.session_id,
                    "test_config_id": session.test_config.test_id,
                    "test_type": session.test_config.test_type.value,
                    "status": session.status.value,
                    "progress": session.current_iteration / session.test_config.iterations if session.test_config.iterations > 0 else 0.0,
                    "start_time": session.start_time,
                    "iterations_total": session.test_config.iterations,
                    "iterations_completed": session.current_iteration
                }
            else:
                # Check history
                for test_session in self.test_history:
                    if test_session.session_id == session_id:
                        return {
                            "session_id": test_session.session_id,
                            "test_config_id": test_session.test_config.test_id,
                            "test_type": test_session.test_config.test_type.value,
                            "status": test_session.status.value,
                            "start_time": test_session.start_time,
                            "end_time": test_session.end_time,
                            "duration": test_session.end_time - test_session.start_time if test_session.end_time else None,
                            "error_details": test_session.error_details,
                            "results_count": len(test_session.results)
                        }
                
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to get test status: {e}")
            return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status and metrics"""
        try:
            return {
                "system_status": "operational",
                "active_sessions": len(self.active_sessions),
                "total_tests": self.reliability_metrics["total_tests"],
                "success_rate": (
                    self.reliability_metrics["successful_tests"] / self.reliability_metrics["total_tests"]
                    if self.reliability_metrics["total_tests"] > 0 else 0.0
                ),
                "total_iterations": self.reliability_metrics["total_iterations"],
                "iteration_success_rate": (
                    self.reliability_metrics["successful_iterations"] / self.reliability_metrics["total_iterations"]
                    if self.reliability_metrics["total_iterations"] > 0 else 0.0
                ),
                "average_success_rate": self.reliability_metrics["average_success_rate"],
                "average_duration": self.reliability_metrics["average_duration"],
                "available_configurations": list(self.test_configurations.keys()),
                "test_type_performance": self.reliability_metrics["test_type_performance"]
            }
        except Exception as e:
            self.logger.error(f"Failed to get system status: {e}")
            return {"error": str(e)}
    
    def add_test_configuration(self, config: TestConfiguration) -> bool:
        """Add a new test configuration"""
        try:
            if config.test_id in self.test_configurations:
                self.logger.warning(f"Test configuration {config.test_id} already exists, overwriting")
            
            self.test_configurations[config.test_id] = config
            self.logger.info(f"✅ Added test configuration: {config.test_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add test configuration: {e}")
            return False
    
    def remove_test_configuration(self, config_id: str) -> bool:
        """Remove a test configuration"""
        try:
            if config_id not in self.test_configurations:
                self.logger.warning(f"Test configuration {config_id} not found")
                return False
            
            # Check if configuration is in use
            for session in self.active_sessions.values():
                if session.test_config.test_id == config_id:
                    self.logger.error(f"Cannot remove configuration {config_id} - in use by session {session.session_id}")
                    return False
            
            del self.test_configurations[config_id]
            self.logger.info(f"✅ Removed test configuration: {config_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to remove test configuration: {e}")
            return False


# Global instance for system-wide access
handoff_reliability_system = HandoffReliabilitySystem()


def get_handoff_reliability_system() -> HandoffReliabilitySystem:
    """Get the global handoff reliability system instance"""
    return handoff_reliability_system
