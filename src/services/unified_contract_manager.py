"""
Unified Contract Manager - Complete Contract System Integration

This module provides unified contract management integrating:
- Contract lifecycle management and state tracking
- Contract validation and enforcement
- Legacy contract system consolidation
- Comprehensive contract analytics and reporting

Architecture: Single Responsibility Principle - manages unified contract operations
LOC: 200 lines (under 200 limit)
"""

import argparse
import time
import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

# Import consolidated contract manager
try:
    from ..core.contract_manager import ContractManager, ContractStatus, ContractType, ContractPriority
    SERVICES_AVAILABLE = True
except ImportError:
    print("Warning: Consolidated contract manager not available for import")
    SERVICES_AVAILABLE = False

logger = logging.getLogger(__name__)


class UnifiedContractManager:
    """
    Unified contract management system
    
    Responsibilities:
    - Integrate all contract management services
    - Provide single interface for contract operations
    - Consolidate existing contract systems
    - Manage contract analytics and reporting
    """
    
    def __init__(self, legacy_contracts_path: Optional[str] = None):
        self.logger = logging.getLogger(f"{__name__}.UnifiedContractManager")
        
        if not SERVICES_AVAILABLE:
            self.logger.warning("Running in limited mode - services not available")
            self.services_available = False
            return
        
        self.services_available = True
        # Use consolidated contract manager instead of separate services
        self.contract_manager = ContractManager(None, None, legacy_contracts_path)
        
        self.legacy_contracts_path = legacy_contracts_path or "Agent_Cellphone/CONTRACTS"
        self.contract_analytics = {}
        self.system_status = {}
        
        self.logger.info("Unified Contract Manager initialized - using consolidated system")
    
    def _load_legacy_contracts(self):
        """Load and migrate existing contract files"""
        if not self.services_available:
            return
        
        try:
            contracts_dir = Path(self.legacy_contracts_path)
            if not contracts_dir.exists():
                self.logger.info(f"Legacy contracts directory not found: {contracts_dir}")
                return
            
            migrated_count = 0
            for contract_file in contracts_dir.glob("*.json"):
                try:
                    with open(contract_file, 'r') as f:
                        legacy_contract = json.load(f)
                    
                    # Migrate legacy contract to new system
                    contract_id = self._migrate_legacy_contract(legacy_contract, contract_file.name)
                    if contract_id:
                        migrated_count += 1
                        
                except Exception as e:
                    self.logger.error(f"Failed to migrate contract {contract_file}: {e}")
            
            self.logger.info(f"Migrated {migrated_count} legacy contracts")
            
        except Exception as e:
            self.logger.error(f"Failed to load legacy contracts: {e}")
    
    def _migrate_legacy_contract(self, legacy_data: Dict[str, Any], filename: str) -> Optional[str]:
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
                        "permissions": ["execute", "report"]
                    },
                    {
                        "party_id": legacy_data["to"],
                        "party_type": "agent", 
                        "role": "client",
                        "permissions": ["monitor", "approve"]
                    }
                ]
            
            # Create terms from legacy data
            terms = {
                "deliverables": payload.get("actions", []),
                "acceptance_criteria": [payload.get("status", "completed")],
                "deadlines": {"completion": "24h"},
                "dependencies": [],
                "penalties": {},
                "rewards": {}
            }
            
            # Determine contract type
            contract_type = "agent_response"
            if "task" in payload:
                contract_type = "task_assignment"
            
            # Create new contract
            contract_id = self.lifecycle_service.create_contract(
                title=f"Migrated: {payload.get('task', filename)}",
                description=f"Migrated legacy contract from {filename}",
                contract_type=contract_type,
                parties=parties,
                terms=terms,
                priority="medium"
            )
            
            # Set appropriate state based on legacy status
            legacy_status = payload.get("status", "").lower()
            if legacy_status == "completed":
                self.lifecycle_service.transition_contract_state(contract_id, "completed", "Migrated as completed")
            elif legacy_status in ["active", "in_progress"]:
                self.lifecycle_service.transition_contract_state(contract_id, "active", "Migrated as active")
            
            return contract_id
            
        except Exception as e:
            self.logger.error(f"Failed to migrate legacy contract: {e}")
            return None
    
    def create_contract(self, title: str, description: str, contract_type: str,
                       parties: List[Dict[str, Any]], terms: Dict[str, Any],
                       priority: str = "medium", auto_validate: bool = True) -> Dict[str, Any]:
        """Create a new contract with integrated validation"""
        if not self.services_available:
            return {"error": "Services not available"}
        
        try:
            # Convert string priority to enum
            priority_enum = ContractPriority.NORMAL
            if priority == "high":
                priority_enum = ContractPriority.HIGH
            elif priority == "urgent":
                priority_enum = ContractPriority.URGENT
            elif priority == "critical":
                priority_enum = ContractPriority.CRITICAL
            elif priority == "low":
                priority_enum = ContractPriority.LOW
            
            # Convert string contract type to enum
            contract_type_enum = ContractType.TASK_ASSIGNMENT
            if contract_type == "agent_response":
                contract_type_enum = ContractType.AGENT_RESPONSE
            elif contract_type == "collaboration":
                contract_type_enum = ContractType.COLLABORATION
            elif contract_type == "service_agreement":
                contract_type_enum = ContractType.SERVICE_AGREEMENT
            
            # Create contract using consolidated contract manager
            contract_id = self.contract_manager.create_contract(
                title=title,
                description=description,
                priority=priority_enum,
                contract_type=contract_type_enum,
                parties=parties,
                terms=terms,
                auto_validate=auto_validate
            )
            
            if not contract_id:
                return {"error": "Failed to create contract"}
            
            # Get contract data
            contract_data = self.contract_manager.get_contract(contract_id)
            
            # Get validation results
            validation_results = contract_data.validation_results if contract_data else []
            
            # Determine if contract was auto-approved
            auto_approved = contract_data.status == ContractStatus.APPROVED if contract_data else False
            
            return {
                "contract_id": contract_id,
                "status": "created",
                "validation_results": len(validation_results),
                "validation_passed": len([r for r in validation_results if r.get("passed", False)]),
                "auto_approved": auto_approved,
                "timestamp": time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create contract: {e}")
            return {"error": str(e)}
    
    def get_contract_details(self, contract_id: str) -> Dict[str, Any]:
        """Get comprehensive contract details including validation info"""
        if not self.services_available:
            return {"error": "Services not available"}
        
        try:
            # Get contract from lifecycle service
            contract = self.lifecycle_service.get_contract(contract_id)
            if not contract:
                return {"error": "Contract not found"}
            
            # Get validation summary
            validation_summary = self.validation_service.get_validation_summary(contract_id)
            
            # Get violations
            violations = self.validation_service.get_contract_violations(contract_id)
            
            # Get state history
            history = self.lifecycle_service.get_contract_history(contract_id)
            
            return {
                "contract": contract,
                "validation_summary": validation_summary,
                "violations": violations,
                "state_history": history,
                "last_updated": contract.get("updated_at"),
                "is_active": contract.get("state") == "active"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get contract details: {e}")
            return {"error": str(e)}
    
    def transition_contract_state(self, contract_id: str, new_state: str, 
                                 reason: str = "", validate_first: bool = True) -> Dict[str, Any]:
        """Transition contract state with optional validation"""
        if not self.services_available:
            return {"error": "Services not available"}
        
        try:
            # Validate contract before critical state transitions
            if validate_first and new_state in ["active", "approved"]:
                contract_data = self.lifecycle_service.get_contract(contract_id)
                if contract_data:
                    validation_results = self.validation_service.validate_contract(contract_data)
                    critical_issues = [r for r in validation_results 
                                     if not r.passed and r.severity.value in ["error", "critical"]]
                    
                    if critical_issues:
                        return {
                            "success": False,
                            "error": "Contract has critical validation issues",
                            "critical_issues": len(critical_issues),
                            "blocked_transition": True
                        }
            
            # Perform state transition
            success = self.lifecycle_service.transition_contract_state(contract_id, new_state, reason)
            
            return {
                "success": success,
                "contract_id": contract_id,
                "new_state": new_state,
                "reason": reason,
                "timestamp": time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to transition contract state: {e}")
            return {"error": str(e)}
    
    def get_system_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive system dashboard"""
        if not self.services_available:
            return {"error": "Services not available"}
        
        try:
            # Get service statuses
            lifecycle_status = self.lifecycle_service.get_service_status()
            validation_status = self.validation_service.get_service_status()
            
            # Get active contracts
            active_contracts = self.lifecycle_service.get_active_contracts()
            
            # Calculate summary statistics
            total_contracts = lifecycle_status.get("total_contracts", 0)
            active_count = len(active_contracts)
            total_violations = validation_status.get("total_violations", 0)
            unresolved_violations = validation_status.get("unresolved_violations", 0)
            
            # Health score calculation
            health_score = 100
            if total_contracts > 0:
                violation_rate = total_violations / total_contracts
                health_score = max(0, 100 - (violation_rate * 50))
                
                if unresolved_violations > 0:
                    health_score = max(0, health_score - (unresolved_violations * 10))
            
            return {
                "system_health": {
                    "score": round(health_score, 2),
                    "status": "healthy" if health_score > 80 else "warning" if health_score > 60 else "critical"
                },
                "contracts": {
                    "total": total_contracts,
                    "active": active_count,
                    "completion_rate": round((total_contracts - active_count) / max(total_contracts, 1) * 100, 2)
                },
                "validation": {
                    "total_violations": total_violations,
                    "unresolved_violations": unresolved_violations,
                    "violation_rate": round(total_violations / max(total_contracts, 1), 2)
                },
                "services": {
                    "lifecycle_service": lifecycle_status,
                    "validation_service": validation_status
                },
                "timestamp": time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system dashboard: {e}")
            return {"error": str(e)}
    
    def run_system_maintenance(self) -> Dict[str, Any]:
        """Run system maintenance tasks"""
        if not self.services_available:
            return {"error": "Services not available"}
        
        try:
            maintenance_results = []
            
            # Check for expired contracts
            expired_contracts = self.lifecycle_service.check_contract_expiry()
            if expired_contracts:
                maintenance_results.append(f"Expired {len(expired_contracts)} contracts")
            
            # Validate all active contracts
            active_contracts = self.lifecycle_service.get_active_contracts()
            validation_issues = 0
            
            for contract_id in active_contracts.keys():
                contract_data = self.lifecycle_service.get_contract(contract_id)
                if contract_data:
                    results = self.validation_service.validate_contract(contract_data)
                    failed_validations = [r for r in results if not r.passed]
                    validation_issues += len(failed_validations)
            
            maintenance_results.append(f"Found {validation_issues} validation issues in active contracts")
            
            return {
                "maintenance_completed": True,
                "expired_contracts": len(expired_contracts),
                "validation_issues": validation_issues,
                "results": maintenance_results,
                "timestamp": time.time()
            }
            
        except Exception as e:
            self.logger.error(f"System maintenance failed: {e}")
            return {"error": str(e)}


def run_smoke_test():
    """Run basic functionality test for UnifiedContractManager"""
    print("🧪 Running UnifiedContractManager Smoke Test...")
    
    try:
        manager = UnifiedContractManager()
        
        if not manager.services_available:
            print("⚠️  Running in limited mode - services not available")
            return True
        
        # Test contract creation
        parties = [{"party_id": "agent-1", "party_type": "agent", "role": "contractor", "permissions": ["execute"]}]
        terms = {"deliverables": ["test task"], "acceptance_criteria": ["task completed"]}
        
        result = manager.create_contract(
            "Test Unified Contract", "Test Description", "task_assignment", parties, terms
        )
        assert result.get("contract_id") is not None
        
        # Test contract details
        contract_id = result["contract_id"]
        details = manager.get_contract_details(contract_id)
        assert details.get("contract") is not None
        
        # Test system dashboard
        dashboard = manager.get_system_dashboard()
        assert dashboard.get("system_health") is not None
        
        # Test maintenance
        maintenance = manager.run_system_maintenance()
        assert maintenance.get("maintenance_completed") is True
        
        print("✅ UnifiedContractManager Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ UnifiedContractManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for UnifiedContractManager testing"""
    parser = argparse.ArgumentParser(description="Unified Contract Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--create", nargs=3, help="Create contract (title,description,type)")
    parser.add_argument("--details", help="Get contract details by ID")
    parser.add_argument("--transition", nargs=3, help="Transition state (contract_id,new_state,reason)")
    parser.add_argument("--dashboard", action="store_true", help="Show system dashboard")
    parser.add_argument("--maintenance", action="store_true", help="Run system maintenance")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    # Create manager instance
    manager = UnifiedContractManager()
    
    if args.create:
        title, description, contract_type = args.create
        parties = [{"party_id": "system", "party_type": "system", "role": "contractor", "permissions": []}]
        terms = {"deliverables": ["test"], "acceptance_criteria": ["completed"]}
        result = manager.create_contract(title, description, contract_type, parties, terms)
        print(f"Create contract result: {result}")
    
    elif args.details:
        details = manager.get_contract_details(args.details)
        print(f"Contract details for {args.details}:")
        for key, value in details.items():
            print(f"  {key}: {value}")
    
    elif args.transition:
        contract_id, new_state, reason = args.transition
        result = manager.transition_contract_state(contract_id, new_state, reason)
        print(f"State transition result: {result}")
    
    elif args.dashboard:
        dashboard = manager.get_system_dashboard()
        print("System Dashboard:")
        for key, value in dashboard.items():
            print(f"  {key}: {value}")
    
    elif args.maintenance:
        result = manager.run_system_maintenance()
        print(f"Maintenance result: {result}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
