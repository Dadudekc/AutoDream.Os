#!/usr/bin/env python3
"""
Agent Contract Completion Form - Agent Cellphone V2
==================================================

Simple form for agents to mark contracts as completed.
This triggers the Captain instruction system to create new contracts.
"""

import sys
import json
from pathlib import Path

def get_contract_completion_details():
    """Get contract completion details from user"""
    print("🎯 AGENT CONTRACT COMPLETION FORM")
    print("=" * 50)
    print("Complete this form to mark your contract as done!")
    print("This will prompt Captain-5 to create new contracts for you!")
    print("=" * 50)
    
    # Get contract ID
    contract_id = input("Enter Contract ID (e.g., CONTRACT-001): ").strip()
    if not contract_id:
        print("❌ Contract ID is required")
        return None
    
    # Get agent ID
    print("\nAvailable Agents:")
    print("1. Agent-1")
    print("2. Agent-2") 
    print("3. Agent-3")
    print("4. Agent-4")
    
    agent_choice = input("Select Agent (1-4): ").strip()
    agent_map = {"1": "Agent-1", "2": "Agent-2", "3": "Agent-3", "4": "Agent-4"}
    
    if agent_choice not in agent_map:
        print("❌ Invalid agent choice")
        return None
    
    agent_id = agent_map[agent_choice]
    
    # Get quality score
    print("\nQuality Assessment:")
    print("100 = Perfect, meets all criteria")
    print("90-99 = Excellent, minor issues")
    print("80-89 = Good, some issues")
    print("70-79 = Acceptable, several issues")
    print("Below 70 = Needs improvement")
    
    try:
        quality_score = float(input("Enter Quality Score (0-100): ").strip())
        if not (0 <= quality_score <= 100):
            print("❌ Quality score must be between 0 and 100")
            return None
    except ValueError:
        print("❌ Invalid quality score")
        return None
    
    # Get actual effort
    print("\nEffort Tracking:")
    print("Examples: '2 hours', '1.5 hours', '45 minutes'")
    actual_effort = input("Enter Actual Effort: ").strip()
    
    # Get notes
    notes = input("Enter any notes or comments (optional): ").strip()
    
    return {
        "contract_id": contract_id,
        "agent_id": agent_id,
        "quality_score": quality_score,
        "actual_effort": actual_effort,
        "notes": notes
    }

def mark_contract_completed(completion_data):
    """Mark contract as completed using the Captain instruction service"""
    try:
        # Import the captain instruction service
        sys.path.append(str(Path(__file__).resolve().parents[1] / "src" / "services"))
        
        from captain_contract_instruction_service import CaptainContractInstructionService
        
        # Initialize service
        service = CaptainContractInstructionService()
        
        # Mark contract as completed
        success = service.process_contract_completion(
            completion_data["contract_id"],
            completion_data["agent_id"],
            completion_data["quality_score"],
            completion_data["actual_effort"],
            completion_data["notes"]
        )
        
        if success:
            print(f"\n✅ CONTRACT {completion_data['contract_id']} MARKED AS COMPLETED!")
            print(f"🎯 Agent: {completion_data['agent_id']}")
            print(f"⭐ Quality Score: {completion_data['quality_score']}/100")
            print(f"⏱️ Actual Effort: {completion_data['actual_effort']}")
            
            print(f"\n🚀 CAPTAIN INSTRUCTION CREATED!")
            print(f"📋 Captain-5 has been instructed to create new contracts for you!")
            print(f"📬 Check Captain-5's inbox for contract creation instructions")
            
            # Show completion summary
            summary = service.get_completion_summary()
            print(f"\n📊 TEAM PROGRESS: {summary.get('completion_rate', '0%')}")
            print(f"🎯 Target: 50 contracts = Automatic Election Trigger!")
            
            return True
        else:
            print(f"\n❌ Failed to mark contract {completion_data['contract_id']} as completed")
            return False
            
    except ImportError as e:
        print(f"❌ Error importing captain instruction service: {e}")
        print("Make sure the service is properly installed")
        return False
    except Exception as e:
        print(f"❌ Error marking contract completed: {e}")
        return False

def main():
    """Main function"""
    print("🎖️ AGENT CELLPHONE V2 - CONTRACT COMPLETION SYSTEM")
    print("=" * 60)
    print("This system instructs Captain-5 to create new contracts when you complete work!")
    print("Creating a perpetual motion system where the Captain creates contracts for you!")
    print("=" * 60)
    
    # Get completion details
    completion_data = get_contract_completion_details()
    if not completion_data:
        print("\n❌ Contract completion cancelled")
        return
    
    # Confirm completion
    print(f"\n📋 CONFIRMATION:")
    print(f"Contract ID: {completion_data['contract_id']}")
    print(f"Agent: {completion_data['agent_id']}")
    print(f"Quality Score: {completion_data['quality_score']}/100")
    print(f"Actual Effort: {completion_data['actual_effort']}")
    
    confirm = input("\nConfirm completion? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Contract completion cancelled")
        return
    
    # Mark as completed
    print("\n🔄 Processing contract completion...")
    success = mark_contract_completed(completion_data)
    
    if success:
        print("\n🎉 CONTRACT COMPLETION PROCESSED SUCCESSFULLY!")
        print("📱 Captain-5 has been instructed to create new contracts for you!")
        print("💪 Keep the momentum going!")
        print("\n📬 Next Steps:")
        print("1. Captain-5 will review the instruction")
        print("2. New contracts will be created based on your performance")
        print("3. You'll receive new assignments automatically!")
    else:
        print("\n❌ Contract completion failed. Please try again or contact support.")

if __name__ == "__main__":
    main()
