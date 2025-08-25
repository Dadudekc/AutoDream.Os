#!/usr/bin/env python3
"""
Performance Core - Unified Performance Validation Logic
======================================================

Core performance validation logic extracted and consolidated from multiple files.
Follows Single Responsibility Principle with focused validation functionality.

Author: Performance Validation Consolidation Team
License: MIT
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# from src.utils.stability_improvements import stability_manager, safe_import

# Import required dependencies
try:
    from ..agent_manager import AgentManager, AgentStatus, AgentCapability, AgentInfo
    from ..config_manager import ConfigManager
    from ..assignment_engine import ContractManager
    from ..workflow import (
        WorkflowOrchestrator as AdvancedWorkflowEngine,
        WorkflowType,
        TaskPriority as WorkflowPriority,
        WorkflowTask as WorkflowStep,
    )
except ImportError:
    # Fallback imports for standalone testing
    # Mock classes for standalone testing
    class AgentManager:
        pass
    
    class AgentStatus:
        pass
    
    class AgentCapability:
        pass
    
    class AgentInfo:
        pass
    
    class ConfigManager:
        pass
    
    class ContractManager:
        pass
    
    class AdvancedWorkflowEngine:
        pass
    
    class WorkflowType:
        pass
    
    class WorkflowPriority:
        pass
    
    class WorkflowStep:
        pass


@dataclass
class BenchmarkResult:
    """Standardized benchmark result structure."""
    benchmark_id: str
    benchmark_type: str
    start_time: datetime
    end_time: datetime
    duration: float
    metrics: Dict[str, Any]
    validation_result: Dict[str, Any]
    performance_level: str
    optimization_recommendations: List[str]


@dataclass
class ValidationRule:
    """Performance validation rule definition."""
    rule_name: str
    metric_name: str
    threshold: float
    operator: str  # 'gt', 'lt', 'eq', 'gte', 'lte'
    severity: str  # 'critical', 'warning', 'info'
    description: str


class PerformanceValidationCore:
    """
    Core performance validation logic consolidated from multiple files.
    
    Responsibilities:
    - Core validation rule engine
    - Performance metrics calculation
    - Validation result processing
    - Benchmark orchestration logic
    """
    
    def __init__(
        self,
        agent_manager: Optional[AgentManager] = None,
        config_manager: Optional[ConfigManager] = None,
        contract_manager: Optional[ContractManager] = None,
        workflow_engine: Optional[AdvancedWorkflowEngine] = None,
    ):
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.contract_manager = contract_manager
        self.workflow_engine = workflow_engine
        
        self.logger = logging.getLogger(f"{__name__}.PerformanceValidationCore")
        
        # Initialize validation rules
        self._setup_validation_rules()
    
    def _setup_validation_rules(self):
        """Setup default validation rules."""
        self.validation_rules = [
            ValidationRule(
                rule_name="response_time_threshold",
                metric_name="average_response_time",
                threshold=0.5,  # 500ms
                operator="lte",
                severity="critical",
                description="Response time must be under 500ms"
            ),
            ValidationRule(
                rule_name="throughput_minimum",
                metric_name="average_throughput",
                threshold=1000,  # 1000 req/s
                operator="gte",
                severity="warning",
                description="Throughput should be at least 1000 req/s"
            ),
            ValidationRule(
                rule_name="scalability_efficiency",
                metric_name="scalability_factor",
                threshold=0.8,  # 80% efficiency
                operator="gte",
                severity="warning",
                description="Scalability efficiency should be at least 80%"
            ),
            ValidationRule(
                rule_name="reliability_threshold",
                metric_name="success_rate",
                threshold=0.99,  # 99% success rate
                operator="gte",
                severity="critical",
                description="Success rate must be at least 99%"
            )
        ]
    
    def validate_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate performance metrics against defined rules.
        
        Args:
            metrics: Dictionary of performance metrics
            
        Returns:
            Dictionary containing validation results for each rule
        """
        validation_results = {}
        
        for rule in self.validation_rules:
            metric_value = metrics.get(rule.metric_name)
            if metric_value is None:
                validation_results[rule.rule_name] = {
                    "status": "error",
                    "message": f"Metric '{rule.metric_name}' not found",
                    "severity": rule.severity
                }
                continue
            
            # Apply validation rule
            is_valid = self._apply_validation_rule(metric_value, rule)
            
            validation_results[rule.rule_name] = {
                "status": "pass" if is_valid else "fail",
                "metric_value": metric_value,
                "threshold": rule.threshold,
                "operator": rule.operator,
                "severity": rule.severity,
                "description": rule.description,
                "message": f"Metric {rule.metric_name}={metric_value} {'meets' if is_valid else 'fails'} {rule.description}"
            }
        
        return validation_results
    
    def _apply_validation_rule(self, metric_value: float, rule: ValidationRule) -> bool:
        """Apply a single validation rule to a metric value."""
        if rule.operator == "gt":
            return metric_value > rule.threshold
        elif rule.operator == "lt":
            return metric_value < rule.threshold
        elif rule.operator == "eq":
            return abs(metric_value - rule.threshold) < 0.001  # Small tolerance for float comparison
        elif rule.operator == "gte":
            return metric_value >= rule.threshold
        elif rule.operator == "lte":
            return metric_value <= rule.threshold
        else:
            self.logger.warning(f"Unknown operator: {rule.operator}")
            return False
    
    def calculate_performance_level(self, validation_results: Dict[str, Any]) -> str:
        """
        Calculate overall performance level based on validation results.
        
        Args:
            validation_results: Results from validate_metrics()
            
        Returns:
            Performance level: 'excellent', 'good', 'acceptable', 'poor', 'critical'
        """
        critical_failures = 0
        warning_failures = 0
        total_rules = len(validation_results)
        
        for rule_name, result in validation_results.items():
            if result["status"] == "fail":
                if result["severity"] == "critical":
                    critical_failures += 1
                elif result["severity"] == "warning":
                    warning_failures += 1
        
        # Determine performance level
        if critical_failures == 0 and warning_failures == 0:
            return "excellent"
        elif critical_failures == 0 and warning_failures <= 1:
            return "good"
        elif critical_failures == 0 and warning_failures <= 2:
            return "acceptable"
        elif critical_failures == 0:
            return "poor"
        else:
            return "critical"
    
    def generate_optimization_recommendations(
        self, 
        validation_results: Dict[str, Any]
    ) -> List[str]:
        """
        Generate optimization recommendations based on validation failures.
        
        Args:
            validation_results: Results from validate_metrics()
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        for rule_name, result in validation_results.items():
            if result["status"] == "fail":
                if rule_name == "response_time_threshold":
                    recommendations.append(
                        "Optimize database queries and reduce computational complexity"
                    )
                elif rule_name == "throughput_minimum":
                    recommendations.append(
                        "Increase system resources and optimize request processing"
                    )
                elif rule_name == "scalability_efficiency":
                    recommendations.append(
                        "Review load balancing and resource allocation strategies"
                    )
                elif rule_name == "reliability_threshold":
                    recommendations.append(
                        "Implement better error handling and retry mechanisms"
                    )
        
        # Add general recommendations if none specific
        if not recommendations:
            recommendations.append("Performance meets all targets - maintain current configuration")
        
        return recommendations
    
    def create_benchmark_result(
        self,
        benchmark_type: str,
        metrics: Dict[str, Any],
        start_time: datetime,
        end_time: datetime
    ) -> BenchmarkResult:
        """
        Create a standardized benchmark result.
        
        Args:
            benchmark_type: Type of benchmark performed
            metrics: Performance metrics collected
            start_time: Benchmark start time
            end_time: Benchmark end time
            
        Returns:
            Standardized BenchmarkResult object
        """
        duration = (end_time - start_time).total_seconds()
        
        # Validate metrics
        validation_results = self.validate_metrics(metrics)
        
        # Calculate performance level
        performance_level = self.calculate_performance_level(validation_results)
        
        # Generate optimization recommendations
        optimization_recommendations = self.generate_optimization_recommendations(validation_results)
        
        return BenchmarkResult(
            benchmark_id=str(uuid.uuid4()),
            benchmark_type=benchmark_type,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            metrics=metrics,
            validation_result=validation_results,
            performance_level=performance_level,
            optimization_recommendations=optimization_recommendations
        )
    
    def run_smoke_test(self) -> bool:
        """
        Run a basic smoke test to verify the validation system is working.
        
        Returns:
            True if smoke test passes, False otherwise
        """
        try:
            self.logger.info("Running performance validation smoke test")
            
            # Test with sample metrics
            test_metrics = {
                "average_response_time": 0.3,
                "average_throughput": 1200,
                "scalability_factor": 0.85,
                "success_rate": 0.995
            }
            
            # Validate metrics
            validation_results = self.validate_metrics(test_metrics)
            
            # Check if validation passed
            smoke_test_passed = all(
                result["status"] == "pass" 
                for result in validation_results.values()
            )
            
            if smoke_test_passed:
                self.logger.info("Smoke test passed - validation system working correctly")
            else:
                self.logger.warning("Smoke test failed - some validations failed")
            
            return smoke_test_passed
            
        except Exception as e:
            self.logger.error(f"Smoke test failed with error: {e}")
            return False
