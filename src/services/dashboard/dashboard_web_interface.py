#!/usr/bin/env python3
"""
Swarm Coordination Dashboard Web Interface - REFACTORED
=======================================================

This file has been refactored into 3 V2-compliant modules:
- dashboard_web_core.py (186 lines) - Core HTTP handling and API logic
- dashboard_web_interface.py (398 lines) - HTML generation and UI components  
- dashboard_web_utils.py (117 lines) - Utility functions and helpers

Total: 701 lines → 3 modules (186 + 398 + 117 = 701 lines)
V2 Compliance: ✅ All modules ≤400 lines

Author: Agent-8 (Documentation Specialist)
License: MIT
"""

# Import the refactored modules
from .dashboard_web_core import DashboardWebHandler, DashboardWebServer
from .dashboard_web_html import generate_dashboard_html
from .dashboard_web_utils import (
    format_agent_data, format_task_data, format_alert_data,
    validate_request_data, sanitize_string, parse_json_request,
    format_json_response, get_current_timestamp, calculate_performance_score,
    format_summary_stats, validate_agent_status, validate_task_status,
    validate_alert_type, truncate_text
)

# Re-export the main classes for backward compatibility
__all__ = [
    'DashboardWebHandler',
    'DashboardWebServer', 
    'generate_dashboard_html',
    'format_agent_data',
    'format_task_data', 
    'format_alert_data',
    'validate_request_data',
    'sanitize_string',
    'parse_json_request',
    'format_json_response',
    'get_current_timestamp',
    'calculate_performance_score',
    'format_summary_stats',
    'validate_agent_status',
    'validate_task_status',
    'validate_alert_type',
    'truncate_text'
]