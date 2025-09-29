#!/usr/bin/env python3
"""
Agent Validation
================

Agent validation and role management for Agent Devlog Posting Service
V2 Compliant: ≤400 lines, focused validation logic
"""

from typing import Any

from .models import AgentInfo, DevlogStatus, DevlogType


class AgentValidator:
    """Agent validation and role management"""

    def __init__(self):
        """Initialize agent validator"""
        self.agent_roles = self._initialize_agent_roles()
        self.agent_capabilities = self._initialize_agent_capabilities()

    def _initialize_agent_roles(self) -> dict[str, str]:
        """Initialize agent role mapping"""
        return {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist",
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "Operations & Support Specialist",
        }

    def _initialize_agent_capabilities(self) -> dict[str, list[str]]:
        """Initialize agent capabilities"""
        return {
            "Agent-1": [
                "Core system integration",
                "API development",
                "Database management",
                "System architecture",
            ],
            "Agent-2": [
                "System design",
                "Architecture planning",
                "Technical documentation",
                "Design patterns",
            ],
            "Agent-3": [
                "Infrastructure management",
                "DevOps automation",
                "Deployment pipelines",
                "Monitoring systems",
            ],
            "Agent-4": [
                "Quality assurance",
                "Testing frameworks",
                "Code review",
                "Quality metrics",
            ],
            "Agent-5": ["Business intelligence", "Data analysis", "Reporting systems", "Analytics"],
            "Agent-6": [
                "Team coordination",
                "Communication protocols",
                "Project management",
                "Workflow optimization",
            ],
            "Agent-7": [
                "Web development",
                "Frontend frameworks",
                "User interface design",
                "Web technologies",
            ],
            "Agent-8": [
                "Operations support",
                "System maintenance",
                "Troubleshooting",
                "Performance optimization",
            ],
        }

    def validate_agent_flag(self, agent_flag: str) -> bool:
        """Validate agent flag format and range"""
        if not agent_flag.startswith("Agent-"):
            return False

        try:
            agent_number = int(agent_flag[6:])
            return 1 <= agent_number <= 8
        except ValueError:
            return False

    def get_agent_info(self, agent_id: str) -> AgentInfo | None:
        """Get agent information"""
        if not self.validate_agent_flag(agent_id):
            return None

        return AgentInfo(
            agent_id=agent_id,
            role=self.agent_roles.get(agent_id, "Specialist"),
            status="active",
            capabilities=self.agent_capabilities.get(agent_id, []),
            last_active="unknown",
        )

    def get_agent_role(self, agent_id: str) -> str:
        """Get agent role"""
        return self.agent_roles.get(agent_id, "Specialist")

    def get_agent_capabilities(self, agent_id: str) -> list[str]:
        """Get agent capabilities"""
        return self.agent_capabilities.get(agent_id, [])

    def is_captain_agent(self, agent_id: str) -> bool:
        """Check if agent is a captain"""
        return agent_id in ["Agent-4"]  # Agent-4 is the CAPTAIN

    def get_all_agents(self) -> list[str]:
        """Get all valid agent IDs"""
        return list(self.agent_roles.keys())

    def get_agent_by_role(self, role_keyword: str) -> list[str]:
        """Get agents by role keyword"""
        matching_agents = []
        for agent_id, role in self.agent_roles.items():
            if role_keyword.lower() in role.lower():
                matching_agents.append(agent_id)
        return matching_agents

    def validate_action(self, action: str) -> bool:
        """Validate action string"""
        if not action or not isinstance(action, str):
            return False

        # Check for minimum length
        if len(action.strip()) < 3:
            return False

        # Check for maximum length
        if len(action) > 500:
            return False

        return True

    def validate_status(self, status: str) -> bool:
        """Validate status string"""
        valid_statuses = [s.value for s in DevlogStatus]
        return status.lower() in valid_statuses

    def validate_details(self, details: str) -> bool:
        """Validate details string"""
        if not details:
            return True  # Details are optional

        # Check for maximum length
        if len(details) > 2000:
            return False

        return True

    def suggest_devlog_type(self, action: str, status: str) -> DevlogType:
        """Suggest devlog type based on action and status"""
        action_lower = action.lower()
        status_lower = status.lower()

        if "error" in action_lower or "fail" in action_lower or status_lower == "failed":
            return DevlogType.ERROR_REPORT
        elif "test" in action_lower or "testing" in action_lower:
            return DevlogType.TESTING
        elif "coordinate" in action_lower or "team" in action_lower:
            return DevlogType.COORDINATION
        elif "status" in action_lower or "update" in action_lower:
            return DevlogType.STATUS_UPDATE
        else:
            return DevlogType.ACTION

    def get_agent_statistics(self) -> dict[str, Any]:
        """Get agent statistics"""
        return {
            "total_agents": len(self.agent_roles),
            "captain_agents": len([a for a in self.agent_roles.keys() if self.is_captain_agent(a)]),
            "specialist_agents": len(self.agent_roles)
            - len([a for a in self.agent_roles.keys() if self.is_captain_agent(a)]),
            "agent_roles": self.agent_roles,
            "capabilities_summary": {
                agent_id: len(caps) for agent_id, caps in self.agent_capabilities.items()
            },
        }
