#!/usr/bin/env python3
"""
Coordinate Validator - Redirect to Unified System
================================================

This file redirects to the unified validation system to eliminate DRY violations.

Original functionality moved to: src/core/unified-validation-system.py
"""

import sys
from pathlib import Path

# Redirect to the unified validation system
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.unified_validation_system import validate_coordinates, ValidationIssue

# Re-export for backward compatibility
__all__ = ['validate_coordinates', 'ValidationIssue']