#!/usr/bin/env python3
"""
Coordination Validator Core - Redirect to Unified System
=======================================================

This file redirects to the unified validation system to eliminate DRY violations.

Original functionality moved to: src/core/unified-validation-system.py
"""

import sys
from pathlib import Path

# Redirect to the unified validation system
sys.path.insert(0, str(Path(__file__).parent.parent))
from unified_validation_system import validate_coordination_system, ValidationIssue

# Re-export for backward compatibility
__all__ = ['validate_coordination_system', 'ValidationIssue']