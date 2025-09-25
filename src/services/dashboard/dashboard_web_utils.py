#!/usr/bin/env python3
"""
Swarm Coordination Dashboard Web Utils
======================================

Utility functions and helpers for the Swarm Coordination Dashboard.
Provides data formatting, validation, and helper functions.

Author: Agent-8 (Documentation Specialist)
License: MIT
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


def format_agent_data(agent_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format agent data for API response"""
    return {
        "agent_id": agent_data.get("agent_id", ""),
        "status": agent_data.get("status", "unknown"),
        "current_task": agent_data.get("current_task", ""),
        "last_activity": agent_data.get("last_activity", ""),
        "performance_score": agent_data.get("performance_score", 0),
        "message_count": agent_data.get("message_count", 0),
        "error_count": agent_data.get("error_count", 0)
    }


def format_task_data(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format task data for API response"""
    return {
        "task_id": task_data.get("task_id", ""),
        "title": task_data.get("title", ""),
        "status": task_data.get("status", "unknown"),
        "assigned_agent": task_data.get("assigned_agent", ""),
        "priority": task_data.get("priority", "medium"),
        "progress": task_data.get("progress", 0),
        "updated_at": task_data.get("updated_at", "")
    }


def format_alert_data(alert_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format alert data for API response"""
    return {
        "alert_id": alert_data.get("alert_id", ""),
        "type": alert_data.get("type", "info"),
        "message": alert_data.get("message", ""),
        "timestamp": alert_data.get("timestamp", ""),
        "acknowledged": alert_data.get("acknowledged", False)
    }


def validate_request_data(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """Validate request data has required fields"""
    return all(field in data for field in required_fields)


def sanitize_string(value: str, max_length: int = 1000) -> str:
    """Sanitize string input"""
    if not isinstance(value, str):
        return str(value)
    
    # Remove potentially dangerous characters
    sanitized = value.replace('<', '&lt;').replace('>', '&gt;')
    sanitized = sanitized.replace('"', '&quot;').replace("'", '&#x27;')
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized


def parse_json_request(request_data: bytes) -> Optional[Dict[str, Any]]:
    """Parse JSON request data safely"""
    try:
        return json.loads(request_data.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def format_json_response(data: Any, indent: int = 2) -> str:
    """Format data as JSON response"""
    return json.dumps(data, indent=indent, default=str)


def get_current_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now(timezone.utc).isoformat()


def calculate_performance_score(agent_data: Dict[str, Any]) -> int:
    """Calculate agent performance score"""
    message_count = agent_data.get("message_count", 0)
    error_count = agent_data.get("error_count", 0)
    
    if message_count == 0:
        return 0
    
    error_rate = error_count / message_count
    performance = max(0, min(100, int((1 - error_rate) * 100)))
    
    return performance


def format_summary_stats(agents: Dict[str, Any], tasks: Dict[str, Any], alerts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Format summary statistics"""
    active_agents = sum(1 for agent in agents.values() if agent.get("status") == "active")
    completed_tasks = sum(1 for task in tasks.values() if task.get("status") == "completed")
    total_tasks = len(tasks)
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    pending_alerts = sum(1 for alert in alerts if not alert.get("acknowledged", False))
    
    return {
        "active_agents": active_agents,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate,
        "pending_alerts": pending_alerts,
        "total_agents": len(agents),
        "total_tasks": total_tasks
    }


def validate_agent_status(status: str) -> bool:
    """Validate agent status value"""
    valid_statuses = ["active", "working", "error", "offline", "idle"]
    return status.lower() in valid_statuses


def validate_task_status(status: str) -> bool:
    """Validate task status value"""
    valid_statuses = ["pending", "in-progress", "completed", "failed", "cancelled"]
    return status.lower() in valid_statuses


def validate_alert_type(alert_type: str) -> bool:
    """Validate alert type value"""
    valid_types = ["info", "warning", "error", "success"]
    return alert_type.lower() in valid_types


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."