#!/usr/bin/env python3
"""
Unified Logging System - V2 Compliance Module
============================================

Backward compatibility wrapper for unified logging system.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .unified_logging_system_refactored import UnifiedLoggingSystem
from .unified_logging_system_models import LogLevel, LoggingConfig
from .unified_logging_system_engine import LoggingTemplates

# Backward compatibility - export the refactored class and components
__all__ = ['UnifiedLoggingSystem', 'LogLevel', 'LoggingConfig', 'LoggingTemplates']
