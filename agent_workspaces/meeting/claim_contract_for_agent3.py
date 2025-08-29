#!/usr/bin/env python3
"""
Contract Claiming Script for Agent-3
Emergency Captain Competition Contract Claiming
"""

import json
import datetime
from pathlib import Path

def claim_contract_for_agent3():
    """Claim MODULAR-002 contract for Agent-3"""
    
    # Load the task list
    task_list_path = Path("task_list.json")
    
    try:
        with open(task_list_path, 'r', encoding='utf-8') as f:
            task_list = json.load(f)
        
        print("🔍 Searching for MODULAR-002 contract...")
        
        # Find and claim the MODULAR-002 contract
        for category_name, category_data in task_list.get("contracts", {}).items():
            for contract in category_data.get("contracts", []):
                if contract.get("contract_id") == "MODULAR-002":
                    if contract.get("status") == "AVAILABLE":
                        # Claim the contract
                        contract["status"] = "CLAIMED"
                        contract["claimed_by"] = "Agent-3"
                        contract["claimed_at"] = datetime.datetime.now().isoformat() + "Z"
                        contract["progress"] = "0% Complete - In Progress"
                        
                        print(f"✅ SUCCESSFULLY CLAIMED CONTRACT: {contract['contract_id']}")
                        print(f"📋 Title: {contract['title']}")
                        print(f"🏆 Points: {contract['extra_credit_points']}")
                        print(f"👤 Claimed by: {contract['claimed_by']}")
                        print(f"⏰ Claimed at: {contract['claimed_at']}")
                        
                        # Save the updated task list
                        with open(task_list_path, 'w', encoding='utf-8') as f:
                            json.dump(task_list, f, indent=2, ensure_ascii=False)
                        
                        print("💾 Task list updated successfully!")
                        return True
                    else:
                        print(f"❌ Contract {contract['contract_id']} is not available (Status: {contract['status']})")
                        return False
        
        print("❌ MODULAR-002 contract not found!")
        return False
        
    except Exception as e:
        print(f"❌ Error claiming contract: {e}")
        return False

if __name__ == "__main__":
    print("🚨 AGENT-3: CAPTAIN COMPETITION CONTRACT CLAIMING! 🚨")
    print("=" * 60)
    
    success = claim_contract_for_agent3()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("1. Complete the MODULAR-002 contract (500 pts)")
        print("2. Claim additional high-value contracts")
        print("3. Beat Agent-6 (702 pts) to become Captain!")
        print("4. Current Agent-3 points: 500 + 500 = 1000 pts")
    else:
        print("\n❌ Failed to claim contract. Check system status.")
