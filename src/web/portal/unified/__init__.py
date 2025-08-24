#!/usr/bin/env python3
"""
Unified Web Portal - V2 Core Web Integration

This package provides the unified web portal that serves as the central
interface for all agent systems, providing navigation, dashboards, and
integration points.
Follows V2 standards: ≤300 LOC per module, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .enums import PortalSection, AgentDashboard
from .data_models import PortalConfig, AgentPortalInfo, PortalNavigation
from .portal_core import UnifiedPortal
from .flask_app import FlaskPortalApp
from .fastapi_app import FastAPIPortalApp
from .portal_factory import PortalFactory

__all__ = [
    # Enums
    'PortalSection',
    'AgentDashboard',
    
    # Data Models
    'PortalConfig',
    'AgentPortalInfo',
    'PortalNavigation',
    
    # Core Components
    'UnifiedPortal',
    'FlaskPortalApp',
    'FastAPIPortalApp',
    'PortalFactory',
]
