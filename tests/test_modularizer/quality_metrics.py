"""
🧪 QUALITY ASSURANCE METRICS - MODULARIZED COMPONENT
Testing Framework Enhancement Manager - Agent-3

This module contains quality metrics calculation and assessment functionality.
Extracted from quality_assurance_protocols.py for better modularity.
"""

from typing import Dict, Any
from .quality_models import QualityMetric, QualityThresholds


class QualityMetricsCalculator:
    """Calculator for various quality metrics."""
    
    def __init__(self, thresholds: QualityThresholds):
        self.thresholds = thresholds
    
    def calculate_file_size_reduction(self, original_size: int, modularized_size: int) -> QualityMetric:
        """Calculate file size reduction metric."""
        if original_size > 0:
            size_reduction = (
                (original_size - modularized_size) / original_size * 100
            )
        else:
            size_reduction = 0.0
            
        return QualityMetric(
            "File Size Reduction",
            size_reduction,
            0.2,  # 20% weight
            self.thresholds.get_threshold("file_size_reduction"),
            "PASS" if size_reduction >= self.thresholds.get_threshold("file_size_reduction") else "FAIL"
        )
    
    def calculate_module_count_metric(self, module_count: int) -> QualityMetric:
        """Calculate module count metric."""
        return QualityMetric(
            "Module Count",
            module_count,
            0.15,  # 15% weight
            self.thresholds.get_threshold("module_count"),
            "PASS" if module_count >= self.thresholds.get_threshold("module_count") else "FAIL"
        )
    
    def calculate_interface_quality_metric(self, interface_quality: float) -> QualityMetric:
        """Calculate interface quality metric."""
        return QualityMetric(
            "Interface Quality",
            interface_quality,
            0.2,  # 20% weight
            self.thresholds.get_threshold("interface_quality"),
            "PASS" if interface_quality >= self.thresholds.get_threshold("interface_quality") else "FAIL"
        )
    
    def calculate_dependency_complexity_metric(self, dependency_complexity: float) -> QualityMetric:
        """Calculate dependency complexity metric."""
        return QualityMetric(
            "Dependency Complexity",
            dependency_complexity,
            0.15,  # 15% weight
            self.thresholds.get_threshold("dependency_complexity"),
            "PASS" if dependency_complexity <= self.thresholds.get_threshold("dependency_complexity") else "FAIL"
        )
    
    def calculate_naming_conventions_metric(self, naming_score: float) -> QualityMetric:
        """Calculate naming conventions metric."""
        return QualityMetric(
            "Naming Conventions",
            naming_score,
            0.1,  # 10% weight
            self.thresholds.get_threshold("naming_conventions"),
            "PASS" if naming_score >= self.thresholds.get_threshold("naming_conventions") else "FAIL"
        )
    
    def calculate_code_organization_metric(self, organization_score: float) -> QualityMetric:
        """Calculate code organization metric."""
        return QualityMetric(
            "Code Organization",
            organization_score,
            0.1,  # 10% weight
            self.thresholds.get_threshold("code_organization"),
            "PASS" if organization_score >= self.thresholds.get_threshold("code_organization") else "FAIL"
        )
    
    def calculate_documentation_metric(self, documentation_score: float) -> QualityMetric:
        """Calculate documentation quality metric."""
        return QualityMetric(
            "Documentation Quality",
            documentation_score,
            0.1,  # 10% weight
            self.thresholds.get_threshold("documentation"),
            "PASS" if documentation_score >= self.thresholds.get_threshold("documentation") else "FAIL"
        )


class QualityAssessor:
    """Assessor for various quality aspects."""
    
    @staticmethod
    def assess_interface_quality(modularized_analysis: Dict[str, Any]) -> float:
        """Assess interface quality score."""
        # Placeholder implementation - can be enhanced with more sophisticated analysis
        return 0.8
    
    @staticmethod
    def assess_dependency_complexity(modularized_analysis: Dict[str, Any]) -> float:
        """Assess dependency complexity score."""
        # Placeholder implementation - can be enhanced with more sophisticated analysis
        return 0.5
    
    @staticmethod
    def assess_naming_conventions(modularized_analysis: Dict[str, Any]) -> float:
        """Assess naming convention compliance."""
        # Placeholder implementation - can be enhanced with more sophisticated analysis
        return 0.9
    
    @staticmethod
    def assess_code_organization(modularized_analysis: Dict[str, Any]) -> float:
        """Assess code organization quality."""
        # Placeholder implementation - can be enhanced with more sophisticated analysis
        return 0.85
    
    @staticmethod
    def assess_documentation_quality(modularized_analysis: Dict[str, Any]) -> float:
        """Assess documentation quality."""
        # Placeholder implementation - can be enhanced with more sophisticated analysis
        return 0.75


def calculate_overall_quality_score(metrics: Dict[str, QualityMetric]) -> float:
    """Calculate overall quality score from individual metrics."""
    total_score = 0.0
    total_weight = 0.0
    
    try:
        for metric in metrics.values():
            if isinstance(metric, QualityMetric):
                # Normalize metric value to 0-100 scale
                normalized_value = min(metric.value, 100.0)
                total_score += normalized_value * metric.weight
                total_weight += metric.weight
        
        if total_weight > 0:
            overall_score = total_score / total_weight
        else:
            overall_score = 0.0
            
    except Exception as e:
        print(f"Error calculating overall quality score: {e}")
        overall_score = 0.0
        
    return round(overall_score, 2)
