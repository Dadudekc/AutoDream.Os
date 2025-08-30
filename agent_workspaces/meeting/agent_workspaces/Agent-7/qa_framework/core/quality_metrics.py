"""
🎯 QUALITY METRICS CALCULATOR - CORE COMPONENT
Agent-7 - Quality Completion Optimization Manager

Quality metrics calculation engine for modularization assessment.
Follows V2 coding standards: ≤300 lines per module.
"""

import os
import ast
import re
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from .quality_models import QualityMetric, QualityThresholds


class QualityMetricsCalculator:
    """Calculator for various quality metrics."""
    
    def __init__(self, thresholds: QualityThresholds):
        """Initialize with quality thresholds."""
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
            description="Percentage reduction in total file size",
            unit="%"
        )
    
    def calculate_module_count_metric(self, module_count: int) -> QualityMetric:
        """Calculate module count metric."""
        return QualityMetric(
            "Module Count",
            module_count,
            0.15,  # 15% weight
            self.thresholds.get_threshold("module_count"),
            description="Number of modules created",
            unit="modules"
        )
    
    def calculate_interface_quality_metric(self, interface_quality: float) -> QualityMetric:
        """Calculate interface quality metric."""
        return QualityMetric(
            "Interface Quality",
            interface_quality,
            0.15,  # 15% weight
            self.thresholds.get_threshold("interface_quality"),
            description="Interface design quality score",
            unit="score"
        )
    
    def calculate_dependency_complexity_metric(self, dependency_complexity: float) -> QualityMetric:
        """Calculate dependency complexity metric."""
        return QualityMetric(
            "Dependency Complexity",
            dependency_complexity,
            0.1,  # 10% weight
            self.thresholds.get_threshold("dependency_complexity"),
            description="Dependency complexity score (lower is better)",
            unit="score"
        )
    
    def calculate_naming_conventions_metric(self, naming_score: float) -> QualityMetric:
        """Calculate naming conventions compliance metric."""
        return QualityMetric(
            "Naming Conventions",
            naming_score,
            0.1,  # 10% weight
            self.thresholds.get_threshold("naming_conventions"),
            description="Naming convention compliance score",
            unit="score"
        )
    
    def calculate_documentation_metric(self, documentation_score: float) -> QualityMetric:
        """Calculate documentation quality metric."""
        return QualityMetric(
            "Documentation",
            documentation_score,
            0.1,  # 10% weight
            self.thresholds.get_threshold("documentation"),
            description="Documentation quality score",
            unit="score"
        )
    
    def calculate_code_organization_metric(self, organization_score: float) -> QualityMetric:
        """Calculate code organization metric."""
        return QualityMetric(
            "Code Organization",
            organization_score,
            0.1,  # 10% weight
            self.thresholds.get_threshold("code_organization"),
            description="Code organization quality score",
            unit="score"
        )
    
    def calculate_test_coverage_metric(self, test_coverage: float) -> QualityMetric:
        """Calculate test coverage metric."""
        return QualityMetric(
            "Test Coverage",
            test_coverage,
            0.1,  # 10% weight
            self.thresholds.get_threshold("test_coverage"),
            description="Test coverage percentage",
            unit="%"
        )
    
    def calculate_v2_compliance_metric(self, max_module_lines: int) -> QualityMetric:
        """Calculate V2 compliance metric (max 400 lines per module)."""
        compliance_score = 100.0 if max_module_lines <= 400 else max(0, 100 - (max_module_lines - 400))
        
        return QualityMetric(
            "V2 Compliance",
            compliance_score,
            0.2,  # 20% weight
            100.0,  # 100% threshold
            description="V2 compliance score (400 lines max per module)",
            unit="%"
        )
    
    def calculate_overall_quality_score(self, metrics: Dict[str, QualityMetric]) -> float:
        """Calculate overall quality score from individual metrics."""
        if not metrics:
            return 0.0
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for metric in metrics.values():
            if isinstance(metric.value, (int, float)):
                # Normalize values to 0-100 scale
                if metric.unit == "%":
                    normalized_value = metric.value
                elif metric.unit == "score":
                    normalized_value = metric.value * 100
                else:
                    # For other units, assume they're already normalized
                    normalized_value = metric.value
                
                total_weighted_score += normalized_value * metric.weight
                total_weight += metric.weight
        
        if total_weight > 0:
            return total_weighted_score / total_weight
        else:
            return 0.0


class QualityMetricsCollector:
    """Collects and manages quality metrics during assessment."""
    
    def __init__(self, thresholds: QualityThresholds):
        """Initialize metrics collector."""
        self.thresholds = thresholds
        self.calculator = QualityMetricsCalculator(thresholds)
        self.metrics: Dict[str, QualityMetric] = {}
    
    def collect_file_metrics(self, target_file: str, modularized_dir: str) -> Dict[str, QualityMetric]:
        """Collect file-related quality metrics."""
        metrics = {}
        
        # File size metrics
        original_size = self._get_file_size(target_file)
        modularized_size = self._get_directory_size(modularized_dir)
        
        metrics["file_size_reduction"] = self.calculator.calculate_file_size_reduction(
            original_size, modularized_size
        )
        
        # Module count metric
        module_count = self._count_modules(modularized_dir)
        metrics["module_count"] = self.calculator.calculate_module_count_metric(module_count)
        
        # V2 compliance metric
        max_lines = self._get_max_module_lines(modularized_dir)
        metrics["v2_compliance"] = self.calculator.calculate_v2_compliance_metric(max_lines)
        
        return metrics
    
    def collect_quality_metrics(self, target_file: str, modularized_dir: str) -> Dict[str, QualityMetric]:
        """Collect comprehensive quality metrics."""
        metrics = {}
        
        # File metrics
        file_metrics = self.collect_file_metrics(target_file, modularized_dir)
        metrics.update(file_metrics)
        
        # Code quality metrics
        interface_quality = self._analyze_interface_quality(modularized_dir)
        metrics["interface_quality"] = self.calculator.calculate_interface_quality_metric(interface_quality)
        
        dependency_complexity = self._analyze_dependency_complexity(modularized_dir)
        metrics["dependency_complexity"] = self.calculator.calculate_dependency_complexity_metric(dependency_complexity)
        
        naming_score = self._analyze_naming_conventions(modularized_dir)
        metrics["naming_conventions"] = self.calculator.calculate_naming_conventions_metric(naming_score)
        
        documentation_score = self._analyze_documentation(modularized_dir)
        metrics["documentation"] = self.calculator.calculate_documentation_metric(documentation_score)
        
        organization_score = self._analyze_code_organization(modularized_dir)
        metrics["code_organization"] = self.calculator.calculate_code_organization_metric(organization_score)
        
        test_coverage = self._analyze_test_coverage(modularized_dir)
        metrics["test_coverage"] = self.calculator.calculate_test_coverage_metric(test_coverage)
        
        return metrics
    
    def _get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        try:
            return os.path.getsize(file_path)
        except (OSError, FileNotFoundError):
            return 0
    
    def _get_directory_size(self, dir_path: str) -> int:
        """Get total size of directory in bytes."""
        total_size = 0
        try:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    total_size += self._get_file_size(file_path)
        except (OSError, FileNotFoundError):
            pass
        return total_size
    
    def _count_modules(self, dir_path: str) -> int:
        """Count Python modules in directory."""
        module_count = 0
        try:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if file.endswith('.py'):
                        module_count += 1
        except (OSError, FileNotFoundError):
            pass
        return module_count
    
    def _get_max_module_lines(self, dir_path: str) -> int:
        """Get maximum lines in any module."""
        max_lines = 0
        try:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                lines = len(f.readlines())
                                max_lines = max(max_lines, lines)
                        except (OSError, UnicodeDecodeError):
                            pass
        except (OSError, FileNotFoundError):
            pass
        return max_lines
    
    def _analyze_interface_quality(self, dir_path: str) -> float:
        """Analyze interface quality (placeholder implementation)."""
        # This would implement actual interface quality analysis
        return 0.8  # Placeholder score
    
    def _analyze_dependency_complexity(self, dir_path: str) -> float:
        """Analyze dependency complexity (placeholder implementation)."""
        # This would implement actual dependency complexity analysis
        return 0.5  # Placeholder score
    
    def _analyze_naming_conventions(self, dir_path: str) -> float:
        """Analyze naming convention compliance (placeholder implementation)."""
        # This would implement actual naming convention analysis
        return 0.9  # Placeholder score
    
    def _analyze_documentation(self, dir_path: str) -> float:
        """Analyze documentation quality (placeholder implementation)."""
        # This would implement actual documentation analysis
        return 0.7  # Placeholder score
    
    def _analyze_code_organization(self, dir_path: str) -> float:
        """Analyze code organization quality (placeholder implementation)."""
        # This would implement actual code organization analysis
        return 0.8  # Placeholder score
    
    def _analyze_test_coverage(self, dir_path: str) -> float:
        """Analyze test coverage (placeholder implementation)."""
        # This would implement actual test coverage analysis
        return 75.0  # Placeholder score
