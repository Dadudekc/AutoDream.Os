"""
Modularized Contract Claiming System
A refactored version of the original monolithic contract claiming system.

This package demonstrates proper separation of concerns and follows V2 coding standards:
- Each module ≤400 lines
- Clear separation of responsibilities
- CLI interfaces for testing
- Proper OOP design
"""

from .core.contract_manager import ContractManager
from .core.contract_validator import ContractValidator
from .core.contract_persistence import ContractPersistence
from .operations.contract_lister import ContractLister
from .cli.cli_interface import ContractClaimingCLI

__version__ = "2.0.0"
__author__ = "Agent-1"
__description__ = "Modularized Contract Claiming System"

__all__ = [
    'ContractManager',
    'ContractValidator', 
    'ContractPersistence',
    'ContractLister',
    'ContractClaimingCLI'
]
