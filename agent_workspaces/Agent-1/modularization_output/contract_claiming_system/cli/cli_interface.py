#!/usr/bin/env python3
"""
Command-line interface for the modularized contract claiming system.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from contract_claiming_system.core.contract_manager import ContractManager
from contract_claiming_system.operations.contract_lister import ContractLister


class ContractClaimingCLI:
    """Command-line interface for the contract claiming system."""
    
    def __init__(self, task_list_path: str = "agent_workspaces/meeting/task_list.json"):
        self.contract_manager = ContractManager(task_list_path)
        self.contract_lister = ContractLister(self.contract_manager)
    
    def list_contracts(self, category: Optional[str] = None, show_details: bool = False) -> None:
        """List available contracts."""
        if category:
            contracts = self.contract_lister.list_available_contracts(category)
            print(f"🚀 CONTRACT CLAIMING SYSTEM - Available Contracts ({category})")
        else:
            contracts = self.contract_lister.list_available_contracts()
            print("🚀 CONTRACT CLAIMING SYSTEM - Available Contracts")
        
        print("=" * 60)
        
        if contracts:
            print(f"✅ Found {len(contracts)} available contracts:")
            formatted_output = self.contract_lister.format_contract_list(contracts, show_details)
            print(formatted_output)
        else:
            print("❌ No available contracts found.")
    
    def claim_contract(self, contract_id: str, agent_id: str) -> None:
        """Claim a contract for an agent."""
        print(f"🎯 CLAIMING CONTRACT: {contract_id}")
        print(f"👤 AGENT: {agent_id}")
        print("=" * 40)
        
        result = self.contract_manager.claim_contract(contract_id, agent_id)
        
        if result["success"]:
            print("✅ SUCCESS!")
            print(f"📝 {result['message']}")
            contract = result["contract"]
            print(f"📋 Contract: {contract['title']}")
            print(f"🏷️  Category: {contract['category']}")
            print(f"⭐ Points: {contract['points']}")
        else:
            print("❌ FAILED!")
            print(f"💥 Error: {result['error']}")
    
    def update_progress(self, contract_id: str, agent_id: str, progress: str) -> None:
        """Update contract progress."""
        print(f"📊 UPDATING PROGRESS: {contract_id}")
        print(f"👤 AGENT: {agent_id}")
        print(f"📈 PROGRESS: {progress}")
        print("=" * 40)
        
        result = self.contract_manager.update_contract_progress(contract_id, agent_id, progress)
        
        if result["success"]:
            print("✅ SUCCESS!")
            print(f"📝 {result['message']}")
        else:
            print("❌ FAILED!")
            print(f"💥 Error: {result['error']}")
    
    def complete_contract(self, contract_id: str, agent_id: str, deliverables: str) -> None:
        """Complete a contract with deliverables."""
        print(f"🎉 COMPLETING CONTRACT: {contract_id}")
        print(f"👤 AGENT: {agent_id}")
        print(f"📦 DELIVERABLES: {deliverables}")
        print("=" * 40)
        
        result = self.contract_manager.complete_contract(contract_id, agent_id, deliverables)
        
        if result["success"]:
            print("✅ SUCCESS!")
            print(f"📝 {result['message']}")
            contract = result["contract"]
            print(f"📋 Contract: {contract['title']}")
            print(f"🏁 Status: {contract['status']}")
        else:
            print("❌ FAILED!")
            print(f"💥 Error: {result['error']}")
    
    def show_status(self, contract_id: str) -> None:
        """Show status of a specific contract."""
        print(f"📋 CONTRACT STATUS: {contract_id}")
        print("=" * 40)
        
        result = self.contract_manager.find_contract(contract_id)
        
        if result:
            contract, contract_type, index = result
            print(f"📝 Title: {contract.title}")
            print(f"🏷️  Category: {contract.category}")
            print(f"⭐ Points: {contract.points}")
            print(f"📊 Status: {contract.status}")
            print(f"👤 Agent: {contract.agent_id or 'Unclaimed'}")
            print(f"📈 Progress: {contract.progress}")
            print(f"📦 Deliverables: {', '.join(contract.deliverables) if contract.deliverables else 'None'}")
        else:
            print("❌ Contract not found.")
    
    def show_statistics(self) -> None:
        """Show contract statistics."""
        print("📊 CONTRACT STATISTICS")
        print("=" * 40)
        
        stats = self.contract_manager.get_contract_statistics()
        
        print(f"📋 Total Contracts: {stats['total_contracts']}")
        print(f"✅ Available: {stats['available_contracts']}")
        print(f"🎯 Claimed: {stats['claimed_contracts']}")
        print(f"🎉 Completed: {stats['completed_contracts']}")
        print(f"📈 Completion Rate: {stats['completion_rate']:.1f}%")
        
        # Show summary by category
        print("\n📊 BY CATEGORY:")
        summary = self.contract_lister.get_contract_summary()
        for category, status_counts in summary.items():
            print(f"  {category}:")
            for status, count in status_counts.items():
                print(f"    {status}: {count}")
    
    def run(self) -> None:
        """Run the CLI interface."""
        parser = argparse.ArgumentParser(
            description="Modularized Contract Claiming System CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # List all available contracts
  python cli_interface.py --list

  # List contracts by category
  python cli_interface.py --list --category Modularization

  # Claim a contract
  python cli_interface.py --claim MODULAR-001 --agent Agent-1

  # Update progress
  python cli_interface.py --update-progress MODULAR-001 --agent Agent-1 --progress "50%"

  # Complete a contract
  python cli_interface.py --complete MODULAR-001 --agent Agent-1 --deliverables "Report, Code, Tests"

  # Check contract status
  python cli_interface.py --status MODULAR-001

  # Show statistics
  python cli_interface.py --stats
            """
        )
        
        parser.add_argument("--list", action="store_true", help="List available contracts")
        parser.add_argument("--claim", help="Claim a contract by ID")
        parser.add_argument("--update-progress", help="Update progress for a contract by ID")
        parser.add_argument("--complete", help="Complete a contract by ID")
        parser.add_argument("--status", help="Check status of a specific contract")
        parser.add_argument("--stats", action="store_true", help="Show contract statistics")
        
        parser.add_argument("--agent", help="Agent ID (required for claim, update-progress, complete)")
        parser.add_argument("--category", help="Filter contracts by category")
        parser.add_argument("--progress", help="Progress update text")
        parser.add_argument("--deliverables", help="Comma-separated list of deliverables")
        parser.add_argument("--task-list", default="agent_workspaces/meeting/task_list.json", 
                          help="Path to task list file")
        
        args = parser.parse_args()
        
        # Update task list path if specified
        if args.task_list != "agent_workspaces/meeting/task_list.json":
            self.contract_manager = ContractManager(args.task_list)
            self.contract_lister = ContractLister(self.contract_manager)
        
        # Execute commands
        if args.list:
            self.list_contracts(args.category, show_details=False)
        elif args.claim:
            if not args.agent:
                print("❌ Error: --agent is required for claiming contracts")
                sys.exit(1)
            self.claim_contract(args.claim, args.agent)
        elif args.update_progress:
            if not args.agent:
                print("❌ Error: --agent is required for updating progress")
                sys.exit(1)
            if not args.progress:
                print("❌ Error: --progress is required for updating progress")
                sys.exit(1)
            self.update_progress(args.update_progress, args.agent, args.progress)
        elif args.complete:
            if not args.agent:
                print("❌ Error: --agent is required for completing contracts")
                sys.exit(1)
            if not args.deliverables:
                print("❌ Error: --deliverables is required for completing contracts")
                sys.exit(1)
            self.complete_contract(args.complete, args.agent, args.deliverables)
        elif args.status:
            self.show_status(args.status)
        elif args.stats:
            self.show_statistics()
        else:
            parser.print_help()


def main():
    """Main entry point."""
    cli = ContractClaimingCLI()
    cli.run()


if __name__ == "__main__":
    main()
