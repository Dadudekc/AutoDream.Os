#!/usr/bin/env python3
"""
Contract Availability Checker - Agent-7 Enhancement
==================================================

Checks contract availability and identifies blocking factors.
Part of the contract claiming enhancement system.

Author: Agent-7 - Quality Completion Optimization Manager
"""

import json
import subprocess
import sys
from datetime import datetime

def check_contract_availability():
    """Check contract availability"""
    print("CONTRACT AVAILABILITY CHECKER")
    print("=" * 40)
    
    # Check task list directly
    try:
        with open("agent_workspaces/meeting/task_list.json", 'r') as f:
            task_list = json.load(f)
        
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
                        if isinstance(contract, dict):
                            total_contracts += 1
                            status = contract.get('status', 'UNKNOWN')
                            if status == 'AVAILABLE':
                                available_contracts += 1
        
        print(f"Total contracts found: {total_contracts}")
        print(f"Available contracts: {available_contracts}")
        
    except Exception as e:
        print(f"ERROR Error loading task list: {e}")
    
    print(f"\nAvailability check completed at: {datetime.now()}")

if __name__ == "__main__":
    check_contract_availability()
