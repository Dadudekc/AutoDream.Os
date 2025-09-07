#!/usr/bin/env python3
"""
Status Validation Fix - EMERGENCY-RESTORE-004 Mission
====================================================

This script identifies and fixes contracts with invalid status values.
"""

import json
from pathlib import Path

def fix_invalid_statuses():
    """Fix contracts with invalid status values"""
    task_list_path = Path("../meeting/task_list.json")
    
    # Load the current contracts
    with open(task_list_path, 'r') as f:
        contracts = json.load(f)
    
    print("🔍 Analyzing contract statuses for invalid values...")
    
    # Valid statuses
    valid_statuses = ["AVAILABLE", "CLAIMED", "COMPLETED"]
    
    # Track status issues
    invalid_status_contracts = []
    status_counts = {"AVAILABLE": 0, "CLAIMED": 0, "COMPLETED": 0, "INVALID": 0}
    
    if "contracts" in contracts:
        for category_name, category_data in contracts["contracts"].items():
            if "contracts" in category_data:
                for contract in category_data["contracts"]:
                    contract_id = contract.get("contract_id", "UNKNOWN")
                    status = contract.get("status")
                    
                    if status in valid_statuses:
                        status_counts[status] += 1
                    else:
                        status_counts["INVALID"] += 1
                        invalid_status_contracts.append({
                            "contract_id": contract_id,
                            "current_status": status,
                            "category": category_name
                        })
                        
                        # Fix invalid status to AVAILABLE
                        contract["status"] = "AVAILABLE"
                        status_counts["AVAILABLE"] += 1
                        print(f"🔧 Fixed invalid status for {contract_id}: {status} → AVAILABLE")
    
    print(f"\n📊 Status analysis:")
    print(f"   Available: {status_counts['AVAILABLE']}")
    print(f"   Claimed: {status_counts['CLAIMED']}")
    print(f"   Completed: {status_counts['COMPLETED']}")
    print(f"   Invalid (fixed): {status_counts['INVALID']}")
    
    # Update header counts
    contracts["total_contracts"] = status_counts["AVAILABLE"] + status_counts["CLAIMED"] + status_counts["COMPLETED"]
    contracts["available_contracts"] = status_counts["AVAILABLE"]
    contracts["claimed_contracts"] = status_counts["CLAIMED"]
    contracts["completed_contracts"] = status_counts["COMPLETED"]
    
    print(f"\n📊 Updated header counts:")
    print(f"   Total: {contracts['total_contracts']}")
    print(f"   Available: {contracts['available_contracts']}")
    print(f"   Claimed: {contracts['claimed_contracts']}")
    print(f"   Completed: {contracts['completed_contracts']}")
    
    # Save the fixed contracts
    with open(task_list_path, 'w') as f:
        json.dump(contracts, f, indent=2)
    
    print(f"\n✅ Status validation fix applied and saved!")
    
    if invalid_status_contracts:
        print(f"\n🔧 Fixed {len(invalid_status_contracts)} contracts with invalid statuses:")
        for contract in invalid_status_contracts:
            print(f"   - {contract['contract_id']}: {contract['current_status']} → AVAILABLE")
    
    return {
        "total": contracts["total_contracts"],
        "available": contracts["available_contracts"],
        "claimed": contracts["claimed_contracts"],
        "completed": contracts["completed_contracts"],
        "invalid_fixed": len(invalid_status_contracts)
    }

if __name__ == "__main__":
    print("🚨 STATUS VALIDATION FIX - EMERGENCY-RESTORE-004")
    print("=" * 55)
    
    result = fix_invalid_statuses()
    
    print(f"\n🎉 Status validation complete!")
    print(f"   Total contracts: {result['total']}")
    print(f"   Available: {result['available']}")
    print(f"   Claimed: {result['claimed']}")
    print(f"   Completed: {result['completed']}")
    print(f"   Invalid statuses fixed: {result['invalid_fixed']}")
    
    # Verify consistency
    calculated = result['available'] + result['claimed'] + result['completed']
    if result['total'] == calculated:
        print(f"✅ All counts are now consistent!")
    else:
        print(f"⚠️  Counts still have discrepancies!")
