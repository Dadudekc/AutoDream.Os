#!/usr/bin/env python3
"""
Multi-Agent Project File Planning System - V2 Compliant
======================================================

Coordinates all 5 agents to create a comprehensive plan for essential project files.
Uses debate system and messaging system for coordination.

Author: Agent-4 (Captain)
License: MIT
"""

import json
import os
from pathlib import Path
from datetime import datetime


def create_planning_framework():
    """Create a comprehensive planning framework for all agents."""
    
    planning_framework = {
        "session_id": f"FILE_PLANNING_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "created_by": "Agent-4",
        "created_at": datetime.now().isoformat(),
        "objective": "Determine essential project files for inter-agent coordination",
        "current_state": {
            "total_files": 11977,
            "total_directories": 554,
            "target_files": 500,
            "reduction_percentage": 95.8
        },
        "agent_roles": {
            "Agent-4": {
                "role": "Captain",
                "responsibility": "Overall coordination and final decision making",
                "focus": "Strategic planning and agent coordination"
            },
            "Agent-5": {
                "role": "Coordinator", 
                "responsibility": "Lead multi-agent planning session",
                "focus": "Coordination protocols and workflow management"
            },
            "Agent-6": {
                "role": "Quality Agent",
                "responsibility": "V2 compliance and quality standards",
                "focus": "File size limits (≤400 lines), quality gates, compliance"
            },
            "Agent-7": {
                "role": "Implementation Agent",
                "responsibility": "Core system files and essential functionality",
                "focus": "Implementation requirements and system architecture"
            },
            "Agent-8": {
                "role": "SSOT Manager",
                "responsibility": "Single source of truth and data integrity",
                "focus": "System integration and data consistency"
            }
        },
        "planning_categories": {
            "essential_core": {
                "description": "Core system files absolutely required for inter-agent coordination",
                "target_count": 100,
                "examples": ["src/core/", "src/services/consolidated_messaging_service.py", "agent_workspaces/"]
            },
            "agent_coordination": {
                "description": "Files needed for agent-to-agent communication and coordination",
                "target_count": 50,
                "examples": ["src/services/messaging/", "tools/send_message.py", "config/coordinates.json"]
            },
            "documentation": {
                "description": "Essential documentation for system understanding",
                "target_count": 50,
                "examples": ["docs/CAPTAINS_HANDBOOK.md", "docs/modules/", "README.md"]
            },
            "tools_utilities": {
                "description": "Tools and utilities for system operation",
                "target_count": 100,
                "examples": ["tools/", "scripts/", "quality_gates.py"]
            },
            "configuration": {
                "description": "Configuration files for system operation",
                "target_count": 50,
                "examples": ["config/", ".env", "pyproject.toml"]
            },
            "debatable": {
                "description": "Files that need agent discussion and debate",
                "target_count": 150,
                "examples": ["src/ml/", "swarm_brain/", "browser_service/"]
            }
        },
        "coordination_methods": {
            "debate_system": {
                "description": "Use debate system for complex decisions",
                "when_to_use": "When agents disagree on file necessity",
                "process": "Present arguments, vote, reach consensus"
            },
            "messaging_system": {
                "description": "Use messaging system for coordination",
                "when_to_use": "For ongoing coordination and updates",
                "process": "Send messages, receive responses, coordinate actions"
            },
            "collaborative_planning": {
                "description": "Collaborative planning session",
                "when_to_use": "For initial planning and framework creation",
                "process": "All agents contribute to planning document"
            }
        },
        "success_criteria": {
            "file_reduction": "Reduce from 11,977 to ~500 files (95.8% reduction)",
            "directory_reduction": "Reduce from 554 to ~50 directories",
            "maintainability": "System must be easy to navigate and understand",
            "functionality": "All essential inter-agent coordination must work",
            "quality": "All remaining files must meet V2 compliance standards"
        },
        "next_steps": [
            "Agent-5 leads multi-agent planning session",
            "All agents contribute to planning framework",
            "Use debate system for complex decisions",
            "Create final file list with agent consensus",
            "Execute cleanup based on agreed plan"
        ]
    }
    
    return planning_framework


def create_agent_specific_plans(framework):
    """Create specific planning documents for each agent."""
    
    agents = ["Agent-5", "Agent-6", "Agent-7", "Agent-8"]
    agent_plans = {}
    
    for agent in agents:
        agent_plan = {
            "agent": agent,
            "role": framework["agent_roles"][agent]["role"],
            "responsibility": framework["agent_roles"][agent]["responsibility"],
            "focus": framework["agent_roles"][agent]["focus"],
            "assigned_categories": [],
            "specific_tasks": [],
            "coordination_methods": framework["coordination_methods"],
            "success_criteria": framework["success_criteria"]
        }
        
        # Assign specific categories based on agent role
        if agent == "Agent-5":  # Coordinator
            agent_plan["assigned_categories"] = ["agent_coordination", "coordination_methods"]
            agent_plan["specific_tasks"] = [
                "Lead multi-agent planning session",
                "Coordinate with all agents via messaging system",
                "Facilitate debate system for complex decisions",
                "Create final consensus plan"
            ]
        elif agent == "Agent-6":  # Quality Agent
            agent_plan["assigned_categories"] = ["essential_core", "quality_standards"]
            agent_plan["specific_tasks"] = [
                "Review all files for V2 compliance",
                "Identify files exceeding 400 lines",
                "Ensure quality gates are met",
                "Validate file necessity from quality perspective"
            ]
        elif agent == "Agent-7":  # Implementation Agent
            agent_plan["assigned_categories"] = ["essential_core", "tools_utilities"]
            agent_plan["specific_tasks"] = [
                "Identify core system files",
                "Review implementation requirements",
                "Assess tools and utilities necessity",
                "Validate system architecture needs"
            ]
        elif agent == "Agent-8":  # SSOT Manager
            agent_plan["assigned_categories"] = ["configuration", "debatable"]
            agent_plan["specific_tasks"] = [
                "Review configuration files",
                "Analyze debatable directories (src/ml/, swarm_brain/, browser_service/)",
                "Ensure single source of truth",
                "Validate data integrity requirements"
            ]
        
        agent_plans[agent] = agent_plan
    
    return agent_plans


def main():
    """Main execution function."""
    print("🚀 Starting multi-agent project file planning system...")
    
    # Create planning framework
    framework = create_planning_framework()
    
    # Create agent-specific plans
    agent_plans = create_agent_specific_plans(framework)
    
    # Save planning documents
    with open('MULTI_AGENT_FILE_PLANNING_FRAMEWORK.json', 'w') as f:
        json.dump(framework, f, indent=2)
    
    for agent, plan in agent_plans.items():
        with open(f'{agent}_FILE_PLANNING_TASKS.json', 'w') as f:
            json.dump(plan, f, indent=2)
    
    print(f"\n✅ Multi-agent planning framework created!")
    print(f"  📋 Framework: MULTI_AGENT_FILE_PLANNING_FRAMEWORK.json")
    print(f"  👥 Agent plans: {len(agent_plans)} agent-specific plans")
    print(f"  🎯 Objective: Reduce from {framework['current_state']['total_files']:,} to {framework['current_state']['target_files']} files")
    print(f"  📊 Reduction target: {framework['current_state']['reduction_percentage']}%")
    
    print(f"\n🎯 Next steps:")
    print(f"  1. Agent-5 leads multi-agent planning session")
    print(f"  2. All agents contribute to planning framework")
    print(f"  3. Use debate system for complex decisions")
    print(f"  4. Create final file list with agent consensus")
    print(f"  5. Execute cleanup based on agreed plan")
    
    return framework, agent_plans


if __name__ == "__main__":
    main()
