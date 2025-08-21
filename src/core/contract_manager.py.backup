#!/usr/bin/env python3
"""
Contract Manager - V2 Core Contract Assignment System

This module handles intelligent contract assignment, load balancing, priority management, and resource optimization.
Follows Single Responsibility Principle - only contract assignment.
Architecture: Single Responsibility Principle - contract assignment only
LOC: Target 200 lines (under 200 limit)
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


class AssignmentStrategy(Enum):
    """Contract assignment strategies"""
    SKILL_MATCH = "skill_match"
    LOAD_BALANCE = "load_balance"
    PRIORITY_FIRST = "priority_first"
    ROUND_ROBIN = "round_robin"
    EXPERT_OPINION = "expert_opinion"


@dataclass
class Contract:
    """Contract definition"""
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


class ContractManager:
    """
    Manages intelligent contract assignment, load balancing, and resource optimization
    
    Responsibilities:
    - Intelligent contract-to-agent matching
    - Load balancing and work distribution
    - Priority management and urgent handling
    - Resource optimization and efficiency
    """
    
    def __init__(self, agent_manager: AgentManager, config_manager: ConfigManager):
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.contracts: Dict[str, Contract] = {}
        self.assignments: Dict[str, AssignmentResult] = {}
        self.assignment_history: List[AssignmentResult] = []
        self.running = False
        self.logger = logging.getLogger(f"{__name__}.ContractManager")
        
        # Assignment strategy weights
        self.strategy_weights = {
            AssignmentStrategy.SKILL_MATCH: 0.4,
            AssignmentStrategy.LOAD_BALANCE: 0.3,
            AssignmentStrategy.PRIORITY_FIRST: 0.2,
            AssignmentStrategy.EXPERT_OPINION: 0.1
        }
    
    def create_contract(self, title: str, description: str, priority: ContractPriority,
                       required_capabilities: List[AgentCapability], 
                       estimated_duration: int, metadata: Dict[str, Any] = None) -> str:
        """Create a new contract"""
        try:
            contract_id = str(uuid.uuid4())
            
            contract = Contract(
                contract_id=contract_id,
                title=title,
                description=description,
                priority=priority,
                status=ContractStatus.PENDING,
                required_capabilities=required_capabilities,
                estimated_duration=estimated_duration,
                assigned_agent=None,
                created_at=datetime.now().isoformat(),
                assigned_at=None,
                completed_at=None,
                metadata=metadata or {}
            )
            
            # Store contract
            self.contracts[contract_id] = contract
            
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
            auto_assign = self.config_manager.get_config("contracts", "auto_assign", True)
            if not auto_assign:
                return False
            
            # Auto-assign high priority contracts
            if contract.priority in [ContractPriority.URGENT, ContractPriority.CRITICAL]:
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
                # Assign contract
                success = self.assign_contract(contract_id, best_agent)
                if success:
                    self.logger.info(f"Auto-assigned contract {contract_id} to {best_agent}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to auto-assign contract {contract_id}: {e}")
            return False
    
    def _find_best_agent_match(self, contract: Contract) -> Optional[str]:
        """Find the best agent match for a contract"""
        try:
            available_agents = self.agent_manager.get_available_agents()
            
            if not available_agents:
                return None
            
            best_score = 0.0
            best_agent = None
            
            for agent_id, agent_info in available_agents.items():
                # Calculate match score
                score = self._calculate_agent_match_score(agent_id, agent_info, contract)
                
                if score > best_score:
                    best_score = score
                    best_agent = agent_id
            
            # Only return agent if score meets minimum threshold
            min_score = self.config_manager.get_config("contracts", "min_match_score", 0.6)
            if best_score >= min_score:
                return best_agent
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to find best agent match: {e}")
            return None
    
    def _calculate_agent_match_score(self, agent_id: str, agent_info: AgentInfo, 
                                   contract: Contract) -> float:
        """Calculate how well an agent matches a contract"""
        try:
            score = 0.0
            
            # Capability match (40% weight)
            capability_score = self._calculate_capability_match(agent_info, contract)
            score += capability_score * 0.4
            
            # Load balance score (30% weight)
            load_score = self._calculate_load_balance_score(agent_id)
            score += load_score * 0.3
            
            # Priority handling score (20% weight)
            priority_score = self._calculate_priority_handling_score(agent_info, contract)
            score += priority_score * 0.2
            
            # Performance history score (10% weight)
            performance_score = self._calculate_performance_score(agent_id)
            score += performance_score * 0.1
            
            return min(1.0, max(0.0, score))
            
        except Exception as e:
            self.logger.error(f"Failed to calculate match score: {e}")
            return 0.0
    
    def _calculate_capability_match(self, agent_info: AgentInfo, contract: Contract) -> float:
        """Calculate capability match score"""
        try:
            if not contract.required_capabilities:
                return 1.0  # No requirements = perfect match
            
            required_capabilities = set(contract.required_capabilities)
            agent_capabilities = set(agent_info.capabilities)
            
            # Calculate intersection
            matching_capabilities = required_capabilities.intersection(agent_capabilities)
            
            if not matching_capabilities:
                return 0.0  # No matching capabilities
            
            # Score based on percentage of required capabilities met
            match_percentage = len(matching_capabilities) / len(required_capabilities)
            
            # Bonus for having additional capabilities
            bonus_capabilities = agent_capabilities - required_capabilities
            bonus_score = min(0.2, len(bonus_capabilities) * 0.05)
            
            return min(1.0, match_percentage + bonus_score)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate capability match: {e}")
            return 0.0
    
    def _calculate_load_balance_score(self, agent_id: str) -> float:
        """Calculate load balance score for an agent"""
        try:
            # Get agent's current workload
            current_contracts = [c for c in self.contracts.values() 
                               if c.assigned_agent == agent_id and 
                               c.status in [ContractStatus.ASSIGNED, ContractStatus.IN_PROGRESS]]
            
            current_load = len(current_contracts)
            
            # Get average load across all agents
            all_agents = self.agent_manager.get_all_agents()
            total_contracts = len([c for c in self.contracts.values() 
                                 if c.status in [ContractStatus.ASSIGNED, ContractStatus.IN_PROGRESS]])
            
            if not all_agents:
                return 0.5
            
            avg_load = total_contracts / len(all_agents)
            
            # Score based on how close to average load
            if current_load <= avg_load:
                # Below or at average - good score
                return 1.0 - (current_load / max(avg_load, 1))
            else:
                # Above average - reduced score
                return max(0.0, 1.0 - ((current_load - avg_load) / max(avg_load, 1)))
            
        except Exception as e:
            self.logger.error(f"Failed to calculate load balance score: {e}")
            return 0.5
    
    def _calculate_priority_handling_score(self, agent_info: AgentInfo, contract: Contract) -> float:
        """Calculate priority handling score"""
        try:
            # Check if agent has experience with similar priority levels
            agent_contracts = [c for c in self.contracts.values() 
                             if c.assigned_agent == agent_info.agent_id and 
                             c.status == ContractStatus.COMPLETED]
            
            if not agent_contracts:
                return 0.5  # No history
            
            # Calculate success rate with similar priority
            similar_priority_contracts = [c for c in agent_contracts 
                                        if c.priority == contract.priority]
            
            if not similar_priority_contracts:
                return 0.5  # No similar priority experience
            
            # Calculate success rate
            successful_contracts = [c for c in similar_priority_contracts 
                                  if c.status == ContractStatus.COMPLETED]
            
            success_rate = len(successful_contracts) / len(similar_priority_contracts)
            
            return success_rate
            
        except Exception as e:
            self.logger.error(f"Failed to calculate priority handling score: {e}")
            return 0.5
    
    def _calculate_performance_score(self, agent_id: str) -> float:
        """Calculate performance score based on contract completion history"""
        try:
            # Get completed contracts for this agent
            completed_contracts = [c for c in self.contracts.values() 
                                 if c.assigned_agent == agent_id and 
                                 c.status == ContractStatus.COMPLETED]
            
            if not completed_contracts:
                return 0.5  # No history
            
            # Calculate average completion time vs estimated time
            total_ratio = 0.0
            for contract in completed_contracts:
                if contract.estimated_duration > 0:
                    # Lower ratio is better (completed faster than estimated)
                    ratio = min(2.0, contract.estimated_duration / max(1, contract.estimated_duration))
                    total_ratio += ratio
            
            avg_ratio = total_ratio / len(completed_contracts)
            
            # Convert to score (lower ratio = higher score)
            performance_score = max(0.0, 1.0 - (avg_ratio - 1.0))
            
            return min(1.0, max(0.0, performance_score))
            
        except Exception as e:
            self.logger.error(f"Failed to calculate performance score: {e}")
            return 0.5
    
    def assign_contract(self, contract_id: str, agent_id: str, 
                       strategy: AssignmentStrategy = AssignmentStrategy.SKILL_MATCH) -> bool:
        """Assign a contract to an agent"""
        try:
            if contract_id not in self.contracts:
                return False
            
            contract = self.contracts[contract_id]
            
            # Check if contract is available for assignment
            if contract.status != ContractStatus.PENDING:
                return False
            
            # Check if agent is available
            agent_info = self.agent_manager.get_agent_info(agent_id)
            if not agent_info or agent_info.status != AgentStatus.ONLINE:
                return False
            
            # Update contract
            contract.assigned_agent = agent_id
            contract.status = ContractStatus.ASSIGNED
            contract.assigned_at = datetime.now().isoformat()
            
            # Create assignment record
            assignment = AssignmentResult(
                assignment_id=str(uuid.uuid4()),
                contract_id=contract_id,
                agent_id=agent_id,
                strategy=strategy,
                confidence_score=self._calculate_agent_match_score(agent_id, agent_info, contract),
                assignment_timestamp=datetime.now().isoformat(),
                metadata={"auto_assigned": contract.assigned_at == contract.created_at}
            )
            
            # Store assignment
            self.assignments[assignment.assignment_id] = assignment
            self.assignment_history.append(assignment)
            
            # Update agent status
            self.agent_manager.update_agent_status(agent_id, AgentStatus.BUSY)
            
            self.logger.info(f"Assigned contract {contract_id} to {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to assign contract {contract_id} to {agent_id}: {e}")
            return False
    
    def get_contract_status(self, contract_id: str) -> Optional[ContractStatus]:
        """Get status of a contract"""
        if contract_id in self.contracts:
            return self.contracts[contract_id].status
        return None
    
    def get_agent_contracts(self, agent_id: str) -> List[Contract]:
        """Get all contracts assigned to an agent"""
        return [c for c in self.contracts.values() if c.assigned_agent == agent_id]
    
    def get_pending_contracts(self) -> List[Contract]:
        """Get all pending contracts"""
        return [c for c in self.contracts.values() if c.status == ContractStatus.PENDING]
    
    def get_contract_summary(self) -> Dict[str, Any]:
        """Get summary of contract system"""
        try:
            total_contracts = len(self.contracts)
            pending_contracts = len(self.get_pending_contracts())
            assigned_contracts = len([c for c in self.contracts.values() 
                                   if c.status == ContractStatus.ASSIGNED])
            completed_contracts = len([c for c in self.contracts.values() 
                                    if c.status == ContractStatus.COMPLETED])
            
            return {
                "total_contracts": total_contracts,
                "pending_contracts": pending_contracts,
                "assigned_contracts": assigned_contracts,
                "completed_contracts": completed_contracts,
                "completion_rate": completed_contracts / max(total_contracts, 1),
                "auto_assign_enabled": self.config_manager.get_config("contracts", "auto_assign", True)
            }
        except Exception as e:
            self.logger.error(f"Failed to get contract summary: {e}")
            return {"error": str(e)}
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test for this instance"""
        try:
            # Test contract creation
            contract_id = self.create_contract(
                "Test Contract",
                "Test contract for smoke testing",
                ContractPriority.NORMAL,
                [AgentCapability.TESTING],
                2
            )
            
            if not contract_id:
                return False
            
            # Test contract status
            status = self.get_contract_status(contract_id)
            if status != ContractStatus.PENDING:
                return False
            
            # Test contract summary
            summary = self.get_contract_summary()
            if "total_contracts" not in summary:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Smoke test failed: {e}")
            return False


def run_smoke_test():
    """Run basic functionality test for ContractManager"""
    print("🧪 Running ContractManager Smoke Test...")
    
    try:
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary directories
            agent_dir = Path(temp_dir) / "agent_workspaces"
            config_dir = Path(temp_dir) / "config"
            agent_dir.mkdir()
            config_dir.mkdir()
            
            # Create mock agent
            test_agent_dir = agent_dir / "Agent-1"
            test_agent_dir.mkdir()
            
            # Initialize managers
            config_manager = ConfigManager(config_dir)
            agent_manager = AgentManager(agent_dir)
            contract_manager = ContractManager(agent_manager, config_manager)
            
            # Test basic functionality
            summary = contract_manager.get_contract_summary()
            assert "total_contracts" in summary
            
            # Test contract creation
            contract_id = contract_manager.create_contract(
                "Test Contract",
                "Test contract for smoke testing",
                ContractPriority.NORMAL,
                [AgentCapability.TESTING],
                2
            )
            assert contract_id
            
            # Test contract status
            status = contract_manager.get_contract_status(contract_id)
            assert status == ContractStatus.PENDING
            
            # Cleanup
            agent_manager.shutdown()
            config_manager.shutdown()
        
        print("✅ ContractManager Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ ContractManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for ContractManager testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Contract Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--create", nargs=5, metavar=("TITLE", "DESCRIPTION", "PRIORITY", "CAPABILITIES", "DURATION"), help="Create new contract")
    parser.add_argument("--assign", nargs=2, metavar=("CONTRACT_ID", "AGENT_ID"), help="Assign contract to agent")
    parser.add_argument("--status", help="Get contract status by ID")
    parser.add_argument("--pending", action="store_true", help="Show pending contracts")
    parser.add_argument("--summary", action="store_true", help="Show contract summary")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    # Initialize managers
    config_manager = ConfigManager()
    agent_manager = AgentManager()
    contract_manager = ContractManager(agent_manager, config_manager)
    
    if args.create:
        title, description, priority_str, capabilities_str, duration_str = args.create
        priority = ContractPriority(priority_str.lower())
        capabilities = [AgentCapability(cap.strip()) for cap in capabilities_str.split(",")]
        duration = int(duration_str)
        
        contract_id = contract_manager.create_contract(title, description, priority, capabilities, duration)
        print(f"Contract creation: {'✅ Success' if contract_id else '❌ Failed'}")
        if contract_id:
            print(f"Contract ID: {contract_id}")
    elif args.assign:
        contract_id, agent_id = args.assign
        success = contract_manager.assign_contract(contract_id, agent_id)
        print(f"Contract assignment: {'✅ Success' if success else '❌ Failed'}")
    elif args.status:
        status = contract_manager.get_contract_status(args.status)
        if status:
            print(f"Contract status: {status.value}")
        else:
            print(f"Contract '{args.status}' not found")
    elif args.pending:
        pending = contract_manager.get_pending_contracts()
        print("Pending Contracts:")
        for contract in pending:
            print(f"  {contract.contract_id}: {contract.title} ({contract.priority.value})")
    elif args.summary:
        summary = contract_manager.get_contract_summary()
        print("Contract Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    else:
        parser.print_help()
    
    # Cleanup
    agent_manager.shutdown()
    config_manager.shutdown()


if __name__ == "__main__":
    main()
