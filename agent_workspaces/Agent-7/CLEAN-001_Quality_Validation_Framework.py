#!/usr/bin/env python3
"""
Quality Validation Framework for Cleanup Operations

Contract: CLEAN-001 - Manager Class Duplication Analysis
Agent: Agent-7 (QUALITY ASSURANCE MANAGER)
Mission: CAPTAIN CLEANUP DIRECTIVE - QUALITY COMPLETION OPTIMIZATION
"""

import ast
import logging
import time
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QualityMetrics:
    """Quality metrics for code analysis"""
    maintainability: float = 0.0
    readability: float = 0.0
    complexity: float = 0.0
    duplication: float = 0.0
    overall_score: float = 0.0

@dataclass
class QualityGate:
    """Quality gate configuration"""
    name: str
    threshold: float
    severity: str  # "critical", "warning", "info"
    description: str

class QualityValidationFramework:
    """Framework for validating code quality during cleanup operations"""
    
    def __init__(self):
        self.quality_gates = self._setup_quality_gates()
        self.baseline_metrics: Optional[QualityMetrics] = None
        self.current_metrics: Optional[QualityMetrics] = None
        
    def _setup_quality_gates(self) -> List[QualityGate]:
        """Setup quality gates based on V2 standards"""
        return [
            QualityGate("maintainability", 85.0, "critical", "Maintainability index must be >= 85"),
            QualityGate("readability", 80.0, "critical", "Readability score must be >= 80"),
            QualityGate("complexity", 15.0, "warning", "Complexity score must be <= 15"),
            QualityGate("duplication", 20.0, "critical", "Duplication must be <= 20%"),
            QualityGate("overall_score", 80.0, "critical", "Overall quality score must be >= 80")
        ]
    
    def analyze_codebase(self, codebase_path: str) -> QualityMetrics:
        """Analyze codebase for quality metrics"""
        logger.info(f"Analyzing codebase: {codebase_path}")
        
        metrics = QualityMetrics()
        
        # Analyze Python files
        python_files = list(Path(codebase_path).rglob("*.py"))
        
        if not python_files:
            logger.warning("No Python files found for analysis")
            return metrics
        
        # Calculate metrics
        metrics.maintainability = self._calculate_maintainability(python_files)
        metrics.readability = self._calculate_readability(python_files)
        metrics.complexity = self._calculate_complexity(python_files)
        metrics.duplication = self._calculate_duplication(python_files)
        metrics.overall_score = self._calculate_overall_score(metrics)
        
        return metrics
    
    def _calculate_maintainability(self, files: List[Path]) -> float:
        """Calculate maintainability index"""
        total_score = 0.0
        file_count = 0
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple maintainability calculation
                lines = len(content.splitlines())
                functions = content.count('def ')
                classes = content.count('class ')
                
                # Basic maintainability formula
                if lines > 0:
                    complexity_factor = (functions + classes) / lines
                    maintainability = max(0, 100 - (complexity_factor * 100))
                    total_score += maintainability
                    file_count += 1
                    
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")
        
        return total_score / file_count if file_count > 0 else 0.0
    
    def _calculate_readability(self, files: List[Path]) -> float:
        """Calculate readability score"""
        total_score = 0.0
        file_count = 0
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple readability calculation
                lines = len(content.splitlines())
                avg_line_length = sum(len(line) for line in content.splitlines()) / lines if lines > 0 else 0
                
                # Basic readability formula
                if avg_line_length <= 80:
                    readability = 100
                elif avg_line_length <= 120:
                    readability = 80
                else:
                    readability = 60
                
                total_score += readability
                file_count += 1
                
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")
        
        return total_score / file_count if file_count > 0 else 0.0
    
    def _calculate_complexity(self, files: List[Path]) -> float:
        """Calculate complexity score"""
        total_complexity = 0.0
        file_count = 0
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse AST for complexity analysis
                tree = ast.parse(content)
                
                # Count complexity factors
                complexity = 0
                for node in ast.walk(tree):
                    if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                        complexity += 1
                    elif isinstance(node, ast.FunctionDef):
                        complexity += 2
                    elif isinstance(node, ast.ClassDef):
                        complexity += 3
                
                total_complexity += complexity
                file_count += 1
                
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")
        
        return total_complexity / file_count if file_count > 0 else 0.0
    
    def _calculate_duplication(self, files: List[Path]) -> float:
        """Calculate code duplication percentage"""
        # Simplified duplication calculation
        # In a real implementation, this would use more sophisticated algorithms
        
        total_duplication = 0.0
        file_count = 0
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic duplication detection
                lines = content.splitlines()
                unique_lines = set(lines)
                
                if len(lines) > 0:
                    duplication = ((len(lines) - len(unique_lines)) / len(lines)) * 100
                    total_duplication += duplication
                    file_count += 1
                    
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")
        
        return total_duplication / file_count if file_count > 0 else 0.0
    
    def _calculate_overall_score(self, metrics: QualityMetrics) -> float:
        """Calculate overall quality score"""
        # Weighted average of all metrics
        weights = {
            'maintainability': 0.3,
            'readability': 0.3,
            'complexity': 0.2,
            'duplication': 0.2
        }
        
        # Normalize complexity (lower is better)
        normalized_complexity = max(0, 100 - (metrics.complexity * 5))
        
        overall_score = (
            metrics.maintainability * weights['maintainability'] +
            metrics.readability * weights['readability'] +
            normalized_complexity * weights['complexity'] +
            (100 - metrics.duplication) * weights['duplication']
        )
        
        return round(overall_score, 2)
    
    def validate_quality_gates(self, metrics: QualityMetrics) -> Dict[str, Any]:
        """Validate metrics against quality gates"""
        results = {
            'passed': True,
            'gates': [],
            'overall_status': 'PASSED'
        }
        
        for gate in self.quality_gates:
            if gate.name == 'complexity':
                # For complexity, lower is better
                passed = metrics.complexity <= gate.threshold
            else:
                # For other metrics, higher is better
                passed = getattr(metrics, gate.name) >= gate.threshold
            
            gate_result = {
                'name': gate.name,
                'threshold': gate.threshold,
                'actual': getattr(metrics, gate.name),
                'passed': passed,
                'severity': gate.severity,
                'description': gate.description
            }
            
            results['gates'].append(gate_result)
            
            if not passed and gate.severity == 'critical':
                results['passed'] = False
                results['overall_status'] = 'FAILED'
        
        return results
    
    def establish_baseline(self, codebase_path: str) -> QualityMetrics:
        """Establish baseline quality metrics"""
        logger.info("Establishing quality baseline...")
        self.baseline_metrics = self.analyze_codebase(codebase_path)
        logger.info(f"Baseline established: {self.baseline_metrics}")
        return self.baseline_metrics
    
    def validate_cleanup_operation(self, codebase_path: str) -> Dict[str, Any]:
        """Validate cleanup operation against baseline"""
        if not self.baseline_metrics:
            raise ValueError("Baseline metrics not established. Call establish_baseline() first.")
        
        logger.info("Validating cleanup operation...")
        self.current_metrics = self.analyze_codebase(codebase_path)
        
        # Compare with baseline
        comparison = self._compare_with_baseline()
        
        # Validate quality gates
        gate_validation = self.validate_quality_gates(self.current_metrics)
        
        return {
            'baseline': self.baseline_metrics,
            'current': self.current_metrics,
            'comparison': comparison,
            'quality_gates': gate_validation,
            'cleanup_status': 'APPROVED' if gate_validation['passed'] else 'REJECTED'
        }
    
    def _compare_with_baseline(self) -> Dict[str, Any]:
        """Compare current metrics with baseline"""
        if not self.baseline_metrics or not self.current_metrics:
            return {}
        
        comparison = {}
        
        for field in ['maintainability', 'readability', 'complexity', 'duplication', 'overall_score']:
            baseline_value = getattr(self.baseline_metrics, field)
            current_value = getattr(self.current_metrics, field)
            
            if field == 'complexity':
                # For complexity, lower is better
                improvement = baseline_value - current_value
                percentage_change = ((baseline_value - current_value) / baseline_value) * 100 if baseline_value > 0 else 0
            else:
                # For other metrics, higher is better
                improvement = current_value - baseline_value
                percentage_change = ((current_value - baseline_value) / baseline_value) * 100 if baseline_value > 0 else 0
            
            comparison[field] = {
                'baseline': baseline_value,
                'current': current_value,
                'improvement': improvement,
                'percentage_change': round(percentage_change, 2),
                'status': 'IMPROVED' if improvement > 0 else 'MAINTAINED' if improvement == 0 else 'DEGRADED'
            }
        
        return comparison
    
    def generate_report(self, validation_results: Dict[str, Any]) -> str:
        """Generate quality validation report"""
        report = []
        report.append("=" * 60)
        report.append("QUALITY VALIDATION REPORT - CLEANUP OPERATIONS")
        report.append("=" * 60)
        report.append(f"Overall Status: {validation_results['cleanup_status']}")
        report.append(f"Quality Gates: {validation_results['quality_gates']['overall_status']}")
        report.append("")
        
        # Quality Gates Results
        report.append("QUALITY GATES VALIDATION:")
        report.append("-" * 40)
        for gate in validation_results['quality_gates']['gates']:
            status = "✅ PASS" if gate['passed'] else "❌ FAIL"
            report.append(f"{gate['name'].upper()}: {status}")
            report.append(f"  Threshold: {gate['threshold']}, Actual: {gate['actual']}")
            report.append(f"  {gate['description']}")
            report.append("")
        
        # Comparison with Baseline
        report.append("COMPARISON WITH BASELINE:")
        report.append("-" * 40)
        for metric, data in validation_results['comparison'].items():
            report.append(f"{metric.upper()}:")
            report.append(f"  Baseline: {data['baseline']}")
            report.append(f"  Current: {data['current']}")
            report.append(f"  Change: {data['improvement']} ({data['percentage_change']}%)")
            report.append(f"  Status: {data['status']}")
            report.append("")
        
        return "\n".join(report)

def main():
    """Main function for testing the quality validation framework"""
    framework = QualityValidationFramework()
    
    # Example usage
    print("🚀 Quality Validation Framework for Cleanup Operations")
    print("=" * 60)
    
    # Establish baseline (simulate with current directory)
    try:
        baseline = framework.establish_baseline(".")
        print(f"✅ Baseline established: Overall Score = {baseline.overall_score}")
        
        # Simulate cleanup validation
        print("\n🔍 Validating cleanup operation...")
        validation_results = framework.validate_cleanup_operation(".")
        
        # Generate report
        report = framework.generate_report(validation_results)
        print("\n📊 Quality Validation Report:")
        print(report)
        
    except Exception as e:
        print(f"❌ Error during validation: {e}")

if __name__ == "__main__":
    main()
