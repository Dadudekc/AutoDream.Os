#!/usr/bin/env python3
"""
Discord Commander Swarm - Redirect to Unified System
===================================================

This file redirects to the unified Discord system to eliminate DRY violations.

Original functionality moved to: src/core/unified-discord-system.py
"""

import sys
from pathlib import Path

# Redirect to the unified Discord system
sys.path.insert(0, str(Path(__file__).parent))
from core.unified_discord_system import get_unified_discord, send_status

# Re-export for backward compatibility
__all__ = ['get_unified_discord', 'send_status']