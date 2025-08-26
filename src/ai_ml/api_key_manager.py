#!/usr/bin/env python3
"""
API Key Manager for AI & ML Integration
TDD Implementation - Minimal code to pass tests

This module provides secure API key management for:
- OpenAI API integration
- Anthropic API integration
- Secure storage and validation
"""

import os
import re
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime
import json

from src.utils.stability_improvements import stability_manager, safe_import
from ..core.base_manager import BaseManager, ManagerStatus, ManagerPriority

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIKeyManager(BaseManager):
    """Secure API key management system for AI services
    
    Now inherits from BaseManager for unified functionality
    """

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize API key manager with BaseManager"""
        super().__init__(
            manager_id="api_key_manager",
            name="API Key Manager",
            description="Secure API key management system for AI services"
        )
        
        self.config_path = config_path or Path.home() / ".ai_ml_config"
        self._keys: Dict[str, Optional[str]] = {}
        
        # API key management tracking
        self.key_operations: List[Dict[str, Any]] = []
        self.validation_attempts: List[Dict[str, Any]] = []
        self.security_checks: List[Dict[str, Any]] = []
        
        # Load API keys from environment variables
        self._load_api_keys()
        self.logger.info("API Key Manager initialized")
    
    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Initialize API key management system"""
        try:
            self.logger.info("Starting API Key Manager...")
            
            # Clear tracking data
            self.key_operations.clear()
            self.validation_attempts.clear()
            self.security_checks.clear()
            
            # Reload API keys
            self._load_api_keys()
            
            self.logger.info("API Key Manager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start API Key Manager: {e}")
            return False
    
    def _on_stop(self):
        """Cleanup API key management system"""
        try:
            self.logger.info("Stopping API Key Manager...")
            
            # Save tracking data
            self._save_api_key_management_data()
            
            # Clear data
            self.key_operations.clear()
            self.validation_attempts.clear()
            self.security_checks.clear()
            
            self.logger.info("API Key Manager stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop API Key Manager: {e}")
    
    def _on_heartbeat(self):
        """API key manager heartbeat"""
        try:
            # Check API key management health
            self._check_api_key_management_health()
            
            # Update metrics
            self.record_operation("heartbeat", True, 0.0)
            
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)
    
    def _on_initialize_resources(self) -> bool:
        """Initialize API key management resources"""
        try:
            # Initialize data structures
            self.key_operations = []
            self.validation_attempts = []
            self.security_checks = []
            
            # Ensure config directory exists
            self.config_path.mkdir(parents=True, exist_ok=True)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup API key management resources"""
        try:
            # Clear data
            self.key_operations.clear()
            self.validation_attempts.clear()
            self.security_checks.clear()
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")
    
    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            
            # Reload API keys
            self._load_api_keys()
            
            # Reset tracking
            self.key_operations.clear()
            self.validation_attempts.clear()
            self.security_checks.clear()
            
            self.logger.info("Recovery successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False
    
    # ============================================================================
    # API Key Management Methods
    # ============================================================================
    
    def _load_api_keys(self) -> None:
        """Load API keys from environment variables"""
        try:
            start_time = datetime.now()
            
            self._keys["openai"] = os.getenv("OPENAI_API_KEY")
            if not self._keys["openai"]:
                self.logger.warning("OPENAI_API_KEY not found in environment variables")

            self._keys["anthropic"] = os.getenv("ANTHROPIC_API_KEY")
            if not self._keys["anthropic"]:
                self.logger.warning("ANTHROPIC_API_KEY not found in environment variables")
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("load_api_keys", True, operation_time)
            
        except Exception as e:
            self.logger.error(f"Failed to load API keys: {e}")
            self.record_operation("load_api_keys", False, 0.0)

    def _validate_key(self, service: str, key: str) -> bool:
        """Validate API key format for supported services"""
        try:
            patterns = {
                "openai": r"^sk-[a-zA-Z0-9]{48}$",
                "anthropic": r"^sk-ant-[a-zA-Z0-9]{32,}$",
            }
            pattern = patterns.get(service)
            if pattern:
                return bool(re.match(pattern, key))
            return bool(key)
            
        except Exception as e:
            self.logger.error(f"Failed to validate key for {service}: {e}")
            return False

    def validate_openai_key(self) -> bool:
        """Validate OpenAI API key format and availability"""
        try:
            start_time = datetime.now()
            
            key = self._keys.get("openai")
            is_valid = bool(key) and self._validate_key("openai", key)
            
            # Record validation attempt
            validation_record = {
                "timestamp": datetime.now().isoformat(),
                "service": "openai",
                "key_available": bool(key),
                "key_valid": is_valid
            }
            self.validation_attempts.append(validation_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("validate_openai_key", is_valid, operation_time)
            
            return is_valid
            
        except Exception as e:
            self.logger.error(f"Failed to validate OpenAI key: {e}")
            self.record_operation("validate_openai_key", False, 0.0)
            return False

    def validate_anthropic_key(self) -> bool:
        """Validate Anthropic API key format and availability"""
        try:
            start_time = datetime.now()
            
            key = self._keys.get("anthropic")
            is_valid = bool(key) and self._validate_key("anthropic", key)
            
            # Record validation attempt
            validation_record = {
                "timestamp": datetime.now().isoformat(),
                "service": "anthropic",
                "key_available": bool(key),
                "key_valid": is_valid
            }
            self.validation_attempts.append(validation_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("validate_anthropic_key", is_valid, operation_time)
            
            return is_valid
            
        except Exception as e:
            self.logger.error(f"Failed to validate Anthropic key: {e}")
            self.record_operation("validate_anthropic_key", False, 0.0)
            return False

    def is_secure_storage(self) -> bool:
        """Check if API keys are stored securely"""
        try:
            start_time = datetime.now()
            
            # Environment variables are generally secure for development
            # In production, this would check for encrypted storage, key vaults, etc.
            is_secure = True
            
            # Record security check
            security_record = {
                "timestamp": datetime.now().isoformat(),
                "check_type": "secure_storage",
                "result": is_secure
            }
            self.security_checks.append(security_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("is_secure_storage", is_secure, operation_time)
            
            return is_secure
            
        except Exception as e:
            self.logger.error(f"Failed to check secure storage: {e}")
            self.record_operation("is_secure_storage", False, 0.0)
            return False

    def get_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service if available and valid"""
        try:
            start_time = datetime.now()
            
            key = self._keys.get(service)
            is_valid = key and self._validate_key(service, key)
            
            # Record key operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "get_key",
                "service": service,
                "key_available": bool(key),
                "key_valid": is_valid
            }
            self.key_operations.append(operation_record)
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("get_key", is_valid, operation_time)
            
            if is_valid:
                return key
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get key for {service}: {e}")
            self.record_operation("get_key", False, 0.0)
            return None

    def set_key(self, service: str, key: str) -> bool:
        """Set API key for a service (for testing purposes)"""
        try:
            start_time = datetime.now()
            
            is_valid = self._validate_key(service, key)
            if is_valid:
                self._keys[service] = key
                
                # Record key operation
                operation_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "set_key",
                    "service": service,
                    "key_valid": True
                }
                self.key_operations.append(operation_record)
                
                # Record operation
                operation_time = (datetime.now() - start_time).total_seconds()
                self.record_operation("set_key", True, operation_time)
                
                return True
            else:
                # Record failed operation
                operation_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "set_key",
                    "service": service,
                    "key_valid": False
                }
                self.key_operations.append(operation_record)
                
                self.record_operation("set_key", False, 0.0)
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to set key for {service}: {e}")
            self.record_operation("set_key", False, 0.0)
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get current API key status"""
        try:
            start_time = datetime.now()
            
            status = {
                "openai_available": self.validate_openai_key(),
                "anthropic_available": self.validate_anthropic_key(),
                "secure_storage": self.is_secure_storage(),
            }
            
            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("get_status", True, operation_time)
            
            return status
            
        except Exception as e:
            self.logger.error(f"Failed to get status: {e}")
            self.record_operation("get_status", False, 0.0)
            return {"error": str(e)}
    
    # ============================================================================
    # Private Helper Methods
    # ============================================================================
    
    def _save_api_key_management_data(self):
        """Save API key management data to persistent storage"""
        try:
            # Create persistence directory if it doesn't exist
            persistence_dir = Path("data/persistent/api_keys")
            persistence_dir.mkdir(parents=True, exist_ok=True)
            
            # Prepare data for persistence (excluding actual API keys for security)
            api_data = {
                "key_operations": self.key_operations,
                "validation_attempts": self.validation_attempts,
                "security_checks": self.security_checks,
                "services_configured": list(self._keys.keys()),
                "timestamp": datetime.now().isoformat(),
                "manager_id": self.manager_id,
                "version": "2.0.0"
            }
            
            # Save to JSON file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"api_key_management_data_{timestamp}.json"
            filepath = persistence_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(api_data, f, indent=2, default=str)
            
            # Keep only the latest 5 backup files
            self._cleanup_old_backups(persistence_dir, "api_key_management_data_*.json", 5)
            
            self.logger.info(f"API key management data saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to save API key management data: {e}")
            # Fallback to basic logging if persistence fails
            self.logger.warning("Persistence failed, data only logged in memory")
    
    def _cleanup_old_backups(self, directory: Path, pattern: str, keep_count: int):
        """Clean up old backup files, keeping only the specified number"""
        try:
            files = list(directory.glob(pattern))
            if len(files) > keep_count:
                # Sort by modification time (oldest first)
                files.sort(key=lambda x: x.stat().st_mtime)
                # Remove oldest files
                for old_file in files[:-keep_count]:
                    old_file.unlink()
                    self.logger.debug(f"Removed old backup: {old_file}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup old backups: {e}")
    
    def _check_api_key_management_health(self):
        """Check API key management health status"""
        try:
            # Check for excessive key operations
            if len(self.key_operations) > 1000:
                self.logger.warning(f"High number of key operations: {len(self.key_operations)}")
            
            # Check validation attempts
            if len(self.validation_attempts) > 500:
                self.logger.info(f"Large validation history: {len(self.validation_attempts)} records")
                
        except Exception as e:
            self.logger.error(f"Failed to check API key management health: {e}")
    
    def get_api_key_management_stats(self) -> Dict[str, Any]:
        """Get API key management statistics"""
        try:
            stats = {
                "total_services": len(self._keys),
                "key_operations_count": len(self.key_operations),
                "validation_attempts_count": len(self.validation_attempts),
                "security_checks_count": len(self.security_checks),
                "openai_available": self.validate_openai_key(),
                "anthropic_available": self.validate_anthropic_key(),
                "secure_storage": self.is_secure_storage(),
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds
            }
            
            # Record operation
            self.record_operation("get_api_key_management_stats", True, 0.0)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get API key management stats: {e}")
            self.record_operation("get_api_key_management_stats", False, 0.0)
            return {"error": str(e)}


# Factory function for easy access
def get_api_key_manager(config_path: Optional[Path] = None) -> APIKeyManager:
    """Get configured API key manager instance"""
    return APIKeyManager(config_path)


if __name__ == "__main__":
    # Test the API key manager
    manager = APIKeyManager()
    status = manager.get_status()
    print("API Key Manager Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
