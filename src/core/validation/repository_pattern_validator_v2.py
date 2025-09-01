#!/usr/bin/env python3
"""
Repository Pattern Validator V2 - Agent Cellphone V2
==================================================

V2 compliant repository pattern validator with extracted models and utilities.
Reduced from 563 lines to 200 lines through modular architecture.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import os
from typing import Dict, Any, List
from datetime import datetime

from .models.repository_pattern_models import (
    RepositoryPatternType, RepositoryPatternProfile, RepositoryPatternResult,
    RepositoryPatternMetrics, RepositoryPatternConfig, RepositoryPatternThresholds
)
from .utils.repository_pattern_utils import RepositoryPatternUtils
from .validation_models import ValidationIssue, ValidationSeverity

class RepositoryPatternValidator:
    """
    V2 compliant repository pattern validator.
    
    Provides comprehensive validation for:
    - Generic repository pattern implementation
    - Specific repository pattern implementation
    - Unit of Work pattern validation
    - Specification pattern validation
    - CQRS pattern validation
    - Repository pattern quality assessment
    """

    def __init__(self):
        """Initialize the repository pattern validator."""
        self.utils = RepositoryPatternUtils()
        self.config = RepositoryPatternConfig()
        self.thresholds = RepositoryPatternThresholds()
        self.metrics = RepositoryPatternMetrics(
            total_files_analyzed=0,
            v2_compliant_files=0,
            pattern_implementations=0,
            generic_repositories=0,
            specific_repositories=0,
            unit_of_work_patterns=0,
            specification_patterns=0,
            cqrs_patterns=0,
            average_pattern_score=0.0,
            average_implementation_quality=0.0
        )

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
                    message=f"File not found: {file_path}",
                    severity=ValidationSeverity.ERROR,
                    file_path=file_path
                ))
                return issues
            
            # Analyze repository pattern
            profile = self.utils.analyze_repository_pattern(file_path)
            
            # Check V2 compliance
            if not profile.v2_compliant:
                issues.append(ValidationIssue(
                    rule_id="v2_compliance_violation",
                    rule_name="V2 Compliance Violation",
                    message=f"File exceeds V2 limit: {len(profile.classes_found)} classes",
                    severity=ValidationSeverity.ERROR,
                    file_path=file_path
                ))
            
            # Check pattern score
            if profile.pattern_score < self.thresholds.acceptable_score:
                issues.append(ValidationIssue(
                    rule_id="low_pattern_score",
                    rule_name="Low Pattern Score",
                    message=f"Repository pattern score too low: {profile.pattern_score:.1f} < {self.thresholds.acceptable_score}",
                    severity=ValidationSeverity.WARNING,
                    file_path=file_path
                ))
            
            # Check implementation quality
            if profile.implementation_quality < self.thresholds.acceptable_quality:
                issues.append(ValidationIssue(
                    rule_id="low_implementation_quality",
                    rule_name="Low Implementation Quality",
                    message=f"Implementation quality too low: {profile.implementation_quality:.1f} < {self.thresholds.acceptable_quality}",
                    severity=ValidationSeverity.WARNING,
                    file_path=file_path
                ))
            
            # Check separation score
            if profile.separation_score < self.thresholds.acceptable_score:
                issues.append(ValidationIssue(
                    rule_id="poor_separation",
                    rule_name="Poor Separation of Concerns",
                    message=f"Separation score too low: {profile.separation_score:.1f} < {self.thresholds.acceptable_score}",
                    severity=ValidationSeverity.WARNING,
                    file_path=file_path
                ))
            
            # Update metrics
            self._update_metrics(profile)
            
        except Exception as e:
            issues.append(ValidationIssue(
                rule_id="validation_error",
                rule_name="Validation Error",
                message=f"Error during validation: {str(e)}",
                severity=ValidationSeverity.ERROR,
                file_path=file_path
            ))
        
        return issues

    def create_repository_profile(self, file_path: str) -> RepositoryPatternProfile:
        """
        Create a repository pattern profile for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Repository pattern profile
        """
        return self.utils.analyze_repository_pattern(file_path)

    def generate_repository_result(self, file_path: str) -> RepositoryPatternResult:
        """
        Generate comprehensive repository pattern result for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Repository pattern result
        """
        try:
            profile = self.utils.analyze_repository_pattern(file_path)
            
            # Validate and collect issues
            issues = self.validate_repository_pattern(file_path)
            issue_messages = [issue.message for issue in issues]
            
            # Generate recommendations
            recommendations = self.utils.generate_recommendations(profile)
            
            # Calculate metrics
            is_v2_compliant = profile.v2_compliant
            pattern_score = profile.pattern_score
            implementation_quality = profile.implementation_quality
            separation_score = profile.separation_score
            estimated_effort = self.utils.estimate_refactoring_effort(profile)
            
            result = RepositoryPatternResult(
                file_path=file_path,
                pattern_type=profile.pattern_type,
                is_v2_compliant=is_v2_compliant,
                pattern_score=pattern_score,
                implementation_quality=implementation_quality,
                separation_score=separation_score,
                issues=issue_messages,
                recommendations=recommendations,
                classes_implemented=profile.classes_found,
                interfaces_implemented=profile.interfaces_found,
                methods_implemented=profile.methods_found,
                estimated_effort=estimated_effort
            )
            
            return result
            
        except Exception as e:
            # Return error result
            return RepositoryPatternResult(
                file_path=file_path,
                pattern_type=RepositoryPatternType.GENERIC_REPOSITORY,
                is_v2_compliant=False,
                pattern_score=0.0,
                implementation_quality=0.0,
                separation_score=0.0,
                issues=[f"Error generating result: {str(e)}"],
                recommendations=["Fix file analysis errors"],
                classes_implemented=[],
                interfaces_implemented=[],
                methods_implemented=[],
                estimated_effort=1
            )

    def _update_metrics(self, profile: RepositoryPatternProfile):
        """Update validation metrics."""
        self.metrics.total_files_analyzed += 1
        
        if profile.v2_compliant:
            self.metrics.v2_compliant_files += 1
        
        self.metrics.pattern_implementations += 1
        
        # Count pattern types
        if profile.pattern_type == RepositoryPatternType.GENERIC_REPOSITORY:
            self.metrics.generic_repositories += 1
        elif profile.pattern_type == RepositoryPatternType.SPECIFIC_REPOSITORY:
            self.metrics.specific_repositories += 1
        elif profile.pattern_type == RepositoryPatternType.UNIT_OF_WORK:
            self.metrics.unit_of_work_patterns += 1
        elif profile.pattern_type == RepositoryPatternType.SPECIFICATION_PATTERN:
            self.metrics.specification_patterns += 1
        elif profile.pattern_type == RepositoryPatternType.CQRS_PATTERN:
            self.metrics.cqrs_patterns += 1
        
        # Update averages
        if self.metrics.total_files_analyzed > 0:
            self.metrics.average_pattern_score = (
                (self.metrics.average_pattern_score * (self.metrics.total_files_analyzed - 1) + profile.pattern_score) 
                / self.metrics.total_files_analyzed
            )
            self.metrics.average_implementation_quality = (
                (self.metrics.average_implementation_quality * (self.metrics.total_files_analyzed - 1) + profile.implementation_quality) 
                / self.metrics.total_files_analyzed
            )

    def get_validation_metrics(self) -> RepositoryPatternMetrics:
        """Get current validation metrics."""
        return self.metrics

    def reset_metrics(self):
        """Reset validation metrics."""
        self.metrics = RepositoryPatternMetrics(
            total_files_analyzed=0,
            v2_compliant_files=0,
            pattern_implementations=0,
            generic_repositories=0,
            specific_repositories=0,
            unit_of_work_patterns=0,
            specification_patterns=0,
            cqrs_patterns=0,
            average_pattern_score=0.0,
            average_implementation_quality=0.0
        )
