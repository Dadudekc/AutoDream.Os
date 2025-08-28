#!/usr/bin/env python3
"""
Workflow Validation System - Agent-5
====================================

This module implements a comprehensive validation system for automated refactoring
workflows as part of contract REFACTOR-002 deliverables.

Features:
- Multi-level validation rules
- Reliability testing and metrics
- Quality assurance automation
- Performance benchmarking integration

Author: Agent-5 (REFACTORING MANAGER)
Contract: REFACTOR-002 - Automated Refactoring Workflow Implementation
Status: IN PROGRESS
"""

import os
import sys
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import traceback
import statistics
import time

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.managers.base_manager import BaseManager
from core.refactoring.refactoring_performance_benchmark import RefactoringPerformanceBenchmark

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Validation level enumeration."""
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"
    EXPERT = "expert"


class ValidationResult(Enum):
    """Validation result enumeration."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class ValidationRule:
    """Individual validation rule definition."""
    rule_id: str
    name: str
    description: str
    validation_func: Callable
    level: ValidationLevel = ValidationLevel.STANDARD
    weight: float = 1.0
    timeout: float = 30.0  # seconds
    dependencies: List[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    """Result of a single validation rule execution."""
    rule_id: str
    rule_name: str
    result: ValidationResult
    score: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class WorkflowValidationReport:
    """Complete workflow validation report."""
    workflow_id: str
    validation_level: ValidationLevel
    start_time: datetime
    end_time: Optional[datetime] = None
    total_rules: int = 0
    passed_rules: int = 0
    failed_rules: int = 0
    warning_rules: int = 0
    error_rules: int = 0
    skipped_rules: int = 0
    overall_score: float = 0.0
    reliability_score: float = 0.0
    quality_score: float = 0.0
    performance_score: float = 0.0
    rule_results: List[ValidationResult] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class WorkflowValidationSystem(BaseManager):
    """
    Comprehensive workflow validation system for refactoring operations.
    
    This class provides multi-level validation, reliability testing, and quality
    assurance for automated refactoring workflows.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the workflow validation system."""
        super().__init__(config or {})
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.validation_reports: Dict[str, WorkflowValidationReport] = {}
        self.performance_benchmarks: Dict[str, float] = {}
        self.reliability_history: List[float] = []
        
        self._initialize_validation_rules()
        self._setup_logging()
    
    def _initialize_validation_rules(self):
        """Initialize comprehensive validation rules for different aspects."""
        # Code Quality Validation Rules
        self._add_validation_rule(
            ValidationRule(
                rule_id="code_quality_srp_compliance",
                name="SRP Compliance Check",
                description="Verify Single Responsibility Principle compliance",
                validation_func=self._validate_srp_compliance,
                level=ValidationLevel.STANDARD,
                weight=2.0
            )
        )
        
        self._add_validation_rule(
            ValidationRule(
                rule_id="code_quality_complexity_reduction",
                name="Complexity Reduction Validation",
                description="Verify that code complexity was reduced",
                validation_func=self._validate_complexity_reduction,
                level=ValidationLevel.STANDARD,
                weight=1.5
            )
        )
        
        self._add_validation_rule(
            ValidationRule(
                rule_id="code_quality_duplication_removal",
                name="Duplication Removal Validation",
                description="Verify that code duplication was removed",
                validation_func=self._validate_duplication_removal,
                level=ValidationLevel.STANDARD,
                weight=1.8
            )
        )
        
        # Performance Validation Rules
        self._add_validation_rule(
            ValidationRule(
                rule_id="performance_execution_time",
                name="Execution Time Validation",
                description="Verify workflow execution time improvements",
                validation_func=self._validate_execution_time,
                level=ValidationLevel.STANDARD,
                weight=1.2
            )
        )
        
        self._add_validation_rule(
            ValidationRule(
                rule_id="performance_resource_usage",
                name="Resource Usage Validation",
                description="Verify resource usage optimization",
                validation_func=self._validate_resource_usage,
                level=ValidationLevel.COMPREHENSIVE,
                weight=1.0
            )
        )
        
        # Reliability Validation Rules
        self._add_validation_rule(
            ValidationRule(
                rule_id="reliability_error_handling",
                name="Error Handling Validation",
                description="Verify robust error handling implementation",
                validation_func=self._validate_error_handling,
                level=ValidationLevel.STANDARD,
                weight=1.5
            )
        )
        
        self._add_validation_rule(
            ValidationRule(
                rule_id="reliability_consistency",
                name="Consistency Validation",
                description="Verify consistent behavior across executions",
                validation_func=self._validate_consistency,
                level=ValidationLevel.COMPREHENSIVE,
                weight=1.3
            )
        )
        
        # Test Coverage Validation Rules
        self._add_validation_rule(
            ValidationRule(
                rule_id="test_coverage_maintenance",
                name="Test Coverage Maintenance",
                description="Verify test coverage is maintained or improved",
                validation_func=self._validate_test_coverage,
                level=ValidationLevel.STANDARD,
                weight=1.4
            )
        )
        
        self._add_validation_rule(
            ValidationRule(
                rule_id="test_quality_assurance",
                name="Test Quality Assurance",
                description="Verify test quality and reliability",
                validation_func=self._validate_test_quality,
                level=ValidationLevel.COMPREHENSIVE,
                weight=1.1
            )
        )
        
        # Architecture Validation Rules
        self._add_validation_rule(
            ValidationRule(
                rule_id="architecture_modularity",
                name="Modularity Validation",
                description="Verify improved modularity and separation of concerns",
                validation_func=self._validate_modularity,
                level=ValidationLevel.STANDARD,
                weight=1.6
            )
        )
        
        self._add_validation_rule(
            ValidationRule(
                rule_id="architecture_dependency_management",
                name="Dependency Management Validation",
                description="Verify proper dependency management",
                validation_func=self._validate_dependency_management,
                level=ValidationLevel.COMPREHENSIVE,
                weight=1.2
            )
        )
    
    def _add_validation_rule(self, rule: ValidationRule):
        """Add a validation rule to the system."""
        self.validation_rules[rule.rule_id] = rule
        logger.info(f"Added validation rule: {rule.name}")
    
    async def validate_workflow(self, workflow_id: str, 
                               validation_level: ValidationLevel = ValidationLevel.STANDARD,
                               target_files: Optional[List[str]] = None,
                               workflow_data: Optional[Dict[str, Any]] = None) -> WorkflowValidationReport:
        """
        Perform comprehensive workflow validation.
        
        Args:
            workflow_id: ID of the workflow to validate
            validation_level: Level of validation to perform
            target_files: Optional list of target files for validation
            workflow_data: Optional workflow execution data
            
        Returns:
            Comprehensive validation report
        """
        logger.info(f"Starting workflow validation for {workflow_id} at {validation_level.value} level")
        
        # Create validation report
        report = WorkflowValidationReport(
            workflow_id=workflow_id,
            validation_level=validation_level,
            start_time=datetime.now()
        )
        
        # Filter rules based on validation level
        applicable_rules = self._get_applicable_rules(validation_level)
        report.total_rules = len(applicable_rules)
        
        logger.info(f"Executing {len(applicable_rules)} validation rules")
        
        # Execute validation rules
        for rule in applicable_rules:
            try:
                result = await self._execute_validation_rule(rule, workflow_id, target_files, workflow_data)
                report.rule_results.append(result)
                
                # Update counters
                if result.result == ValidationResult.PASSED:
                    report.passed_rules += 1
                elif result.result == ValidationResult.FAILED:
                    report.failed_rules += 1
                elif result.result == ValidationResult.WARNING:
                    report.warning_rules += 1
                elif result.result == ValidationResult.ERROR:
                    report.error_rules += 1
                else:
                    report.skipped_rules += 1
                    
            except Exception as e:
                logger.error(f"Validation rule {rule.rule_id} failed with error: {str(e)}")
                error_result = ValidationResult(
                    rule_id=rule.rule_id,
                    rule_name=rule.name,
                    result=ValidationResult.ERROR,
                    error_message=str(e),
                    timestamp=datetime.now()
                )
                report.rule_results.append(error_result)
                report.error_rules += 1
        
        # Calculate scores
        report = self._calculate_validation_scores(report)
        
        # Generate recommendations
        report.recommendations = self._generate_recommendations(report)
        
        # Finalize report
        report.end_time = datetime.now()
        
        # Store report
        self.validation_reports[workflow_id] = report
        
        # Update reliability history
        self.reliability_history.append(report.reliability_score)
        
        logger.info(f"Workflow validation completed for {workflow_id}")
        logger.info(f"Overall score: {report.overall_score:.2f}%, Reliability: {report.reliability_score:.2f}%")
        
        return report
    
    def _get_applicable_rules(self, validation_level: ValidationLevel) -> List[ValidationRule]:
        """Get validation rules applicable to the specified level."""
        level_priorities = {
            ValidationLevel.BASIC: 1,
            ValidationLevel.STANDARD: 2,
            ValidationLevel.COMPREHENSIVE: 3,
            ValidationLevel.EXPERT: 4
        }
        
        target_priority = level_priorities[validation_level]
        applicable_rules = []
        
        for rule in self.validation_rules.values():
            rule_priority = level_priorities[rule.level]
            if rule_priority <= target_priority:
                applicable_rules.append(rule)
        
        # Sort by weight (descending) for optimal execution order
        applicable_rules.sort(key=lambda r: r.weight, reverse=True)
        
        return applicable_rules
    
    async def _execute_validation_rule(self, rule: ValidationRule, workflow_id: str,
                                     target_files: Optional[List[str]], 
                                     workflow_data: Optional[Dict[str, Any]]) -> ValidationResult:
        """Execute a single validation rule."""
        start_time = time.time()
        
        try:
            # Execute validation with timeout
            if asyncio.iscoroutinefunction(rule.validation_func):
                result = await asyncio.wait_for(
                    rule.validation_func(workflow_id, target_files, workflow_data),
                    timeout=rule.timeout
                )
            else:
                result = rule.validation_func(workflow_id, target_files, workflow_data)
            
            execution_time = time.time() - start_time
            
            # Create validation result
            validation_result = ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                result=result.get("status", ValidationResult.PASSED),
                score=result.get("score", 100.0),
                details=result.get("details", {}),
                execution_time=execution_time,
                timestamp=datetime.now()
            )
            
            return validation_result
            
        except asyncio.TimeoutError:
            execution_time = time.time() - start_time
            return ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                result=ValidationResult.ERROR,
                error_message="Validation rule execution timed out",
                execution_time=execution_time,
                timestamp=datetime.now()
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ValidationResult(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                result=ValidationResult.ERROR,
                error_message=str(e),
                execution_time=execution_time,
                timestamp=datetime.now()
            )
    
    def _calculate_validation_scores(self, report: WorkflowValidationReport) -> WorkflowValidationReport:
        """Calculate comprehensive validation scores."""
        if not report.rule_results:
            return report
        
        # Calculate overall score (weighted average)
        total_weight = 0.0
        weighted_score = 0.0
        
        for result in report.rule_results:
            rule = self.validation_rules.get(result.rule_id)
            if rule:
                weight = rule.weight
                total_weight += weight
                weighted_score += result.score * weight
        
        if total_weight > 0:
            report.overall_score = weighted_score / total_weight
        
        # Calculate reliability score (based on passed vs failed rules)
        if report.total_rules > 0:
            reliability_factors = {
                ValidationResult.PASSED: 1.0,
                ValidationResult.WARNING: 0.8,
                ValidationResult.FAILED: 0.3,
                ValidationResult.ERROR: 0.0,
                ValidationResult.SKIPPED: 0.5
            }
            
            reliability_score = 0.0
            for result in report.rule_results:
                factor = reliability_factors.get(result.result, 0.0)
                reliability_score += factor
            
            report.reliability_score = (reliability_score / report.total_rules) * 100
        
        # Calculate quality score (based on individual rule scores)
        valid_scores = [r.score for r in report.rule_results if r.result != ValidationResult.ERROR]
        if valid_scores:
            report.quality_score = statistics.mean(valid_scores)
        
        # Calculate performance score (based on execution times)
        execution_times = [r.execution_time for r in report.rule_results if r.execution_time > 0]
        if execution_times:
            avg_time = statistics.mean(execution_times)
            # Normalize to 0-100 scale (faster = higher score)
            report.performance_score = max(0, 100 - (avg_time * 10))
        
        return report
    
    def _generate_recommendations(self, report: WorkflowValidationReport) -> List[str]:
        """Generate actionable recommendations based on validation results."""
        recommendations = []
        
        # Analyze failed rules
        failed_rules = [r for r in report.rule_results if r.result == ValidationResult.FAILED]
        if failed_rules:
            recommendations.append(f"Address {len(failed_rules)} failed validation rules to improve overall score")
            
            for rule in failed_rules[:3]:  # Top 3 failures
                recommendations.append(f"Fix {rule.rule_name}: {rule.error_message or 'Review implementation'}")
        
        # Analyze warning rules
        warning_rules = [r for r in report.rule_results if r.result == ValidationResult.WARNING]
        if warning_rules:
            recommendations.append(f"Review {len(warning_rules)} warning validation rules for potential improvements")
        
        # Performance recommendations
        if report.performance_score < 70:
            recommendations.append("Optimize validation rule execution times for better performance")
        
        # Reliability recommendations
        if report.reliability_score < 80:
            recommendations.append("Improve error handling and consistency for better reliability")
        
        # Quality recommendations
        if report.quality_score < 85:
            recommendations.append("Enhance individual rule implementations for higher quality scores")
        
        # General improvement recommendations
        if report.overall_score < 90:
            recommendations.append("Consider implementing additional validation rules for comprehensive coverage")
        
        if not recommendations:
            recommendations.append("Excellent validation results! Maintain current quality standards.")
        
        return recommendations
    
    # Validation Rule Implementations
    
    async def _validate_srp_compliance(self, workflow_id: str, target_files: Optional[List[str]], 
                                     workflow_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate Single Responsibility Principle compliance."""
        # Simulate SRP validation
        await asyncio.sleep(1.5)
        
        # Mock validation logic
        srp_score = 85.0
        violations_found = 2
        
        if violations_found == 0:
            status = ValidationResult.PASSED
            message = "SRP compliance validation passed"
        elif violations_found <= 2:
            status = ValidationResult.WARNING
            message = "Minor SRP violations detected"
        else:
            status = ValidationResult.FAILED
            message = "Significant SRP violations detected"
        
        return {
            "status": status,
            "score": srp_score,
            "details": {
                "violations_found": violations_found,
                "compliance_level": "good" if srp_score >= 80 else "needs_improvement",
                "recommendations": "Consider extracting mixed responsibilities into separate classes"
            }
        }
    
    async def _validate_complexity_reduction(self, workflow_id: str, target_files: Optional[List[str]], 
                                           workflow_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate that code complexity was reduced."""
        await asyncio.sleep(1.0)
        
        # Mock complexity analysis
        complexity_reduction = 25.0  # percentage
        complexity_score = 90.0 if complexity_reduction >= 20 else 70.0
        
        status = ValidationResult.PASSED if complexity_reduction >= 15 else ValidationResult.FAILED
        
        return {
            "status": status,
            "score": complexity_score,
            "details": {
                "complexity_reduction": f"{complexity_reduction}%",
                "target_achieved": complexity_reduction >= 15,
                "improvement_level": "significant" if complexity_reduction >= 25 else "moderate"
            }
        }
    
    async def _validate_duplication_removal(self, workflow_id: str, target_files: Optional[List[str]], 
                                          workflow_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate that code duplication was removed."""
        await asyncio.sleep(1.2)
        
        # Mock duplication analysis
        duplication_removed = 18  # lines
        duplication_score = 88.0
        
        status = ValidationResult.PASSED if duplication_removed >= 10 else ValidationResult.FAILED
        
        return {
            "status": status,
            "score": duplication_score,
            "details": {
                "duplication_removed": f"{duplication_removed} lines",
                "efficiency_gain": "high" if duplication_removed >= 15 else "moderate",
                "maintainability_improvement": "significant"
            }
        }
    
    async def _validate_execution_time(self, workflow_id: str, target_files: Optional[List[str]], 
                                     workflow_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate workflow execution time improvements."""
        await asyncio.sleep(0.8)
        
        # Mock execution time analysis
        time_improvement = 35.0  # percentage
        time_score = 92.0 if time_improvement >= 30 else 75.0
        
        status = ValidationResult.PASSED if time_improvement >= 20 else ValidationResult.WARNING
        
        return {
            "status": status,
            "score": time_score,
            "details": {
                "time_improvement": f"{time_improvement}%",
                "performance_gain": "excellent" if time_improvement >= 30 else "good",
                "efficiency_level": "high"
            }
        }
    
    async def _validate_resource_usage(self, workflow_id: str, target_files: Optional[List[str]], 
                                     workflow_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate resource usage optimization."""
        await asyncio.sleep(1.3)
        
        # Mock resource analysis
        memory_reduction = 28.0  # percentage
        cpu_optimization = 22.0  # percentage
        resource_score = 85.0
        
        status = ValidationResult.PASSED if memory_reduction >= 20 else ValidationResult.WARNING
        
        return {
            "status": status,
            "score": resource_score,
            "details": {
                "memory_reduction": f"{memory_reduction}%",
                "cpu_optimization": f"{cpu_optimization}%",
                "resource_efficiency": "improved",
                "optimization_level": "good"
            }
        }
    
    async def _validate_error_handling(self, workflow_id: str, target_files: Optional[List[str]], 
                                     workflow_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate robust error handling implementation."""
        await asyncio.sleep(1.1)
        
        # Mock error handling analysis
        error_handling_coverage = 92.0  # percentage
        error_score = 90.0
        
        status = ValidationResult.PASSED if error_handling_coverage >= 85 else ValidationResult.FAILED
        
        return {
            "status": status,
            "score": error_score,
            "details": {
                "error_handling_coverage": f"{error_handling_coverage}%",
                "robustness_level": "high" if error_handling_coverage >= 90 else "moderate",
                "reliability": "excellent"
            }
        }
    
    async def _validate_consistency(self, workflow_id: str, target_files: Optional[List[str]], 
                                  workflow_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate consistent behavior across executions."""
        await asyncio.sleep(1.4)
        
        # Mock consistency analysis
        consistency_score = 87.0
        variation_level = "low"
        
        status = ValidationResult.PASSED if consistency_score >= 80 else ValidationResult.WARNING
        
        return {
            "status": status,
            "score": consistency_score,
            "details": {
                "consistency_level": "high" if consistency_score >= 85 else "moderate",
                "variation_level": variation_level,
                "predictability": "good"
            }
        }
    
    async def _validate_test_coverage(self, workflow_id: str, target_files: Optional[List[str]], 
                                    workflow_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate test coverage maintenance."""
        await asyncio.sleep(1.0)
        
        # Mock test coverage analysis
        test_coverage = 89.0  # percentage
        test_score = 88.0
        
        status = ValidationResult.PASSED if test_coverage >= 80 else ValidationResult.FAILED
        
        return {
            "status": status,
            "score": test_score,
            "details": {
                "test_coverage": f"{test_coverage}%",
                "coverage_maintained": True,
                "test_quality": "good"
            }
        }
    
    async def _validate_test_quality(self, workflow_id: str, target_files: Optional[List[str]], 
                                   workflow_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate test quality and reliability."""
        await asyncio.sleep(1.2)
        
        # Mock test quality analysis
        test_quality_score = 86.0
        test_reliability = "high"
        
        status = ValidationResult.PASSED if test_quality_score >= 80 else ValidationResult.WARNING
        
        return {
            "status": status,
            "score": test_quality_score,
            "details": {
                "test_reliability": test_reliability,
                "test_maintainability": "good",
                "test_coverage_depth": "adequate"
            }
        }
    
    async def _validate_modularity(self, workflow_id: str, target_files: Optional[List[str]], 
                                 workflow_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate improved modularity and separation of concerns."""
        await asyncio.sleep(1.3)
        
        # Mock modularity analysis
        modularity_score = 91.0
        separation_level = "excellent"
        
        status = ValidationResult.PASSED if modularity_score >= 85 else ValidationResult.WARNING
        
        return {
            "status": status,
            "score": modularity_score,
            "details": {
                "modularity_level": "high",
                "separation_of_concerns": separation_level,
                "maintainability": "improved"
            }
        }
    
    async def _validate_dependency_management(self, workflow_id: str, target_files: Optional[List[str]], 
                                           workflow_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate proper dependency management."""
        await asyncio.sleep(1.1)
        
        # Mock dependency analysis
        dependency_score = 84.0
        coupling_level = "reduced"
        
        status = ValidationResult.PASSED if dependency_score >= 80 else ValidationResult.WARNING
        
        return {
            "status": status,
            "score": dependency_score,
            "details": {
                "coupling_level": coupling_level,
                "dependency_clarity": "good",
                "management_quality": "adequate"
            }
        }
    
    def get_validation_report(self, workflow_id: str) -> Optional[WorkflowValidationReport]:
        """Get a validation report by workflow ID."""
        return self.validation_reports.get(workflow_id)
    
    def list_validation_reports(self) -> List[Dict[str, Any]]:
        """List all validation reports with summary information."""
        report_list = []
        
        for workflow_id, report in self.validation_reports.items():
            report_info = {
                "workflow_id": workflow_id,
                "validation_level": report.validation_level.value,
                "overall_score": report.overall_score,
                "reliability_score": report.reliability_score,
                "quality_score": report.quality_score,
                "performance_score": report.performance_score,
                "total_rules": report.total_rules,
                "passed_rules": report.passed_rules,
                "failed_rules": report.failed_rules,
                "start_time": report.start_time.isoformat(),
                "end_time": report.end_time.isoformat() if report.end_time else None
            }
            report_list.append(report_info)
        
        return report_list
    
    def get_reliability_trends(self) -> Dict[str, Any]:
        """Get reliability trends and statistics."""
        if not self.reliability_history:
            return {"message": "No reliability data available"}
        
        return {
            "current_reliability": self.reliability_history[-1] if self.reliability_history else 0,
            "average_reliability": statistics.mean(self.reliability_history),
            "reliability_trend": "improving" if len(self.reliability_history) >= 2 and 
                                self.reliability_history[-1] > self.reliability_history[-2] else "stable",
            "total_validations": len(self.reliability_history),
            "reliability_history": self.reliability_history[-10:]  # Last 10 values
        }
    
    def export_validation_report(self, workflow_id: str, output_path: str) -> bool:
        """Export a validation report to JSON."""
        report = self.get_validation_report(workflow_id)
        if not report:
            return False
        
        try:
            # Prepare export data
            export_data = {
                "workflow_id": report.workflow_id,
                "validation_level": report.validation_level.value,
                "start_time": report.start_time.isoformat(),
                "end_time": report.end_time.isoformat() if report.end_time else None,
                "scores": {
                    "overall_score": report.overall_score,
                    "reliability_score": report.reliability_score,
                    "quality_score": report.quality_score,
                    "performance_score": report.performance_score
                },
                "rule_results": [
                    {
                        "rule_id": result.rule_id,
                        "rule_name": result.rule_name,
                        "result": result.result.value,
                        "score": result.score,
                        "details": result.details,
                        "execution_time": result.execution_time,
                        "error_message": result.error_message,
                        "timestamp": result.timestamp.isoformat()
                    }
                    for result in report.rule_results
                ],
                "recommendations": report.recommendations,
                "metadata": report.metadata
            }
            
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Validation report exported to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export validation report: {str(e)}")
            return False


# Example usage and testing
async def demo_workflow_validation():
    """Demonstrate the workflow validation system."""
    print("🔍 Workflow Validation System Demo")
    print("=" * 50)
    
    # Initialize validation system
    validation_system = WorkflowValidationSystem()
    
    # Perform comprehensive validation
    workflow_id = "demo_workflow_001"
    target_files = [
        "src/services/financial/portfolio/rebalancing.py",
        "src/core/performance/performance_orchestrator.py"
    ]
    
    print(f"✅ Starting validation for workflow: {workflow_id}")
    
    # Run validation at comprehensive level
    report = await validation_system.validate_workflow(
        workflow_id=workflow_id,
        validation_level=ValidationLevel.COMPREHENSIVE,
        target_files=target_files
    )
    
    print(f"\n📊 Validation Results:")
    print(f"  Overall Score: {report.overall_score:.2f}%")
    print(f"  Reliability Score: {report.reliability_score:.2f}%")
    print(f"  Quality Score: {report.quality_score:.2f}%")
    print(f"  Performance Score: {report.performance_score:.2f}%")
    print(f"  Rules Passed: {report.passed_rules}/{report.total_rules}")
    
    print(f"\n💡 Recommendations:")
    for i, recommendation in enumerate(report.recommendations[:3], 1):
        print(f"  {i}. {recommendation}")
    
    # Export validation report
    report_path = "workflow_validation_report.json"
    if validation_system.export_validation_report(workflow_id, report_path):
        print(f"\n📊 Validation report exported to: {report_path}")
    
    # Get reliability trends
    trends = validation_system.get_reliability_trends()
    print(f"\n📈 Reliability Trends:")
    print(f"  Current: {trends['current_reliability']:.2f}%")
    print(f"  Average: {trends['average_reliability']:.2f}%")
    print(f"  Trend: {trends['reliability_trend']}")
    
    print("\n🎉 Validation demo completed successfully!")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_workflow_validation())
