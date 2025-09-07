"""
🧪 QUALITY ASSURANCE COMPLIANCE - MODULARIZED COMPONENT
Testing Framework Enhancement Manager - Agent-3

This module contains compliance checking and recommendations functionality.
Extracted from quality_assurance_protocols.py for better modularity.
"""

from typing import Dict, List
from .quality_models import QualityMetric


class ComplianceChecker:
    """Checker for quality compliance status."""
    
    @staticmethod
    def check_compliance(metrics: Dict[str, QualityMetric]) -> Dict[str, str]:
        """
        Check compliance with quality thresholds.
        
        Args:
            metrics: Dictionary of quality metrics
            
        Returns:
            Dictionary of compliance status for each metric
        """
        compliance = {}
        
        try:
            for metric_name, metric in metrics.items():
                if isinstance(metric, QualityMetric):
                    compliance[metric_name] = metric.status
                    
        except Exception as e:
            print(f"Error checking compliance: {e}")
            
        return compliance


class RecommendationsGenerator:
    """Generator for quality improvement recommendations."""
    
    @staticmethod
    def generate_recommendations(metrics: Dict[str, QualityMetric], 
                               compliance: Dict[str, str]) -> List[str]:
        """
        Generate quality improvement recommendations.
        
        Args:
            metrics: Dictionary of quality metrics
            compliance: Dictionary of compliance status
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        try:
            for metric_name, metric in metrics.items():
                if isinstance(metric, QualityMetric) and metric.status == "FAIL":
                    if metric_name == "file_size_reduction":
                        recommendations.append(
                            f"Increase file size reduction from {metric.value:.1f}% to at least {metric.threshold}%"
                        )
                    elif metric_name == "module_count":
                        recommendations.append(
                            f"Increase module count from {metric.value} to at least {metric.threshold}"
                        )
                    elif metric_name == "interface_quality":
                        recommendations.append(
                            f"Improve interface quality from {metric.value:.2f} to at least {metric.threshold}"
                        )
                    elif metric_name == "dependency_complexity":
                        recommendations.append(
                            f"Reduce dependency complexity from {metric.value:.2f} to at most {metric.threshold}"
                        )
                    elif metric_name == "naming_conventions":
                        recommendations.append(
                            f"Improve naming conventions from {metric.value:.2f} to at least {metric.threshold}"
                        )
                    elif metric_name == "code_organization":
                        recommendations.append(
                            f"Improve code organization from {metric.value:.2f} to at least {metric.threshold}"
                        )
                    elif metric_name == "documentation":
                        recommendations.append(
                            f"Improve documentation quality from {metric.value:.2f} to at least {metric.threshold}"
                        )
                        
        except Exception as e:
            recommendations.append(f"Error generating recommendations: {e}")
            
        return recommendations
    
    @staticmethod
    def generate_general_recommendations(overall_score: float) -> List[str]:
        """Generate general recommendations based on overall score."""
        recommendations = []
        
        if overall_score < 60.0:
            recommendations.append("Critical quality issues detected. Immediate refactoring required.")
            recommendations.append("Consider breaking down large functions and classes.")
            recommendations.append("Review and improve error handling throughout the codebase.")
        elif overall_score < 75.0:
            recommendations.append("Quality improvements needed. Focus on code organization.")
            recommendations.append("Consider extracting utility functions to reduce duplication.")
            recommendations.append("Improve documentation for complex logic.")
        elif overall_score < 90.0:
            recommendations.append("Good quality with room for improvement.")
            recommendations.append("Consider adding more comprehensive tests.")
            recommendations.append("Review naming conventions for consistency.")
        else:
            recommendations.append("Excellent quality! Maintain current standards.")
            recommendations.append("Consider adding performance optimizations.")
            recommendations.append("Document best practices for team reference.")
        
        return recommendations
