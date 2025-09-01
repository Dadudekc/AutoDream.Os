#!/usr/bin/env python3
"""
Gaming Performance Integration - Agent Cellphone V2
================================================

Advanced performance integration system for gaming components.
Provides comprehensive performance validation, benchmarking, and monitoring
for gaming infrastructure components with specialized thresholds and metrics.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import asyncio
import time
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import os
import statistics

from .validation_models import ValidationIssue, ValidationSeverity
from .gaming_performance_validator import GamingPerformanceValidator, GamingPerformanceMetrics


class PerformanceTestType(Enum):
    """Types of performance tests."""
    LOAD_TEST = "load_test"
    STRESS_TEST = "stress_test"
    ENDURANCE_TEST = "endurance_test"
    SPIKE_TEST = "spike_test"
    VOLUME_TEST = "volume_test"


@dataclass
class GamingComponentProfile:
    """Gaming component performance profile."""
    component_name: str
    component_type: str
    file_path: str
    performance_thresholds: Dict[str, float]
    baseline_metrics: Dict[str, float] = field(default_factory=dict)
    current_metrics: Dict[str, float] = field(default_factory=dict)
    performance_score: float = 0.0
    compliance_status: str = "pending"
    last_validated: Optional[datetime] = None


@dataclass
class PerformanceTestResult:
    """Performance test execution result."""
    test_type: PerformanceTestType
    component_name: str
    execution_time: float
    metrics: Dict[str, Any]
    threshold_compliance: Dict[str, bool]
    performance_score: float
    recommendations: List[str]
    timestamp: datetime


class GamingPerformanceIntegration:
    """
    Advanced gaming performance integration system.
    
    Provides comprehensive performance capabilities for:
    - Multi-metric benchmarking and validation
    - Statistical analysis and regression detection
    - Automated reporting and threshold validation
    - Custom performance thresholds for gaming components
    - Real-time metrics collection and monitoring
    """

    def __init__(self, monitoring_interval: float = 1.0):
        """Initialize the gaming performance integration system."""
        self.validator = GamingPerformanceValidator()
        self.monitoring_interval = monitoring_interval
        self.component_profiles: Dict[str, GamingComponentProfile] = {}
        self.performance_history: List[PerformanceTestResult] = []
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        
        # Performance test configurations
        self.test_configurations = {
            PerformanceTestType.LOAD_TEST: {
                "duration_seconds": 60,
                "concurrent_operations": 10,
                "operation_interval": 0.1
            },
            PerformanceTestType.STRESS_TEST: {
                "duration_seconds": 30,
                "concurrent_operations": 50,
                "operation_interval": 0.05
            },
            PerformanceTestType.ENDURANCE_TEST: {
                "duration_seconds": 300,
                "concurrent_operations": 5,
                "operation_interval": 1.0
            },
            PerformanceTestType.SPIKE_TEST: {
                "duration_seconds": 10,
                "concurrent_operations": 100,
                "operation_interval": 0.01
            },
            PerformanceTestType.VOLUME_TEST: {
                "duration_seconds": 120,
                "concurrent_operations": 20,
                "operation_interval": 0.2
            }
        }

    def register_gaming_component(
        self,
        component_name: str,
        component_type: str,
        file_path: str,
        custom_thresholds: Optional[Dict[str, float]] = None
    ) -> None:
        """
        Register a gaming component for performance monitoring.
        
        Args:
            component_name: Name of the gaming component
            component_type: Type of component (Integration Core, Alert Manager, Test Runner, Infrastructure)
            file_path: Path to the component file
            custom_thresholds: Custom performance thresholds (optional)
        """
        # Get default thresholds based on component type
        default_thresholds = self.validator.get_component_thresholds(component_type)
        thresholds = custom_thresholds or default_thresholds
        
        self.component_profiles[component_name] = GamingComponentProfile(
            component_name=component_name,
            component_type=component_type,
            file_path=file_path,
            performance_thresholds=thresholds
        )
        
        print(f"Gaming component '{component_name}' registered for performance monitoring")

    async def execute_comprehensive_performance_validation(
        self,
        component_names: List[str],
        test_types: List[PerformanceTestType] = None
    ) -> Dict[str, Any]:
        """
        Execute comprehensive performance validation for gaming components.
        
        Args:
            component_names: List of component names to validate
            test_types: List of test types to execute (default: all types)
            
        Returns:
            Comprehensive performance validation results
        """
        if test_types is None:
            test_types = list(PerformanceTestType)
        
        start_time = time.time()
        validation_results = {
            "timestamp": datetime.now().isoformat(),
            "components_tested": len(component_names),
            "test_types_executed": [t.value for t in test_types],
            "component_results": {},
            "overall_performance_score": 0.0,
            "threshold_compliance": {},
            "recommendations": [],
            "summary": {}
        }
        
        try:
            # Execute performance tests for each component
            for component_name in component_names:
                if component_name in self.component_profiles:
                    component_results = await self._execute_component_performance_tests(
                        component_name, test_types
                    )
                    validation_results["component_results"][component_name] = component_results
            
            # Calculate overall performance metrics
            validation_results["overall_performance_score"] = self._calculate_overall_performance_score()
            validation_results["threshold_compliance"] = self._calculate_threshold_compliance()
            validation_results["recommendations"] = self._generate_performance_recommendations()
            validation_results["summary"] = self._generate_performance_summary()
            
        except Exception as e:
            validation_results["error"] = f"Performance validation failed: {str(e)}"
        
        end_time = time.time()
        validation_results["total_execution_time_ms"] = (end_time - start_time) * 1000
        
        return validation_results

    async def _execute_component_performance_tests(
        self,
        component_name: str,
        test_types: List[PerformanceTestType]
    ) -> Dict[str, Any]:
        """Execute performance tests for a specific component."""
        component_profile = self.component_profiles[component_name]
        component_results = {
            "component_name": component_name,
            "component_type": component_profile.component_type,
            "test_results": {},
            "performance_score": 0.0,
            "threshold_compliance": {},
            "baseline_comparison": {},
            "recommendations": []
        }
        
        # Execute each test type
        for test_type in test_types:
            test_result = await self._execute_performance_test(component_name, test_type)
            component_results["test_results"][test_type.value] = test_result
            self.performance_history.append(test_result)
        
        # Calculate component performance score
        component_results["performance_score"] = self._calculate_component_performance_score(component_name)
        
        # Check threshold compliance
        component_results["threshold_compliance"] = self._check_component_threshold_compliance(component_name)
        
        # Generate baseline comparison
        component_results["baseline_comparison"] = self._compare_with_baseline(component_name)
        
        # Generate recommendations
        component_results["recommendations"] = self._generate_component_recommendations(component_name)
        
        return component_results

    async def _execute_performance_test(
        self,
        component_name: str,
        test_type: PerformanceTestType
    ) -> PerformanceTestResult:
        """Execute a specific performance test for a component."""
        component_profile = self.component_profiles[component_name]
        test_config = self.test_configurations[test_type]
        
        start_time = time.time()
        
        # Initialize metrics collection
        metrics_collector = self._initialize_metrics_collector()
        
        # Execute performance test based on type
        if test_type == PerformanceTestType.LOAD_TEST:
            metrics = await self._execute_load_test(component_name, test_config, metrics_collector)
        elif test_type == PerformanceTestType.STRESS_TEST:
            metrics = await self._execute_stress_test(component_name, test_config, metrics_collector)
        elif test_type == PerformanceTestType.ENDURANCE_TEST:
            metrics = await self._execute_endurance_test(component_name, test_config, metrics_collector)
        elif test_type == PerformanceTestType.SPIKE_TEST:
            metrics = await self._execute_spike_test(component_name, test_config, metrics_collector)
        elif test_type == PerformanceTestType.VOLUME_TEST:
            metrics = await self._execute_volume_test(component_name, test_config, metrics_collector)
        else:
            metrics = {}
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Check threshold compliance
        threshold_compliance = self._check_metrics_threshold_compliance(component_name, metrics)
        
        # Calculate performance score
        performance_score = self._calculate_test_performance_score(metrics, threshold_compliance)
        
        # Generate recommendations
        recommendations = self._generate_test_recommendations(metrics, threshold_compliance, test_type)
        
        return PerformanceTestResult(
            test_type=test_type,
            component_name=component_name,
            execution_time=execution_time,
            metrics=metrics,
            threshold_compliance=threshold_compliance,
            performance_score=performance_score,
            recommendations=recommendations,
            timestamp=datetime.now()
        )

    def _initialize_metrics_collector(self) -> Dict[str, Any]:
        """Initialize metrics collection system."""
        return {
            "response_times": [],
            "throughput_measurements": [],
            "memory_usage": [],
            "cpu_usage": [],
            "error_count": 0,
            "operation_count": 0,
            "start_time": time.time()
        }

    async def _execute_load_test(
        self,
        component_name: str,
        test_config: Dict[str, Any],
        metrics_collector: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute load test for gaming component."""
        duration = test_config["duration_seconds"]
        concurrent_ops = test_config["concurrent_operations"]
        interval = test_config["operation_interval"]
        
        end_time = time.time() + duration
        tasks = []
        
        while time.time() < end_time:
            # Create concurrent operations
            for _ in range(concurrent_ops):
                task = asyncio.create_task(self._simulate_gaming_operation(component_name, metrics_collector))
                tasks.append(task)
            
            # Wait for interval before next batch
            await asyncio.sleep(interval)
        
        # Wait for all tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return self._finalize_metrics(metrics_collector)

    async def _execute_stress_test(
        self,
        component_name: str,
        test_config: Dict[str, Any],
        metrics_collector: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute stress test for gaming component."""
        duration = test_config["duration_seconds"]
        concurrent_ops = test_config["concurrent_operations"]
        interval = test_config["operation_interval"]
        
        end_time = time.time() + duration
        tasks = []
        
        while time.time() < end_time:
            # Create high-concurrency operations
            for _ in range(concurrent_ops):
                task = asyncio.create_task(self._simulate_stress_operation(component_name, metrics_collector))
                tasks.append(task)
            
            # Shorter interval for stress testing
            await asyncio.sleep(interval)
        
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return self._finalize_metrics(metrics_collector)

    async def _execute_endurance_test(
        self,
        component_name: str,
        test_config: Dict[str, Any],
        metrics_collector: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute endurance test for gaming component."""
        duration = test_config["duration_seconds"]
        concurrent_ops = test_config["concurrent_operations"]
        interval = test_config["operation_interval"]
        
        end_time = time.time() + duration
        tasks = []
        
        while time.time() < end_time:
            # Create sustained operations
            for _ in range(concurrent_ops):
                task = asyncio.create_task(self._simulate_endurance_operation(component_name, metrics_collector))
                tasks.append(task)
            
            # Longer interval for endurance testing
            await asyncio.sleep(interval)
        
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return self._finalize_metrics(metrics_collector)

    async def _execute_spike_test(
        self,
        component_name: str,
        test_config: Dict[str, Any],
        metrics_collector: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute spike test for gaming component."""
        duration = test_config["duration_seconds"]
        concurrent_ops = test_config["concurrent_operations"]
        interval = test_config["operation_interval"]
        
        end_time = time.time() + duration
        tasks = []
        
        while time.time() < end_time:
            # Create spike operations
            for _ in range(concurrent_ops):
                task = asyncio.create_task(self._simulate_spike_operation(component_name, metrics_collector))
                tasks.append(task)
            
            # Very short interval for spike testing
            await asyncio.sleep(interval)
        
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return self._finalize_metrics(metrics_collector)

    async def _execute_volume_test(
        self,
        component_name: str,
        test_config: Dict[str, Any],
        metrics_collector: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute volume test for gaming component."""
        duration = test_config["duration_seconds"]
        concurrent_ops = test_config["concurrent_operations"]
        interval = test_config["operation_interval"]
        
        end_time = time.time() + duration
        tasks = []
        
        while time.time() < end_time:
            # Create volume operations
            for _ in range(concurrent_ops):
                task = asyncio.create_task(self._simulate_volume_operation(component_name, metrics_collector))
                tasks.append(task)
            
            # Medium interval for volume testing
            await asyncio.sleep(interval)
        
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return self._finalize_metrics(metrics_collector)

    async def _simulate_gaming_operation(
        self,
        component_name: str,
        metrics_collector: Dict[str, Any]
    ) -> None:
        """Simulate a gaming operation for performance testing."""
        start_time = time.time()
        
        try:
            # Simulate gaming operation based on component type
            component_profile = self.component_profiles[component_name]
            
            if component_profile.component_type == "Integration Core":
                await self._simulate_integration_core_operation()
            elif component_profile.component_type == "Alert Manager":
                await self._simulate_alert_manager_operation()
            elif component_profile.component_type == "Test Runner":
                await self._simulate_test_runner_operation()
            elif component_profile.component_type == "Infrastructure":
                await self._simulate_infrastructure_operation()
            
            # Record successful operation
            response_time = (time.time() - start_time) * 1000
            metrics_collector["response_times"].append(response_time)
            metrics_collector["operation_count"] += 1
            
        except Exception as e:
            # Record error
            metrics_collector["error_count"] += 1
            print(f"Gaming operation error in {component_name}: {str(e)}")

    async def _simulate_stress_operation(
        self,
        component_name: str,
        metrics_collector: Dict[str, Any]
    ) -> None:
        """Simulate a stress operation for performance testing."""
        await self._simulate_gaming_operation(component_name, metrics_collector)
        # Add additional stress simulation
        await asyncio.sleep(0.001)  # Minimal delay to simulate stress

    async def _simulate_endurance_operation(
        self,
        component_name: str,
        metrics_collector: Dict[str, Any]
    ) -> None:
        """Simulate an endurance operation for performance testing."""
        await self._simulate_gaming_operation(component_name, metrics_collector)
        # Add endurance-specific simulation
        await asyncio.sleep(0.1)  # Longer delay for endurance testing

    async def _simulate_spike_operation(
        self,
        component_name: str,
        metrics_collector: Dict[str, Any]
    ) -> None:
        """Simulate a spike operation for performance testing."""
        await self._simulate_gaming_operation(component_name, metrics_collector)
        # Add spike-specific simulation
        await asyncio.sleep(0.0001)  # Very short delay for spike testing

    async def _simulate_volume_operation(
        self,
        component_name: str,
        metrics_collector: Dict[str, Any]
    ) -> None:
        """Simulate a volume operation for performance testing."""
        await self._simulate_gaming_operation(component_name, metrics_collector)
        # Add volume-specific simulation
        await asyncio.sleep(0.05)  # Medium delay for volume testing

    async def _simulate_integration_core_operation(self) -> None:
        """Simulate Integration Core operation."""
        # Simulate gaming integration core processing
        await asyncio.sleep(0.01)  # 10ms simulation

    async def _simulate_alert_manager_operation(self) -> None:
        """Simulate Alert Manager operation."""
        # Simulate gaming alert management
        await asyncio.sleep(0.05)  # 50ms simulation

    async def _simulate_test_runner_operation(self) -> None:
        """Simulate Test Runner operation."""
        # Simulate gaming test execution
        await asyncio.sleep(0.1)  # 100ms simulation

    async def _simulate_infrastructure_operation(self) -> None:
        """Simulate Infrastructure operation."""
        # Simulate gaming infrastructure management
        await asyncio.sleep(0.2)  # 200ms simulation

    def _finalize_metrics(self, metrics_collector: Dict[str, Any]) -> Dict[str, Any]:
        """Finalize and calculate metrics from collector."""
        total_time = time.time() - metrics_collector["start_time"]
        
        # Calculate response time statistics
        response_times = metrics_collector["response_times"]
        avg_response_time = statistics.mean(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        
        # Calculate throughput
        throughput = metrics_collector["operation_count"] / total_time if total_time > 0 else 0
        
        # Calculate error rate
        error_rate = (metrics_collector["error_count"] / metrics_collector["operation_count"] * 100) if metrics_collector["operation_count"] > 0 else 0
        
        # Get system metrics
        memory_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent()
        
        return {
            "avg_response_time_ms": avg_response_time,
            "min_response_time_ms": min_response_time,
            "max_response_time_ms": max_response_time,
            "throughput_ops_per_sec": throughput,
            "error_rate_percent": error_rate,
            "memory_usage_percent": memory_usage,
            "cpu_usage_percent": cpu_usage,
            "total_operations": metrics_collector["operation_count"],
            "total_errors": metrics_collector["error_count"],
            "test_duration_seconds": total_time
        }

    def _check_metrics_threshold_compliance(
        self,
        component_name: str,
        metrics: Dict[str, Any]
    ) -> Dict[str, bool]:
        """Check metrics against component thresholds."""
        component_profile = self.component_profiles[component_name]
        thresholds = component_profile.performance_thresholds
        compliance = {}
        
        # Check response time compliance
        if "max_response_time_ms" in thresholds:
            compliance["response_time"] = metrics["avg_response_time_ms"] <= thresholds["max_response_time_ms"]
        
        # Check throughput compliance
        if "min_throughput_ops_per_sec" in thresholds:
            compliance["throughput"] = metrics["throughput_ops_per_sec"] >= thresholds["min_throughput_ops_per_sec"]
        
        # Check error rate compliance
        if "max_error_rate_percent" in thresholds:
            compliance["error_rate"] = metrics["error_rate_percent"] <= thresholds["max_error_rate_percent"]
        
        # Check memory usage compliance
        if "max_memory_usage_percent" in thresholds:
            compliance["memory_usage"] = metrics["memory_usage_percent"] <= thresholds["max_memory_usage_percent"]
        
        # Check CPU usage compliance
        if "max_cpu_usage_percent" in thresholds:
            compliance["cpu_usage"] = metrics["cpu_usage_percent"] <= thresholds["max_cpu_usage_percent"]
        
        return compliance

    def _calculate_test_performance_score(
        self,
        metrics: Dict[str, Any],
        threshold_compliance: Dict[str, bool]
    ) -> float:
        """Calculate performance score for a test result."""
        score = 0.0
        total_checks = len(threshold_compliance)
        
        if total_checks == 0:
            return 100.0
        
        # Base score from threshold compliance
        passed_checks = sum(1 for passed in threshold_compliance.values() if passed)
        compliance_score = (passed_checks / total_checks) * 60  # 60% weight for compliance
        
        # Performance bonus (40% weight)
        performance_bonus = 0.0
        
        # Response time bonus
        if metrics["avg_response_time_ms"] < 10:
            performance_bonus += 10
        elif metrics["avg_response_time_ms"] < 50:
            performance_bonus += 5
        
        # Throughput bonus
        if metrics["throughput_ops_per_sec"] > 1000:
            performance_bonus += 10
        elif metrics["throughput_ops_per_sec"] > 500:
            performance_bonus += 5
        
        # Error rate bonus
        if metrics["error_rate_percent"] == 0:
            performance_bonus += 10
        elif metrics["error_rate_percent"] < 1:
            performance_bonus += 5
        
        # Memory efficiency bonus
        if metrics["memory_usage_percent"] < 50:
            performance_bonus += 10
        elif metrics["memory_usage_percent"] < 80:
            performance_bonus += 5
        
        # CPU efficiency bonus
        if metrics["cpu_usage_percent"] < 50:
            performance_bonus += 10
        elif metrics["cpu_usage_percent"] < 80:
            performance_bonus += 5
        
        return min(100.0, compliance_score + performance_bonus)

    def _generate_test_recommendations(
        self,
        metrics: Dict[str, Any],
        threshold_compliance: Dict[str, bool],
        test_type: PerformanceTestType
    ) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        # Response time recommendations
        if not threshold_compliance.get("response_time", True):
            recommendations.append(f"Optimize response time: {metrics['avg_response_time_ms']:.2f}ms exceeds threshold")
        
        # Throughput recommendations
        if not threshold_compliance.get("throughput", True):
            recommendations.append(f"Improve throughput: {metrics['throughput_ops_per_sec']:.2f} ops/sec below threshold")
        
        # Error rate recommendations
        if not threshold_compliance.get("error_rate", True):
            recommendations.append(f"Reduce error rate: {metrics['error_rate_percent']:.2f}% exceeds threshold")
        
        # Memory usage recommendations
        if not threshold_compliance.get("memory_usage", True):
            recommendations.append(f"Optimize memory usage: {metrics['memory_usage_percent']:.2f}% exceeds threshold")
        
        # CPU usage recommendations
        if not threshold_compliance.get("cpu_usage", True):
            recommendations.append(f"Optimize CPU usage: {metrics['cpu_usage_percent']:.2f}% exceeds threshold")
        
        # Test-specific recommendations
        if test_type == PerformanceTestType.STRESS_TEST:
            if metrics["error_rate_percent"] > 5:
                recommendations.append("Component shows instability under stress - consider load balancing")
        
        elif test_type == PerformanceTestType.ENDURANCE_TEST:
            if metrics["memory_usage_percent"] > 80:
                recommendations.append("Memory usage increases over time - check for memory leaks")
        
        elif test_type == PerformanceTestType.SPIKE_TEST:
            if metrics["avg_response_time_ms"] > 100:
                recommendations.append("Component struggles with traffic spikes - implement caching")
        
        return recommendations

    def _calculate_component_performance_score(self, component_name: str) -> float:
        """Calculate overall performance score for a component."""
        component_tests = [result for result in self.performance_history 
                          if result.component_name == component_name]
        
        if not component_tests:
            return 0.0
        
        scores = [test.performance_score for test in component_tests]
        return statistics.mean(scores)

    def _check_component_threshold_compliance(self, component_name: str) -> Dict[str, bool]:
        """Check overall threshold compliance for a component."""
        component_tests = [result for result in self.performance_history 
                          if result.component_name == component_name]
        
        if not component_tests:
            return {}
        
        # Aggregate compliance across all tests
        all_compliance = {}
        for test in component_tests:
            for metric, compliant in test.threshold_compliance.items():
                if metric not in all_compliance:
                    all_compliance[metric] = []
                all_compliance[metric].append(compliant)
        
        # Calculate overall compliance (all tests must pass)
        overall_compliance = {}
        for metric, compliance_list in all_compliance.items():
            overall_compliance[metric] = all(compliance_list)
        
        return overall_compliance

    def _compare_with_baseline(self, component_name: str) -> Dict[str, Any]:
        """Compare current performance with baseline metrics."""
        component_profile = self.component_profiles[component_name]
        baseline = component_profile.baseline_metrics
        
        if not baseline:
            return {"status": "no_baseline", "message": "No baseline metrics available"}
        
        component_tests = [result for result in self.performance_history 
                          if result.component_name == component_name]
        
        if not component_tests:
            return {"status": "no_tests", "message": "No test results available"}
        
        # Calculate average current metrics
        current_metrics = {}
        for test in component_tests:
            for metric, value in test.metrics.items():
                if metric not in current_metrics:
                    current_metrics[metric] = []
                current_metrics[metric].append(value)
        
        # Calculate averages
        avg_current = {}
        for metric, values in current_metrics.items():
            avg_current[metric] = statistics.mean(values)
        
        # Compare with baseline
        comparison = {}
        for metric in baseline:
            if metric in avg_current:
                baseline_value = baseline[metric]
                current_value = avg_current[metric]
                change_percent = ((current_value - baseline_value) / baseline_value * 100) if baseline_value != 0 else 0
                
                comparison[metric] = {
                    "baseline": baseline_value,
                    "current": current_value,
                    "change_percent": change_percent,
                    "improved": change_percent < 0 if "time" in metric.lower() or "usage" in metric.lower() else change_percent > 0
                }
        
        return comparison

    def _generate_component_recommendations(self, component_name: str) -> List[str]:
        """Generate recommendations for a specific component."""
        recommendations = []
        component_profile = self.component_profiles[component_name]
        
        # Get latest test results
        component_tests = [result for result in self.performance_history 
                          if result.component_name == component_name]
        
        if not component_tests:
            return ["No performance test results available for recommendations"]
        
        # Aggregate recommendations from all tests
        all_recommendations = []
        for test in component_tests:
            all_recommendations.extend(test.recommendations)
        
        # Remove duplicates and prioritize
        unique_recommendations = list(set(all_recommendations))
        
        # Add component-specific recommendations
        if component_profile.component_type == "Integration Core":
            unique_recommendations.append("Consider implementing connection pooling for better performance")
            unique_recommendations.append("Review gaming API integration patterns for optimization")
        
        elif component_profile.component_type == "Alert Manager":
            unique_recommendations.append("Implement alert batching to reduce processing overhead")
            unique_recommendations.append("Consider using async alert processing for better throughput")
        
        elif component_profile.component_type == "Test Runner":
            unique_recommendations.append("Implement parallel test execution for better performance")
            unique_recommendations.append("Consider test result caching to reduce redundant operations")
        
        elif component_profile.component_type == "Infrastructure":
            unique_recommendations.append("Implement resource monitoring and auto-scaling")
            unique_recommendations.append("Consider infrastructure-as-code for better resource management")
        
        return unique_recommendations[:10]  # Limit to top 10 recommendations

    def _calculate_overall_performance_score(self) -> float:
        """Calculate overall performance score across all components."""
        if not self.performance_history:
            return 0.0
        
        scores = [result.performance_score for result in self.performance_history]
        return statistics.mean(scores)

    def _calculate_threshold_compliance(self) -> Dict[str, Any]:
        """Calculate overall threshold compliance across all components."""
        total_checks = 0
        passed_checks = 0
        
        for result in self.performance_history:
            for metric, compliant in result.threshold_compliance.items():
                total_checks += 1
                if compliant:
                    passed_checks += 1
        
        compliance_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        return {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "compliance_rate_percent": compliance_rate
        }

    def _generate_performance_recommendations(self) -> List[str]:
        """Generate overall performance recommendations."""
        recommendations = []
        
        # Check overall performance score
        overall_score = self._calculate_overall_performance_score()
        if overall_score < 80:
            recommendations.append("Overall performance score below 80% - focus on critical performance issues")
        
        # Check threshold compliance
        compliance = self._calculate_threshold_compliance()
        if compliance["compliance_rate_percent"] < 90:
            recommendations.append("Threshold compliance below 90% - address failing performance thresholds")
        
        # Component-specific recommendations
        for component_name in self.component_profiles:
            component_recommendations = self._generate_component_recommendations(component_name)
            recommendations.extend(component_recommendations[:3])  # Top 3 per component
        
        # General recommendations
        recommendations.append("Implement continuous performance monitoring")
        recommendations.append("Establish performance baselines and regression detection")
        recommendations.append("Regular performance testing in CI/CD pipeline")
        
        return list(set(recommendations))[:15]  # Limit to top 15 unique recommendations

    def _generate_performance_summary(self) -> Dict[str, Any]:
        """Generate comprehensive performance summary."""
        total_components = len(self.component_profiles)
        tested_components = len(set(result.component_name for result in self.performance_history))
        total_tests = len(self.performance_history)
        
        # Calculate average metrics across all tests
        all_metrics = {}
        for result in self.performance_history:
            for metric, value in result.metrics.items():
                if metric not in all_metrics:
                    all_metrics[metric] = []
                all_metrics[metric].append(value)
        
        avg_metrics = {}
        for metric, values in all_metrics.items():
            avg_metrics[metric] = statistics.mean(values)
        
        return {
            "total_components": total_components,
            "tested_components": tested_components,
            "total_tests_executed": total_tests,
            "overall_performance_score": self._calculate_overall_performance_score(),
            "threshold_compliance": self._calculate_threshold_compliance(),
            "average_metrics": avg_metrics,
            "test_coverage_percent": (tested_components / total_components * 100) if total_components > 0 else 0
        }

    def start_real_time_monitoring(self) -> None:
        """Start real-time performance monitoring."""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        print("Real-time performance monitoring started")

    def stop_real_time_monitoring(self) -> None:
        """Stop real-time performance monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        print("Real-time performance monitoring stopped")

    def _monitoring_loop(self) -> None:
        """Real-time monitoring loop."""
        while self.monitoring_active:
            try:
                # Collect real-time metrics for all components
                for component_name in self.component_profiles:
                    self._collect_real_time_metrics(component_name)
                
                time.sleep(self.monitoring_interval)
            except Exception as e:
                print(f"Monitoring loop error: {str(e)}")
                time.sleep(self.monitoring_interval)

    def _collect_real_time_metrics(self, component_name: str) -> None:
        """Collect real-time metrics for a component."""
        try:
            # Get current system metrics
            memory_usage = psutil.virtual_memory().percent
            cpu_usage = psutil.cpu_percent()
            
            # Update component profile with current metrics
            component_profile = self.component_profiles[component_name]
            component_profile.current_metrics = {
                "memory_usage_percent": memory_usage,
                "cpu_usage_percent": cpu_usage,
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            print(f"Error collecting real-time metrics for {component_name}: {str(e)}")

    def get_performance_integration_summary(self) -> str:
        """Get human-readable performance integration summary."""
        summary = f"Gaming Performance Integration Summary:\n"
        summary += f"Components Registered: {len(self.component_profiles)}\n"
        summary += f"Performance Tests Executed: {len(self.performance_history)}\n"
        summary += f"Overall Performance Score: {self._calculate_overall_performance_score():.1f}/100\n"
        
        compliance = self._calculate_threshold_compliance()
        summary += f"Threshold Compliance: {compliance['compliance_rate_percent']:.1f}%\n"
        summary += f"Real-time Monitoring: {'Active' if self.monitoring_active else 'Inactive'}\n"
        
        # Component breakdown
        for component_name, profile in self.component_profiles.items():
            component_score = self._calculate_component_performance_score(component_name)
            summary += f"  {component_name}: {component_score:.1f}/100\n"
        
        return summary
