"""
Contract Claiming System Models Package
Contains data models and enums for the contract claiming system.
"""

# Import directly to avoid relative import issues
try:
    from contract_status import ContractStatus
    from contract import Contract
except ImportError:
    # Fallback for when running as module
    from .contract_status import ContractStatus
    from .contract import Contract

__all__ = ['Contract', 'ContractStatus']
