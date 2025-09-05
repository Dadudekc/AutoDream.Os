#!/usr/bin/env python3
"""
DRY Elimination Violation Detection Engine (V2 Refactored)
=========================================================

V2 Refactored violation detection engine for DRY elimination system.
Handles duplicate detection, unused code detection, and violation analysis.

V2 COMPLIANT: Focused violation detection under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR VIOLATION DETECTION
@license MIT
"""

# V2 Refactored - Backward Compatibility Wrapper
from .violation_detection_engine_refactored import ViolationDetectionEngine

# Maintain backward compatibility
__all__ = ['ViolationDetectionEngine']


def create_violation_detection_engine() -> ViolationDetectionEngine:
    """Create a new violation detection engine instance"""
    return ViolationDetectionEngine()