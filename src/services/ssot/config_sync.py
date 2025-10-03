#!/usr/bin/env python3
"""
Configuration Synchronization Tool
=================================

V2 Compliant: ≤400 lines, implements configuration synchronization
between JSON and YAML configuration files.

This module ensures consistency between different configuration
formats and automatically corrects inconsistencies.

🐝 WE ARE SWARM - SSOT System Optimization
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List
import logging
import shutil
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigSyncTool:
    """Synchronizes configuration files to maintain SSOT compliance."""
    
    def __init__(self, config_dir: str = "config"):
        """Initialize configuration sync tool."""
        self.config_dir = Path(config_dir)
        self.backup_dir = self.config_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    def sync_all_configs(self) -> Dict[str, Any]:
        """Synchronize all configuration files."""
        logger.info("Starting configuration synchronization")
        
        results = {
            "synced_files": [],
            "backups_created": [],
            "inconsistencies_fixed": [],
            "sync_timestamp": datetime.now().isoformat()
        }
        
        # Sync JSON and YAML configs
        json_file = self.config_dir / "unified_config.json"
        yaml_file = self.config_dir / "unified_config.yaml"
        
        if json_file.exists() and yaml_file.exists():
            sync_result = self._sync_json_yaml(json_file, yaml_file)
            if sync_result["synced"]:
                results["synced_files"].extend(sync_result["files"])
                results["backups_created"].extend(sync_result["backups"])
                results["inconsistencies_fixed"].extend(sync_result["fixes"])
        
        # Sync coordinates
        coord_file = self.config_dir / "coordinates.json"
        if coord_file.exists():
            coord_result = self._sync_coordinates(coord_file)
            if coord_result["synced"]:
                results["synced_files"].append(str(coord_file))
                results["backups_created"].extend(coord_result["backups"])
                results["inconsistencies_fixed"].extend(coord_result["fixes"])
        
        logger.info(f"Configuration sync complete. Fixed {len(results['inconsistencies_fixed'])} issues")
        return results
    
    def _sync_json_yaml(self, json_file: Path, yaml_file: Path) -> Dict[str, Any]:
        """Synchronize JSON and YAML configuration files."""
        logger.info("Synchronizing JSON and YAML configurations")
        
        result = {
            "synced": False,
            "files": [],
            "backups": [],
            "fixes": []
        }
        
        try:
            # Load both files
            with open(json_file, 'r', encoding='utf-8') as f:
                json_config = json.load(f)
            
            with open(yaml_file, 'r', encoding='utf-8') as f:
                yaml_config = yaml.safe_load(f)
            
            # Create backups
            backup_json = self._create_backup(json_file)
            backup_yaml = self._create_backup(yaml_file)
            result["backups"].extend([backup_json, backup_yaml])
            
            # Check for inconsistencies
            inconsistencies = self._find_inconsistencies(json_config, yaml_config)
            
            if inconsistencies:
                # Use JSON as source of truth
                self._update_yaml_from_json(yaml_file, json_config)
                result["fixes"].extend(inconsistencies)
                result["synced"] = True
                result["files"].extend([str(json_file), str(yaml_file)])
                logger.info(f"Fixed {len(inconsistencies)} inconsistencies")
            else:
                logger.info("No inconsistencies found")
                
        except Exception as e:
            logger.error(f"Error syncing JSON/YAML: {e}")
        
        return result
    
    def _sync_coordinates(self, coord_file: Path) -> Dict[str, Any]:
        """Synchronize coordinate configuration."""
        logger.info("Synchronizing coordinate configuration")
        
        result = {
            "synced": False,
            "backups": [],
            "fixes": []
        }
        
        try:
            # Load coordinates
            with open(coord_file, 'r', encoding='utf-8') as f:
                coord_config = json.load(f)
            
            # Create backup
            backup = self._create_backup(coord_file)
            result["backups"].append(backup)
            
            # Check for coordinate inconsistencies
            fixes = self._fix_coordinate_inconsistencies(coord_config)
            
            if fixes:
                # Save updated coordinates
                with open(coord_file, 'w', encoding='utf-8') as f:
                    json.dump(coord_config, f, indent=2, ensure_ascii=False)
                
                result["fixes"].extend(fixes)
                result["synced"] = True
                logger.info(f"Fixed {len(fixes)} coordinate inconsistencies")
            else:
                logger.info("No coordinate inconsistencies found")
                
        except Exception as e:
            logger.error(f"Error syncing coordinates: {e}")
        
        return result
    
    def _find_inconsistencies(self, json_config: Dict[str, Any], yaml_config: Dict[str, Any]) -> List[str]:
        """Find inconsistencies between JSON and YAML configs."""
        inconsistencies = []
        
        # Check agent roles
        if "agents" in json_config and "agents" in yaml_config:
            for agent_id in json_config["agents"]:
                if agent_id in yaml_config["agents"]:
                    json_role = json_config["agents"][agent_id].get("role")
                    yaml_role = yaml_config["agents"][agent_id].get("role")
                    if json_role != yaml_role:
                        inconsistencies.append(f"Role mismatch for {agent_id}: JSON={json_role}, YAML={yaml_role}")
        
        return inconsistencies
    
    def _fix_coordinate_inconsistencies(self, coord_config: Dict[str, Any]) -> List[str]:
        """Fix coordinate inconsistencies."""
        fixes = []
        
        # Standard coordinates for known agents
        standard_coords = {
            "Agent-7": [700, 938]  # Correct coordinates
        }
        
        for agent_id, coords in coord_config.items():
            if agent_id in standard_coords:
                expected_coords = standard_coords[agent_id]
                if coords.get("chat_input_coordinates") != expected_coords:
                    coords["chat_input_coordinates"] = expected_coords
                    fixes.append(f"Fixed {agent_id} coordinates to {expected_coords}")
        
        return fixes
    
    def _update_yaml_from_json(self, yaml_file: Path, json_config: Dict[str, Any]):
        """Update YAML file to match JSON configuration."""
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(json_config, f, default_flow_style=False, allow_unicode=True)
    
    def _create_backup(self, file_path: Path) -> str:
        """Create backup of configuration file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        
        return str(backup_path)
    
    def validate_sync(self) -> Dict[str, Any]:
        """Validate that synchronization was successful."""
        logger.info("Validating configuration synchronization")
        
        validation_results = {
            "json_yaml_consistent": False,
            "coordinates_consistent": False,
            "validation_timestamp": datetime.now().isoformat()
        }
        
        # Check JSON/YAML consistency
        json_file = self.config_dir / "unified_config.json"
        yaml_file = self.config_dir / "unified_config.yaml"
        
        if json_file.exists() and yaml_file.exists():
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_config = json.load(f)
                
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    yaml_config = yaml.safe_load(f)
                
                inconsistencies = self._find_inconsistencies(json_config, yaml_config)
                validation_results["json_yaml_consistent"] = len(inconsistencies) == 0
                
            except Exception as e:
                logger.error(f"Error validating JSON/YAML: {e}")
        
        return validation_results

def main():
    """Main execution function."""
    sync_tool = ConfigSyncTool()
    
    # Execute synchronization
    results = sync_tool.sync_all_configs()
    print(f"Configuration sync complete:")
    print(f"  Synced files: {len(results['synced_files'])}")
    print(f"  Backups created: {len(results['backups_created'])}")
    print(f"  Inconsistencies fixed: {len(results['inconsistencies_fixed'])}")
    
    # Validate results
    validation = sync_tool.validate_sync()
    print(f"Validation results:")
    print(f"  JSON/YAML consistent: {validation['json_yaml_consistent']}")

if __name__ == "__main__":
    main()
