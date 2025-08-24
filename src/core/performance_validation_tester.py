"""Benchmark execution utilities for the Performance Validation System."""
import logging
import time
import uuid
from datetime import datetime

from .agent_manager import AgentStatus, AgentCapability
from .contract_models import ContractPriority
from .performance.metrics.collector import BenchmarkType, PerformanceBenchmark
from .performance_validation_core import PerformanceValidationCore
from .performance_validation_config import PerformanceValidationConfig


class PerformanceValidationTester:
    """Runs individual performance benchmarks."""

    def __init__(
        self,
        core: PerformanceValidationCore,
        config: PerformanceValidationConfig | None = None,
    ) -> None:
        self.core = core
        self.config = config or core.config
        self.logger = logging.getLogger(
            f"{__name__}.PerformanceValidationTester"
        )

    # ------------------------------------------------------------------
    # Benchmark implementations
    # ------------------------------------------------------------------
    def run_response_time_benchmark(self) -> PerformanceBenchmark:
        try:
            start_time = datetime.now()
            response_times = []
            for i in range(self.config.response_iterations):
                agent_start = time.time()
                agent_id = f"response_test_agent_{i}"
                success = self.core.agent_manager.register_agent(
                    agent_id, f"Response Test Agent {i}", [AgentCapability.TESTING]
                )
                agent_end = time.time()
                if success:
                    response_time_ms = (agent_end - agent_start) * 1000
                    response_times.append(response_time_ms)
                    self.core.agent_manager.update_agent_status(
                        agent_id, AgentStatus.OFFLINE
                    )
                time.sleep(self.config.response_delay)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            metrics = self.core.metrics_collector.collect_response_time_metrics(
                response_times
            )
            target = self.core.metrics_collector.benchmark_targets[
                BenchmarkType.RESPONSE_TIME
            ]["target"]
            avg_response = metrics.get("average_response_time", float("inf"))
            performance_level = self.core.validation_rules.classify_performance_level(
                avg_response, target, lower_is_better=True
            )
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
                optimization_recommendations=[],
            )
            benchmark.optimization_recommendations = (
                self.core.validation_rules.generate_optimization_recommendations(
                    benchmark
                )
            )
            self.core.metrics_collector.store_benchmark(benchmark)
            return benchmark
        except Exception as e:
            self.logger.error(f"Response time benchmark failed: {e}")
            return self.core.create_failed_benchmark(
                BenchmarkType.RESPONSE_TIME, "Response Time Test"
            )

    def run_throughput_benchmark(self) -> PerformanceBenchmark:
        try:
            start_time = datetime.now()
            contracts_created = 0
            test_duration = self.config.throughput_test_duration
            test_start = time.time()
            while time.time() - test_start < test_duration:
                contract_id = self.core.contract_manager.create_contract(
                    f"Throughput Test Contract {contracts_created}",
                    "Contract for throughput testing",
                    ContractPriority.NORMAL,
                    [AgentCapability.TESTING],
                    1,
                )
                if contract_id:
                    contracts_created += 1
                time.sleep(self.config.throughput_delay)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            metrics = self.core.metrics_collector.collect_throughput_metrics(
                contracts_created, test_duration
            )
            target = self.core.metrics_collector.benchmark_targets[
                BenchmarkType.THROUGHPUT
            ]["target"]
            throughput = metrics.get("throughput_ops_per_sec", 0)
            performance_level = self.core.validation_rules.classify_performance_level(
                throughput, target, lower_is_better=False
            )
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
                optimization_recommendations=[],
            )
            benchmark.optimization_recommendations = (
                self.core.validation_rules.generate_optimization_recommendations(
                    benchmark
                )
            )
            self.core.metrics_collector.store_benchmark(benchmark)
            return benchmark
        except Exception as e:
            self.logger.error(f"Throughput benchmark failed: {e}")
            return self.core.create_failed_benchmark(
                BenchmarkType.THROUGHPUT, "Throughput Test"
            )

    def run_scalability_benchmark(self) -> PerformanceBenchmark:
        try:
            start_time = datetime.now()
            scalability_results = []
            for concurrent_count in self.config.scalability_levels:
                agent_ids = []
                for i in range(concurrent_count):
                    agent_id = f"scalability_agent_{concurrent_count}_{i}"
                    success = self.core.agent_manager.register_agent(
                        agent_id, f"Scalability Agent {i}", [AgentCapability.TESTING]
                    )
                    if success:
                        agent_ids.append(agent_id)
                perf_start = time.time()
                for agent_id in agent_ids:
                    self.core.agent_manager.update_agent_status(
                        agent_id, AgentStatus.BUSY
                    )
                    self.core.agent_manager.update_agent_status(
                        agent_id, AgentStatus.ONLINE
                    )
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
                for agent_id in agent_ids:
                    self.core.agent_manager.update_agent_status(
                        agent_id, AgentStatus.OFFLINE
                    )
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            metrics = self.core.metrics_collector.collect_scalability_metrics(
                scalability_results
            )
            target = self.core.metrics_collector.benchmark_targets[
                BenchmarkType.SCALABILITY
            ]["target"]
            scalability_score = metrics.get("scalability_score", 0)
            performance_level = self.core.validation_rules.classify_performance_level(
                scalability_score, target, lower_is_better=False
            )
            benchmark = PerformanceBenchmark(
                benchmark_id=str(uuid.uuid4()),
                benchmark_type=BenchmarkType.SCALABILITY,
                test_name="System Scalability Test",
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration=duration,
                metrics=metrics,
                target_metrics={"target_scalability": target},
                performance_level=performance_level,
                optimization_recommendations=[],
            )
            benchmark.optimization_recommendations = (
                self.core.validation_rules.generate_optimization_recommendations(
                    benchmark
                )
            )
            self.core.metrics_collector.store_benchmark(benchmark)
            return benchmark
        except Exception as e:
            self.logger.error(f"Scalability benchmark failed: {e}")
            return self.core.create_failed_benchmark(
                BenchmarkType.SCALABILITY, "Scalability Test"
            )

    def run_reliability_benchmark(self) -> PerformanceBenchmark:
        try:
            start_time = datetime.now()
            total_operations = self.config.reliability_operations
            failed_operations = 0
            for i in range(total_operations):
                try:
                    agent_id = f"reliability_agent_{i}"
                    success = self.core.agent_manager.register_agent(
                        agent_id, f"Reliability Agent {i}", [AgentCapability.TESTING]
                    )
                    if success:
                        self.core.agent_manager.update_agent_status(
                            agent_id, AgentStatus.BUSY
                        )
                        self.core.agent_manager.update_agent_status(
                            agent_id, AgentStatus.OFFLINE
                        )
                    else:
                        failed_operations += 1
                except Exception:
                    failed_operations += 1
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            metrics = self.core.metrics_collector.collect_reliability_metrics(
                total_operations, failed_operations, duration
            )
            target = self.core.metrics_collector.benchmark_targets[
                BenchmarkType.RELIABILITY
            ]["target"]
            success_rate = metrics.get("success_rate_percent", 0)
            performance_level = self.core.validation_rules.classify_performance_level(
                success_rate, target, lower_is_better=False
            )
            benchmark = PerformanceBenchmark(
                benchmark_id=str(uuid.uuid4()),
                benchmark_type=BenchmarkType.RELIABILITY,
                test_name="System Reliability Test",
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration=duration,
                metrics=metrics,
                target_metrics={"target_reliability": target},
                performance_level=performance_level,
                optimization_recommendations=[],
            )
            benchmark.optimization_recommendations = (
                self.core.validation_rules.generate_optimization_recommendations(
                    benchmark
                )
            )
            self.core.metrics_collector.store_benchmark(benchmark)
            return benchmark
        except Exception as e:
            self.logger.error(f"Reliability benchmark failed: {e}")
            return self.core.create_failed_benchmark(
                BenchmarkType.RELIABILITY, "Reliability Test"
            )

    def run_latency_benchmark(self) -> PerformanceBenchmark:
        try:
            start_time = datetime.now()
            latency_times = []
            for i in range(self.config.latency_iterations):
                latency_start = time.time()
                # Use summary retrieval to simulate a small operation
                self.core.agent_manager.get_agent_summary()
                latency_end = time.time()
                latency_ms = (latency_end - latency_start) * 1000
                latency_times.append(latency_ms)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            metrics = self.core.metrics_collector.collect_latency_metrics(latency_times)
            target = self.core.metrics_collector.benchmark_targets[
                BenchmarkType.LATENCY
            ]["target"]
            avg_latency = metrics.get("average_latency_ms", float("inf"))
            performance_level = self.core.validation_rules.classify_performance_level(
                avg_latency, target, lower_is_better=True
            )
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
                optimization_recommendations=[],
            )
            benchmark.optimization_recommendations = (
                self.core.validation_rules.generate_optimization_recommendations(
                    benchmark
                )
            )
            self.core.metrics_collector.store_benchmark(benchmark)
            return benchmark
        except Exception as e:
            self.logger.error(f"Latency benchmark failed: {e}")
            return self.core.create_failed_benchmark(
                BenchmarkType.LATENCY, "Latency Test"
            )
