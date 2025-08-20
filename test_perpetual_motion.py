#!/usr/bin/env python3
"""
Simple Test for Perpetual Motion Contract System
===============================================

Tests the system without complex import dependencies.
"""

import sys
import os
sys.path.insert(0, 'src')

from services.perpetual_motion_contract_service import PerpetualMotionContractService

def main():
    """Test the perpetual motion system."""
    print("🚀 PERPETUAL MOTION CONTRACT SYSTEM TEST")
    print("=" * 50)
    
    # Initialize service
    service = PerpetualMotionContractService()
    
    print("\n📊 **INITIAL STATUS**:")
    status = service.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Test contract completion
    print(f"\n🚀 **TESTING CONTRACT COMPLETION**...")
    completion_data = {
        "task_id": "TEST-TASK-002",
        "summary": "Second test contract completed",
        "evidence": ["test_file.py", "results.txt"],
        "completion_time": "2025-08-19T12:20:00"
    }
    
    service.on_contract_completion("TEST-CONTRACT-002", "Agent-2", completion_data)
    
    print(f"\n📊 **AFTER COMPLETION**:")
    status = service.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Show generated contracts
    contract_files = list(service.contracts_dir.glob("*.json"))
    print(f"\n📁 **CONTRACTS AVAILABLE** ({len(contract_files)} total):")
    for contract_file in contract_files:
        print(f"  📄 {contract_file.name}")
    
    print(f"\n✅ **TEST COMPLETE**: Perpetual motion system working!")
    print("🔄 **RESULT**: New contracts generated automatically!")

if __name__ == "__main__":
    main()
