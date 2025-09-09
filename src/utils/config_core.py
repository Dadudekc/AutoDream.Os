#!/usr/bin/env python3
"""
🚨 MIGRATION NOTICE: CONFIGURATION CONSOLIDATION
===============================================

This file has been MIGRATED to the SINGLE SOURCE OF TRUTH configuration system.

NEW LOCATION: src/core/config_core.py

This stub file exists only for backward compatibility during the migration period.
All imports should be updated to use: from ..core.config_core import ...

V2 Compliance: Single Source of Truth (SSOT) Implementation
Migration Status: LEGACY FILE - UPDATE IMPORTS IMMEDIATELY

Author: Agent-1 (System Recovery Specialist) - Consolidation Champion
"""

import warnings
from ..core.config_core import *

# Issue deprecation warning
warnings.warn(
    "src.utils.config_core is deprecated. "
    "Use core.config_core instead (Single Source of Truth). "
    "Update your imports: from ..core.config_core import ...",
    DeprecationWarning,
    stacklevel=2
)
