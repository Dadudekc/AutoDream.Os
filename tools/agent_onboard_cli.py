#!/usr/bin/env python3
"""
Deprecation shim for tools/agent_onboard_cli.py

This module provides backward compatibility while redirecting to the
canonical implementation: src.services.agent_hard_onboarding

DEPRECATED: Use the canonical module directly.
"""

import warnings

# Symbol mappings for backward compatibility
# Import from canonical module: src.services.agent_hard_onboarding
from src.services.agent_hard_onboarding import *

# Deprecation warning
warnings.warn(
    "Module tools/agent_onboard_cli.py is deprecated. Use src.services.agent_hard_onboarding directly.",
    DeprecationWarning,
    stacklevel=2,
)
