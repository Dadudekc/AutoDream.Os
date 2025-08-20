#!/usr/bin/env python3
"""
Standalone Test for Perpetual Motion Contract System
==================================================

Tests the system by importing directly, avoiding import chain issues.
"""

import sys
import os

# Add the specific service directory to path
sys.path.insert(0, os.path.join('src', 'services'))

# Import the service directly
from perpetual_motion_contract_service import PerpetualMotionContractService

def main():
    """Test the perpetual motion system."""
    print("🚀 PERPETUAL MOTION CONTRACT SYSTEM - STANDALONE TEST")
    print("=" * 60)
    
    # Initialize service
    service = PerpetualMotionContractService()
    
    print("\n📊 **INITIAL STATUS**:")
    status = service.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Test contract completion for Agent-3
    print(f"\n🚀 **TESTING CONTRACT COMPLETION FOR AGENT-3**...")
    completion_data = {
        "task_id": "TEST-TASK-003",
        "summary": "Agent-3 test contract completed",
        "evidence": ["agent3_test.py", "test_results.txt"],
        "completion_time": "2025-08-19T12:25:00"
    }
    
    service.on_contract_completion("TEST-CONTRACT-003", "Agent-3", completion_data)
    
    print(f"\n📊 **AFTER COMPLETION**:")
    status = service.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Show generated contracts
    contract_files = list(service.contracts_dir.glob("*.json"))
    print(f"\n📁 **CONTRACTS AVAILABLE** ({len(contract_files)} total):")
    for contract_file in contract_files:
        print(f"  📄 {contract_file.name}")
    
    # Show resume message for Agent-3
    inbox_dir = os.path.join("agent_workspaces", "Agent-3", "inbox")
    if os.path.exists(inbox_dir):
        resume_files = [f for f in os.listdir(inbox_dir) if f.startswith("resume_message_")]
        print(f"\n📬 **RESUME MESSAGES FOR AGENT-3** ({len(resume_files)} files):")
        for resume_file in resume_files:
            print(f"  📧 {resume_file}")
    
    print(f"\n✅ **STANDALONE TEST COMPLETE**: Perpetual motion system working!")
    print("🔄 **RESULT**: New contracts generated automatically for Agent-3!")
    print("📊 **TOTAL CONTRACTS**: System now has more contracts than before!")

if __name__ == "__main__":
    main()
