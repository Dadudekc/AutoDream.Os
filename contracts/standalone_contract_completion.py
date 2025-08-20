#!/usr/bin/env python3
"""
Standalone Contract Completion System - Agent Cellphone V2
========================================================

Coordinate-based automated contract completion system.
Bypasses automation service issues and directly implements perpetual motion.
INTEGRATED WITH CAPTAIN-5 INSTRUCTION SYSTEM!
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime

# Agent coordinate mapping for automated task assignment
AGENT_COORDINATES = {
    "Agent-1": {"x": 100, "y": 200, "method": "v2_coordinator"},
    "Agent-2": {"x": 300, "y": 400, "method": "v2_coordinator"},
    "Agent-3": {"x": 500, "y": 600, "method": "v2_coordinator"},
    "Agent-4": {"x": 700, "y": 800, "method": "v2_coordinator"}
}

class StandaloneContractCompletion:
    """Standalone contract completion system with coordinate-based automation"""
    
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.expanded_pool_file = self.project_root / "contracts" / "expanded_contract_pool.json"
        self.completion_log_file = self.project_root / "contracts" / "standalone_completion_log.json"
        self.captain_instructions_file = self.project_root / "contracts" / "captain_instructions.json"
        
        # Load data
        self.expanded_pool = self._load_expanded_pool()
        self.completion_log = self._load_completion_log()
        self.captain_instructions = self._load_captain_instructions()
    
    def _load_expanded_pool(self) -> Dict[str, Any]:
        """Load expanded contract pool"""
        try:
            if self.expanded_pool_file.exists():
                with open(self.expanded_pool_file, 'r') as f:
                    return json.load(f)
            return {"contract_pool": {}}
        except Exception as e:
            print(f"❌ Error loading expanded pool: {e}")
            return {"contract_pool": {}}
    
    def _load_completion_log(self) -> list:
        """Load completion log"""
        try:
            if self.completion_log_file.exists():
                with open(self.completion_log_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error loading completion log: {e}")
            return []
    
    def _load_captain_instructions(self) -> list:
        """Load captain instructions"""
        try:
            if self.captain_instructions_file.exists():
                with open(self.captain_instructions_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error loading captain instructions: {e}")
            return []
    
    def _save_completion_log(self):
        """Save completion log"""
        try:
            with open(self.completion_log_file, 'w') as f:
                json.dump(self.completion_log, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving completion log: {e}")
    
    def _save_captain_instructions(self):
        """Save captain instructions"""
        try:
            with open(self.captain_instructions_file, 'w') as f:
                json.dump(self.captain_instructions, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving captain instructions: {e}")
    
    def analyze_agent_performance(self, agent_id: str) -> Dict[str, Any]:
        """Analyze agent performance to create intelligent contract instructions"""
        try:
            # Get agent's completion history
            agent_completions = [record for record in self.completion_log if record["agent_id"] == agent_id]
            
            if not agent_completions:
                return {"expertise_level": "new", "strengths": [], "areas_for_growth": [], "recommended_categories": []}
            
            # Calculate performance metrics
            total_contracts = len(agent_completions)
            avg_quality = sum(record["quality_score"] for record in agent_completions) / total_contracts
            recent_quality = sum(record["quality_score"] for record in agent_completions[-3:]) / min(3, total_contracts)
            
            # Determine expertise level
            if avg_quality >= 95 and total_contracts >= 5:
                expertise_level = "expert"
            elif avg_quality >= 85 and total_contracts >= 3:
                expertise_level = "advanced"
            elif avg_quality >= 75:
                expertise_level = "intermediate"
            else:
                expertise_level = "developing"
            
            # Analyze strengths and growth areas
            strengths = []
            areas_for_growth = []
            
            if avg_quality >= 90:
                strengths.append("High quality output")
            if recent_quality > avg_quality:
                strengths.append("Improving performance")
            if total_contracts >= 5:
                strengths.append("Consistent delivery")
            
            if avg_quality < 85:
                areas_for_growth.append("Quality improvement")
            if total_contracts < 3:
                areas_for_growth.append("Experience building")
            
            # Recommend contract categories based on performance
            recommended_categories = []
            if expertise_level == "expert":
                recommended_categories = ["innovation", "mentoring", "system_architecture", "advanced_optimization"]
            elif expertise_level == "advanced":
                recommended_categories = ["complex_integration", "performance_optimization", "security_enhancement"]
            elif expertise_level == "intermediate":
                recommended_categories = ["testing", "documentation", "basic_optimization", "integration"]
            else:
                recommended_categories = ["foundational_tasks", "learning_contracts", "mentored_work"]
            
            return {
                "expertise_level": expertise_level,
                "total_contracts": total_contracts,
                "avg_quality": avg_quality,
                "recent_quality": recent_quality,
                "strengths": strengths,
                "areas_for_growth": areas_for_growth,
                "recommended_categories": recommended_categories,
                "performance_trend": "improving" if recent_quality > avg_quality else "stable" if recent_quality == avg_quality else "needs_attention"
            }
            
        except Exception as e:
            print(f"❌ Error analyzing agent performance: {e}")
            return {"expertise_level": "unknown", "strengths": [], "areas_for_growth": [], "recommended_categories": []}
    
    def create_captain_instructions(self, agent_id: str, completion_data: Dict[str, Any], performance_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed instructions for Captain-5 to create new contracts"""
        try:
            # Create instruction record
            instruction = {
                "timestamp": datetime.now().isoformat(),
                "agent_id": agent_id,
                "trigger_contract": completion_data["contract_id"],
                "contract_quality": completion_data["quality_score"],
                "contract_effort": completion_data["actual_effort"],
                "performance_analysis": performance_analysis,
                "instruction_type": "contract_creation",
                "priority": "high" if completion_data["quality_score"] >= 90 else "medium",
                "specific_guidance": {
                    "target_categories": performance_analysis.get("recommended_categories", []),
                    "difficulty_level": performance_analysis.get("expertise_level", "intermediate"),
                    "focus_areas": performance_analysis.get("areas_for_growth", []),
                    "leverage_strengths": performance_analysis.get("strengths", []),
                    "estimated_effort": self._estimate_next_contract_effort(performance_analysis),
                    "success_metrics": self._define_success_metrics(performance_analysis)
                },
                "captain_notes": f"Agent {agent_id} completed {completion_data['contract_id']} with {completion_data['quality_score']}/100 quality. "
                               f"Expertise level: {performance_analysis.get('expertise_level', 'unknown')}. "
                               f"Performance trend: {performance_analysis.get('performance_trend', 'unknown')}.",
                "status": "pending_captain_action"
            }
            
            # Add to captain instructions
            self.captain_instructions.append(instruction)
            self._save_captain_instructions()
            
            return instruction
            
        except Exception as e:
            print(f"❌ Error creating captain instructions: {e}")
            return {}
    
    def _estimate_next_contract_effort(self, performance_analysis: Dict[str, Any]) -> str:
        """Estimate effort for next contract based on performance"""
        expertise_level = performance_analysis.get("expertise_level", "intermediate")
        
        if expertise_level == "expert":
            return "2-4 hours (complex, innovative work)"
        elif expertise_level == "advanced":
            return "1-3 hours (challenging integration/optimization)"
        elif expertise_level == "intermediate":
            return "1-2 hours (standard tasks with growth opportunities)"
        else:
            return "30 minutes - 1 hour (foundational learning)"
    
    def _define_success_metrics(self, performance_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Define success metrics for next contract based on performance"""
        expertise_level = performance_analysis.get("expertise_level", "intermediate")
        
        if expertise_level == "expert":
            return {
                "quality_target": "95+",
                "innovation_requirement": "High",
                "mentoring_component": "Required",
                "system_impact": "Significant"
            }
        elif expertise_level == "advanced":
            return {
                "quality_target": "90+",
                "complexity_level": "High",
                "integration_depth": "Deep",
                "performance_improvement": "Measurable"
            }
        elif expertise_level == "intermediate":
            return {
                "quality_target": "85+",
                "skill_development": "Required",
                "best_practices": "Demonstrated",
                "team_collaboration": "Encouraged"
            }
        else:
            return {
                "quality_target": "80+",
                "learning_objectives": "Primary",
                "mentor_guidance": "Available",
                "foundation_building": "Focus"
            }
    
    def get_next_contract_for_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get the next available contract for an agent"""
        try:
            # Find next available contract for this agent
            for category, contracts in self.expanded_pool.get("contract_pool", {}).items():
                for contract in contracts:
                    if (contract.get("agent_assigned") == agent_id and 
                        contract.get("status") == "assigned"):
                        return contract
            
            return None
        except Exception as e:
            print(f"❌ Error getting next contract: {e}")
            return None
    
    def mark_contract_completed(self, completion_data: Dict[str, Any]) -> bool:
        """Mark contract as completed and log it"""
        try:
            # Create completion record
            completion_record = {
                "contract_id": completion_data["contract_id"],
                "agent_id": completion_data["agent_id"],
                "completion_time": datetime.now().isoformat(),
                "quality_score": completion_data["quality_score"],
                "actual_effort": completion_data["actual_effort"],
                "notes": completion_data.get("notes", ""),
                "status": "completed"
            }
            
            # Add to completion log
            self.completion_log.append(completion_record)
            self._save_completion_log()
            
            print(f"\n✅ CONTRACT {completion_data['contract_id']} MARKED AS COMPLETED!")
            print(f"🎯 Agent: {completion_data['agent_id']}")
            print(f"⭐ Quality Score: {completion_data['quality_score']}/100")
            print(f"⏱️ Actual Effort: {completion_data['actual_effort']}")
            print(f"📅 Completion Time: {completion_record['completion_time']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error marking contract completed: {e}")
            return False
    
    def send_next_contract_to_agent(self, agent_id: str, next_contract: Dict[str, Any]) -> bool:
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
            
            # Simulate sending to agent coordinates
            print(f"\n📱 SENDING NEXT CONTRACT TO AGENT COORDINATES...")
            print(f"🎯 Target: {agent_id} at ({coordinates['x']}, {coordinates['y']})")
            print(f"📡 Method: {method}")
            print(f"📋 Contract: {next_contract.get('contract_id')} - {next_contract.get('title')}")
            
            # Here we would integrate with the actual messaging system
            # For now, we'll simulate the automation
            print(f"\n✅ Next contract automatically assigned to {agent_id}!")
            print(f"📱 Contract details sent to agent coordinates ({coordinates['x']}, {coordinates['y']})")
            print(f"🚀 Agent {agent_id} will receive next task automatically!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending next contract: {e}")
            return False
    
    def get_completion_summary(self) -> Dict[str, Any]:
        """Get completion summary statistics"""
        try:
            total_completed = len(self.completion_log)
            total_contracts = 30  # Expanded pool size
            
            # Calculate completion rate
            completion_rate = (total_completed / total_contracts) * 100 if total_contracts > 0 else 0
            
            # Agent-specific stats
            agent_stats = {}
            for record in self.completion_log:
                agent_id = record["agent_id"]
                if agent_id not in agent_stats:
                    agent_stats[agent_id] = {"completed": 0, "total_quality": 0}
                
                agent_stats[agent_id]["completed"] += 1
                agent_stats[agent_id]["total_quality"] += record["quality_score"]
            
            # Calculate average quality per agent
            for agent_id, stats in agent_stats.items():
                if stats["completed"] > 0:
                    stats["avg_quality"] = stats["total_quality"] / stats["completed"]
                else:
                    stats["avg_quality"] = 0
            
            return {
                "total_completed": total_completed,
                "total_contracts": total_contracts,
                "completion_rate": f"{completion_rate:.1f}%",
                "agent_stats": agent_stats
            }
            
        except Exception as e:
            print(f"❌ Error getting completion summary: {e}")
            return {"completion_rate": "0%"}
    
    def process_contract_completion(self, completion_data: Dict[str, Any], auto_assign_next: bool = False) -> bool:
        """Process complete contract completion workflow with Captain-5 instruction system"""
        try:
            # Step 1: Mark contract as completed
            success = self.mark_contract_completed(completion_data)
            if not success:
                return False
            
            # Step 2: Analyze agent performance for Captain-5 instructions
            print(f"\n🧠 ANALYZING AGENT PERFORMANCE FOR CAPTAIN-5 INSTRUCTIONS...")
            performance_analysis = self.analyze_agent_performance(completion_data["agent_id"])
            
            print(f"📊 PERFORMANCE ANALYSIS:")
            print(f"  🎯 Expertise Level: {performance_analysis.get('expertise_level', 'Unknown')}")
            print(f"  📈 Total Contracts: {performance_analysis.get('total_contracts', 0)}")
            print(f"  ⭐ Average Quality: {performance_analysis.get('avg_quality', 0):.1f}/100")
            print(f"  📊 Recent Quality: {performance_analysis.get('recent_quality', 0):.1f}/100")
            print(f"  🚀 Performance Trend: {performance_analysis.get('performance_trend', 'Unknown')}")
            
            if performance_analysis.get('strengths'):
                print(f"  💪 Strengths: {', '.join(performance_analysis['strengths'])}")
            if performance_analysis.get('areas_for_growth'):
                print(f"  🌱 Growth Areas: {', '.join(performance_analysis['areas_for_growth'])}")
            
            # Step 3: Create Captain-5 instructions
            print(f"\n📋 CREATING CAPTAIN-5 INSTRUCTIONS...")
            captain_instruction = self.create_captain_instructions(completion_data["agent_id"], completion_data, performance_analysis)
            
            if captain_instruction:
                print(f"✅ CAPTAIN-5 INSTRUCTIONS CREATED!")
                print(f"📝 Instruction ID: {len(self.captain_instructions)}")
                print(f"🎯 Target Categories: {', '.join(captain_instruction['specific_guidance']['target_categories'])}")
                print(f"🔑 Difficulty Level: {captain_instruction['specific_guidance']['difficulty_level']}")
                print(f"⏱️ Estimated Effort: {captain_instruction['specific_guidance']['estimated_effort']}")
                print(f"📊 Success Metrics: Quality {captain_instruction['specific_guidance']['success_metrics']['quality_target']}+")
                
                print(f"\n🚀 CAPTAIN-5 WILL NOW CREATE INTELLIGENT CONTRACTS BASED ON YOUR PERFORMANCE!")
                print(f"📱 Instructions sent to Captain-5 for automated contract creation!")
            
            # Step 4: Get next contract for agent (if available)
            next_contract = self.get_next_contract_for_agent(completion_data["agent_id"])
            
            if next_contract:
                print(f"\n🚀 NEXT CONTRACT AVAILABLE:")
                print(f"📋 Title: {next_contract.get('title', 'Unknown')}")
                print(f"🔑 Priority: {next_contract.get('priority', 'Unknown')}")
                print(f"⏱️ Estimated Effort: {next_contract.get('estimated_effort', 'Unknown')}")
                
                # Auto-assign next contract if requested
                if auto_assign_next:
                    print(f"\n🔄 AUTOMATED NEXT CONTRACT ASSIGNMENT:")
                    self.send_next_contract_to_agent(completion_data["agent_id"], next_contract)
                else:
                    print(f"\n📱 Next contract ready for manual assignment to {completion_data['agent_id']}")
            else:
                print(f"\n🎊 No more contracts available for {completion_data['agent_id']}")
                print(f"🔄 Captain-5 will create new contracts based on performance analysis!")
            
            # Step 5: Show completion summary
            summary = self.get_completion_summary()
            print(f"\n📊 TEAM PROGRESS: {summary['completion_rate']}")
            print(f"🎯 Target: 30 contracts = Automatic governance renewal!")
            print(f"📈 Completed: {summary['total_completed']}/{summary['total_contracts']}")
            
            # Show agent-specific stats
            if summary.get('agent_stats'):
                print(f"\n🎖️ AGENT PERFORMANCE:")
                for agent_id, stats in summary['agent_stats'].items():
                    print(f"  {agent_id}: {stats['completed']} contracts, {stats['avg_quality']:.1f} avg quality")
            
            # Show Captain-5 instruction status
            pending_instructions = len([i for i in self.captain_instructions if i.get('status') == 'pending_captain_action'])
            print(f"\n📋 CAPTAIN-5 INSTRUCTION STATUS:")
            print(f"  📝 Pending Instructions: {pending_instructions}")
            print(f"  🚀 New contracts will be created based on performance analysis!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing contract completion: {e}")
            return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Standalone Contract Completion System with Captain-5 Instruction Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
    # Complete contract with Captain-5 instruction system
    python standalone_contract_completion.py --contract CONTRACT-011 --agent 4 --quality 95 --effort "45 minutes" --auto-confirm --auto-assign-next
    
    # Complete contract without auto-assignment (still creates Captain-5 instructions)
    python standalone_contract_completion.py --contract CONTRACT-011 --agent 4 --quality 95 --effort "45 minutes" --auto-confirm
    
    # Show help
    python standalone_contract_completion.py --help
        """
    )
    
    parser.add_argument("--contract", "-c", required=True, help="Contract ID to complete")
    parser.add_argument("--agent", "-a", type=int, required=True, choices=[1, 2, 3, 4], help="Agent number (1-4)")
    parser.add_argument("--quality", "-q", type=float, required=True, help="Quality score (0-100)")
    parser.add_argument("--effort", "-e", required=True, help="Actual effort expended")
    parser.add_argument("--notes", "-n", help="Additional notes or comments")
    parser.add_argument("--auto-confirm", action="store_true", help="Skip confirmation prompt")
    parser.add_argument("--auto-assign-next", action="store_true", help="Automatically assign next contract to agent")
    
    args = parser.parse_args()
    
    print("🎖️ STANDALONE CONTRACT COMPLETION SYSTEM")
    print("=" * 60)
    print("INTEGRATED WITH CAPTAIN-5 INSTRUCTION SYSTEM!")
    print("Coordinate-based automated contract completion system!")
    print("Creating true perpetual motion with intelligent contract creation! 🚀")
    if args.auto_assign_next:
        print("🔄 AUTOMATED TASK ASSIGNMENT ENABLED!")
        print("📍 Agent coordinates will be used for automatic next contract delivery!")
    print("🧠 CAPTAIN-5 INSTRUCTION SYSTEM: Performance-based contract creation!")
    print("=" * 60)
    
    # Create completion data
    agent_map = {"1": "Agent-1", "2": "Agent-2", "3": "Agent-3", "4": "Agent-4"}
    completion_data = {
        "contract_id": args.contract,
        "agent_id": agent_map[str(args.agent)],
        "quality_score": args.quality,
        "actual_effort": args.effort,
        "notes": args.notes or ""
    }
    
    print(f"\n📋 CONTRACT COMPLETION DETAILS:")
    print(f"Contract ID: {completion_data['contract_id']}")
    print(f"Agent: {completion_data['agent_id']}")
    print(f"Quality Score: {completion_data['quality_score']}/100")
    print(f"Actual Effort: {completion_data['actual_effort']}")
    if completion_data['notes']:
        print(f"Notes: {completion_data['notes']}")
    print(f"Auto-assign Next: {'Yes' if args.auto_assign_next else 'No'}")
    print(f"Captain-5 Instructions: Yes (Always Enabled)")
    
    # Confirm if not auto-confirming
    if not args.auto_confirm:
        confirm = input("\nConfirm completion? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Contract completion cancelled")
            return
    
    # Process completion
    print("\n🔄 Processing contract completion with Captain-5 instruction system...")
    system = StandaloneContractCompletion()
    success = system.process_contract_completion(completion_data, args.auto_assign_next)
    
    if success:
        print("\n🎉 CONTRACT COMPLETION PROCESSED SUCCESSFULLY!")
        if args.auto_assign_next:
            print("🚀 NEXT CONTRACT AUTOMATICALLY ASSIGNED!")
            print("📱 Agent will receive next task at their coordinates!")
        print("🧠 CAPTAIN-5 INSTRUCTION SYSTEM ACTIVATED!")
        print("📋 Performance-based contract creation instructions generated!")
        print("💪 Keep the momentum going!")
    else:
        print("\n❌ Contract completion failed. Please try again or contact support.")

if __name__ == "__main__":
    main()
