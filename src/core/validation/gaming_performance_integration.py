#!/usr/bin/env python3
"""
Gaming Performance Integration V2 - Agent Cellphone V2
====================================================

Advanced performance integration system for gaming components.
Refactored for V2 compliance with modular architecture.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import asyncio
import time
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

from .validation_models import ValidationIssue, ValidationSeverity
from .gaming_performance_validator import GamingPerformanceValidator, GamingPerformanceMetrics
from .models.gaming_performance_models import (
    PerformanceTestType, GamingComponentProfile, PerformanceTestResult,
    PerformanceIntegrationConfig, PerformanceMetrics, PerformanceAnalysisResult
)
from .utils.gaming_performance_utils import (
    PerformanceTestConfigurations, PerformanceCalculations,
    PerformanceRecommendations, PerformanceThresholds
)
from .handlers.gaming_performance_handlers import (
    PerformanceTestHandlers, PerformanceMonitoringHandlers, PerformanceAnalysisHandlers
)


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

    def __init__(self, config: Optional[PerformanceIntegrationConfig] = None):
        """Initialize the gaming performance integration system."""
        self.validator = GamingPerformanceValidator()
        self.config = config or PerformanceIntegrationConfig()
        self.component_profiles: Dict[str, GamingComponentProfile] = {}
        self.performance_history: List[PerformanceTestResult] = []
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        
        # Performance test configurations
        self.test_configurations = PerformanceTestConfigurations.get_test_configurations()

    def register_gaming_component(
        self,
        component_name: str,
        component_type: str,
        file_path: str,
        custom_thresholds: Optional[Dict[str, float]] = None
    ) -> None:
        """Register a gaming component for performance monitoring."""
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
        """Execute comprehensive performance validation for gaming components."""
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
            
            # Calculate overall performance score
            if validation_results["component_results"]:
                scores = [
                    result["overall_performance_score"]
                    for result in validation_results["component_results"].values()
                    if "overall_performance_score" in result
                ]
                validation_results["overall_performance_score"] = sum(scores) / len(scores) if scores else 0.0
            
            # Generate summary
            validation_results["summary"] = self._generate_validation_summary(validation_results)
            
            execution_time = time.time() - start_time
            validation_results["execution_time"] = execution_time
            
            print(f"Comprehensive performance validation completed in {execution_time:.2f} seconds")
            
        except Exception as e:
            print(f"Error in comprehensive performance validation: {e}")
            validation_results["error"] = str(e)
        
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
            "test_results": [],
            "overall_performance_score": 0.0,
            "threshold_compliance": {},
            "recommendations": []
        }
        
        try:
            # Execute each test type using extracted handlers
            for test_type in test_types:
                if test_type in self.test_configurations:
                    test_config = self.test_configurations[test_type]
                    
                    # Execute performance test using handler
                    test_result = await PerformanceTestHandlers.execute_performance_test(
                        test_type, component_name, component_profile, test_config
                    )
                    
                    component_results["test_results"].append(test_result)
                    self.performance_history.append(test_result)
            
            # Calculate overall performance score
            if component_results["test_results"]:
                scores = [result.performance_score for result in component_results["test_results"]]
                component_results["overall_performance_score"] = sum(scores) / len(scores)
                
                # Aggregate threshold compliance and recommendations
                all_compliance = {}
                all_recommendations = []
                for result in component_results["test_results"]:
                    for metric, compliant in result.threshold_compliance.items():
                        if metric not in all_compliance:
                            all_compliance[metric] = []
                        all_compliance[metric].append(compliant)
                    all_recommendations.extend(result.recommendations)
                
                # Calculate compliance percentage for each metric
                for metric, compliance_list in all_compliance.items():
                    component_results["threshold_compliance"][metric] = (
                        sum(compliance_list) / len(compliance_list) * 100
                    )
                
                component_results["recommendations"] = list(set(all_recommendations))
            
            print(f"Performance tests completed for component '{component_name}'")
            
        except Exception as e:
            print(f"Error executing performance tests for component '{component_name}': {e}")
            component_results["error"] = str(e)
        
        return component_results

    def start_real_time_monitoring(self) -> None:
        """Start real-time performance monitoring."""
        PerformanceMonitoringHandlers.start_real_time_monitoring(
            self, self.config.monitoring_interval
        )

    def stop_real_time_monitoring(self) -> None:
        """Stop real-time performance monitoring."""
        PerformanceMonitoringHandlers.stop_real_time_monitoring(self)

    def perform_statistical_analysis(self, component_name: str) -> PerformanceAnalysisResult:
        """Perform statistical analysis on performance history."""
        return PerformanceAnalysisHandlers.perform_statistical_analysis(
            self.performance_history, component_name
        )

    def generate_performance_report(self, component_names: List[str] = None) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        if component_names is None:
            component_names = list(self.component_profiles.keys())
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "components_analyzed": len(component_names),
            "component_analyses": {},
            "overall_summary": {},
            "recommendations": []
        }
        
        try:
            # Analyze each component
            for component_name in component_names:
                if component_name in self.component_profiles:
                    analysis = self.perform_statistical_analysis(component_name)
                    report["component_analyses"][component_name] = {
                        "baseline_metrics": analysis.baseline_metrics,
                        "current_metrics": analysis.current_metrics,
                        "performance_delta": analysis.performance_delta,
                        "regression_detected": analysis.regression_detected,
                        "recommendations": analysis.recommendations,
                        "confidence_score": analysis.confidence_score
                    }
            
            # Generate overall summary
            report["overall_summary"] = self._generate_performance_summary(report["component_analyses"])
            
            print(f"Performance report generated for {len(component_names)} components")
            
        except Exception as e:
            print(f"Error generating performance report: {e}")
            report["error"] = str(e)
        
        return report

    def _generate_validation_summary(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate validation summary."""
        component_results = validation_results.get("component_results", {})
        
        return {
            "total_components": len(component_results),
            "successful_tests": len([r for r in component_results.values() if "error" not in r]),
            "failed_tests": len([r for r in component_results.values() if "error" in r]),
            "average_performance_score": validation_results.get("overall_performance_score", 0.0),
            "test_types_executed": validation_results.get("test_types_executed", [])
        }

    def _generate_performance_summary(self, component_analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance summary."""
        if not component_analyses:
            return {}
        
        total_components = len(component_analyses)
        regressions_detected = sum(
            1 for analysis in component_analyses.values()
            if analysis.get("regression_detected", False)
        )
        
        avg_confidence = sum(
            analysis.get("confidence_score", 0.0)
            for analysis in component_analyses.values()
        ) / total_components if total_components > 0 else 0.0
        
        return {
            "total_components_analyzed": total_components,
            "regressions_detected": regressions_detected,
            "regression_percentage": (regressions_detected / total_components * 100) if total_components > 0 else 0.0,
            "average_confidence_score": avg_confidence,
            "analysis_timestamp": datetime.now().isoformat()
        }
