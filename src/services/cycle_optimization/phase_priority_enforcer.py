#!/usr/bin/env python3
"""
General Cycle Phase Priority Consistency Enforcer
=================================================

V2 Compliant: ≤400 lines, implements phase priority consistency
across all agent roles in the General Cycle.

This module ensures consistent phase priorities (CRITICAL/HIGH/MEDIUM)
across all agent roles to prevent priority confusion and improve
coordination efficiency.

🐝 WE ARE SWARM - General Cycle Optimization
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PhasePriorityEnforcer:
    """Enforces consistent phase priorities across all agent roles."""
    
    def __init__(self, config_dir: str = "config"):
        """Initialize phase priority enforcer."""
        self.config_dir = Path(config_dir)
        self.standard_priorities = {
            "check_inbox": "CRITICAL",
            "evaluate_tasks": "HIGH", 
            "execute_role": "HIGH",
            "quality_gates": "HIGH",
            "cycle_done": "CRITICAL"
        }
        
    def enforce_all_roles(self) -> Dict[str, Any]:
        """Enforce phase priority consistency for all agent roles."""
        logger.info("Starting phase priority consistency enforcement")
        
        results = {
            "enforced_roles": [],
            "updated_files": [],
            "standard_priorities": self.standard_priorities
        }
        
        # Process all role protocol files
        protocol_dir = self.config_dir / "protocols"
        if protocol_dir.exists():
            for protocol_file in protocol_dir.glob("*.json"):
                if self._enforce_role_file(protocol_file):
                    results["enforced_roles"].append(protocol_file.stem)
                    results["updated_files"].append(str(protocol_file))
        
        logger.info(f"Enforced priorities for {len(results['enforced_roles'])} roles")
        return results
    
    def _enforce_role_file(self, protocol_file: Path) -> bool:
        """Enforce phase priorities in a role protocol file."""
        try:
            with open(protocol_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated = False
            
            # Enforce general cycle adaptations
            if "general_cycle_adaptations" in data:
                for phase, config in data["general_cycle_adaptations"].items():
                    if isinstance(config, dict) and "priority" in config:
                        standard_priority = self.standard_priorities.get(phase)
                        if standard_priority and config["priority"] != standard_priority:
                            config["priority"] = standard_priority
                            updated = True
            
            # Save updated file
            if updated:
                with open(protocol_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                logger.info(f"Updated phase priorities in {protocol_file.name}")
                return True
                
        except Exception as e:
            logger.error(f"Error processing {protocol_file}: {e}")
            
        return False
    
    def validate_consistency(self) -> Dict[str, Any]:
        """Validate that phase priorities are consistent."""
        logger.info("Validating phase priority consistency")
        
        validation_results = {
            "consistent_files": [],
            "inconsistent_files": [],
            "standard_priorities": self.standard_priorities
        }
        
        protocol_dir = self.config_dir / "protocols"
        if protocol_dir.exists():
            for protocol_file in protocol_dir.glob("*.json"):
                if self._validate_file(protocol_file):
                    validation_results["consistent_files"].append(str(protocol_file))
                else:
                    validation_results["inconsistent_files"].append(str(protocol_file))
        
        return validation_results
    
    def _validate_file(self, protocol_file: Path) -> bool:
        """Validate that a file has consistent phase priorities."""
        try:
            with open(protocol_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check general cycle adaptations
            if "general_cycle_adaptations" in data:
                for phase, config in data["general_cycle_adaptations"].items():
                    if isinstance(config, dict) and "priority" in config:
                        standard_priority = self.standard_priorities.get(phase)
                        if standard_priority and config["priority"] != standard_priority:
                            return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating {protocol_file}: {e}")
            return False

def main():
    """Main execution function."""
    enforcer = PhasePriorityEnforcer()
    
    # Execute enforcement
    results = enforcer.enforce_all_roles()
    print(f"Enforced priorities for {len(results['enforced_roles'])} roles")
    print(f"Updated {len(results['updated_files'])} files")
    
    # Validate results
    validation = enforcer.validate_consistency()
    print(f"Consistent files: {len(validation['consistent_files'])}")
    
    if validation['inconsistent_files']:
        print(f"Inconsistent files: {validation['inconsistent_files']}")

if __name__ == "__main__":
    main()
