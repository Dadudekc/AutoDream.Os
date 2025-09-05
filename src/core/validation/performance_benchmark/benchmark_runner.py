#!/usr/bin/env python3
"""
Performance Benchmark Runner
============================

Backward compatibility wrapper for benchmark runner.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

# Import all components from refactored modules
from .benchmark_runner_refactored import *

# Re-export all components for backward compatibility
__all__ = ['BenchmarkRunner']