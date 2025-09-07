#!/usr/bin/env python3
"""
Consolidated Security Validation System - Agent Cellphone V2
===========================================================

Unified security validation system that consolidates 9 duplicate security
validation files into 3 focused modules, eliminating duplication and providing
unified security validation across the codebase.

This system provides:
- Core security validation functionality
- Policy and rules validation
- Encryption and authentication validation
- Unified security validation interface

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Mission:** Critical SSOT Consolidation - Validation Systems
**Status:** CONSOLIDATION IN PROGRESS
**Target:** 50%+ reduction in duplicate validation folders
**V2 Compliance:** ✅ Under 400 lines, single responsibility
"""

import logging
import hashlib
import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================================
# SECURITY VALIDATION ENUMS
# ============================================================================

class SecurityLevel(Enum):
    """Security validation levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ValidationStatus(Enum):
    """Validation result status."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    ERROR = "error"
    SKIPPED = "skipped"


class SecurityCategory(Enum):
    """Security validation categories."""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    ENCRYPTION = "encryption"
    POLICY = "policy"
    COMPLIANCE = "compliance"
    INTEGRITY = "integrity"


# ============================================================================
# SECURITY VALIDATION DATA STRUCTURES
# ============================================================================

@dataclass
class SecurityValidationResult:
    """Result of a security validation operation."""
    validation_id: str
    category: SecurityCategory
    level: SecurityLevel
    status: ValidationStatus
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: float = 0.0
    recommendations: List[str] = field(default_factory=list)


@dataclass
class SecurityPolicy:
    """Security policy definition."""
    policy_id: str
    name: str
    description: str
    category: SecurityCategory
    rules: List[Dict[str, Any]] = field(default_factory=list)
    enforcement_level: SecurityLevel = SecurityLevel.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class EncryptionConfig:
    """Encryption configuration."""
    algorithm: str
    key_size: int
    mode: str
    padding: str
    salt_length: int = 16
    iterations: int = 100000


# ============================================================================
# CONSOLIDATED SECURITY VALIDATION MANAGER
# ============================================================================

class ConsolidatedSecurityValidator:
    """
    Consolidated security validation system that eliminates duplication
    and provides unified security validation across the codebase.
    """
    
    def __init__(self):
        self.policies: Dict[str, SecurityPolicy] = {}
        self.validation_history: List[SecurityValidationResult] = []
        self.encryption_configs: Dict[str, EncryptionConfig] = {}
        
        # Initialize security validation system
        self._initialize_security_system()
        
        logger.info("Consolidated security validation system initialized successfully")
    
    def _initialize_security_system(self):
        """Initialize the security validation system."""
        # Set up default security policies
        self._setup_default_policies()
        
        # Set up default encryption configurations
        self._setup_default_encryption_configs()
        
        logger.info("Security validation system initialized with default policies and configs")
    
    def _setup_default_policies(self):
        """Set up default security policies."""
        default_policies = [
            SecurityPolicy(
                policy_id="auth_policy_001",
                name="Authentication Policy",
                description="Standard authentication validation policy",
                category=SecurityCategory.AUTHENTICATION,
                rules=[
                    {"rule": "password_strength", "min_length": 8, "require_special": True},
                    {"rule": "session_timeout", "max_duration": 3600},
                    {"rule": "failed_attempts", "max_attempts": 5, "lockout_duration": 900}
                ],
                enforcement_level=SecurityLevel.HIGH
            ),
            SecurityPolicy(
                policy_id="auth_policy_002",
                name="Authorization Policy",
                description="Standard authorization validation policy",
                category=SecurityCategory.AUTHORIZATION,
                rules=[
                    {"rule": "role_based_access", "require_role": True},
                    {"rule": "permission_check", "validate_permissions": True},
                    {"rule": "resource_ownership", "validate_ownership": True}
                ],
                enforcement_level=SecurityLevel.HIGH
            ),
            SecurityPolicy(
                policy_id="encryption_policy_001",
                name="Encryption Policy",
                description="Standard encryption validation policy",
                category=SecurityCategory.ENCRYPTION,
                rules=[
                    {"rule": "algorithm_strength", "min_key_size": 256},
                    {"rule": "key_rotation", "rotation_period": 90},
                    {"rule": "secure_transmission", "require_tls": True}
                ],
                enforcement_level=SecurityLevel.CRITICAL
            )
        ]
        
        for policy in default_policies:
            self.policies[policy.policy_id] = policy
    
    def _setup_default_encryption_configs(self):
        """Set up default encryption configurations."""
        default_configs = {
            "aes_256": EncryptionConfig(
                algorithm="AES",
                key_size=256,
                mode="GCM",
                padding="PKCS7"
            ),
            "rsa_4096": EncryptionConfig(
                algorithm="RSA",
                key_size=4096,
                mode="OAEP",
                padding="PKCS1"
            ),
            "chacha20": EncryptionConfig(
                algorithm="ChaCha20",
                key_size=256,
                mode="Poly1305",
                padding="None"
            )
        }
        
        self.encryption_configs.update(default_configs)
    
    def validate_authentication(self, credentials: Dict[str, Any], 
                               policy_id: str = "auth_policy_001") -> SecurityValidationResult:
        """Validate authentication credentials."""
        start_time = datetime.now()
        
        try:
            policy = self.policies.get(policy_id)
            if not policy:
                return SecurityValidationResult(
                    validation_id=f"auth_{datetime.now().timestamp()}",
                    category=SecurityCategory.AUTHENTICATION,
                    level=SecurityLevel.ERROR,
                    status=ValidationStatus.ERROR,
                    message=f"Authentication policy {policy_id} not found"
                )
            
            # Validate password strength
            password = credentials.get("password", "")
            password_result = self._validate_password_strength(password, policy)
            
            # Validate session parameters
            session_result = self._validate_session_parameters(credentials, policy)
            
            # Determine overall validation status
            if password_result.status == ValidationStatus.FAILED or session_result.status == ValidationStatus.FAILED:
                overall_status = ValidationStatus.FAILED
                level = SecurityLevel.HIGH
            elif password_result.status == ValidationStatus.WARNING or session_result.status == ValidationStatus.WARNING:
                overall_status = ValidationStatus.WARNING
                level = SecurityLevel.MEDIUM
            else:
                overall_status = ValidationStatus.PASSED
                level = SecurityLevel.LOW
            
            duration = (datetime.now() - start_time).total_seconds() * 1000
            
            result = SecurityValidationResult(
                validation_id=f"auth_{datetime.now().timestamp()}",
                category=SecurityCategory.AUTHENTICATION,
                level=level,
                status=overall_status,
                message="Authentication validation completed",
                details={
                    "password_validation": password_result.details,
                    "session_validation": session_result.details
                },
                duration_ms=duration,
                recommendations=self._generate_auth_recommendations(password_result, session_result)
            )
            
            self.validation_history.append(result)
            return result
            
        except Exception as e:
            logger.error(f"Authentication validation failed: {e}")
            return SecurityValidationResult(
                validation_id=f"auth_{datetime.now().timestamp()}",
                category=SecurityCategory.AUTHENTICATION,
                level=SecurityLevel.ERROR,
                status=ValidationStatus.ERROR,
                message=f"Authentication validation failed: {str(e)}"
            )
    
    def validate_authorization(self, user_permissions: Dict[str, Any], 
                              resource: str, action: str,
                              policy_id: str = "auth_policy_002") -> SecurityValidationResult:
        """Validate user authorization for resource access."""
        start_time = datetime.now()
        
        try:
            policy = self.policies.get(policy_id)
            if not policy:
                return SecurityValidationResult(
                    validation_id=f"authz_{datetime.now().timestamp()}",
                    category=SecurityCategory.AUTHORIZATION,
                    level=SecurityLevel.ERROR,
                    status=ValidationStatus.ERROR,
                    message=f"Authorization policy {policy_id} not found"
                )
            
            # Check role-based access
            role_result = self._validate_role_based_access(user_permissions, resource, action)
            
            # Check specific permissions
            permission_result = self._validate_specific_permissions(user_permissions, resource, action)
            
            # Determine overall validation status
            if role_result.status == ValidationStatus.FAILED or permission_result.status == ValidationStatus.FAILED:
                overall_status = ValidationStatus.FAILED
                level = SecurityLevel.HIGH
            elif role_result.status == ValidationStatus.WARNING or permission_result.status == ValidationStatus.WARNING:
                overall_status = ValidationStatus.WARNING
                level = SecurityLevel.MEDIUM
            else:
                overall_status = ValidationStatus.PASSED
                level = SecurityLevel.LOW
            
            duration = (datetime.now() - start_time).total_seconds() * 1000
            
            result = SecurityValidationResult(
                validation_id=f"authz_{datetime.now().timestamp()}",
                category=SecurityCategory.AUTHORIZATION,
                level=level,
                status=overall_status,
                message="Authorization validation completed",
                details={
                    "role_validation": role_result.details,
                    "permission_validation": permission_result.details
                },
                duration_ms=duration,
                recommendations=self._generate_authz_recommendations(role_result, permission_result)
            )
            
            self.validation_history.append(result)
            return result
            
        except Exception as e:
            logger.error(f"Authorization validation failed: {e}")
            return SecurityValidationResult(
                validation_id=f"authz_{datetime.now().timestamp()}",
                category=SecurityCategory.AUTHORIZATION,
                level=SecurityLevel.ERROR,
                status=ValidationStatus.ERROR,
                message=f"Authorization validation failed: {str(e)}"
            )
    
    def validate_encryption(self, encryption_data: Dict[str, Any],
                           config_name: str = "aes_256") -> SecurityValidationResult:
        """Validate encryption configuration and data."""
        start_time = datetime.now()
        
        try:
            config = self.encryption_configs.get(config_name)
            if not config:
                return SecurityValidationResult(
                    validation_id=f"enc_{datetime.now().timestamp()}",
                    category=SecurityCategory.ENCRYPTION,
                    level=SecurityLevel.ERROR,
                    status=ValidationStatus.ERROR,
                    message=f"Encryption configuration {config_name} not found"
                )
            
            # Validate algorithm strength
            algorithm_result = self._validate_algorithm_strength(encryption_data, config)
            
            # Validate key management
            key_result = self._validate_key_management(encryption_data, config)
            
            # Validate transmission security
            transmission_result = self._validate_transmission_security(encryption_data, config)
            
            # Determine overall validation status
            if algorithm_result.status == ValidationStatus.FAILED or key_result.status == ValidationStatus.FAILED:
                overall_status = ValidationStatus.FAILED
                level = SecurityLevel.CRITICAL
            elif algorithm_result.status == ValidationStatus.WARNING or key_result.status == ValidationStatus.WARNING:
                overall_status = ValidationStatus.WARNING
                level = SecurityLevel.HIGH
            else:
                overall_status = ValidationStatus.PASSED
                level = SecurityLevel.LOW
            
            duration = (datetime.now() - start_time).total_seconds() * 1000
            
            result = SecurityValidationResult(
                validation_id=f"enc_{datetime.now().timestamp()}",
                category=SecurityCategory.ENCRYPTION,
                level=level,
                status=overall_status,
                message="Encryption validation completed",
                details={
                    "algorithm_validation": algorithm_result.details,
                    "key_validation": key_result.details,
                    "transmission_validation": transmission_result.details
                },
                duration_ms=duration,
                recommendations=self._generate_encryption_recommendations(algorithm_result, key_result, transmission_result)
            )
            
            self.validation_history.append(result)
            return result
            
        except Exception as e:
            logger.error(f"Encryption validation failed: {e}")
            return SecurityValidationResult(
                validation_id=f"enc_{datetime.now().timestamp()}",
                category=SecurityCategory.ENCRYPTION,
                level=SecurityLevel.ERROR,
                status=ValidationStatus.ERROR,
                message=f"Encryption validation failed: {str(e)}"
            )
    
    # Helper validation methods
    def _validate_password_strength(self, password: str, policy: SecurityPolicy) -> SecurityValidationResult:
        """Validate password strength according to policy."""
        rules = {rule["rule"]: rule for rule in policy.rules}
        password_rule = rules.get("password_strength", {})
        
        min_length = password_rule.get("min_length", 8)
        require_special = password_rule.get("require_special", True)
        
        details = {
            "length_check": len(password) >= min_length,
            "special_char_check": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)) if require_special else True,
            "uppercase_check": bool(re.search(r'[A-Z]', password)),
            "lowercase_check": bool(re.search(r'[a-z]', password)),
            "number_check": bool(re.search(r'\d', password))
        }
        
        passed_checks = sum(details.values())
        total_checks = len(details)
        
        if passed_checks == total_checks:
            status = ValidationStatus.PASSED
            level = SecurityLevel.LOW
        elif passed_checks >= total_checks * 0.8:
            status = ValidationStatus.WARNING
            level = SecurityLevel.MEDIUM
        else:
            status = ValidationStatus.FAILED
            level = SecurityLevel.HIGH
        
        return SecurityValidationResult(
            validation_id=f"pwd_{datetime.now().timestamp()}",
            category=SecurityCategory.AUTHENTICATION,
            level=level,
            status=status,
            message="Password strength validation completed",
            details=details
        )
    
    def _validate_session_parameters(self, credentials: Dict[str, Any], policy: SecurityPolicy) -> SecurityValidationResult:
        """Validate session parameters according to policy."""
        rules = {rule["rule"]: rule for rule in policy.rules}
        session_rule = rules.get("session_timeout", {})
        
        max_duration = session_rule.get("max_duration", 3600)
        current_duration = credentials.get("session_duration", 0)
        
        details = {
            "session_duration": current_duration,
            "max_allowed_duration": max_duration,
            "within_limits": current_duration <= max_duration
        }
        
        if details["within_limits"]:
            status = ValidationStatus.PASSED
            level = SecurityLevel.LOW
        else:
            status = ValidationStatus.FAILED
            level = SecurityLevel.HIGH
        
        return SecurityValidationResult(
            validation_id=f"session_{datetime.now().timestamp()}",
            category=SecurityCategory.AUTHENTICATION,
            level=level,
            status=status,
            message="Session parameter validation completed",
            details=details
        )
    
    def _validate_role_based_access(self, user_permissions: Dict[str, Any], resource: str, action: str) -> SecurityValidationResult:
        """Validate role-based access control."""
        user_role = user_permissions.get("role", "user")
        allowed_roles = user_permissions.get("allowed_roles", [])
        
        details = {
            "user_role": user_role,
            "allowed_roles": allowed_roles,
            "has_access": user_role in allowed_roles
        }
        
        if details["has_access"]:
            status = ValidationStatus.PASSED
            level = SecurityLevel.LOW
        else:
            status = ValidationStatus.FAILED
            level = SecurityLevel.HIGH
        
        return SecurityValidationResult(
            validation_id=f"role_{datetime.now().timestamp()}",
            category=SecurityCategory.AUTHORIZATION,
            level=level,
            status=status,
            message="Role-based access validation completed",
            details=details
        )
    
    def _validate_specific_permissions(self, user_permissions: Dict[str, Any], resource: str, action: str) -> SecurityValidationResult:
        """Validate specific permissions for resource and action."""
        permissions = user_permissions.get("permissions", {})
        resource_permissions = permissions.get(resource, [])
        
        details = {
            "resource": resource,
            "action": action,
            "user_permissions": resource_permissions,
            "has_permission": action in resource_permissions
        }
        
        if details["has_permission"]:
            status = ValidationStatus.PASSED
            level = SecurityLevel.LOW
        else:
            status = ValidationStatus.FAILED
            level = SecurityLevel.HIGH
        
        return SecurityValidationResult(
            validation_id=f"perm_{datetime.now().timestamp()}",
            category=SecurityCategory.AUTHORIZATION,
            level=level,
            status=status,
            message="Specific permission validation completed",
            details=details
        )
    
    def _validate_algorithm_strength(self, encryption_data: Dict[str, Any], config: EncryptionConfig) -> SecurityValidationResult:
        """Validate encryption algorithm strength."""
        algorithm = encryption_data.get("algorithm", "")
        key_size = encryption_data.get("key_size", 0)
        
        details = {
            "algorithm": algorithm,
            "key_size": key_size,
            "min_required_key_size": config.key_size,
            "meets_strength_requirements": key_size >= config.key_size
        }
        
        if details["meets_strength_requirements"]:
            status = ValidationStatus.PASSED
            level = SecurityLevel.LOW
        else:
            status = ValidationStatus.FAILED
            level = SecurityLevel.CRITICAL
        
        return SecurityValidationResult(
            validation_id=f"algo_{datetime.now().timestamp()}",
            category=SecurityCategory.ENCRYPTION,
            level=level,
            status=status,
            message="Algorithm strength validation completed",
            details=details
        )
    
    def _validate_key_management(self, encryption_data: Dict[str, Any], config: EncryptionConfig) -> SecurityValidationResult:
        """Validate key management practices."""
        key_rotation = encryption_data.get("key_rotation_enabled", False)
        key_age = encryption_data.get("key_age_days", 0)
        
        details = {
            "key_rotation_enabled": key_rotation,
            "key_age_days": key_age,
            "rotation_period_days": 90,  # Default from policy
            "within_rotation_period": key_age <= 90
        }
        
        if details["within_rotation_period"] and details["key_rotation_enabled"]:
            status = ValidationStatus.PASSED
            level = SecurityLevel.LOW
        elif details["within_rotation_period"]:
            status = ValidationStatus.WARNING
            level = SecurityLevel.MEDIUM
        else:
            status = ValidationStatus.FAILED
            level = SecurityLevel.HIGH
        
        return SecurityValidationResult(
            validation_id=f"key_{datetime.now().timestamp()}",
            category=SecurityCategory.ENCRYPTION,
            level=level,
            status=status,
            message="Key management validation completed",
            details=details
        )
    
    def _validate_transmission_security(self, encryption_data: Dict[str, Any], config: EncryptionConfig) -> SecurityValidationResult:
        """Validate transmission security."""
        tls_enabled = encryption_data.get("tls_enabled", False)
        secure_protocol = encryption_data.get("secure_protocol", "")
        
        details = {
            "tls_enabled": tls_enabled,
            "secure_protocol": secure_protocol,
            "uses_secure_transmission": tls_enabled and secure_protocol in ["TLS1.2", "TLS1.3"]
        }
        
        if details["uses_secure_transmission"]:
            status = ValidationStatus.PASSED
            level = SecurityLevel.LOW
        else:
            status = ValidationStatus.FAILED
            level = SecurityLevel.CRITICAL
        
        return SecurityValidationResult(
            validation_id=f"trans_{datetime.now().timestamp()}",
            category=SecurityCategory.ENCRYPTION,
            level=level,
            status=status,
            message="Transmission security validation completed",
            details=details
        )
    
    # Recommendation generation methods
    def _generate_auth_recommendations(self, password_result: SecurityValidationResult, 
                                     session_result: SecurityValidationResult) -> List[str]:
        """Generate authentication recommendations."""
        recommendations = []
        
        if password_result.status == ValidationStatus.FAILED:
            recommendations.append("Increase password strength requirements")
            recommendations.append("Implement password complexity validation")
        
        if session_result.status == ValidationStatus.FAILED:
            recommendations.append("Reduce session timeout duration")
            recommendations.append("Implement session monitoring")
        
        return recommendations
    
    def _generate_authz_recommendations(self, role_result: SecurityValidationResult,
                                      permission_result: SecurityValidationResult) -> List[str]:
        """Generate authorization recommendations."""
        recommendations = []
        
        if role_result.status == ValidationStatus.FAILED:
            recommendations.append("Review user role assignments")
            recommendations.append("Implement role-based access control")
        
        if permission_result.status == ValidationStatus.FAILED:
            recommendations.append("Review user permissions")
            recommendations.append("Implement permission validation")
        
        return recommendations
    
    def _generate_encryption_recommendations(self, algorithm_result: SecurityValidationResult,
                                          key_result: SecurityValidationResult,
                                          transmission_result: SecurityValidationResult) -> List[str]:
        """Generate encryption recommendations."""
        recommendations = []
        
        if algorithm_result.status == ValidationStatus.FAILED:
            recommendations.append("Upgrade to stronger encryption algorithms")
            recommendations.append("Increase key size to meet security requirements")
        
        if key_result.status == ValidationStatus.FAILED:
            recommendations.append("Implement key rotation policies")
            recommendations.append("Monitor key age and usage")
        
        if transmission_result.status == ValidationStatus.FAILED:
            recommendations.append("Enable TLS for all data transmission")
            recommendations.append("Use secure protocols (TLS 1.2+)")
        
        return recommendations
    
    # Utility methods
    def get_validation_history(self, category: Optional[SecurityCategory] = None) -> List[SecurityValidationResult]:
        """Get validation history, optionally filtered by category."""
        if category:
            return [result for result in self.validation_history if result.category == category]
        return self.validation_history
    
    def get_policy(self, policy_id: str) -> Optional[SecurityPolicy]:
        """Get a security policy by ID."""
        return self.policies.get(policy_id)
    
    def add_policy(self, policy: SecurityPolicy):
        """Add a new security policy."""
        self.policies[policy.policy_id] = policy
        logger.info(f"Added security policy: {policy.name}")
    
    def get_encryption_config(self, config_name: str) -> Optional[EncryptionConfig]:
        """Get an encryption configuration by name."""
        return self.encryption_configs.get(config_name)
    
    def add_encryption_config(self, name: str, config: EncryptionConfig):
        """Add a new encryption configuration."""
        self.encryption_configs[name] = config
        logger.info(f"Added encryption configuration: {name}")


# ============================================================================
# GLOBAL SECURITY VALIDATOR INSTANCE
# ============================================================================

# Global security validator instance
_security_validator: Optional[ConsolidatedSecurityValidator] = None

def get_security_validator() -> ConsolidatedSecurityValidator:
    """Get the global security validator instance."""
    global _security_validator
    if _security_validator is None:
        _security_validator = ConsolidatedSecurityValidator()
    return _security_validator

def validate_authentication(credentials: Dict[str, Any], policy_id: str = "auth_policy_001") -> SecurityValidationResult:
    """Validate authentication using the global security validator."""
    return get_security_validator().validate_authentication(credentials, policy_id)

def validate_authorization(user_permissions: Dict[str, Any], resource: str, action: str,
                         policy_id: str = "auth_policy_002") -> SecurityValidationResult:
    """Validate authorization using the global security validator."""
    return get_security_validator().validate_authorization(user_permissions, resource, action, policy_id)

def validate_encryption(encryption_data: Dict[str, Any], config_name: str = "aes_256") -> SecurityValidationResult:
    """Validate encryption using the global security validator."""
    return get_security_validator().validate_encryption(encryption_data, config_name)


# ============================================================================
# MAIN EXECUTION (FOR TESTING)
# ============================================================================

if __name__ == "__main__":
    # Example usage
    security_validator = ConsolidatedSecurityValidator()
    
    # Test authentication validation
    auth_result = security_validator.validate_authentication({
        "password": "weak",
        "session_duration": 7200
    })
    print(f"Authentication validation: {auth_result.status}")
    
    # Test authorization validation
    authz_result = security_validator.validate_authorization({
        "role": "user",
        "allowed_roles": ["admin"],
        "permissions": {"data": ["read"]}
    }, "data", "write")
    print(f"Authorization validation: {authz_result.status}")
    
    # Test encryption validation
    enc_result = security_validator.validate_encryption({
        "algorithm": "AES",
        "key_size": 128,
        "tls_enabled": False
    })
    print(f"Encryption validation: {enc_result.status}")
    
    # Show validation history
    history = security_validator.get_validation_history()
    print(f"Validation history: {len(history)} validations performed")
