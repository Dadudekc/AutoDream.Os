"""
Browser Infrastructure - V2 Consolidation
=========================================

Unified browser automation for Thea Manager.
Consolidated from 15→5 files by Agent-3.

Author: Agent-3 (Infrastructure & DevOps) - Browser Consolidation
"""

from .browser_models import BrowserConfig
from .thea_browser_service import TheaBrowserService, create_thea_browser_service
from .thea_content_operations import (
    ScrapedContent,
    TheaContentOperations,
    create_thea_content_operations,
)
from .thea_session_management import TheaSessionManagement, create_thea_session_management

__all__ = [
    # Models
    "BrowserConfig",
    "ScrapedContent",
    # Services
    "TheaBrowserService",
    "TheaSessionManagement",
    "TheaContentOperations",
    # Factories
    "create_thea_browser_service",
    "create_thea_session_management",
    "create_thea_content_operations",
]
