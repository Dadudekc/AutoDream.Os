"""
Learning Utilities - Helper Functions
Captain Agent-3: MODULAR-001 Implementation
"""

import json
from typing import Dict, Any, List

def validate_learning_config(config: Dict[str, Any]) -> bool:
    """Validate learning configuration"""
    required_keys = ['module_type', 'parameters', 'version']
    return all(key in config for key in required_keys)

def format_learning_result(result: Any, status: str = "success") -> Dict[str, Any]:
    """Format learning result"""
    return {
        "result": result,
        "status": status,
        "timestamp": "2025-08-28T22:55:00.000000Z"
    }

def get_learning_metrics(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract learning metrics from session data"""
    return {
        "duration": session_data.get("duration", 0),
        "progress": session_data.get("progress", 0),
        "accuracy": session_data.get("accuracy", 0.0)
    }
