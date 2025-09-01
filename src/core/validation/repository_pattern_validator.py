#!/usr/bin/env python3
"""
Repository Pattern Validator - Agent Cellphone V2
===============================================

Advanced validation system for repository pattern implementation.
Provides comprehensive validation for repository pattern compliance,
modular architecture patterns, and V2 compliance standards.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import re
import os
import ast
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .validation_models import ValidationIssue, ValidationSeverity


class RepositoryPatternType(Enum):
    """Types of repository patterns."""
    INTERFACE = "interface"
    IMPLEMENTATION = "implementation"
    SERVICE = "service"
    FACTORY = "factory"
    UNIT_OF_WORK = "unit_of_work"


@dataclass
class RepositoryPatternMetrics:
    """Repository pattern validation metrics."""
    file_path: str
    pattern_type: RepositoryPatternType
    interface_count: int
    implementation_count: int
    method_count: int
    dependency_injection_count: int
    abstraction_level: float
    coupling_score: float
    cohesion_score: float
    v2_compliant: bool
    violations: List[str] = field(default_factory=list)


class RepositoryPatternValidator:
    """
    Advanced repository pattern validator for V2 compliance.
    
    Provides comprehensive validation for:
    - Repository pattern implementation compliance
    - Modular architecture patterns
    - Dependency injection validation
    - Interface segregation and abstraction
    - V2 compliance standards
    """

    def __init__(self):
        """Initialize the repository pattern validator."""
        self.pattern_thresholds = {
            "max_methods_per_interface": 10,
            "max_methods_per_implementation": 20,
            "min_abstraction_level": 0.7,
            "max_coupling_score": 0.3,
            "min_cohesion_score": 0.8,
            "max_file_lines": 300,
            "min_interface_segregation": 0.8
        }
        
        self.pattern_indicators = {
            "repository_keywords": ["Repository", "Repo", "DataAccess", "Persistence"],
            "interface_keywords": ["Interface", "I", "Contract", "Abstract"],
            "service_keywords": ["Service", "Manager", "Handler", "Controller"],
            "factory_keywords": ["Factory", "Builder", "Creator", "Provider"],
            "dependency_keywords": ["Dependency", "Inject", "DI", "Container"]
        }

    def validate_repository_pattern(self, file_path: str) -> List[ValidationIssue]:
        """
        Validate repository pattern implementation in a file.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            List of validation issues
        """
        issues = []
        
        try:
            if not os.path.exists(file_path):
                issues.append(ValidationIssue(
                    rule_id="file_not_found",
                    rule_name="File Not Found",
                    severity=ValidationSeverity.ERROR,
                    message=f"Repository pattern file not found: {file_path}",
                    details={"file_path": file_path},
                    timestamp=datetime.now(),
                    component="repository_pattern_validator"
                ))
                return issues

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyze file metrics
            metrics = self._analyze_repository_metrics(file_path, content)
            
            # Validate against repository pattern rules
            issues.extend(self._validate_pattern_structure(metrics, content))
            issues.extend(self._validate_interface_segregation(metrics, content))
            issues.extend(self._validate_dependency_injection(metrics, content))
            issues.extend(self._validate_abstraction_level(metrics, content))
            issues.extend(self._validate_coupling_cohesion(metrics, content))
            issues.extend(self._validate_v2_compliance(metrics, content))
            
        except Exception as e:
            issues.append(ValidationIssue(
                rule_id="repository_analysis_error",
                rule_name="Repository Analysis Error",
                severity=ValidationSeverity.ERROR,
                message=f"Failed to analyze repository pattern in {file_path}: {str(e)}",
                details={"file_path": file_path, "error": str(e)},
                timestamp=datetime.now(),
                component="repository_pattern_validator"
            ))
        
        return issues

    def _analyze_repository_metrics(self, file_path: str, content: str) -> RepositoryPatternMetrics:
        """Analyze repository pattern metrics from file content."""
        lines = content.split('\n')
        total_lines = len(lines)
        
        # Count interfaces and implementations
        interface_count = len(re.findall(r'(?:interface|abstract class)\s+\w+', content, re.IGNORECASE))
        implementation_count = len(re.findall(r'class\s+\w+.*implements', content, re.IGNORECASE))
        
        # Count methods
        method_count = len(re.findall(r'(?:public|private|protected)?\s*(?:async\s+)?(?:function|\w+)\s*\([^)]*\)\s*\{', content))
        
        # Count dependency injection patterns
        di_count = len(re.findall(r'constructor\s*\([^)]*\)', content)) + len(re.findall(r'@inject|@Injectable', content))
        
        # Calculate abstraction level
        abstraction_level = self._calculate_abstraction_level(content)
        
        # Calculate coupling and cohesion scores
        coupling_score = self._calculate_coupling_score(content)
        cohesion_score = self._calculate_cohesion_score(content)
        
        # Determine pattern type
        pattern_type = self._determine_pattern_type(content)
        
        return RepositoryPatternMetrics(
            file_path=file_path,
            pattern_type=pattern_type,
            interface_count=interface_count,
            implementation_count=implementation_count,
            method_count=method_count,
            dependency_injection_count=di_count,
            abstraction_level=abstraction_level,
            coupling_score=coupling_score,
            cohesion_score=cohesion_score,
            v2_compliant=True  # Will be updated based on validation
        )

    def _determine_pattern_type(self, content: str) -> RepositoryPatternType:
        """Determine the type of repository pattern."""
        content_lower = content.lower()
        
        # Check for repository keywords
        for keyword in self.pattern_indicators["repository_keywords"]:
            if keyword.lower() in content_lower:
                return RepositoryPatternType.REPOSITORY
        
        # Check for interface keywords
        for keyword in self.pattern_indicators["interface_keywords"]:
            if keyword.lower() in content_lower:
                return RepositoryPatternType.INTERFACE
        
        # Check for service keywords
        for keyword in self.pattern_indicators["service_keywords"]:
            if keyword.lower() in content_lower:
                return RepositoryPatternType.SERVICE
        
        # Check for factory keywords
        for keyword in self.pattern_indicators["factory_keywords"]:
            if keyword.lower() in content_lower:
                return RepositoryPatternType.FACTORY
        
        return RepositoryPatternType.IMPLEMENTATION

    def _calculate_abstraction_level(self, content: str) -> float:
        """Calculate abstraction level of the repository pattern."""
        # Count abstract elements (interfaces, abstract classes, abstract methods)
        abstract_elements = len(re.findall(r'abstract\s+', content, re.IGNORECASE))
        interface_elements = len(re.findall(r'interface\s+\w+', content, re.IGNORECASE))
        
        # Count concrete elements (classes, methods)
        concrete_elements = len(re.findall(r'class\s+\w+', content, re.IGNORECASE))
        method_elements = len(re.findall(r'(?:public|private|protected)?\s*(?:async\s+)?(?:function|\w+)\s*\(', content))
        
        total_abstract = abstract_elements + interface_elements
        total_concrete = concrete_elements + method_elements
        
        if total_concrete == 0:
            return 1.0  # Fully abstract
        
        return total_abstract / (total_abstract + total_concrete)

    def _calculate_coupling_score(self, content: str) -> float:
        """Calculate coupling score (lower is better)."""
        # Count external dependencies (imports, requires)
        external_deps = len(re.findall(r'(?:import|require|from)\s+', content))
        
        # Count internal dependencies (class references, method calls)
        internal_deps = len(re.findall(r'new\s+\w+\(', content)) + len(re.findall(r'this\.\w+', content))
        
        total_deps = external_deps + internal_deps
        if total_deps == 0:
            return 0.0
        
        # Normalize based on file size
        lines = content.split('\n')
        return min(1.0, total_deps / len(lines) * 10)

    def _calculate_cohesion_score(self, content: str) -> float:
        """Calculate cohesion score (higher is better)."""
        # Count related methods and properties
        methods = re.findall(r'(?:public|private|protected)?\s*(?:async\s+)?(?:function|\w+)\s*\([^)]*\)', content)
        properties = re.findall(r'(?:public|private|protected)?\s*(?:readonly\s+)?\w+\s*:', content)
        
        # Simple cohesion calculation based on method-property relationships
        if len(methods) == 0:
            return 1.0
        
        # Count methods that reference properties
        cohesive_methods = 0
        for method in methods:
            if any(prop.split(':')[0].strip() in method for prop in properties):
                cohesive_methods += 1
        
        return cohesive_methods / len(methods)

    def _validate_pattern_structure(self, metrics: RepositoryPatternMetrics, content: str) -> List[ValidationIssue]:
        """Validate repository pattern structure."""
        issues = []
        
        # Check for proper interface definition
        if metrics.pattern_type == RepositoryPatternType.INTERFACE:
            if not re.search(r'interface\s+\w+', content, re.IGNORECASE):
                issues.append(ValidationIssue(
                    rule_id="missing_interface_definition",
                    rule_name="Missing Interface Definition",
                    severity=ValidationSeverity.ERROR,
                    message="Repository interface file missing proper interface definition",
                    details={"file_path": metrics.file_path},
                    timestamp=datetime.now(),
                    component="repository_pattern_validator"
                ))
        
        # Check for proper implementation
        if metrics.pattern_type == RepositoryPatternType.IMPLEMENTATION:
            if not re.search(r'implements\s+\w+', content, re.IGNORECASE):
                issues.append(ValidationIssue(
                    rule_id="missing_implementation_contract",
                    rule_name="Missing Implementation Contract",
                    severity=ValidationSeverity.WARNING,
                    message="Repository implementation missing interface contract",
                    details={"file_path": metrics.file_path},
                    timestamp=datetime.now(),
                    component="repository_pattern_validator"
                ))
        
        # Check method count limits
        if metrics.method_count > self.pattern_thresholds["max_methods_per_interface"]:
            issues.append(ValidationIssue(
                rule_id="excessive_methods_interface",
                rule_name="Excessive Methods in Interface",
                severity=ValidationSeverity.WARNING,
                message=f"Interface has {metrics.method_count} methods, exceeding limit of {self.pattern_thresholds['max_methods_per_interface']}",
                details={
                    "file_path": metrics.file_path,
                    "method_count": metrics.method_count,
                    "limit": self.pattern_thresholds["max_methods_per_interface"]
                },
                timestamp=datetime.now(),
                component="repository_pattern_validator"
            ))
        
        return issues

    def _validate_interface_segregation(self, metrics: RepositoryPatternMetrics, content: str) -> List[ValidationIssue]:
        """Validate interface segregation principle."""
        issues = []
        
        # Check for interface segregation violations
        if metrics.pattern_type == RepositoryPatternType.INTERFACE:
            # Look for methods that don't belong together
            methods = re.findall(r'(?:public|private|protected)?\s*(?:async\s+)?(?:function|\w+)\s*\([^)]*\)', content)
            
            # Check for mixed responsibilities
            crud_methods = [m for m in methods if any(keyword in m.lower() for keyword in ['create', 'read', 'update', 'delete', 'save', 'find', 'get'])]
            business_methods = [m for m in methods if any(keyword in m.lower() for keyword in ['validate', 'process', 'calculate', 'transform'])]
            
            if len(crud_methods) > 0 and len(business_methods) > 0:
                issues.append(ValidationIssue(
                    rule_id="interface_segregation_violation",
                    rule_name="Interface Segregation Violation",
                    severity=ValidationSeverity.WARNING,
                    message="Interface mixes data access and business logic methods",
                    details={
                        "file_path": metrics.file_path,
                        "crud_methods": len(crud_methods),
                        "business_methods": len(business_methods)
                    },
                    timestamp=datetime.now(),
                    component="repository_pattern_validator"
                ))
        
        return issues

    def _validate_dependency_injection(self, metrics: RepositoryPatternMetrics, content: str) -> List[ValidationIssue]:
        """Validate dependency injection patterns."""
        issues = []
        
        # Check for constructor dependency injection
        if metrics.pattern_type in [RepositoryPatternType.IMPLEMENTATION, RepositoryPatternType.SERVICE]:
            constructor_match = re.search(r'constructor\s*\(([^)]*)\)', content)
            if constructor_match:
                params = constructor_match.group(1).strip()
                if not params:
                    issues.append(ValidationIssue(
                        rule_id="missing_dependency_injection",
                        rule_name="Missing Dependency Injection",
                        severity=ValidationSeverity.WARNING,
                        message="Repository implementation missing dependency injection in constructor",
                        details={"file_path": metrics.file_path},
                        timestamp=datetime.now(),
                        component="repository_pattern_validator"
                    ))
            else:
                issues.append(ValidationIssue(
                    rule_id="missing_constructor",
                    rule_name="Missing Constructor",
                    severity=ValidationSeverity.ERROR,
                    message="Repository implementation missing constructor for dependency injection",
                    details={"file_path": metrics.file_path},
                    timestamp=datetime.now(),
                    component="repository_pattern_validator"
                ))
        
        # Check for direct instantiation (anti-pattern)
        direct_instantiation = re.findall(r'new\s+\w+\([^)]*\)', content)
        if len(direct_instantiation) > 2:  # Allow some direct instantiation
            issues.append(ValidationIssue(
                rule_id="excessive_direct_instantiation",
                rule_name="Excessive Direct Instantiation",
                severity=ValidationSeverity.WARNING,
                message=f"Repository has {len(direct_instantiation)} direct instantiations, consider dependency injection",
                details={
                    "file_path": metrics.file_path,
                    "direct_instantiations": len(direct_instantiation)
                },
                timestamp=datetime.now(),
                component="repository_pattern_validator"
            ))
        
        return issues

    def _validate_abstraction_level(self, metrics: RepositoryPatternMetrics, content: str) -> List[ValidationIssue]:
        """Validate abstraction level compliance."""
        issues = []
        
        if metrics.abstraction_level < self.pattern_thresholds["min_abstraction_level"]:
            issues.append(ValidationIssue(
                rule_id="low_abstraction_level",
                rule_name="Low Abstraction Level",
                severity=ValidationSeverity.WARNING,
                message=f"Repository abstraction level {metrics.abstraction_level:.2f} below minimum {self.pattern_thresholds['min_abstraction_level']}",
                details={
                    "file_path": metrics.file_path,
                    "abstraction_level": metrics.abstraction_level,
                    "minimum": self.pattern_thresholds["min_abstraction_level"]
                },
                timestamp=datetime.now(),
                component="repository_pattern_validator"
            ))
        
        return issues

    def _validate_coupling_cohesion(self, metrics: RepositoryPatternMetrics, content: str) -> List[ValidationIssue]:
        """Validate coupling and cohesion metrics."""
        issues = []
        
        # Check coupling score
        if metrics.coupling_score > self.pattern_thresholds["max_coupling_score"]:
            issues.append(ValidationIssue(
                rule_id="high_coupling_score",
                rule_name="High Coupling Score",
                severity=ValidationSeverity.WARNING,
                message=f"Repository coupling score {metrics.coupling_score:.2f} exceeds maximum {self.pattern_thresholds['max_coupling_score']}",
                details={
                    "file_path": metrics.file_path,
                    "coupling_score": metrics.coupling_score,
                    "maximum": self.pattern_thresholds["max_coupling_score"]
                },
                timestamp=datetime.now(),
                component="repository_pattern_validator"
            ))
        
        # Check cohesion score
        if metrics.cohesion_score < self.pattern_thresholds["min_cohesion_score"]:
            issues.append(ValidationIssue(
                rule_id="low_cohesion_score",
                rule_name="Low Cohesion Score",
                severity=ValidationSeverity.WARNING,
                message=f"Repository cohesion score {metrics.cohesion_score:.2f} below minimum {self.pattern_thresholds['min_cohesion_score']}",
                details={
                    "file_path": metrics.file_path,
                    "cohesion_score": metrics.cohesion_score,
                    "minimum": self.pattern_thresholds["min_cohesion_score"]
                },
                timestamp=datetime.now(),
                component="repository_pattern_validator"
            ))
        
        return issues

    def _validate_v2_compliance(self, metrics: RepositoryPatternMetrics, content: str) -> List[ValidationIssue]:
        """Validate V2 compliance standards."""
        issues = []
        
        # Check file line count
        lines = content.split('\n')
        if len(lines) > self.pattern_thresholds["max_file_lines"]:
            issues.append(ValidationIssue(
                rule_id="file_line_limit_exceeded",
                rule_name="File Line Limit Exceeded",
                severity=ValidationSeverity.ERROR,
                message=f"Repository file has {len(lines)} lines, exceeding V2 limit of {self.pattern_thresholds['max_file_lines']}",
                details={
                    "file_path": metrics.file_path,
                    "line_count": len(lines),
                    "limit": self.pattern_thresholds["max_file_lines"]
                },
                timestamp=datetime.now(),
                component="repository_pattern_validator"
            ))
            metrics.v2_compliant = False
        
        # Check for proper error handling
        if not re.search(r'try\s*\{|catch\s*\(', content):
            issues.append(ValidationIssue(
                rule_id="missing_error_handling",
                rule_name="Missing Error Handling",
                severity=ValidationSeverity.WARNING,
                message="Repository missing error handling patterns",
                details={"file_path": metrics.file_path},
                timestamp=datetime.now(),
                component="repository_pattern_validator"
            ))
        
        # Check for proper documentation
        comment_lines = len([line for line in lines if line.strip().startswith('//') or line.strip().startswith('/*')])
        comment_ratio = comment_lines / len(lines) if len(lines) > 0 else 0
        
        if comment_ratio < 0.1:  # 10% minimum comment ratio
            issues.append(ValidationIssue(
                rule_id="insufficient_documentation",
                rule_name="Insufficient Documentation",
                severity=ValidationSeverity.INFO,
                message=f"Repository documentation ratio {comment_ratio:.2%} below recommended 10%",
                details={
                    "file_path": metrics.file_path,
                    "comment_ratio": comment_ratio,
                    "comment_lines": comment_lines,
                    "total_lines": len(lines)
                },
                timestamp=datetime.now(),
                component="repository_pattern_validator"
            ))
        
        return issues

    def validate_multiple_repositories(self, file_paths: List[str]) -> Dict[str, List[ValidationIssue]]:
        """Validate multiple repository pattern files."""
        results = {}
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                results[file_path] = self.validate_repository_pattern(file_path)
            else:
                results[file_path] = [ValidationIssue(
                    rule_id="file_not_found",
                    rule_name="File Not Found",
                    severity=ValidationSeverity.ERROR,
                    message=f"Repository file not found: {file_path}",
                    details={"file_path": file_path},
                    timestamp=datetime.now(),
                    component="repository_pattern_validator"
                )]
        
        return results

    def generate_repository_compliance_report(self, validation_results: Dict[str, List[ValidationIssue]]) -> Dict[str, Any]:
        """Generate comprehensive repository pattern compliance report."""
        total_files = len(validation_results)
        compliant_files = 0
        total_issues = 0
        issue_summary = {
            "error": 0,
            "warning": 0,
            "info": 0
        }
        
        file_summaries = []
        
        for file_path, issues in validation_results.items():
            file_compliant = len(issues) == 0
            if file_compliant:
                compliant_files += 1
            
            total_issues += len(issues)
            
            # Count issues by severity
            for issue in issues:
                if issue.severity == ValidationSeverity.ERROR:
                    issue_summary["error"] += 1
                elif issue.severity == ValidationSeverity.WARNING:
                    issue_summary["warning"] += 1
                else:
                    issue_summary["info"] += 1
            
            file_summaries.append({
                "file_path": file_path,
                "compliant": file_compliant,
                "issue_count": len(issues),
                "issues": [
                    {
                        "rule_id": issue.rule_id,
                        "rule_name": issue.rule_name,
                        "severity": issue.severity.value,
                        "message": issue.message
                    }
                    for issue in issues
                ]
            })
        
        compliance_rate = (compliant_files / total_files * 100) if total_files > 0 else 0
        
        return {
            "report_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_files": total_files,
                "compliant_files": compliant_files,
                "compliance_rate": round(compliance_rate, 2),
                "total_issues": total_issues,
                "issue_breakdown": issue_summary
            },
            "file_details": file_summaries,
            "recommendations": self._generate_repository_recommendations(issue_summary, compliance_rate)
        }

    def _generate_repository_recommendations(self, issue_summary: Dict[str, int], compliance_rate: float) -> List[str]:
        """Generate recommendations based on repository validation results."""
        recommendations = []
        
        if compliance_rate < 80:
            recommendations.append("Focus on achieving 80%+ repository pattern compliance rate")
        
        if issue_summary["error"] > 0:
            recommendations.append("Address all ERROR level issues immediately - these violate V2 compliance")
        
        if issue_summary["warning"] > 5:
            recommendations.append("Review and address WARNING level issues to improve repository pattern quality")
        
        if issue_summary["info"] > 10:
            recommendations.append("Consider improving documentation and code structure based on INFO level suggestions")
        
        recommendations.append("Implement dependency injection containers for better repository management")
        recommendations.append("Establish repository pattern guidelines and code review processes")
        recommendations.append("Consider implementing unit of work pattern for transaction management")
        
        return recommendations
