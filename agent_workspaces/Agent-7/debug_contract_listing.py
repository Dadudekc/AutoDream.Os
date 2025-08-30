#!/usr/bin/env python3
"""
Debug Contract Listing - Agent-7
================================

Debug script to test contract listing functionality.
"""

import json
import sys
from pathlib import Path

def debug_contract_listing():
    """Debug the contract listing functionality"""
    print("DEBUG CONTRACT LISTING")
    print("=" * 50)
    
    # Load the task list
    task_list_path = Path("agent_workspaces/meeting/task_list.json")
    
    if not task_list_path.exists():
        print(f"ERROR: Task list not found at {task_list_path}")
        return
    
    try:
        with open(task_list_path, 'r', encoding='utf-8') as f:
            task_list = json.load(f)
        
        print(f"Task list loaded successfully")
        print(f"Root keys: {list(task_list.keys())}")
        
        # Check if contracts key exists
        if "contracts" in task_list:
            print(f"Contracts key found")
            contracts_section = task_list["contracts"]
            print(f"Contracts section keys: {list(contracts_section.keys())}")
            
            # Look for available contracts
            available_count = 0
            available_contracts = []
            
            for category_key, category_data in contracts_section.items():
                if isinstance(category_data, dict) and 'contracts' in category_data:
                    print(f"Category: {category_key}")
                    contracts_list = category_data.get('contracts', [])
                    print(f"  Contracts count: {len(contracts_list)}")
                    
                    for contract in contracts_list:
                        if isinstance(contract, dict):
                            status = contract.get('status', 'UNKNOWN')
                            contract_id = contract.get('contract_id', 'N/A')
                            if status == 'AVAILABLE':
                                available_count += 1
                                available_contracts.append(contract_id)
                                print(f"  AVAILABLE: {contract_id}")
            
            print(f"\nTotal available contracts found: {available_count}")
            print(f"Available contract IDs: {available_contracts}")
            
        else:
            print("ERROR: No 'contracts' key found in task list")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    debug_contract_listing()
