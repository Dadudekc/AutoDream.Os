#!/usr/bin/env python3
"""
Thea Service - Unified V2 Implementation
=========================================

Single unified Thea communication service.

This is the SINGLE authoritative Thea implementation,
consolidating 25+ scattered files into one modular service.

Usage:
    from src.services.thea import TheaService

    # Simple usage
    thea = TheaService()
    result = thea.communicate("Hello Thea!")
    print(result['response'])

    # With context manager
    with TheaService(headless=False) as thea:
        result = thea.communicate("Hello Thea!")
        print(result['response'])

Author: Agent-2 (Architecture) - V2 Consolidation
License: MIT
"""

from .thea_browser import TheaBrowser
from .thea_config import TheaConfig
from .thea_cookies import TheaCookieManager
from .thea_detector import TheaDetector
from .thea_messaging import TheaMessenger
from .thea_service_unified import TheaService, create_thea_service

__all__ = [
    "TheaService",
    "create_thea_service",
    "TheaConfig",
    "TheaBrowser",
    "TheaCookieManager",
    "TheaMessenger",
    "TheaDetector",
]

__version__ = "2.0.0"
__author__ = "Agent-2 (Architecture) - V2 Consolidation"
