#!/usr/bin/env python3
"""
Role Consistency Enforcer
=========================

V2 Compliant: ≤400 lines, implements agent role consistency
enforcement across all system files.

This module ensures consistent agent role assignments and
automatically corrects role conflicts and inconsistencies.

🐝 WE ARE SWARM - SSOT System Optimization
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RoleConsistencyEnforcer:
    """Enforces consistent agent role assignments across all systems."""
    
    def __init__(self, project_root: str = "."):
        """Initialize role consistency enforcer."""
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "config"
        
        # Standard role assignments
        self.standard_roles = {
            "Agent-1": "INTEGRATION_SPECIALIST",
            "Agent-2": "ARCHITECTURE_SPECIALIST", 
            "Agent-3": "INFRASTRUCTURE_SPECIALIST",
            "Agent-4": "CAPTAIN",
            "Agent-5": "COORDINATOR",
            "Agent-6": "QUALITY_SPECIALIST",
            "Agent-7": "IMPLEMENTATION_SPECIALIST",
            "Agent-8": "SSOT_MANAGER"
        }
        
    def enforce_all_roles(self) -> Dict[str, Any]:
        """Enforce role consistency across all files."""
        logger.info("Starting role consistency enforcement")
        
        results = {
            "enforced_files": [],
            "role_corrections": [],
            "enforcement_timestamp": datetime.now().isoformat()
        }
        
        # Enforce in configuration files
        config_files = [
            self.config_dir / "unified_config.json",
            self.config_dir / "unified_config.yaml"
        ]
        
        for config_file in config_files:
            if config_file.exists():
                corrections = self._enforce_config_roles(config_file)
                if corrections:
                    results["enforced_files"].append(str(config_file))
                    results["role_corrections"].extend(corrections)
        
        # Enforce in documentation files
        doc_files = [
            self.project_root / "AGENT_ONBOARDING_CONTEXT_PACKAGE.md"
        ]
        
        for doc_file in doc_files:
            if doc_file.exists():
                corrections = self._enforce_doc_roles(doc_file)
                if corrections:
                    results["enforced_files"].append(str(doc_file))
                    results["role_corrections"].extend(corrections)
        
        logger.info(f"Role enforcement complete. Made {len(results['role_corrections'])} corrections")
        return results
    
    def _enforce_config_roles(self, config_file: Path) -> List[str]:
        """Enforce role consistency in configuration file."""
        logger.info(f"Enforcing roles in {config_file.name}")
        
        corrections = []
        
        try:
            # Load configuration
            if config_file.suffix == '.json':
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
            
            # Check and correct agent roles
            if "agents" in config:
                for agent_id, agent_config in config["agents"].items():
                    if isinstance(agent_config, dict) and "role" in agent_config:
                        current_role = agent_config["role"]
                        expected_role = self.standard_roles.get(agent_id)
                        
                        if expected_role and current_role != expected_role:
                            agent_config["role"] = expected_role
                            corrections.append(f"{agent_id}: {current_role} → {expected_role}")
            
            # Save corrected configuration
            if corrections:
                if config_file.suffix == '.json':
                    with open(config_file, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
                else:
                    with open(config_file, 'w', encoding='utf-8') as f:
                        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
                
                logger.info(f"Corrected {len(corrections)} roles in {config_file.name}")
                
        except Exception as e:
            logger.error(f"Error enforcing roles in {config_file}: {e}")
        
        return corrections
    
    def _enforce_doc_roles(self, doc_file: Path) -> List[str]:
        """Enforce role consistency in documentation file."""
        logger.info(f"Enforcing roles in {doc_file.name}")
        
        corrections = []
        
        try:
            # Read documentation content
            content = doc_file.read_text(encoding='utf-8')
            original_content = content
            
            # Correct Agent-6 role references
            if "Agent-6 (SSOT_MANAGER)" in content:
                content = content.replace("Agent-6 (SSOT_MANAGER)", "Agent-6 (QUALITY_SPECIALIST)")
                corrections.append("Agent-6: SSOT_MANAGER → QUALITY_SPECIALIST")
            
            # Ensure Agent-8 is correctly referenced as SSOT_MANAGER
            if "Agent-8" in content and "SSOT_MANAGER" not in content:
                # Add Agent-8 SSOT_MANAGER reference if missing
                content = content.replace("Agent-8", "Agent-8 (SSOT_MANAGER)")
                corrections.append("Added Agent-8 SSOT_MANAGER reference")
            
            # Save corrected documentation
            if content != original_content:
                doc_file.write_text(content, encoding='utf-8')
                logger.info(f"Corrected {len(corrections)} role references in {doc_file.name}")
                
        except Exception as e:
            logger.error(f"Error enforcing roles in {doc_file}: {e}")
        
        return corrections
    
    def validate_role_consistency(self) -> Dict[str, Any]:
        """Validate that all roles are consistent."""
        logger.info("Validating role consistency")
        
        validation_results = {
            "consistent_files": [],
            "inconsistent_files": [],
            "role_violations": [],
            "validation_timestamp": datetime.now().isoformat()
        }
        
        # Check configuration files
        config_files = [
            self.config_dir / "unified_config.json",
            self.config_dir / "unified_config.yaml"
        ]
        
        for config_file in config_files:
            if config_file.exists():
                violations = self._check_config_roles(config_file)
                if violations:
                    validation_results["inconsistent_files"].append(str(config_file))
                    validation_results["role_violations"].extend(violations)
                else:
                    validation_results["consistent_files"].append(str(config_file))
        
        # Check documentation files
        doc_files = [
            self.project_root / "AGENT_ONBOARDING_CONTEXT_PACKAGE.md"
        ]
        
        for doc_file in doc_files:
            if doc_file.exists():
                violations = self._check_doc_roles(doc_file)
                if violations:
                    validation_results["inconsistent_files"].append(str(doc_file))
                    validation_results["role_violations"].extend(violations)
                else:
                    validation_results["consistent_files"].append(str(doc_file))
        
        return validation_results
    
    def _check_config_roles(self, config_file: Path) -> List[str]:
        """Check role consistency in configuration file."""
        violations = []
        
        try:
            # Load configuration
            if config_file.suffix == '.json':
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
            
            # Check agent roles
            if "agents" in config:
                for agent_id, agent_config in config["agents"].items():
                    if isinstance(agent_config, dict) and "role" in agent_config:
                        current_role = agent_config["role"]
                        expected_role = self.standard_roles.get(agent_id)
                        
                        if expected_role and current_role != expected_role:
                            violations.append(f"{agent_id}: Expected {expected_role}, got {current_role}")
                            
        except Exception as e:
            logger.error(f"Error checking roles in {config_file}: {e}")
        
        return violations
    
    def _check_doc_roles(self, doc_file: Path) -> List[str]:
        """Check role consistency in documentation file."""
        violations = []
        
        try:
            content = doc_file.read_text(encoding='utf-8')
            
            # Check for incorrect Agent-6 references
            if "Agent-6 (SSOT_MANAGER)" in content:
                violations.append("Agent-6 incorrectly listed as SSOT_MANAGER")
            
            # Check for missing Agent-8 SSOT_MANAGER references
            if "SSOT_MANAGER" in content and "Agent-8 (SSOT_MANAGER)" not in content:
                violations.append("Missing Agent-8 SSOT_MANAGER reference")
                
        except Exception as e:
            logger.error(f"Error checking roles in {doc_file}: {e}")
        
        return violations

def main():
    """Main execution function."""
    enforcer = RoleConsistencyEnforcer()
    
    # Execute enforcement
    results = enforcer.enforce_all_roles()
    print(f"Role enforcement complete:")
    print(f"  Enforced files: {len(results['enforced_files'])}")
    print(f"  Role corrections: {len(results['role_corrections'])}")
    
    # Validate results
    validation = enforcer.validate_role_consistency()
    print(f"Validation results:")
    print(f"  Consistent files: {len(validation['consistent_files'])}")
    print(f"  Inconsistent files: {len(validation['inconsistent_files'])}")

if __name__ == "__main__":
    main()
