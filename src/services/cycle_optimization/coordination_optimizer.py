#!/usr/bin/env python3
"""
General Cycle Coordination Optimizer
====================================

V2 Compliant: ≤400 lines, implements coordination optimization
for all agent roles in the General Cycle.

This module optimizes coordination levels across all agent roles
to ensure maximum coordination for SSOT_MANAGER and appropriate
levels for other roles.

🐝 WE ARE SWARM - General Cycle Optimization
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoordinationOptimizer:
    """Optimizes coordination levels across all agent roles."""
    
    def __init__(self, config_dir: str = "config"):
        """Initialize coordination optimizer."""
        self.config_dir = Path(config_dir)
        self.coordination_levels = {
            "SSOT_MANAGER": "maximum",
            "CAPTAIN": "maximum",
            "COORDINATOR": "high",
            "QUALITY_ASSURANCE": "high",
            "INTEGRATION_SPECIALIST": "medium",
            "IMPLEMENTATION_SPECIALIST": "medium",
            "FINANCIAL_ANALYST": "low",
            "TRADING_STRATEGIST": "low",
            "RISK_MANAGER": "medium",
            "MARKET_RESEARCHER": "low",
            "PORTFOLIO_OPTIMIZER": "low",
            "COMPLIANCE_AUDITOR": "medium",
            "TASK_EXECUTOR": "low",
            "RESEARCHER": "low",
            "TROUBLESHOOTER": "medium",
            "OPTIMIZER": "low"
        }
        
    def optimize_all_roles(self) -> Dict[str, Any]:
        """Optimize coordination levels for all agent roles."""
        logger.info("Starting coordination level optimization")
        
        results = {
            "optimized_roles": [],
            "updated_files": [],
            "coordination_levels": self.coordination_levels
        }
        
        # Process all role protocol files
        protocol_dir = self.config_dir / "protocols"
        if protocol_dir.exists():
            for protocol_file in protocol_dir.glob("*.json"):
                if self._optimize_role_file(protocol_file):
                    results["optimized_roles"].append(protocol_file.stem)
                    results["updated_files"].append(str(protocol_file))
        
        logger.info(f"Optimized coordination for {len(results['optimized_roles'])} roles")
        return results
    
    def _optimize_role_file(self, protocol_file: Path) -> bool:
        """Optimize coordination levels in a role protocol file."""
        try:
            with open(protocol_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated = False
            role_name = data.get("role", "")
            
            # Get optimal coordination level for this role
            optimal_level = self.coordination_levels.get(role_name, "medium")
            
            # Update behavior adaptations
            if "behavior_adaptations" in data:
                if data["behavior_adaptations"].get("coordination_level") != optimal_level:
                    data["behavior_adaptations"]["coordination_level"] = optimal_level
                    updated = True
            
            # Update general cycle adaptations
            if "general_cycle_adaptations" in data:
                for phase, config in data["general_cycle_adaptations"].items():
                    if isinstance(config, dict) and "coordination_level" in config:
                        if config["coordination_level"] != optimal_level:
                            config["coordination_level"] = optimal_level
                            updated = True
            
            # Save updated file
            if updated:
                with open(protocol_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                logger.info(f"Updated coordination level in {protocol_file.name}")
                return True
                
        except Exception as e:
            logger.error(f"Error processing {protocol_file}: {e}")
            
        return False
    
    def validate_optimization(self) -> Dict[str, Any]:
        """Validate that coordination optimization was applied correctly."""
        logger.info("Validating coordination level optimization")
        
        validation_results = {
            "optimized_files": [],
            "non_optimized_files": [],
            "coordination_levels": self.coordination_levels
        }
        
        protocol_dir = self.config_dir / "protocols"
        if protocol_dir.exists():
            for protocol_file in protocol_dir.glob("*.json"):
                if self._validate_file(protocol_file):
                    validation_results["optimized_files"].append(str(protocol_file))
                else:
                    validation_results["non_optimized_files"].append(str(protocol_file))
        
        return validation_results
    
    def _validate_file(self, protocol_file: Path) -> bool:
        """Validate that a file has optimal coordination levels."""
        try:
            with open(protocol_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            role_name = data.get("role", "")
            optimal_level = self.coordination_levels.get(role_name, "medium")
            
            # Check behavior adaptations
            if "behavior_adaptations" in data:
                if data["behavior_adaptations"].get("coordination_level") != optimal_level:
                    return False
            
            # Check general cycle adaptations
            if "general_cycle_adaptations" in data:
                for config in data["general_cycle_adaptations"].values():
                    if isinstance(config, dict) and "coordination_level" in config:
                        if config["coordination_level"] != optimal_level:
                            return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating {protocol_file}: {e}")
            return False

def main():
    """Main execution function."""
    optimizer = CoordinationOptimizer()
    
    # Execute optimization
    results = optimizer.optimize_all_roles()
    print(f"Optimized coordination for {len(results['optimized_roles'])} roles")
    print(f"Updated {len(results['updated_files'])} files")
    
    # Validate results
    validation = optimizer.validate_optimization()
    print(f"Optimized files: {len(validation['optimized_files'])}")
    
    if validation['non_optimized_files']:
        print(f"Non-optimized files: {validation['non_optimized_files']}")

if __name__ == "__main__":
    main()
