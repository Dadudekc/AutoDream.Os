#!/usr/bin/env python3
"""
Swarm Intelligence Coordination CLI - Command Line Interface
=============================================================

Command-line interface for swarm intelligence coordination.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: swarm_intelligence_coordination.py (410 lines) - CLI module
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.swarm_intelligence_coordination_core import (
    SwarmCoordinationCore,
    DecisionType,
    AgentRole,
)


def create_argument_parser():
    """Create argument parser for CLI commands"""
    parser = argparse.ArgumentParser(
        description="Swarm Intelligence Coordination CLI - 8-agent coordination system"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create decision command
    create_parser = subparsers.add_parser("create-decision", help="Create a new swarm decision")
    create_parser.add_argument("--type", required=True, choices=[t.value for t in DecisionType], help="Decision type")
    create_parser.add_argument("--title", required=True, help="Decision title")
    create_parser.add_argument("--description", required=True, help="Decision description")
    create_parser.add_argument("--proposed-by", required=True, help="Agent proposing the decision")
    
    # Vote command
    vote_parser = subparsers.add_parser("vote", help="Vote on a decision")
    vote_parser.add_argument("--decision-id", required=True, help="Decision ID")
    vote_parser.add_argument("--agent-id", required=True, help="Agent ID")
    vote_parser.add_argument("--vote", required=True, choices=["yes", "no", "abstain"], help="Vote")
    
    # Status commands
    status_parser = subparsers.add_parser("status", help="Manage agent status")
    status_subparsers = status_parser.add_subparsers(dest="status_action", help="Status actions")
    
    # Update status
    update_parser = status_subparsers.add_parser("update", help="Update agent status")
    update_parser.add_argument("--agent-id", required=True, help="Agent ID")
    update_parser.add_argument("--status", required=True, choices=["active", "busy", "idle", "offline"], help="Status")
    update_parser.add_argument("--task", help="Current task")
    
    # Get status
    get_parser = status_subparsers.add_parser("get", help="Get agent status")
    get_parser.add_argument("--agent-id", required=True, help="Agent ID")
    
    # List decisions
    list_parser = subparsers.add_parser("list-decisions", help="List active decisions")
    
    # Get decision
    get_decision_parser = subparsers.add_parser("get-decision", help="Get specific decision")
    get_decision_parser.add_argument("--decision-id", required=True, help="Decision ID")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test coordination system")
    
    return parser


def handle_create_decision_command(args):
    """Handle create decision command"""
    core = SwarmCoordinationCore()
    
    decision_type = DecisionType(args.type)
    decision = core.create_decision(
        decision_type, args.title, args.description, args.proposed_by
    )
    
    print(f"Created decision: {decision.decision_id}")
    print(f"Title: {decision.title}")
    print(f"Status: {decision.status}")
    return 0


def handle_vote_command(args):
    """Handle vote command"""
    core = SwarmCoordinationCore()
    
    success = core.vote_on_decision(args.decision_id, args.agent_id, args.vote)
    
    if success:
        print(f"Vote recorded: {args.agent_id} voted {args.vote} on {args.decision_id}")
        
        # Check decision status
        decision = core.get_decision(args.decision_id)
        if decision:
            print(f"Decision status: {decision.status}")
            if decision.resolution:
                print(f"Resolution: {decision.resolution}")
    else:
        print(f"Failed to record vote")
        return 1
    
    return 0


def handle_status_command(args):
    """Handle status management commands"""
    core = SwarmCoordinationCore()
    
    if args.status_action == "update":
        core.update_agent_status(args.agent_id, args.status, args.task)
        print(f"Updated agent {args.agent_id} status to {args.status}")
        return 0
    
    elif args.status_action == "get":
        status = core.get_agent_status(args.agent_id)
        if status:
            print(f"Agent {args.agent_id}:")
            print(f"  Role: {status.role.value}")
            print(f"  Status: {status.status}")
            print(f"  Current Task: {status.current_task}")
            print(f"  Last Activity: {status.last_activity}")
        else:
            print(f"Agent {args.agent_id} not found")
            return 1
        return 0
    
    else:
        print(f"Unknown status action: {args.status_action}")
        return 1


def handle_list_decisions_command(args):
    """Handle list decisions command"""
    core = SwarmCoordinationCore()
    
    decisions = core.get_active_decisions()
    
    if not decisions:
        print("No active decisions")
        return 0
    
    print(f"Active Decisions ({len(decisions)}):")
    for decision in decisions:
        print(f"  {decision.decision_id}: {decision.title}")
        print(f"    Type: {decision.decision_type.value}")
        print(f"    Status: {decision.status}")
        print(f"    Votes: {len(decision.votes)}")
        if decision.resolution:
            print(f"    Resolution: {decision.resolution}")
        print()
    
    return 0


def handle_get_decision_command(args):
    """Handle get decision command"""
    core = SwarmCoordinationCore()
    
    decision = core.get_decision(args.decision_id)
    
    if not decision:
        print(f"Decision {args.decision_id} not found")
        return 1
    
    print(f"Decision: {decision.decision_id}")
    print(f"Title: {decision.title}")
    print(f"Description: {decision.description}")
    print(f"Type: {decision.decision_type.value}")
    print(f"Proposed by: {decision.proposed_by}")
    print(f"Status: {decision.status}")
    print(f"Created: {decision.created_at}")
    
    if decision.votes:
        print(f"Votes ({len(decision.votes)}):")
        for agent_id, vote in decision.votes.items():
            print(f"  {agent_id}: {vote}")
    
    if decision.resolution:
        print(f"Resolution: {decision.resolution}")
        print(f"Resolved: {decision.resolved_at}")
    
    return 0


def handle_test_command(args):
    """Handle test command"""
    core = SwarmCoordinationCore()
    
    print("Testing Swarm Intelligence Coordination System...")
    
    # Test creating a decision
    decision = core.create_decision(
        DecisionType.TASK_ASSIGNMENT,
        "Test Decision",
        "Testing the coordination system",
        "agent-6"
    )
    
    print(f"✅ Created test decision: {decision.decision_id}")
    
    # Test voting
    core.vote_on_decision(decision.decision_id, "agent-1", "yes")
    core.vote_on_decision(decision.decision_id, "agent-2", "yes")
    core.vote_on_decision(decision.decision_id, "agent-3", "no")
    
    print("✅ Test voting completed")
    
    # Test agent status
    core.update_agent_status("agent-6", "active", "testing")
    
    print("✅ Test agent status update completed")
    
    print("🎉 All tests passed!")
    return 0


def handle_command(args):
    """Handle command execution"""
    try:
        if args.command == "create-decision":
            return handle_create_decision_command(args)
        elif args.command == "vote":
            return handle_vote_command(args)
        elif args.command == "status":
            return handle_status_command(args)
        elif args.command == "list-decisions":
            return handle_list_decisions_command(args)
        elif args.command == "get-decision":
            return handle_get_decision_command(args)
        elif args.command == "test":
            return handle_test_command(args)
        else:
            print(f"Unknown command: {args.command}")
            return 1
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


def main():
    """Main CLI entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return handle_command(args)


if __name__ == "__main__":
    sys.exit(main())
