#!/usr/bin/env python3
"""
SSOT Validator
==============

Validates Single Source of Truth compliance (Operating Order v1.0).
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Set

from ...agent_devlog_automation import auto_create_devlog

logger = logging.getLogger(__name__)


class SSOTValidator:
    """Validates Single Source of Truth compliance."""
    
    def __init__(self, agent_id: str, workspace_dir: Path):
        """Initialize SSOT validator."""
        self.agent_id = agent_id
        self.workspace_dir = workspace_dir
        self.project_root = workspace_dir.parent.parent.parent.parent
        self.ssot_registry_file = workspace_dir / "ssot_registry.json"
        self.ssot_violations_file = workspace_dir / "ssot_violations.json"
    
    async def validate_ssot_compliance(self) -> Dict[str, Any]:
        """Validate SSOT compliance across the project (Operating Order v1.0)."""
        try:
            results = {
                "compliant": True,
                "violations": [],
                "warnings": [],
                "registry_updated": False,
                "duplicate_files": [],
                "missing_registry_entries": [],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
            }
            
            # Check for duplicate files
            duplicates = await self._find_duplicate_files()
            results["duplicate_files"] = duplicates
            if duplicates:
                results["compliant"] = False
                results["violations"].extend([f"Duplicate file: {dup}" for dup in duplicates])
            
            # Check registry compliance
            registry_violations = await self._check_registry_compliance()
            results["missing_registry_entries"] = registry_violations
            if registry_violations:
                results["compliant"] = False
                results["violations"].extend([f"Missing registry entry: {violation}" for violation in registry_violations])
            
            # Check for side copies
            side_copies = await self._find_side_copies()
            if side_copies:
                results["compliant"] = False
                results["violations"].extend([f"Side copy detected: {copy}" for copy in side_copies])
            
            # Update registry
            await self._update_ssot_registry()
            results["registry_updated"] = True
            
            # Save violations
            await self._save_ssot_violations(results)
            
            # Create devlog
            await auto_create_devlog(
                self.agent_id,
                "SSOT compliance validation",
                "completed" if results["compliant"] else "failed",
                results
            )
            
            return results
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error validating SSOT compliance: {e}")
            return {
                "compliant": False,
                "violations": [str(e)],
                "warnings": [],
                "registry_updated": False,
                "duplicate_files": [],
                "missing_registry_entries": [],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
            }
    
    async def _find_duplicate_files(self) -> List[str]:
        """Find duplicate files that violate SSOT."""
        try:
            duplicates = []
            
            # Check for duplicate configuration files
            config_patterns = ["config*.json", "config*.yaml", "config*.yml", "settings*.json"]
            for pattern in config_patterns:
                files = list(self.project_root.glob(f"**/{pattern}"))
                file_names = {}
                for file_path in files:
                    name = file_path.name
                    if name in file_names:
                        duplicates.append(f"{name} found in {file_names[name]} and {file_path}")
                    else:
                        file_names[name] = file_path
            
            # Check for duplicate constants files
            constants_files = list(self.project_root.glob("**/constants*.py"))
            constants_names = {}
            for file_path in constants_files:
                name = file_path.name
                if name in constants_names:
                    duplicates.append(f"{name} found in {constants_names[name]} and {file_path}")
                else:
                    constants_names[name] = file_path
            
            # Check for duplicate registry files
            registry_files = list(self.project_root.glob("**/registry*.json"))
            if len(registry_files) > 1:
                duplicates.append(f"Multiple registry files: {[str(f) for f in registry_files]}")
            
            return duplicates
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error finding duplicate files: {e}")
            return []
    
    async def _check_registry_compliance(self) -> List[str]:
        """Check that all configuration files are registered."""
        try:
            violations = []
            
            # Load existing registry
            registry = await self._load_ssot_registry()
            
            # Check configuration files
            config_files = list(self.project_root.glob("**/config*.json"))
            config_files.extend(list(self.project_root.glob("**/config*.yaml")))
            config_files.extend(list(self.project_root.glob("**/config*.yml")))
            
            for config_file in config_files:
                relative_path = config_file.relative_to(self.project_root)
                if str(relative_path) not in registry.get("config_files", []):
                    violations.append(f"Unregistered config file: {relative_path}")
            
            # Check constants files
            constants_files = list(self.project_root.glob("**/constants*.py"))
            for constants_file in constants_files:
                relative_path = constants_file.relative_to(self.project_root)
                if str(relative_path) not in registry.get("constants_files", []):
                    violations.append(f"Unregistered constants file: {relative_path}")
            
            return violations
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error checking registry compliance: {e}")
            return []
    
    async def _find_side_copies(self) -> List[str]:
        """Find side copies that should use the main source."""
        try:
            side_copies = []
            
            # Check for backup files
            backup_files = list(self.project_root.glob("**/*.bak"))
            backup_files.extend(list(self.project_root.glob("**/*.backup")))
            backup_files.extend(list(self.project_root.glob("**/*.old")))
            
            for backup_file in backup_files:
                side_copies.append(f"Backup file: {backup_file}")
            
            # Check for temporary copies
            temp_files = list(self.project_root.glob("**/*.tmp"))
            temp_files.extend(list(self.project_root.glob("**/*.temp")))
            
            for temp_file in temp_files:
                side_copies.append(f"Temporary file: {temp_file}")
            
            # Check for copy files
            copy_files = list(self.project_root.glob("**/*copy*.py"))
            copy_files.extend(list(self.project_root.glob("**/*copy*.json")))
            
            for copy_file in copy_files:
                side_copies.append(f"Copy file: {copy_file}")
            
            return side_copies
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error finding side copies: {e}")
            return []
    
    async def _load_ssot_registry(self) -> Dict[str, Any]:
        """Load the SSOT registry."""
        try:
            if not self.ssot_registry_file.exists():
                return {
                    "config_files": [],
                    "constants_files": [],
                    "registry_files": [],
                    "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S")
                }
            
            with open(self.ssot_registry_file, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"{self.agent_id}: Error loading SSOT registry: {e}")
            return {}
    
    async def _update_ssot_registry(self) -> None:
        """Update the SSOT registry with current files."""
        try:
            registry = {
                "config_files": [],
                "constants_files": [],
                "registry_files": [],
                "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "agent_id": self.agent_id
            }
            
            # Scan configuration files
            config_files = list(self.project_root.glob("**/config*.json"))
            config_files.extend(list(self.project_root.glob("**/config*.yaml")))
            config_files.extend(list(self.project_root.glob("**/config*.yml")))
            
            for config_file in config_files:
                relative_path = config_file.relative_to(self.project_root)
                registry["config_files"].append(str(relative_path))
            
            # Scan constants files
            constants_files = list(self.project_root.glob("**/constants*.py"))
            for constants_file in constants_files:
                relative_path = constants_file.relative_to(self.project_root)
                registry["constants_files"].append(str(relative_path))
            
            # Scan registry files
            registry_files = list(self.project_root.glob("**/registry*.json"))
            for registry_file in registry_files:
                relative_path = registry_file.relative_to(self.project_root)
                registry["registry_files"].append(str(relative_path))
            
            # Save updated registry
            with open(self.ssot_registry_file, 'w') as f:
                json.dump(registry, f, indent=2)
            
            logger.info(f"{self.agent_id}: SSOT registry updated")
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error updating SSOT registry: {e}")
    
    async def _save_ssot_violations(self, results: Dict[str, Any]) -> None:
        """Save SSOT violations to file."""
        try:
            with open(self.ssot_violations_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"{self.agent_id}: SSOT violations saved")
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error saving SSOT violations: {e}")
    
    async def get_ssot_status(self) -> Dict[str, Any]:
        """Get current SSOT compliance status."""
        try:
            if not self.ssot_violations_file.exists():
                return {"status": "no_results", "message": "No SSOT validation results found"}
            
            with open(self.ssot_violations_file, 'r') as f:
                results = json.load(f)
            
            return {
                "status": "results_found",
                "compliant": results.get("compliant", False),
                "violations_count": len(results.get("violations", [])),
                "warnings_count": len(results.get("warnings", [])),
                "last_updated": results.get("timestamp", "unknown")
            }
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Error getting SSOT status: {e}")
            return {"status": "error", "message": str(e)}


