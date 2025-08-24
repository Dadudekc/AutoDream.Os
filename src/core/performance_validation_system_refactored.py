#!/usr/bin/env python3
"""
Performance Validation System - V2 Core Performance Testing & Optimization
==========================================================================

Refactored performance validation system using modular architecture.
Orchestrates metrics collection, validation, reporting, and alerting modules.
Follows Single Responsibility Principle - orchestration and coordination only.
"""

import logging
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

from src.utils.stability_improvements import stability_manager, safe_import
from .agent_manager import AgentManager, AgentStatus, AgentCapability, AgentInfo
from .config_manager import ConfigManager
from .assignment_engine import ContractManager
from .contract_models import ContractPriority, ContractStatus
from .workflow import (
    WorkflowOrchestrator as AdvancedWorkflowEngine,
    WorkflowType,
    TaskPriority as WorkflowPriority,
    WorkflowTask as WorkflowStep,
)

# Import the extracted performance modules
from .performance.metrics.collector import (
    MetricsCollector, 
    BenchmarkType, 
    PerformanceLevel, 
    PerformanceBenchmark
)
from .performance.validation.rules import ValidationRules, OptimizationTarget
from .performance.reporting.generator import ReportGenerator, SystemPerformanceReport
from .performance.alerts.manager import AlertManager, AlertSeverity, AlertType

logger = logging.getLogger(__name__)


class PerformanceValidationSystem:
    """
    Comprehensive performance validation and optimization system
    
    Responsibilities:
    - Orchestrate performance benchmarking workflow
    - Coordinate between metrics, validation, reporting, and alerting modules
    - Provide unified interface for performance validation
    - Manage benchmark execution lifecycle
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
        
        # Initialize performance modules
        self.metrics_collector = MetricsCollector()
        self.validation_rules = ValidationRules()
        self.report_generator = ReportGenerator()
        self.alert_manager = AlertManager()
        
        # Setup alert handlers
        self._setup_alert_handlers()
        
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
            
            # Calculate overall performance level using validation rules
            overall_level = self.validation_rules.calculate_overall_performance_level(benchmark_results)
            
            # Generate comprehensive recommendations
            all_recommendations = []
            for benchmark in benchmark_results:
                recommendations = self.validation_rules.generate_optimization_recommendations(benchmark)
                all_recommendations.extend(recommendations)
            
            # Remove duplicates while preserving order
            unique_recommendations = []
            seen = set()
            for rec in all_recommendations:
                if rec not in seen:
                    unique_recommendations.append(rec)
                    seen.add(rec)
            
            # Generate performance report
            report = self.report_generator.generate_performance_report(
                benchmark_results, overall_level, unique_recommendations
            )
            
            # Check for alerts
            for benchmark in benchmark_results:
                self.alert_manager.check_benchmark_for_alerts(benchmark)
            
            self.logger.info(
                f"Completed comprehensive benchmark: {benchmark_id} "
                f"(Duration: {duration:.2f}s, Level: {overall_level.value})"
            )
            
            return benchmark_id
            
        except Exception as e:
            self.logger.error(f"Comprehensive benchmark failed: {e}")
            return ""
    
    def _run_response_time_benchmark(self) -> PerformanceBenchmark:
        """Run response time benchmark using metrics collector"""
        try:
            start_time = datetime.now()
            
            # Test agent registration response times
            response_times = []
            
            for i in range(10):
                agent_start = time.time()
                
                agent_id = f"response_test_agent_{i}"
                success = self.agent_manager.register_agent(
                    agent_id, f"Response Test Agent {i}", [AgentCapability.TESTING]
                )
                
                agent_end = time.time()
                
                if success:
                    response_time_ms = (agent_end - agent_start) * 1000
                    response_times.append(response_time_ms)
                    
                    # Cleanup
                    self.agent_manager.remove_agent(agent_id)
                
                time.sleep(0.1)  # Small delay between tests
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Use metrics collector to process response times
            metrics = self.metrics_collector.collect_response_time_metrics(response_times)
            
            # Get target and classify performance
            target = self.metrics_collector.benchmark_targets[BenchmarkType.RESPONSE_TIME]["target"]
            avg_response = metrics.get("average_response_time", float('inf'))
            
            performance_level = self.validation_rules.classify_performance_level(
                avg_response, target, lower_is_better=True
            )
            
            # Generate recommendations
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
                optimization_recommendations=[]
            )
            
            # Generate recommendations using validation rules
            benchmark.optimization_recommendations = self.validation_rules.generate_optimization_recommendations(benchmark)
            
            # Store in metrics collector
            self.metrics_collector.store_benchmark(benchmark)
            
            return benchmark
            
        except Exception as e:
            self.logger.error(f"Response time benchmark failed: {e}")
            return self._create_failed_benchmark(BenchmarkType.RESPONSE_TIME, "Response Time Test")
    
    def _run_throughput_benchmark(self) -> PerformanceBenchmark:
        """Run throughput benchmark using metrics collector"""
        try:
            start_time = datetime.now()
            
            # Test contract creation throughput
            contracts_created = 0
            test_duration = 5.0
            test_start = time.time()
            
            while time.time() - test_start < test_duration:
                contract_id = self.contract_manager.create_contract(
                    f"Throughput Test Contract {contracts_created}",
                    "Contract for throughput testing",
                    ContractPriority.NORMAL,
                    [AgentCapability.TESTING],
                    1,
                )
                
                if contract_id:
                    contracts_created += 1
                
                time.sleep(0.01)  # Small delay to prevent overwhelming
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Use metrics collector to process throughput
            metrics = self.metrics_collector.collect_throughput_metrics(contracts_created, test_duration)
            
            # Get target and classify performance
            target = self.metrics_collector.benchmark_targets[BenchmarkType.THROUGHPUT]["target"]
            throughput = metrics.get("throughput_ops_per_sec", 0)
            
            performance_level = self.validation_rules.classify_performance_level(
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
                optimization_recommendations=[]
            )
            
            # Generate recommendations
            benchmark.optimization_recommendations = self.validation_rules.generate_optimization_recommendations(benchmark)
            
            # Store in metrics collector
            self.metrics_collector.store_benchmark(benchmark)
            
            return benchmark
            
        except Exception as e:
            self.logger.error(f"Throughput benchmark failed: {e}")
            return self._create_failed_benchmark(BenchmarkType.THROUGHPUT, "Throughput Test")
    
    def _run_scalability_benchmark(self) -> PerformanceBenchmark:
        """Run scalability benchmark using metrics collector"""
        try:
            start_time = datetime.now()
            
            # Test system performance with increasing load
            scalability_results = []
            
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
                
                scalability_results.append({
                    "concurrent_agents": concurrent_count,
                    "operation_time": operation_time,
                    "operations_per_second": concurrent_count / operation_time if operation_time > 0 else 0,
                })
                
                # Cleanup
                for agent_id in agent_ids:
                    self.agent_manager.remove_agent(agent_id)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Use metrics collector to process scalability
            metrics = self.metrics_collector.collect_scalability_metrics(scalability_results)
            
            # Get target and classify performance
            target = self.metrics_collector.benchmark_targets[BenchmarkType.SCALABILITY]["target"]
            scalability_score = metrics.get("scalability_score", 0)
            
            performance_level = self.validation_rules.classify_performance_level(
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
                optimization_recommendations=[]
            )
            
            # Generate recommendations
            benchmark.optimization_recommendations = self.validation_rules.generate_optimization_recommendations(benchmark)
            
            # Store in metrics collector
            self.metrics_collector.store_benchmark(benchmark)
            
            return benchmark
            
        except Exception as e:
            self.logger.error(f"Scalability benchmark failed: {e}")
            return self._create_failed_benchmark(BenchmarkType.SCALABILITY, "Scalability Test")
    
    def _run_reliability_benchmark(self) -> PerformanceBenchmark:
        """Run reliability benchmark using metrics collector"""
        try:
            start_time = datetime.now()
            
            # Test system reliability under stress
            total_operations = 100
            failed_operations = 0
            
            for i in range(total_operations):
                try:
                    # Attempt agent registration and removal
                    agent_id = f"reliability_agent_{i}"
                    success = self.agent_manager.register_agent(
                        agent_id, f"Reliability Agent {i}", [AgentCapability.TESTING]
                    )
                    
                    if success:
                        # Try to update status
                        self.agent_manager.update_agent_status(agent_id, AgentStatus.BUSY)
                        self.agent_manager.remove_agent(agent_id)
                    else:
                        failed_operations += 1
                        
                except Exception:
                    failed_operations += 1
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Use metrics collector to process reliability
            metrics = self.metrics_collector.collect_reliability_metrics(
                total_operations, failed_operations, duration
            )
            
            # Get target and classify performance
            target = self.metrics_collector.benchmark_targets[BenchmarkType.RELIABILITY]["target"]
            success_rate = metrics.get("success_rate_percent", 0)
            
            performance_level = self.validation_rules.classify_performance_level(
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
                optimization_recommendations=[]
            )
            
            # Generate recommendations
            benchmark.optimization_recommendations = self.validation_rules.generate_optimization_recommendations(benchmark)
            
            # Store in metrics collector
            self.metrics_collector.store_benchmark(benchmark)
            
            return benchmark
            
        except Exception as e:
            self.logger.error(f"Reliability benchmark failed: {e}")
            return self._create_failed_benchmark(BenchmarkType.RELIABILITY, "Reliability Test")
    
    def _run_latency_benchmark(self) -> PerformanceBenchmark:
        """Run latency benchmark using metrics collector"""
        try:
            start_time = datetime.now()
            
            # Test system latency
            latency_times = []
            
            for i in range(20):
                latency_start = time.time()
                
                # Simulate a quick operation
                agent_info = self.agent_manager.get_agent_info(f"test_agent_{i}")
                
                latency_end = time.time()
                latency_ms = (latency_end - latency_start) * 1000
                latency_times.append(latency_ms)
                
                time.sleep(0.05)  # Small delay between tests
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Use metrics collector to process latency
            metrics = self.metrics_collector.collect_latency_metrics(latency_times)
            
            # Get target and classify performance
            target = self.metrics_collector.benchmark_targets[BenchmarkType.LATENCY]["target"]
            avg_latency = metrics.get("average_latency", float('inf'))
            
            performance_level = self.validation_rules.classify_performance_level(
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
                optimization_recommendations=[]
            )
            
            # Generate recommendations
            benchmark.optimization_recommendations = self.validation_rules.generate_optimization_recommendations(benchmark)
            
            # Store in metrics collector
            self.metrics_collector.store_benchmark(benchmark)
            
            return benchmark
            
        except Exception as e:
            self.logger.error(f"Latency benchmark failed: {e}")
            return self._create_failed_benchmark(BenchmarkType.LATENCY, "Latency Test")
    
    def _create_failed_benchmark(self, benchmark_type: BenchmarkType, test_name: str) -> PerformanceBenchmark:
        """Create a failed benchmark result"""
        return PerformanceBenchmark(
            benchmark_id=str(uuid.uuid4()),
            benchmark_type=benchmark_type,
            test_name=test_name,
            start_time=datetime.now().isoformat(),
            end_time=datetime.now().isoformat(),
            duration=0.0,
            metrics={},
            target_metrics={},
            performance_level=PerformanceLevel.NOT_READY,
            optimization_recommendations=["Benchmark execution failed - investigate system issues"]
        )
    
    def get_latest_performance_report(self) -> Optional[SystemPerformanceReport]:
        """Get the latest performance report"""
        return self.report_generator.get_latest_report()
    
    def get_benchmark_summary(self) -> Dict[str, Any]:
        """Get summary of all benchmarks"""
        return self.metrics_collector.get_benchmark_summary()
    
    def get_active_alerts(self) -> List:
        """Get active performance alerts"""
        return self.alert_manager.get_active_alerts()
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of performance alerts"""
        return self.alert_manager.get_alert_summary()
    
    def _setup_alert_handlers(self) -> None:
        """Setup alert handlers for different severity levels"""
        def critical_alert_handler(alert):
            self.logger.critical(f"CRITICAL ALERT: {alert.title} - {alert.message}")
        
        def high_alert_handler(alert):
            self.logger.error(f"HIGH ALERT: {alert.title} - {alert.message}")
        
        def medium_alert_handler(alert):
            self.logger.warning(f"MEDIUM ALERT: {alert.title} - {alert.message}")
        
        def low_alert_handler(alert):
            self.logger.info(f"LOW ALERT: {alert.title} - {alert.message}")
        
        # Register alert handlers
        self.alert_manager.register_alert_handler(AlertSeverity.CRITICAL, critical_alert_handler)
        self.alert_manager.register_alert_handler(AlertSeverity.HIGH, high_alert_handler)
        self.alert_manager.register_alert_handler(AlertSeverity.MEDIUM, medium_alert_handler)
        self.alert_manager.register_alert_handler(AlertSeverity.LOW, low_alert_handler)
    
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


# Standalone functions for CLI usage
def run_smoke_test():
    """Run basic functionality test for PerformanceValidationSystem"""
    try:
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
        
        # Run smoke test
        success = perf_system.run_smoke_test()
        
        if success:
            logger.info("✅ PerformanceValidationSystem Smoke Test PASSED")
        else:
            logger.error("❌ PerformanceValidationSystem Smoke Test FAILED")
        
        return success
        
    except Exception as e:
        logger.error(f"❌ PerformanceValidationSystem Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for PerformanceValidationSystem testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Performance Validation System CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--benchmark", action="store_true", help="Run comprehensive benchmark")
    parser.add_argument("--summary", action="store_true", help="Show benchmark summary")
    parser.add_argument("--report", action="store_true", help="Show latest performance report")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    # Initialize managers for other operations
    config_manager = ConfigManager()
    agent_manager = AgentManager()
    contract_manager = ContractManager(agent_manager, config_manager)
    
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
        print(f"Benchmark completed: {benchmark_id}")
    
    if args.summary:
        summary = perf_system.get_benchmark_summary()
        print("Benchmark Summary:")
        print(json.dumps(summary, indent=2))
    
    if args.report:
        report = perf_system.get_latest_performance_report()
        if report:
            formatted_report = perf_system.report_generator.format_report_as_text(report)
            print(formatted_report)
        else:
            print("No performance reports available")


if __name__ == "__main__":
    main()
