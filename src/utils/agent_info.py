"""
Agent Information Module - Agent Role Definitions

This module contains agent role definitions and information structures.
Follows Single Responsibility Principle - only manages agent metadata.

Architecture: Single Responsibility Principle - agent information only
LOC: 150 lines (under 200 limit)
"""

from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class AgentRole(Enum):
    """Agent role types"""
    SYSTEM_COORDINATOR = "System Coordinator & Project Manager"
    TECHNICAL_ARCHITECT = "Technical Architect & Developer"
    DATA_ENGINEER = "Data Engineer & Analytics Specialist"
    DEVOPS_ENGINEER = "DevOps Engineer & Infrastructure Specialist"
    AI_ML_ENGINEER = "AI/ML Engineer & Algorithm Specialist"
    FRONTEND_DEVELOPER = "Frontend Developer & UI/UX Specialist"
    BACKEND_DEVELOPER = "Backend Developer & API Specialist"
    QA_SPECIALIST = "Quality Assurance & Testing Specialist"


@dataclass
class AgentResponsibilities:
    """Agent responsibilities structure"""
    role: str
    emoji: str
    key_responsibilities: List[str]
    leadership: str
    onboarding_path: str
    priority_docs: List[str]


class AgentInfoManager:
    """
    Manages agent information and role definitions.
    
    Responsibilities:
    - Provide agent role information
    - Manage agent metadata
    - Support agent lookup operations
    """

    def __init__(self):
        self.agent_info = {
            "Agent-1": AgentResponsibilities(
                role=AgentRole.SYSTEM_COORDINATOR.value,
                emoji="🎯",
                key_responsibilities=[
                    "Project coordination and task assignment",
                    "Progress monitoring and bottleneck identification",
                    "Conflict resolution and team leadership",
                    "Quality assurance and strategic planning"
                ],
                leadership="You are the team leader and coordinator.",
                onboarding_path="D:/repos/Dadudekc/onboarding/README.md",
                priority_docs=[
                    "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
                    "D:/repos/Dadudekc/onboarding/protocols/agent_protocols.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/onboarding_checklist.md"
                ]
            ),
            "Agent-2": AgentResponsibilities(
                role=AgentRole.TECHNICAL_ARCHITECT.value,
                emoji="🏗️",
                key_responsibilities=[
                    "System architecture and technical design",
                    "Code development and implementation",
                    "Technical problem-solving and optimization",
                    "Code review and quality assurance"
                ],
                leadership="You are the technical lead and architect.",
                onboarding_path="D:/repos/Dadudekc/onboarding/README.md",
                priority_docs=[
                    "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/development_standards.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/tools_and_technologies.md"
                ]
            ),
            "Agent-3": AgentResponsibilities(
                role=AgentRole.DATA_ENGINEER.value,
                emoji="📊",
                key_responsibilities=[
                    "Data pipeline development and maintenance",
                    "Data analysis and insights generation",
                    "Database design and optimization",
                    "Data quality assurance and governance"
                ],
                leadership="You are the data and analytics expert.",
                onboarding_path="D:/repos/Dadudekc/onboarding/README.md",
                priority_docs=[
                    "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/development_standards.md",
                    "D:/repos/Dadudekc/onboarding/protocols/workflow_protocols.md"
                ]
            ),
            "Agent-4": AgentResponsibilities(
                role=AgentRole.DEVOPS_ENGINEER.value,
                emoji="⚙️",
                key_responsibilities=[
                    "Infrastructure automation and deployment",
                    "System monitoring and reliability",
                    "Security implementation and compliance",
                    "Performance optimization and scaling"
                ],
                leadership="You are the infrastructure and operations expert.",
                onboarding_path="D:/repos/Dadudekc/onboarding/README.md",
                priority_docs=[
                    "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/tools_and_technologies.md",
                    "D:/repos/Dadudekc/onboarding/protocols/command_reference.md"
                ]
            ),
            "Agent-5": AgentResponsibilities(
                role=AgentRole.AI_ML_ENGINEER.value,
                emoji="🤖",
                key_responsibilities=[
                    "Machine learning model development",
                    "AI algorithm implementation and optimization",
                    "Data preprocessing and feature engineering",
                    "Model evaluation and deployment"
                ],
                leadership="You are the AI and machine learning expert.",
                onboarding_path="D:/repos/Dadudekc/onboarding/README.md",
                priority_docs=[
                    "D:/repos/Dadudekc/onboarding/training_documents/agent_roles_and_responsibilities.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/development_standards.md",
                    "D:/repos/Dadudekc/onboarding/training_documents/best_practices.md"
                ]
            )
        }

    def get_agent_info(self, agent_name: str) -> AgentResponsibilities:
        """Get agent information for the specified agent"""
        return self.agent_info.get(agent_name, AgentResponsibilities(
            role="Team Member",
            emoji="👤",
            key_responsibilities=["General team support and collaboration"],
            leadership="You are a valuable team member.",
            onboarding_path="agent_workspaces/onboarding/README.md",
            priority_docs=[
                "agent_workspaces/onboarding/training_documents/agent_roles_and_responsibilities.md",
                "agent_workspaces/onboarding/training_documents/development_standards.md",
                "agent_workspaces/onboarding/training_documents/best_practices.md"
            ]
        ))

    def get_all_agents(self) -> Dict[str, AgentResponsibilities]:
        """Get all agent information"""
        return self.agent_info.copy()

    def get_agent_role(self, agent_name: str) -> str:
        """Get the role of a specific agent"""
        agent = self.get_agent_info(agent_name)
        return agent.role

    def get_agent_emoji(self, agent_name: str) -> str:
        """Get the emoji of a specific agent"""
        agent = self.get_agent_info(agent_name)
        return agent.emoji


def run_smoke_test():
    """Run basic functionality test for AgentInfoManager"""
    print("🧪 Running AgentInfoManager Smoke Test...")

    try:
        manager = AgentInfoManager()
        
        # Test getting agent info
        agent1 = manager.get_agent_info("Agent-1")
        assert agent1.role == "System Coordinator & Project Manager"
        assert agent1.emoji == "🎯"
        
        # Test getting unknown agent
        unknown = manager.get_agent_info("Unknown")
        assert unknown.role == "Team Member"
        
        # Test getting all agents
        all_agents = manager.get_all_agents()
        assert len(all_agents) == 5
        
        print("✅ AgentInfoManager Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ AgentInfoManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for AgentInfoManager testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Info Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--agent", help="Get info for specific agent")
    parser.add_argument("--list", action="store_true", help="List all agents")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    manager = AgentInfoManager()
    
    if args.agent:
        agent_info = manager.get_agent_info(args.agent)
        print(f"Agent: {args.agent}")
        print(f"Role: {agent_info.role}")
        print(f"Emoji: {agent_info.emoji}")
        print(f"Leadership: {agent_info.leadership}")
        print("Responsibilities:")
        for resp in agent_info.key_responsibilities:
            print(f"  • {resp}")
    elif args.list:
        agents = manager.get_all_agents()
        for name, info in agents.items():
            print(f"{name}: {info.emoji} {info.role}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
