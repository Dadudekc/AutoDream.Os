#!/usr/bin/env python3
"""
Final Count Fix - EMERGENCY-RESTORE-004 Mission
===============================================

This script fixes the final count discrepancy between header and data.
"""

import json
from pathlib import Path

def fix_final_counts():
    """Fix the final count discrepancy"""
    task_list_path = Path("../meeting/task_list.json")
    
    # Load the current contracts
    with open(task_list_path, 'r') as f:
        contracts = json.load(f)
    
    print("🔍 Analyzing final count discrepancy...")
    
    # Count actual contracts and their statuses
    total_actual = 0
    available_actual = 0
    claimed_actual = 0
    completed_actual = 0
    
    if "contracts" in contracts:
        for category_name, category_data in contracts["contracts"].items():
            if "contracts" in category_data:
                for contract in category_data["contracts"]:
                    total_actual += 1
                    status = contract.get("status")
                    if status == "AVAILABLE":
                        available_actual += 1
                    elif status == "CLAIMED":
                        claimed_actual += 1
                    elif status == "COMPLETED":
                        completed_actual += 1
    
    print(f"📊 Actual data counts:")
    print(f"   Total: {total_actual}")
    print(f"   Available: {available_actual}")
    print(f"   Claimed: {claimed_actual}")
    print(f"   Completed: {completed_actual}")
    
    # Verify the math
    calculated_total = available_actual + claimed_actual + completed_actual
    print(f"   Calculated: {calculated_total}")
    
    if calculated_total != total_actual:
        print(f"⚠️  Warning: Status counts don't add up to total!")
        print(f"   This suggests some contracts have invalid status values")
    
    # Update the header counts to match actual data
    contracts["total_contracts"] = total_actual
    contracts["available_contracts"] = available_actual
    contracts["claimed_contracts"] = claimed_actual
    contracts["completed_contracts"] = completed_actual
    
    print(f"\n📊 Updated header counts:")
    print(f"   Total: {contracts['total_contracts']}")
    print(f"   Available: {contracts['available_contracts']}")
    print(f"   Claimed: {contracts['claimed_contracts']}")
    print(f"   Completed: {contracts['completed_contracts']}")
    
    # Save the fixed contracts
    with open(task_list_path, 'w') as f:
        json.dump(contracts, f, indent=2)
    
    print(f"\n✅ Final count fix applied and saved!")
    
    return {
        "total": total_actual,
        "available": available_actual,
        "claimed": claimed_actual,
        "completed": completed_actual,
        "calculated": calculated_total
    }

if __name__ == "__main__":
    print("🚨 FINAL COUNT FIX - EMERGENCY-RESTORE-004")
    print("=" * 50)
    
    result = fix_final_counts()
    
    print(f"\n🎉 Final fix complete!")
    print(f"   Total contracts: {result['total']}")
    print(f"   Available: {result['available']}")
    print(f"   Claimed: {result['claimed']}")
    print(f"   Completed: {result['completed']}")
    print(f"   Calculated: {result['calculated']}")
    
    if result['total'] == result['calculated']:
        print(f"✅ All counts are now consistent!")
    else:
        print(f"⚠️  Counts still have discrepancies - manual review needed")
