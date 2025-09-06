#!/usr/bin/env python3
"""
Contract Service - Agent Cellphone V2
====================================

Dedicated service for contract management and task assignment.
Extracted from messaging_cli.py to maintain LOC compliance.

Author: V2 SWARM CAPTAIN
License: MIT
"""


class ContractService:
    """Dedicated service for contract operations."""

    def __init__(self, lock_config: Optional[LockConfig] = None):
        """Initialize contract service."""
        self.contracts = self._get_contract_definitions()
        self.lock_manager = FileLockManager(lock_config)

    def _get_contract_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Get contract definitions from SSOT."""
        return {
            "Agent-5": {
                "name": "V2 Compliance Business Intelligence Analysis",
                "category": "Business Intelligence",
                "priority": "HIGH",
                "points": 425,
                "description": (
                    "Analyze business intelligence systems for V2 compliance optimization"
                ),
            },
            "Agent-7": {
                "name": "Web Development V2 Compliance Implementation",
                "category": "Web Development",
                "priority": "HIGH",
                "points": 685,
                "description": (
                    "Implement V2 compliance for web development components and systems"
                ),
            },
            "Agent-1": {
                "name": "Integration & Core Systems V2 Compliance",
                "category": "Integration & Core Systems",
                "priority": "HIGH",
                "points": 600,
                "description": (
                    "Implement V2 compliance for integration and core systems"
                ),
            },
            "Agent-2": {
                "name": "Architecture & Design V2 Compliance",
                "category": "Architecture & Design",
                "priority": "HIGH",
                "points": 550,
                "description": (
                    "Implement V2 compliance for architecture and design systems"
                ),
            },
            "Agent-3": {
                "name": "Infrastructure & DevOps V2 Compliance",
                "category": "Infrastructure & DevOps",
                "priority": "HIGH",
                "points": 575,
                "description": (
                    "Implement V2 compliance for infrastructure and DevOps systems"
                ),
            },
            "Agent-6": {
                "name": "Coordination & Communication V2 Compliance",
                "category": "Coordination & Communication",
                "priority": "HIGH",
                "points": 500,
                "description": (
                    "Implement V2 compliance for coordination and communication systems"
                ),
            },
            "Agent-8": {
                "name": "SSOT Maintenance & System Integration V2 Compliance",
                "category": "SSOT & System Integration",
                "priority": "HIGH",
                "points": 650,
                "description": (
                    "Implement V2 compliance for SSOT maintenance and system integration"
                ),
            },
        }

    def get_contract(self, agent_id: str) -> Dict[str, Any]:
        """Get contract for specific agent."""
        return self.contracts.get(agent_id)

    def display_contract_assignment(
        self, agent_id: str, contract: Dict[str, Any]
    ) -> None:
        """Display contract assignment details."""
        get_logger(__name__).info(f"✅ CONTRACT ASSIGNED: {contract['name']}")
        get_logger(__name__).info(f"📋 Category: {contract['category']}")
        get_logger(__name__).info(f"🎯 Priority: {contract['priority']}")
        get_logger(__name__).info(f"⭐ Points: {contract['points']}")
        get_logger(__name__).info(f"📝 Description: {contract['description']}")
        get_logger(__name__).info()
        get_logger(__name__).info("🚀 IMMEDIATE ACTIONS REQUIRED:")
        get_logger(__name__).info("1. Begin task execution immediately")
        get_logger(__name__).info("2. Maintain V2 compliance standards")
        get_logger(__name__).info("3. Provide daily progress reports via inbox")
        get_logger(__name__).info("4. Coordinate with other agents as needed")
        get_logger(__name__).info()
        get_logger(__name__).info("📧 Send status updates to Captain Agent-4 via inbox")
        get_logger(__name__).info("⚡ WE. ARE. SWARM.")

    def check_agent_status(self) -> None:
        """Check and display status of all agents."""
        get_logger(__name__).info("📊 AGENT STATUS & CONTRACT AVAILABILITY")
        get_logger(__name__).info("=" * 50)

        # Check agent status files
        agent_workspaces = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
            "Agent-4",
        ]

        for agent_id in agent_workspaces:
            status_file = f"agent_workspaces/{agent_id}/status.json"
            if get_unified_utility().path.exists(status_file):
                try:
                    # Use direct file reading instead of atomic_read to avoid lock issues
                    with open(status_file, "r", encoding="utf-8") as f:
                        status_content = f.read()

                    if status_content:
                        status = json.loads(status_content)
                        get_logger(__name__).info(
                            f"✅ {agent_id}: {status.get('status', 'UNKNOWN')} - {status.get('current_mission', 'No mission')}"
                        )
                    else:
                        get_logger(__name__).info(
                            f"⚠️ {agent_id}: Status file exists but is empty"
                        )
                except Exception as e:
                    get_logger(__name__).info(
                        f"⚠️ {agent_id}: Status file exists but unreadable - {str(e)}"
                    )
            else:
                get_logger(__name__).info(f"❌ {agent_id}: No status file found")

        get_logger(__name__).info()
        get_logger(__name__).info("🎯 CONTRACT SYSTEM STATUS: READY FOR ASSIGNMENT")
        get_logger(__name__).info(
            "📋 Available contracts: 40+ contracts across all categories"
        )
        get_logger(__name__).info(
            "🚀 Use --get-next-task with --agent to claim assignments"
        )
