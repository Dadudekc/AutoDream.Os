#!/usr/bin/env python3
"""Simplified contract management and assignment engine."""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

from .agent_manager import AgentManager
from .config_manager import ConfigManager
from .contract_models import (
    AssignmentResult,
    AssignmentStrategy,
    Contract,
    ContractPriority,
    ContractStatus,
)
from .validation import ContractValidator


class ContractManager:
    """Manages contract lifecycle and basic assignment."""

    def __init__(
        self, agent_manager: AgentManager, config_manager: ConfigManager
    ) -> None:
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.validator = ContractValidator()
        self.contracts: Dict[str, Contract] = {}
        self.assignments: Dict[str, AssignmentResult] = {}
        self.logger = logging.getLogger(f"{__name__}.ContractManager")
        self.running = False

    # ------------------------------------------------------------------
    # Contract creation and storage
    # ------------------------------------------------------------------
    def create_contract(
        self,
        title: str,
        description: str,
        priority: ContractPriority = ContractPriority.NORMAL,
        required_capabilities: Optional[List[Any]] = None,
        estimated_duration: int = 1,
        metadata: Optional[Dict[str, Any]] = None,
        auto_validate: bool = True,
    ) -> str:
        """Create and optionally validate a new contract."""
        contract_id = str(uuid.uuid4())
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
            validation_results=[],
        )
        if auto_validate:
            results = self.validator.validate_contract(
                {
                    "title": title,
                    "description": description,
                    "priority": priority.value,
                    "required_capabilities": required_capabilities or [],
                }
            )
            contract.validation_results = results
            if all(r["passed"] for r in results):
                contract.status = ContractStatus.APPROVED
        self.contracts[contract_id] = contract
        self.logger.info("Created contract %s", contract_id)
        return contract_id

    # ------------------------------------------------------------------
    # Assignment operations
    # ------------------------------------------------------------------
    def assign_contract(
        self,
        contract_id: str,
        agent_id: str,
        strategy: AssignmentStrategy = AssignmentStrategy.SKILL_MATCH,
    ) -> bool:
        """Assign a contract to an agent."""
        contract = self.contracts.get(contract_id)
        if not contract or contract.status not in {
            ContractStatus.PENDING,
            ContractStatus.APPROVED,
        }:
            return False
        if self.agent_manager and not self.agent_manager.get_agent_info(agent_id):
            return False
        assignment_id = str(uuid.uuid4())
        contract.assigned_agent = agent_id
        contract.assigned_at = datetime.now().isoformat()
        contract.status = ContractStatus.ASSIGNED
        result = AssignmentResult(
            assignment_id=assignment_id,
            contract_id=contract_id,
            agent_id=agent_id,
            strategy=strategy,
            confidence_score=1.0,
            assignment_timestamp=datetime.now().isoformat(),
            metadata={},
        )
        self.assignments[assignment_id] = result
        self.logger.info("Assigned contract %s to agent %s", contract_id, agent_id)
        return True

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------
    def get_contract(self, contract_id: str) -> Optional[Contract]:
        return self.contracts.get(contract_id)

    def get_contract_status(self, contract_id: str) -> Optional[ContractStatus]:
        contract = self.get_contract(contract_id)
        return contract.status if contract else None

    def get_pending_contracts(self) -> List[Contract]:
        return [
            c for c in self.contracts.values() if c.status == ContractStatus.PENDING
        ]

    def get_contract_summary(self) -> Dict[str, Any]:
        total = len(self.contracts)
        pending = len(self.get_pending_contracts())
        active = len(
            [
                c
                for c in self.contracts.values()
                if c.status in {ContractStatus.ASSIGNED, ContractStatus.IN_PROGRESS}
            ]
        )
        completed = len(
            [c for c in self.contracts.values() if c.status == ContractStatus.COMPLETED]
        )
        return {
            "total_contracts": total,
            "pending_contracts": pending,
            "active_contracts": active,
            "completed_contracts": completed,
            "total_assignments": len(self.assignments),
        }

    # ------------------------------------------------------------------
    # Lifecycle controls
    # ------------------------------------------------------------------
    def start(self) -> None:
        self.running = True
        self.logger.info("ContractManager started")

    def shutdown(self) -> None:
        self.running = False
        self.logger.info("ContractManager stopped")
