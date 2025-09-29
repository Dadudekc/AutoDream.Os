#!/usr/bin/env python3
"""
V3 Contract System Package
==========================

Modular contract execution system for V3 components.
V2 Compliance: All modules ≤400 lines, focused responsibilities.
"""

from .contract_execution_core import ContractExecutionCore
from .contract_models import ContractPriority, ContractStatus, V3Contract, create_default_contracts
from .contract_performance_monitor import ContractPerformanceMonitor
from .contract_quality_validator import ContractQualityValidator
from .contract_utils import (
    calculate_contract_metrics,
    filter_contracts_by_priority,
    filter_contracts_by_status,
    get_contract_by_id,
    update_contract_status,
    validate_contract_structure,
)

__all__ = [
    "ContractPriority",
    "ContractStatus",
    "V3Contract",
    "create_default_contracts",
    "ContractExecutionCore",
    "ContractQualityValidator",
    "ContractPerformanceMonitor",
    "filter_contracts_by_status",
    "filter_contracts_by_priority",
    "get_contract_by_id",
    "update_contract_status",
    "calculate_contract_metrics",
    "validate_contract_structure",
]
