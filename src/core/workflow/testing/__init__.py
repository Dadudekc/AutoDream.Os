#!/usr/bin/env python3
"""
Workflow Testing Package - Integration Testing Framework
======================================================

Integration testing framework for unified workflow system.
Follows V2 standards: modular, focused testing components.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

from .integration_test_core import IntegrationTestCore
from .integration_test_coordinator import IntegrationTestCoordinator

__all__ = [
    "IntegrationTestCore",
    "IntegrationTestCoordinator"
]

__version__ = "2.0.0"
__author__ = "Agent-3 (Integration & Testing)"
__description__ = "Integration testing framework for workflow system"
