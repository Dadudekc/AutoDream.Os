#!/usr/bin/env python3
"""
Performance Validation System - V2 Core Performance Testing & Optimization

This module provides comprehensive performance benchmarking, optimization validation,
and enterprise readiness testing for the V2 system.
Follows Single Responsibility Principle - only performance validation.
Architecture: Single Responsibility Principle - performance validation only
LOC: Target 300 lines (under 350 limit)
"""

import os
import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Any, Set, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import threading
import time
import uuid
from collections import defaultdict
import statistics
import asyncio
import concurrent.futures

from .agent_manager import AgentManager, AgentStatus, AgentCapability, AgentInfo
from .config_manager import ConfigManager
from .assignment_engine import ContractManager
from .contract_models import ContractPriority, ContractStatus
from .workflow import (
    WorkflowOrchestrator as AdvancedWorkflowEngine,  # Backward compatibility alias
    WorkflowType,
    TaskPriority as WorkflowPriority,  # Backward compatibility alias
    WorkflowTask as WorkflowStep,  # Backward compatibility alias
)

logger = logging.getLogger(__name__)


class BenchmarkType(Enum):
    """Performance benchmark types"""

    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    SCALABILITY = "scalability"
    RELIABILITY = "reliability"
    RESOURCE_UTILIZATION = "resource_utilization"
    LATENCY = "latency"


class PerformanceLevel(Enum):
    """Performance level classifications"""

    ENTERPRISE_READY = "enterprise_ready"
    PRODUCTION_READY = "production_ready"
    DEVELOPMENT_READY = "development_ready"
    NOT_READY = "not_ready"


class OptimizationTarget(Enum):
    """Optimization targets"""

    RESPONSE_TIME_IMPROVEMENT = "response_time_improvement"
    THROUGHPUT_INCREASE = "throughput_increase"
    SCALABILITY_ENHANCEMENT = "scalability_enhancement"
    RELIABILITY_IMPROVEMENT = "reliability_improvement"
    RESOURCE_EFFICIENCY = "resource_efficiency"


@dataclass
class PerformanceBenchmark:
    """Performance benchmark result"""

    benchmark_id: str
    benchmark_type: BenchmarkType
    test_name: str
    start_time: str
    end_time: str
    duration: float
    metrics: Dict[str, float]
    target_metrics: Dict[str, float]
    performance_level: PerformanceLevel
    optimization_recommendations: List[str]


@dataclass
class SystemPerformanceReport:
    """System performance report"""

    report_id: str
    timestamp: str
    overall_performance_level: PerformanceLevel
    benchmark_results: List[PerformanceBenchmark]
    optimization_opportunities: List[OptimizationTarget]
    enterprise_readiness_score: float
    recommendations: List[str]


class PerformanceValidationSystem:
    """
    Comprehensive performance validation and optimization system

    Responsibilities:
    - Performance benchmarking and testing
    - Optimization validation and measurement
    - Enterprise readiness assessment
    - Scalability and reliability testing
    - Performance optimization recommendations
    """

    def __init__(
        self,
        agent_manager: AgentManager,
        config_manager: ConfigManager,
        contract_manager: ContractManager,
        workflow_engine: AdvancedWorkflowEngine,
    ):
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.contract_manager = contract_manager
        self.workflow_engine = workflow_engine

        # Performance data
        self.benchmarks: Dict[str, PerformanceBenchmark] = {}
        self.performance_reports: List[SystemPerformanceReport] = []
        self.optimization_history: List[Dict[str, Any]] = []

        # Benchmark targets
        self.benchmark_targets = {
            BenchmarkType.RESPONSE_TIME: {"target": 100, "unit": "ms"},  # <100ms target
            BenchmarkType.THROUGHPUT: {
                "target": 1000,
                "unit": "ops/sec",
            },  # 1000 ops/sec target
            BenchmarkType.SCALABILITY: {
                "target": 100,
                "unit": "concurrent_users",
            },  # 100 concurrent users
            BenchmarkType.RELIABILITY: {
                "target": 99.9,
                "unit": "%",
            },  # 99.9% uptime target
            BenchmarkType.LATENCY: {"target": 50, "unit": "ms"},  # <50ms latency target
        }

        # Performance thresholds
        self.performance_thresholds = {
            PerformanceLevel.ENTERPRISE_READY: 0.95,  # 95% of targets met
            PerformanceLevel.PRODUCTION_READY: 0.85,  # 85% of targets met
            PerformanceLevel.DEVELOPMENT_READY: 0.70,  # 70% of targets met
            PerformanceLevel.NOT_READY: 0.0,  # Below 70%
        }

        self.logger = logging.getLogger(f"{__name__}.PerformanceValidationSystem")

    def run_comprehensive_benchmark(self) -> str:
        """Run comprehensive performance benchmark suite"""
        try:
            benchmark_id = str(uuid.uuid4())
            start_time = datetime.now()

            self.logger.info(f"Starting comprehensive benchmark: {benchmark_id}")

            # Run all benchmark types
            benchmark_results = []

            # Response time benchmark
            response_benchmark = self._run_response_time_benchmark()
            benchmark_results.append(response_benchmark)

            # Throughput benchmark
            throughput_benchmark = self._run_throughput_benchmark()
            benchmark_results.append(throughput_benchmark)

            # Scalability benchmark
            scalability_benchmark = self._run_scalability_benchmark()
            benchmark_results.append(scalability_benchmark)

            # Reliability benchmark
            reliability_benchmark = self._run_reliability_benchmark()
            benchmark_results.append(reliability_benchmark)

            # Latency benchmark
            latency_benchmark = self._run_latency_benchmark()
            benchmark_results.append(latency_benchmark)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Calculate overall performance level
            overall_level = self._calculate_overall_performance_level(benchmark_results)

            # Generate performance report
            report = SystemPerformanceReport(
                report_id=str(uuid.uuid4()),
                timestamp=datetime.now().isoformat(),
                overall_performance_level=overall_level,
                benchmark_results=benchmark_results,
                optimization_opportunities=self._identify_optimization_opportunities(
                    benchmark_results
                ),
                enterprise_readiness_score=self._calculate_enterprise_readiness_score(
                    benchmark_results
                ),
                recommendations=self._generate_performance_recommendations(
                    benchmark_results
                ),
            )

            self.performance_reports.append(report)

            self.logger.info(
                f"Comprehensive benchmark completed: {benchmark_id} in {duration:.2f}s"
            )
            return benchmark_id

        except Exception as e:
            self.logger.error(f"Comprehensive benchmark failed: {e}")
            return ""

    def _run_response_time_benchmark(self) -> PerformanceBenchmark:
        """Run response time benchmark"""
        try:
            start_time = datetime.now()

            # Test agent registration response time
            response_times = []
            for i in range(10):
                test_start = time.time()

                # Register test agent
                success = self.agent_manager.register_agent(
                    f"benchmark_agent_{i}",
                    f"Benchmark Agent {i}",
                    [AgentCapability.TESTING],
                )

                test_end = time.time()
                response_time = (test_end - test_start) * 1000  # Convert to ms
                response_times.append(response_time)

                # Cleanup
                if success:
                    self.agent_manager.remove_agent(f"benchmark_agent_{i}")

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Calculate metrics
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)

            metrics = {
                "average_response_time": avg_response_time,
                "min_response_time": min_response_time,
                "max_response_time": max_response_time,
                "response_time_variance": statistics.variance(response_times),
            }

            # Determine performance level
            target = self.benchmark_targets[BenchmarkType.RESPONSE_TIME]["target"]
            performance_level = self._classify_performance_level(
                avg_response_time, target, lower_is_better=True
            )

            # Generate recommendations
            recommendations = []
            if avg_response_time > target:
                recommendations.append("Optimize agent registration process")
                recommendations.append("Consider caching mechanisms")
                recommendations.append("Review database query performance")

            benchmark = PerformanceBenchmark(
                benchmark_id=str(uuid.uuid4()),
                benchmark_type=BenchmarkType.RESPONSE_TIME,
                test_name="Agent Registration Response Time",
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration=duration,
                metrics=metrics,
                target_metrics={"target_response_time": target},
                performance_level=performance_level,
                optimization_recommendations=recommendations,
            )

            self.benchmarks[benchmark.benchmark_id] = benchmark
            return benchmark

        except Exception as e:
            self.logger.error(f"Response time benchmark failed: {e}")
            return self._create_failed_benchmark(
                BenchmarkType.RESPONSE_TIME, "Response Time Test"
            )

    def _run_throughput_benchmark(self) -> PerformanceBenchmark:
        """Run throughput benchmark"""
        try:
            start_time = datetime.now()

            # Test contract creation throughput
            contract_creation_times = []
            contracts_created = 0

            # Create contracts rapidly for 5 seconds
            test_duration = 5.0
            test_start = time.time()

            while time.time() - test_start < test_duration:
                contract_start = time.time()

                contract_id = self.contract_manager.create_contract(
                    f"Throughput Test Contract {contracts_created}",
                    "Contract for throughput testing",
                    ContractPriority.NORMAL,
                    [AgentCapability.TESTING],
                    1,
                )

                contract_end = time.time()
                if contract_id:
                    contracts_created += 1
                    contract_creation_times.append(contract_end - contract_start)

                # Small delay to prevent overwhelming
                time.sleep(0.01)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Calculate throughput metrics
            total_contracts = contracts_created
            throughput_ops_per_sec = total_contracts / test_duration
            avg_creation_time = (
                statistics.mean(contract_creation_times)
                if contract_creation_times
                else 0
            )

            metrics = {
                "total_contracts_created": total_contracts,
                "throughput_ops_per_sec": throughput_ops_per_sec,
                "average_creation_time": avg_creation_time,
                "test_duration": test_duration,
            }

            # Determine performance level
            target = self.benchmark_targets[BenchmarkType.THROUGHPUT]["target"]
            performance_level = self._classify_performance_level(
                throughput_ops_per_sec, target, lower_is_better=False
            )

            # Generate recommendations
            recommendations = []
            if throughput_ops_per_sec < target:
                recommendations.append("Optimize contract creation process")
                recommendations.append("Consider batch contract creation")
                recommendations.append("Review database write performance")

            benchmark = PerformanceBenchmark(
                benchmark_id=str(uuid.uuid4()),
                benchmark_type=BenchmarkType.THROUGHPUT,
                test_name="Contract Creation Throughput",
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration=duration,
                metrics=metrics,
                target_metrics={"target_throughput": target},
                performance_level=performance_level,
                optimization_recommendations=recommendations,
            )

            self.benchmarks[benchmark.benchmark_id] = benchmark
            return benchmark

        except Exception as e:
            self.logger.error(f"Throughput benchmark failed: {e}")
            return self._create_failed_benchmark(
                BenchmarkType.THROUGHPUT, "Throughput Test"
            )

    def _run_scalability_benchmark(self) -> PerformanceBenchmark:
        """Run scalability benchmark"""
        try:
            start_time = datetime.now()

            # Test system performance with increasing load
            scalability_results = []
            max_concurrent_agents = 50

            for concurrent_count in [10, 25, 50]:
                # Create concurrent agents
                agent_ids = []
                for i in range(concurrent_count):
                    agent_id = f"scalability_agent_{concurrent_count}_{i}"
                    success = self.agent_manager.register_agent(
                        agent_id, f"Scalability Agent {i}", [AgentCapability.TESTING]
                    )
                    if success:
                        agent_ids.append(agent_id)

                # Measure system performance
                perf_start = time.time()

                # Perform operations with current load
                for agent_id in agent_ids:
                    self.agent_manager.update_agent_status(agent_id, AgentStatus.BUSY)
                    self.agent_manager.update_agent_status(agent_id, AgentStatus.ONLINE)

                perf_end = time.time()
                operation_time = perf_end - perf_start

                scalability_results.append(
                    {
                        "concurrent_agents": concurrent_count,
                        "operation_time": operation_time,
                        "operations_per_second": concurrent_count / operation_time
                        if operation_time > 0
                        else 0,
                    }
                )

                # Cleanup
                for agent_id in agent_ids:
                    self.agent_manager.remove_agent(agent_id)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Calculate scalability metrics
            scalability_score = self._calculate_scalability_score(scalability_results)
            max_ops_per_sec = max(
                result["operations_per_second"] for result in scalability_results
            )

            metrics = {
                "scalability_score": scalability_score,
                "max_operations_per_second": max_ops_per_sec,
                "concurrent_agent_tests": len(scalability_results),
                "scalability_results": scalability_results,
            }

            # Determine performance level
            target = self.benchmark_targets[BenchmarkType.SCALABILITY]["target"]
            performance_level = self._classify_performance_level(
                scalability_score, target, lower_is_better=False
            )

            # Generate recommendations
            recommendations = []
            if scalability_score < target * 0.8:
                recommendations.append("Optimize concurrent agent handling")
                recommendations.append("Review thread pool management")
                recommendations.append("Consider connection pooling")

            benchmark = PerformanceBenchmark(
                benchmark_id=str(uuid.uuid4()),
                benchmark_type=BenchmarkType.SCALABILITY,
                test_name="Concurrent Agent Scalability",
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration=duration,
                metrics=metrics,
                target_metrics={"target_concurrent_users": target},
                performance_level=performance_level,
                optimization_recommendations=recommendations,
            )

            self.benchmarks[benchmark.benchmark_id] = benchmark
            return benchmark

        except Exception as e:
            self.logger.error(f"Scalability benchmark failed: {e}")
            return self._create_failed_benchmark(
                BenchmarkType.SCALABILITY, "Scalability Test"
            )

    def _run_reliability_benchmark(self) -> PerformanceBenchmark:
        """Run reliability benchmark"""
        try:
            start_time = datetime.now()

            # Test system reliability with repeated operations
            total_operations = 100
            successful_operations = 0
            failed_operations = 0
            operation_times = []

            for i in range(total_operations):
                try:
                    op_start = time.time()

                    # Perform reliability test operation
                    success = self.agent_manager.register_agent(
                        f"reliability_agent_{i}",
                        f"Reliability Agent {i}",
                        [AgentCapability.TESTING],
                    )

                    op_end = time.time()
                    operation_time = op_end - op_start
                    operation_times.append(operation_time)

                    if success:
                        successful_operations += 1
                        # Cleanup
                        self.agent_manager.remove_agent(f"reliability_agent_{i}")
                    else:
                        failed_operations += 1

                except Exception as e:
                    failed_operations += 1
                    self.logger.warning(f"Reliability test operation {i} failed: {e}")

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Calculate reliability metrics
            success_rate = (successful_operations / total_operations) * 100
            failure_rate = (failed_operations / total_operations) * 100
            avg_operation_time = (
                statistics.mean(operation_times) if operation_times else 0
            )

            metrics = {
                "total_operations": total_operations,
                "successful_operations": successful_operations,
                "failed_operations": failed_operations,
                "success_rate_percent": success_rate,
                "failure_rate_percent": failure_rate,
                "average_operation_time": avg_operation_time,
            }

            # Determine performance level
            target = self.benchmark_targets[BenchmarkType.RELIABILITY]["target"]
            performance_level = self._classify_performance_level(
                success_rate, target, lower_is_better=False
            )

            # Generate recommendations
            recommendations = []
            if success_rate < target:
                recommendations.append("Investigate operation failures")
                recommendations.append("Improve error handling")
                recommendations.append("Review system stability")

            benchmark = PerformanceBenchmark(
                benchmark_id=str(uuid.uuid4()),
                benchmark_type=BenchmarkType.RELIABILITY,
                test_name="System Reliability Test",
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration=duration,
                metrics=metrics,
                target_metrics={"target_success_rate": target},
                performance_level=performance_level,
                optimization_recommendations=recommendations,
            )

            self.benchmarks[benchmark.benchmark_id] = benchmark
            return benchmark

        except Exception as e:
            self.logger.error(f"Reliability benchmark failed: {e}")
            return self._create_failed_benchmark(
                BenchmarkType.RELIABILITY, "Reliability Test"
            )

    def _run_latency_benchmark(self) -> PerformanceBenchmark:
        """Run latency benchmark"""
        try:
            start_time = datetime.now()

            # Test system latency with various operations
            latency_measurements = []

            # Test different operation types
            operations = [
                ("agent_status_check", lambda: self.agent_manager.get_all_agents()),
                (
                    "contract_list",
                    lambda: self.contract_manager.get_pending_contracts(),
                ),
                (
                    "workflow_status",
                    lambda: self.workflow_engine.get_workflow_status("test")
                    if "test" in self.workflow_engine.workflows
                    else None,
                ),
            ]

            for op_name, op_func in operations:
                for i in range(20):  # 20 measurements per operation
                    try:
                        op_start = time.time()
                        op_func()
                        op_end = time.time()

                        latency = (op_end - op_start) * 1000  # Convert to ms
                        latency_measurements.append(
                            {
                                "operation": op_name,
                                "latency_ms": latency,
                                "iteration": i,
                            }
                        )

                    except Exception as e:
                        # Record failed operation
                        latency_measurements.append(
                            {
                                "operation": op_name,
                                "latency_ms": float("inf"),
                                "iteration": i,
                                "error": str(e),
                            }
                        )

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Calculate latency metrics
            successful_measurements = [
                m for m in latency_measurements if m["latency_ms"] != float("inf")
            ]

            if successful_measurements:
                avg_latency = statistics.mean(
                    m["latency_ms"] for m in successful_measurements
                )
                min_latency = min(m["latency_ms"] for m in successful_measurements)
                max_latency = max(m["latency_ms"] for m in successful_measurements)
                p95_latency = self._calculate_percentile(
                    [m["latency_ms"] for m in successful_measurements], 95
                )
            else:
                avg_latency = min_latency = max_latency = p95_latency = 0

            metrics = {
                "average_latency_ms": avg_latency,
                "min_latency_ms": min_latency,
                "max_latency_ms": max_latency,
                "p95_latency_ms": p95_latency,
                "total_measurements": len(latency_measurements),
                "successful_measurements": len(successful_measurements),
            }

            # Determine performance level
            target = self.benchmark_targets[BenchmarkType.LATENCY]["target"]
            performance_level = self._classify_performance_level(
                avg_latency, target, lower_is_better=True
            )

            # Generate recommendations
            recommendations = []
            if avg_latency > target:
                recommendations.append("Optimize database queries")
                recommendations.append("Implement caching strategies")
                recommendations.append("Review network latency")

            benchmark = PerformanceBenchmark(
                benchmark_id=str(uuid.uuid4()),
                benchmark_type=BenchmarkType.LATENCY,
                test_name="System Latency Test",
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration=duration,
                metrics=metrics,
                target_metrics={"target_latency": target},
                performance_level=performance_level,
                optimization_recommendations=recommendations,
            )

            self.benchmarks[benchmark.benchmark_id] = benchmark
            return benchmark

        except Exception as e:
            self.logger.error(f"Latency benchmark failed: {e}")
            return self._create_failed_benchmark(BenchmarkType.LATENCY, "Latency Test")

    def _calculate_scalability_score(
        self, scalability_results: List[Dict[str, Any]]
    ) -> float:
        """Calculate scalability score based on results"""
        try:
            if len(scalability_results) < 2:
                return 0.0

            # Calculate how well the system scales
            base_performance = scalability_results[0]["operations_per_second"]
            max_performance = max(
                result["operations_per_second"] for result in scalability_results
            )

            if base_performance == 0:
                return 0.0

            # Score based on performance increase vs load increase
            load_increase = (
                scalability_results[-1]["concurrent_agents"]
                / scalability_results[0]["concurrent_agents"]
            )
            performance_increase = max_performance / base_performance

            # Ideal scaling would have performance increase proportional to load increase
            scaling_efficiency = performance_increase / load_increase

            return min(100.0, scaling_efficiency * 100)

        except Exception as e:
            self.logger.error(f"Failed to calculate scalability score: {e}")
            return 0.0

    def _calculate_percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile value"""
        try:
            if not values:
                return 0.0

            sorted_values = sorted(values)
            index = int((percentile / 100) * len(sorted_values))
            return sorted_values[min(index, len(sorted_values) - 1)]

        except Exception as e:
            self.logger.error(f"Failed to calculate percentile: {e}")
            return 0.0

    def _classify_performance_level(
        self, actual_value: float, target_value: float, lower_is_better: bool = False
    ) -> PerformanceLevel:
        """Classify performance level based on target"""
        try:
            if target_value == 0:
                return PerformanceLevel.NOT_READY

            if lower_is_better:
                # For metrics where lower is better (e.g., response time, latency)
                ratio = target_value / actual_value if actual_value > 0 else 0
            else:
                # For metrics where higher is better (e.g., throughput, success rate)
                ratio = actual_value / target_value

            if ratio >= self.performance_thresholds[PerformanceLevel.ENTERPRISE_READY]:
                return PerformanceLevel.ENTERPRISE_READY
            elif (
                ratio >= self.performance_thresholds[PerformanceLevel.PRODUCTION_READY]
            ):
                return PerformanceLevel.PRODUCTION_READY
            elif (
                ratio >= self.performance_thresholds[PerformanceLevel.DEVELOPMENT_READY]
            ):
                return PerformanceLevel.DEVELOPMENT_READY
            else:
                return PerformanceLevel.NOT_READY

        except Exception as e:
            self.logger.error(f"Failed to classify performance level: {e}")
            return PerformanceLevel.NOT_READY

    def _calculate_overall_performance_level(
        self, benchmarks: List[PerformanceBenchmark]
    ) -> PerformanceLevel:
        """Calculate overall performance level from all benchmarks"""
        try:
            if not benchmarks:
                return PerformanceLevel.NOT_READY

            # Count performance levels
            level_counts = defaultdict(int)
            for benchmark in benchmarks:
                level_counts[benchmark.performance_level] += 1

            # Calculate weighted score
            total_benchmarks = len(benchmarks)
            enterprise_score = (
                level_counts[PerformanceLevel.ENTERPRISE_READY] / total_benchmarks
            )
            production_score = (
                level_counts[PerformanceLevel.PRODUCTION_READY] / total_benchmarks
            )
            development_score = (
                level_counts[PerformanceLevel.DEVELOPMENT_READY] / total_benchmarks
            )

            # Determine overall level
            if enterprise_score >= 0.6:  # 60% enterprise ready
                return PerformanceLevel.ENTERPRISE_READY
            elif production_score >= 0.6:  # 60% production ready
                return PerformanceLevel.PRODUCTION_READY
            elif development_score >= 0.6:  # 60% development ready
                return PerformanceLevel.DEVELOPMENT_READY
            else:
                return PerformanceLevel.NOT_READY

        except Exception as e:
            self.logger.error(f"Failed to calculate overall performance level: {e}")
            return PerformanceLevel.NOT_READY

    def _calculate_enterprise_readiness_score(
        self, benchmarks: List[PerformanceBenchmark]
    ) -> float:
        """Calculate enterprise readiness score (0-100)"""
        try:
            if not benchmarks:
                return 0.0

            total_score = 0.0
            for benchmark in benchmarks:
                if benchmark.performance_level == PerformanceLevel.ENTERPRISE_READY:
                    total_score += 100
                elif benchmark.performance_level == PerformanceLevel.PRODUCTION_READY:
                    total_score += 85
                elif benchmark.performance_level == PerformanceLevel.DEVELOPMENT_READY:
                    total_score += 70
                else:
                    total_score += 0

            return total_score / len(benchmarks)

        except Exception as e:
            self.logger.error(f"Failed to calculate enterprise readiness score: {e}")
            return 0.0

    def _identify_optimization_opportunities(
        self, benchmarks: List[PerformanceBenchmark]
    ) -> List[OptimizationTarget]:
        """Identify optimization opportunities from benchmarks"""
        try:
            opportunities = []

            for benchmark in benchmarks:
                if benchmark.performance_level in [
                    PerformanceLevel.DEVELOPMENT_READY,
                    PerformanceLevel.NOT_READY,
                ]:
                    if benchmark.benchmark_type == BenchmarkType.RESPONSE_TIME:
                        opportunities.append(
                            OptimizationTarget.RESPONSE_TIME_IMPROVEMENT
                        )
                    elif benchmark.benchmark_type == BenchmarkType.THROUGHPUT:
                        opportunities.append(OptimizationTarget.THROUGHPUT_INCREASE)
                    elif benchmark.benchmark_type == BenchmarkType.SCALABILITY:
                        opportunities.append(OptimizationTarget.SCALABILITY_ENHANCEMENT)
                    elif benchmark.benchmark_type == BenchmarkType.RELIABILITY:
                        opportunities.append(OptimizationTarget.RELIABILITY_IMPROVEMENT)
                    elif benchmark.benchmark_type == BenchmarkType.LATENCY:
                        opportunities.append(
                            OptimizationTarget.RESPONSE_TIME_IMPROVEMENT
                        )

            return list(set(opportunities))  # Remove duplicates

        except Exception as e:
            self.logger.error(f"Failed to identify optimization opportunities: {e}")
            return []

    def _generate_performance_recommendations(
        self, benchmarks: List[PerformanceBenchmark]
    ) -> List[str]:
        """Generate performance recommendations from benchmarks"""
        try:
            recommendations = []

            for benchmark in benchmarks:
                if benchmark.performance_level in [
                    PerformanceLevel.DEVELOPMENT_READY,
                    PerformanceLevel.NOT_READY,
                ]:
                    recommendations.extend(benchmark.optimization_recommendations)

            # Add general recommendations
            if len(recommendations) > 0:
                recommendations.append("Implement comprehensive performance monitoring")
                recommendations.append("Establish performance baselines and targets")
                recommendations.append("Regular performance testing and optimization")

            return list(set(recommendations))  # Remove duplicates

        except Exception as e:
            self.logger.error(f"Failed to generate performance recommendations: {e}")
            return ["Review system performance and implement optimizations"]

    def _create_failed_benchmark(
        self, benchmark_type: BenchmarkType, test_name: str
    ) -> PerformanceBenchmark:
        """Create a failed benchmark result"""
        return PerformanceBenchmark(
            benchmark_id=str(uuid.uuid4()),
            benchmark_type=benchmark_type,
            test_name=test_name,
            start_time=datetime.now().isoformat(),
            end_time=datetime.now().isoformat(),
            duration=0.0,
            metrics={"error": "Benchmark failed"},
            target_metrics={},
            performance_level=PerformanceLevel.NOT_READY,
            optimization_recommendations=[
                "Investigate benchmark failure",
                "Review system stability",
            ],
        )

    def get_latest_performance_report(self) -> Optional[SystemPerformanceReport]:
        """Get the latest performance report"""
        if self.performance_reports:
            return self.performance_reports[-1]
        return None

    def get_benchmark_summary(self) -> Dict[str, Any]:
        """Get summary of all benchmarks"""
        try:
            total_benchmarks = len(self.benchmarks)
            successful_benchmarks = len(
                [
                    b
                    for b in self.benchmarks.values()
                    if b.performance_level != PerformanceLevel.NOT_READY
                ]
            )

            performance_distribution = defaultdict(int)
            for benchmark in self.benchmarks.values():
                performance_distribution[benchmark.performance_level.value] += 1

            return {
                "total_benchmarks": total_benchmarks,
                "successful_benchmarks": successful_benchmarks,
                "success_rate": (successful_benchmarks / total_benchmarks * 100)
                if total_benchmarks > 0
                else 0,
                "performance_distribution": dict(performance_distribution),
                "latest_report": self.get_latest_performance_report().report_id
                if self.get_latest_performance_report()
                else None,
            }

        except Exception as e:
            self.logger.error(f"Failed to get benchmark summary: {e}")
            return {"error": str(e)}

    def run_smoke_test(self) -> bool:
        """Run basic functionality test"""
        try:
            # Test benchmark creation
            benchmark_id = self.run_comprehensive_benchmark()
            if not benchmark_id:
                return False

            # Test report retrieval
            report = self.get_latest_performance_report()
            if not report:
                return False

            # Test summary retrieval
            summary = self.get_benchmark_summary()
            if "total_benchmarks" not in summary:
                return False

            return True

        except Exception as e:
            self.logger.error(f"Smoke test failed: {e}")
            return False


def run_smoke_test():
    """Run basic functionality test for PerformanceValidationSystem"""
    print("🧪 Running PerformanceValidationSystem Smoke Test...")

    try:
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary directories
            agent_dir = Path(temp_dir) / "agent_workspaces"
            config_dir = Path(temp_dir) / "config"
            agent_dir.mkdir()
            config_dir.mkdir()

            # Create mock agent
            test_agent_dir = agent_dir / "Agent-1"
            test_agent_dir.mkdir()

            # Initialize managers
            config_manager = ConfigManager(config_dir)
            agent_manager = AgentManager(agent_dir)
            contract_manager = ContractManager(agent_manager, config_manager)

            # Initialize workflow engine (mock)
            class MockWorkflowEngine:
                def __init__(self):
                    self.workflows = {}

            workflow_engine = MockWorkflowEngine()

            # Initialize performance validation system
            perf_system = PerformanceValidationSystem(
                agent_manager, config_manager, contract_manager, workflow_engine
            )

            # Test basic functionality
            success = perf_system.run_smoke_test()
            assert success, "Smoke test failed"

            # Cleanup
            agent_manager.shutdown()
            config_manager.shutdown()

        print("✅ PerformanceValidationSystem Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ PerformanceValidationSystem Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for PerformanceValidationSystem testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Performance Validation System CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--benchmark", action="store_true", help="Run comprehensive benchmark"
    )
    parser.add_argument("--summary", action="store_true", help="Show benchmark summary")
    parser.add_argument(
        "--report", action="store_true", help="Show latest performance report"
    )

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    # Initialize managers
    config_manager = ConfigManager()
    agent_manager = AgentManager()
    contract_manager = ContractManager(agent_manager, config_manager)

    # Initialize workflow engine (mock)
    class MockWorkflowEngine:
        def __init__(self):
            self.workflows = {}

    workflow_engine = MockWorkflowEngine()

    # Initialize performance validation system
    perf_system = PerformanceValidationSystem(
        agent_manager, config_manager, contract_manager, workflow_engine
    )

    if args.benchmark:
        benchmark_id = perf_system.run_comprehensive_benchmark()
        print(f"Comprehensive benchmark: {'✅ Started' if benchmark_id else '❌ Failed'}")
        if benchmark_id:
            print(f"Benchmark ID: {benchmark_id}")

    elif args.summary:
        summary = perf_system.get_benchmark_summary()
        print("Benchmark Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")

    elif args.report:
        report = perf_system.get_latest_performance_report()
        if report:
            print(f"Latest Performance Report: {report.report_id}")
            print(f"Overall Performance: {report.overall_performance_level.value}")
            print(f"Enterprise Readiness: {report.enterprise_readiness_score:.1f}%")
        else:
            print("No performance reports available")

    else:
        parser.print_help()

    # Cleanup
    agent_manager.shutdown()
    config_manager.shutdown()


if __name__ == "__main__":
    main()
