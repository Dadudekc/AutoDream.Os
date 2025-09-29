#!/usr/bin/env python3
"""
Contract Utils
==============

Utility functions for contract management and operations.
V2 Compliance: ≤100 lines, utility functions, KISS principle.
"""

import logging
from datetime import UTC, datetime
from typing import Any

from .contract_models import ContractPriority, ContractStatus, V3Contract

logger = logging.getLogger(__name__)


def filter_contracts_by_status(
    contracts: list[V3Contract], status: ContractStatus
) -> list[V3Contract]:
    """Filter contracts by status."""
    return [contract for contract in contracts if contract.status == status]


def filter_contracts_by_priority(
    contracts: list[V3Contract], priority: ContractPriority
) -> list[V3Contract]:
    """Filter contracts by priority."""
    return [contract for contract in contracts if contract.priority == priority]


def get_contract_by_id(contracts: list[V3Contract], contract_id: str) -> V3Contract | None:
    """Get contract by ID."""
    for contract in contracts:
        if contract.contract_id == contract_id:
            return contract
    return None


def update_contract_status(
    contract: V3Contract, status: ContractStatus, agent_id: str | None = None
) -> None:
    """Update contract status and timestamp."""
    try:
        contract.status = status
        contract.updated_at = datetime.now(UTC)

        if agent_id:
            contract.assigned_agent = agent_id

        logger.info(f"Contract {contract.contract_id} status updated to {status.value}")

    except Exception as e:
        logger.error(f"Failed to update contract status: {e}")


def calculate_contract_metrics(contracts: list[V3Contract]) -> dict[str, Any]:
    """Calculate contract metrics."""
    try:
        total_contracts = len(contracts)

        status_counts = {}
        for status in ContractStatus:
            status_counts[status.value] = len(filter_contracts_by_status(contracts, status))

        priority_counts = {}
        for priority in ContractPriority:
            priority_counts[priority.value] = len(filter_contracts_by_priority(contracts, priority))

        return {
            "total_contracts": total_contracts,
            "status_distribution": status_counts,
            "priority_distribution": priority_counts,
            "completion_rate": (status_counts["completed"] / total_contracts * 100)
            if total_contracts > 0
            else 0,
        }

    except Exception as e:
        logger.error(f"Failed to calculate contract metrics: {e}")
        return {"error": str(e)}


def validate_contract_structure(contract: V3Contract) -> dict[str, Any]:
    """Validate contract structure."""
    try:
        issues = []

        # Check required fields
        if not contract.contract_id or not contract.contract_id.strip():
            issues.append("Missing contract ID")

        if not contract.title or not contract.title.strip():
            issues.append("Missing contract title")

        if not contract.description or not contract.description.strip():
            issues.append("Missing contract description")

        # Check ID format
        if contract.contract_id and not contract.contract_id.startswith("V3-"):
            issues.append("Invalid contract ID format (should start with 'V3-')")

        # Check cycles requirement
        if contract.cycles_required < 1:
            issues.append("Cycles required must be at least 1")

        return {"is_valid": len(issues) == 0, "issues": issues}

    except Exception as e:
        logger.error(f"Failed to validate contract structure: {e}")
        return {"is_valid": False, "issues": [f"Validation error: {str(e)}"]}
