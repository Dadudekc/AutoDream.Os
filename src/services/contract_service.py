#!/usr/bin/env python3
"""
Contract Service - Agent Cellphone V2
====================================

SOLID-compliant contract management service.
Refactored to follow Single Responsibility, Open-Closed, and Dependency Inversion principles.

Author: Agent-6 (SOLID Sentinel)
License: MIT
"""

import os
import json
from typing import Dict, Any, Protocol, Optional
from abc import ABC, abstractmethod

# DIP: Define abstraction for contract storage
class IContractStorage(Protocol):
    """Interface for contract storage operations."""
    def save_contract(self, agent_id: str, contract_data: Dict[str, Any]) -> bool:
        """Save contract data."""
        ...

    def load_contract(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Load contract data."""
        ...

    def list_contracts(self) -> Dict[str, Dict[str, Any]]:
        """List all contracts."""
        ...


# SRP: Separate contract definitions
class ContractDefinitions:
    """Responsible for contract definitions only."""

    @staticmethod
    def get_contract_definitions() -> Dict[str, Dict[str, Any]]:
        """Get contract definitions from SSOT."""
        return {
            "Agent-5": {
                "name": "V2 Compliance Business Intelligence Analysis",
                "category": "Business Intelligence",
                "priority": "HIGH",
                "points": 425,
                "description": "Analyze business intelligence systems for V2 compliance optimization"
            },
            "Agent-7": {
                "name": "Web Development V2 Compliance Implementation",
                "category": "Web Development",
                "priority": "HIGH",
                "points": 685,
                "description": "Implement V2 compliance for web development components and systems"
            },
            "Agent-1": {
                "name": "Integration & Core Systems V2 Compliance",
                "category": "Integration & Core Systems",
                "priority": "HIGH",
                "points": 600,
                "description": "Implement V2 compliance for integration and core systems"
            },
            "Agent-2": {
                "name": "Architecture & Design V2 Compliance",
                "category": "Architecture & Design",
                "priority": "HIGH",
                "points": 550,
                "description": "Implement V2 compliance for architecture and design systems"
            },
            "Agent-3": {
                "name": "Infrastructure & DevOps V2 Compliance",
                "category": "Infrastructure & DevOps",
                "priority": "HIGH",
                "points": 575,
                "description": "Implement V2 compliance for infrastructure and DevOps systems"
            },
            "Agent-6": {
                "name": "Coordination & Communication V2 Compliance",
                "category": "Coordination & Communication",
                "priority": "HIGH",
                "points": 500,
                "description": "Implement V2 compliance for coordination and communication systems"
            },
            "Agent-8": {
                "name": "SSOT Maintenance & System Integration V2 Compliance",
                "category": "SSOT & System Integration",
                "priority": "HIGH",
                "points": 650,
                "description": "Implement V2 compliance for SSOT maintenance and system integration"
            }
        }


# SRP: Separate status checking
class AgentStatusChecker:
    """Responsible for checking agent status only."""

    def check_agent_status(self) -> None:
        """Check and display status of all agents."""
        print("📊 AGENT STATUS & CONTRACT AVAILABILITY")
        print("=" * 50)

        # Check agent status files
        agent_workspaces = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-5",
            "Agent-6", "Agent-7", "Agent-8", "Agent-4"
        ]

        for agent_id in agent_workspaces:
            status_file = f"agent_workspaces/{agent_id}/status.json"
            if os.path.exists(status_file):
                try:
                    with open(status_file, 'r') as f:
                        status = json.load(f)
                    print(f"✅ {agent_id}: {status.get('status', 'UNKNOWN')} - {status.get('current_mission', 'No mission')}")
                except:
                    print(f"⚠️ {agent_id}: Status file exists but unreadable")
            else:
                print(f"❌ {agent_id}: No status file found")

        print()
        print("🎯 CONTRACT SYSTEM STATUS: READY FOR ASSIGNMENT")
        print("📋 Available contracts: 40+ contracts across all categories")
        print("🚀 Use --get-next-task with --agent to claim assignments")


# SRP: Separate contract display
class ContractDisplay:
    """Responsible for displaying contract information only."""

    def display_contract_assignment(self, agent_id: str, contract: Dict[str, Any]) -> None:
        """Display contract assignment details."""
        print(f"✅ CONTRACT ASSIGNED: {contract['name']}")
        print(f"📋 Category: {contract['category']}")
        print(f"🎯 Priority: {contract['priority']}")
        print(f"⭐ Points: {contract['points']}")
        print(f"📝 Description: {contract['description']}")
        print()
        print("🚀 IMMEDIATE ACTIONS REQUIRED:")
        print("1. Begin task execution immediately")
        print("2. Maintain V2 compliance standards")
        print("3. Provide daily progress reports via inbox")
        print("4. Coordinate with other agents as needed")
        print()
        print("📧 Send status updates to Captain Agent-4 via inbox")
        print("⚡ WE. ARE. SWARM.")


# DIP: Depends on abstraction, not concrete storage
class ContractService:
    """SOLID-compliant contract service with dependency injection."""

    def __init__(self, storage: Optional[IContractStorage] = None):
        """Initialize contract service with dependency injection."""
        self.contract_definitions = ContractDefinitions()
        self.contracts = self.contract_definitions.get_contract_definitions()
        self.storage = storage  # DIP: Depend on abstraction
        self.status_checker = AgentStatusChecker()
        self.display = ContractDisplay()

    # SRP: Contract service methods delegate to specialized classes
    def get_contract(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get contract for specific agent."""
        return self.contracts.get(agent_id)

    def display_contract_assignment(self, agent_id: str, contract: Dict[str, Any]) -> None:
        """Display contract assignment details."""
        self.display.display_contract_assignment(agent_id, contract)

    def check_agent_status(self) -> None:
        """Check and display status of all agents."""
        self.status_checker.check_agent_status()

    # OCP: Open for extension through storage abstraction
    def save_contract(self, agent_id: str, contract_data: Dict[str, Any]) -> bool:
        """Save contract data using injected storage."""
        if self.storage:
            return self.storage.save_contract(agent_id, contract_data)
        # Default implementation
        return True

    def load_contract(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Load contract data using injected storage."""
        if self.storage:
            return self.storage.load_contract(agent_id)
        return self.get_contract(agent_id)

    def list_all_contracts(self) -> Dict[str, Dict[str, Any]]:
        """List all available contracts."""
        if self.storage:
            return self.storage.list_contracts()
        return self.contracts
