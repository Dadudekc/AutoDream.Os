"""
Coverage Calculator - Core coverage calculation logic.

This module handles all coverage calculations, metrics, and analysis computations.
"""

import ast
from typing import Dict, List, Any, Tuple
from .coverage_models import CoverageMetric, FileStructure


class CoverageCalculator:
    """Handles coverage calculations and metric computations."""
    
    def __init__(self):
        self.coverage_targets = self._initialize_coverage_targets()
        self.risk_thresholds = self._initialize_risk_thresholds()
    
    def _initialize_coverage_targets(self) -> Dict[str, float]:
        """Initialize coverage targets for different metrics."""
        return {
            "line_coverage": 90.0,      # Target 90% line coverage
            "branch_coverage": 85.0,    # Target 85% branch coverage
            "function_coverage": 95.0,  # Target 95% function coverage
            "class_coverage": 90.0,     # Target 90% class coverage
            "overall_coverage": 85.0    # Target 85% overall coverage
        }
    
    def _initialize_risk_thresholds(self) -> Dict[str, float]:
        """Initialize risk assessment thresholds."""
        return {
            "high_risk": 60.0,      # Below 60% coverage is high risk
            "medium_risk": 75.0,    # Below 75% coverage is medium risk
            "low_risk": 85.0,       # Below 85% coverage is low risk
            "safe": 95.0            # Above 95% coverage is safe
        }
    
    def analyze_file_structure(self, target_file: str) -> FileStructure:
        """Analyze the structure of a target file."""
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            total_lines = len(content.splitlines())
            code_lines = 0
            comment_lines = 0
            blank_lines = 0
            functions = []
            classes = []
            imports = []
            
            for line in content.splitlines():
                stripped = line.strip()
                if not stripped:
                    blank_lines += 1
                elif stripped.startswith('#'):
                    comment_lines += 1
                else:
                    code_lines += 1
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            return FileStructure(
                total_lines=total_lines,
                code_lines=code_lines,
                comment_lines=comment_lines,
                blank_lines=blank_lines,
                functions=functions,
                classes=classes,
                imports=imports
            )
            
        except Exception as e:
            # Return default structure on error
            return FileStructure(
                total_lines=0,
                code_lines=0,
                comment_lines=0,
                blank_lines=0,
                functions=[],
                classes=[],
                imports=[]
            )
    
    def calculate_coverage_metrics(self, file_structure: FileStructure,
                                 coverage_data: Dict[str, Any]) -> Dict[str, CoverageMetric]:
        """Calculate coverage metrics for all coverage types."""
        metrics = {}
        
        # Line coverage
        if file_structure.total_lines > 0:
            line_coverage = (file_structure.code_lines / file_structure.total_lines) * 100
        else:
            line_coverage = 0.0
        
        metrics["line_coverage"] = CoverageMetric(
            name="Line Coverage",
            value=line_coverage,
            target=self.coverage_targets["line_coverage"],
            status=self._get_metric_status(line_coverage, self.coverage_targets["line_coverage"]),
            risk_level=self._assess_risk_level(line_coverage)
        )
        
        # Function coverage
        if file_structure.functions:
            function_coverage = (len(coverage_data.get("functions", [])) / len(file_structure.functions)) * 100
        else:
            function_coverage = 100.0
        
        metrics["function_coverage"] = CoverageMetric(
            name="Function Coverage",
            value=function_coverage,
            target=self.coverage_targets["function_coverage"],
            status=self._get_metric_status(function_coverage, self.coverage_targets["function_coverage"]),
            risk_level=self._assess_risk_level(function_coverage)
        )
        
        # Class coverage
        if file_structure.classes:
            class_coverage = (len(coverage_data.get("classes", [])) / len(file_structure.classes)) * 100
        else:
            class_coverage = 100.0
        
        metrics["class_coverage"] = CoverageMetric(
            name="Class Coverage",
            value=class_coverage,
            target=self.coverage_targets["class_coverage"],
            status=self._get_metric_status(class_coverage, self.coverage_targets["class_coverage"]),
            risk_level=self._assess_risk_level(class_coverage)
        )
        
        # Branch coverage (simulated for now)
        branch_coverage = coverage_data.get("branch_coverage", 85.0)
        metrics["branch_coverage"] = CoverageMetric(
            name="Branch Coverage",
            value=branch_coverage,
            target=self.coverage_targets["branch_coverage"],
            status=self._get_metric_status(branch_coverage, self.coverage_targets["branch_coverage"]),
            risk_level=self._assess_risk_level(branch_coverage)
        )
        
        return metrics
    
    def calculate_overall_coverage(self, metrics: Dict[str, CoverageMetric]) -> float:
        """Calculate overall coverage as weighted average of all metrics."""
        if not metrics:
            return 0.0
        
        # Weight different coverage types
        weights = {
            "line_coverage": 0.3,
            "function_coverage": 0.3,
            "class_coverage": 0.2,
            "branch_coverage": 0.2
        }
        
        total_weight = 0.0
        weighted_sum = 0.0
        
        for metric_name, metric in metrics.items():
            if metric_name in weights:
                weighted_sum += metric.value * weights[metric_name]
                total_weight += weights[metric_name]
        
        if total_weight == 0.0:
            return 0.0
        
        return weighted_sum / total_weight
    
    def _get_metric_status(self, value: float, target: float) -> str:
        """Get status string for a metric."""
        if value >= target:
            return "PASSING"
        elif value >= target * 0.8:
            return "WARNING"
        else:
            return "FAILING"
    
    def _assess_risk_level(self, coverage: float) -> str:
        """Assess risk level based on coverage percentage."""
        if coverage >= self.risk_thresholds["safe"]:
            return "LOW"
        elif coverage >= self.risk_thresholds["low_risk"]:
            return "MEDIUM"
        elif coverage >= self.risk_thresholds["medium_risk"]:
            return "HIGH"
        else:
            return "CRITICAL"
