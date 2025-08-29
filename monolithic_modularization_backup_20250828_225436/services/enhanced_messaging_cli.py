"""
Enhanced Messaging CLI with FSM Integration
Provides command-line interface for the unified messaging service
Enables automated contract workflow management
"""

import argparse
import json
import sys
import asyncio
from typing import Dict, Any
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.services.unified_messaging_service import get_unified_messaging, unified_messaging
    from src.core.fsm_contract_integration import get_fsm_integration, fsm_integration
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure the FSM integration and unified messaging services are available")
    sys.exit(1)

def print_banner():
    """Print CLI banner"""
    print("🚀 Enhanced Messaging CLI with FSM Integration")
    print("=" * 60)
    print("🔗 Unified FSM-Contract-Messaging System")
    print("🔄 Perpetual Motion Workflow Engine")
    print("=" * 60)

def print_json(data: Dict[str, Any], indent: int = 2):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=indent))

def handle_get_next_task(args):
    """Handle get-next-task command"""
    service = unified_messaging
    
    print(f"🔍 Getting next task for {args.agent}...")
    result = service.get_next_task(args.agent)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return 1
    
    print("✅ Next task retrieved successfully!")
    print_json(result)
    
    if result.get("status") == "task_found":
        print(f"\n📋 To claim this contract, run:")
        print(f"   {result['claim_command']}")
    
    return 0

def handle_claim_contract(args):
    """Handle claim-contract command"""
    service = unified_messaging
    
    print(f"📋 Claiming contract {args.contract_id} for {args.agent}...")
    result = service.claim_contract(args.agent, args.contract_id)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return 1
    
    print("✅ Contract claimed successfully!")
    print_json(result)
    
    if result.get("status") == "contract_claimed":
        print(f"\n🚀 To start work, run:")
        print(f"   python -m src.services.enhanced_messaging_cli --agent {args.agent} --start-work")
    
    return 0

def handle_start_work(args):
    """Handle start-work command"""
    service = unified_messaging
    
    print(f"🚀 Starting work for {args.agent}...")
    result = service.start_contract_work(args.agent)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return 1
    
    print("✅ Work started successfully!")
    print_json(result)
    
    if result.get("status") == "work_started":
        print(f"\n✅ To complete contract, run:")
        print(f"   python -m src.services.enhanced_messaging_cli --agent {args.agent} --complete-contract")
    
    return 0

def handle_complete_contract(args):
    """Handle complete-contract command"""
    service = unified_messaging
    
    print(f"✅ Completing contract for {args.agent}...")
    result = service.complete_contract(args.agent)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return 1
    
    print("🎉 Contract completed successfully!")
    print_json(result)
    
    if result.get("status") == "contract_completed":
        print(f"\n🏆 Contract completed! Earned {result.get('extra_credit_earned', 0)} extra credit points!")
        print(f"📊 Total extra credit: {result.get('total_extra_credit', 0)}")
        print(f"📈 Contracts completed: {result.get('contracts_completed', 0)}")
    
    return 0

def handle_contract_status(args):
    """Handle contract-status command"""
    service = unified_messaging
    
    print("📊 Getting contract system status...")
    result = service.get_contract_status()
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return 1
    
    print("✅ Contract status retrieved successfully!")
    print_json(result)
    
    # Print summary
    if "contract_system_status" in result:
        status = result["contract_system_status"]
        print(f"\n📈 System Summary:")
        print(f"   Total Agents: {status.get('total_agents', 0)}")
        print(f"   Active Contracts: {status.get('active_contracts', 0)}")
        print(f"   Available Contracts: {status.get('available_contracts', 0)}")
        print(f"   Completed Contracts: {status.get('completed_contracts', 0)}")
        print(f"   Total Extra Credit Earned: {status.get('total_extra_credit_earned', 0)}")
        print(f"   Workflow Status: {status.get('workflow_status', 'unknown')}")
    
    return 0

def handle_agent_status(args):
    """Handle agent-status command"""
    service = unified_messaging
    
    print(f"👤 Getting workflow status for {args.agent}...")
    result = service.get_agent_workflow_status(args.agent)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return 1
    
    print("✅ Agent status retrieved successfully!")
    print_json(result)
    
    # Print agent summary
    if result.get("status") == "success":
        print(f"\n👤 Agent Summary:")
        print(f"   Role: {result.get('role', 'Unknown')}")
        print(f"   FSM State: {result.get('fsm_state', 'Unknown')}")
        print(f"   Current Contract: {result.get('current_contract', {}).get('id', 'None')}")
        print(f"   Contracts Completed: {result.get('contracts_completed', 0)}")
        print(f"   Extra Credit Earned: {result.get('extra_credit_earned', 0)}")
        print(f"   Last Activity: {result.get('last_activity', 'Unknown')}")
        
        next_actions = result.get('next_actions', [])
        if next_actions:
            print(f"   Next Actions: {', '.join(next_actions)}")
    
    return 0

def handle_start_auto_workflow(args):
    """Handle start-auto-workflow command"""
    service = unified_messaging
    
    print("🚀 Starting automated workflow...")
    result = service.start_auto_workflow()
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return 1
    
    print("✅ Automated workflow started successfully!")
    print_json(result)
    
    if result.get("status") == "workflow_started":
        print(f"\n🔄 Perpetual Motion Engine Activated!")
        print(f"   Agents will now work continuously and automatically")
        print(f"   To stop the workflow, run:")
        print(f"   python -m src.services.enhanced_messaging_cli --stop-auto-workflow")
    
    return 0

def handle_stop_auto_workflow(args):
    """Handle stop-auto-workflow command"""
    service = unified_messaging
    
    print("🛑 Stopping automated workflow...")
    result = service.stop_auto_workflow()
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return 1
    
    print("✅ Automated workflow stopped successfully!")
    print_json(result)
    
    return 0

def handle_messaging_history(args):
    """Handle messaging-history command"""
    service = unified_messaging
    
    limit = args.limit if hasattr(args, 'limit') else 50
    print(f"📜 Getting messaging history (last {limit} actions)...")
    
    history = service.get_messaging_history(limit)
    
    if not history:
        print("📜 No messaging history available")
        return 0
    
    print(f"✅ Retrieved {len(history)} messaging actions:")
    print_json(history)
    
    return 0

def handle_fsm_status(args):
    """Handle fsm-status command"""
    fsm = fsm_integration
    
    if not fsm:
        print("❌ FSM integration not available")
        return 1
    
    print("🔧 Getting FSM integration status...")
    
    # Get agent status summary
    summary = fsm.get_agent_status_summary()
    
    print("✅ FSM Integration Status:")
    print_json(summary)
    
    # Print FSM details
    print(f"\n🔧 FSM Details:")
    print(f"   Workflow Running: {fsm.workflow_running}")
    print(f"   Continuous Cycle Active: {fsm.continuous_cycle_active}")
    print(f"   Total Agents: {len(fsm.agents)}")
    print(f"   Total Contracts: {len(fsm.contracts)}")
    
    return 0

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Enhanced Messaging CLI with FSM Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get next task for Agent-7
  python -m src.services.enhanced_messaging_cli --agent Agent-7 --get-next-task
  
  # Claim contract COORD-004 for Agent-7
  python -m src.services.enhanced_messaging_cli --agent Agent-7 --claim-contract COORD-004
  
  # Start work for Agent-7
  python -m src.services.enhanced_messaging_cli --agent Agent-7 --start-work
  
  # Complete contract for Agent-7
  python -m src.services.enhanced_messaging_cli --agent Agent-7 --complete-contract
  
  # Get contract status
  python -m src.services.enhanced_messaging_cli --contract-status
  
  # Start automated workflow
  python -m src.services.enhanced_messaging_cli --start-auto-workflow
  
  # Get FSM status
  python -m src.services.enhanced_messaging_cli --fsm-status
        """
    )
    
    # Agent argument (required for most commands)
    parser.add_argument("--agent", "-a", help="Agent ID (e.g., Agent-7)")
    
    # Contract argument
    parser.add_argument("--contract-id", "-c", dest="contract_id", help="Contract ID (e.g., COORD-004)")
    
    # Command flags
    parser.add_argument("--get-next-task", action="store_true", help="Get next available task for agent")
    parser.add_argument("--claim-contract", action="store_true", help="Claim specific contract for agent")
    parser.add_argument("--start-work", action="store_true", help="Start work on claimed contract")
    parser.add_argument("--complete-contract", action="store_true", help="Complete current contract")
    parser.add_argument("--contract-status", action="store_true", help="Get overall contract system status")
    parser.add_argument("--agent-status", action="store_true", help="Get workflow status for specific agent")
    parser.add_argument("--start-auto-workflow", action="store_true", help="Start automated workflow for all agents")
    parser.add_argument("--stop-auto-workflow", action="store_true", help="Stop automated workflow")
    parser.add_argument("--messaging-history", action="store_true", help="Get messaging action history")
    parser.add_argument("--fsm-status", action="store_true", help="Get FSM integration status")
    
    # Optional arguments
    parser.add_argument("--limit", "-l", type=int, default=50, help="Limit for history commands (default: 50)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Validate arguments
    if not any([
        args.get_next_task, args.claim_contract, args.start_work, args.complete_contract,
        args.contract_status, args.agent_status, args.start_auto_workflow, 
        args.stop_auto_workflow, args.messaging_history, args.fsm_status
    ]):
        print("❌ No command specified. Use --help for usage information.")
        return 1
    
    # Validate agent requirement
    agent_required_commands = [
        args.get_next_task, args.claim_contract, args.start_work, args.complete_contract, args.agent_status
    ]
    
    if any(agent_required_commands) and not args.agent:
        print("❌ Agent ID required for this command. Use --agent AGENT-ID")
        return 1
    
    # Validate contract requirement
    if args.claim_contract and not args.contract_id:
        print("❌ Contract ID required for claiming. Use --contract-id CONTRACT-ID")
        return 1
    
    # Execute commands
    try:
        if args.get_next_task:
            return handle_get_next_task(args)
        elif args.claim_contract:
            return handle_claim_contract(args)
        elif args.start_work:
            return handle_start_work(args)
        elif args.complete_contract:
            return handle_complete_contract(args)
        elif args.contract_status:
            return handle_contract_status(args)
        elif args.agent_status:
            return handle_agent_status(args)
        elif args.start_auto_workflow:
            return handle_start_auto_workflow(args)
        elif args.stop_auto_workflow:
            return handle_stop_auto_workflow(args)
        elif args.messaging_history:
            return handle_messaging_history(args)
        elif args.fsm_status:
            return handle_fsm_status(args)
        else:
            print("❌ Unknown command")
            return 1
            
    except KeyboardInterrupt:
        print("\n🛑 Operation interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
