"""Lifecycle management for contracts."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from .models import (
    ContractRequirement,
    ContractStatus,
    ContractValidation,
    TaskStatus,
    ValidationLevel,
)
from .parser import parse_contract_requirements
from .validator import validate_contract

logger = logging.getLogger(__name__)


class ContractManager:
    """Manage contract statuses and lifecycle operations."""

    def __init__(self, contracts_dir: str = "logs") -> None:
        self.contracts_dir = Path(contracts_dir)
        self.contracts_dir.mkdir(exist_ok=True)
        self.status_file = self.contracts_dir / "contract_statuses.json"
        self.contract_statuses: Dict[str, ContractStatus] = {}
        self.load_statuses()

    def load_statuses(self) -> None:
        """Load existing contract statuses from disk."""
        if not self.status_file.exists():
            return
        try:
            with self.status_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
            for contract_id, status_data in data.items():
                if "current_status" in status_data:
                    try:
                        status_data["current_status"] = TaskStatus(
                            status_data["current_status"]
                        )
                    except ValueError:
                        status_data["current_status"] = TaskStatus.PENDING
                validation_data = status_data.get("validation_result")
                if validation_data:
                    status_data["validation_result"] = ContractValidation(
                        **validation_data
                    )
                self.contract_statuses[contract_id] = ContractStatus(**status_data)
        except Exception as exc:  # pragma: no cover - log error path
            logger.error("Error loading contract statuses: %s", exc)
            self.contract_statuses = {}

    def save_statuses(self) -> None:
        """Persist contract statuses to disk."""
        data: Dict[str, Dict[str, object]] = {}
        for contract_id, status in self.contract_statuses.items():
            status_dict = status.__dict__.copy()
            status_dict["current_status"] = status.current_status.value
            if status.validation_result:
                status_dict[
                    "validation_result"
                ] = status.validation_result.__dict__.copy()
            data[contract_id] = status_dict
        try:
            with self.status_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except Exception as exc:  # pragma: no cover - log error path
            logger.error("Error saving contract statuses: %s", exc)

    def get_contract_requirements(
        self, contract_file: Path
    ) -> List[ContractRequirement]:
        """Parse and return contract requirements from a file."""
        return parse_contract_requirements(contract_file)

    def get_agent_contracts(self, agent_id: str) -> List[ContractStatus]:
        """Return all contracts assigned to a specific agent."""
        return [
            status
            for status in self.contract_statuses.values()
            if status.agent_id == agent_id
        ]

    def create_contract_status(
        self, contract_id: str, agent_id: str, contract_file: Path
    ) -> ContractStatus:
        """Create and register a new contract status."""
        requirements = parse_contract_requirements(contract_file)
        status = ContractStatus(
            contract_id=contract_id,
            agent_id=agent_id,
            current_status=TaskStatus.PENDING,
            progress_percentage=0.0,
            last_updated="",
            requirements_completed=0,
            total_requirements=len(requirements),
        )
        status.update_timestamp()
        self.contract_statuses[contract_id] = status
        self.save_statuses()
        return status

    def update_requirement_status(
        self, contract_id: str, requirement_id: str, completed: bool, notes: str = ""
    ) -> bool:
        """Update the completion state of a requirement."""
        status = self.contract_statuses.get(contract_id)
        if not status:
            logger.error("Contract %s not found", contract_id)
            return False
        contract_file = (
            self.contracts_dir
            / f"contracts_{status.agent_id.lower().replace('-', '_')}"
            / f"{contract_id.lower()}.md"
        )
        if not contract_file.exists():
            logger.error("Contract file not found: %s", contract_file)
            return False
        requirements = parse_contract_requirements(contract_file)
        for req in requirements:
            if req.requirement_id == requirement_id:
                req.completed = completed
                req.validation_notes = notes
                if completed:
                    req.completion_timestamp = datetime.now().isoformat()
                break
        else:
            logger.error(
                "Requirement %s not found in contract %s", requirement_id, contract_id
            )
            return False
        validate_contract(status, self.contracts_dir)
        self.save_statuses()
        return True

    def validate_contract_completion(
        self,
        contract_id: str,
        validation_level: ValidationLevel = ValidationLevel.STANDARD,
    ) -> ContractValidation:
        """Validate a contract and update its status."""
        status = self.contract_statuses.get(contract_id)
        if not status:
            return ContractValidation(
                is_valid=False,
                missing_requirements=["Contract not found"],
                validation_errors=["Contract ID not found in system"],
                warnings=[],
                score=0.0,
                timestamp=datetime.now().isoformat(),
            )
        validation = validate_contract(status, self.contracts_dir, validation_level)
        self.save_statuses()
        return validation

    def auto_discover_contracts(self) -> None:
        """Automatically discover new contract files and register them."""
        for agent_dir in self.contracts_dir.glob("contracts_agent_*"):
            agent_id = (
                agent_dir.name.replace("contracts_", "").replace("_", "-").upper()
            )
            for contract_file in agent_dir.glob("*.md"):
                contract_id = contract_file.stem.upper()
                if contract_id not in self.contract_statuses:
                    logger.info(
                        "Auto-discovered new contract: %s for %s", contract_id, agent_id
                    )
                    self.create_contract_status(contract_id, agent_id, contract_file)
