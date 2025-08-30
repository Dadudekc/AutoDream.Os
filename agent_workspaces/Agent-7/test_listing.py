#!/usr/bin/env python3
"""
Test Contract Listing - Agent-7
================================

Test script to test the list_available_contracts method directly.
"""

import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from agent_workspaces.meeting.contract_claiming_system import ContractClaimingSystem

def test_listing():
    """Test the listing functionality"""
    print("TESTING CONTRACT LISTING")
    print("=" * 50)
    
    # Initialize the system
    system = ContractClaimingSystem("agent_workspaces/meeting/task_list.json")
    
    # Test listing
    print("Testing list_available_contracts...")
    available = system.list_available_contracts()
    
    print(f"Available contracts returned: {len(available) if available else 0}")
    
    if available:
        print("Available contracts:")
        for contract in available:
            contract_id = contract.get('contract_id', 'N/A')
            title = contract.get('title', 'N/A')
            status = contract.get('status', 'N/A')
            print(f"  {contract_id}: {title} ({status})")
    else:
        print("No available contracts returned")
    
    # Test stats for comparison
    print("\nTesting get_contract_statistics...")
    stats = system.get_contract_statistics()
    print(f"Stats: {stats}")

if __name__ == "__main__":
    test_listing()
