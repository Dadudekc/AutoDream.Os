#!/usr/bin/env python3
"""
Configuration Backup Automation Script
=====================================

Infrastructure & DevOps support for CONFIG-ORGANIZE-001 mission.
Automates backup creation before configuration changes.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: CONFIG-ORGANIZE-001 - Configuration and Schema Management
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class ConfigurationBackupManager:
    """Manages configuration file backups with timestamping and validation."""
    
    def __init__(self, config_dir: str = "config", backup_dir: str = "config/backup"):
        self.config_dir = Path(config_dir)
        self.backup_dir = Path(backup_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = self.backup_dir / self.timestamp
        
    def create_backup(self) -> Dict[str, Any]:
        """Create timestamped backup of all configuration files."""
        backup_info = {
            "timestamp": self.timestamp,
            "backup_path": str(self.backup_path),
            "files_backed_up": [],
            "backup_size": 0,
            "status": "success"
        }
        
        try:
            # Create backup directory
            self.backup_path.mkdir(parents=True, exist_ok=True)
            
            # Find all config files
            config_files = self._find_config_files()
            
            # Backup each file
            for file_path in config_files:
                backup_file = self.backup_path / file_path.name
                shutil.copy2(file_path, backup_file)
                backup_info["files_backed_up"].append(str(file_path))
                backup_info["backup_size"] += file_path.stat().st_size
                
            # Create backup manifest
            self._create_backup_manifest(backup_info)
            
            print(f"✅ Configuration backup created: {self.backup_path}")
            print(f"📁 Files backed up: {len(backup_info['files_backed_up'])}")
            print(f"💾 Backup size: {backup_info['backup_size']} bytes")
            
        except Exception as e:
            backup_info["status"] = "error"
            backup_info["error"] = str(e)
            print(f"❌ Backup failed: {e}")
            
        return backup_info
    
    def _find_config_files(self) -> List[Path]:
        """Find all configuration files to backup."""
        config_extensions = ['.yaml', '.yml', '.json', '.toml', '.ini', '.cfg']
        config_files = []
        
        for file_path in self.config_dir.iterdir():
            if file_path.is_file() and file_path.suffix in config_extensions:
                config_files.append(file_path)
                
        return config_files
    
    def _create_backup_manifest(self, backup_info: Dict[str, Any]) -> None:
        """Create a manifest file for the backup."""
        manifest_path = self.backup_path / "backup_manifest.json"
        
        with open(manifest_path, 'w') as f:
            json.dump(backup_info, f, indent=2)
    
    def restore_backup(self, backup_timestamp: str) -> Dict[str, Any]:
        """Restore configuration from a specific backup."""
        restore_info = {
            "timestamp": backup_timestamp,
            "restore_path": str(self.backup_dir / backup_timestamp),
            "files_restored": [],
            "status": "success"
        }
        
        try:
            backup_path = self.backup_dir / backup_timestamp
            
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup {backup_timestamp} not found")
            
            # Read manifest
            manifest_path = backup_path / "backup_manifest.json"
            if manifest_path.exists():
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                    restore_info["files_restored"] = manifest["files_backed_up"]
            
            # Restore files
            for file_path in backup_path.iterdir():
                if file_path.is_file() and file_path.name != "backup_manifest.json":
                    target_path = self.config_dir / file_path.name
                    shutil.copy2(file_path, target_path)
                    
            print(f"✅ Configuration restored from backup: {backup_timestamp}")
            print(f"📁 Files restored: {len(restore_info['files_restored'])}")
            
        except Exception as e:
            restore_info["status"] = "error"
            restore_info["error"] = str(e)
            print(f"❌ Restore failed: {e}")
            
        return restore_info
    
    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups."""
        backups = []
        
        if not self.backup_dir.exists():
            return backups
            
        for backup_path in self.backup_dir.iterdir():
            if backup_path.is_dir():
                manifest_path = backup_path / "backup_manifest.json"
                backup_info = {
                    "timestamp": backup_path.name,
                    "path": str(backup_path),
                    "created": datetime.fromtimestamp(backup_path.stat().st_mtime).isoformat()
                }
                
                if manifest_path.exists():
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                        backup_info.update(manifest)
                        
                backups.append(backup_info)
                
        return sorted(backups, key=lambda x: x["timestamp"], reverse=True)

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Configuration Backup Automation")
    parser.add_argument("--action", choices=["backup", "restore", "list"], 
                       default="backup", help="Action to perform")
    parser.add_argument("--timestamp", help="Backup timestamp for restore")
    parser.add_argument("--config-dir", default="config", help="Configuration directory")
    parser.add_argument("--backup-dir", default="config/backup", help="Backup directory")
    
    args = parser.parse_args()
    
    backup_manager = ConfigurationBackupManager(args.config_dir, args.backup_dir)
    
    if args.action == "backup":
        result = backup_manager.create_backup()
        print(json.dumps(result, indent=2))
    elif args.action == "restore":
        if not args.timestamp:
            print("❌ Timestamp required for restore")
            return
        result = backup_manager.restore_backup(args.timestamp)
        print(json.dumps(result, indent=2))
    elif args.action == "list":
        backups = backup_manager.list_backups()
        print(json.dumps(backups, indent=2))

if __name__ == "__main__":
    main()
