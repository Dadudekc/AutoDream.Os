#!/usr/bin/env python3
"""
Contract Availability Checker - Agent-7 Enhancement
==================================================

Checks contract availability and identifies blocking factors.
Part of the contract claiming enhancement system.

Author: Agent-7 - Quality Completion Optimization Manager
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.contracting.claim_utils import load_tasks, validate_contract

def check_contract_availability():
    """Check contract availability"""
    print("CONTRACT AVAILABILITY CHECKER")
    print("=" * 40)
    
    # Check task list directly
    task_list = load_tasks("agent_workspaces/meeting/task_list.json")
    if task_list:
        print("OK Task list loaded successfully")

        # Analyze contract availability
        contracts_section = task_list.get("contracts", {})
        total_contracts = 0
        available_contracts = 0

        for contract_type, contract_data in contracts_section.items():
            if isinstance(contract_data, dict) and 'contracts' in contract_data:
                contracts_list = contract_data.get('contracts', [])
                if isinstance(contracts_list, list):
                    for contract in contracts_list:
                        if isinstance(contract, dict) and validate_contract(contract):
                            total_contracts += 1
                            if contract.get('status') == 'AVAILABLE':
                                available_contracts += 1

        print(f"Total contracts found: {total_contracts}")
        print(f"Available contracts: {available_contracts}")
    else:
        print("ERROR Error loading task list")
    
    print(f"\nAvailability check completed at: {datetime.now()}")

if __name__ == "__main__":
    check_contract_availability()
