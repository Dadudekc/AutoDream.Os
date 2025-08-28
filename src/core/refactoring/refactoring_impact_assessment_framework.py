#!/usr/bin/env python3
"""
Refactoring Impact Assessment Framework - Agent Cellphone V2
==========================================================

Framework for assessing refactoring impact and ROI.
Part of SPRINT ACCELERATION mission to reach INNOVATION PLANNING MODE.

Follows V2 coding standards: ≤300 lines per module, OOP design, SRP.
"""

import logging
import json
import time
import math
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta

from src.core.base_manager import BaseManager


class ImpactLevel(Enum):
    """Impact level enumeration."""
    NEGLIGIBLE = "negligible"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ImpactCategory(Enum):
    """Impact category enumeration."""
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    READABILITY = "readability"
    TESTABILITY = "testability"
    SECURITY = "security"
    COMPATIBILITY = "compatibility"


@dataclass
class ImpactMetric:
    """Impact metric data structure."""
    category: ImpactCategory
    level: ImpactLevel
    score: float
    description: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class RefactoringImpact:
    """Refactoring impact assessment."""
    refactoring_id: str
    timestamp: str
    before_metrics: Dict[str, float]
    after_metrics: Dict[str, float]
    impact_metrics: List[ImpactMetric]
    overall_impact_score: float
    roi_estimate: float
    risk_assessment: str
    recommendations: List[str]


class ImpactAssessmentFramework(BaseManager):
    """
    Refactoring Impact Assessment Framework.
    
    Assesses the impact of refactoring changes, calculates ROI,
    and provides risk assessment and recommendations.
    """
    
    def __init__(self):
        """Initialize Impact Assessment Framework."""
        super().__init__(
            manager_id="impact_assessment_framework",
            name="Refactoring Impact Assessment Framework",
            description="Framework for assessing refactoring impact and ROI"
        )
        
        self.impact_weights = self._initialize_impact_weights()
        self.assessment_history = []
        self.baseline_metrics = {}
        
    def _initialize_impact_weights(self) -> Dict[ImpactCategory, float]:
        """Initialize impact category weights."""
        return {
            ImpactCategory.PERFORMANCE: 0.25,
            ImpactCategory.MAINTAINABILITY: 0.30,
            ImpactCategory.READABILITY: 0.20,
            ImpactCategory.TESTABILITY: 0.15,
            ImpactCategory.SECURITY: 0.05,
            ImpactCategory.COMPATIBILITY: 0.05
        }
    
    def assess_refactoring_impact(self,
                                refactoring_id: str,
                                before_files: Dict[str, str],
                                after_files: Dict[str, str],
                                refactoring_effort: float = 1.0) -> RefactoringImpact:
        """
        Assess the impact of refactoring changes.
        
        Args:
            refactoring_id: Unique identifier for the refactoring
            before_files: Dictionary of file paths to original content
            after_files: Dictionary of file paths to refactored content
            refactoring_effort: Estimated effort in developer days
            
        Returns:
            Comprehensive impact assessment
        """
        start_time = time.time()
        
        self.logger.info(f"Starting impact assessment: {refactoring_id}")
        
        # Calculate before and after metrics
        before_metrics = self._calculate_system_metrics(before_files)
        after_metrics = self._calculate_system_metrics(after_files)
        
        # Calculate impact metrics
        impact_metrics = self._calculate_impact_metrics(before_metrics, after_metrics)
        
        # Calculate overall impact score
        overall_impact_score = self._calculate_overall_impact_score(impact_metrics)
        
        # Calculate ROI estimate
        roi_estimate = self._calculate_roi_estimate(before_metrics, after_metrics, refactoring_effort)
        
        # Assess risks
        risk_assessment = self._assess_risks(impact_metrics, before_metrics, after_metrics)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(impact_metrics, risk_assessment)
        
        # Create impact assessment
        assessment = RefactoringImpact(
            refactoring_id=refactoring_id,
            timestamp=datetime.now().isoformat(),
            before_metrics=before_metrics,
            after_metrics=after_metrics,
            impact_metrics=impact_metrics,
            overall_impact_score=overall_impact_score,
            roi_estimate=roi_estimate,
            risk_assessment=risk_assessment,
            recommendations=recommendations
        )
        
        # Store in history
        self.assessment_history.append(assessment)
        
        execution_time = time.time() - start_time
        self.logger.info(f"Impact assessment completed: {refactoring_id} in {execution_time:.2f}s")
        
        return assessment
    
    def _calculate_system_metrics(self, files: Dict[str, str]) -> Dict[str, float]:
        """Calculate comprehensive system metrics."""
        metrics = {
            "total_lines": 0,
            "total_functions": 0,
            "total_classes": 0,
            "average_complexity": 0,
            "duplication_ratio": 0,
            "documentation_coverage": 0,
            "test_coverage": 0,
            "import_dependencies": 0,
            "nested_depth": 0,
            "magic_numbers": 0
        }
        
        if not files:
            return metrics
        
        total_files = len(files)
        complexity_sum = 0
        documentation_lines = 0
        total_code_lines = 0
        
        for file_path, content in files.items():
            if not file_path.endswith('.py'):
                continue
                
            lines = content.splitlines()
            metrics["total_lines"] += len(lines)
            
            # Count functions and classes
            for line in lines:
                line = line.strip()
                if line.startswith('def '):
                    metrics["total_functions"] += 1
                elif line.startswith('class '):
                    metrics["total_classes"] += 1
                elif line.startswith('"""') or line.startswith("'''") or line.startswith('#'):
                    documentation_lines += 1
                elif line and not line.startswith('#'):
                    total_code_lines += 1
            
            # Calculate complexity
            complexity = self._calculate_file_complexity(content)
            complexity_sum += complexity
            
            # Count magic numbers
            magic_count = self._count_magic_numbers(content)
            metrics["magic_numbers"] += magic_count
        
        # Calculate averages and ratios
        if total_files > 0:
            metrics["average_complexity"] = complexity_sum / total_files
            metrics["duplication_ratio"] = self._calculate_duplication_ratio(files)
            metrics["documentation_coverage"] = (documentation_lines / metrics["total_lines"] * 100) if metrics["total_lines"] > 0 else 0
            metrics["import_dependencies"] = self._count_import_dependencies(files)
            metrics["nested_depth"] = self._calculate_average_nesting_depth(files)
        
        return metrics
    
    def _calculate_file_complexity(self, content: str) -> float:
        """Calculate complexity for a single file."""
        complexity = 0
        lines = content.splitlines()
        
        for line in lines:
            line = line.strip()
            if line.startswith(('if ', 'for ', 'while ', 'try:', 'except:', 'finally:', 'with ')):
                complexity += 1
            elif line.startswith('def '):
                complexity += 0.5
            elif line.startswith('class '):
                complexity += 0.3
        
        return complexity
    
    def _count_magic_numbers(self, content: str) -> int:
        """Count magic numbers in content."""
        import re
        magic_numbers = re.findall(r'\b\d{2,}\b', content)
        return len(magic_numbers)
    
    def _calculate_duplication_ratio(self, files: Dict[str, str]) -> float:
        """Calculate code duplication ratio."""
        if len(files) < 2:
            return 0.0
        
        all_content = " ".join(files.values())
        total_length = len(all_content)
        
        # Simple duplication detection
        duplication_score = 0
        for file_path, content in files.items():
            if len(content) > 100:  # Only check substantial files
                # Check for repeated patterns
                for other_path, other_content in files.items():
                    if file_path != other_path and len(other_content) > 100:
                        common_patterns = self._find_common_patterns(content, other_content)
                        duplication_score += common_patterns
        
        return min(duplication_score / total_length * 100, 100.0)
    
    def _find_common_patterns(self, content1: str, content2: str) -> float:
        """Find common patterns between two content strings."""
        # Simple pattern matching
        words1 = set(content1.split())
        words2 = set(content2.split())
        common_words = words1.intersection(words2)
        
        return len(common_words) / max(len(words1), len(words2)) * 100
    
    def _count_import_dependencies(self, files: Dict[str, str]) -> int:
        """Count import dependencies."""
        import re
        total_imports = 0
        
        for content in files.values():
            import_lines = re.findall(r'(?:from|import)\s+\w+', content)
            total_imports += len(import_lines)
        
        return total_imports
    
    def _calculate_average_nesting_depth(self, files: Dict[str, str]) -> float:
        """Calculate average nesting depth."""
        total_depth = 0
        file_count = 0
        
        for content in files.values():
            max_depth = 0
            current_depth = 0
            
            for line in content.splitlines():
                line = line.strip()
                if line.startswith(('if ', 'for ', 'while ', 'try:', 'except:', 'finally:', 'with ')):
                    current_depth += 1
                    max_depth = max(max_depth, current_depth)
                elif line.startswith(('elif ', 'else:')):
                    pass  # Same nesting level
                elif line and not line.startswith(('#', '"', "'")):
                    if line in ('pass', 'break', 'continue', 'return') or line.endswith(':'):
                        current_depth = max(0, current_depth - 1)
            
            total_depth += max_depth
            file_count += 1
        
        return total_depth / file_count if file_count > 0 else 0
    
    def _calculate_impact_metrics(self, before_metrics: Dict[str, float], after_metrics: Dict[str, float]) -> List[ImpactMetric]:
        """Calculate impact metrics for each category."""
        impact_metrics = []
        
        # Performance impact
        perf_score = self._calculate_performance_impact(before_metrics, after_metrics)
        impact_metrics.append(ImpactMetric(
            category=ImpactCategory.PERFORMANCE,
            level=self._score_to_level(perf_score),
            score=perf_score,
            description="Performance impact assessment",
            details={"before": before_metrics.get("average_complexity", 0), "after": after_metrics.get("average_complexity", 0)}
        ))
        
        # Maintainability impact
        maint_score = self._calculate_maintainability_impact(before_metrics, after_metrics)
        impact_metrics.append(ImpactMetric(
            category=ImpactCategory.MAINTAINABILITY,
            level=self._score_to_level(maint_score),
            score=maint_score,
            description="Maintainability impact assessment",
            details={"before": before_metrics.get("duplication_ratio", 0), "after": after_metrics.get("duplication_ratio", 0)}
        ))
        
        # Readability impact
        read_score = self._calculate_readability_impact(before_metrics, after_metrics)
        impact_metrics.append(ImpactMetric(
            category=ImpactCategory.READABILITY,
            level=self._score_to_level(read_score),
            score=read_score,
            description="Readability impact assessment",
            details={"before": before_metrics.get("documentation_coverage", 0), "after": after_metrics.get("documentation_coverage", 0)}
        ))
        
        # Testability impact
        test_score = self._calculate_testability_impact(before_metrics, after_metrics)
        impact_metrics.append(ImpactMetric(
            category=ImpactCategory.TESTABILITY,
            level=self._score_to_level(test_score),
            score=test_score,
            description="Testability impact assessment",
            details={"before": before_metrics.get("total_functions", 0), "after": after_metrics.get("total_functions", 0)}
        ))
        
        # Security impact
        sec_score = self._calculate_security_impact(before_metrics, after_metrics)
        impact_metrics.append(ImpactMetric(
            category=ImpactCategory.SECURITY,
            level=self._score_to_level(sec_score),
            score=sec_score,
            description="Security impact assessment"
        ))
        
        # Compatibility impact
        comp_score = self._calculate_compatibility_impact(before_metrics, after_metrics)
        impact_metrics.append(ImpactMetric(
            category=ImpactCategory.COMPATIBILITY,
            level=self._score_to_level(comp_score),
            score=comp_score,
            description="Compatibility impact assessment"
        ))
        
        return impact_metrics
    
    def _calculate_performance_impact(self, before: Dict[str, float], after: Dict[str, float]) -> float:
        """Calculate performance impact score."""
        before_complexity = before.get("average_complexity", 0)
        after_complexity = after.get("average_complexity", 0)
        
        if before_complexity == 0:
            return 0.0
        
        improvement = (before_complexity - after_complexity) / before_complexity * 100
        return max(-100, min(100, improvement))
    
    def _calculate_maintainability_impact(self, before: Dict[str, float], after: Dict[str, float]) -> float:
        """Calculate maintainability impact score."""
        before_duplication = before.get("duplication_ratio", 0)
        after_duplication = after.get("duplication_ratio", 0)
        
        if before_duplication == 0:
            return 0.0
        
        improvement = (before_duplication - after_duplication) / before_duplication * 100
        return max(-100, min(100, improvement))
    
    def _calculate_readability_impact(self, before: Dict[str, float], after: Dict[str, float]) -> float:
        """Calculate readability impact score."""
        before_docs = before.get("documentation_coverage", 0)
        after_docs = after.get("documentation_coverage", 0)
        
        improvement = after_docs - before_docs
        return max(-100, min(100, improvement))
    
    def _calculate_testability_impact(self, before: Dict[str, float], after: Dict[str, float]) -> float:
        """Calculate testability impact score."""
        before_functions = before.get("total_functions", 0)
        after_functions = after.get("total_functions", 0)
        
        if before_functions == 0:
            return 0.0
        
        # More functions generally means better testability
        improvement = (after_functions - before_functions) / before_functions * 100
        return max(-100, min(100, improvement))
    
    def _calculate_security_impact(self, before: Dict[str, float], after: Dict[str, float]) -> float:
        """Calculate security impact score."""
        # Placeholder for security assessment
        return 0.0
    
    def _calculate_compatibility_impact(self, before: Dict[str, float], after: Dict[str, float]) -> float:
        """Calculate compatibility impact score."""
        # Placeholder for compatibility assessment
        return 0.0
    
    def _score_to_level(self, score: float) -> ImpactLevel:
        """Convert numeric score to impact level."""
        if score >= 50:
            return ImpactLevel.CRITICAL
        elif score >= 25:
            return ImpactLevel.HIGH
        elif score >= 10:
            return ImpactLevel.MEDIUM
        elif score >= 1:
            return ImpactLevel.LOW
        else:
            return ImpactLevel.NEGLIGIBLE
    
    def _calculate_overall_impact_score(self, impact_metrics: List[ImpactMetric]) -> float:
        """Calculate overall impact score."""
        weighted_score = 0.0
        total_weight = 0.0
        
        for metric in impact_metrics:
            weight = self.impact_weights.get(metric.category, 0.1)
            weighted_score += metric.score * weight
            total_weight += weight
        
        return weighted_score / total_weight if total_weight > 0 else 0.0
    
    def _calculate_roi_estimate(self, before_metrics: Dict[str, float], after_metrics: Dict[str, float], effort: float) -> float:
        """Calculate ROI estimate for refactoring."""
        # Calculate improvement in key metrics
        complexity_improvement = (before_metrics.get("average_complexity", 0) - after_metrics.get("average_complexity", 0)) / max(before_metrics.get("average_complexity", 1), 1)
        duplication_improvement = (before_metrics.get("duplication_ratio", 0) - after_metrics.get("duplication_ratio", 0)) / max(before_metrics.get("duplication_ratio", 1), 1)
        
        # Estimate maintenance time savings
        maintenance_savings = (complexity_improvement + duplication_improvement) * 0.5
        
        # Calculate ROI
        if effort > 0:
            roi = (maintenance_savings * 100) / effort
            return max(-100, min(1000, roi))  # Cap ROI at reasonable bounds
        
        return 0.0
    
    def _assess_risks(self, impact_metrics: List[ImpactMetric], before_metrics: Dict[str, float], after_metrics: Dict[str, float]) -> str:
        """Assess overall risk level."""
        critical_issues = 0
        high_issues = 0
        
        for metric in impact_metrics:
            if metric.level == ImpactLevel.CRITICAL:
                critical_issues += 1
            elif metric.level == ImpactLevel.HIGH:
                high_issues += 1
        
        if critical_issues > 0:
            return "HIGH_RISK"
        elif high_issues > 2:
            return "MEDIUM_RISK"
        elif high_issues > 0:
            return "LOW_RISK"
        else:
            return "LOW_RISK"
    
    def _generate_recommendations(self, impact_metrics: List[ImpactMetric], risk_assessment: str) -> List[str]:
        """Generate recommendations based on impact assessment."""
        recommendations = []
        
        if risk_assessment == "HIGH_RISK":
            recommendations.append("Consider rolling back changes and implementing incrementally")
            recommendations.append("Increase testing coverage before deployment")
        
        for metric in impact_metrics:
            if metric.level == ImpactLevel.CRITICAL:
                recommendations.append(f"Address {metric.category.value} issues immediately")
            elif metric.level == ImpactLevel.HIGH:
                recommendations.append(f"Review {metric.category.value} changes before deployment")
        
        if not recommendations:
            recommendations.append("Refactoring appears safe to proceed")
        
        return recommendations
    
    def get_assessment_history(self) -> List[RefactoringImpact]:
        """Get assessment history."""
        return self.assessment_history.copy()
    
    def export_assessment_report(self, assessment: RefactoringImpact, output_path: str) -> bool:
        """Export assessment report to file."""
        try:
            with open(output_path, 'w') as f:
                json.dump(asdict(assessment), f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Failed to export assessment report: {e}")
            return False
    
    # BaseManager abstract method implementations
    def _on_start(self) -> bool:
        """Start the impact assessment framework."""
        try:
            self.logger.info("Starting Refactoring Impact Assessment Framework...")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start framework: {e}")
            return False
    
    def _on_stop(self):
        """Stop the impact assessment framework."""
        try:
            self.logger.info("Refactoring Impact Assessment Framework stopped")
        except Exception as e:
            self.logger.error(f"Error during framework shutdown: {e}")
    
    def _on_heartbeat(self):
        """Framework heartbeat."""
        try:
            history_size = len(self.assessment_history)
            self.logger.debug(f"Framework heartbeat - history size: {history_size}")
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
    
    def _on_initialize_resources(self) -> bool:
        """Initialize framework resources."""
        try:
            self.assessment_history.clear()
            return True
        except Exception as e:
            self.logger.error(f"Resource initialization failed: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup framework resources."""
        try:
            self.assessment_history.clear()
        except Exception as e:
            self.logger.error(f"Resource cleanup error: {e}")


def main():
    """CLI interface for Refactoring Impact Assessment Framework."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Refactoring Impact Assessment Framework")
    parser.add_argument("--assess", help="Assess refactoring impact")
    parser.add_argument("--history", action="store_true", help="Show assessment history")
    
    args = parser.parse_args()
    
    framework = ImpactAssessmentFramework()
    
    if args.assess:
        print(f"Impact assessment: {args.assess}")
    elif args.history:
        history = framework.get_assessment_history()
        print(f"Assessment History: {len(history)} assessments")
    else:
        print("Refactoring Impact Assessment Framework - Agent Cellphone V2")
        print("Use --assess or --history for assessment operations")


if __name__ == "__main__":
    main()
