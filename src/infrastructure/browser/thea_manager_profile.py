"""
Thea Manager Profile - V2 Compliance Refactored
==============================================

Specialized profile for THEA Manager GPT with modular architecture.
Refactored into focused modules for V2 compliance (< 400 lines).

This profile handles Victor Dixon's THEA Manager requirements:
- Autonomous AI orchestrator for project cleanup and optimization
- Specialized webscraping for project analysis
- Integrated authentication and session management
- Enhanced cursor response detection with DOM polling

V2 COMPLIANCE: Modular architecture, single responsibility principle
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
from typing import Optional, Dict, List, Any

# Import modular components
from .thea_modules import (
    TheaManagerProfile,
    TheaConfigManager,
    TheaManagerConfig,
    ScrapedContent
)

logger = logging.getLogger(__name__)

# Re-export for backward compatibility
__all__ = [
    'TheaManagerProfile',
    'TheaConfigManager',
    'TheaManagerConfig',
    'ScrapedContent'
]