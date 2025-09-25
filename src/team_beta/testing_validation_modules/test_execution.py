#!/usr/bin/env python3
"""
Test Execution Module - Main Interface
======================================

Main interface for Team Beta Testing Validation System
V2 Compliant: ≤50 lines, focused interface and coordination
"""

from .test_execution_core import TestExecutor

# Main interface - TestExecutor is now provided by test_execution_core module
# This file serves as the main entry point for backward compatibility

__all__ = ['TestExecutor']