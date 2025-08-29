#!/usr/bin/env python3
"""
Status.json Generator for Agents
===============================

This script helps agents generate a personalized status.json file for their workspace.
Run this script to create a status.json file with your contract details.

Usage:
    python generate_status.py --agent Agent-1 --contract-id CONTRACT-ID --title "Contract Title"
"""

import json
import os
import argparse
from datetime import datetime
from pathlib import Path

def generate_status_json(agent_id, contract_id, contract_title, contract_category, points, difficulty, estimated_time):
    """Generate a personalized status.json file for an agent"""
    
    # Create the status data structure
    status_data = {
        "agent_id": agent_id,
        "current_contract": {
            "contract_id": contract_id,
            "title": contract_title,
            "category": contract_category,
            "extra_credit_points": points,
            "difficulty": difficulty,
            "estimated_time": estimated_time
        },
        "progress": {
            "percentage": "0%",
            "current_phase": "Planning",
            "tasks_completed": 0,
            "total_tasks": 0,
            "last_milestone": "Contract claimed"
        },
        "work_status": {
            "status": "IN_PROGRESS",
            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "estimated_completion": f"{datetime.now().strftime('%Y-%m-%d')} {int(datetime.now().hour) + 2}:00:00",
            "actual_completion": None,
            "time_spent": "0 hours"
        },
        "blockers": {
            "current_blockers": [],
            "resolved_blockers": [],
            "escalation_needed": False,
            "escalation_reason": None
        },
        "deliverables": {
            "completed": [],
            "in_progress": [],
            "pending": [
                "Deliverable 1",
                "Deliverable 2", 
                "Deliverable 3"
            ],
            "quality_score": None
        },
        "communication": {
            "last_devlog_update": None,
            "last_inbox_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages_sent": 0,
            "messages_received": 0,
            "coordination_needed": False
        },
        "workspace_health": {
            "files_created": 0,
            "files_modified": 0,
            "files_deleted": 0,
            "workspace_clean": True,
            "last_cleanup": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "quality_metrics": {
            "code_reviews_requested": 0,
            "code_reviews_completed": 0,
            "testing_coverage": "0%",
            "documentation_updated": False,
            "standards_compliance": "PENDING"
        },
        "next_actions": [
            "Review contract requirements",
            "Set up development environment", 
            "Create initial project structure",
            "Begin first deliverable"
        ],
        "notes": f"Status file generated for {agent_id} working on {contract_title}",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0"
    }
    
    return status_data

def save_status_file(agent_id, status_data):
    """Save the status.json file to the agent's workspace"""
    
    # Create agent workspace path
    workspace_path = Path(f"agent_workspaces/{agent_id}")
    status_file_path = workspace_path / "status.json"
    
    # Ensure workspace directory exists
    workspace_path.mkdir(parents=True, exist_ok=True)
    
    # Save status.json file
    with open(status_file_path, 'w', encoding='utf-8') as f:
        json.dump(status_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Status file created: {status_file_path}")
    return status_file_path

def main():
    """Main function to handle command line arguments and generate status file"""
    
    parser = argparse.ArgumentParser(description="Generate personalized status.json for agents")
    parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-1)")
    parser.add_argument("--contract-id", required=True, help="Contract ID (e.g., SSOT-001)")
    parser.add_argument("--title", required=True, help="Contract title")
    parser.add_argument("--category", default="General", help="Contract category")
    parser.add_argument("--points", type=int, default=0, help="Contract points")
    parser.add_argument("--difficulty", default="MEDIUM", help="Contract difficulty")
    parser.add_argument("--estimated-time", default="2-3 hours", help="Estimated completion time")
    
    args = parser.parse_args()
    
    print(f"🚀 Generating status.json for {args.agent}")
    print(f"📋 Contract: {args.contract_id} - {args.title}")
    print(f"💎 Points: {args.points}")
    print(f"⏰ Estimated Time: {args.estimated_time}")
    
    # Generate status data
    status_data = generate_status_json(
        agent_id=args.agent,
        contract_id=args.contract_id,
        contract_title=args.title,
        contract_category=args.category,
        points=args.points,
        difficulty=args.difficulty,
        estimated_time=args.estimated_time
    )
    
    # Save status file
    status_file_path = save_status_file(args.agent, status_data)
    
    print(f"\n📁 Status file saved to: {status_file_path}")
    print(f"🔧 Next steps:")
    print(f"   1. Review the generated status.json file")
    print(f"   2. Update progress as you work on your contract")
    print(f"   3. Use devlog system: python -m src.core.devlog_cli --add 'Your progress message'")
    print(f"   4. Check your inbox regularly for messages")
    print(f"   5. Keep workspace clean and organized")
    
    print(f"\n🎯 Good luck with your contract: {args.title}!")

if __name__ == "__main__":
    main()
