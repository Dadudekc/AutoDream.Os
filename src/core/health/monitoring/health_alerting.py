#!/usr/bin/env python3
"""
Health Alerting System - V2 Compliant Redirect
==============================================

This module redirects to the new modular alerting system.
V2 COMPLIANT: Under 50 lines, simple import redirect.

Author: Agent-3 (Infrastructure Specialist)
License: MIT
"""

# Import all components from the new modular alerting system
from .alerts import (
    AlertChannel,
    AlertChannelConfig,
    AlertChannelManager,
    AlertChannelType,
    EmailAlertChannel,
    LogAlertChannel,
    SlackAlertChannel,
    AlertEscalationEngine,
    AlertInstance,
    EscalationLevel,
    EscalationPolicy,
    HealthAlert,
    HealthAlertingSystem,
    AlertSeverity
)

# For backward compatibility
__all__ = [
    "AlertChannel",
    "AlertChannelConfig",
    "AlertChannelManager", 
    "AlertChannelType",
    "EmailAlertChannel",
    "LogAlertChannel",
    "SlackAlertChannel",
    "AlertEscalationEngine",
    "AlertInstance",
    "EscalationLevel",
    "EscalationPolicy",
    "HealthAlert",
    "HealthAlertingSystem",
    "AlertSeverity"
]