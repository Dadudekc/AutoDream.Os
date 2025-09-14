#!/usr/bin/env python3
"""
🚨 MIGRATION NOTICE: MESSAGING SYSTEM CONSOLIDATION
==================================================

This file has been MIGRATED to the SINGLE SOURCE OF TRUTH messaging system.

NEW LOCATION: src/core/messaging_core.py

This stub file exists only for backward compatibility during the migration period.
All imports should be updated to use: from src.core.messaging_core import ...

V2 Compliance: Single Source of Truth (SSOT) Implementation
Migration Status: LEGACY FILE - UPDATE IMPORTS IMMEDIATELY

Author: Agent-1 (System Recovery Specialist) - Messaging Consolidation Champion
"""

import warnings

from src.core.messaging_core import *

# Issue deprecation warning
warnings.warn(
    "src.services.messaging_core is deprecated. "
    "Use src.core.messaging_core instead (Single Source of Truth). "
    "Update your imports: from src.core.messaging_core import ...",
    DeprecationWarning,
    stacklevel=2
)


# Legacy content removed - use src.core.messaging_core instead
