#!/usr/bin/env python3
"""
Contract Automation Service - Agent Cellphone V2
===============================================

Automated contract assignment system that creates perpetual motion:
- Automatically assigns next contract when one is completed
- Sends completion messages to agents
- Maintains continuous workflow
- Tracks progress and triggers next assignments
"""

import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
log = logging.getLogger("contract_automation_service")

@dataclass
class ContractCompletion:
    """Contract completion event"""
    contract_id: str
    agent_id: str
    completion_time: str
    quality_score: float
    actual_effort: str
    notes: str = ""

@dataclass
class NextContractAssignment:
    """Next contract assignment for agent"""
    contract_id: str
    title: str
    description: str
    priority: str
    estimated_effort: str
    category: str
    success_criteria: str

class ContractAutomationService:
    """Automated contract assignment and completion system"""
    
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        self.contract_pool_file = self.project_root / "contracts" / "contract_pool.json"
        self.completion_log_file = self.project_root / "contracts" / "completion_log.json"
        self.agent_workload_file = self.project_root / "contracts" / "agent_workload.json"
        
        # Load existing data
        self.contract_pool = self._load_contract_pool()
        self.completion_log = self._load_completion_log()
        self.agent_workload = self._load_agent_workload()
        
        log.info("Contract Automation Service initialized")
    
    def _load_contract_pool(self) -> Dict[str, Any]:
        """Load contract pool from file"""
        try:
            if self.contract_pool_file.exists():
                with open(self.contract_pool_file, 'r') as f:
                    return json.load(f)
            return {"contract_pool": {}, "contract_stats": {}}
        except Exception as e:
            log.error(f"Error loading contract pool: {e}")
            return {"contract_pool": {}, "contract_stats": {}}
    
    def _load_completion_log(self) -> List[ContractCompletion]:
        """Load completion log from file"""
        try:
            if self.completion_log_file.exists():
                with open(self.completion_log_file, 'r') as f:
                    data = json.load(f)
                    return [ContractCompletion(**item) for item in data.get("completions", [])]
            return []
        except Exception as e:
            log.error(f"Error loading completion log: {e}")
            return []
    
    def _load_agent_workload(self) -> Dict[str, Any]:
        """Load agent workload from file"""
        try:
            if self.agent_workload_file.exists():
                with open(self.agent_workload_file, 'r') as f:
                    return json.load(f)
            return {"agent_workload": {}}
        except Exception as e:
            log.error(f"Error loading agent workload: {e}")
            return {"agent_workload": {}}
    
    def _save_completion_log(self):
        """Save completion log to file"""
        try:
            data = {"completions": [asdict(completion) for completion in self.completion_log]}
            with open(self.completion_log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            log.error(f"Error saving completion log: {e}")
    
    def _save_agent_workload(self):
        """Save agent workload to file"""
        try:
            with open(self.agent_workload_file, 'w') as f:
                json.dump(self.agent_workload, f, indent=2)
        except Exception as e:
            log.error(f"Error saving agent workload: {e}")
    
    def mark_contract_completed(self, contract_id: str, agent_id: str, 
                               quality_score: float = 100.0, 
                               actual_effort: str = "", 
                               notes: str = "") -> bool:
        """Mark a contract as completed and trigger next assignment"""
        try:
            # Create completion record
            completion = ContractCompletion(
                contract_id=contract_id,
                agent_id=agent_id,
                completion_time=datetime.now().isoformat(),
                quality_score=quality_score,
                actual_effort=actual_effort,
                notes=notes
            )
            
            # Add to completion log
            self.completion_log.append(completion)
            self._save_completion_log()
            
            # Update contract status in pool
            self._update_contract_status(contract_id, "completed")
            
            # Update agent workload
            self._update_agent_workload(agent_id, contract_id, "completed")
            
            # Find and assign next contract
            next_contract = self._find_next_contract_for_agent(agent_id)
            
            if next_contract:
                self._assign_contract_to_agent(next_contract["contract_id"], agent_id)
                log.info(f"Contract {contract_id} completed by {agent_id}. Next contract {next_contract['contract_id']} assigned.")
                return True
            else:
                log.info(f"Contract {contract_id} completed by {agent_id}. No more contracts available.")
                return False
                
        except Exception as e:
            log.error(f"Error marking contract completed: {e}")
            return False
    
    def _update_contract_status(self, contract_id: str, status: str):
        """Update contract status in pool"""
        try:
            for category, contracts in self.contract_pool.get("contract_pool", {}).items():
                for contract in contracts:
                    if contract.get("contract_id") == contract_id:
                        contract["status"] = status
                        contract["completion_time"] = datetime.now().isoformat()
                        break
            
            # Update stats
            self._update_contract_stats()
            
        except Exception as e:
            log.error(f"Error updating contract status: {e}")
    
    def _update_contract_stats(self):
        """Update contract statistics"""
        try:
            total_contracts = 0
            completed_contracts = 0
            assigned_contracts = 0
            pending_contracts = 0
            
            for category, contracts in self.contract_pool.get("contract_pool", {}).items():
                for contract in contracts:
                    total_contracts += 1
                    status = contract.get("status", "pending")
                    if status == "completed":
                        completed_contracts += 1
                    elif status == "assigned":
                        assigned_contracts += 1
                    else:
                        pending_contracts += 1
            
            # Update stats
            if "contract_stats" not in self.contract_pool:
                self.contract_pool["contract_stats"] = {}
            
            self.contract_pool["contract_stats"].update({
                "total_contracts": total_contracts,
                "completed_contracts": completed_contracts,
                "assigned_contracts": assigned_contracts,
                "pending_contracts": pending_contracts,
                "completion_rate": f"{(completed_contracts/total_contracts*100):.1f}%" if total_contracts > 0 else "0%"
            })
            
        except Exception as e:
            log.error(f"Error updating contract stats: {e}")
    
    def _update_agent_workload(self, agent_id: str, contract_id: str, status: str):
        """Update agent workload tracking"""
        try:
            if "agent_workload" not in self.agent_workload:
                self.agent_workload["agent_workload"] = {}
            
            if agent_id not in self.agent_workload["agent_workload"]:
                self.agent_workload["agent_workload"][agent_id] = {
                    "assigned": 0,
                    "completed": 0,
                    "in_progress": 0,
                    "contracts": []
                }
            
            agent_data = self.agent_workload["agent_workload"][agent_id]
            
            # Update contract in agent's list
            contract_found = False
            for contract in agent_data["contracts"]:
                if contract["contract_id"] == contract_id:
                    contract["status"] = status
                    contract["completion_time"] = datetime.now().isoformat()
                    contract_found = True
                    break
            
            if not contract_found:
                agent_data["contracts"].append({
                    "contract_id": contract_id,
                    "status": status,
                    "assignment_time": datetime.now().isoformat(),
                    "completion_time": None
                })
            
            # Update counts
            agent_data["assigned"] = len([c for c in agent_data["contracts"] if c["status"] in ["assigned", "in_progress"]])
            agent_data["completed"] = len([c for c in agent_data["contracts"] if c["status"] == "completed"])
            agent_data["in_progress"] = len([c for c in agent_data["contracts"] if c["status"] == "in_progress"])
            
            self._save_agent_workload()
            
        except Exception as e:
            log.error(f"Error updating agent workload: {e}")
    
    def _find_next_contract_for_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Find the next available contract for an agent"""
        try:
            # Get agent's current workload
            agent_data = self.agent_workload.get("agent_workload", {}).get(agent_id, {})
            current_workload = agent_data.get("assigned", 0) + agent_data.get("in_progress", 0)
            
            # Don't assign more than 3 contracts at once
            if current_workload >= 3:
                return None
            
            # Find available contracts by priority
            priorities = ["HIGH", "MEDIUM", "LOW"]
            
            for priority in priorities:
                for category, contracts in self.contract_pool.get("contract_pool", {}).items():
                    for contract in contracts:
                        if (contract.get("status") == "ready_for_assignment" and 
                            contract.get("priority") == priority):
                            return contract
            
            return None
            
        except Exception as e:
            log.error(f"Error finding next contract: {e}")
            return None
    
    def _assign_contract_to_agent(self, contract_id: str, agent_id: str):
        """Assign contract to agent"""
        try:
            # Update contract status
            for category, contracts in self.contract_pool.get("contract_pool", {}).items():
                for contract in contracts:
                    if contract.get("contract_id") == contract_id:
                        contract["status"] = "assigned"
                        contract["agent_assigned"] = agent_id
                        contract["assignment_time"] = datetime.now().isoformat()
                        break
            
            # Update agent workload
            self._update_agent_workload(agent_id, contract_id, "assigned")
            
            # Save updated contract pool
            with open(self.contract_pool_file, 'w') as f:
                json.dump(self.contract_pool, f, indent=2)
            
            log.info(f"Contract {contract_id} assigned to {agent_id}")
            
        except Exception as e:
            log.error(f"Error assigning contract: {e}")
    
    def get_agent_next_contract(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get the next contract for an agent"""
        try:
            agent_data = self.agent_workload.get("agent_workload", {}).get(agent_id, {})
            
            # Find assigned contracts
            assigned_contracts = [c for c in agent_data.get("contracts", []) 
                                if c["status"] == "assigned"]
            
            if assigned_contracts:
                contract_id = assigned_contracts[0]["contract_id"]
                
                # Get contract details
                for category, contracts in self.contract_pool.get("contract_pool", {}).items():
                    for contract in contracts:
                        if contract.get("contract_id") == contract_id:
                            return contract
            
            return None
            
        except Exception as e:
            log.error(f"Error getting agent next contract: {e}")
            return None
    
    def get_completion_summary(self) -> Dict[str, Any]:
        """Get summary of contract completions"""
        try:
            total_completions = len(self.completion_log)
            today_completions = len([c for c in self.completion_log 
                                   if c.completion_time.startswith(datetime.now().date().isoformat())])
            
            agent_completions = {}
            for completion in self.completion_log:
                agent_id = completion.agent_id
                if agent_id not in agent_completions:
                    agent_completions[agent_id] = 0
                agent_completions[agent_id] += 1
            
            return {
                "total_completions": total_completions,
                "today_completions": today_completions,
                "agent_completions": agent_completions,
                "completion_rate": f"{(total_completions/50*100):.1f}%" if total_completions > 0 else "0%"
            }
            
        except Exception as e:
            log.error(f"Error getting completion summary: {e}")
            return {}
    
    def create_completion_message(self, agent_id: str, completed_contract: Dict[str, Any], 
                                next_contract: Optional[Dict[str, Any]]) -> str:
        """Create completion message for agent"""
        try:
            message = f"🎉 CONTRACT COMPLETED: {completed_contract.get('title', 'Unknown')}\n\n"
            message += f"✅ Status: COMPLETED\n"
            message += f"⏰ Completion Time: {datetime.now().strftime('%H:%M:%S')}\n"
            message += f"📊 Progress: {self.get_completion_summary().get('completion_rate', '0%')}\n\n"
            
            if next_contract:
                message += f"🚀 NEXT CONTRACT ASSIGNED:\n"
                message += f"📋 Title: {next_contract.get('title', 'Unknown')}\n"
                message += f"📝 Description: {next_contract.get('description', 'No description')}\n"
                message += f"🔑 Priority: {next_contract.get('priority', 'Unknown')}\n"
                message += f"⏱️ Estimated Effort: {next_contract.get('estimated_effort', 'Unknown')}\n"
                message += f"🎯 Success Criteria: {next_contract.get('success_criteria', 'No criteria')}\n\n"
                message += f"💪 Keep the momentum going! Complete this contract to get your next assignment automatically!"
            else:
                message += f"🎊 All contracts completed! You're ready for the next phase!"
            
            return message
            
        except Exception as e:
            log.error(f"Error creating completion message: {e}")
            return f"Contract completed. Error creating message: {e}"

def main():
    """CLI interface for Contract Automation Service"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Contract Automation Service")
    parser.add_argument("--complete", nargs=3, metavar=("CONTRACT_ID", "AGENT_ID", "QUALITY_SCORE"), 
                       help="Mark contract as completed")
    parser.add_argument("--status", action="store_true", help="Show completion status")
    parser.add_argument("--next", metavar="AGENT_ID", help="Get next contract for agent")
    parser.add_argument("--summary", action="store_true", help="Show completion summary")
    
    args = parser.parse_args()
    
    service = ContractAutomationService()
    
    if args.complete:
        contract_id, agent_id, quality_score = args.complete
        success = service.mark_contract_completed(
            contract_id, agent_id, float(quality_score)
        )
        if success:
            print(f"✅ Contract {contract_id} marked as completed by {agent_id}")
        else:
            print(f"❌ Failed to mark contract {contract_id} as completed")
    
    elif args.status:
        summary = service.get_completion_summary()
        print(json.dumps(summary, indent=2))
    
    elif args.next:
        next_contract = service.get_agent_next_contract(args.next)
        if next_contract:
            print(f"Next contract for {args.next}: {json.dumps(next_contract, indent=2)}")
        else:
            print(f"No next contract available for {args.next}")
    
    elif args.summary:
        summary = service.get_completion_summary()
        print("=== CONTRACT COMPLETION SUMMARY ===")
        print(f"Total Completions: {summary.get('total_completions', 0)}")
        print(f"Today's Completions: {summary.get('today_completions', 0)}")
        print(f"Completion Rate: {summary.get('completion_rate', '0%')}")
        print(f"Agent Completions: {summary.get('agent_completions', {})}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
