#!/usr/bin/env python3
"""
Simple Validation - KISS Compliant
==================================

Simple validation functions following KISS principles.
No overengineering, no complex patterns, just simple validation.

Author: Agent-8 - SSOT & System Integration Specialist
Mission: KISS Simplification
"""

def validate_string(value, min_length=1, max_length=1000):
    """Validate string value."""
    if not isinstance(value, str):
        return False, "Must be string"
    if len(value) < min_length:
        return False, f"Too short (min {min_length})"
    if len(value) > max_length:
        return False, f"Too long (max {max_length})"
    return True, "Valid"

def validate_number(value, min_val=None, max_val=None):
    """Validate number value."""
    if not isinstance(value, (int, float)):
        return False, "Must be number"
    if min_val is not None and value < min_val:
        return False, f"Too small (min {min_val})"
    if max_val is not None and value > max_val:
        return False, f"Too large (max {max_val})"
    return True, "Valid"

def validate_email(email):
    """Validate email address."""
    if not isinstance(email, str):
        return False, "Must be string"
    if "@" not in email or "." not in email:
        return False, "Invalid email format"
    return True, "Valid"

def validate_required(data, required_fields):
    """Validate required fields."""
    missing = [field for field in required_fields if field not in data]
    if missing:
        return False, f"Missing fields: {missing}"
    return True, "Valid"

def validate_json(data):
    """Validate JSON data."""
    try:
        import json
        json.dumps(data)
        return True, "Valid JSON"
    except Exception as e:
        return False, f"Invalid JSON: {e}"
