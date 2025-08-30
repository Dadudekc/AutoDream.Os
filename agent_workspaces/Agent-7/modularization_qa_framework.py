#!/usr/bin/env python3
"""
Modularization Quality Assurance Framework - MODULAR-009 Mission
===============================================================

Comprehensive QA framework for ensuring quality of modularized components.
Implements automated quality checks, architecture validation, and compliance monitoring.

Author: Agent-7 - Quality Completion Optimization Manager
Mission: MODULAR-009 - Modularization Quality Assurance Framework
Priority: URGENT - Captain's Directive
"""

import ast
import json
import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class QualityMetric:
    """Represents a single quality metric measurement"""
    metric_name: str
    value: Any
    threshold: Any
    status: str  # PASS, FAIL, WARNING
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    recommendations: List[str]


@dataclass
class ModuleQualityReport:
    """Complete quality report for a single module"""
    module_path: str
    module_name: str
    timestamp: str
    overall_score: float
    overall_status: str
    metrics: List[QualityMetric]
    violations: List[str]
    recommendations: List[str]
    compliance_status: Dict[str, bool]


class CodeQualityAnalyzer:
    """Analyzes code quality metrics for modularized components"""
    
    def __init__(self):
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for quality analysis"""
        logger = logging.getLogger("CodeQualityAnalyzer")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def analyze_lines_of_code(self, file_path: str) -> QualityMetric:
        """Analyze lines of code compliance"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Count non-empty, non-comment lines
            code_lines = 0
            for line in lines:
                stripped = line.strip()
                if stripped and not stripped.startswith('#') and not stripped.startswith('"""'):
                    code_lines += 1
            
            # Determine threshold based on file type
            if 'gui' in file_path.lower() or 'interface' in file_path.lower():
                threshold = 600
                file_type = "GUI"
            else:
                threshold = 400
                file_type = "Standard"
            
            status = "PASS" if code_lines <= threshold else "FAIL"
            severity = "CRITICAL" if code_lines > threshold else "LOW"
            
            recommendations = []
            if code_lines > threshold:
                recommendations.append(f"Refactor to reduce from {code_lines} to ≤{threshold} lines")
                recommendations.append("Extract classes/functions into separate modules")
                recommendations.append("Apply Single Responsibility Principle")
            
            return QualityMetric(
                metric_name="Lines of Code",
                value=code_lines,
                threshold=f"≤{threshold} ({file_type})",
                status=status,
                severity=severity,
                description=f"Module contains {code_lines} lines of code",
                recommendations=recommendations
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing LOC for {file_path}: {e}")
            return QualityMetric(
                metric_name="Lines of Code",
                value="ERROR",
                threshold="N/A",
                status="FAIL",
                severity="CRITICAL",
                description=f"Failed to analyze: {e}",
                recommendations=["Fix file access issues", "Verify file encoding"]
            )
    
    def analyze_single_responsibility(self, file_path: str) -> QualityMetric:
        """Analyze Single Responsibility Principle compliance"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST to analyze class and function responsibilities
            tree = ast.parse(content)
            
            class_count = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            function_count = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            
            # Calculate responsibility score
            total_methods = class_count + function_count
            if total_methods == 0:
                score = 100  # No methods means no responsibility violations
            else:
                # Penalize files with too many responsibilities
                if total_methods <= 5:
                    score = 100
                elif total_methods <= 10:
                    score = 80
                elif total_methods <= 15:
                    score = 60
                else:
                    score = 40
            
            status = "PASS" if score >= 80 else "WARNING" if score >= 60 else "FAIL"
            severity = "HIGH" if score < 60 else "MEDIUM" if score < 80 else "LOW"
            
            recommendations = []
            if score < 80:
                recommendations.append("Split file into multiple focused modules")
                recommendations.append("Group related functionality into separate classes")
                recommendations.append("Extract utility functions to dedicated modules")
            
            return QualityMetric(
                metric_name="Single Responsibility Principle",
                value=f"{score}/100",
                threshold="≥80/100",
                status=status,
                severity=severity,
                description=f"File has {total_methods} methods/classes (score: {score})",
                recommendations=recommendations
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing SRP for {file_path}: {e}")
            return QualityMetric(
                metric_name="Single Responsibility Principle",
                value="ERROR",
                threshold="≥80/100",
                status="FAIL",
                severity="CRITICAL",
                description=f"Failed to analyze: {e}",
                recommendations=["Fix syntax errors", "Verify Python compatibility"]
            )
    
    def analyze_dependency_injection(self, file_path: str) -> QualityMetric:
        """Analyze dependency injection compliance"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for dependency injection patterns
            di_patterns = [
                r'def __init__\(self[^)]*\):',
                r'def __init__\(self, [^)]*\):',
                r'@inject',
                r'@dependency',
                r'def configure\([^)]*\):',
                r'def setup\([^)]*\):'
            ]
            
            di_score = 0
            found_patterns = []
            
            for pattern in di_patterns:
                if re.search(pattern, content, re.MULTILINE):
                    di_score += 20
                    found_patterns.append(pattern)
            
            # Check for hardcoded dependencies
            hardcoded_patterns = [
                r'import\s+\w+',
                r'from\s+\w+\s+import',
                r'new\s+\w+\(',
                r'\w+\(\s*\)'
            ]
            
            hardcoded_count = 0
            for pattern in hardcoded_patterns:
                matches = re.findall(pattern, content)
                hardcoded_count += len(matches)
            
            # Adjust score based on hardcoded dependencies
            if hardcoded_count > 10:
                di_score = max(0, di_score - 30)
            elif hardcoded_count > 5:
                di_score = max(0, di_score - 15)
            
            status = "PASS" if di_score >= 60 else "WARNING" if di_score >= 40 else "FAIL"
            severity = "HIGH" if di_score < 40 else "MEDIUM" if di_score < 60 else "LOW"
            
            recommendations = []
            if di_score < 60:
                recommendations.append("Implement dependency injection patterns")
                recommendations.append("Use constructor injection for dependencies")
                recommendations.append("Avoid hardcoded class instantiations")
                recommendations.append("Consider using a DI container")
            
            return QualityMetric(
                metric_name="Dependency Injection",
                value=f"{di_score}/100",
                threshold="≥60/100",
                status=status,
                severity=severity,
                description=f"DI compliance score: {di_score}, hardcoded deps: {hardcoded_count}",
                recommendations=recommendations
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing DI for {file_path}: {e}")
            return QualityMetric(
                metric_name="Dependency Injection",
                value="ERROR",
                threshold="≥60/100",
                status="FAIL",
                severity="CRITICAL",
                description=f"Failed to analyze: {e}",
                recommendations=["Fix syntax errors", "Verify file format"]
            )


class ArchitectureValidator:
    """Validates architecture compliance for modularized components"""
    
    def __init__(self):
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for architecture validation"""
        logger = logging.getLogger("ArchitectureValidator")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def validate_module_interfaces(self, file_path: str) -> QualityMetric:
        """Validate module interface consistency"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for proper interface definitions
            interface_patterns = [
                r'class\s+\w+\([^)]*\):',
                r'def\s+\w+\([^)]*\):',
                r'@abstractmethod',
                r'@interface',
                r'Protocol\[',
                r'typing\.Protocol'
            ]
            
            interface_score = 0
            found_patterns = []
            
            for pattern in interface_patterns:
                if re.search(pattern, content, re.MULTILINE):
                    interface_score += 15
                    found_patterns.append(pattern)
            
            # Check for proper type hints
            type_hint_patterns = [
                r':\s*\w+\[',
                r':\s*Optional\[',
                r':\s*List\[',
                r':\s*Dict\[',
                r':\s*Tuple\[',
                r':\s*Union\['
            ]
            
            type_hint_count = 0
            for pattern in type_hint_patterns:
                matches = re.findall(pattern, content)
                type_hint_count += len(matches)
            
            if type_hint_count > 5:
                interface_score += 25
            
            status = "PASS" if interface_score >= 60 else "WARNING" if interface_score >= 40 else "FAIL"
            severity = "HIGH" if interface_score < 40 else "MEDIUM" if interface_score < 60 else "LOW"
            
            recommendations = []
            if interface_score < 60:
                recommendations.append("Define clear class interfaces")
                recommendations.append("Use proper inheritance patterns")
                recommendations.append("Add comprehensive type hints")
                recommendations.append("Implement abstract base classes where appropriate")
            
            return QualityMetric(
                metric_name="Module Interface Consistency",
                value=f"{interface_score}/100",
                threshold="≥60/100",
                status=status,
                severity=severity,
                description=f"Interface score: {interface_score}, type hints: {type_hint_count}",
                recommendations=recommendations
            )
            
        except Exception as e:
            self.logger.error(f"Error validating interfaces for {file_path}: {e}")
            return QualityMetric(
                metric_name="Module Interface Consistency",
                value="ERROR",
                threshold="≥60/100",
                status="FAIL",
                severity="CRITICAL",
                description=f"Failed to validate: {e}",
                recommendations=["Fix syntax errors", "Verify file format"]
            )
    
    def validate_ssot_compliance(self, file_path: str) -> QualityMetric:
        """Validate Single Source of Truth compliance"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for potential SSOT violations
            ssot_violations = [
                r'class\s+\w+Manager',
                r'class\s+\w+Handler',
                r'class\s+\w+Controller',
                r'def\s+get_\w+',
                r'def\s+set_\w+',
                r'def\s+update_\w+',
                r'def\s+delete_\w+'
            ]
            
            violation_count = 0
            found_violations = []
            
            for pattern in ssot_violations:
                matches = re.findall(pattern, content)
                if matches:
                    violation_count += len(matches)
                    found_violations.extend(matches)
            
            # Calculate SSOT compliance score
            if violation_count == 0:
                ssot_score = 100
            elif violation_count <= 3:
                ssot_score = 80
            elif violation_count <= 6:
                ssot_score = 60
            else:
                ssot_score = 40
            
            status = "PASS" if ssot_score >= 80 else "WARNING" if ssot_score >= 60 else "FAIL"
            severity = "HIGH" if ssot_score < 60 else "MEDIUM" if ssot_score < 80 else "LOW"
            
            recommendations = []
            if ssot_score < 80:
                recommendations.append("Review data access patterns")
                recommendations.append("Consolidate data management into single modules")
                recommendations.append("Avoid duplicate data handling logic")
                recommendations.append("Implement centralized data access layer")
            
            return QualityMetric(
                metric_name="SSOT Compliance",
                value=f"{ssot_score}/100",
                threshold="≥80/100",
                status=status,
                severity=severity,
                description=f"SSOT score: {ssot_score}, potential violations: {violation_count}",
                recommendations=recommendations
            )
            
        except Exception as e:
            self.logger.error(f"Error validating SSOT for {file_path}: {e}")
            return QualityMetric(
                metric_name="SSOT Compliance",
                value="ERROR",
                threshold="≥80/100",
                status="FAIL",
                severity="CRITICAL",
                description=f"Failed to validate: {e}",
                recommendations=["Fix syntax errors", "Verify file format"]
            )


class ModularizationQAFramework:
    """Main QA framework for modularized components"""
    
    def __init__(self):
        self.code_analyzer = CodeQualityAnalyzer()
        self.arch_validator = ArchitectureValidator()
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the QA framework"""
        logger = logging.getLogger("ModularizationQAFramework")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def analyze_module_quality(self, file_path: str) -> ModuleQualityReport:
        """Analyze quality of a single module"""
        self.logger.info(f"Analyzing module quality: {file_path}")
        
        # Run all quality checks
        metrics = []
        
        # Code quality metrics
        metrics.append(self.code_analyzer.analyze_lines_of_code(file_path))
        metrics.append(self.code_analyzer.analyze_single_responsibility(file_path))
        metrics.append(self.code_analyzer.analyze_dependency_injection(file_path))
        
        # Architecture validation metrics
        metrics.append(self.arch_validator.validate_module_interfaces(file_path))
        metrics.append(self.arch_validator.validate_ssot_compliance(file_path))
        
        # Calculate overall score
        total_score = 0
        valid_metrics = 0
        
        for metric in metrics:
            if isinstance(metric.value, (int, float)) or (isinstance(metric.value, str) and '/' in str(metric.value)):
                try:
                    if '/' in str(metric.value):
                        score = int(str(metric.value).split('/')[0])
                    else:
                        score = float(metric.value)
                    total_score += score
                    valid_metrics += 1
                except (ValueError, IndexError):
                    continue
        
        overall_score = total_score / valid_metrics if valid_metrics > 0 else 0
        
        # Determine overall status
        if overall_score >= 80:
            overall_status = "EXCELLENT"
        elif overall_score >= 60:
            overall_status = "GOOD"
        elif overall_score >= 40:
            overall_status = "FAIR"
        else:
            overall_status = "POOR"
        
        # Collect violations and recommendations
        violations = []
        recommendations = []
        
        for metric in metrics:
            if metric.status == "FAIL":
                violations.append(f"{metric.metric_name}: {metric.description}")
            recommendations.extend(metric.recommendations)
        
        # Remove duplicate recommendations
        recommendations = list(set(recommendations))
        
        # Compliance status
        compliance_status = {
            "loc_compliant": any(m.metric_name == "Lines of Code" and m.status == "PASS" for m in metrics),
            "srp_compliant": any(m.metric_name == "Single Responsibility Principle" and m.status == "PASS" for m in metrics),
            "di_compliant": any(m.metric_name == "Dependency Injection" and m.status == "PASS" for m in metrics),
            "interface_compliant": any(m.metric_name == "Module Interface Consistency" and m.status == "PASS" for m in metrics),
            "ssot_compliant": any(m.metric_name == "SSOT Compliance" and m.status == "PASS" for m in metrics)
        }
        
        return ModuleQualityReport(
            module_path=file_path,
            module_name=Path(file_path).name,
            timestamp=datetime.now().isoformat(),
            overall_score=overall_score,
            overall_status=overall_status,
            metrics=metrics,
            violations=violations,
            recommendations=recommendations,
            compliance_status=compliance_status
        )
    
    def generate_quality_report(self, file_path: str, output_file: Optional[str] = None) -> str:
        """Generate and optionally save a quality report"""
        report = self.analyze_module_quality(file_path)
        
        # Format report
        report_text = self._format_report_text(report)
        
        # Save to file if specified
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(report_text)
                self.logger.info(f"Quality report saved to: {output_file}")
            except Exception as e:
                self.logger.error(f"Failed to save report: {e}")
        
        return report_text
    
    def _format_report_text(self, report: ModuleQualityReport) -> str:
        """Format quality report as text"""
        output = []
        
        # Header
        output.append("=" * 80)
        output.append("MODULARIZATION QUALITY ASSURANCE REPORT")
        output.append("=" * 80)
        output.append(f"Module: {report.module_name}")
        output.append(f"Path: {report.module_path}")
        output.append(f"Timestamp: {report.timestamp}")
        output.append(f"Overall Score: {report.overall_score:.1f}/100")
        output.append(f"Overall Status: {report.overall_status}")
        
        # Compliance Summary
        output.append("")
        output.append("COMPLIANCE SUMMARY:")
        output.append("-" * 40)
        for compliance, status in report.compliance_status.items():
            status_icon = "✅" if status else "❌"
            output.append(f"{status_icon} {compliance.replace('_', ' ').title()}: {'COMPLIANT' if status else 'NON-COMPLIANT'}")
        
        # Quality Metrics
        output.append("")
        output.append("QUALITY METRICS:")
        output.append("-" * 40)
        for metric in report.metrics:
            status_icon = "✅" if metric.status == "PASS" else "❌" if metric.status == "FAIL" else "⚠️"
            output.append(f"\n{status_icon} {metric.metric_name}")
            output.append(f"   Value: {metric.value}")
            output.append(f"   Threshold: {metric.threshold}")
            output.append(f"   Status: {metric.status}")
            output.append(f"   Severity: {metric.severity}")
            output.append(f"   Description: {metric.description}")
            
            if metric.recommendations:
                output.append("   Recommendations:")
                for rec in metric.recommendations:
                    output.append(f"     • {rec}")
        
        # Violations
        if report.violations:
            output.append("")
            output.append("VIOLATIONS DETECTED:")
            output.append("-" * 40)
            for violation in report.violations:
                output.append(f"❌ {violation}")
        
        # Recommendations
        if report.recommendations:
            output.append("")
            output.append("OVERALL RECOMMENDATIONS:")
            output.append("-" * 40)
            for i, recommendation in enumerate(report.recommendations, 1):
                output.append(f"{i}. {recommendation}")
        
        return "\n".join(output)


def main():
    """Main entry point for the QA framework"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Modularization Quality Assurance Framework - MODULAR-009 Mission",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python modularization_qa_framework.py module.py
  python modularization_qa_framework.py module.py --output report.txt
  python modularization_qa_framework.py --help
        """
    )
    
    parser.add_argument(
        "file_path",
        help="Path to the Python module to analyze"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file for the quality report"
    )
    
    args = parser.parse_args()
    
    # Initialize QA framework
    qa_framework = ModularizationQAFramework()
    
    # Generate quality report
    try:
        report = qa_framework.generate_quality_report(args.file_path, args.output)
        print(report)
    except Exception as e:
        print(f"Error generating quality report: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
