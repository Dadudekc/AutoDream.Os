"""
Common Utility Functions
Captain Agent-3: Shared, Non-Duplicated Utilities
"""

import json
import hashlib
from typing import Any, Dict

def generate_hash(data: Any) -> str:
    """Generate hash for data - single implementation"""
    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

def validate_config(config: Dict) -> bool:
    """Validate configuration - single implementation"""
    required_keys = ['name', 'version', 'status']
    return all(key in config for key in required_keys)

def format_response(data: Any, status: str = "success") -> Dict:
    """Format response - single implementation"""
    return {"status": status, "data": data, "timestamp": "2025-08-28T22:15:00.000000Z"}
