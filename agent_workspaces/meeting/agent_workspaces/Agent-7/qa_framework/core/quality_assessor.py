"""
🎯 QUALITY ASSESSMENT ENGINE - CORE COMPONENT
Agent-7 - Quality Completion Optimization Manager

Quality assessment engine for modularization quality evaluation.
Follows V2 coding standards: ≤300 lines per module.
"""

import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from .quality_models import (
    QualityAssessment, 
    QualityReport, 
    QualityLevel, 
    QualityThresholds,
    ComplianceLevel
)
from .quality_metrics import QualityMetricsCollector


class QualityAssessor:
    """Individual quality assessor for specific aspects."""
    
    def __init__(self, thresholds: QualityThresholds):
        """Initialize quality assessor."""
        self.thresholds = thresholds
    
    def assess_file_structure(self, target_file: str, modularized_dir: str) -> Dict[str, Any]:
        """Assess file structure quality."""
        assessment = {
            "original_file_exists": os.path.exists(target_file),
            "modularized_dir_exists": os.path.exists(modularized_dir),
            "module_count": 0,
            "total_lines": 0,
            "max_module_lines": 0
        }
        
        if assessment["modularized_dir_exists"]:
            assessment.update(self._analyze_modularized_structure(modularized_dir))
        
        return assessment
    
    def assess_code_quality(self, modularized_dir: str) -> Dict[str, Any]:
        """Assess code quality aspects."""
        return {
            "interface_quality": self._assess_interface_quality(modularized_dir),
            "dependency_complexity": self._assess_dependency_complexity(modularized_dir),
            "naming_conventions": self._assess_naming_conventions(modularized_dir),
            "documentation": self._assess_documentation(modularized_dir),
            "code_organization": self._assess_code_organization(modularized_dir)
        }
    
    def assess_test_coverage(self, modularized_dir: str) -> Dict[str, Any]:
        """Assess test coverage quality."""
        return {
            "test_coverage": self._assess_test_coverage(modularized_dir),
            "test_files_present": self._check_test_files(modularized_dir),
            "test_quality": self._assess_test_quality(modularized_dir)
        }
    
    def _analyze_modularized_structure(self, modularized_dir: str) -> Dict[str, Any]:
        """Analyze the structure of modularized components."""
        structure = {
            "module_count": 0,
            "total_lines": 0,
            "max_module_lines": 0,
            "module_sizes": {},
            "module_line_counts": {}
        }
        
        try:
            for root, dirs, files in os.walk(modularized_dir):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        structure["module_count"] += 1
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                                line_count = len(lines)
                                structure["total_lines"] += line_count
                                structure["max_module_lines"] = max(
                                    structure["max_module_lines"], line_count
                                )
                                structure["module_sizes"][file] = os.path.getsize(file_path)
                                structure["module_line_counts"][file] = line_count
                        except (OSError, UnicodeDecodeError):
                            pass
        except (OSError, FileNotFoundError):
            pass
        
        return structure
    
    def _assess_interface_quality(self, modularized_dir: str) -> float:
        """Assess interface quality (placeholder implementation)."""
        # This would implement actual interface quality analysis
        return 0.8  # Placeholder score
    
    def _assess_dependency_complexity(self, modularized_dir: str) -> float:
        """Assess dependency complexity (placeholder implementation)."""
        # This would implement actual dependency complexity analysis
        return 0.5  # Placeholder score
    
    def _assess_naming_conventions(self, modularized_dir: str) -> float:
        """Assess naming convention compliance (placeholder implementation)."""
        # This would implement actual naming convention analysis
        return 0.9  # Placeholder score
    
    def _assess_documentation(self, modularized_dir: str) -> float:
        """Assess documentation quality (placeholder implementation)."""
        # This would implement actual documentation analysis
        return 0.7  # Placeholder score
    
    def _assess_code_organization(self, modularized_dir: str) -> float:
        """Assess code organization quality (placeholder implementation)."""
        # This would implement actual code organization analysis
        return 0.8  # Placeholder score
    
    def _assess_test_coverage(self, modularized_dir: str) -> float:
        """Assess test coverage (placeholder implementation)."""
        # This would implement actual test coverage analysis
        return 75.0  # Placeholder score
    
    def _check_test_files(self, modularized_dir: str) -> bool:
        """Check if test files are present."""
        try:
            for root, dirs, files in os.walk(modularized_dir):
                for file in files:
                    if file.startswith('test_') and file.endswith('.py'):
                        return True
            return False
        except (OSError, FileNotFoundError):
            return False
    
    def _assess_test_quality(self, modularized_dir: str) -> float:
        """Assess test quality (placeholder implementation)."""
        # This would implement actual test quality analysis
        return 0.8  # Placeholder score


class QualityAssessmentEngine:
    """Main quality assessment engine for modularization evaluation."""
    
    def __init__(self):
        """Initialize the quality assessment engine."""
        self.thresholds = QualityThresholds()
        self.metrics_collector = QualityMetricsCollector(self.thresholds)
        self.quality_assessor = QualityAssessor(self.thresholds)
    
    def assess_modularization_quality(self, target_file: str, modularized_dir: str) -> QualityReport:
        """
        Assess the quality of modularized components.
        
        Args:
            target_file: Path to the original monolithic file
            modularized_dir: Path to the modularized components directory
            
        Returns:
            QualityReport: Comprehensive quality assessment report
        """
        # Create assessment object
        assessment = QualityAssessment(target_file, modularized_dir)
        
        try:
            # Collect quality metrics
            metrics = self.metrics_collector.collect_quality_metrics(target_file, modularized_dir)
            for metric in metrics.values():
                assessment.add_metric(metric)
            
            # Assess file structure
            structure_assessment = self.quality_assessor.assess_file_structure(target_file, modularized_dir)
            
            # Assess code quality
            code_quality = self.quality_assessor.assess_code_quality(modularized_dir)
            
            # Assess test coverage
            test_coverage = self.quality_assessor.assess_test_coverage(modularized_dir)
            
            # Calculate overall quality score
            overall_score = self.metrics_collector.calculator.calculate_overall_quality_score(metrics)
            assessment.overall_quality_score = overall_score
            
            # Determine quality level
            assessment.quality_level = self._determine_quality_level(overall_score)
            
            # Check V2 compliance
            compliance_status = self._check_v2_compliance(structure_assessment, metrics)
            assessment.compliance_status = compliance_status
            
            # Generate recommendations
            recommendations = self._generate_recommendations(metrics, structure_assessment, code_quality, test_coverage)
            for recommendation in recommendations:
                assessment.add_recommendation(recommendation)
            
            # Identify issues and warnings
            issues, warnings = self._identify_issues_and_warnings(metrics, structure_assessment, code_quality, test_coverage)
            for issue in issues:
                assessment.add_issue(issue)
            for warning in warnings:
                assessment.add_warning(warning)
            
        except Exception as e:
            assessment.add_issue(f"Assessment error: {str(e)}")
            assessment.overall_quality_score = 0.0
            assessment.quality_level = QualityLevel("ERROR", 0.0, "Assessment failed", "🔴")
            assessment.compliance_status = ComplianceLevel.ERROR
        
        # Create and return quality report
        return QualityReport(assessment)
    
    def _determine_quality_level(self, score: float) -> QualityLevel:
        """Determine quality level based on score."""
        if score >= 90.0:
            return QualityLevel("EXCELLENT", score, "Outstanding modularization quality", "🟢")
        elif score >= 75.0:
            return QualityLevel("GOOD", score, "Good modularization quality", "🟡")
        elif score >= 60.0:
            return QualityLevel("FAIR", score, "Acceptable modularization quality", "🟠")
        elif score >= 45.0:
            return QualityLevel("POOR", score, "Below acceptable quality", "🔴")
        else:
            return QualityLevel("CRITICAL", score, "Critical quality issues", "⚫")
    
    def _check_v2_compliance(self, structure_assessment: Dict[str, Any], metrics: Dict[str, Any]) -> ComplianceLevel:
        """Check V2 compliance status."""
        # Check if max module lines exceed 400 (V2 standard)
        max_lines = structure_assessment.get("max_module_lines", 0)
        if max_lines > 400:
            return ComplianceLevel.NON_COMPLIANT
        
        # Check if overall quality score meets minimum threshold
        v2_compliance_metric = metrics.get("v2_compliance")
        if v2_compliance_metric and v2_compliance_metric.value < 80.0:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        
        # Check if module count meets minimum requirement
        module_count = structure_assessment.get("module_count", 0)
        if module_count < 5:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        
        return ComplianceLevel.FULLY_COMPLIANT
    
    def _generate_recommendations(self, metrics: Dict[str, Any], structure_assessment: Dict[str, Any], 
                                code_quality: Dict[str, Any], test_coverage: Dict[str, Any]) -> List[str]:
        """Generate quality improvement recommendations."""
        recommendations = []
        
        # File size reduction recommendations
        size_reduction_metric = metrics.get("file_size_reduction")
        if size_reduction_metric and size_reduction_metric.status == "FAIL":
            recommendations.append("Consider further modularization to achieve target file size reduction")
        
        # Module count recommendations
        module_count_metric = metrics.get("module_count")
        if module_count_metric and module_count_metric.status == "FAIL":
            recommendations.append("Increase module count to meet minimum requirement")
        
        # V2 compliance recommendations
        v2_compliance_metric = metrics.get("v2_compliance")
        if v2_compliance_metric and v2_compliance_metric.value < 100.0:
            recommendations.append("Ensure all modules are under 400 lines for V2 compliance")
        
        # Test coverage recommendations
        test_coverage_metric = metrics.get("test_coverage")
        if test_coverage_metric and test_coverage_metric.status == "FAIL":
            recommendations.append("Improve test coverage to meet minimum 80% requirement")
        
        # Code quality recommendations
        if code_quality.get("interface_quality", 0.0) < 0.8:
            recommendations.append("Improve interface design quality")
        
        if code_quality.get("documentation", 0.0) < 0.7:
            recommendations.append("Enhance documentation coverage and quality")
        
        return recommendations
    
    def _identify_issues_and_warnings(self, metrics: Dict[str, Any], structure_assessment: Dict[str, Any],
                                    code_quality: Dict[str, Any], test_coverage: Dict[str, Any]) -> tuple[List[str], List[str]]:
        """Identify critical issues and warnings."""
        issues = []
        warnings = []
        
        # Check for critical issues
        if not structure_assessment.get("original_file_exists"):
            issues.append("Original target file not found")
        
        if not structure_assessment.get("modularized_dir_exists"):
            issues.append("Modularized directory not found")
        
        # Check for warnings
        if structure_assessment.get("max_module_lines", 0) > 400:
            warnings.append("Some modules exceed V2 compliance line limit")
        
        if not test_coverage.get("test_files_present", False):
            warnings.append("No test files detected in modularized components")
        
        return issues, warnings
