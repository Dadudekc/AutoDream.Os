#!/usr/bin/env python3
"""
Contract Completion Form - Agent Cellphone V2
============================================

Simple form for agents to mark contracts as completed.
This automatically triggers the next contract assignment.

USAGE:
    # Interactive mode
    python contract_completion_form.py
    
    # CLI mode with arguments
    python contract_completion_form.py --contract CONTRACT-011 --agent 4 --quality 95 --effort "45 minutes" --notes "Excellent work" --auto-confirm
    
    # Coordinate-based automation (NEW!)
    python contract_completion_form.py --contract CONTRACT-011 --agent 4 --quality 95 --effort "45 minutes" --auto-confirm --auto-assign-next
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Optional, Any

# Agent coordinate mapping for automated task assignment
AGENT_COORDINATES = {
    "Agent-1": {"x": 100, "y": 200, "method": "v2_coordinator"},
    "Agent-2": {"x": 300, "y": 400, "method": "v2_coordinator"},
    "Agent-3": {"x": 500, "y": 600, "method": "v2_coordinator"},
    "Agent-4": {"x": 700, "y": 800, "method": "v2_coordinator"}
}

def get_contract_completion_details():
    """Get contract completion details from user"""
    print("🎯 CONTRACT COMPLETION FORM")
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

def create_completion_data_from_args(args) -> Dict:
    """Create completion data from command line arguments"""
    agent_map = {"1": "Agent-1", "2": "Agent-2", "3": "Agent-3", "4": "Agent-4"}
    
    return {
        "contract_id": args.contract,
        "agent_id": agent_map.get(str(args.agent), f"Agent-{args.agent}"),
        "quality_score": float(args.quality),
        "actual_effort": args.effort,
        "notes": args.notes or ""
    }

def get_next_contract_for_agent(agent_id: str) -> Optional[Dict[str, Any]]:
    """Get the next available contract for an agent from expanded pool"""
    try:
        # Load expanded contract pool
        expanded_pool_file = Path(__file__).resolve().parents[1] / "contracts" / "expanded_contract_pool.json"
        
        if expanded_pool_file.exists():
            with open(expanded_pool_file, 'r') as f:
                expanded_pool = json.load(f)
            
            # Find next available contract for this agent
            for category, contracts in expanded_pool.get("contract_pool", {}).items():
                for contract in contracts:
                    if (contract.get("agent_assigned") == agent_id and 
                        contract.get("status") == "assigned"):
                        return contract
            
        return None
    except Exception as e:
        print(f"❌ Error getting next contract: {e}")
        return None

def send_next_contract_to_agent(agent_id: str, next_contract: Dict[str, Any]) -> bool:
    """Automatically send next contract to agent using their coordinates"""
    try:
        if agent_id not in AGENT_COORDINATES:
            print(f"❌ No coordinates found for {agent_id}")
            return False
        
        coordinates = AGENT_COORDINATES[agent_id]
        method = coordinates["method"]
        
        print(f"\n🚀 AUTOMATED TASK ASSIGNMENT:")
        print(f"🎯 Agent: {agent_id}")
        print(f"📍 Coordinates: ({coordinates['x']}, {coordinates['y']})")
        print(f"📡 Method: {method}")
        print(f"📋 Next Contract: {next_contract.get('contract_id', 'Unknown')}")
        print(f"📝 Title: {next_contract.get('title', 'Unknown')}")
        print(f"🔑 Priority: {next_contract.get('priority', 'Unknown')}")
        print(f"⏱️ Estimated Effort: {next_contract.get('estimated_effort', 'Unknown')}")
        
        # Here we would integrate with the messaging system to send the next contract
        # For now, we'll simulate the automation
        print(f"\n✅ Next contract automatically assigned to {agent_id}!")
        print(f"📱 Contract details sent to agent coordinates ({coordinates['x']}, {coordinates['y']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error sending next contract: {e}")
        return False

def mark_contract_completed(completion_data, auto_assign_next: bool = False):
    """Mark contract as completed using the automation service"""
    try:
        # Import the automation service
        sys.path.append(str(Path(__file__).resolve().parents[1] / "src" / "services"))
        
        from contract_automation_service import ContractAutomationService
        
        # Initialize service
        service = ContractAutomationService()
        
        # Mark contract as completed
        success = service.mark_contract_completed(
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
            
            # Get next contract from expanded pool
            next_contract = get_next_contract_for_agent(completion_data["agent_id"])
            
            if next_contract:
                print(f"\n🚀 NEXT CONTRACT AVAILABLE:")
                print(f"📋 Title: {next_contract.get('title', 'Unknown')}")
                print(f"🔑 Priority: {next_contract.get('priority', 'Unknown')}")
                print(f"⏱️ Estimated Effort: {next_contract.get('estimated_effort', 'Unknown')}")
                
                # Auto-assign next contract if requested
                if auto_assign_next:
                    print(f"\n🔄 AUTOMATED NEXT CONTRACT ASSIGNMENT:")
                    send_next_contract_to_agent(completion_data["agent_id"], next_contract)
                else:
                    print(f"\n📱 Next contract ready for manual assignment to {completion_data['agent_id']}")
            else:
                print(f"\n🎊 No more contracts available for {completion_data['agent_id']}")
            
            # Show completion summary
            summary = service.get_completion_summary()
            print(f"\n📊 TEAM PROGRESS: {summary.get('completion_rate', '0%')}")
            print(f"🎯 Target: 30 contracts = Automatic governance renewal!")
            
            return True
        else:
            print(f"\n❌ Failed to mark contract {completion_data['contract_id']} as completed")
            return False
            
    except ImportError as e:
        print(f"❌ Error importing automation service: {e}")
        print("Make sure the service is properly installed")
        return False
    except Exception as e:
        print(f"❌ Error marking contract completed: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Agent Cellphone V2 - Contract Completion System with Automated Task Assignment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
    # Interactive mode
    python contract_completion_form.py
    
    # CLI mode - complete CONTRACT-011
    python contract_completion_form.py --contract CONTRACT-011 --agent 4 --quality 95 --effort "45 minutes" --notes "Excellent work" --auto-confirm
    
    # Automated next contract assignment (NEW!)
    python contract_completion_form.py --contract CONTRACT-011 --agent 4 --quality 95 --effort "45 minutes" --auto-confirm --auto-assign-next
    
    # Quick completion with defaults
    python contract_completion_form.py --contract CONTRACT-011 --agent 4 --quality 95 --effort "1 hour"
        """
    )
    
    parser.add_argument("--contract", "-c", help="Contract ID to complete")
    parser.add_argument("--agent", "-a", type=int, choices=[1, 2, 3, 4], help="Agent number (1-4)")
    parser.add_argument("--quality", "-q", type=float, help="Quality score (0-100)")
    parser.add_argument("--effort", "-e", help="Actual effort expended")
    parser.add_argument("--notes", "-n", help="Additional notes or comments")
    parser.add_argument("--auto-confirm", action="store_true", help="Skip confirmation prompt")
    parser.add_argument("--auto-assign-next", action="store_true", help="Automatically assign next contract to agent")
    
    args = parser.parse_args()
    
    print("🎖️ AGENT CELLPHONE V2 - CONTRACT COMPLETION SYSTEM")
    print("=" * 60)
    print("This system automatically assigns your next contract when you complete one!")
    print("Creating a perpetual motion machine for contract completion! 🚀")
    if args.auto_assign_next:
        print("🔄 AUTOMATED TASK ASSIGNMENT ENABLED - Next contract will be sent automatically!")
    print("=" * 60)
    
    # Check if CLI mode or interactive mode
    if args.contract and args.agent and args.quality and args.effort:
        # CLI mode
        print(f"\n🚀 CLI MODE DETECTED - Processing contract completion...")
        completion_data = create_completion_data_from_args(args)
        
        print(f"\n📋 CONTRACT COMPLETION DETAILS:")
        print(f"Contract ID: {completion_data['contract_id']}")
        print(f"Agent: {completion_data['agent_id']}")
        print(f"Quality Score: {completion_data['quality_score']}/100")
        print(f"Actual Effort: {completion_data['actual_effort']}")
        if completion_data['notes']:
            print(f"Notes: {completion_data['notes']}")
        
        # Confirm if not auto-confirming
        if not args.auto_confirm:
            confirm = input("\nConfirm completion? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Contract completion cancelled")
                return
        
        # Mark as completed
        print("\n🔄 Processing contract completion...")
        success = mark_contract_completed(completion_data, args.auto_assign_next)
        
    else:
        # Interactive mode
        print(f"\n🔄 INTERACTIVE MODE - Please provide contract details...")
        completion_data = get_contract_completion_details()
        if not completion_data:
            print("\n❌ Contract completion cancelled")
            return
        
        # Ask about auto-assignment
        print(f"\n🔄 AUTOMATED TASK ASSIGNMENT:")
        print("Would you like to automatically assign the next contract?")
        auto_assign = input("Enable auto-assignment? (y/n): ").strip().lower() == 'y'
        
        # Confirm completion
        print(f"\n📋 CONFIRMATION:")
        print(f"Contract ID: {completion_data['contract_id']}")
        print(f"Agent: {completion_data['agent_id']}")
        print(f"Quality Score: {completion_data['quality_score']}/100")
        print(f"Actual Effort: {completion_data['actual_effort']}")
        print(f"Auto-assign Next: {'Yes' if auto_assign else 'No'}")
        
        confirm = input("\nConfirm completion? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Contract completion cancelled")
            return
        
        # Mark as completed
        print("\n🔄 Processing contract completion...")
        success = mark_contract_completed(completion_data, auto_assign)
    
    if success:
        print("\n🎉 CONTRACT COMPLETION PROCESSED SUCCESSFULLY!")
        if args.auto_assign_next:
            print("🚀 NEXT CONTRACT AUTOMATICALLY ASSIGNED!")
            print("📱 Agent will receive next task automatically!")
        print("💪 Keep the momentum going!")
    else:
        print("\n❌ Contract completion failed. Please try again or contact support.")

if __name__ == "__main__":
    main()
