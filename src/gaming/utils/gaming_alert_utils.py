"""
Gaming Alert Utilities

Extracted utility functions for gaming alert system to achieve V2 compliance.
Contains alert creation, validation, and formatting utilities.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Implementation - Gaming Infrastructure Refactoring
"""

import time
import logging
from datetime import datetime
from typing import Dict, Any, List
from ..models.gaming_alert_models import GamingAlert, AlertType, AlertSeverity

logger = logging.getLogger(__name__)


def create_alert_id(alert_type: AlertType, existing_count: int) -> str:
    """
    Create a unique alert ID.
    
    Args:
        alert_type: Type of alert
        existing_count: Current count of alerts
        
    Returns:
        Unique alert ID string
    """
    return f"gaming_alert_{int(time.time())}_{existing_count}"


def validate_alert_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and sanitize alert metadata.
    
    Args:
        metadata: Raw metadata dictionary
        
    Returns:
        Validated metadata dictionary
    """
    if not metadata:
        return {}
    
    # Ensure metadata values are serializable
    validated = {}
    for key, value in metadata.items():
        if isinstance(value, (str, int, float, bool, list, dict)):
            validated[key] = value
        else:
            validated[key] = str(value)
    
    return validated


def format_alert_message(alert_type: AlertType, severity: AlertSeverity, 
                        details: Dict[str, Any]) -> str:
    """
    Format alert message based on type and severity.
    
    Args:
        alert_type: Type of alert
        severity: Alert severity level
        details: Alert details dictionary
        
    Returns:
        Formatted alert message string
    """
    base_message = f"{severity.value.upper()} {alert_type.value.replace('_', ' ')} alert"
    
    if details:
        detail_str = ", ".join([f"{k}: {v}" for k, v in details.items()])
        return f"{base_message}: {detail_str}"
    
    return base_message


def calculate_alert_priority(severity: AlertSeverity, alert_type: AlertType) -> int:
    """
    Calculate alert priority score.
    
    Args:
        severity: Alert severity level
        alert_type: Type of alert
        
    Returns:
        Priority score (higher = more important)
    """
    severity_scores = {
        AlertSeverity.LOW: 1,
        AlertSeverity.MEDIUM: 2,
        AlertSeverity.HIGH: 3,
        AlertSeverity.CRITICAL: 4
    }
    
    type_scores = {
        AlertType.CRITICAL: 2,
        AlertType.SYSTEM_HEALTH: 1.5,
        AlertType.PERFORMANCE: 1.2,
        AlertType.USER_ENGAGEMENT: 1.0,
        AlertType.GAME_STATE: 0.8,
        AlertType.ENTERTAINMENT_SYSTEM: 0.6
    }
    
    return severity_scores[severity] * type_scores.get(alert_type, 1.0)
