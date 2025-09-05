#!/usr/bin/env python3
"""
Error Analysis Engine - V2 Compliant
===================================

Error analysis, severity assessment, and recovery analysis.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant error analysis and assessment
"""

from typing import Dict, Any, List
from datetime import datetime
from .error_handling_models import (
    ErrorSummary, ErrorSeverity, ErrorSeverityMapping, RecoverableErrors
)


class ErrorAnalysisEngine:
    """Engine for error analysis and assessment."""
    
    def __init__(self):
        """Initialize error analysis engine."""
        pass
    
    def create_error_summary(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create error summary from list of errors.
        
        Args:
            errors: List of error dictionaries
            
        Returns:
            Dict[str, Any]: Error summary
        """
        if not errors:
            return ErrorSummary().to_dict()
        
        error_types = {}
        operations = {}
        
        for error in errors:
            # Count error types
            error_type = error.get("error_type", "Unknown")
            error_types[error_type] = error_types.get(error_type, 0) + 1
            
            # Count operations
            operation = error.get("operation", "Unknown")
            operations[operation] = operations.get(operation, 0) + 1
        
        summary = ErrorSummary(
            total_errors=len(errors),
            error_types=error_types,
            operations=operations
        )
        
        return summary.to_dict()
    
    def is_recoverable_error(self, error: Exception) -> bool:
        """
        Check if error is recoverable.
        
        Args:
            error: Exception to check
            
        Returns:
            bool: True if error is recoverable
        """
        return isinstance(error, RecoverableErrors.TYPES)
    
    def get_error_severity(self, error: Exception) -> str:
        """
        Get error severity level.
        
        Args:
            error: Exception to analyze
            
        Returns:
            str: Severity level (low, medium, high, critical)
        """
        if isinstance(error, ErrorSeverityMapping.CRITICAL):
            return ErrorSeverity.CRITICAL.value
        elif isinstance(error, ErrorSeverityMapping.HIGH):
            return ErrorSeverity.HIGH.value
        elif isinstance(error, ErrorSeverityMapping.MEDIUM):
            return ErrorSeverity.MEDIUM.value
        else:
            return ErrorSeverity.LOW.value
    
    def analyze_error_patterns(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze error patterns from error list.
        
        Args:
            errors: List of error dictionaries
            
        Returns:
            Dict[str, Any]: Pattern analysis results
        """
        if not errors:
            return {
                "patterns": {},
                "recommendations": [],
                "critical_issues": []
            }
        
        patterns = {}
        recommendations = []
        critical_issues = []
        
        # Analyze error frequency by type
        error_counts = {}
        for error in errors:
            error_type = error.get("error_type", "Unknown")
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        # Identify high-frequency errors
        total_errors = len(errors)
        for error_type, count in error_counts.items():
            frequency = count / total_errors
            if frequency > 0.3:  # More than 30% of errors
                patterns[error_type] = {
                    "count": count,
                    "frequency": frequency,
                    "severity": "high"
                }
                recommendations.append(f"Address frequent {error_type} errors ({count} occurrences)")
        
        # Identify critical issues
        for error in errors:
            error_type = error.get("error_type")
            if error_type in ["SystemError", "MemoryError", "KeyboardInterrupt"]:
                critical_issues.append({
                    "error_type": error_type,
                    "operation": error.get("operation", "Unknown"),
                    "timestamp": error.get("timestamp", "Unknown")
                })
        
        return {
            "patterns": patterns,
            "recommendations": recommendations,
            "critical_issues": critical_issues,
            "total_analyzed": total_errors
        }
    
    def calculate_error_trends(self, errors: List[Dict[str, Any]], time_window_hours: int = 24) -> Dict[str, Any]:
        """
        Calculate error trends over time.
        
        Args:
            errors: List of error dictionaries
            time_window_hours: Time window for trend analysis
            
        Returns:
            Dict[str, Any]: Trend analysis results
        """
        if not errors:
            return {
                "trend": "stable",
                "error_rate": 0.0,
                "peak_hours": [],
                "declining_errors": [],
                "increasing_errors": []
            }
        
        # Simple trend analysis - would be more sophisticated in production
        recent_errors = len([e for e in errors[-100:]])  # Last 100 errors as proxy
        older_errors = len([e for e in errors[-200:-100]])  # Previous 100 errors
        
        if recent_errors > older_errors * 1.2:
            trend = "increasing"
        elif recent_errors < older_errors * 0.8:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "error_rate": recent_errors / max(1, time_window_hours),
            "recent_count": recent_errors,
            "previous_count": older_errors,
            "change_percentage": ((recent_errors - older_errors) / max(1, older_errors)) * 100
        }
    
    def get_recovery_recommendations(self, error: Exception, context: Dict[str, Any] = None) -> List[str]:
        """
        Get recovery recommendations for specific error.
        
        Args:
            error: Exception to analyze
            context: Additional context information
            
        Returns:
            List[str]: Recovery recommendations
        """
        recommendations = []
        error_type = type(error).__name__
        
        # General recommendations based on error type
        if isinstance(error, FileNotFoundError):
            recommendations.extend([
                "Verify file path exists",
                "Check file permissions",
                "Ensure directory structure is created"
            ])
        elif isinstance(error, PermissionError):
            recommendations.extend([
                "Check file/directory permissions",
                "Run with appropriate privileges",
                "Verify user access rights"
            ])
        elif isinstance(error, ConnectionError):
            recommendations.extend([
                "Check network connectivity",
                "Verify service endpoint availability",
                "Consider retry with exponential backoff"
            ])
        elif isinstance(error, TimeoutError):
            recommendations.extend([
                "Increase timeout duration",
                "Check service response time",
                "Consider breaking operation into smaller chunks"
            ])
        elif isinstance(error, ValueError):
            recommendations.extend([
                "Validate input parameters",
                "Check data format and types",
                "Review function arguments"
            ])
        else:
            recommendations.append("Review error details and context for specific resolution")
        
        # Add severity-based recommendations
        severity = self.get_error_severity(error)
        if severity == ErrorSeverity.CRITICAL.value:
            recommendations.insert(0, "CRITICAL: Immediate attention required")
        elif severity == ErrorSeverity.HIGH.value:
            recommendations.insert(0, "HIGH PRIORITY: Address as soon as possible")
        
        return recommendations
    
    def assess_system_health(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assess overall system health based on error patterns.
        
        Args:
            errors: List of recent error dictionaries
            
        Returns:
            Dict[str, Any]: System health assessment
        """
        if not errors:
            return {
                "health_score": 100,
                "status": "excellent",
                "concerns": [],
                "recommendations": ["Continue monitoring"]
            }
        
        total_errors = len(errors)
        critical_errors = len([e for e in errors if e.get("error_type") in ["SystemError", "MemoryError"]])
        
        # Simple health scoring
        if critical_errors > 0:
            health_score = max(0, 50 - (critical_errors * 10))
            status = "critical"
        elif total_errors > 50:
            health_score = max(20, 80 - (total_errors - 50))
            status = "degraded"
        elif total_errors > 20:
            health_score = max(60, 90 - (total_errors - 20))
            status = "fair"
        else:
            health_score = max(80, 100 - total_errors)
            status = "good"
        
        concerns = []
        recommendations = []
        
        if critical_errors > 0:
            concerns.append(f"{critical_errors} critical errors detected")
            recommendations.append("Investigate critical errors immediately")
        
        if total_errors > 30:
            concerns.append(f"High error volume: {total_errors} errors")
            recommendations.append("Review error patterns and implement preventive measures")
        
        return {
            "health_score": health_score,
            "status": status,
            "total_errors": total_errors,
            "critical_errors": critical_errors,
            "concerns": concerns,
            "recommendations": recommendations
        }
