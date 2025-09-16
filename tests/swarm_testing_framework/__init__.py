#!/usr/bin/env python3
"""
Swarm Testing Framework Module
==============================

Modularized swarm testing framework.
Replaces the original swarm_testing_framework.py (651 lines)
with 3 V2-compliant modules (≤400 lines each).

Modules:
- swarm_testing_framework_core.py: Core components and data structures
- swarm_testing_framework_execution.py: Test execution and progress tracking
- swarm_testing_framework_reporting.py: Report generation and analytics
- swarm_testing_framework_main.py: Main orchestration and CLI

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from .swarm_testing_framework_core import (
    ComponentDiscovery,
    CoverageCalculator,
    SwarmTestingReport,
    TestFileManager,
    TestingComponent,
)
from .swarm_testing_framework_execution import TestExecutor
from .swarm_testing_framework_main import SwarmTestingFramework
from .swarm_testing_framework_reporting import ReportGenerator

__version__ = "2.0.0"
__author__ = "Agent-2 (Architecture & Design Specialist)"

__all__ = [
    "TestingComponent",
    "SwarmTestingReport",
    "ComponentDiscovery",
    "TestFileManager",
    "CoverageCalculator",
    "TestExecutor",
    "ReportGenerator",
    "SwarmTestingFramework",
]
