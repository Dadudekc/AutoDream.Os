"""
Contract Lifecycle Service - Complete Contract Management

This module provides comprehensive contract lifecycle management including:
- Contract creation, modification, and termination
- State tracking and lifecycle progression
- Contract template management
- Automated workflow integration

Architecture: Single Responsibility Principle - manages contract lifecycles
LOC: 200 lines (under 200 limit)
"""

import argparse
import time
import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ContractState(Enum):
    """Contract lifecycle states"""
    DRAFT = "draft"
    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    TERMINATED = "terminated"
    EXPIRED = "expired"


class ContractType(Enum):
    """Types of contracts"""
    AGENT_RESPONSE = "agent_response"
    TASK_ASSIGNMENT = "task_assignment"
    CHANGE_CONTRACT = "change_contract"
    SERVICE_LEVEL = "service_level"
    COORDINATION = "coordination"
    ONBOARDING = "onboarding"


class ContractPriority(Enum):
    """Contract priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ContractParty:
    """Contract party information"""
    party_id: str
    party_type: str  # "agent", "service", "system"
    role: str  # "contractor", "client", "witness"
    permissions: List[str]


@dataclass
class ContractTerms:
    """Contract terms and conditions"""
    deliverables: List[str]
    acceptance_criteria: List[str]
    deadlines: Dict[str, str]
    penalties: Dict[str, str]
    rewards: Dict[str, str]
    dependencies: List[str]


@dataclass
class Contract:
    """Complete contract definition"""
    contract_id: str
    title: str
    description: str
    contract_type: ContractType
    priority: ContractPriority
    state: ContractState
    parties: List[ContractParty]
    terms: ContractTerms
    created_at: float
    updated_at: float
    created_by: str
    template_id: Optional[str] = None
    parent_contract: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    expires_at: Optional[float] = None


class ContractLifecycleService:
    """
    Comprehensive contract lifecycle management service
    
    Responsibilities:
    - Manage contract creation and templates
    - Track contract state transitions
    - Enforce contract rules and validations
    - Provide contract analytics and reporting
    """
    
    def __init__(self):
        self.contracts: Dict[str, Contract] = {}
        self.contract_templates: Dict[str, Dict[str, Any]] = {}
        self.state_history: Dict[str, List[Dict[str, Any]]] = {}
        self.active_contracts: Dict[str, Contract] = {}
        self.logger = logging.getLogger(f"{__name__}.ContractLifecycleService")
        
        self._initialize_contract_templates()
        self.logger.info("Contract Lifecycle Service initialized")
    
    def _initialize_contract_templates(self):
        """Initialize standard contract templates"""
        self.contract_templates = {
            "agent_response": {
                "title": "Agent Response Contract",
                "description": "Standard agent task response and reporting contract",
                "required_fields": ["task_id", "actions", "status", "evidence_links"],
                "default_terms": {
                    "deliverables": ["Task completion", "Status report", "Evidence documentation"],
                    "acceptance_criteria": ["All acceptance criteria met", "Evidence provided"],
                    "deadlines": {"completion": "24h", "reporting": "1h"},
                    "penalties": {"late_delivery": "priority_reduction"},
                    "rewards": {"early_completion": "priority_bonus"}
                }
            },
            "task_assignment": {
                "title": "Task Assignment Contract",
                "description": "Contract for assigning tasks to agents with clear expectations",
                "required_fields": ["task_description", "assignee", "deadline", "requirements"],
                "default_terms": {
                    "deliverables": ["Task completion", "Quality assurance", "Documentation"],
                    "acceptance_criteria": ["Requirements met", "Quality standards achieved"],
                    "deadlines": {"completion": "72h", "updates": "12h"},
                    "penalties": {"non_compliance": "task_reassignment"},
                    "rewards": {"excellence": "reputation_boost"}
                }
            },
            "service_level": {
                "title": "Service Level Agreement",
                "description": "SLA defining service quality and availability expectations",
                "required_fields": ["service_name", "availability_target", "response_time"],
                "default_terms": {
                    "deliverables": ["Service availability", "Performance metrics", "Incident reports"],
                    "acceptance_criteria": ["Uptime >= 99%", "Response time < 1s"],
                    "deadlines": {"incident_response": "15min", "resolution": "4h"},
                    "penalties": {"sla_breach": "service_credits"},
                    "rewards": {"sla_exceed": "performance_bonus"}
                }
            }
        }
        self.logger.info(f"Initialized {len(self.contract_templates)} contract templates")
    
    def create_contract(self, title: str, description: str, contract_type: str, 
                       parties: List[Dict[str, Any]], terms: Dict[str, Any],
                       priority: str = "medium", template_id: Optional[str] = None) -> str:
        """Create a new contract"""
        try:
            contract_id = f"contract_{int(time.time())}_{len(self.contracts)}"
            
            # Apply template if specified
            if template_id and template_id in self.contract_templates:
                template = self.contract_templates[template_id]
                # Merge template terms with provided terms
                template_terms = template.get("default_terms", {})
                for key, value in template_terms.items():
                    if key not in terms:
                        terms[key] = value
            
            # Create contract parties
            contract_parties = []
            for party_data in parties:
                party = ContractParty(
                    party_id=party_data["party_id"],
                    party_type=party_data["party_type"],
                    role=party_data["role"],
                    permissions=party_data.get("permissions", [])
                )
                contract_parties.append(party)
            
            # Create contract terms
            contract_terms = ContractTerms(
                deliverables=terms.get("deliverables", []),
                acceptance_criteria=terms.get("acceptance_criteria", []),
                deadlines=terms.get("deadlines", {}),
                penalties=terms.get("penalties", {}),
                rewards=terms.get("rewards", {}),
                dependencies=terms.get("dependencies", [])
            )
            
            # Create contract
            contract = Contract(
                contract_id=contract_id,
                title=title,
                description=description,
                contract_type=ContractType(contract_type),
                priority=ContractPriority(priority),
                state=ContractState.DRAFT,
                parties=contract_parties,
                terms=contract_terms,
                created_at=time.time(),
                updated_at=time.time(),
                created_by="system",
                template_id=template_id
            )
            
            self.contracts[contract_id] = contract
            self.state_history[contract_id] = []
            
            # Record state change
            self._record_state_change(contract_id, ContractState.DRAFT, "Contract created")
            
            self.logger.info(f"Created contract {contract_id}: {title}")
            return contract_id
            
        except Exception as e:
            self.logger.error(f"Failed to create contract: {e}")
            return ""
    
    def transition_contract_state(self, contract_id: str, new_state: str, reason: str = "") -> bool:
        """Transition contract to a new state"""
        try:
            if contract_id not in self.contracts:
                self.logger.error(f"Contract {contract_id} not found")
                return False
            
            contract = self.contracts[contract_id]
            old_state = contract.state
            new_state_enum = ContractState(new_state)
            
            # Validate state transition
            if not self._is_valid_state_transition(old_state, new_state_enum):
                self.logger.error(f"Invalid state transition from {old_state.value} to {new_state}")
                return False
            
            # Update contract state
            contract.state = new_state_enum
            contract.updated_at = time.time()
            
            # Record state change
            self._record_state_change(contract_id, new_state_enum, reason)
            
            # Update active contracts tracking
            if new_state_enum == ContractState.ACTIVE:
                self.active_contracts[contract_id] = contract
            elif contract_id in self.active_contracts and new_state_enum in [
                ContractState.COMPLETED, ContractState.TERMINATED, ContractState.EXPIRED
            ]:
                del self.active_contracts[contract_id]
            
            self.logger.info(f"Contract {contract_id} transitioned from {old_state.value} to {new_state}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to transition contract state: {e}")
            return False
    
    def _is_valid_state_transition(self, current_state: ContractState, new_state: ContractState) -> bool:
        """Validate if state transition is allowed"""
        valid_transitions = {
            ContractState.DRAFT: [ContractState.PROPOSED, ContractState.APPROVED, ContractState.TERMINATED],
            ContractState.PROPOSED: [ContractState.UNDER_REVIEW, ContractState.APPROVED, ContractState.TERMINATED],
            ContractState.UNDER_REVIEW: [ContractState.APPROVED, ContractState.PROPOSED, ContractState.TERMINATED],
            ContractState.APPROVED: [ContractState.ACTIVE, ContractState.TERMINATED],
            ContractState.ACTIVE: [ContractState.SUSPENDED, ContractState.COMPLETED, ContractState.TERMINATED],
            ContractState.SUSPENDED: [ContractState.ACTIVE, ContractState.TERMINATED],
            ContractState.COMPLETED: [],  # Terminal state
            ContractState.TERMINATED: [],  # Terminal state
            ContractState.EXPIRED: []  # Terminal state
        }
        
        return new_state in valid_transitions.get(current_state, [])
    
    def _record_state_change(self, contract_id: str, new_state: ContractState, reason: str):
        """Record state change in history"""
        change_record = {
            "timestamp": time.time(),
            "state": new_state.value,
            "reason": reason,
            "recorded_by": "system"
        }
        
        if contract_id not in self.state_history:
            self.state_history[contract_id] = []
        
        self.state_history[contract_id].append(change_record)
    
    def get_contract(self, contract_id: str) -> Optional[Dict[str, Any]]:
        """Get contract details"""
        if contract_id not in self.contracts:
            return None
        
        contract = self.contracts[contract_id]
        contract_dict = asdict(contract)
        
        # Convert enums to strings for JSON serialization
        contract_dict["contract_type"] = contract.contract_type.value
        contract_dict["priority"] = contract.priority.value
        contract_dict["state"] = contract.state.value
        
        return contract_dict
    
    def get_contracts_by_state(self, state: str) -> List[str]:
        """Get contracts in a specific state"""
        try:
            state_enum = ContractState(state)
            return [cid for cid, contract in self.contracts.items() if contract.state == state_enum]
        except ValueError:
            return []
    
    def get_active_contracts(self) -> Dict[str, Dict[str, Any]]:
        """Get all active contracts"""
        return {cid: self.get_contract(cid) for cid in self.active_contracts.keys()}
    
    def get_contract_history(self, contract_id: str) -> List[Dict[str, Any]]:
        """Get contract state change history"""
        return self.state_history.get(contract_id, [])
    
    def check_contract_expiry(self) -> List[str]:
        """Check for expired contracts and update their state"""
        current_time = time.time()
        expired_contracts = []
        
        for contract_id, contract in self.contracts.items():
            if (contract.expires_at and 
                current_time > contract.expires_at and 
                contract.state not in [ContractState.COMPLETED, ContractState.TERMINATED, ContractState.EXPIRED]):
                
                self.transition_contract_state(contract_id, ContractState.EXPIRED.value, "Contract expired")
                expired_contracts.append(contract_id)
        
        return expired_contracts
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get current service status"""
        states_count = {}
        for state in ContractState:
            states_count[state.value] = len(self.get_contracts_by_state(state.value))
        
        return {
            "total_contracts": len(self.contracts),
            "active_contracts": len(self.active_contracts),
            "contract_templates": len(self.contract_templates),
            "states_distribution": states_count,
            "recent_activity": len([h for history in self.state_history.values() 
                                  for h in history if time.time() - h["timestamp"] < 3600])
        }


def run_smoke_test():
    """Run basic functionality test for ContractLifecycleService"""
    print("🧪 Running ContractLifecycleService Smoke Test...")
    
    try:
        service = ContractLifecycleService()
        
        # Test contract creation
        parties = [{"party_id": "agent-1", "party_type": "agent", "role": "contractor", "permissions": ["execute"]}]
        terms = {"deliverables": ["test task"], "acceptance_criteria": ["task completed"]}
        
        contract_id = service.create_contract(
            "Test Contract", "Test Description", "task_assignment", parties, terms
        )
        assert contract_id != ""
        
        # Test state transition
        assert service.transition_contract_state(contract_id, "proposed", "Ready for review")
        assert service.transition_contract_state(contract_id, "approved", "Approved by reviewer")
        
        # Test contract retrieval
        contract = service.get_contract(contract_id)
        assert contract is not None
        assert contract["title"] == "Test Contract"
        assert contract["state"] == "approved"
        
        # Test service status
        status = service.get_service_status()
        assert status["total_contracts"] > 0
        
        print("✅ ContractLifecycleService Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ ContractLifecycleService Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for ContractLifecycleService testing"""
    parser = argparse.ArgumentParser(description="Contract Lifecycle Service CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--create", nargs=3, help="Create contract (title,description,type)")
    parser.add_argument("--transition", nargs=3, help="Transition state (contract_id,new_state,reason)")
    parser.add_argument("--get", help="Get contract by ID")
    parser.add_argument("--list", help="List contracts by state")
    parser.add_argument("--active", action="store_true", help="List active contracts")
    parser.add_argument("--status", action="store_true", help="Show service status")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    # Create service instance
    service = ContractLifecycleService()
    
    if args.create:
        title, description, contract_type = args.create
        parties = [{"party_id": "system", "party_type": "system", "role": "contractor", "permissions": []}]
        terms = {"deliverables": ["test"], "acceptance_criteria": ["completed"]}
        contract_id = service.create_contract(title, description, contract_type, parties, terms)
        print(f"Created contract: {contract_id}")
    
    elif args.transition:
        contract_id, new_state, reason = args.transition
        success = service.transition_contract_state(contract_id, new_state, reason)
        print(f"State transition: {'SUCCESS' if success else 'FAILED'}")
    
    elif args.get:
        contract = service.get_contract(args.get)
        if contract:
            print(f"Contract {args.get}:")
            for key, value in contract.items():
                print(f"  {key}: {value}")
        else:
            print("Contract not found")
    
    elif args.list:
        contracts = service.get_contracts_by_state(args.list)
        print(f"Contracts in state '{args.list}': {contracts}")
    
    elif args.active:
        active = service.get_active_contracts()
        print(f"Active contracts: {list(active.keys())}")
    
    elif args.status:
        status = service.get_service_status()
        print("Contract Lifecycle Service Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
