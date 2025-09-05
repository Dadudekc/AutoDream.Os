#!/usr/bin/env python3
"""
Contract Handler Refactored - V2 Compliance Module
==================================================

Main refactored entry point for contract handler.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

from .contract_handler_core import ContractHandlerCore
from .contract_handler_operations import ContractHandlerOperations


class ContractHandler(ContractHandlerCore, ContractHandlerOperations):
    """Unified contract handler with core and operations functionality."""
    
    def __init__(self):
        """Initialize unified contract handler."""
        ContractHandlerCore.__init__(self)
        ContractHandlerOperations.__init__(self)
