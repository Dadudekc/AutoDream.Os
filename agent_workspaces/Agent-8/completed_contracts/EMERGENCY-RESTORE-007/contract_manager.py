#!/usr/bin/env python3
"""
Contract Manager Module
======================

Handles contract generation and management operations.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

from .momentum_core import ContractMetrics, AccelerationMeasure


@dataclass
class ContractTemplate:
    """Contract template for generation"""
    template_id: str
    name: str
    description: str
    difficulty: str
    estimated_time: int  # minutes
    points_value: int
    skills_required: List[str]
    category: str


@dataclass
class GeneratedContract:
    """Generated contract instance"""
    contract_id: str
    template_id: str
    name: str
    description: str
    difficulty: str
    estimated_time: int
    points_value: int
    skills_required: List[str]
    category: str
    generated_at: str
    status: str = "available"
    claimed_by: Optional[str] = None
    claimed_at: Optional[str] = None
    completed_at: Optional[str] = None


class ContractManager:
    """Manages contract generation and lifecycle"""
    
    def __init__(self, contracts_dir: str = "contracts"):
        self.contracts_dir = Path(contracts_dir)
        self.logger = self._setup_logging()
        self.contract_templates: List[ContractTemplate] = []
        self.generated_contracts: List[GeneratedContract] = []
        self.contract_metrics = ContractMetrics(
            total_contracts=0,
            available_contracts=0,
            claimed_contracts=0,
            completed_contracts=0,
            completion_rate=0.0,
            extra_credit_points=0
        )
        
        self._load_contract_templates()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for contract operations"""
        logger = logging.getLogger("ContractManager")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[CONTRACT] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _load_contract_templates(self) -> None:
        """Load contract templates from configuration"""
        try:
            # Default templates for emergency scenarios
            default_templates = [
                ContractTemplate(
                    template_id="emergency_001",
                    name="Emergency System Recovery",
                    description="Immediate system recovery and stabilization",
                    difficulty="critical",
                    estimated_time=15,
                    points_value=500,
                    skills_required=["system_recovery", "emergency_response"],
                    category="emergency"
                ),
                ContractTemplate(
                    template_id="momentum_001",
                    name="Momentum Acceleration",
                    description="Implement momentum acceleration measures",
                    difficulty="high",
                    estimated_time=30,
                    points_value=750,
                    skills_required=["optimization", "acceleration"],
                    category="momentum"
                ),
                ContractTemplate(
                    template_id="optimization_001",
                    name="System Optimization",
                    description="Optimize system performance and efficiency",
                    difficulty="medium",
                    estimated_time=45,
                    points_value=600,
                    skills_required=["optimization", "analysis"],
                    category="optimization"
                )
            ]
            
            self.contract_templates.extend(default_templates)
            self.logger.info(f"Loaded {len(self.contract_templates)} contract templates")
            
        except Exception as e:
            self.logger.error(f"Error loading contract templates: {e}")
    
    def generate_contracts(self, count: int, category: Optional[str] = None) -> List[GeneratedContract]:
        """Generate specified number of contracts"""
        try:
            generated = []
            
            for i in range(count):
                # Select template based on category or random
                if category:
                    available_templates = [t for t in self.contract_templates if t.category == category]
                else:
                    available_templates = self.contract_templates
                
                if not available_templates:
                    self.logger.warning(f"No templates available for category: {category}")
                    break
                
                template = random.choice(available_templates)
                
                # Generate unique contract ID
                contract_id = f"{template.template_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}"
                
                contract = GeneratedContract(
                    contract_id=contract_id,
                    template_id=template.template_id,
                    name=template.name,
                    description=template.description,
                    difficulty=template.difficulty,
                    estimated_time=template.estimated_time,
                    points_value=template.points_value,
                    skills_required=template.skills_required.copy(),
                    category=template.category,
                    generated_at=datetime.now().isoformat()
                )
                
                generated.append(contract)
                self.generated_contracts.append(contract)
            
            # Update metrics
            self._update_contract_metrics()
            
            self.logger.info(f"Generated {len(generated)} contracts")
            return generated
            
        except Exception as e:
            self.logger.error(f"Error generating contracts: {e}")
            return []
    
    def claim_contract(self, contract_id: str, agent_id: str) -> bool:
        """Claim a contract for an agent"""
        try:
            contract = self._find_contract(contract_id)
            if not contract:
                self.logger.warning(f"Contract {contract_id} not found")
                return False
            
            if contract.status != "available":
                self.logger.warning(f"Contract {contract_id} is not available (status: {contract.status})")
                return False
            
            contract.status = "claimed"
            contract.claimed_by = agent_id
            contract.claimed_at = datetime.now().isoformat()
            
            # Update metrics
            self._update_contract_metrics()
            
            self.logger.info(f"Contract {contract_id} claimed by agent {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error claiming contract {contract_id}: {e}")
            return False
    
    def complete_contract(self, contract_id: str, agent_id: str) -> bool:
        """Mark a contract as completed"""
        try:
            contract = self._find_contract(contract_id)
            if not contract:
                self.logger.warning(f"Contract {contract_id} not found")
                return False
            
            if contract.status != "claimed":
                self.logger.warning(f"Contract {contract_id} is not claimed (status: {contract.status})")
                return False
            
            if contract.claimed_by != agent_id:
                self.logger.warning(f"Contract {contract_id} is claimed by different agent")
                return False
            
            contract.status = "completed"
            contract.completed_at = datetime.now().isoformat()
            
            # Update metrics
            self._update_contract_metrics()
            
            self.logger.info(f"Contract {contract_id} completed by agent {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error completing contract {contract_id}: {e}")
            return False
    
    def _find_contract(self, contract_id: str) -> Optional[GeneratedContract]:
        """Find contract by ID"""
        for contract in self.generated_contracts:
            if contract.contract_id == contract_id:
                return contract
        return None
    
    def _update_contract_metrics(self) -> None:
        """Update contract metrics based on current state"""
        try:
            total = len(self.generated_contracts)
            available = sum(1 for c in self.generated_contracts if c.status == "available")
            claimed = sum(1 for c in self.generated_contracts if c.status == "claimed")
            completed = sum(1 for c in self.generated_contracts if c.status == "completed")
            
            completion_rate = completed / total if total > 0 else 0.0
            extra_credit = sum(c.points_value for c in self.generated_contracts if c.status == "completed")
            
            self.contract_metrics = ContractMetrics(
                total_contracts=total,
                available_contracts=available,
                claimed_contracts=claimed,
                completed_contracts=completed,
                completion_rate=completion_rate,
                extra_credit_points=extra_credit
            )
            
        except Exception as e:
            self.logger.error(f"Error updating contract metrics: {e}")
    
    def get_available_contracts(self, agent_skills: Optional[List[str]] = None) -> List[GeneratedContract]:
        """Get list of available contracts, optionally filtered by skills"""
        try:
            available = [c for c in self.generated_contracts if c.status == "available"]
            
            if agent_skills:
                # Filter by skills (at least one skill match)
                filtered = []
                for contract in available:
                    if any(skill in contract.skills_required for skill in agent_skills):
                        filtered.append(contract)
                return filtered
            
            return available
            
        except Exception as e:
            self.logger.error(f"Error getting available contracts: {e}")
            return []
    
    def get_contract_summary(self) -> Dict[str, Any]:
        """Get summary of contract system status"""
        try:
            return {
                "metrics": asdict(self.contract_metrics),
                "total_templates": len(self.contract_templates),
                "total_generated": len(self.generated_contracts),
                "by_category": self._get_contracts_by_category(),
                "by_status": self._get_contracts_by_status(),
                "last_update": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting contract summary: {e}")
            return {"error": str(e)}
    
    def _get_contracts_by_category(self) -> Dict[str, int]:
        """Get count of contracts by category"""
        try:
            categories = {}
            for contract in self.generated_contracts:
                categories[contract.category] = categories.get(contract.category, 0) + 1
            return categories
        except Exception:
            return {}
    
    def _get_contracts_by_status(self) -> Dict[str, int]:
        """Get count of contracts by status"""
        try:
            statuses = {}
            for contract in self.generated_contracts:
                statuses[contract.status] = statuses.get(contract.status, 0) + 1
            return statuses
        except Exception:
            return {}
