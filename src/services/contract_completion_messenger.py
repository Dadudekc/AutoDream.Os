#!/usr/bin/env python3
"""
Contract Completion Messenger - Agent Cellphone V2
================================================

Automatically sends completion messages and next contract assignments to agents.
This creates the perpetual motion machine where completing one contract automatically
triggers the next assignment.
"""

import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import our services
from contract_automation_service import ContractAutomationService
from captain_coordinator_v2 import CaptainCoordinatorV2

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
log = logging.getLogger("contract_completion_messenger")

class ContractCompletionMessenger:
    """Automated messaging service for contract completion"""
    
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[3]
        self.automation_service = ContractAutomationService()
        self.coordinator = CaptainCoordinatorV2()
        
        log.info("Contract Completion Messenger initialized")
    
    def process_contract_completion(self, contract_id: str, agent_id: str, 
                                  quality_score: float = 100.0, 
                                  actual_effort: str = "", 
                                  notes: str = "") -> bool:
        """Process contract completion and send automated messages"""
        try:
            log.info(f"Processing completion of contract {contract_id} by {agent_id}")
            
            # Mark contract as completed in automation service
            success = self.automation_service.mark_contract_completed(
                contract_id, agent_id, quality_score, actual_effort, notes
            )
            
            if not success:
                log.error(f"Failed to mark contract {contract_id} as completed")
                return False
            
            # Get the completed contract details
            completed_contract = self._get_contract_details(contract_id)
            if not completed_contract:
                log.error(f"Could not find contract {contract_id} details")
                return False
            
            # Get the next assigned contract
            next_contract = self.automation_service.get_agent_next_contract(agent_id)
            
            # Create completion message
            completion_message = self.automation_service.create_completion_message(
                agent_id, completed_contract, next_contract
            )
            
            # Send completion message to agent
            message_sent = self.coordinator.send_message_to_agent(
                agent_id, completion_message, high_priority=True
            )
            
            if message_sent:
                log.info(f"Completion message sent to {agent_id} for contract {contract_id}")
                
                # If there's a next contract, send additional motivation
                if next_contract:
                    self._send_motivation_message(agent_id, next_contract)
                
                return True
            else:
                log.error(f"Failed to send completion message to {agent_id}")
                return False
                
        except Exception as e:
            log.error(f"Error processing contract completion: {e}")
            return False
    
    def _get_contract_details(self, contract_id: str) -> Optional[Dict[str, Any]]:
        """Get contract details from pool"""
        try:
            contract_pool = self.automation_service.contract_pool
            
            for category, contracts in contract_pool.get("contract_pool", {}).items():
                for contract in contracts:
                    if contract.get("contract_id") == contract_id:
                        return contract
            
            return None
            
        except Exception as e:
            log.error(f"Error getting contract details: {e}")
            return None
    
    def _send_motivation_message(self, agent_id: str, next_contract: Dict[str, Any]):
        """Send motivational message for next contract"""
        try:
            motivation_message = f"🔥 MOTIVATION BOOST FOR {agent_id}!\n\n"
            motivation_message += f"🎯 You're on fire! Contract completed successfully!\n"
            motivation_message += f"🚀 Your next challenge awaits: {next_contract.get('title', 'Unknown')}\n"
            motivation_message += f"💪 Estimated effort: {next_contract.get('estimated_effort', 'Unknown')}\n"
            motivation_message += f"🏆 Success criteria: {next_contract.get('success_criteria', 'No criteria')}\n\n"
            motivation_message += f"⚡ Keep the momentum going! Every contract brings us closer to 50!\n"
            motivation_message += f"🎖️ Captain-5 is counting on you!"
            
            # Send motivation message
            self.coordinator.send_message_to_agent(
                agent_id, motivation_message, high_priority=False
            )
            
            log.info(f"Motivation message sent to {agent_id}")
            
        except Exception as e:
            log.error(f"Error sending motivation message: {e}")
    
    def send_contract_reminder(self, agent_id: str) -> bool:
        """Send reminder about current contract"""
        try:
            next_contract = self.automation_service.get_agent_next_contract(agent_id)
            
            if next_contract:
                reminder_message = f"⏰ CONTRACT REMINDER FOR {agent_id}\n\n"
                reminder_message += f"📋 Current Contract: {next_contract.get('title', 'Unknown')}\n"
                reminder_message += f"📝 Description: {next_contract.get('description', 'No description')[:100]}...\n"
                reminder_message += f"🔑 Priority: {next_contract.get('priority', 'Unknown')}\n"
                reminder_message += f"⏱️ Estimated Effort: {next_contract.get('estimated_effort', 'Unknown')}\n"
                reminder_message += f"🎯 Success Criteria: {next_contract.get('success_criteria', 'No criteria')[:100]}...\n\n"
                reminder_message += f"💪 Keep pushing forward! Every completed contract brings us closer to the election!"
                
                return self.coordinator.send_message_to_agent(
                    agent_id, reminder_message, high_priority=False
                )
            else:
                log.info(f"No current contract for {agent_id} to remind about")
                return False
                
        except Exception as e:
            log.error(f"Error sending contract reminder: {e}")
            return False
    
    def send_progress_update(self, agent_id: str) -> bool:
        """Send progress update to agent"""
        try:
            summary = self.automation_service.get_completion_summary()
            agent_data = self.automation_service.agent_workload.get("agent_workload", {}).get(agent_id, {})
            
            progress_message = f"📊 PROGRESS UPDATE FOR {agent_id}\n\n"
            progress_message += f"🎯 Overall Progress: {summary.get('completion_rate', '0%')}\n"
            progress_message += f"📈 Your Personal Progress:\n"
            progress_message += f"   ✅ Completed: {agent_data.get('completed', 0)}\n"
            progress_message += f"   🔄 In Progress: {agent_data.get('in_progress', 0)}\n"
            progress_message += f"   📋 Assigned: {agent_data.get('assigned', 0)}\n\n"
            progress_message += f"🏆 Team Progress: {summary.get('total_completions', 0)}/50 contracts completed\n"
            progress_message += f"🎖️ Captain-5's Target: 50 contracts = Automatic Election Trigger!\n\n"
            progress_message += f"💪 You're making a difference! Keep up the excellent work!"
            
            return self.coordinator.send_message_to_agent(
                agent_id, progress_message, high_priority=False
            )
            
        except Exception as e:
            log.error(f"Error sending progress update: {e}")
            return False
    
    def broadcast_team_progress(self) -> Dict[str, bool]:
        """Broadcast team progress to all agents"""
        try:
            summary = self.automation_service.get_completion_summary()
            
            broadcast_message = f"📢 TEAM PROGRESS BROADCAST\n\n"
            broadcast_message += f"🎯 Overall Progress: {summary.get('completion_rate', '0%')}\n"
            broadcast_message += f"📊 Total Completions: {summary.get('total_completions', 0)}/50\n"
            broadcast_message += f"📈 Today's Completions: {summary.get('today_completions', 0)}\n\n"
            broadcast_message += f"🏆 Individual Contributions:\n"
            
            for agent_id, completions in summary.get('agent_completions', {}).items():
                broadcast_message += f"   {agent_id}: {completions} contracts completed\n"
            
            broadcast_message += f"\n🎖️ Captain-5's Message: We're building momentum! "
            broadcast_message += f"Every contract brings us closer to the automatic election trigger. "
            broadcast_message += f"Keep pushing forward, team!"
            
            # Send to all agents
            results = self.coordinator.send_message_to_all_agents(
                broadcast_message, high_priority=False
            )
            
            log.info(f"Team progress broadcast sent. Results: {results}")
            return results
            
        except Exception as e:
            log.error(f"Error broadcasting team progress: {e}")
            return {}
    
    def send_contract_completion_notification(self, contract_id: str, agent_id: str, 
                                            quality_score: float) -> bool:
        """Send notification about contract completion to all agents"""
        try:
            completed_contract = self._get_contract_details(contract_id)
            if not completed_contract:
                return False
            
            notification_message = f"🎉 CONTRACT COMPLETION NOTIFICATION\n\n"
            notification_message += f"🏆 Agent: {agent_id}\n"
            notification_message += f"📋 Contract: {completed_contract.get('title', 'Unknown')}\n"
            notification_message += f"⭐ Quality Score: {quality_score}/100\n"
            notification_message += f"⏰ Completed: {datetime.now().strftime('%H:%M:%S')}\n\n"
            notification_message += f"📊 Progress: {self.automation_service.get_completion_summary().get('completion_rate', '0%')}\n"
            notification_message += f"🎯 Target: 50 contracts = Automatic Election!\n\n"
            notification_message += f"💪 Great job, {agent_id}! You're inspiring the team!"
            
            # Send to all agents
            results = self.coordinator.send_message_to_all_agents(
                notification_message, high_priority=False
            )
            
            success_count = sum(results.values())
            log.info(f"Contract completion notification sent. {success_count}/{len(results)} successful")
            
            return success_count > 0
            
        except Exception as e:
            log.error(f"Error sending contract completion notification: {e}")
            return False

def main():
    """CLI interface for Contract Completion Messenger"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Contract Completion Messenger")
    parser.add_argument("--complete", nargs=4, 
                       metavar=("CONTRACT_ID", "AGENT_ID", "QUALITY_SCORE", "EFFORT"), 
                       help="Process contract completion")
    parser.add_argument("--reminder", metavar="AGENT_ID", help="Send contract reminder to agent")
    parser.add_argument("--progress", metavar="AGENT_ID", help="Send progress update to agent")
    parser.add_argument("--broadcast", action="store_true", help="Broadcast team progress")
    parser.add_argument("--notify", nargs=3, 
                       metavar=("CONTRACT_ID", "AGENT_ID", "QUALITY_SCORE"),
                       help="Send completion notification to all agents")
    
    args = parser.parse_args()
    
    messenger = ContractCompletionMessenger()
    
    if args.complete:
        contract_id, agent_id, quality_score, effort = args.complete
        success = messenger.process_contract_completion(
            contract_id, agent_id, float(quality_score), effort
        )
        if success:
            print(f"✅ Contract completion processed successfully for {agent_id}")
        else:
            print(f"❌ Failed to process contract completion for {agent_id}")
    
    elif args.reminder:
        success = messenger.send_contract_reminder(args.reminder)
        if success:
            print(f"✅ Contract reminder sent to {args.reminder}")
        else:
            print(f"❌ Failed to send reminder to {args.reminder}")
    
    elif args.progress:
        success = messenger.send_progress_update(args.progress)
        if success:
            print(f"✅ Progress update sent to {args.progress}")
        else:
            print(f"❌ Failed to send progress update to {args.progress}")
    
    elif args.broadcast:
        results = messenger.broadcast_team_progress()
        success_count = sum(results.values())
        print(f"✅ Team progress broadcast sent. {success_count}/{len(results)} successful")
    
    elif args.notify:
        contract_id, agent_id, quality_score = args.notify
        success = messenger.send_contract_completion_notification(
            contract_id, agent_id, float(quality_score)
        )
        if success:
            print(f"✅ Completion notification sent for contract {contract_id}")
        else:
            print(f"❌ Failed to send completion notification")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
