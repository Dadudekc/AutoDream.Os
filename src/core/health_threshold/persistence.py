#!/usr/bin/env python3
"""
Health Threshold Persistence - Agent_Cellphone_V2

Extracted persistence service for health threshold management.
Part of the HealthThresholdManager refactoring for SRP compliance.

Author: Agent-7 (Refactoring Specialist)
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from .models import HealthThreshold, ThresholdOperation, ValidationOperation, ConfigurationChange


class HealthThresholdPersistence:
    """Service for persisting health threshold data"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.persistence_dir = Path("data/persistent/health_thresholds")
        self.max_backups = 5
    
    def save_data(
        self,
        thresholds: Dict[str, HealthThreshold],
        threshold_operations: list,
        validation_operations: list,
        configuration_changes: list,
        manager_id: str,
        version: str = "2.0.0"
    ) -> bool:
        """Save health threshold management data to persistent storage"""
        try:
            # Create persistence directory if it doesn't exist
            self.persistence_dir.mkdir(parents=True, exist_ok=True)
            
            # Prepare data for persistence
            threshold_data = {
                "thresholds": {k: v.to_dict() for k, v in thresholds.items()},
                "threshold_operations": threshold_operations,
                "validation_operations": validation_operations,
                "configuration_changes": configuration_changes,
                "timestamp": datetime.now().isoformat(),
                "manager_id": manager_id,
                "version": version
            }
            
            # Save to JSON file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"health_thresholds_data_{timestamp}.json"
            filepath = self.persistence_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(threshold_data, f, indent=2, default=str)
            
            # Cleanup old backup files
            self._cleanup_old_backups()
            
            self.logger.info(f"Health threshold management data saved to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save health threshold management data: {e}")
            return False
    
    def load_data(self, filepath: str = None) -> Dict[str, Any]:
        """Load health threshold data from file"""
        try:
            if filepath is None:
                # Find the most recent backup file
                files = list(self.persistence_dir.glob("health_thresholds_data_*.json"))
                if not files:
                    return {}
                files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                filepath = str(files[0])
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Convert thresholds back to HealthThreshold objects
            if "thresholds" in data:
                thresholds = {}
                for k, v in data["thresholds"].items():
                    thresholds[k] = HealthThreshold.from_dict(v)
                data["thresholds"] = thresholds
            
            self.logger.info(f"Health threshold data loaded from {filepath}")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to load health threshold data: {e}")
            return {}
    
    def _cleanup_old_backups(self):
        """Clean up old backup files, keeping only the specified number"""
        try:
            files = list(self.persistence_dir.glob("health_thresholds_data_*.json"))
            if len(files) > self.max_backups:
                # Sort by modification time (oldest first)
                files.sort(key=lambda x: x.stat().st_mtime)
                # Remove oldest files
                for old_file in files[:-self.max_backups]:
                    old_file.unlink()
                    self.logger.debug(f"Removed old backup: {old_file}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup old backups: {e}")
    
    def get_backup_files(self) -> list:
        """Get list of available backup files"""
        try:
            files = list(self.persistence_dir.glob("health_thresholds_data_*.json"))
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return [str(f) for f in files]
        except Exception as e:
            self.logger.error(f"Failed to get backup files: {e}")
            return []
    
    def delete_backup_file(self, filepath: str) -> bool:
        """Delete a specific backup file"""
        try:
            file_path = Path(filepath)
            if file_path.exists() and file_path.name.startswith("health_thresholds_data_"):
                file_path.unlink()
                self.logger.info(f"Deleted backup file: {filepath}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to delete backup file {filepath}: {e}")
            return False
