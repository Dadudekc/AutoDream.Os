#!/usr/bin/env python3
"""
Extended API Key Manager - Agent Cellphone V2
============================================

Consolidated APIKeyManager inheriting from BaseManager.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import hashlib
import secrets
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from src.core.base_manager import BaseManager


class ExtendedAPIKeyManager(BaseManager):
    """Extended API Key Manager - inherits from BaseManager for unified functionality"""
    
    def __init__(self, config_path: str = "config/ai_ml/api_key_manager.json"):
        super().__init__(
            manager_name="ExtendedAPIKeyManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # Initialize API key-specific functionality
        self.api_keys: Dict[str, Dict[str, Any]] = {}
        self.key_hashes: Dict[str, str] = {}
        self.service_keys: Dict[str, List[str]] = {}
        self.key_usage: Dict[str, Dict[str, Any]] = {}
        
        # Load API key configuration
        self._load_api_key_config()
        
        logger.info("ExtendedAPIKeyManager initialized successfully")
    
    def _load_api_key_config(self):
        """Load API key-specific configuration"""
        try:
            if self.config:
                api_config = self.config.get("api_keys", {})
                self.api_keys = api_config.get("keys", {})
                self.service_keys = api_config.get("service_keys", {})
                
                # Emit configuration loaded event
                self.emit_event("api_key_config_loaded", {
                    "keys_count": len(self.api_keys),
                    "services_count": len(self.service_keys)
                })
        except Exception as e:
            logger.error(f"Error loading API key config: {e}")
    
    def generate_api_key(self, service: str, description: str = "", expires_in_days: int = 365) -> str:
        """Generate a new API key for a service"""
        try:
            # Generate secure random key
            api_key = secrets.token_urlsafe(32)
            key_id = hashlib.sha256(api_key.encode()).hexdigest()[:16]
            
            # Create key record
            key_record = {
                "service": service,
                "description": description,
                "created_at": self.last_activity.isoformat(),
                "expires_at": (self.last_activity + timedelta(days=expires_in_days)).isoformat(),
                "is_active": True,
                "usage_count": 0,
                "last_used": None,
                "permissions": ["read", "write"]
            }
            
            # Store key record
            self.api_keys[key_id] = key_record
            self.key_hashes[key_id] = hashlib.sha256(api_key.encode()).hexdigest()
            
            # Update service keys mapping
            if service not in self.service_keys:
                self.service_keys[service] = []
            self.service_keys[service].append(key_id)
            
            # Initialize usage tracking
            self.key_usage[key_id] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "last_request": None
            }
            
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit key generated event
            self.emit_event("api_key_generated", {
                "key_id": key_id,
                "service": service,
                "description": description
            })
            
            logger.info(f"Generated API key for service: {service} (ID: {key_id})")
            return api_key
            
        except Exception as e:
            logger.error(f"Error generating API key for service {service}: {e}")
            self.metrics.failed_operations += 1
            return ""
    
    def validate_api_key(self, api_key: str, service: str) -> bool:
        """Validate an API key for a service"""
        try:
            # Hash the provided key
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()
            
            # Find matching key ID
            key_id = None
            for kid, stored_hash in self.key_hashes.items():
                if stored_hash == key_hash:
                    key_id = kid
                    break
            
            if not key_id or key_id not in self.api_keys:
                return False
            
            key_record = self.api_keys[key_id]
            
            # Check if key is active
            if not key_record.get("is_active", False):
                return False
            
            # Check if key is for the correct service
            if key_record.get("service") != service:
                return False
            
            # Check if key has expired
            expires_at = datetime.fromisoformat(key_record["expires_at"])
            if datetime.now() > expires_at:
                return False
            
            # Update usage statistics
            self._update_key_usage(key_id, True)
            
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit key validated event
            self.emit_event("api_key_validated", {
                "key_id": key_id,
                "service": service
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating API key: {e}")
            self.metrics.failed_operations += 1
            return False
    
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke an API key"""
        try:
            if key_id not in self.api_keys:
                return False
            
            # Mark key as inactive
            self.api_keys[key_id]["is_active"] = False
            self.api_keys[key_id]["revoked_at"] = self.last_activity.isoformat()
            
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit key revoked event
            self.emit_event("api_key_revoked", {"key_id": key_id})
            
            logger.info(f"Revoked API key: {key_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error revoking API key {key_id}: {e}")
            self.metrics.failed_operations += 1
            return False
    
    def get_api_key_info(self, key_id: str) -> Optional[Dict[str, Any]]:
        """Get information about an API key"""
        if key_id not in self.api_keys:
            return None
        
        key_info = self.api_keys[key_id].copy()
        if key_id in self.key_usage:
            key_info["usage"] = self.key_usage[key_id]
        
        return key_info
    
    def list_api_keys(self, service: Optional[str] = None) -> List[str]:
        """List API key IDs, optionally filtered by service"""
        if service:
            return self.service_keys.get(service, [])
        return list(self.api_keys.keys())
    
    def _update_key_usage(self, key_id: str, success: bool):
        """Update key usage statistics"""
        if key_id not in self.key_usage:
            return
        
        usage = self.key_usage[key_id]
        usage["total_requests"] += 1
        usage["last_request"] = self.last_activity.isoformat()
        
        if success:
            usage["successful_requests"] += 1
        else:
            usage["failed_requests"] += 1
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get extended manager status including API key metrics"""
        base_status = super().get_manager_status()
        
        # Add API key-specific status
        api_key_status = {
            "total_api_keys": len(self.api_keys),
            "active_api_keys": len([k for k in self.api_keys.values() if k.get("is_active", False)]),
            "services_supported": len(self.service_keys),
            "total_key_requests": sum(u.get("total_requests", 0) for u in self.key_usage.values()),
            "successful_key_requests": sum(u.get("successful_requests", 0) for u in self.key_usage.values()),
            "failed_key_requests": sum(u.get("failed_requests", 0) for u in self.key_usage.values())
        }
        
        base_status.update(api_key_status)
        return base_status

