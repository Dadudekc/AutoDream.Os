"""
Strategic Oversight Validators - V2 Compliance Module
====================================================

Validation utilities for strategic oversight data models.

V2 Compliance: < 300 lines, single responsibility, validation logic.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Dict, Any

from .enums import ConfidenceLevel, ImpactLevel
from .data_models import StrategicOversightReport, SwarmCoordinationInsight


class StrategicOversightValidator:
    """Validator class for strategic oversight data models."""
    
    @staticmethod
    def validate_oversight_report(report: StrategicOversightReport) -> Dict[str, Any]:
        """Validate strategic oversight report."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Check required fields
        if not report.title:
            validation['errors'].append("Report title is required")
            validation['is_valid'] = False
        
        if not report.summary:
            validation['errors'].append("Report summary is required")
            validation['is_valid'] = False
        
        # Check confidence level
        if not isinstance(report.confidence_level, ConfidenceLevel):
            validation['warnings'].append("Invalid confidence level")
        
        # Check impact level
        if not isinstance(report.impact_level, ImpactLevel):
            validation['warnings'].append("Invalid impact level")
        
        return validation
    
    @staticmethod
    def validate_swarm_insight(insight: SwarmCoordinationInsight) -> Dict[str, Any]:
        """Validate swarm coordination insight."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Check required fields
        if not insight.description:
            validation['errors'].append("Insight description is required")
            validation['is_valid'] = False
        
        # Check confidence range
        if not 0.0 <= insight.confidence <= 1.0:
            validation['warnings'].append("Confidence should be between 0.0 and 1.0")
        
        # Check impact score range
        if not 0.0 <= insight.impact_score <= 1.0:
            validation['warnings'].append("Impact score should be between 0.0 and 1.0")
        
        return validation
    
    @staticmethod
    def validate_confidence_level(confidence: float) -> bool:
        """Validate confidence level is in valid range."""
        return 0.0 <= confidence <= 1.0
    
    @staticmethod
    def validate_impact_score(impact_score: float) -> bool:
        """Validate impact score is in valid range."""
        return 0.0 <= impact_score <= 1.0
    
    @staticmethod
    def validate_priority_level(priority: int) -> bool:
        """Validate priority level is in valid range."""
        return 1 <= priority <= 5
    
    @staticmethod
    def validate_performance_score(score: float) -> bool:
        """Validate performance score is in valid range."""
        return 0.0 <= score <= 1.0
    
    @staticmethod
    def validate_health_score(score: float) -> bool:
        """Validate health score is in valid range."""
        return 0.0 <= score <= 1.0
    
    @staticmethod
    def validate_agent_list(agents: list) -> bool:
        """Validate agent list is not empty."""
        return len(agents) > 0
    
    @staticmethod
    def validate_required_string(value: str, field_name: str) -> Dict[str, Any]:
        """Validate required string field."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        if not value or not value.strip():
            validation['errors'].append(f"{field_name} is required")
            validation['is_valid'] = False
        
        return validation
    
    @staticmethod
    def validate_positive_number(value: float, field_name: str) -> Dict[str, Any]:
        """Validate positive number field."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        if value < 0:
            validation['errors'].append(f"{field_name} must be positive")
            validation['is_valid'] = False
        
        return validation
