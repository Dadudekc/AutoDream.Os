#!/usr/bin/env python3
"""
Benchmark Runner Refactored - V2 Compliance Module
==================================================

Main refactored entry point for benchmark runner.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

from .benchmark_runner_core import BenchmarkRunnerCore
from .benchmark_runner_operations import BenchmarkRunnerOperations


class BenchmarkRunner(BenchmarkRunnerCore, BenchmarkRunnerOperations):
    """Unified benchmark runner with core and operations functionality."""
    
    def __init__(self):
        """Initialize unified benchmark runner."""
        BenchmarkRunnerCore.__init__(self)
        BenchmarkRunnerOperations.__init__(self)
