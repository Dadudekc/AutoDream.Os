#!/usr/bin/env python3
"""
Deprecation shim for src.services.consolidated_messaging_service

This module provides backward compatibility while redirecting to the
canonical implementation.

DEPRECATED: Use the canonical module directly.
"""

import warnings

from src.services.messaging_service import *

# Deprecation warning
warnings.warn(
    "Module src.services.messaging_service is the canonical implementation.",
    DeprecationWarning,
    stacklevel=2,
)
