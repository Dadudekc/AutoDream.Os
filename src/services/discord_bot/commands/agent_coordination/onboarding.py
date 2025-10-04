#!/usr/bin/env python3
"""
Deprecation shim for src/services/discord_bot/commands/agent_coordination/onboarding.py

This module provides backward compatibility while redirecting to the
canonical implementation: src.services.agent_hard_onboarding

DEPRECATED: Use the canonical module directly.
"""

import warnings

from src.services.agent_hard_onboarding import *

# Symbol mappings for backward compatibility
# Import from canonical module: src.services.agent_hard_onboarding

# Deprecation warning
warnings.warn(
    "Module src/services/discord_bot/commands/agent_coordination/onboarding.py is deprecated. Use src.services.agent_hard_onboarding directly.",
    DeprecationWarning,
    stacklevel=2,
)
