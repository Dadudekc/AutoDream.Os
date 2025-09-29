#!/usr/bin/env python3
"""
Contract Integration for Dynamic Role Assignment
===============================================

Integrates dynamic role assignment with the contract system.
Defines role-based contracts and general cycle protocols.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class GeneralCycle:
    """General cycle definition for all agents."""

    phase: str
    priority: str
    description: str
    role_adaptations: dict[str, dict]


@dataclass
class RoleContract:
    """Role-based contract definition."""

    role: str
    general_cycle: list[GeneralCycle]
    specific_requirements: dict
    performance_metrics: dict
    escalation_procedures: dict


class ContractIntegration:
    """Contract integration for role-based assignments."""

    def __init__(self):
        """Initialize contract integration."""
        self.general_cycle = self._define_general_cycle()
        self.role_contracts = self._load_role_contracts()

    def _define_general_cycle(self) -> list[GeneralCycle]:
        """Define the general cycle that all agents follow."""
        return [
            GeneralCycle(
                phase="CHECK_INBOX",
                priority="CRITICAL",
                description="Scan agent inbox for messages, process role assignments, handle coordination",
                role_adaptations={
                    "INTEGRATION_SPECIALIST": {
                        "focus": "integration_requests, service_notifications",
                        "priority": "CRITICAL",
                    },
                    "QUALITY_ASSURANCE": {
                        "focus": "quality_requests, test_notifications, compliance_alerts",
                        "priority": "CRITICAL",
                    },
                    "SSOT_MANAGER": {
                        "focus": "ssot_violations, configuration_changes, coordination_requests",
                        "priority": "CRITICAL",
                    },
                },
            ),
            GeneralCycle(
                phase="EVALUATE_TASKS",
                priority="HIGH",
                description="Check for available tasks, claim tasks based on current role capabilities",
                role_adaptations={
                    "INTEGRATION_SPECIALIST": {
                        "focus": "integration_tasks, api_development, webhook_setup",
                        "priority": "HIGH",
                    },
                    "QUALITY_ASSURANCE": {
                        "focus": "testing_tasks, quality_reviews, compliance_checks",
                        "priority": "HIGH",
                    },
                    "SSOT_MANAGER": {
                        "focus": "ssot_validation, system_integration, coordination_tasks",
                        "priority": "HIGH",
                    },
                },
            ),
            GeneralCycle(
                phase="EXECUTE_ROLE",
                priority="HIGH",
                description="Execute tasks using current role protocols and behavior adaptations",
                role_adaptations={
                    "INTEGRATION_SPECIALIST": {
                        "focus": "system_integration, api_development, webhook_management",
                        "priority": "HIGH",
                    },
                    "QUALITY_ASSURANCE": {
                        "focus": "test_development, quality_validation, compliance_checking",
                        "priority": "HIGH",
                    },
                    "SSOT_MANAGER": {
                        "focus": "ssot_management, system_coordination, configuration_validation",
                        "priority": "HIGH",
                    },
                },
            ),
            GeneralCycle(
                phase="QUALITY_GATES",
                priority="HIGH",
                description="Enforce V2 compliance, validate SSOT requirements, run role-specific quality checks",
                role_adaptations={
                    "INTEGRATION_SPECIALIST": {
                        "focus": "integration_testing, api_validation, webhook_testing",
                        "priority": "HIGH",
                    },
                    "QUALITY_ASSURANCE": {
                        "focus": "comprehensive_testing, compliance_validation, performance_testing",
                        "priority": "CRITICAL",
                    },
                    "SSOT_MANAGER": {
                        "focus": "ssot_compliance, configuration_consistency, system_integration",
                        "priority": "CRITICAL",
                    },
                },
            ),
            GeneralCycle(
                phase="CYCLE_DONE",
                priority="CRITICAL",
                description="Send CYCLE_DONE message, report completion, prepare for next cycle",
                role_adaptations={
                    "INTEGRATION_SPECIALIST": {
                        "focus": "integration_status, service_health, next_integration_steps",
                        "priority": "CRITICAL",
                    },
                    "QUALITY_ASSURANCE": {
                        "focus": "quality_status, test_results, compliance_status",
                        "priority": "CRITICAL",
                    },
                    "SSOT_MANAGER": {
                        "focus": "ssot_status, system_coordination, configuration_health",
                        "priority": "CRITICAL",
                    },
                },
            ),
        ]

    def _load_role_contracts(self) -> dict[str, RoleContract]:
        """Load role-based contracts from configuration files."""
        contracts = {}
        protocols_dir = Path("config/protocols")

        for protocol_file in protocols_dir.glob("*.json"):
            try:
                with open(protocol_file) as f:
                    role_data = json.load(f)

                # Create role contract from protocol data
                contract = RoleContract(
                    role=role_data["role"],
                    general_cycle=self._adapt_general_cycle_for_role(role_data["role"]),
                    specific_requirements=role_data.get("ssot_requirements", {}),
                    performance_metrics=role_data.get("quality_gates", {}),
                    escalation_procedures=role_data.get("escalation_procedures", {}),
                )

                contracts[role_data["role"]] = contract

            except Exception as e:
                logger.error(f"Failed to load role contract from {protocol_file}: {e}")

        return contracts

    def _adapt_general_cycle_for_role(self, role: str) -> list[GeneralCycle]:
        """Adapt general cycle for specific role."""
        adapted_cycle = []

        for phase in self.general_cycle:
            # Get role-specific adaptations
            role_adaptations = phase.role_adaptations.get(role, {})

            # Create adapted phase
            adapted_phase = GeneralCycle(
                phase=phase.phase,
                priority=role_adaptations.get("priority", phase.priority),
                description=phase.description,
                role_adaptations={role: role_adaptations},
            )

            adapted_cycle.append(adapted_phase)

        return adapted_cycle

    def get_general_cycle(self) -> list[GeneralCycle]:
        """Get the general cycle definition."""
        return self.general_cycle

    def get_role_contract(self, role: str) -> RoleContract | None:
        """Get contract for specific role."""
        return self.role_contracts.get(role)

    def get_role_cycle_adaptations(self, role: str) -> dict[str, dict]:
        """Get cycle adaptations for specific role."""
        contract = self.get_role_contract(role)
        if not contract:
            return {}

        adaptations = {}
        for phase in contract.general_cycle:
            adaptations[phase.phase] = phase.role_adaptations.get(role, {})

        return adaptations

    def validate_role_contract(self, role: str) -> bool:
        """Validate that role contract exists and is complete."""
        contract = self.get_role_contract(role)
        if not contract:
            return False

        # Check required components
        required_phases = [
            "CHECK_INBOX",
            "EVALUATE_TASKS",
            "EXECUTE_ROLE",
            "QUALITY_GATES",
            "CYCLE_DONE",
        ]
        contract_phases = [phase.phase for phase in contract.general_cycle]

        return all(phase in contract_phases for phase in required_phases)

    def get_contract_summary(self, role: str) -> dict:
        """Get summary of role contract."""
        contract = self.get_role_contract(role)
        if not contract:
            return {}

        return {
            "role": contract.role,
            "phases": len(contract.general_cycle),
            "requirements": len(contract.specific_requirements),
            "performance_metrics": len(contract.performance_metrics),
            "escalation_procedures": len(contract.escalation_procedures),
            "is_valid": self.validate_role_contract(role),
        }


def main():
    """Test contract integration."""
    integration = ContractIntegration()

    print("General Cycle Definition:")
    for phase in integration.get_general_cycle():
        print(f"  {phase.phase}: {phase.description} (Priority: {phase.priority})")

    print("\nRole Contracts:")
    for role, contract in integration.role_contracts.items():
        summary = integration.get_contract_summary(role)
        print(
            f"  {role}: {summary['phases']} phases, {summary['requirements']} requirements, Valid: {summary['is_valid']}"
        )

    print("\nRole Cycle Adaptations for INTEGRATION_SPECIALIST:")
    adaptations = integration.get_role_cycle_adaptations("INTEGRATION_SPECIALIST")
    for phase, adaptation in adaptations.items():
        print(f"  {phase}: {adaptation}")


if __name__ == "__main__":
    main()
