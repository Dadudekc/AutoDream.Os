#!/usr/bin/env python3
"""
Recommendations Engine - Generates coverage improvement recommendations.

This module provides intelligent recommendations for improving test coverage.
"""

from typing import Dict, List, Any
from .coverage_models import CoverageMetric


class RecommendationsEngine:
    """Generates intelligent recommendations for coverage improvement."""
    
    def __init__(self):
        self.recommendation_templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, List[str]]:
        """Initialize recommendation templates for different scenarios."""
        return {
            "line_coverage": [
                "Add test cases to cover lines {lines} in {function}",
                "Create edge case tests for {function} to improve line coverage",
                "Add boundary condition tests for {function}"
            ],
            "function_coverage": [
                "Create unit tests for uncovered function '{function}'",
                "Add integration tests for {function}",
                "Test error handling paths in {function}"
            ],
            "class_coverage": [
                "Add unit tests for class '{class_name}'",
                "Test all methods in {class_name}",
                "Create mock objects for {class_name} dependencies"
            ],
            "branch_coverage": [
                "Add tests for conditional branches in {function}",
                "Test both true and false paths in {function}",
                "Cover exception handling in {function}"
            ]
        }
    
    def generate_coverage_recommendations(self, metrics: Dict[str, CoverageMetric],
                                       uncovered_areas: List[str]) -> List[str]:
        """Generate comprehensive coverage improvement recommendations."""
        recommendations = []
        
        # Generate metric-specific recommendations
        for metric_name, metric in metrics.items():
            if metric.value < metric.target:
                metric_recommendations = self._generate_metric_recommendations(
                    metric_name, metric, uncovered_areas
                )
                recommendations.extend(metric_recommendations)
        
        # Generate general recommendations based on overall performance
        general_recommendations = self._generate_general_recommendations(metrics)
        recommendations.extend(general_recommendations)
        
        # Generate specific recommendations for uncovered areas
        specific_recommendations = self._generate_specific_recommendations(uncovered_areas)
        recommendations.extend(specific_recommendations)
        
        # Prioritize recommendations
        prioritized_recommendations = self._prioritize_recommendations(recommendations, metrics)
        
        return prioritized_recommendations
    
    def _generate_metric_recommendations(self, metric_name: str, metric: CoverageMetric,
                                       uncovered_areas: List[str]) -> List[str]:
        """Generate recommendations for a specific metric."""
        recommendations = []
        
        if metric_name == "line_coverage":
            if metric.value < 50.0:
                recommendations.append("CRITICAL: Line coverage is extremely low. Focus on basic functionality tests first.")
            elif metric.value < 75.0:
                recommendations.append("HIGH PRIORITY: Line coverage needs significant improvement. Add comprehensive test cases.")
            else:
                recommendations.append(f"Increase line coverage from {metric.value:.1f}% to at least {metric.target:.1f}%")
        
        elif metric_name == "function_coverage":
            if metric.value < 80.0:
                recommendations.append("HIGH PRIORITY: Many functions are untested. Create unit tests for all public functions.")
            else:
                recommendations.append(f"Improve function coverage from {metric.value:.1f}% to {metric.target:.1f}%")
        
        elif metric_name == "class_coverage":
            if metric.value < 70.0:
                recommendations.append("HIGH PRIORITY: Class coverage is poor. Test all class methods and constructors.")
            else:
                recommendations.append(f"Enhance class coverage from {metric.value:.1f}% to {metric.target:.1f}%")
        
        elif metric_name == "branch_coverage":
            if metric.value < 60.0:
                recommendations.append("CRITICAL: Branch coverage is very low. Test all conditional paths and edge cases.")
            else:
                recommendations.append(f"Improve branch coverage from {metric.value:.1f}% to {metric.target:.1f}%")
        
        return recommendations
    
    def _generate_general_recommendations(self, metrics: Dict[str, CoverageMetric]) -> List[str]:
        """Generate general improvement recommendations."""
        recommendations = []
        
        # Check for overall patterns
        failing_metrics = [m for m in metrics.values() if m.status == "FAILING"]
        warning_metrics = [m for m in metrics.values() if m.status == "WARNING"]
        
        if len(failing_metrics) >= 3:
            recommendations.append("CRITICAL: Multiple metrics are failing. Consider comprehensive test suite overhaul.")
        elif len(failing_metrics) >= 2:
            recommendations.append("HIGH PRIORITY: Several metrics need attention. Focus on most critical areas first.")
        
        if len(warning_metrics) >= 2:
            recommendations.append("MEDIUM PRIORITY: Multiple metrics are in warning range. Plan improvements for next iteration.")
        
        # Check for specific metric combinations
        if "line_coverage" in metrics and "function_coverage" in metrics:
            line_metric = metrics["line_coverage"]
            func_metric = metrics["function_coverage"]
            
            if line_metric.value < func_metric.value:
                recommendations.append("Focus on line coverage - functions are tested but not all code paths are covered.")
            elif func_metric.value < line_metric.value:
                recommendations.append("Focus on function coverage - add tests for untested functions.")
        
        return recommendations
    
    def _generate_specific_recommendations(self, uncovered_areas: List[str]) -> List[str]:
        """Generate specific recommendations based on uncovered areas."""
        recommendations = []
        
        for area in uncovered_areas:
            if "Function" in area:
                func_name = area.split("'")[1] if "'" in area else "unknown"
                recommendations.append(f"Create unit tests for function '{func_name}'")
            elif "Class" in area:
                class_name = area.split("'")[1] if "'" in area else "unknown"
                recommendations.append(f"Add comprehensive tests for class '{class_name}'")
            elif "Line coverage" in area:
                recommendations.append("Add test cases to cover untested lines")
            elif "Branch coverage" in area:
                recommendations.append("Test all conditional branches and edge cases")
        
        return recommendations
    
    def _prioritize_recommendations(self, recommendations: List[str],
                                  metrics: Dict[str, CoverageMetric]) -> List[str]:
        """Prioritize recommendations based on urgency and impact."""
        if not recommendations:
            return []
        
        # Categorize recommendations by priority
        critical = []
        high = []
        medium = []
        low = []
        
        for rec in recommendations:
            if any(keyword in rec.upper() for keyword in ["CRITICAL", "EXTREMELY LOW", "VERY LOW"]):
                critical.append(rec)
            elif any(keyword in rec.upper() for keyword in ["HIGH PRIORITY", "SIGNIFICANT", "MANY"]):
                high.append(rec)
            elif any(keyword in rec.upper() for keyword in ["MEDIUM PRIORITY", "CONSIDER", "PLAN"]):
                medium.append(rec)
            else:
                low.append(rec)
        
        # Return prioritized list
        prioritized = []
        prioritized.extend(critical)
        prioritized.extend(high)
        prioritized.extend(medium)
        prioritized.extend(low)
        
        return prioritized
