#!/usr/bin/env python3
"""
Database Integrity Operations - EMERGENCY-RESTORE-004 Mission
============================================================

Database operations and file handling for integrity checking.
Part of the emergency system restoration mission for Agent-5.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional


class DatabaseOperations:
    """Database operations for integrity checking"""
    
    def __init__(self, task_list_path: str = "agent_workspaces/meeting/task_list.json"):
        self.task_list_path = Path(task_list_path)
        self.contracts = {}
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for database operations"""
        logger = logging.getLogger("DatabaseOperations")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def load_contracts(self) -> bool:
        """Load contracts from the task list file"""
        try:
            if not self.task_list_path.exists():
                self.logger.error(f"Task list file not found: {self.task_list_path}")
                return False
            
            with open(self.task_list_path, 'r') as f:
                self.contracts = json.load(f)
            
            self.logger.info(f"Loaded {self.contracts.get('total_contracts', 0)} contracts")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to load contracts: {e}")
            return False
    
    def save_contracts(self) -> bool:
        """Save contracts back to the task list file"""
        try:
            with open(self.task_list_path, 'w') as f:
                json.dump(self.contracts, f, indent=2)
            
            self.logger.info("Contracts saved successfully")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to save contracts: {e}")
            return False
    
    def get_contracts_data(self) -> Dict[str, Any]:
        """Get the loaded contracts data"""
        return self.contracts.copy()
    
    def validate_file_structure(self) -> Dict[str, Any]:
        """Validate the basic file structure"""
        validation_result = {
            "file_exists": self.task_list_path.exists(),
            "file_readable": False,
            "is_json": False,
            "has_required_sections": False,
            "error_message": None
        }
        
        if not validation_result["file_exists"]:
            validation_result["error_message"] = f"File not found: {self.task_list_path}"
            return validation_result
        
        try:
            # Test if file is readable
            with open(self.task_list_path, 'r') as f:
                content = f.read()
                validation_result["file_readable"] = True
            
            # Test if content is valid JSON
            json.loads(content)
            validation_result["is_json"] = True
            
            # Test if it has required sections
            data = json.loads(content)
            required_sections = ["total_contracts", "claimed_contracts", "completed_contracts", "available_contracts"]
            validation_result["has_required_sections"] = all(section in data for section in required_sections)
            
        except json.JSONDecodeError as e:
            validation_result["error_message"] = f"Invalid JSON: {e}"
        except Exception as e:
            validation_result["error_message"] = f"File read error: {e}"
        
        return validation_result
    
    def backup_contracts(self, backup_path: Optional[str] = None) -> bool:
        """Create a backup of the contracts file"""
        if backup_path is None:
            backup_path = f"{self.task_list_path}.backup"
        
        try:
            if self.task_list_path.exists():
                import shutil
                shutil.copy2(self.task_list_path, backup_path)
                self.logger.info(f"Backup created: {backup_path}")
                return True
            else:
                self.logger.warning("No file to backup")
                return False
        
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return False
    
    def restore_contracts(self, backup_path: str) -> bool:
        """Restore contracts from backup"""
        try:
            if not Path(backup_path).exists():
                self.logger.error(f"Backup file not found: {backup_path}")
                return False
            
            import shutil
            shutil.copy2(backup_path, self.task_list_path)
            self.logger.info(f"Contracts restored from: {backup_path}")
            
            # Reload the contracts
            return self.load_contracts()
        
        except Exception as e:
            self.logger.error(f"Failed to restore contracts: {e}")
            return False
    
    def get_file_info(self) -> Dict[str, Any]:
        """Get information about the contracts file"""
        if not self.task_list_path.exists():
            return {
                "exists": False,
                "size": 0,
                "modified": None,
                "error": "File not found"
            }
        
        try:
            stat = self.task_list_path.stat()
            return {
                "exists": True,
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "path": str(self.task_list_path),
                "error": None
            }
        except Exception as e:
            return {
                "exists": False,
                "size": 0,
                "modified": None,
                "error": str(e)
            }
