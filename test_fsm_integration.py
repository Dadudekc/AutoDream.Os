#!/usr/bin/env python3
"""
Test script for FSM integration debugging
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.core.fsm_contract_integration import FSMContractIntegration
    print("✅ FSM integration imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_fsm_integration():
    """Test the FSM integration step by step"""
    print("🚀 Testing FSM Integration Step by Step")
    print("=" * 50)
    
    # Create FSM integration instance
    fsm = FSMContractIntegration()
    print(f"✅ FSM integration created with {len(fsm.agents)} agents and {len(fsm.contracts)} contracts")
    
    # Test 1: Check initial state
    print("\n📊 Test 1: Initial State")
    print(f"Agent-7 state: {fsm.fsm_states['Agent-7']}")
    print(f"Agent-7 current_contract: {fsm.agents['Agent-7'].current_contract}")
    
    # Test 2: Get available contracts
    print("\n📋 Test 2: Available Contracts")
    available = fsm.get_available_contracts()
    print(f"Available contracts: {len(available)}")
    for contract in available[:3]:  # Show first 3
        print(f"  - {contract.contract_id}: {contract.title}")
    
    # Test 3: Claim contract
    print("\n📋 Test 3: Claim Contract COORD-001")
    success = fsm.claim_contract_for_agent("Agent-7", "COORD-001")
    print(f"Claim result: {success}")
    
    # Test 4: Check state after claiming
    print("\n📊 Test 4: State After Claiming")
    print(f"Agent-7 FSM state: {fsm.fsm_states['Agent-7']}")
    print(f"Agent-7 current_contract: {fsm.agents['Agent-7'].current_contract}")
    if fsm.agents['Agent-7'].current_contract:
        print(f"Contract details: {fsm.agents['Agent-7'].current_contract.contract_id} - {fsm.agents['Agent-7'].current_contract.title}")
    
    # Test 5: Check contract status
    print("\n📊 Test 5: Contract Status")
    contract = fsm.contracts.get("COORD-001")
    if contract:
        print(f"COORD-001 status: {contract.status}")
        print(f"COORD-001 agent_id: {contract.agent_id}")
        print(f"COORD-001 claimed_at: {contract.claimed_at}")
    
    # Test 6: Get agent status summary
    print("\n📊 Test 6: Agent Status Summary")
    summary = fsm.get_agent_status_summary()
    agent_7_status = summary['agent_states']['Agent-7']
    print(f"Agent-7 summary state: {agent_7_status['current_state']}")
    print(f"Agent-7 summary contract: {agent_7_status['current_contract']}")
    
    # Test 7: Start work
    print("\n🚀 Test 7: Start Work")
    work_started = fsm.start_contract_work("Agent-7")
    print(f"Work start result: {work_started}")
    
    # Test 8: Final state check
    print("\n📊 Test 8: Final State Check")
    print(f"Agent-7 FSM state: {fsm.fsm_states['Agent-7']}")
    print(f"Agent-7 current_contract: {fsm.agents['Agent-7'].current_contract}")
    
    print("\n✅ FSM integration test completed!")

if __name__ == "__main__":
    test_fsm_integration()
