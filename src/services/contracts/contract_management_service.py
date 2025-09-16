#!/usr/bin/env python3
"""
Contract Management Service - V2 Compliance Module
=================================================

Contract management service for agent task commitments and tracking.

V2 Compliance: < 300 lines, single responsibility, contract management.

Author: Agent-2 (Architecture & Design Specialist) - Extracted from integrated_onboarding_coordination_system.py
License: MIT
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from src.core.coordination.contract_system import ContractType, AgentContract
from src.core.coordination.fsm_system import AgentState

logger = logging.getLogger(__name__)


class ContractManagementService:
    """Service for contract creation, tracking, and management."""
    
    def __init__(self):
        """Initialize the contract management service."""
        self.active_contracts: Dict[str, AgentContract] = {}
        self.contract_history: List[AgentContract] = []
        self.contract_metrics: Dict[str, Dict] = {}
    
    def create_contract(self, agent_id: str, contract_type: ContractType, 
                       description: str, estimated_cycles: int, dependencies: List[str] = None) -> AgentContract:
        """Create a new contract for an agent."""
        contract = AgentContract(
            agent_id=agent_id,
            contract_type=contract_type,
            description=description,
            estimated_cycles=estimated_cycles,
            dependencies=dependencies or []
        )
        self.active_contracts[agent_id] = contract
        self.contract_history.append(contract)
        
        # Initialize metrics for this contract
        self.contract_metrics[agent_id] = {
            "created_at": datetime.now(),
            "estimated_cycles": estimated_cycles,
            "actual_cycles": 0,
            "progress_updates": 0,
            "status_changes": 0
        }
        
        logger.info(f"📋 Contract created for {agent_id}: {contract_type.value} - {description}")
        return contract
    
    def start_contract(self, agent_id: str) -> bool:
        """Start execution of a contract."""
        contract = self.active_contracts.get(agent_id)
        if not contract:
            logger.error(f"❌ No active contract found for {agent_id}")
            return False
        
        if contract.status == "pending":
            contract.start_contract()
            self._update_contract_metrics(agent_id, "status_changes")
            logger.info(f"🚀 Contract started for {agent_id}: {contract.contract_type.value}")
            return True
        else:
            logger.warning(f"⚠️ Contract already active for {agent_id}")
            return False
    
    def update_contract_progress(self, agent_id: str, percentage: int) -> bool:
        """Update contract progress."""
        contract = self.active_contracts.get(agent_id)
        if not contract:
            logger.error(f"❌ No active contract found for {agent_id}")
            return False
        
        old_progress = contract.progress_percentage
        contract.update_progress(percentage)
        self._update_contract_metrics(agent_id, "progress_updates")
        
        logger.info(f"📊 Contract progress updated for {agent_id}: {old_progress}% → {percentage}%")
        
        if contract.is_completed():
            self._finalize_contract(agent_id)
        
        return True
    
    def complete_contract(self, agent_id: str) -> bool:
        """Mark contract as completed."""
        contract = self.active_contracts.get(agent_id)
        if not contract:
            logger.error(f"❌ No active contract found for {agent_id}")
            return False
        
        contract.complete_contract()
        self._finalize_contract(agent_id)
        logger.info(f"✅ Contract completed for {agent_id}: {contract.contract_type.value}")
        return True
    
    def cancel_contract(self, agent_id: str, reason: str = "Cancelled") -> bool:
        """Cancel an active contract."""
        contract = self.active_contracts.get(agent_id)
        if not contract:
            logger.error(f"❌ No active contract found for {agent_id}")
            return False
        
        contract.status = "cancelled"
        contract.cycle_end = datetime.now()
        self._update_contract_metrics(agent_id, "status_changes")
        
        logger.warning(f"⚠️ Contract cancelled for {agent_id}: {reason}")
        return True
    
    def get_contract_status(self, agent_id: str) -> Optional[Dict]:
        """Get contract status for an agent."""
        contract = self.active_contracts.get(agent_id)
        if not contract:
            return None
        
        metrics = self.contract_metrics.get(agent_id, {})
        
        return {
            "agent_id": agent_id,
            "contract_type": contract.contract_type.value,
            "description": contract.description,
            "status": contract.status,
            "progress_percentage": contract.progress_percentage,
            "estimated_cycles": contract.estimated_cycles,
            "actual_cycles": metrics.get("actual_cycles", 0),
            "created_at": contract.created_at.isoformat(),
            "cycle_start": contract.cycle_start.isoformat() if contract.cycle_start else None,
            "cycle_end": contract.cycle_end.isoformat() if contract.cycle_end else None,
            "dependencies": contract.dependencies
        }
    
    def get_active_contracts(self) -> Dict[str, AgentContract]:
        """Get all active contracts."""
        return self.active_contracts.copy()
    
    def get_contract_history(self, agent_id: str = None) -> List[AgentContract]:
        """Get contract history."""
        if agent_id:
            return [contract for contract in self.contract_history if contract.agent_id == agent_id]
        return self.contract_history.copy()
    
    def get_contract_metrics(self, agent_id: str = None) -> Dict:
        """Get contract metrics."""
        if agent_id:
            return self.contract_metrics.get(agent_id, {})
        return self.contract_metrics.copy()
    
    def validate_contract_dependencies(self, agent_id: str) -> List[str]:
        """Validate contract dependencies."""
        contract = self.active_contracts.get(agent_id)
        if not contract:
            return []
        
        unmet_dependencies = []
        for dependency in contract.dependencies:
            dep_contract = self.active_contracts.get(dependency)
            if not dep_contract or not dep_contract.is_completed():
                unmet_dependencies.append(dependency)
        
        return unmet_dependencies
    
    def can_start_contract(self, agent_id: str) -> bool:
        """Check if contract can be started (dependencies met)."""
        unmet_dependencies = self.validate_contract_dependencies(agent_id)
        return len(unmet_dependencies) == 0
    
    def get_contracts_by_type(self, contract_type: ContractType) -> List[AgentContract]:
        """Get all contracts of a specific type."""
        return [contract for contract in self.active_contracts.values() 
                if contract.contract_type == contract_type]
    
    def get_contracts_by_status(self, status: str) -> List[AgentContract]:
        """Get all contracts with a specific status."""
        return [contract for contract in self.active_contracts.values() 
                if contract.status == status]
    
    def _finalize_contract(self, agent_id: str) -> None:
        """Finalize contract completion."""
        contract = self.active_contracts.get(agent_id)
        if contract and contract.is_completed():
            metrics = self.contract_metrics.get(agent_id, {})
            if contract.cycle_start and contract.cycle_end:
                duration = contract.cycle_end - contract.cycle_start
                metrics["actual_cycles"] = duration.total_seconds() / 60  # Convert to cycles
                self.contract_metrics[agent_id] = metrics
            
            # Move from active to history
            del self.active_contracts[agent_id]
            logger.info(f"📋 Contract finalized for {agent_id}")
    
    def _update_contract_metrics(self, agent_id: str, metric_type: str) -> None:
        """Update contract metrics."""
        if agent_id in self.contract_metrics:
            self.contract_metrics[agent_id][metric_type] = self.contract_metrics[agent_id].get(metric_type, 0) + 1