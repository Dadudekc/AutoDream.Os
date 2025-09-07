#!/usr/bin/env python3
"""
Database Recovery Operations Module
==================================

Handles database recovery and repair operations.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from .database_audit_core import FileInfo, AuditResult


@dataclass
class RecoveryAction:
    """Container for recovery action information"""
    action_id: str
    action_type: str
    target_file: str
    description: str
    status: str
    timestamp: str
    details: Dict[str, Any]


class DatabaseRecoveryOps:
    """Database recovery operations handler"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.logger = self._setup_logging()
        self.recovery_actions: List[RecoveryAction] = []
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for recovery operations"""
        logger = logging.getLogger("DatabaseRecoveryOps")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[RECOVERY] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def create_backup(self, filepath: Path, backup_suffix: str = ".backup") -> bool:
        """Create a backup of the specified file"""
        try:
            if not filepath.exists():
                self.logger.warning(f"Cannot backup non-existent file: {filepath}")
                return False
            
            backup_path = filepath.with_suffix(filepath.suffix + backup_suffix)
            shutil.copy2(filepath, backup_path)
            
            action = RecoveryAction(
                action_id=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                action_type="backup",
                target_file=str(filepath),
                description=f"Created backup: {backup_path.name}",
                status="completed",
                timestamp=datetime.now().isoformat(),
                details={"backup_path": str(backup_path)}
            )
            self.recovery_actions.append(action)
            
            self.logger.info(f"Created backup: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create backup of {filepath}: {e}")
            return False
    
    def restore_from_backup(self, filepath: Path, backup_suffix: str = ".backup") -> bool:
        """Restore a file from its backup"""
        try:
            backup_path = filepath.with_suffix(filepath.suffix + backup_suffix)
            
            if not backup_path.exists():
                self.logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Create backup of current file if it exists
            if filepath.exists():
                self.create_backup(filepath, ".pre_restore")
            
            # Restore from backup
            shutil.copy2(backup_path, filepath)
            
            action = RecoveryAction(
                action_id=f"restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                action_type="restore",
                target_file=str(filepath),
                description=f"Restored from backup: {backup_path.name}",
                status="completed",
                timestamp=datetime.now().isoformat(),
                details={"backup_path": str(backup_path)}
            )
            self.recovery_actions.append(action)
            
            self.logger.info(f"Restored {filepath} from backup")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore {filepath} from backup: {e}")
            return False
    
    def repair_json_file(self, filepath: Path) -> bool:
        """Attempt to repair a corrupted JSON file"""
        try:
            if not filepath.exists():
                self.logger.warning(f"Cannot repair non-existent file: {filepath}")
                return False
            
            # Create backup before attempting repair
            self.create_backup(filepath, ".pre_repair")
            
            # Read file content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to parse JSON
            try:
                json.loads(content)
                self.logger.info(f"File {filepath} is already valid JSON")
                return True
            except json.JSONDecodeError as e:
                self.logger.info(f"Attempting to repair JSON file: {filepath}")
                
                # Basic JSON repair attempts
                repaired_content = self._attempt_json_repair(content)
                
                if repaired_content:
                    # Write repaired content
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(repaired_content)
                    
                    # Verify repair
                    try:
                        json.loads(repaired_content)
                        
                        action = RecoveryAction(
                            action_id=f"repair_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                            action_type="repair",
                            target_file=str(filepath),
                            description="Repaired corrupted JSON file",
                            status="completed",
                            timestamp=datetime.now().isoformat(),
                            details={"repair_method": "json_repair"}
                        )
                        self.recovery_actions.append(action)
                        
                        self.logger.info(f"Successfully repaired JSON file: {filepath}")
                        return True
                        
                    except json.JSONDecodeError:
                        self.logger.error(f"JSON repair failed for: {filepath}")
                        return False
                else:
                    self.logger.error(f"Could not repair JSON file: {filepath}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Failed to repair JSON file {filepath}: {e}")
            return False
    
    def _attempt_json_repair(self, content: str) -> Optional[str]:
        """Attempt to repair common JSON issues"""
        try:
            # Remove trailing commas
            content = content.replace(',}', '}').replace(',]', ']')
            
            # Fix common quote issues
            content = content.replace('"', '"').replace('"', '"')
            content = content.replace(''', "'").replace(''', "'")
            
            # Try to parse
            json.loads(content)
            return content
            
        except json.JSONDecodeError:
            # Try more aggressive repair
            try:
                # Remove problematic characters
                content = content.replace('\x00', '')
                content = content.replace('\r', '')
                
                # Try to find JSON boundaries
                start = content.find('{')
                end = content.rfind('}')
                
                if start != -1 and end != -1 and end > start:
                    content = content[start:end+1]
                    json.loads(content)
                    return content
                    
            except json.JSONDecodeError:
                pass
        
        return None
    
    def validate_file_integrity(self, filepath: Path) -> Dict[str, Any]:
        """Validate the integrity of a file"""
        try:
            validation_result = {
                "file_path": str(filepath),
                "exists": filepath.exists(),
                "readable": False,
                "valid_json": False,
                "size_bytes": 0,
                "integrity_score": 0.0,
                "issues": []
            }
            
            if not validation_result["exists"]:
                validation_result["issues"].append("File does not exist")
                return validation_result
            
            # Check readability
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    validation_result["readable"] = True
                    validation_result["size_bytes"] = len(content.encode('utf-8'))
            except Exception as e:
                validation_result["issues"].append(f"File not readable: {e}")
                return validation_result
            
            # Check JSON validity
            try:
                json.loads(content)
                validation_result["valid_json"] = True
            except json.JSONDecodeError as e:
                validation_result["issues"].append(f"Invalid JSON: {e}")
            
            # Calculate integrity score
            score = 0.0
            if validation_result["exists"]:
                score += 25.0
            if validation_result["readable"]:
                score += 25.0
            if validation_result["valid_json"]:
                score += 50.0
            
            validation_result["integrity_score"] = score
            
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Error validating file integrity for {filepath}: {e}")
            return {
                "file_path": str(filepath),
                "exists": False,
                "readable": False,
                "valid_json": False,
                "size_bytes": 0,
                "integrity_score": 0.0,
                "issues": [f"Validation error: {e}"]
            }
    
    def get_recovery_summary(self) -> Dict[str, Any]:
        """Get summary of all recovery actions"""
        total_actions = len(self.recovery_actions)
        completed_actions = sum(1 for a in self.recovery_actions if a.status == "completed")
        failed_actions = total_actions - completed_actions
        
        action_types = {}
        for action in self.recovery_actions:
            action_types[action.action_type] = action_types.get(action.action_type, 0) + 1
        
        return {
            "total_actions": total_actions,
            "completed_actions": completed_actions,
            "failed_actions": failed_actions,
            "success_rate": (completed_actions / total_actions * 100) if total_actions > 0 else 0,
            "action_types": action_types,
            "recent_actions": [
                {
                    "action_id": a.action_id,
                    "action_type": a.action_type,
                    "target_file": a.target_file,
                    "status": a.status,
                    "timestamp": a.timestamp
                }
                for a in sorted(self.recovery_actions, key=lambda x: x.timestamp, reverse=True)[:10]
            ]
        }
