#!/usr/bin/env python3
"""
Contract System Validator
=========================

Validates V3 contract system structure and dependencies.
V2 Compliance: ≤200 lines, focused responsibility, KISS principle.
"""

import json
from pathlib import Path
from typing import Dict, List, Any


class ContractSystemValidator:
    """Validates V3 contract system."""
    
    def __init__(self, agent_workspaces: Path):
        self.agent_workspaces = agent_workspaces
        self.team_alpha = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
    
    def validate(self) -> Dict[str, Any]:
        """Validate V3 contract system."""
        print("🔍 Validating V3 contract system...")
        
        contract_validation = {}
        
        for agent_id in self.team_alpha:
            agent_contracts = self._get_agent_contracts(agent_id)
            
            # Validate contract aspects
            validation_results = self._validate_contract_aspects(agent_contracts)
            
            contract_validation[agent_id] = {
                "contracts_count": len(agent_contracts),
                "dependencies_valid": validation_results["dependencies_valid"],
                "timelines_valid": validation_results["timelines_valid"],
                "priorities_valid": validation_results["priorities_valid"],
                "overall_valid": all(validation_results.values())
            }
        
        overall_valid = all(result["overall_valid"] for result in contract_validation.values())
        
        return {
            "category": "contract_system_validation",
            "status": "PASSED" if overall_valid else "FAILED",
            "results": contract_validation,
            "summary": f"Contract system: {'Valid' if overall_valid else 'Invalid'}"
        }
    
    def _get_agent_contracts(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get contracts for specific agent."""
        try:
            contracts_file = self.agent_workspaces / agent_id / "future_tasks.json"
            if not contracts_file.exists():
                return []
            
            with open(contracts_file, 'r') as f:
                contracts_data = json.load(f)
            
            return contracts_data.get("future_tasks", [])
            
        except Exception:
            return []
    
    def _validate_contract_aspects(self, contracts: List[Dict[str, Any]]) -> Dict[str, bool]:
        """Validate various aspects of contracts."""
        return {
            "dependencies_valid": self._validate_contract_dependencies(contracts),
            "timelines_valid": self._validate_cycle_timelines(contracts),
            "priorities_valid": self._validate_contract_priorities(contracts)
        }
    
    def _validate_contract_dependencies(self, contracts: List[Dict[str, Any]]) -> bool:
        """Validate contract dependencies."""
        try:
            contract_ids = {contract["task_id"] for contract in contracts}
            
            for contract in contracts:
                dependencies = contract.get("dependencies", [])
                for dep in dependencies:
                    if dep not in contract_ids and not dep.startswith("V3-"):
                        return False
            
            return True
            
        except Exception:
            return False
    
    def _validate_cycle_timelines(self, contracts: List[Dict[str, Any]]) -> bool:
        """Validate cycle-based timelines."""
        try:
            for contract in contracts:
                duration = contract.get("estimated_duration", "")
                if not duration.endswith("cycle") and not duration.endswith("cycles"):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _validate_contract_priorities(self, contracts: List[Dict[str, Any]]) -> bool:
        """Validate contract priorities."""
        valid_priorities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        
        try:
            for contract in contracts:
                priority = contract.get("priority", "")
                if priority not in valid_priorities:
                    return False
            
            return True
            
        except Exception:
            return False
