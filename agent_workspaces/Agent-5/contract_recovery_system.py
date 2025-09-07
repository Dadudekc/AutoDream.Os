#!/usr/bin/env python3
"""
Contract Recovery System - EMERGENCY-RESTORE-004 Mission
=======================================================

This system recovers corrupted contracts and restores database integrity.
Part of the emergency system restoration mission for Agent-5.
"""

import json
import datetime
from pathlib import Path
from typing import Dict, List, Any

class ContractRecoverySystem:
    """Recovers corrupted contracts and restores database integrity"""
    
    def __init__(self, task_list_path: str = "agent_workspaces/meeting/task_list.json"):
        self.task_list_path = Path(task_list_path)
        self.contracts = {}
            
    def load_contracts(self) -> bool:
        """Load contracts from the task list file"""
        try:
            if not self.task_list_path.exists():
                print(f"❌ Task list file not found: {self.task_list_path}")
                return False
                
            with open(self.task_list_path, 'r') as f:
                self.contracts = json.load(f)
                
            print(f"✅ Loaded {self.contracts.get('total_contracts', 0)} contracts")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load contracts: {e}")
            return False
            
    def fix_timestamp_issues(self) -> int:
        """Fix invalid timestamp issues in contracts"""
        fixed_count = 0
        current_time = datetime.datetime.now().isoformat() + "Z"
        
        if "contracts" not in self.contracts:
            return fixed_count
            
        for category_name, category_data in self.contracts["contracts"].items():
            if "contracts" not in category_data:
                continue
                
            for contract in category_data["contracts"]:
                contract_id = contract.get("contract_id", "UNKNOWN")
                
                # Fix future timestamps (impossible dates)
                if "claimed_at" in contract and contract["claimed_at"]:
                    try:
                        # Check if timestamp is in the future
                        claimed_time = datetime.datetime.fromisoformat(
                            contract["claimed_at"].replace('Z', '+00:00')
                        )
                        current_dt = datetime.datetime.now(claimed_time.tzinfo)
                        if claimed_time > current_dt:
                            contract["claimed_at"] = current_time
                            fixed_count += 1
                            print(f"🔧 Fixed future timestamp for {contract_id}")
                    except ValueError:
                        # Invalid timestamp format
                        contract["claimed_at"] = current_time
                        fixed_count += 1
                        print(f"🔧 Fixed invalid timestamp format for {contract_id}")
                        
                if "completed_at" in contract and contract["completed_at"]:
                    try:
                        # Check if timestamp is in the future
                        completed_time = datetime.datetime.fromisoformat(
                            contract["completed_at"].replace('Z', '+00:00')
                        )
                        current_dt = datetime.datetime.now(completed_time.tzinfo)
                        if completed_time > current_dt:
                            contract["completed_at"] = current_time
                            fixed_count += 1
                            print(f"🔧 Fixed future timestamp for {contract_id}")
                    except ValueError:
                        # Invalid timestamp format
                        contract["completed_at"] = current_time
                        fixed_count += 1
                        print(f"🔧 Fixed invalid timestamp format for {contract_id}")
                        
        return fixed_count
        
    def fix_status_inconsistencies(self) -> int:
        """Fix contract status inconsistencies"""
        fixed_count = 0
        
        if "contracts" not in self.contracts:
            return fixed_count
            
        for category_name, category_data in self.contracts["contracts"].items():
            if "contracts" not in category_data:
                continue
                
            for contract in category_data["contracts"]:
                contract_id = contract.get("contract_id", "UNKNOWN")
                status = contract.get("status")
                
                # Fix CLAIMED status without agent assignment
                if status == "CLAIMED" and not contract.get("claimed_by"):
                    contract["status"] = "AVAILABLE"
                    contract.pop("claimed_at", None)
                    fixed_count += 1
                    print(f"🔧 Fixed CLAIMED status without agent for {contract_id}")
                    
                # Fix COMPLETED status without completion timestamp
                elif status == "COMPLETED" and not contract.get("completed_at"):
                    contract["status"] = "CLAIMED"
                    fixed_count += 1
                    print(f"🔧 Fixed COMPLETED status without timestamp for {contract_id}")
                    
                # Fix missing progress field
                if "progress" not in contract:
                    if status == "AVAILABLE":
                        contract["progress"] = "0% Complete - Ready for Claiming"
                    elif status == "CLAIMED":
                        contract["progress"] = "0% Complete - In Progress"
                    elif status == "COMPLETED":
                        contract["progress"] = "100% Complete - Finished"
                    fixed_count += 1
                    print(f"🔧 Added missing progress field for {contract_id}")
                    
        return fixed_count
        
    def recalculate_contract_counts(self) -> bool:
        """Recalculate and fix contract counts"""
        try:
            total_claimed = 0
            total_completed = 0
            total_available = 0
            
            if "contracts" in self.contracts:
                for category_name, category_data in self.contracts["contracts"].items():
                    if "contracts" not in category_data:
                        continue
                        
                    for contract in category_data["contracts"]:
                        status = contract.get("status")
                        if status == "CLAIMED":
                            total_claimed += 1
                        elif status == "COMPLETED":
                            total_completed += 1
                        elif status == "AVAILABLE":
                            total_available += 1
                            
            total_contracts = total_claimed + total_completed + total_available
            
            # Update counts
            self.contracts["claimed_contracts"] = total_claimed
            self.contracts["completed_contracts"] = total_completed
            self.contracts["available_contracts"] = total_available
            self.contracts["total_contracts"] = total_contracts
            
            print(f"✅ Contract counts recalculated:")
            print(f"   Total: {total_contracts}")
            print(f"   Available: {total_available}")
            print(f"   Claimed: {total_claimed}")
            print(f"   Completed: {total_completed}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to recalculate counts: {e}")
            return False
            
    def add_missing_fields(self) -> int:
        """Add missing required fields to contracts"""
        added_count = 0
        
        if "contracts" not in self.contracts:
            return added_count
            
        for category_name, category_data in self.contracts["contracts"].items():
            if "contracts" not in category_data:
                continue
                
            for contract in category_data["contracts"]:
                contract_id = contract.get("contract_id", "UNKNOWN")
                
                # Add missing required fields
                if "extra_credit_claimed" not in contract:
                    contract["extra_credit_claimed"] = False
                    added_count += 1
                    
                if "final_deliverables" not in contract and contract.get("status") == "COMPLETED":
                    contract["final_deliverables"] = contract.get("deliverables", [])
                    added_count += 1
                    
        return added_count
        
    def save_recovered_contracts(self) -> bool:
        """Save the recovered contracts back to the database"""
        try:
            with open(self.task_list_path, 'w') as f:
                json.dump(self.contracts, f, indent=2)
                
            print(f"✅ Recovered contracts saved to: {self.task_list_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save recovered contracts: {e}")
            return False
            
    def run_recovery(self) -> Dict[str, Any]:
        """Run the complete contract recovery process"""
        print("🚨 EMERGENCY-RESTORE-004: CONTRACT DATABASE RECOVERY")
        print("=" * 60)

        # Load contracts
        print("\n📋 Step 1: Loading contracts...")
        if not self.load_contracts():
            return {"success": False, "error": "Failed to load contracts"}

        # Fix issues
        print("\n📋 Step 2: Fixing timestamp issues...")
        timestamp_fixes = self.fix_timestamp_issues()

        print("\n📋 Step 3: Fixing status inconsistencies...")
        status_fixes = self.fix_status_inconsistencies()

        print("\n📋 Step 4: Adding missing fields...")
        field_fixes = self.add_missing_fields()

        print("\n📋 Step 5: Recalculating contract counts...")
        if not self.recalculate_contract_counts():
            return {"success": False, "error": "Failed to recalculate counts"}

        # Save recovered contracts
        print("\n📋 Step 6: Saving recovered contracts...")
        if not self.save_recovered_contracts():
            return {"success": False, "error": "Failed to save recovered contracts"}
            
        # Generate recovery summary
        total_fixes = timestamp_fixes + status_fixes + field_fixes
        
        recovery_summary = {
            "success": True,
            "timestamp_fixes": timestamp_fixes,
            "status_fixes": status_fixes,
            "field_fixes": field_fixes,
            "total_fixes": total_fixes,
            "recovery_timestamp": datetime.datetime.now().isoformat()
        }
        
        print(f"\n🎉 RECOVERY COMPLETE!")
        print(f"   Timestamp fixes: {timestamp_fixes}")
        print(f"   Status fixes: {status_fixes}")
        print(f"   Field fixes: {field_fixes}")
        print(f"   Total fixes: {total_fixes}")

        return recovery_summary

def main():
    """Main function for command-line execution"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Contract Recovery System - EMERGENCY-RESTORE-004 Mission"
    )
    parser.add_argument(
        "--task-list", 
        default="agent_workspaces/meeting/task_list.json",
        help="Path to task list file"
    )
    
    args = parser.parse_args()
    
    # Initialize recovery system
    recovery_system = ContractRecoverySystem(args.task_list)
    
    # Run recovery
    result = recovery_system.run_recovery()
    
    if result["success"]:
        print(f"\n✅ Contract database recovery successful!")
        print(f"   Total fixes applied: {result['total_fixes']}")
        print(f"   Recovery timestamp: {result['recovery_timestamp']}")
    else:
        print(f"\n❌ Contract database recovery failed!")
        print(f"   Error: {result['error']}")
        
    return result["success"]

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
