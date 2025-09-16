#!/usr/bin/env python3
"""
Contracts Test Module
=====================

Modularized contract system test suite.
Replaces the original test_contract_system.py (653 lines)
with 3 V2-compliant modules (≤400 lines each).

Modules:
- test_contract_creation.py: Contract creation and validation tests
- test_contract_execution.py: Contract execution and progress tracking tests
- test_contract_rewards.py: XP rewards and distribution tests

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from .test_contract_creation import TestContractCreation
from .test_contract_execution import TestContractExecution
from .test_contract_rewards import TestXPRewards

__version__ = "2.0.0"
__author__ = "Agent-2 (Architecture & Design Specialist)"

__all__ = [
    "TestContractCreation",
    "TestContractExecution", 
    "TestXPRewards"
]