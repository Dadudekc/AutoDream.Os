#!/usr/bin/env python3
"""
Contract Claiming System for Agent Efficiency Optimization
Created by Agent-2 (PHASE TRANSITION OPTIMIZATION MANAGER)

This system allows agents to claim, track, and complete contracts for extra credit.
NOTE: All agents use --message flag for fresh coordination, not --onboarding flag.
"""

import json
import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class ContractClaimingSystem:
    def __init__(self, task_list_path: str = "task_list.json"):
        self.task_list_path = Path(task_list_path)
        self.contracts = self.load_contracts()
        
    def load_contracts(self) -> Dict[str, Any]:
        """Load the current task list and contracts."""
        try:
            with open(self.task_list_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Task list not found at {self.task_list_path}")
            return {}
            
    def save_contracts(self) -> bool:
        """Save the updated contracts to the task list file."""
        try:
            with open(self.task_list_path, 'w') as f:
                json.dump(self.contracts, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving contracts: {e}")
            return False
            
    def list_available_contracts(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all available contracts, optionally filtered by category."""
        available = []
        
        for category_name, category_data in self.contracts.get("contracts", {}).items():
            if category and category_name != category.upper():
                continue
                
            for contract in category_data.get("contracts", []):
                if contract.get("status") == "AVAILABLE":
                    contract_copy = contract.copy()
                    contract_copy["category"] = category_data["category"]
                    contract_copy["manager"] = category_data["manager"]
                    available.append(contract_copy)
                    
        return available
        
    def claim_contract(self, contract_id: str, agent_id: str) -> Dict[str, Any]:
        """Claim a contract for an agent."""
        timestamp = datetime.datetime.now().isoformat() + "Z"
        
        for category_name, category_data in self.contracts.get("contracts", {}).items():
            for contract in category_data.get("contracts", []):
                if contract.get("contract_id") == contract_id:
                    if contract.get("status") != "AVAILABLE":
                        return {
                            "success": False,
                            "message": f"Contract {contract_id} is not available for claiming",
                            "current_status": contract.get("status")
                        }
                        
                    # Claim the contract
                    contract["status"] = "CLAIMED"
                    contract["claimed_by"] = agent_id
                    contract["claimed_at"] = timestamp
                    contract["progress"] = "0% Complete - In Progress"
                    
                    # Update statistics
                    self.contracts["available_contracts"] -= 1
                    self.contracts["claimed_contracts"] += 1
                    
                    # Save changes
                    if self.save_contracts():
                        return {
                            "success": True,
                            "message": f"Contract {contract_id} successfully claimed by {agent_id}",
                            "contract": contract
                        }
                    else:
                        return {
                            "success": False,
                            "message": "Failed to save contract changes"
                        }
                        
        return {
            "success": False,
            "message": f"Contract {contract_id} not found"
        }
        
    def update_contract_progress(self, contract_id: str, agent_id: str, progress: str) -> Dict[str, Any]:
        """Update the progress of a claimed contract."""
        for category_name, category_data in self.contracts.get("contracts", {}).items():
            for contract in category_data.get("contracts", []):
                if contract.get("contract_id") == contract_id:
                    if contract.get("claimed_by") != agent_id:
                        return {
                            "success": False,
                            "message": f"Contract {contract_id} is not claimed by {agent_id}"
                        }
                        
                    if contract.get("status") != "CLAIMED":
                        return {
                            "success": False,
                            "message": f"Contract {contract_id} is not in CLAIMED status"
                        }
                        
                    # Update progress
                    contract["progress"] = progress
                    
                    # Save changes
                    if self.save_contracts():
                        return {
                            "success": True,
                            "message": f"Progress updated for contract {contract_id}",
                            "contract": contract
                        }
                    else:
                        return {
                            "success": False,
                            "message": "Failed to save contract changes"
                        }
                        
        return {
            "success": False,
            "message": f"Contract {contract_id} not found"
        }
        
    def complete_contract(self, contract_id: str, agent_id: str, deliverables: List[str]) -> Dict[str, Any]:
        """Complete a contract and claim extra credit."""
        timestamp = datetime.datetime.now().isoformat() + "Z"
        
        for category_name, category_data in self.contracts.get("contracts", {}).items():
            for contract in category_data.get("contracts", []):
                if contract.get("contract_id") == contract_id:
                    if contract.get("claimed_by") != agent_id:
                        return {
                            "success": False,
                            "message": f"Contract {contract_id} is not claimed by {agent_id}"
                        }
                        
                    if contract.get("status") != "CLAIMED":
                        return {
                            "success": False,
                            "message": f"Contract {contract_id} is not in CLAIMED status"
                        }
                        
                    # Complete the contract
                    contract["status"] = "COMPLETED"
                    contract["completed_at"] = timestamp
                    contract["extra_credit_claimed"] = True
                    contract["final_deliverables"] = deliverables
                    contract["progress"] = "100% Complete - Finished"
                    
                    # Update statistics
                    self.contracts["claimed_contracts"] -= 1
                    self.contracts["completed_contracts"] += 1
                    
                    # Calculate extra credit points
                    base_points = contract.get("extra_credit_points", 0)
                    difficulty = contract.get("difficulty", "MEDIUM")
                    
                    # Apply difficulty multiplier
                    difficulty_multipliers = {
                        "LOW": 1.0,
                        "MEDIUM": 1.2,
                        "HIGH": 1.5
                    }
                    
                    final_points = int(base_points * difficulty_multipliers.get(difficulty, 1.0))
                    
                    # Save changes
                    if self.save_contracts():
                        return {
                            "success": True,
                            "message": f"Contract {contract_id} completed successfully!",
                            "extra_credit_earned": final_points,
                            "contract": contract
                        }
                    else:
                        return {
                            "success": False,
                            "message": "Failed to save contract changes"
                        }
                        
        return {
            "success": False,
            "message": f"Contract {contract_id} not found"
        }
        
    def get_agent_contracts(self, agent_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get all contracts for a specific agent."""
        agent_contracts = {
            "claimed": [],
            "completed": []
        }
        
        for category_name, category_data in self.contracts.get("contracts", {}).items():
            for contract in category_data.get("contracts", []):
                if contract.get("claimed_by") == agent_id:
                    contract_copy = contract.copy()
                    contract_copy["category"] = category_data["category"]
                    contract_copy["manager"] = category_data["manager"]
                    
                    if contract.get("status") == "CLAIMED":
                        agent_contracts["claimed"].append(contract_copy)
                    elif contract.get("status") == "COMPLETED":
                        agent_contracts["completed"].append(contract_copy)
                        
        return agent_contracts
        
    def get_contract_statistics(self) -> Dict[str, Any]:
        """Get overall contract statistics."""
        return {
            "total_contracts": self.contracts.get("total_contracts", 0),
            "available_contracts": self.contracts.get("available_contracts", 0),
            "claimed_contracts": self.contracts.get("claimed_contracts", 0),
            "completed_contracts": self.contracts.get("completed_contracts", 0),
            "total_extra_credit": self.contracts.get("extra_credit_system", {}).get("total_available_points", 0)
        }
        
    def display_available_contracts(self, category: Optional[str] = None):
        """Display available contracts in a readable format."""
        available = self.list_available_contracts(category)
        
        if not available:
            print("No available contracts found.")
            return
            
        print(f"\n{'='*80}")
        print(f"AVAILABLE CONTRACTS{' - ' + category.upper() if category else ''}")
        print(f"{'='*80}")
        
        for contract in available:
            print(f"\n📋 Contract ID: {contract['contract_id']}")
            print(f"📝 Title: {contract['title']}")
            print(f"📖 Description: {contract['description']}")
            print(f"⚡ Difficulty: {contract['difficulty']}")
            print(f"⏱️  Estimated Time: {contract['estimated_time']}")
            print(f"🏆 Extra Credit: {contract['extra_credit_points']} points")
            print(f"👤 Manager: {contract['manager']}")
            print(f"📋 Requirements: {', '.join(contract['requirements'])}")
            print(f"📦 Deliverables: {', '.join(contract['deliverables'])}")
            print("-" * 80)

def main():
    """Main function to demonstrate the contract claiming system."""
    system = ContractClaimingSystem()
    
    print("🤖 AGENT CONTRACT CLAIMING SYSTEM")
    print("=" * 50)
    print("Created by Agent-2 (PHASE TRANSITION OPTIMIZATION MANAGER)")
    print("=" * 50)
    
    while True:
        print("\n📋 Available Actions:")
        print("1. List all available contracts")
        print("2. List contracts by category")
        print("3. Claim a contract")
        print("4. Update contract progress")
        print("5. Complete a contract")
        print("6. View agent contracts")
        print("7. View statistics")
        print("8. Exit")
        
        choice = input("\n🎯 Select an action (1-8): ").strip()
        
        if choice == "1":
            system.display_available_contracts()
            
        elif choice == "2":
            categories = ["coordination_enhancement", "phase_transition_optimization", 
                        "testing_framework_enhancement", "strategic_oversight", 
                        "refactoring_tool_preparation", "performance_optimization"]
            print("\n📂 Available categories:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            
            cat_choice = input("\n🎯 Select category (1-6): ").strip()
            try:
                cat_index = int(cat_choice) - 1
                if 0 <= cat_index < len(categories):
                    system.display_available_contracts(categories[cat_index])
                else:
                    print("❌ Invalid category selection")
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif choice == "3":
            contract_id = input("\n🎯 Enter contract ID to claim: ").strip()
            agent_id = input("👤 Enter your agent ID: ").strip()
            
            result = system.claim_contract(contract_id, agent_id)
            if result["success"]:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
                
        elif choice == "4":
            contract_id = input("\n🎯 Enter contract ID: ").strip()
            agent_id = input("👤 Enter your agent ID: ").strip()
            progress = input("📊 Enter progress update: ").strip()
            
            result = system.update_contract_progress(contract_id, agent_id, progress)
            if result["success"]:
                print(f"✅ {result['message']}")
            else:
                print(f"❌ {result['message']}")
                
        elif choice == "5":
            contract_id = input("\n🎯 Enter contract ID: ").strip()
            agent_id = input("👤 Enter your agent ID: ").strip()
            print("📦 Enter deliverables (comma-separated):")
            deliverables_input = input().strip()
            deliverables = [d.strip() for d in deliverables_input.split(",")]
            
            result = system.complete_contract(contract_id, agent_id, deliverables)
            if result["success"]:
                print(f"✅ {result['message']}")
                print(f"🏆 Extra credit earned: {result['extra_credit_earned']} points!")
            else:
                print(f"❌ {result['message']}")
                
        elif choice == "6":
            agent_id = input("\n👤 Enter agent ID: ").strip()
            agent_contracts = system.get_agent_contracts(agent_id)
            
            print(f"\n📋 Contracts for {agent_id}:")
            print(f"Claimed: {len(agent_contracts['claimed'])}")
            print(f"Completed: {len(agent_contracts['completed'])}")
            
            if agent_contracts['claimed']:
                print("\n🔄 CLAIMED CONTRACTS:")
                for contract in agent_contracts['claimed']:
                    print(f"  - {contract['contract_id']}: {contract['title']} ({contract['progress']})")
                    
            if agent_contracts['completed']:
                print("\n✅ COMPLETED CONTRACTS:")
                for contract in agent_contracts['completed']:
                    print(f"  - {contract['contract_id']}: {contract['title']} (+{contract['extra_credit_points']} points)")
                    
        elif choice == "7":
            stats = system.get_contract_statistics()
            print(f"\n📊 CONTRACT STATISTICS:")
            print(f"Total Contracts: {stats['total_contracts']}")
            print(f"Available: {stats['available_contracts']}")
            print(f"Claimed: {stats['claimed_contracts']}")
            print(f"Completed: {stats['completed_contracts']}")
            print(f"Total Extra Credit: {stats['total_extra_credit']} points")
            
        elif choice == "8":
            print("\n👋 Thank you for using the Agent Contract Claiming System!")
            print("🏆 Good luck with your contracts and extra credit!")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-8.")

if __name__ == "__main__":
    main()
