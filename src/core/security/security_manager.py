# V3-001: Cloud Infrastructure Setup - Security Manager
# Agent-1: Architecture Foundation Specialist
# 
# Unified security management for the V2_SWARM system

import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
from dataclasses import dataclass
from enum import Enum

from .oauth2_provider import OAuth2Provider, OAuth2Client
from .jwt_manager import JWTManager, TokenPayload


class SecurityLevel(Enum):
    """Security level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityPolicy:
    """Security policy configuration."""
    name: str
    level: SecurityLevel
    max_login_attempts: int = 5
    lockout_duration: int = 300  # seconds
    password_min_length: int = 8
    require_2fa: bool = False
    session_timeout: int = 3600  # seconds
    allowed_ips: List[str] = None
    
    def __post_init__(self):
        if self.allowed_ips is None:
            self.allowed_ips = []


class SecurityManager:
    """Unified security management for V2_SWARM system."""
    
    def __init__(self):
        self.oauth2_provider = OAuth2Provider()
        self.jwt_manager = JWTManager()
        self.security_policies: Dict[str, SecurityPolicy] = {}
        self.failed_attempts: Dict[str, int] = {}
        self.locked_accounts: Dict[str, datetime] = {}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self._initialize_default_policies()
    
    def _initialize_default_policies(self) -> None:
        """Initialize default security policies."""
        default_policy = SecurityPolicy(
            name="default",
            level=SecurityLevel.MEDIUM,
            max_login_attempts=5,
            lockout_duration=300,
            password_min_length=8,
            require_2fa=False,
            session_timeout=3600
        )
        
        agent_policy = SecurityPolicy(
            name="agent",
            level=SecurityLevel.HIGH,
            max_login_attempts=3,
            lockout_duration=600,
            password_min_length=12,
            require_2fa=True,
            session_timeout=7200
        )
        
        admin_policy = SecurityPolicy(
            name="admin",
            level=SecurityLevel.CRITICAL,
            max_login_attempts=3,
            lockout_duration=1800,
            password_min_length=16,
            require_2fa=True,
            session_timeout=1800
        )
        
        self.security_policies = {
            "default": default_policy,
            "agent": agent_policy,
            "admin": admin_policy
        }
    
    def hash_password(self, password: str, salt: str = None) -> tuple[str, str]:
        """Hash password with salt."""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Use PBKDF2 for password hashing
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        
        return password_hash.hex(), salt
    
    def verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """Verify password against hash."""
        computed_hash, _ = self.hash_password(password, salt)
        return computed_hash == password_hash
    
    def check_account_lockout(self, user_id: str) -> bool:
        """Check if account is locked out."""
        if user_id in self.locked_accounts:
            lockout_time = self.locked_accounts[user_id]
            policy = self._get_user_policy(user_id)
            
            if datetime.utcnow() < lockout_time + timedelta(seconds=policy.lockout_duration):
                return True
            else:
                # Remove expired lockout
                del self.locked_accounts[user_id]
                self.failed_attempts[user_id] = 0
        
        return False
    
    def record_failed_attempt(self, user_id: str) -> bool:
        """Record failed login attempt and check for lockout."""
        self.failed_attempts[user_id] = self.failed_attempts.get(user_id, 0) + 1
        
        policy = self._get_user_policy(user_id)
        
        if self.failed_attempts[user_id] >= policy.max_login_attempts:
            self.locked_accounts[user_id] = datetime.utcnow()
            return True  # Account locked
        
        return False
    
    def reset_failed_attempts(self, user_id: str) -> None:
        """Reset failed login attempts for user."""
        self.failed_attempts[user_id] = 0
        if user_id in self.locked_accounts:
            del self.locked_accounts[user_id]
    
    def _get_user_policy(self, user_id: str) -> SecurityPolicy:
        """Get security policy for user."""
        # Determine policy based on user type
        if user_id.startswith("agent-"):
            return self.security_policies["agent"]
        elif user_id.startswith("admin-"):
            return self.security_policies["admin"]
        else:
            return self.security_policies["default"]
    
    def create_session(self, user_id: str, agent_id: str = None, 
                      roles: List[str] = None) -> str:
        """Create authenticated session."""
        if self.check_account_lockout(user_id):
            raise ValueError("Account is locked out")
        
        # Create JWT token
        token = self.jwt_manager.create_access_token(
            user_id=user_id,
            agent_id=agent_id,
            roles=roles or []
        )
        
        # Store session info
        session_info = {
            "user_id": user_id,
            "agent_id": agent_id,
            "roles": roles or [],
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow()
        }
        
        self.active_sessions[token] = session_info
        return token
    
    def validate_session(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate session token."""
        # Verify JWT token
        payload = self.jwt_manager.verify_token(token)
        if not payload:
            return None
        
        # Check if session exists
        if token not in self.active_sessions:
            return None
        
        session_info = self.active_sessions[token]
        
        # Check session timeout
        policy = self._get_user_policy(session_info["user_id"])
        if (datetime.utcnow() - session_info["last_activity"]).seconds > policy.session_timeout:
            del self.active_sessions[token]
            return None
        
        # Update last activity
        session_info["last_activity"] = datetime.utcnow()
        
        return {
            "user_id": payload["user_id"],
            "agent_id": payload.get("agent_id"),
            "roles": payload.get("roles", []),
            "permissions": payload.get("permissions", [])
        }
    
    def revoke_session(self, token: str) -> bool:
        """Revoke session token."""
        if token in self.active_sessions:
            del self.active_sessions[token]
            return True
        return False
    
    def create_oauth2_client(self, client_id: str, redirect_uris: List[str],
                           scopes: List[str] = None) -> OAuth2Client:
        """Create OAuth2 client."""
        return self.oauth2_provider.create_client(client_id, redirect_uris, scopes)
    
    def oauth2_authorize(self, client_id: str, user_id: str, 
                        redirect_uri: str, scope: str) -> str:
        """OAuth2 authorization flow."""
        return self.oauth2_provider.generate_authorization_code(
            client_id, user_id, redirect_uri, scope
        )
    
    def oauth2_token_exchange(self, code: str, client_id: str, 
                            client_secret: str) -> Optional[str]:
        """OAuth2 token exchange."""
        access_token = self.oauth2_provider.exchange_code_for_token(
            code, client_id, client_secret
        )
        return access_token.token if access_token else None
    
    def validate_oauth2_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate OAuth2 token."""
        return self.oauth2_provider.validate_token(token)
    
    def get_security_policy(self, policy_name: str) -> Optional[SecurityPolicy]:
        """Get security policy by name."""
        return self.security_policies.get(policy_name)
    
    def update_security_policy(self, policy_name: str, 
                             policy: SecurityPolicy) -> None:
        """Update security policy."""
        self.security_policies[policy_name] = policy
    
    def get_active_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Get all active sessions."""
        return self.active_sessions.copy()
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions."""
        current_time = datetime.utcnow()
        expired_tokens = []
        
        for token, session_info in self.active_sessions.items():
            policy = self._get_user_policy(session_info["user_id"])
            if (current_time - session_info["last_activity"]).seconds > policy.session_timeout:
                expired_tokens.append(token)
        
        for token in expired_tokens:
            del self.active_sessions[token]
        
        return len(expired_tokens)
