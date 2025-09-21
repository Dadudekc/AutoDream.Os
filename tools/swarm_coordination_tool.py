#!/usr/bin/env python3
"""
Swarm Intelligence Coordination Tool
Advanced 8-agent coordination with real-time communication and democratic decision-making
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from services.swarm_intelligence_coordination import SwarmIntelligenceCoordination, DecisionType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_swarm_status():
    """Get comprehensive swarm status"""
    print("🐝 Getting Swarm Intelligence Coordination Status...")
    
    swarm = SwarmIntelligenceCoordination()
    
    try:
        await swarm.initialize()
        status = await swarm.get_swarm_status()
        
        print(f"\n🌟 Swarm Intelligence Coordination Status:")
        print(f"📊 Swarm Version: {status['swarm_version']}")
        print(f"🤖 Total Agents: {status['total_agents']}")
        print(f"📋 Active Decisions: {status['active_decisions']}")
        print(f"📨 Coordination History: {status['coordination_history_size']} messages")
        
        print(f"\n📈 Swarm Metrics:")
        for metric, value in status['swarm_metrics'].items():
            print(f"  {metric}: {value}")
            
        print(f"\n🤖 Agent Status:")
        for agent_id, agent_status in status['agent_status'].items():
            print(f"  {agent_id} ({agent_status['role']}):")
            print(f"    Specialization: {agent_status['specialization']}")
            print(f"    Coordination Weight: {agent_status['coordination_weight']}")
            print(f"    Workload: {agent_status['workload']:.1%}")
            print(f"    Availability: {agent_status['availability']}")
            print(f"    Last Coordination: {agent_status['last_coordination']}")
            
        if status['active_decisions']:
            print(f"\n📋 Active Decisions:")
            for decision_id, decision_info in status['active_decisions'].items():
                print(f"  {decision_id}:")
                print(f"    Title: {decision_info['title']}")
                print(f"    Type: {decision_info['type']}")
                print(f"    Proposed by: {decision_info['proposed_by']}")
                print(f"    Status: {decision_info['status']}")
                print(f"    Votes Cast: {decision_info['votes_cast']}")
                print(f"    Consensus Score: {decision_info['consensus_score']:.2f}")
                
    except Exception as e:
        logger.error(f"Error getting swarm status: {e}")
        print(f"❌ Error: {e}")
    finally:
        await swarm.close()

async def propose_decision(agent_id: str, decision_type: str, title: str, description: str):
    """Propose a new decision for swarm consideration"""
    print(f"🐝 Proposing decision from {agent_id}...")
    
    swarm = SwarmIntelligenceCoordination()
    
    try:
        await swarm.initialize()
        
        # Convert string to DecisionType enum
        try:
            decision_type_enum = DecisionType(decision_type)
        except ValueError:
            print(f"❌ Invalid decision type: {decision_type}")
            print(f"Valid types: {[dt.value for dt in DecisionType]}")
            return
            
        decision_id = await swarm.propose_decision(
            agent_id=agent_id,
            decision_type=decision_type_enum,
            title=title,
            description=description
        )
        
        print(f"✅ Decision proposed successfully!")
        print(f"📋 Decision ID: {decision_id}")
        print(f"🎯 Type: {decision_type}")
        print(f"📝 Title: {title}")
        print(f"📄 Description: {description}")
        
    except Exception as e:
        logger.error(f"Error proposing decision: {e}")
        print(f"❌ Error: {e}")
    finally:
        await swarm.close()

async def cast_vote(agent_id: str, decision_id: str, vote: str):
    """Cast vote on a decision"""
    print(f"🗳️ Casting vote from {agent_id} on {decision_id}...")
    
    swarm = SwarmIntelligenceCoordination()
    
    try:
        await swarm.initialize()
        
        success = await swarm.cast_vote(agent_id, decision_id, vote)
        
        if success:
            print(f"✅ Vote cast successfully!")
            print(f"🗳️ Agent: {agent_id}")
            print(f"📋 Decision: {decision_id}")
            print(f"🎯 Vote: {vote}")
        else:
            print(f"❌ Failed to cast vote")
            
    except Exception as e:
        logger.error(f"Error casting vote: {e}")
        print(f"❌ Error: {e}")
    finally:
        await swarm.close()

async def run_swarm_coordination_cycle():
    """Run a full swarm coordination cycle"""
    print("🐝 Running Swarm Intelligence Coordination Cycle...")
    
    swarm = SwarmIntelligenceCoordination()
    
    try:
        await swarm.initialize()
        
        # Get current status
        status = await swarm.get_swarm_status()
        print(f"📊 Swarm Status: {status['total_agents']} agents, {status['active_decisions']} active decisions")
        
        # Check for workload balancing
        workload_balance = await swarm._balance_workload()
        if workload_balance["rebalancing_needed"]:
            print(f"⚖️ Workload rebalancing needed for {len(workload_balance['rebalancing_needed'])} agents")
        else:
            print(f"✅ Workload balanced across all agents")
            
        # Check coordination efficiency
        efficiency = status['swarm_metrics']['coordination_efficiency']
        print(f"📈 Coordination Efficiency: {efficiency:.1%}")
        
        print(f"✅ Swarm coordination cycle completed")
        
    except Exception as e:
        logger.error(f"Error in swarm coordination cycle: {e}")
        print(f"❌ Error: {e}")
    finally:
        await swarm.close()

def main():
    parser = argparse.ArgumentParser(description="Swarm Intelligence Coordination Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Get swarm status")
    
    # Propose decision command
    propose_parser = subparsers.add_parser("propose", help="Propose a new decision")
    propose_parser.add_argument("--agent", required=True, help="Agent ID proposing the decision")
    propose_parser.add_argument("--type", required=True, help="Decision type")
    propose_parser.add_argument("--title", required=True, help="Decision title")
    propose_parser.add_argument("--description", required=True, help="Decision description")
    
    # Cast vote command
    vote_parser = subparsers.add_parser("vote", help="Cast vote on a decision")
    vote_parser.add_argument("--agent", required=True, help="Agent ID casting the vote")
    vote_parser.add_argument("--decision", required=True, help="Decision ID")
    vote_parser.add_argument("--vote", required=True, choices=["yes", "no", "abstain"], help="Vote choice")
    
    # Coordination cycle command
    cycle_parser = subparsers.add_parser("cycle", help="Run swarm coordination cycle")
    
    args = parser.parse_args()
    
    if args.command == "status":
        asyncio.run(get_swarm_status())
    elif args.command == "propose":
        asyncio.run(propose_decision(args.agent, args.type, args.title, args.description))
    elif args.command == "vote":
        asyncio.run(cast_vote(args.agent, args.decision, args.vote))
    elif args.command == "cycle":
        asyncio.run(run_swarm_coordination_cycle())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


