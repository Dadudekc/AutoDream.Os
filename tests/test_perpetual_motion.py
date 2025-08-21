#!/usr/bin/env python3
"""
🧪 TEST: Perpetual Motion Contract System
==========================================

This script tests the perpetual motion system to ensure contracts
automatically generate new contracts when completed.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from services.perpetual_motion_contract_service import PerpetualMotionContractService

def test_perpetual_motion_cycle():
    """Test the complete perpetual motion cycle."""
    print("🧪 TESTING PERPETUAL MOTION CONTRACT SYSTEM")
    print("=" * 50)
    
    # Initialize service
    service = PerpetualMotionContractService()
    
    # Test 1: Generate initial contracts
    print("\n📋 TEST 1: Generating initial contracts...")
    initial_contracts = service._generate_new_contracts("Agent-1", 3)
    for contract in initial_contracts:
        service._save_contract(contract)
    print(f"✅ Generated {len(initial_contracts)} initial contracts")
    
    # Test 2: Simulate contract completion
    print("\n🔄 TEST 2: Simulating contract completion...")
    test_data = {
        "test": True,
        "timestamp": "2025-01-19T10:00:00",
        "message": "Testing perpetual motion system"
    }
    
    result = service.detect_contract_completion("Agent-1", "fsm_update", test_data)
    
    if result:
        print("✅ PERPETUAL MOTION TRIGGERED SUCCESSFULLY!")
        print("🔄 New contracts should be generated automatically")
        
        # Check what was created
        print("\n📊 CHECKING RESULTS:")
        
        # Check contracts directory
        contracts = list(service.contracts_dir.glob("*.json"))
        print(f"📁 Contracts available: {len(contracts)}")
        
        # Check agent workspace
        agent_tasks = list(Path("agent_workspaces/Agent-1/tasks").glob("*.json"))
        print(f"📋 Tasks assigned: {len(agent_tasks)}")
        
        # Check agent inbox
        agent_inbox = list(Path("agent_workspaces/Agent-1/inbox").glob("*.json"))
        print(f"📬 Inbox messages: {len(agent_inbox)}")
        
        # Check metrics
        metrics_file = Path("persistent_data/perpetual_motion_metrics.json")
        if metrics_file.exists():
            print("📊 Perpetual motion metrics updated")
        else:
            print("⚠️ No metrics file found")
            
    else:
        print("❌ PERPETUAL MOTION TEST FAILED")
        print("No completion detected or error occurred")
    
    print("\n" + "=" * 50)
    print("🧪 TEST COMPLETE")
    
    return result

if __name__ == "__main__":
    test_perpetual_motion_cycle()
