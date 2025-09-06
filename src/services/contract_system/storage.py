"""
Contract System Storage - V2 Compliant Module
=============================================

Handles persistence and retrieval of contract data.
Manages file-based storage for contracts and tasks.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import Contract, Task, TaskStatus


class ContractStorage:
    """Handles contract data persistence."""

    def __init__(self, base_path: str = "agent_workspaces/contracts"):
        """Initialize contract storage."""
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.contracts_file = self.base_path / "contracts.json"
        self.tasks_file = self.base_path / "tasks.json"
        self.agent_contracts_dir = self.base_path / "agent_contracts"
        self.agent_contracts_dir.mkdir(exist_ok=True)

    def save_contract(self, contract: Contract) -> bool:
        """Save contract to storage."""
        try:
            # Save to main contracts file
            contracts = self.load_all_contracts()
            contracts[contract.contract_id] = contract.to_dict()
            self._write_json(self.contracts_file, contracts)

            # Save to agent-specific file
            agent_file = (
                self.agent_contracts_dir / f"{contract.agent_id}_contracts.json"
            )
            agent_contracts = self.load_agent_contracts(contract.agent_id)
            agent_contracts[contract.contract_id] = contract.to_dict()
            self._write_json(agent_file, agent_contracts)

            return True
        except Exception as e:
            print(f"ERROR: Error saving contract: {e}")
            return False

    def load_contract(self, contract_id: str) -> Optional[Contract]:
        """Load specific contract."""
        try:
            contracts = self.load_all_contracts()
            if contract_id in contracts:
                return Contract.from_dict(contracts[contract_id])
            return None
        except Exception as e:
            print(f"ERROR: Error loading contract: {e}")
            return None

    def get_contract(self, contract_id: str) -> Optional[Contract]:
        """Get contract by ID - alias for load_contract."""
        return self.load_contract(contract_id)

    def load_all_contracts(self) -> Dict[str, Dict[str, Any]]:
        """Load all contracts."""
        try:
            if self.contracts_file.exists():
                return self._read_json(self.contracts_file)
            return {}
        except Exception as e:
            print(f"ERROR: Error loading contracts: {e}")
            return {}

    def load_agent_contracts(self, agent_id: str) -> Dict[str, Dict[str, Any]]:
        """Load contracts for specific agent."""
        try:
            agent_file = self.agent_contracts_dir / f"{agent_id}_contracts.json"
            if agent_file.exists():
                return self._read_json(agent_file)
            return {}
        except Exception as e:
            print(f"ERROR: Error loading agent contracts: {e}")
            return {}

    def get_agent_contracts(self, agent_id: str) -> List[Contract]:
        """Get contracts for specific agent as Contract objects."""
        try:
            agent_contracts_data = self.load_agent_contracts(agent_id)
            contracts = []
            for contract_data in agent_contracts_data.values():
                contract = Contract.from_dict(contract_data)
                contracts.append(contract)
            return contracts
        except Exception as e:
            print(f"ERROR: Error getting agent contracts: {e}")
            return []

    def get_available_tasks(self, agent_id: str) -> List[Task]:
        """Get available tasks for agent."""
        try:
            agent_contracts = self.load_agent_contracts(agent_id)
            available_tasks = []

            for contract_data in agent_contracts.values():
                contract = Contract.from_dict(contract_data)
                for task in contract.tasks:
                    if (
                        task.status == TaskStatus.PENDING
                        and task.assigned_agent is None
                    ):
                        available_tasks.append(task)

            # Sort by priority and creation time
            available_tasks.sort(key=lambda t: (t.priority.value, t.created_at))

            return available_tasks
        except Exception as e:
            print(f"ERROR: Error getting available tasks: {e}")
            return []

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        """Assign task to agent."""
        try:
            # Find task in all contracts
            contracts = self.load_all_contracts()
            for contract_data in contracts.values():
                contract = Contract.from_dict(contract_data)
                for task in contract.tasks:
                    if task.task_id == task_id:
                        task.assigned_agent = agent_id
                        task.status = TaskStatus.ASSIGNED
                        task.assigned_at = datetime.now()

                        # Update contract status
                        contract.update_status()

                        # Save updated contract
                        self.save_contract(contract)
                        return True

            return False
        except Exception as e:
            print(f"ERROR: Error assigning task: {e}")
            return False

    def complete_task(self, task_id: str, completion_notes: str = "") -> bool:
        """Mark task as completed."""
        try:
            # Find task in all contracts
            contracts = self.load_all_contracts()
            for contract_data in contracts.values():
                contract = Contract.from_dict(contract_data)
                for task in contract.tasks:
                    if task.task_id == task_id:
                        task.status = TaskStatus.COMPLETED
                        task.completed_at = datetime.now()
                        task.completion_notes = completion_notes

                        # Update contract status
                        contract.update_status()

                        # Save updated contract
                        self.save_contract(contract)
                        return True

            return False
        except Exception as e:
            print(f"ERROR: Error completing task: {e}")
            return False

    def get_agent_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get summary of agent's contract status."""
        try:
            agent_contracts = self.load_agent_contracts(agent_id)
            contracts = [Contract.from_dict(data) for data in agent_contracts.values()]

            total_contracts = len(contracts)
            active_contracts = len(
                [
                    c
                    for c in contracts
                    if c.status in [TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS]
                ]
            )
            completed_contracts = len(
                [c for c in contracts if c.status == TaskStatus.COMPLETED]
            )

            total_points = sum(c.total_points for c in contracts)
            completed_points = sum(c.completed_points for c in contracts)
            completion_rate = (
                (completed_points / total_points * 100) if total_points > 0 else 0
            )

            current_tasks = []
            for contract in contracts:
                for task in contract.tasks:
                    if task.status in [TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS]:
                        current_tasks.append(task)

            return {
                "agent_id": agent_id,
                "total_contracts": total_contracts,
                "active_contracts": active_contracts,
                "completed_contracts": completed_contracts,
                "total_points": total_points,
                "completed_points": completed_points,
                "completion_rate": round(completion_rate, 2),
                "current_tasks": [task.to_dict() for task in current_tasks],
            }
        except Exception as e:
            print(f"ERROR: Error getting agent summary: {e}")
            return {}

    def _read_json(self, file_path: Path) -> Dict[str, Any]:
        """Read JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"ERROR: Error reading JSON file {file_path}: {e}")
            return {}

    def _write_json(self, file_path: Path, data: Dict[str, Any]) -> bool:
        """Write JSON file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"ERROR: Error writing JSON file {file_path}: {e}")
            return False
