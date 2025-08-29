#!/usr/bin/env python3
"""
Contract Claiming System - Emergency Restoration Component
Implements contract claiming, management, and validation for Agent-6
Emergency Restoration Mission EMERGENCY-RESTORE-008
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pathlib import Path

class ContractClaimingSystem:
    """Emergency Contract Claiming System for System Synchronization"""
    
    def __init__(self, task_list_path: str):
        self.task_list_path = Path(task_list_path)
        self.contracts = self._load_contracts()
        
    def _load_contracts(self) -> Dict[str, Any]:
        """Load contracts from task list"""
        try:
            if self.task_list_path.exists():
                with open(self.task_list_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"❌ Task list not found: {self.task_list_path}")
                return {}
        except Exception as e:
            print(f"❌ Error loading contracts: {e}")
            return {}
    
    def _save_contracts(self) -> bool:
        """Save contracts to task list"""
        try:
            with open(self.task_list_path, 'w', encoding='utf-8') as f:
                json.dump(self.contracts, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving contracts: {e}")
            return False
    
    def list_available_contracts(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all available contracts, optionally filtered by category"""
        available = []
        seen_contracts = {}  # Track contracts by ID to detect duplicates
        
        # The contracts are nested under the "contracts" key
        contracts_section = self.contracts.get("contracts", {})
        
        for contract_type, contract_data in contracts_section.items():
            if isinstance(contract_data, dict) and 'contracts' in contract_data:
                # Handle structure: {category, manager, contracts: [list]}
                contracts_list = contract_data.get('contracts', [])
                if isinstance(contracts_list, list):
                    for contract in contracts_list:
                        if isinstance(contract, dict):
                            contract_id = contract.get('contract_id', '')
                            if contract_id:
                                # Check if we've seen this contract before
                                if contract_id in seen_contracts:
                                    # Resolve duplicate: prefer completed status over available
                                    existing_status = seen_contracts[contract_id].get('status', '')
                                    current_status = contract.get('status', '')
                                    
                                    if existing_status == 'COMPLETED' or current_status == 'COMPLETED':
                                        # Mark as completed in our tracking
                                        seen_contracts[contract_id]['status'] = 'COMPLETED'
                                        # Remove from available if it was there
                                        if seen_contracts[contract_id] in available:
                                            available.remove(seen_contracts[contract_id])
                                    elif existing_status == 'CLAIMED' or current_status == 'CLAIMED':
                                        # Mark as claimed in our tracking
                                        seen_contracts[contract_id]['status'] = 'CLAIMED'
                                        # Remove from available if it was there
                                        if seen_contracts[contract_id] in available:
                                            available.remove(seen_contracts[contract_id])
                                    else:
                                        # Both are available, keep the first one
                                        continue
                                else:
                                    # First time seeing this contract
                                    seen_contracts[contract_id] = contract
                                    
                                    # Check if contract is truly available (not completed)
                                    status = contract.get('status', '')
                                    if status == 'AVAILABLE' and not contract.get('completed_at'):
                                        if category is None or contract.get('category') == category:
                                            available.append(contract)
            elif isinstance(contract_data, list):
                # Handle direct list structure (fallback)
                for contract in contract_data:
                    if isinstance(contract, dict):
                        contract_id = contract.get('contract_id', '')
                        if contract_id:
                            # Check if we've seen this contract before
                            if contract_id in seen_contracts:
                                # Resolve duplicate: prefer completed status over available
                                existing_status = seen_contracts[contract_id].get('status', '')
                                current_status = contract.get('status', '')
                                
                                if existing_status == 'COMPLETED' or current_status == 'COMPLETED':
                                    # Mark as completed in our tracking
                                    seen_contracts[contract_id]['status'] = 'COMPLETED'
                                    # Remove from available if it was there
                                    if seen_contracts[contract_id] in available:
                                        available.remove(seen_contracts[contract_id])
                                elif existing_status == 'CLAIMED' or current_status == 'CLAIMED':
                                    # Mark as claimed in our tracking
                                    seen_contracts[contract_id]['status'] = 'CLAIMED'
                                    # Remove from available if it was there
                                    if seen_contracts[contract_id] in available:
                                        available.remove(seen_contracts[contract_id])
                                else:
                                    # Both are available, keep the first one
                                    continue
                            else:
                                # First time seeing this contract
                                seen_contracts[contract_id] = contract
                                
                                # Check if contract is truly available (not completed)
                                status = contract.get('status', '')
                                if status == 'AVAILABLE' and not contract.get('completed_at'):
                                    if category is None or contract.get('category') == category:
                                        available.append(contract)
        
        return available
    
    def claim_contract(self, contract_id: str, agent_id: str) -> Dict[str, Any]:
        """Claim a contract for an agent"""
        try:
            # Find the contract
            contract = None
            contract_location = None
            
            contracts_section = self.contracts.get("contracts", {})
            for contract_type, contract_data in contracts_section.items():
                if isinstance(contract_data, dict) and 'contracts' in contract_data:
                    # Handle structure: {category, manager, contracts: [list]}
                    contracts_list = contract_data.get('contracts', [])
                    if isinstance(contracts_list, list):
                        for i, c in enumerate(contracts_list):
                            if isinstance(c, dict) and c.get('contract_id') == contract_id:
                                contract = c
                                contract_location = (contract_type, i)
                                break
                        if contract:
                            break
                elif isinstance(contract_data, list):
                    # Handle direct list structure (fallback)
                    for i, c in enumerate(contract_data):
                        if isinstance(c, dict) and c.get('contract_id') == contract_id:
                            contract = c
                            contract_location = (contract_type, i)
                            break
                    if contract:
                        break
            
            if not contract:
                return {
                    "success": False,
                    "message": f"Contract {contract_id} not found"
                }
            
            if contract.get('status') != 'AVAILABLE':
                return {
                    "success": False,
                    "message": f"Contract {contract_id} is not available (status: {contract.get('status')})"
                }
            
            # Update contract status
            contract['status'] = 'CLAIMED'
            contract['claimed_by'] = agent_id
            contract['claimed_at'] = datetime.now(timezone.utc).isoformat()
            contract['progress'] = '0% Complete - In Progress'
            
            # Save changes
            if self._save_contracts():
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
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error claiming contract: {e}"
            }
    
    def update_contract_progress(self, contract_id: str, agent_id: str, progress: str) -> Dict[str, Any]:
        """Update contract progress"""
        try:
            # Find the contract
            contract = None
            
            contracts_section = self.contracts.get("contracts", {})
            for contract_type, contract_data in contracts_section.items():
                if isinstance(contract_data, dict) and 'contracts' in contract_data:
                    # Handle structure: {category, manager, contracts: [list]}
                    contracts_list = contract_data.get('contracts', [])
                    if isinstance(contracts_list, list):
                        for c in contracts_list:
                            if isinstance(c, dict) and c.get('contract_id') == contract_id:
                                contract = c
                                break
                        if contract:
                            break
                elif isinstance(contract_data, list):
                    # Handle direct list structure (fallback)
                    for c in contract_data:
                        if isinstance(c, dict) and c.get('contract_id') == contract_id:
                            contract = c
                            break
                    if contract:
                        break
            
            if not contract:
                return {
                    "success": False,
                    "message": f"Contract {contract_id} not found"
                }
            
            if contract.get('claimed_by') != agent_id:
                return {
                    "success": False,
                    "message": f"Contract {contract_id} is not claimed by {agent_id}"
                }
            
            # Update progress
            contract['progress'] = progress
            contract['last_updated'] = datetime.now(timezone.utc).isoformat()
            
            # Save changes
            if self._save_contracts():
                return {
                    "success": True,
                    "message": f"Progress updated for contract {contract_id}: {progress}"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to save progress changes"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating progress: {e}"
            }
    
    def complete_contract(self, contract_id: str, agent_id: str, deliverables: List[str]) -> Dict[str, Any]:
        """Complete a contract with deliverables"""
        try:
            # Find the contract
            contract = None
            
            contracts_section = self.contracts.get("contracts", {})
            for contract_type, contract_data in contracts_section.items():
                if isinstance(contract_data, dict) and 'contracts' in contract_data:
                    # Handle structure: {category, manager, contracts: [list]}
                    contracts_list = contract_data.get('contracts', [])
                    if isinstance(contracts_list, list):
                        for c in contracts_list:
                            if isinstance(c, dict) and c.get('contract_id') == contract_id:
                                contract = c
                                break
                        if contract:
                            break
                elif isinstance(contract_data, list):
                    # Handle direct list structure (fallback)
                    for c in contract_data:
                        if isinstance(c, dict) and c.get('contract_id') == contract_id:
                            contract = c
                            break
                    if contract:
                        break
            
            if not contract:
                return {
                    "success": False,
                    "message": f"Contract {contract_id} not found"
                }
            
            if contract.get('claimed_by') != agent_id:
                return {
                    "success": False,
                    "message": f"Contract {contract_id} is not claimed by {agent_id}"
                }
            
            if contract.get('status') != 'CLAIMED':
                return {
                    "success": False,
                    "message": f"Contract {contract_id} is not in CLAIMED status"
                }
            
            # Calculate points earned
            base_points = contract.get('extra_credit_points', 0)
            progress_bonus = 0
            
            # Add progress bonus if progress is high
            progress = contract.get('progress', '0%')
            if '100%' in progress or 'complete' in progress.lower():
                progress_bonus = int(base_points * 0.1)  # 10% bonus for completion
            
            total_points = base_points + progress_bonus
            
            # Update contract status
            contract['status'] = 'COMPLETED'
            contract['completed_at'] = datetime.now(timezone.utc).isoformat()
            contract['progress'] = '100% Complete'
            contract['deliverables'] = deliverables
            contract['points_earned'] = total_points
            
            # Save changes
            if self._save_contracts():
                return {
                    "success": True,
                    "message": f"Contract {contract_id} completed successfully by {agent_id}",
                    "points_earned": total_points,
                    "deliverables": deliverables
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to save completion changes"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error completing contract: {e}"
            }
    
    def get_contract_status(self, contract_id: str) -> Dict[str, Any]:
        """Get status of a specific contract"""
        try:
            # Find the contract
            contract = None
            
            contracts_section = self.contracts.get("contracts", {})
            for contract_type, contract_data in contracts_section.items():
                if isinstance(contract_data, dict) and 'contracts' in contract_data:
                    # Handle structure: {category, manager, contracts: [list]}
                    contracts_list = contract_data.get('contracts', [])
                    if isinstance(contracts_list, list):
                        for c in contracts_list:
                            if isinstance(c, dict) and c.get('contract_id') == contract_id:
                                contract = c
                                break
                        if contract:
                            break
                elif isinstance(contract_data, list):
                    # Handle direct list structure (fallback)
                    for c in contract_data:
                        if isinstance(c, dict) and c.get('contract_id') == contract_id:
                            contract = c
                            break
                    if contract:
                        break
            
            if not contract:
                return {
                    "success": False,
                    "message": f"Contract {contract_id} not found"
                }
            
            return {
                "success": True,
                "contract": contract
            }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error getting contract status: {e}"
            }
    
    def get_contract_statistics(self) -> Dict[str, Any]:
        """Get overall contract statistics"""
        try:
            total_contracts = 0
            available_contracts = 0
            claimed_contracts = 0
            completed_contracts = 0
            total_extra_credit = 0
            
            # The contracts are nested under the "contracts" key
            contracts_section = self.contracts.get("contracts", {})
            for contract_type, contract_data in contracts_section.items():
                if isinstance(contract_data, dict) and 'contracts' in contract_data:
                    # Handle structure: {category, manager, contracts: [list]}
                    contracts_list = contract_data.get('contracts', [])
                    if isinstance(contracts_list, list):
                        for contract in contracts_list:
                            if isinstance(contract, dict):
                                total_contracts += 1
                                status = contract.get('status', 'UNKNOWN')
                                
                                if status == 'AVAILABLE':
                                    available_contracts += 1
                                elif status == 'CLAIMED':
                                    claimed_contracts += 1
                                elif status == 'COMPLETED':
                                    completed_contracts += 1
                                
                                # Add points
                                if status == 'COMPLETED':
                                    total_extra_credit += contract.get('points_earned', 0)
                                else:
                                    total_extra_credit += contract.get('extra_credit_points', 0)
                elif isinstance(contract_data, list):
                    # Handle direct list structure (fallback)
                    for contract in contract_data:
                        if isinstance(contract, dict):
                            total_contracts += 1
                            status = contract.get('status', 'UNKNOWN')
                            
                            if status == 'AVAILABLE':
                                available_contracts += 1
                            elif status == 'CLAIMED':
                                claimed_contracts += 1
                            elif status == 'COMPLETED':
                                completed_contracts += 1
                            
                            # Add points
                            if status == 'COMPLETED':
                                total_extra_credit += contract.get('points_earned', 0)
                            else:
                                total_extra_credit += contract.get('extra_credit_points', 0)
            
            return {
                "total_contracts": total_contracts,
                "available_contracts": available_contracts,
                "claimed_contracts": claimed_contracts,
                "completed_contracts": completed_contracts,
                "total_extra_credit": total_extra_credit
            }
                
        except Exception as e:
            return {
                "total_contracts": 0,
                "available_contracts": 0,
                "claimed_contracts": 0,
                "completed_contracts": 0,
                "total_extra_credit": 0
            }

def main():
    """Main command-line interface for contract claiming system"""
    parser = argparse.ArgumentParser(
        description="Contract Claiming System - Emergency Restoration Component",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all available contracts
  python contract_claiming_system.py --list
  
  # List contracts by category
  python contract_claiming_system.py --list --category SSOT_Resolution
  
  # Claim a contract
  python contract_claiming_system.py --claim SSOT-001 --agent Agent-1
  
  # Update progress
  python contract_claiming_system.py --update-progress SSOT-001 --agent Agent-1 --progress "50% Complete"
  
  # Complete a contract
  python contract_claiming_system.py --complete SSOT-001 --agent Agent-1 --deliverables "Analysis report, Resolution plan"
  
  # Check contract status
  python contract_claiming_system.py --status SSOT-001
  
  # Show statistics
  python contract_claiming_system.py --stats
        """
    )
    
    # Action flags
    parser.add_argument('--list', action='store_true', help='List available contracts')
    parser.add_argument('--claim', type=str, help='Claim a contract by ID')
    parser.add_argument('--update-progress', type=str, dest='update_progress', help='Update progress for a contract by ID')
    parser.add_argument('--complete', type=str, help='Complete a contract by ID')
    parser.add_argument('--status', type=str, help='Check status of a specific contract')
    parser.add_argument('--stats', action='store_true', help='Show contract statistics')
    
    # Required arguments for actions
    parser.add_argument('--agent', type=str, help='Agent ID (required for claim, update-progress, complete)')
    parser.add_argument('--category', type=str, help='Filter contracts by category')
    parser.add_argument('--progress', type=str, help='Progress update text')
    parser.add_argument('--deliverables', type=str, help='Comma-separated list of deliverables')
    
    # Optional arguments
    parser.add_argument('--task-list', type=str, default='agent_workspaces/meeting/task_list.json', 
                       help='Path to task list file (default: agent_workspaces/meeting/task_list.json)')
    
    args = parser.parse_args()
    
    # Initialize system
    if os.path.isabs(args.task_list):
        task_list_path = args.task_list
    else:
        # If relative path, try to resolve it from current working directory
        task_list_path = os.path.join(os.getcwd(), args.task_list)
    
    system = ContractClaimingSystem(task_list_path)
    
    # Execute actions
    if args.list:
        print("🚀 CONTRACT CLAIMING SYSTEM - Available Contracts")
        print("=" * 60)
        
        contracts = system.list_available_contracts(args.category)
        if contracts:
            category_filter = f" in category '{args.category}'" if args.category else ""
            print(f"✅ Found {len(contracts)} available contracts{category_filter}:")
            for contract in contracts:
                contract_id = contract.get('contract_id', 'N/A')
                title = contract.get('title', contract.get('name', 'N/A'))
                points = contract.get('extra_credit_points', contract.get('points', 0))
                category = contract.get('category', 'N/A')
                print(f"  📋 {contract_id}: {title} ({points} pts) - {category}")
        else:
            print("❌ No available contracts found")
    
    elif args.claim:
        if not args.agent:
            print("❌ Error: --agent is required for claiming contracts")
            sys.exit(1)
        
        print(f"📋 Claiming contract {args.claim} for {args.agent}...")
        result = system.claim_contract(args.claim, args.agent)
        
        if result["success"]:
            print(f"✅ {result['message']}")
            contract = result['contract']
            title = contract.get('title', contract.get('name', 'N/A'))
            points = contract.get('extra_credit_points', contract.get('points', 0))
            print(f"📊 Contract: {title}")
            print(f"🏆 Points: {points}")
        else:
            print(f"❌ {result['message']}")
            sys.exit(1)
    
    elif args.update_progress:
        if not args.agent:
            print("❌ Error: --agent is required for updating progress")
            sys.exit(1)
        if not args.progress:
            print("❌ Error: --progress is required for updating progress")
            sys.exit(1)
        
        print(f"📈 Updating progress for contract {args.update_progress}...")
        result = system.update_contract_progress(args.update_progress, args.agent, args.progress)
        
        if result["success"]:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['message']}")
            sys.exit(1)
    
    elif args.complete:
        if not args.agent:
            print("❌ Error: --agent is required for completing contracts")
            sys.exit(1)
        if not args.deliverables:
            print("❌ Error: --deliverables is required for completing contracts")
            sys.exit(1)
        
        deliverables = [d.strip() for d in args.deliverables.split(',')]
        print(f"🎯 Completing contract {args.complete} for {args.agent}...")
        result = system.complete_contract(args.complete, args.agent, deliverables)
        
        if result["success"]:
            print(f"✅ {result['message']}")
            print(f"🏆 Points earned: {result['points_earned']}")
            print(f"📦 Deliverables: {', '.join(result['deliverables'])}")
        else:
            print(f"❌ {result['message']}")
            sys.exit(1)
    
    elif args.status:
        print(f"📊 Checking status of contract {args.status}...")
        result = system.get_contract_status(args.status)
        
        if result["success"]:
            contract = result['contract']
            print(f"📋 Contract ID: {contract.get('contract_id', 'N/A')}")
            print(f"📝 Title: {contract.get('title', contract.get('name', 'N/A'))}")
            print(f"📈 Status: {contract.get('status', 'N/A')}")
            print(f"🤖 Claimed by: {contract.get('claimed_by', 'N/A')}")
            print(f"📊 Progress: {contract.get('progress', 'N/A')}")
            print(f"🏆 Points: {contract.get('extra_credit_points', contract.get('points', 0))}")
        else:
            print(f"❌ {result['message']}")
            sys.exit(1)
    
    elif args.stats:
        print("📊 CONTRACT CLAIMING SYSTEM - Statistics")
        print("=" * 60)
        
        stats = system.get_contract_statistics()
        print(f"📋 Total Contracts: {stats['total_contracts']}")
        print(f"✅ Available: {stats['available_contracts']}")
        print(f"🔄 Claimed: {stats['claimed_contracts']}")
        print(f"🏆 Completed: {stats['completed_contracts']}")
        print(f"💎 Total Points: {stats['total_extra_credit']}")
    
    else:
        # No action specified, show help
        parser.print_help()

if __name__ == "__main__":
    main()
