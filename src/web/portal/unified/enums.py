#!/usr/bin/env python3
"""
Unified Portal Enums - V2 Core Web Integration

Portal navigation sections and dashboard types.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from enum import Enum


class PortalSection(Enum):
    """Portal navigation sections"""
    DASHBOARD = "dashboard"
    AGENTS = "agents"
    AUTOMATION = "automation"
    PROJECTS = "projects"
    COORDINATION = "coordination"
    SETTINGS = "settings"
    HELP = "help"
    MONITORING = "monitoring"
    REPORTS = "reports"
    INTEGRATIONS = "integrations"
    SECURITY = "security"
    PERFORMANCE = "performance"


class AgentDashboard(Enum):
    """Agent-specific dashboard types"""
    PROJECT_MANAGEMENT = "project_management"
    COORDINATION = "coordination"
    WEB_DEVELOPMENT = "web_development"
    AUTOMATION = "automation"
    DATA_ANALYSIS = "data_analysis"
    SYSTEM_ADMIN = "system_admin"
    USER_INTERFACE = "user_interface"
    INTEGRATION = "integration"
    FINANCIAL = "financial"
    GAMING = "gaming"
    MULTIMEDIA = "multimedia"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"
    SECURITY = "security"
