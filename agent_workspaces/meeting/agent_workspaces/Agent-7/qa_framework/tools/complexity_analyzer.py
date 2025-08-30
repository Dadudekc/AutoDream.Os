"""
🎯 CODE COMPLEXITY ANALYZER - TOOLS COMPONENT
Agent-7 - Quality Completion Optimization Manager

Code complexity analysis tool for quality assurance.
Follows V2 coding standards: ≤300 lines per module.
"""

import os
import ast
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ComplexityResult:
    """Code complexity analysis result."""
    file_path: str
    cyclomatic_complexity: float
    cognitive_complexity: float
    nesting_depth: int
    function_count: int
    class_count: int
    average_function_complexity: float
    max_function_complexity: int
    complexity_distribution: Dict[str, int]


class CodeComplexityAnalyzer:
    """Analyzes code complexity for modularized components."""
    
    def __init__(self):
        """Initialize code complexity analyzer."""
        self.complexity_thresholds = {
            "cyclomatic": 10.0,      # Maximum average cyclomatic complexity
            "cognitive": 15.0,       # Maximum average cognitive complexity
            "nesting": 5,            # Maximum nesting depth
            "function": 15,          # Maximum function complexity
            "class": 20              # Maximum class complexity
        }
    
    def analyze_complexity(self, modularized_dir: str) -> Dict[str, Any]:
        """
        Analyze code complexity for modularized components.
        
        Args:
            modularized_dir: Path to the modularized components directory
            
        Returns:
            dict: Comprehensive complexity analysis results
        """
        complexity_results = {
            "overall_complexity": 0.0,
            "average_cyclomatic": 0.0,
            "average_cognitive": 0.0,
            "max_nesting_depth": 0,
            "total_functions": 0,
            "total_classes": 0,
            "file_complexity": {},
            "complexity_summary": {},
            "recommendations": []
        }
        
        try:
            # Find Python source files
            source_files = self._find_source_files(modularized_dir)
            
            if not source_files:
                complexity_results["error"] = "No Python source files found"
                return complexity_results
            
            # Analyze complexity for each file
            file_results = []
            total_cyclomatic = 0.0
            total_cognitive = 0.0
            total_functions = 0
            total_classes = 0
            
            for source_file in source_files:
                file_result = self._analyze_file_complexity(source_file)
                if file_result:
                    file_results.append(file_result)
                    total_cyclomatic += file_result.cyclomatic_complexity
                    total_cognitive += file_result.cognitive_complexity
                    total_functions += file_result.function_count
                    total_classes += file_result.class_count
            
            # Calculate overall complexity metrics
            if file_results:
                complexity_results["overall_complexity"] = (
                    (total_cyclomatic + total_cognitive) / (len(file_results) * 2)
                )
                complexity_results["average_cyclomatic"] = total_cyclomatic / len(file_results)
                complexity_results["average_cognitive"] = total_cognitive / len(file_results)
                complexity_results["max_nesting_depth"] = max(
                    result.nesting_depth for result in file_results
                )
                complexity_results["total_functions"] = total_functions
                complexity_results["total_classes"] = total_classes
            
            # Store file-level complexity results
            complexity_results["file_complexity"] = {
                result.file_path: {
                    "cyclomatic_complexity": result.cyclomatic_complexity,
                    "cognitive_complexity": result.cognitive_complexity,
                    "nesting_depth": result.nesting_depth,
                    "function_count": result.function_count,
                    "class_count": result.class_count,
                    "average_function_complexity": result.average_function_complexity,
                    "max_function_complexity": result.max_function_complexity
                }
                for result in file_results
            }
            
            # Generate complexity summary
            complexity_results["complexity_summary"] = self._generate_complexity_summary(complexity_results)
            
            # Generate recommendations
            complexity_results["recommendations"] = self._generate_complexity_recommendations(complexity_results)
            
        except Exception as e:
            complexity_results["error"] = str(e)
        
        return complexity_results
    
    def _find_source_files(self, modularized_dir: str) -> List[str]:
        """Find Python source files in the modularized directory."""
        source_files = []
        try:
            for root, dirs, files in os.walk(modularized_dir):
                for file in files:
                    if file.endswith('.py') and not file.startswith('test_'):
                        source_files.append(os.path.join(root, file))
        except (OSError, FileNotFoundError):
            pass
        return source_files
    
    def _analyze_file_complexity(self, file_path: str) -> Optional[ComplexityResult]:
        """Analyze code complexity for a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST to analyze code structure
            tree = ast.parse(content)
            
            # Analyze complexity metrics
            cyclomatic_complexity = self._calculate_cyclomatic_complexity(tree)
            cognitive_complexity = self._calculate_cognitive_complexity(tree)
            nesting_depth = self._calculate_nesting_depth(tree)
            function_count = self._count_functions(tree)
            class_count = self._count_classes(tree)
            function_complexities = self._analyze_function_complexities(tree)
            
            # Calculate averages
            average_function_complexity = (
                sum(function_complexities) / len(function_complexities)
                if function_complexities else 0.0
            )
            max_function_complexity = max(function_complexities) if function_complexities else 0
            
            # Complexity distribution
            complexity_distribution = self._categorize_complexity(function_complexities)
            
            return ComplexityResult(
                file_path=file_path,
                cyclomatic_complexity=cyclomatic_complexity,
                cognitive_complexity=cognitive_complexity,
                nesting_depth=nesting_depth,
                function_count=function_count,
                class_count=class_count,
                average_function_complexity=average_function_complexity,
                max_function_complexity=max_function_complexity,
                complexity_distribution=complexity_distribution
            )
            
        except (OSError, UnicodeDecodeError, SyntaxError):
            return None
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> float:
        """Calculate cyclomatic complexity for the AST."""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _calculate_cognitive_complexity(self, tree: ast.AST) -> float:
        """Calculate cognitive complexity for the AST."""
        complexity = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, ast.And):
                complexity += 1
            elif isinstance(node, ast.Or):
                complexity += 1
            elif isinstance(node, ast.Compare):
                if len(node.ops) > 1:
                    complexity += len(node.ops) - 1
        
        return complexity
    
    def _calculate_nesting_depth(self, tree: ast.AST) -> int:
        """Calculate maximum nesting depth in the AST."""
        max_depth = 0
        current_depth = 0
        
        def visit_node(node, depth):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.Try, ast.With)):
                    visit_node(child, depth + 1)
                else:
                    visit_node(child, depth)
        
        visit_node(tree, 0)
        return max_depth
    
    def _count_functions(self, tree: ast.AST) -> int:
        """Count functions in the AST."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                count += 1
        return count
    
    def _count_classes(self, tree: ast.AST) -> int:
        """Count classes in the AST."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                count += 1
        return count
    
    def _analyze_function_complexities(self, tree: ast.AST) -> List[int]:
        """Analyze complexity of individual functions."""
        complexities = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_complexity = self._calculate_cyclomatic_complexity(node)
                complexities.append(func_complexity)
        
        return complexities
    
    def _categorize_complexity(self, complexities: List[int]) -> Dict[str, int]:
        """Categorize function complexities."""
        distribution = {
            "low": 0,      # 1-5
            "medium": 0,   # 6-10
            "high": 0,     # 11-15
            "very_high": 0 # 16+
        }
        
        for complexity in complexities:
            if complexity <= 5:
                distribution["low"] += 1
            elif complexity <= 10:
                distribution["medium"] += 1
            elif complexity <= 15:
                distribution["high"] += 1
            else:
                distribution["very_high"] += 1
        
        return distribution
    
    def _generate_complexity_summary(self, complexity_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complexity summary with status indicators."""
        summary = {
            "overall_status": "UNKNOWN",
            "thresholds_met": {},
            "areas_for_improvement": [],
            "excellent_complexity": [],
            "good_complexity": [],
            "poor_complexity": []
        }
        
        # Check threshold compliance
        thresholds = self.complexity_thresholds
        
        # Cyclomatic complexity
        avg_cyclomatic = complexity_results.get("average_cyclomatic", 0.0)
        summary["thresholds_met"]["cyclomatic"] = avg_cyclomatic <= thresholds["cyclomatic"]
        
        # Cognitive complexity
        avg_cognitive = complexity_results.get("average_cognitive", 0.0)
        summary["thresholds_met"]["cognitive"] = avg_cognitive <= thresholds["cognitive"]
        
        # Nesting depth
        max_nesting = complexity_results.get("max_nesting_depth", 0)
        summary["thresholds_met"]["nesting"] = max_nesting <= thresholds["nesting"]
        
        # Categorize complexity levels
        for metric, met in summary["thresholds_met"].items():
            if met:
                summary["excellent_complexity"].append(metric)
            else:
                summary["poor_complexity"].append(metric)
                summary["areas_for_improvement"].append(metric)
        
        # Determine overall status
        if all(summary["thresholds_met"].values()):
            summary["overall_status"] = "EXCELLENT"
        elif len(summary["poor_complexity"]) == 0:
            summary["overall_status"] = "GOOD"
        elif len(summary["poor_complexity"]) <= 1:
            summary["overall_status"] = "FAIR"
        else:
            summary["overall_status"] = "POOR"
        
        return summary
    
    def _generate_complexity_recommendations(self, complexity_results: Dict[str, Any]) -> List[str]:
        """Generate complexity improvement recommendations."""
        recommendations = []
        
        # Cyclomatic complexity recommendations
        avg_cyclomatic = complexity_results.get("average_cyclomatic", 0.0)
        if avg_cyclomatic > self.complexity_thresholds["cyclomatic"]:
            recommendations.append(
                f"Reduce average cyclomatic complexity from {avg_cyclomatic:.1f} to {self.complexity_thresholds['cyclomatic']}"
            )
        
        # Cognitive complexity recommendations
        avg_cognitive = complexity_results.get("average_cognitive", 0.0)
        if avg_cognitive > self.complexity_thresholds["cognitive"]:
            recommendations.append(
                f"Reduce average cognitive complexity from {avg_cognitive:.1f} to {self.complexity_thresholds['cognitive']}"
            )
        
        # Nesting depth recommendations
        max_nesting = complexity_results.get("max_nesting_depth", 0)
        if max_nesting > self.complexity_thresholds["nesting"]:
            recommendations.append(
                f"Reduce maximum nesting depth from {max_nesting} to {self.complexity_thresholds['nesting']}"
            )
        
        # General recommendations
        if not recommendations:
            recommendations.append("Maintain current excellent complexity levels")
        else:
            recommendations.append("Consider breaking down complex functions into smaller, focused functions")
            recommendations.append("Extract complex logic into separate methods or utility functions")
            recommendations.append("Use early returns to reduce nesting levels")
        
        return recommendations
    
    def generate_complexity_report(self, complexity_results: Dict[str, Any]) -> str:
        """Generate a human-readable complexity report."""
        if "error" in complexity_results:
            return f"Complexity Analysis Error: {complexity_results['error']}"
        
        report = []
        report.append("# Code Complexity Analysis Report")
        report.append("")
        
        # Overall complexity summary
        report.append("## Overall Complexity Summary")
        report.append(f"- **Overall Complexity**: {complexity_results.get('overall_complexity', 0.0):.1f}")
        report.append(f"- **Average Cyclomatic**: {complexity_results.get('average_cyclomatic', 0.0):.1f}")
        report.append(f"- **Average Cognitive**: {complexity_results.get('average_cognitive', 0.0):.1f}")
        report.append(f"- **Max Nesting Depth**: {complexity_results.get('max_nesting_depth', 0)}")
        report.append(f"- **Total Functions**: {complexity_results.get('total_functions', 0)}")
        report.append(f"- **Total Classes**: {complexity_results.get('total_classes', 0)}")
        report.append("")
        
        # Complexity summary
        summary = complexity_results.get("complexity_summary", {})
        report.append(f"## Complexity Status: {summary.get('overall_status', 'UNKNOWN')}")
        report.append("")
        
        # Recommendations
        recommendations = complexity_results.get("recommendations", [])
        if recommendations:
            report.append("## Recommendations")
            for rec in recommendations:
                report.append(f"- {rec}")
            report.append("")
        
        return "\n".join(report)
