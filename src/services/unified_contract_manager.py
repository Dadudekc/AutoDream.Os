#!/usr/bin/env python3
"""
Unified Contract Manager - Agent Cellphone V2
============================================

CONSOLIDATED contract management system using BaseManager.
Eliminates duplication by inheriting from unified base manager.

**Author:** V2 Consolidation Specialist
**Created:** Current Sprint
**Status:** ACTIVE - CONSOLIDATION COMPLETE
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime

# Import consolidated base manager system
from ..core.base_manager import BaseManager, ManagerStatus, ManagerPriority, ManagerMetrics

# Import contract-related modules
from ..core.assignment_engine import ContractManager
from ..core.contract_models import (
    Contract,
    ContractStatus,
    ContractType,
    ContractParty,
    ContractTerms,
    ContractMetrics
)


class UnifiedContractManager(BaseManager):
    """
    CONSOLIDATED unified contract manager using BaseManager
    
    Eliminates duplication by inheriting from unified base manager system.
    Provides contract lifecycle, status tracking, and management functionality.
    """

    def __init__(self, legacy_contracts_path: Optional[str] = None):
        # Initialize consolidated base manager
        super().__init__(
            manager_id="unified_contract_manager",
            name="Unified Contract Manager",
            description="Unified contract management system integrating all contract services"
        )
        
        # Contract-specific configuration
        self.legacy_contracts_path = (
            legacy_contracts_path or "Agent_Cellphone/CONTRACTS"
        )
        
        # Contract management components
        self.contract_manager = ContractManager(None, None)
        self.contract_analytics: Dict[str, Any] = {}
        self.system_status: Dict[str, Any] = {}
        
        # Contract storage
        self.contracts: Dict[str, Contract] = {}
        self.contract_history: List[Dict[str, Any]] = []
        
        # Performance tracking
        self.contract_metrics = ContractMetrics()
        
        self.logger.info("Unified Contract Manager initialized - using consolidated system")

    # ============================================================================
    # BASE MANAGER IMPLEMENTATION - Required abstract methods
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Contract-specific startup logic"""
        try:
            # Load legacy contracts
            self._load_legacy_contracts()
            
            # Initialize contract storage
            self._initialize_contract_storage()
            
            self.logger.info("UnifiedContractManager startup completed")
            return True
            
        except Exception as e:
            self.logger.error(f"UnifiedContractManager startup failed: {e}")
            return False
    
    def _on_stop(self):
        """Contract-specific shutdown logic"""
        try:
            # Save contract states
            self._save_contract_states()
            
            # Save analytics
            self._save_contract_analytics()
            
            self.logger.info("UnifiedContractManager shutdown completed")
            
        except Exception as e:
            self.logger.error(f"UnifiedContractManager shutdown failed: {e}")
    
    def _on_heartbeat(self):
        """Contract-specific heartbeat logic"""
        try:
            # Update contract metrics
            self._update_contract_metrics()
            
            # Check contract health
            self._check_contract_health()
            
        except Exception as e:
            self.logger.error(f"UnifiedContractManager heartbeat failed: {e}")
    
    def _on_initialize_resources(self) -> bool:
        """Contract-specific resource initialization"""
        try:
            # Initialize contract storage directory
            contracts_dir = Path(self.legacy_contracts_path)
            contracts_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize analytics storage
            self.contract_analytics = {}
            
            return True
            
        except Exception as e:
            self.logger.error(f"UnifiedContractManager resource initialization failed: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Contract-specific resource cleanup"""
        try:
            # Save all contract data
            self._save_contract_states()
            self._save_contract_analytics()
            
        except Exception as e:
            self.logger.error(f"UnifiedContractManager resource cleanup failed: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Contract-specific recovery logic"""
        try:
            self.logger.info(f"Attempting UnifiedContractManager recovery: {context}")
            
            # Reload contracts
            self._load_legacy_contracts()
            
            # Reinitialize storage
            self._initialize_contract_storage()
            
            self.logger.info("UnifiedContractManager recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"UnifiedContractManager recovery failed: {e}")
            return False

    # ============================================================================
    # CONTRACT MANAGEMENT METHODS - Specific functionality
    # ============================================================================
    
    def _load_legacy_contracts(self):
        """Load and migrate existing contract files"""
        try:
            contracts_dir = Path(self.legacy_contracts_path)
            if not contracts_dir.exists():
                self.logger.info(
                    f"Legacy contracts directory not found: {contracts_dir}. Creating."
                )
                contracts_dir.mkdir(parents=True, exist_ok=True)
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
            
            # Record successful operation
            self.record_operation("load_legacy_contracts", True, migrated_count)

        except Exception as e:
            self.logger.error(f"Failed to load legacy contracts: {e}")
            self.handle_error(e, "load_legacy_contracts")
            self.record_operation("load_legacy_contracts", False)

    def _migrate_legacy_contract(
        self, legacy_data: Dict[str, Any], filename: str
    ) -> Optional[str]:
        """Migrate a legacy contract to the new system"""
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
                "timeline": payload.get("timeline", "immediate"),
                "quality_standards": payload.get("quality", "standard"),
                "success_criteria": payload.get("success_criteria", []),
            }

            # Create new contract
            contract = Contract(
                contract_id=filename.replace(".json", ""),
                contract_type=ContractType.LEGACY_MIGRATION,
                status=ContractStatus.ACTIVE,
                parties=parties,
                terms=terms,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            # Store contract
            self.contracts[contract.contract_id] = contract
            
            # Record successful operation
            self.record_operation("migrate_contract", True)
            
            return contract.contract_id

        except Exception as e:
            self.logger.error(f"Failed to migrate contract {filename}: {e}")
            self.record_operation("migrate_contract", False)
            return None

    def _initialize_contract_storage(self):
        """Initialize contract storage system"""
        try:
            # Create contract storage directory
            storage_dir = Path("contracts/storage")
            storage_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize contract analytics
            self.contract_analytics = {
                "total_contracts": 0,
                "active_contracts": 0,
                "completed_contracts": 0,
                "failed_contracts": 0,
                "migration_count": 0
            }
            
            self.logger.info("Contract storage initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize contract storage: {e}")

    def create_contract(
        self,
        contract_type: ContractType,
        parties: List[ContractParty],
        terms: ContractTerms,
        **kwargs
    ) -> Optional[str]:
        """Create a new contract"""
        try:
            # Generate contract ID
            contract_id = f"contract_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.contracts)}"
            
            # Create contract
            contract = Contract(
                contract_id=contract_id,
                contract_type=contract_type,
                status=ContractStatus.DRAFT,
                parties=parties,
                terms=terms,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                **kwargs
            )
            
            # Store contract
            self.contracts[contract_id] = contract
            
            # Update analytics
            self.contract_analytics["total_contracts"] += 1
            
            # Record successful operation
            self.record_operation("create_contract", True)
            
            self.logger.info(f"Created new contract: {contract_id}")
            return contract_id
            
        except Exception as e:
            self.logger.error(f"Failed to create contract: {e}")
            self.handle_error(e, "create_contract")
            self.record_operation("create_contract", False)
            return None

    def get_contract(self, contract_id: str) -> Optional[Contract]:
        """Get contract by ID"""
        try:
            contract = self.contracts.get(contract_id)
            if contract:
                # Record successful operation
                self.record_operation("get_contract", True)
                return contract
            else:
                self.logger.warning(f"Contract {contract_id} not found")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to get contract {contract_id}: {e}")
            self.handle_error(e, f"get_contract_{contract_id}")
            self.record_operation("get_contract", False)
            return None

    def update_contract_status(self, contract_id: str, status: ContractStatus) -> bool:
        """Update contract status"""
        try:
            if contract_id not in self.contracts:
                self.logger.warning(f"Contract {contract_id} not found")
                return False

            contract = self.contracts[contract_id]
            old_status = contract.status
            contract.status = status
            contract.updated_at = datetime.now()

            # Update analytics
            if old_status == ContractStatus.ACTIVE and status == ContractStatus.COMPLETED:
                self.contract_analytics["active_contracts"] -= 1
                self.contract_analytics["completed_contracts"] += 1
            elif old_status == ContractStatus.ACTIVE and status == ContractStatus.FAILED:
                self.contract_analytics["active_contracts"] -= 1
                self.contract_analytics["failed_contracts"] += 1

            # Save contract state
            self._save_contract_states()

            # Record successful operation
            self.record_operation("update_contract_status", True)
            
            self.logger.info(f"Updated contract {contract_id} status: {old_status} -> {status}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update contract status for {contract_id}: {e}")
            self.handle_error(e, f"update_contract_status_{contract_id}")
            self.record_operation("update_contract_status", False)
            return False

    def get_contracts_by_status(self, status: ContractStatus) -> List[Contract]:
        """Get all contracts with a specific status"""
        try:
            contracts = [c for c in self.contracts.values() if c.status == status]
            
            # Record successful operation
            self.record_operation("get_contracts_by_status", True)
            
            return contracts
            
        except Exception as e:
            self.logger.error(f"Failed to get contracts by status {status}: {e}")
            self.handle_error(e, f"get_contracts_by_status_{status}")
            self.record_operation("get_contracts_by_status", False)
            return []

    def get_all_contracts(self) -> List[Contract]:
        """Get all contracts"""
        try:
            contracts = list(self.contracts.values())
            
            # Record successful operation
            self.record_operation("get_all_contracts", True)
            
            return contracts
            
        except Exception as e:
            self.logger.error(f"Failed to get all contracts: {e}")
            self.handle_error(e, "get_all_contracts")
            self.record_operation("get_all_contracts", False)
            return []

    def delete_contract(self, contract_id: str) -> bool:
        """Delete a contract"""
        try:
            if contract_id not in self.contracts:
                self.logger.warning(f"Contract {contract_id} not found")
                return False

            # Remove contract
            del self.contracts[contract_id]

            # Update analytics
            self.contract_analytics["total_contracts"] -= 1

            # Save contract states
            self._save_contract_states()

            # Record successful operation
            self.record_operation("delete_contract", True)
            
            self.logger.info(f"Deleted contract: {contract_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to delete contract {contract_id}: {e}")
            self.handle_error(e, f"delete_contract_{contract_id}")
            self.record_operation("delete_contract", False)
            return False

    # ============================================================================
    # CONTRACT ANALYTICS AND METRICS
    # ============================================================================
    
    def _update_contract_metrics(self):
        """Update contract performance metrics"""
        try:
            # Update active contracts count
            active_count = len([c for c in self.contracts.values() if c.status == ContractStatus.ACTIVE])
            self.contract_analytics["active_contracts"] = active_count
            
            # Update contract metrics
            self.contract_metrics.total_contracts = len(self.contracts)
            self.contract_metrics.active_contracts = active_count
            self.contract_metrics.completion_rate = self._calculate_completion_rate()
            
        except Exception as e:
            self.logger.error(f"Failed to update contract metrics: {e}")

    def _check_contract_health(self):
        """Check health of all contracts"""
        try:
            current_time = datetime.now()
            for contract_id, contract in self.contracts.items():
                # Check for expired contracts
                if contract.status == ContractStatus.ACTIVE:
                    # Simple expiration check (could be more sophisticated)
                    if hasattr(contract, 'expires_at') and contract.expires_at:
                        if current_time > contract.expires_at:
                            self.update_contract_status(contract_id, ContractStatus.EXPIRED)
                            self.logger.warning(f"Contract {contract_id} marked as expired")

        except Exception as e:
            self.logger.error(f"Failed to check contract health: {e}")

    def _calculate_completion_rate(self) -> float:
        """Calculate contract completion rate"""
        try:
            if self.contract_analytics["total_contracts"] == 0:
                return 0.0
            
            completed = self.contract_analytics["completed_contracts"]
            total = self.contract_analytics["total_contracts"]
            
            return (completed / total) * 100.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate completion rate: {e}")
            return 0.0

    def get_contract_analytics(self) -> Dict[str, Any]:
        """Get comprehensive contract analytics"""
        try:
            analytics = self.contract_analytics.copy()
            analytics.update({
                "completion_rate": self._calculate_completion_rate(),
                "performance_metrics": self.get_performance_summary()
            })
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Failed to get contract analytics: {e}")
            return {"error": str(e)}

    # ============================================================================
    # CONTRACT PERSISTENCE
    # ============================================================================
    
    def _save_contract_states(self):
        """Save current state of all contracts"""
        try:
            storage_dir = Path("contracts/storage")
            storage_dir.mkdir(parents=True, exist_ok=True)
            
            # Save contracts
            contracts_file = storage_dir / "contracts.json"
            contracts_data = {
                contract_id: contract.to_dict() 
                for contract_id, contract in self.contracts.items()
            }
            
            with open(contracts_file, "w") as f:
                json.dump(contracts_data, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Failed to save contract states: {e}")

    def _save_contract_analytics(self):
        """Save contract analytics"""
        try:
            storage_dir = Path("contracts/storage")
            storage_dir.mkdir(parents=True, exist_ok=True)
            
            # Save analytics
            analytics_file = storage_dir / "analytics.json"
            with open(analytics_file, "w") as f:
                json.dump(self.contract_analytics, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Failed to save contract analytics: {e}")

    # ============================================================================
    # ENHANCED STATUS AND METRICS (using BaseManager)
    # ============================================================================
    
    def get_contract_manager_status(self) -> Dict[str, Any]:
        """Get comprehensive contract manager status"""
        base_status = self.get_status()
        
        contract_status = {
            "total_contracts": len(self.contracts),
            "active_contracts": self.contract_analytics.get("active_contracts", 0),
            "completed_contracts": self.contract_analytics.get("completed_contracts", 0),
            "failed_contracts": self.contract_analytics.get("failed_contracts", 0),
            "completion_rate": self._calculate_completion_rate(),
            "performance_summary": self.get_performance_summary()
        }
        
        return {**base_status, **contract_status}

    def __str__(self) -> str:
        return f"UnifiedContractManager(contracts={len(self.contracts)}, status={self.status.value})"

    def __repr__(self) -> str:
        return f"UnifiedContractManager(legacy_path='{self.legacy_contracts_path}', total_contracts={len(self.contracts)})"
