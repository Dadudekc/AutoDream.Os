#!/usr/bin/env python3
"""
Consolidated Contract Manager - V2 Core Contract Management System

This module consolidates all contract management functionality into a single,
comprehensive system. Eliminates duplication from:
- contract_manager.py (original - contract assignment)
- unified_contract_manager.py (unified contract operations)

Follows Single Responsibility Principle - unified contract management.
Architecture: Consolidated single responsibility - all contract operations
LOC: Consolidated from 1,068 lines to ~700 lines (35% reduction)
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Set, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import threading
import time
import uuid
from collections import defaultdict

from .agent_manager import AgentManager, AgentStatus, AgentCapability, AgentInfo
from .config_manager import ConfigManager

logger = logging.getLogger(__name__)


class ContractPriority(Enum):
    """Contract priority levels"""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class ContractStatus(Enum):
    """Contract status"""

    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    APPROVED = "approved"  # Added from unified contract manager


class AssignmentStrategy(Enum):
    """Contract assignment strategies"""

    SKILL_MATCH = "skill_match"
    LOAD_BALANCE = "load_balance"
    PRIORITY_FIRST = "priority_first"
    ROUND_ROBIN = "round_robin"
    EXPERT_OPINION = "expert_opinion"


class ContractType(Enum):
    """Contract types - added from unified contract manager"""

    TASK_ASSIGNMENT = "task_assignment"
    AGENT_RESPONSE = "agent_response"
    COLLABORATION = "collaboration"
    SERVICE_AGREEMENT = "service_agreement"


@dataclass
class Contract:
    """Contract definition - enhanced from original"""

    contract_id: str
    title: str
    description: str
    priority: ContractPriority
    status: ContractStatus
    required_capabilities: List[AgentCapability]
    estimated_duration: int  # hours
    assigned_agent: Optional[str]
    created_at: str
    assigned_at: Optional[str]
    completed_at: Optional[str]
    metadata: Dict[str, Any]
    # Additional fields from unified contract manager
    contract_type: Optional[ContractType] = None
    parties: Optional[List[Dict[str, Any]]] = None
    terms: Optional[Dict[str, Any]] = None
    validation_results: Optional[List[Any]] = None


@dataclass
class AssignmentResult:
    """Contract assignment result"""

    assignment_id: str
    contract_id: str
    agent_id: str
    strategy: AssignmentStrategy
    confidence_score: float
    assignment_timestamp: str
    metadata: Dict[str, Any]


@dataclass
class ContractTemplate:
    """Contract template for standardized contracts"""

    template_id: str
    name: str
    description: str
    contract_type: ContractType
    default_terms: Dict[str, Any]
    required_fields: List[str]
    validation_rules: Dict[str, Any]
    created_at: str
    updated_at: str


class ContractValidator:
    """Validates contract data and structure"""

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ContractValidator")

    def validate_contract(self, contract_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Validate contract data and return validation results"""
        validation_results = []

        try:
            # Required field validation
            required_fields = [
                "title",
                "description",
                "priority",
                "required_capabilities",
            ]
            for field in required_fields:
                if field not in contract_data or not contract_data[field]:
                    validation_results.append(
                        {
                            "field": field,
                            "issue": f"Required field '{field}' is missing or empty",
                            "severity": "critical",
                            "passed": False,
                        }
                    )

            # Priority validation
            if "priority" in contract_data:
                try:
                    ContractPriority(contract_data["priority"])
                except ValueError:
                    validation_results.append(
                        {
                            "field": "priority",
                            "issue": f"Invalid priority value: {contract_data['priority']}",
                            "severity": "critical",
                            "passed": False,
                        }
                    )

            # Capabilities validation
            if "required_capabilities" in contract_data:
                capabilities = contract_data["required_capabilities"]
                if not isinstance(capabilities, list) or len(capabilities) == 0:
                    validation_results.append(
                        {
                            "field": "required_capabilities",
                            "issue": "Required capabilities must be a non-empty list",
                            "severity": "critical",
                            "passed": False,
                        }
                    )

            # If no critical issues found, mark as passed
            if not any(
                r["severity"] == "critical" and not r["passed"]
                for r in validation_results
            ):
                validation_results.append(
                    {
                        "field": "overall",
                        "issue": "Contract validation passed",
                        "severity": "info",
                        "passed": True,
                    }
                )

        except Exception as e:
            validation_results.append(
                {
                    "field": "validation_error",
                    "issue": f"Validation error: {str(e)}",
                    "severity": "critical",
                    "passed": False,
                }
            )

        return validation_results


class ContractManager:
    """
    Consolidated Contract Manager - All contract functionality in one place

    Responsibilities (consolidated from both sources):
    - Intelligent contract-to-agent matching (from original)
    - Load balancing and work distribution (from original)
    - Priority management and urgent handling (from original)
    - Resource optimization and efficiency (from original)
    - Contract lifecycle management (from unified contract manager)
    - Contract validation and enforcement (from unified contract manager)
    - Legacy contract migration (from unified contract manager)
    - Contract analytics and reporting (from unified contract manager)
    """

    def __init__(
        self,
        agent_manager: AgentManager,
        config_manager: ConfigManager,
        legacy_contracts_path: Optional[str] = None,
    ):
        self.agent_manager = agent_manager
        self.config_manager = config_manager

        # Core contract data
        self.contracts: Dict[str, Contract] = {}
        self.assignments: Dict[str, AssignmentResult] = {}
        self.assignment_history: List[AssignmentResult] = []

        # Enhanced functionality from unified contract manager
        self.contract_templates: Dict[str, ContractTemplate] = {}
        self.contract_analytics: Dict[str, Any] = {}
        self.system_status: Dict[str, Any] = {}

        # Legacy contract migration
        self.legacy_contracts_path = (
            legacy_contracts_path or "Agent_Cellphone/CONTRACTS"
        )

        # Validation system
        self.validator = ContractValidator()

        # Assignment strategy weights
        self.strategy_weights = {
            AssignmentStrategy.SKILL_MATCH: 0.4,
            AssignmentStrategy.LOAD_BALANCE: 0.3,
            AssignmentStrategy.PRIORITY_FIRST: 0.2,
            AssignmentStrategy.EXPERT_OPINION: 0.1,
        }

        self.running = False
        self.logger = logging.getLogger(f"{__name__}.ContractManager")

        # Load existing contracts and templates
        self._load_contract_templates()
        self._load_legacy_contracts()

    def _load_contract_templates(self):
        """Load contract templates for standardized contracts"""
        try:
            # Initialize default templates
            default_templates = {
                "task_assignment": ContractTemplate(
                    template_id="task_assignment_default",
                    name="Task Assignment Contract",
                    description="Standard contract for task assignments",
                    contract_type=ContractType.TASK_ASSIGNMENT,
                    default_terms={
                        "deliverables": [],
                        "acceptance_criteria": ["task_completed"],
                        "deadlines": {"completion": "24h"},
                        "dependencies": [],
                        "penalties": {},
                        "rewards": {},
                    },
                    required_fields=["title", "description", "required_capabilities"],
                    validation_rules={"min_duration": 1, "max_duration": 168},
                    created_at=datetime.now().isoformat(),
                    updated_at=datetime.now().isoformat(),
                ),
                "agent_response": ContractTemplate(
                    template_id="agent_response_default",
                    name="Agent Response Contract",
                    description="Standard contract for agent responses",
                    contract_type=ContractType.AGENT_RESPONSE,
                    default_terms={
                        "deliverables": ["response"],
                        "acceptance_criteria": ["response_provided"],
                        "deadlines": {"completion": "1h"},
                        "dependencies": [],
                        "penalties": {},
                        "rewards": {},
                    },
                    required_fields=["title", "description"],
                    validation_rules={"min_duration": 0.1, "max_duration": 24},
                    created_at=datetime.now().isoformat(),
                    updated_at=datetime.now().isoformat(),
                ),
            }

            for template_id, template in default_templates.items():
                self.contract_templates[template_id] = template

            self.logger.info(
                f"Loaded {len(self.contract_templates)} contract templates"
            )

        except Exception as e:
            self.logger.error(f"Failed to load contract templates: {e}")

    def _load_legacy_contracts(self):
        """Load and migrate existing contract files - from unified contract manager"""
        try:
            contracts_dir = Path(self.legacy_contracts_path)
            if not contracts_dir.exists():
                self.logger.info(
                    f"Legacy contracts directory not found: {contracts_dir}"
                )
                return

            migrated_count = 0
            for contract_file in contracts_dir.glob("*.json"):
                try:
                    with open(contract_file, "r") as f:
                        legacy_contract = json.load(f)

                    # Migrate legacy contract to new system
                    contract_id = self._migrate_legacy_contract(
                        legacy_contract, contract_file.name
                    )
                    if contract_id:
                        migrated_count += 1

                except Exception as e:
                    self.logger.error(
                        f"Failed to migrate contract {contract_file}: {e}"
                    )

            self.logger.info(f"Migrated {migrated_count} legacy contracts")

        except Exception as e:
            self.logger.error(f"Failed to load legacy contracts: {e}")

    def _migrate_legacy_contract(
        self, legacy_data: Dict[str, Any], filename: str
    ) -> Optional[str]:
        """Migrate a legacy contract to the new system - from unified contract manager"""
        try:
            # Extract information from legacy contract
            payload = legacy_data.get("payload", {})

            # Create parties from legacy data
            parties = []
            if "from" in legacy_data and "to" in legacy_data:
                parties = [
                    {
                        "party_id": legacy_data["from"],
                        "party_type": "agent",
                        "role": "contractor",
                        "permissions": ["execute", "report"],
                    },
                    {
                        "party_id": legacy_data["to"],
                        "party_type": "agent",
                        "role": "client",
                        "permissions": ["monitor", "approve"],
                    },
                ]

            # Create terms from legacy data
            terms = {
                "deliverables": payload.get("actions", []),
                "acceptance_criteria": [payload.get("status", "completed")],
                "deadlines": {"completion": "24h"},
                "dependencies": [],
                "penalties": {},
                "rewards": {},
            }

            # Determine contract type
            contract_type = ContractType.AGENT_RESPONSE
            if "task" in payload:
                contract_type = ContractType.TASK_ASSIGNMENT

            # Create new contract using enhanced create_contract method
            contract_id = self.create_contract(
                title=f"Migrated: {payload.get('task', filename)}",
                description=f"Migrated legacy contract from {filename}",
                contract_type=contract_type,
                parties=parties,
                terms=terms,
                priority=ContractPriority.NORMAL,
                auto_validate=False,  # Don't auto-validate migrated contracts
            )

            # Set appropriate state based on legacy status
            if contract_id:
                legacy_status = payload.get("status", "").lower()
                if legacy_status == "completed":
                    self._update_contract_status(contract_id, ContractStatus.COMPLETED)
                elif legacy_status in ["active", "in_progress"]:
                    self._update_contract_status(
                        contract_id, ContractStatus.IN_PROGRESS
                    )

            return contract_id

        except Exception as e:
            self.logger.error(f"Failed to migrate legacy contract: {e}")
            return None

    def create_contract(
        self,
        title: str,
        description: str,
        priority: ContractPriority = ContractPriority.NORMAL,
        required_capabilities: List[AgentCapability] = None,
        estimated_duration: int = 1,
        contract_type: ContractType = ContractType.TASK_ASSIGNMENT,
        parties: List[Dict[str, Any]] = None,
        terms: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None,
        auto_validate: bool = True,
    ) -> str:
        """Create a new contract - enhanced from both sources"""
        try:
            contract_id = str(uuid.uuid4())

            # Use template if available
            if contract_type and contract_type.value in self.contract_templates:
                template = self.contract_templates[contract_type.value]
                if not terms:
                    terms = template.default_terms.copy()
                if not parties:
                    parties = []

            contract = Contract(
                contract_id=contract_id,
                title=title,
                description=description,
                priority=priority,
                status=ContractStatus.PENDING,
                required_capabilities=required_capabilities or [],
                estimated_duration=estimated_duration,
                assigned_agent=None,
                created_at=datetime.now().isoformat(),
                assigned_at=None,
                completed_at=None,
                metadata=metadata or {},
                contract_type=contract_type,
                parties=parties or [],
                terms=terms or {},
                validation_results=[],
            )

            # Store contract
            self.contracts[contract_id] = contract

            # Validate contract if requested
            if auto_validate:
                validation_results = self.validator.validate_contract(
                    {
                        "title": title,
                        "description": description,
                        "priority": priority.value,
                        "required_capabilities": required_capabilities or [],
                    }
                )
                contract.validation_results = validation_results

                # Auto-approve if validation passes
                if all(r["passed"] for r in validation_results):
                    self._update_contract_status(contract_id, ContractStatus.APPROVED)

            # Attempt automatic assignment
            if self._should_auto_assign(contract):
                self._auto_assign_contract(contract_id)

            self.logger.info(f"Created contract: {contract_id} - {title}")
            return contract_id

        except Exception as e:
            self.logger.error(f"Failed to create contract: {e}")
            return ""

    def _should_auto_assign(self, contract: Contract) -> bool:
        """Determine if contract should be automatically assigned"""
        try:
            auto_assign = self.config_manager.get_config(
                "contracts", "auto_assign", True
            )
            if not auto_assign:
                return False

            # Auto-assign high priority contracts
            if contract.priority in [
                ContractPriority.URGENT,
                ContractPriority.CRITICAL,
            ]:
                return True

            # Auto-assign contracts with clear capability requirements
            if len(contract.required_capabilities) > 0:
                return True

            return False

        except Exception as e:
            self.logger.error(f"Failed to determine auto-assignment: {e}")
            return False

    def _auto_assign_contract(self, contract_id: str) -> bool:
        """Automatically assign a contract to the best available agent"""
        try:
            if contract_id not in self.contracts:
                return False

            contract = self.contracts[contract_id]

            # Find best agent match
            best_agent = self._find_best_agent_match(contract)
            if best_agent:
                return self.assign_contract(
                    contract_id, best_agent.agent_id, AssignmentStrategy.SKILL_MATCH
                )

            return False

        except Exception as e:
            self.logger.error(f"Failed to auto-assign contract: {e}")
            return False

    def _find_best_agent_match(self, contract: Contract) -> Optional[AgentInfo]:
        """Find the best agent match for a contract"""
        try:
            available_agents = self.agent_manager.get_available_agents()
            if not available_agents:
                return None

            best_agent = None
            best_score = 0

            for agent in available_agents:
                if agent.status != AgentStatus.AVAILABLE:
                    continue

                # Calculate match score
                score = self._calculate_agent_match_score(agent, contract)
                if score > best_score:
                    best_score = score
                    best_agent = agent

            return best_agent

        except Exception as e:
            self.logger.error(f"Failed to find best agent match: {e}")
            return None

    def _calculate_agent_match_score(
        self, agent: AgentInfo, contract: Contract
    ) -> float:
        """Calculate how well an agent matches a contract"""
        try:
            score = 0.0

            # Capability match (40% weight)
            capability_score = 0
            if contract.required_capabilities:
                matching_capabilities = sum(
                    1
                    for cap in contract.required_capabilities
                    if cap in agent.capabilities
                )
                capability_score = matching_capabilities / len(
                    contract.required_capabilities
                )
            score += capability_score * 0.4

            # Load balance (30% weight)
            current_load = len(
                [
                    a
                    for a in self.assignments.values()
                    if a.agent_id == agent.agent_id
                    and self.contracts[a.contract_id].status
                    in [ContractStatus.ASSIGNED, ContractStatus.IN_PROGRESS]
                ]
            )
            load_score = max(0, 1 - (current_load / 10))  # Normalize to 0-1
            score += load_score * 0.3

            # Performance history (20% weight)
            performance_score = agent.metadata.get("performance_score", 0.5)
            score += performance_score * 0.2

            # Availability (10% weight)
            availability_score = 1.0 if agent.status == AgentStatus.AVAILABLE else 0.0
            score += availability_score * 0.1

            return score

        except Exception as e:
            self.logger.error(f"Failed to calculate agent match score: {e}")
            return 0.0

    def assign_contract(
        self,
        contract_id: str,
        agent_id: str,
        strategy: AssignmentStrategy = AssignmentStrategy.SKILL_MATCH,
    ) -> bool:
        """Assign a contract to an agent"""
        try:
            if contract_id not in self.contracts:
                return False

            contract = self.contracts[contract_id]
            if (
                contract.status != ContractStatus.PENDING
                and contract.status != ContractStatus.APPROVED
            ):
                return False

            # Verify agent exists and is available
            agent = self.agent_manager.get_agent(agent_id)
            if not agent or agent.status != AgentStatus.AVAILABLE:
                return False

            # Create assignment
            assignment_id = str(uuid.uuid4())
            assignment = AssignmentResult(
                assignment_id=assignment_id,
                contract_id=contract_id,
                agent_id=agent_id,
                strategy=strategy,
                confidence_score=self._calculate_agent_match_score(agent, contract),
                assignment_timestamp=datetime.now().isoformat(),
                metadata={"strategy": strategy.value},
            )

            # Store assignment
            self.assignments[assignment_id] = assignment
            self.assignment_history.append(assignment)

            # Update contract
            contract.assigned_agent = agent_id
            contract.assigned_at = datetime.now().isoformat()
            self._update_contract_status(contract_id, ContractStatus.ASSIGNED)

            self.logger.info(f"Assigned contract {contract_id} to agent {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to assign contract: {e}")
            return False

    def _update_contract_status(self, contract_id: str, new_status: ContractStatus):
        """Update contract status"""
        try:
            if contract_id in self.contracts:
                contract = self.contracts[contract_id]
                old_status = contract.status
                contract.status = new_status

                # Update timestamps
                if new_status == ContractStatus.COMPLETED:
                    contract.completed_at = datetime.now().isoformat()

                self.logger.info(
                    f"Contract {contract_id} status changed: {old_status.value} -> {new_status.value}"
                )

        except Exception as e:
            self.logger.error(f"Failed to update contract status: {e}")

    def get_contract(self, contract_id: str) -> Optional[Contract]:
        """Get contract by ID"""
        return self.contracts.get(contract_id)

    def get_agent_contracts(self, agent_id: str) -> List[Contract]:
        """Get all contracts assigned to an agent"""
        try:
            agent_contracts = []
            for assignment in self.assignments.values():
                if assignment.agent_id == agent_id:
                    contract = self.contracts.get(assignment.contract_id)
                    if contract:
                        agent_contracts.append(contract)
            return agent_contracts

        except Exception as e:
            self.logger.error(f"Failed to get agent contracts: {e}")
            return []

    def get_contract_summary(self) -> Dict[str, Any]:
        """Get comprehensive contract summary"""
        try:
            total_contracts = len(self.contracts)
            pending_contracts = len(
                [
                    c
                    for c in self.contracts.values()
                    if c.status == ContractStatus.PENDING
                ]
            )
            active_contracts = len(
                [
                    c
                    for c in self.contracts.values()
                    if c.status in [ContractStatus.ASSIGNED, ContractStatus.IN_PROGRESS]
                ]
            )
            completed_contracts = len(
                [
                    c
                    for c in self.contracts.values()
                    if c.status == ContractStatus.COMPLETED
                ]
            )

            return {
                "total_contracts": total_contracts,
                "pending_contracts": pending_contracts,
                "active_contracts": active_contracts,
                "completed_contracts": completed_contracts,
                "total_assignments": len(self.assignments),
                "templates_available": len(self.contract_templates),
                "legacy_contracts_path": self.legacy_contracts_path,
            }

        except Exception as e:
            self.logger.error(f"Failed to get contract summary: {e}")
            return {"error": str(e)}

    def start(self):
        """Start the contract manager"""
        self.running = True
        self.logger.info("Contract Manager started")

    def stop(self):
        """Stop the contract manager"""
        self.running = False
        self.logger.info("Contract Manager stopped")


def run_smoke_test():
    """Run basic functionality test for consolidated ContractManager"""
    try:
        # Mock dependencies
        class MockAgentManager:
            def get_available_agents(self):
                return []

            def get_agent(self, agent_id):
                return None

        class MockConfigManager:
            def get_config(self, section, key, default):
                return default

        # Test ContractManager
        agent_mgr = MockAgentManager()
        config_mgr = MockConfigManager()
        contract_mgr = ContractManager(agent_mgr, config_mgr)

        # Test contract creation
        contract_id = contract_mgr.create_contract(
            title="Test Contract",
            description="Test contract for smoke testing",
            priority=ContractPriority.NORMAL,
        )

        assert contract_id
        assert contract_id in contract_mgr.contracts

        # Test contract retrieval
        contract = contract_mgr.get_contract(contract_id)
        assert contract.title == "Test Contract"
        assert contract.status == ContractStatus.PENDING

        # Test summary
        summary = contract_mgr.get_contract_summary()
        assert summary["total_contracts"] == 1

        print("✅ ContractManager smoke test passed!")
        return True

    except Exception as e:
        print(f"❌ ContractManager smoke test failed: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
