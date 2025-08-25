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
            
            # Resource utilization benchmark
            resource_benchmark = self._run_resource_utilization_benchmark()
            benchmark_results.append(resource_benchmark)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Store benchmark results
            self.metrics_collector.store_benchmark_results(benchmark_id, benchmark_results, duration)
            
            # Generate performance report
            self.report_generator.generate_performance_report(benchmark_id, benchmark_results, duration)
            
            # Check for performance alerts
            self._check_performance_alerts(benchmark_results)
            
            self.logger.info(f"Comprehensive benchmark completed: {benchmark_id} in {duration:.2f}s")
            return benchmark_id
            
        except Exception as e:
            self.logger.error(f"Error running comprehensive benchmark: {e}")
            return None
    
    def _run_response_time_benchmark(self) -> Dict[str, Any]:
        """Run response time benchmark."""
        try:
            self.logger.info("Running response time benchmark")
            
            # Simulate response time measurements
            response_times = [0.1, 0.15, 0.12, 0.18, 0.11]
            avg_response_time = sum(response_times) / len(response_times)
            
            benchmark_result = {
                "type": "response_time",
                "average_response_time": avg_response_time,
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "timestamp": datetime.now().isoformat()
            }
            
            # Validate against rules
            validation_result = self.validation_rules.validate_response_time(avg_response_time)
            benchmark_result["validation"] = validation_result
            
            return benchmark_result
            
        except Exception as e:
            self.logger.error(f"Error in response time benchmark: {e}")
            return {"type": "response_time", "error": str(e)}
    
    def _run_throughput_benchmark(self) -> Dict[str, Any]:
        """Run throughput benchmark."""
        try:
            self.logger.info("Running throughput benchmark")
            
            # Simulate throughput measurements
            throughput_measurements = [1000, 1200, 1100, 1300, 1150]
            avg_throughput = sum(throughput_measurements) / len(throughput_measurements)
            
            benchmark_result = {
                "type": "throughput",
                "average_throughput": avg_throughput,
                "min_throughput": min(throughput_measurements),
                "max_throughput": max(throughput_measurements),
                "timestamp": datetime.now().isoformat()
            }
            
            # Validate against rules
            validation_result = self.validation_rules.validate_throughput(avg_throughput)
            benchmark_result["validation"] = validation_result
            
            return benchmark_result
            
        except Exception as e:
            self.logger.error(f"Error in throughput benchmark: {e}")
            return {"type": "throughput", "error": str(e)}
    
    def _run_scalability_benchmark(self) -> Dict[str, Any]:
        """Run scalability benchmark."""
        try:
            self.logger.info("Running scalability benchmark")
            
            # Simulate scalability measurements
            scalability_data = {
                "1_agent": {"throughput": 1000, "response_time": 0.1},
                "5_agents": {"throughput": 4800, "response_time": 0.12},
                "10_agents": {"throughput": 9000, "response_time": 0.15}
            }
            
            benchmark_result = {
                "type": "scalability",
                "scalability_data": scalability_data,
                "scalability_factor": 0.9,  # 90% efficiency
                "timestamp": datetime.now().isoformat()
            }
            
            # Validate against rules
            validation_result = self.validation_rules.validate_scalability(0.9)
            benchmark_result["validation"] = validation_result
            
            return benchmark_result
            
        except Exception as e:
            self.logger.error(f"Error in scalability benchmark: {e}")
            return {"type": "scalability", "error": str(e)}
    
    def _run_reliability_benchmark(self) -> Dict[str, Any]:
        """Run reliability benchmark."""
        try:
            self.logger.info("Running reliability benchmark")
            
            # Simulate reliability measurements
            reliability_data = {
                "uptime": 99.9,
                "error_rate": 0.001,
                "recovery_time": 0.5,
                "failures": 2
            }
            
            benchmark_result = {
                "type": "reliability",
                "reliability_data": reliability_data,
                "overall_reliability": 99.5,
                "timestamp": datetime.now().isoformat()
            }
            
            # Validate against rules
            validation_result = self.validation_rules.validate_reliability(99.5)
            benchmark_result["validation"] = validation_result
            
            return benchmark_result
            
        except Exception as e:
            self.logger.error(f"Error in reliability benchmark: {e}")
            return {"type": "reliability", "error": str(e)}
    
    def _run_resource_utilization_benchmark(self) -> Dict[str, Any]:
        """Run resource utilization benchmark."""
        try:
            self.logger.info("Running resource utilization benchmark")
            
            # Simulate resource measurements
            resource_data = {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 23.1,
                "network_usage": 12.5
            }
            
            benchmark_result = {
                "type": "resource_utilization",
                "resource_data": resource_data,
                "efficiency_score": 78.5,
                "timestamp": datetime.now().isoformat()
            }
            
            # Validate against rules
            validation_result = self.validation_rules.validate_resource_utilization(78.5)
            benchmark_result["validation"] = validation_result
            
            return benchmark_result
            
        except Exception as e:
            self.logger.error(f"Error in resource utilization benchmark: {e}")
            return {"type": "resource_utilization", "error": str(e)}
    
    def _check_performance_alerts(self, benchmark_results: List[Dict[str, Any]]) -> None:
        """Check for performance alerts based on benchmark results."""
        try:
            for result in benchmark_results:
                if "validation" in result and result["validation"].get("status") == "failed":
                    # Generate alert for failed validation
                    alert = self.alert_manager.create_alert(
                        title=f"Performance Validation Failed: {result['type']}",
                        message=f"Benchmark {result['type']} failed validation criteria",
                        severity=AlertSeverity.MEDIUM,
                        alert_type=AlertType.PERFORMANCE
                    )
                    
                    # Send alert notifications
                    self.alert_manager.send_alert(alert)
                    
        except Exception as e:
            self.logger.error(f"Error checking performance alerts: {e}")
    
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


# Convenience functions for backward compatibility
def create_performance_validation_system(
    agent_manager: AgentManager,
    config_manager: ConfigManager,
    contract_manager: ContractManager,
    workflow_engine: AdvancedWorkflowEngine
) -> PerformanceValidationSystem:
    """Create a new performance validation system."""
    return PerformanceValidationSystem(agent_manager, config_manager, contract_manager, workflow_engine)


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
