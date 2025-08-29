#!/usr/bin/env python3
"""
Base Manager Utilities - Agent Cellphone V2
==========================================

Utility methods for the base manager system.
Extracted from base_manager.py to follow Single Responsibility Principle.

**Author:** Agent-3 (Integration & Testing)
**Created:** Current Sprint
**Status:** ACTIVE - REFACTORING IN PROGRESS
"""

from datetime import datetime
from typing import Dict, Any, List


class BaseManagerUtils:
    """
    Utility methods for base managers.
    
    Provides common helper functions for metrics calculation and data formatting.
    """
    
    @staticmethod
    def calculate_success_rate(operations_processed: int, errors_count: int) -> float:
        """Calculate operation success rate"""
        if operations_processed == 0:
            return 100.0
        return ((operations_processed - errors_count) / operations_processed) * 100.0
    
    @staticmethod
    def calculate_error_rate(operations_processed: int, errors_count: int) -> float:
        """Calculate operation error rate"""
        if operations_processed == 0:
            return 0.0
        return (errors_count / operations_processed) * 100.0
    
    @staticmethod
    def calculate_avg_operation_time(operations_history: List[Dict[str, Any]]) -> float:
        """Calculate average operation time"""
        if not operations_history:
            return 0.0
        
        total_time = sum(op.get("duration_ms", 0) for op in operations_history)
        return total_time / len(operations_history)
    
    @staticmethod
    def get_current_timestamp() -> str:
        """Get current timestamp string"""
        return datetime.now().isoformat()
    
    @staticmethod
    def format_uptime(uptime_seconds: float) -> str:
        """Format uptime in human-readable format"""
        if uptime_seconds < 60:
            return f"{uptime_seconds:.1f}s"
        elif uptime_seconds < 3600:
            minutes = uptime_seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = uptime_seconds / 3600
            return f"{hours:.1f}h"
    
    @staticmethod
    def format_performance_score(score: float) -> str:
        """Format performance score as percentage"""
        return f"{score:.1f}%"
    
    @staticmethod
    def validate_operation_data(operation_data: Dict[str, Any]) -> bool:
        """Validate operation data structure"""
        required_fields = ["operation_type", "start_time"]
        return all(field in operation_data for field in required_fields)
    
    @staticmethod
    def sanitize_error_message(error_message: str) -> str:
        """Sanitize error message for logging"""
        # Remove sensitive information and limit length
        sanitized = error_message[:200]  # Limit length
        return sanitized.replace("password", "***").replace("token", "***")

