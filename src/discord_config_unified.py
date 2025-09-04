#!/usr/bin/env python3
"""
Discord Config Unified - Redirect to Unified System
==================================================

This file redirects to the unified configuration system to eliminate DRY violations.

Original functionality moved to: src/core/unified-configuration-system.py
"""

import sys
from pathlib import Path

# Redirect to the unified configuration system
sys.path.insert(0, str(Path(__file__).parent))
from core.unified_configuration_system import get_unified_config, get_config

# Re-export for backward compatibility
__all__ = ['get_unified_config', 'get_config']