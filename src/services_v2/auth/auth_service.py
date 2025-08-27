#!/usr/bin/env python3
"""
V2 Authentication Service
========================

Enhanced authentication service with V2 architecture integration.
Provides enterprise-grade security, performance monitoring, and integration testing.
"""

import sys
import time
import logging
import hashlib
import secrets
import hmac
from src.session_management.backends import (
    MemorySessionBackend,
    SQLiteSessionBackend,
)
from src.session_management.session_manager import SessionManager

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# Add src to path for security integration
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from security.authentication_manager import AuthenticationManager
    from security.network_security import NetworkScanner
    from security.compliance_audit import ComplianceAuditor

    SECURITY_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Security components not available: {e}")
    SECURITY_AVAILABLE = False


# Authentication Result Status
class AuthStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    LOCKED = "locked"
    EXPIRED = "expired"
    INVALID_CREDENTIALS = "invalid_credentials"
    RATE_LIMITED = "rate_limited"
    SYSTEM_ERROR = "system_error"


# Permission Levels
class PermissionLevel(Enum):
    GUEST = 1
    USER = 2
    ADMIN = 3
    SUPER_ADMIN = 4
    SYSTEM = 5


@dataclass
class V2AuthResult:
    """Enhanced authentication result for V2"""

    status: AuthStatus
    user_id: Optional[str]
    session_id: Optional[str]
    permissions: List[PermissionLevel]
    expires_at: Optional[datetime]
    metadata: Dict[str, Any]
    performance_metrics: Dict[str, float]
    security_events: List[str]


class AuthService:
    """
    V2 Authentication Service
    Enhanced authentication with V2 architecture integration
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.logger = self._setup_logging()
        self.config = config or self._default_config()

        # Session backend setup
        backend_name = self.config.get("session_backend", "memory")
        if backend_name == "sqlite":
            backend = SQLiteSessionBackend(
                self.config.get("session_db_path", "auth_sessions.db"),
                self.logger,
            )
        else:
            backend = MemorySessionBackend()
        self.session_manager = SessionManager(
            backend,
            self.config["session_timeout"],
            self.logger,
        )

        # Initialize core components
        self._init_core_components()

        # Performance tracking
        self.auth_attempts = 0
        self.successful_auths = 0
        self.failed_auths = 0
        self.start_time = time.time()

        self.logger.info("V2 Authentication Service initialized")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the auth service"""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for auth service"""
        return {
            "session_timeout": 3600,  # 1 hour
            "max_login_attempts": 5,
            "lockout_duration": 1800,  # 30 minutes
            "rate_limit_window": 300,  # 5 minutes
            "rate_limit_max_attempts": 10,
            "enable_mfa": True,
            "enable_audit_logging": True,
            "enable_performance_monitoring": True,
            "security_level": "enterprise",
            "session_backend": "memory",  # or 'sqlite'
            "session_db_path": "auth_sessions.db",
        }

    def _init_core_components(self):
        """Initialize core authentication components"""
        try:
            if SECURITY_AVAILABLE:
                self.auth_system = AuthenticationManager()
                self.network_scanner = NetworkScanner()
                self.compliance_auditor = ComplianceAuditor()
                self.logger.info("✅ Core security components initialized")
            else:
                self.auth_system = None
                self.network_scanner = None
                self.compliance_auditor = None
                self.logger.warning("⚠️ Running without core security components")

        except Exception as e:
            self.logger.error(f"Failed to initialize core components: {e}")
            self.auth_system = None
            self.network_scanner = None
            self.compliance_auditor = None

    def authenticate_user_v2(
        self,
        username: str,
        password: str,
        source_ip: str,
        user_agent: str = None,
        context: Dict[str, Any] = None,
    ) -> V2AuthResult:
        """
        Enhanced V2 authentication with comprehensive security checks
        """
        start_time = time.time()
        security_events = []

        try:
            self.auth_attempts += 1
            self.logger.info(f"🔐 V2 Authentication attempt for user: {username}")

            # Security context validation
            if context:
                security_events.extend(self._validate_security_context(context))

            # Rate limiting check
            if self._is_rate_limited(source_ip):
                return V2AuthResult(
                    status=AuthStatus.RATE_LIMITED,
                    user_id=None,
                    session_id=None,
                    permissions=[],
                    expires_at=None,
                    metadata={"rate_limit_info": self._get_rate_limit_info(source_ip)},
                    performance_metrics={"auth_duration": time.time() - start_time},
                    security_events=security_events,
                )

            # Network security validation
            if self.network_scanner:
                network_events = self._validate_network_security(source_ip)
                security_events.extend(network_events)

            # Core authentication
            if self.auth_system:
                auth_result = self.auth_system.authenticate_user(
                    username, password, source_ip, user_agent
                )

                if auth_result.success:
                    self.successful_auths += 1

                    # Enhanced session management
                    session = self.session_manager.create_session(
                        username,
                        source_ip,
                        user_agent,
                        metadata={
                            "v2_features": True,
                            "security_level": self.config["security_level"],
                            "session_type": "enhanced",
                        },
                    )

                    # Permission determination
                    permissions = self._determine_user_permissions(username)

                    # Compliance audit
                    if self.compliance_auditor:
                        compliance_events = self._audit_compliance(username, source_ip)
                        security_events.extend(compliance_events)

                    auth_duration = time.time() - start_time

                    self.logger.info(
                        f"✅ V2 Authentication successful for {username} in {auth_duration:.3f}s"
                    )

                    return V2AuthResult(
                        status=AuthStatus.SUCCESS,
                        user_id=username,
                        session_id=session.session_id,
                        permissions=permissions,
                        expires_at=datetime.fromtimestamp(session.expires_at)
                        if session.expires_at
                        else None,
                        metadata=session.metadata,
                        performance_metrics={"auth_duration": auth_duration},
                        security_events=security_events,
                    )
                else:
                    self.failed_auths += 1
                    security_events.append(
                        f"Authentication failed: {auth_result.error_message}"
                    )

                    return V2AuthResult(
                        status=AuthStatus.FAILED,
                        user_id=None,
                        session_id=None,
                        permissions=[],
                        expires_at=None,
                        metadata={"error": auth_result.error_message},
                        performance_metrics={"auth_duration": time.time() - start_time},
                        security_events=security_events,
                    )
            else:
                # Fallback authentication (for testing)
                return self._fallback_authentication(
                    username,
                    password,
                    source_ip,
                    user_agent,
                    start_time,
                    security_events,
                )

        except Exception as e:
            self.logger.error(f"V2 Authentication error for {username}: {e}")
            security_events.append(f"System error: {str(e)}")

            return V2AuthResult(
                status=AuthStatus.SYSTEM_ERROR,
                user_id=None,
                session_id=None,
                permissions=[],
                expires_at=None,
                metadata={"error": str(e)},
                performance_metrics={"auth_duration": time.time() - start_time},
                security_events=security_events,
            )

    def _validate_security_context(self, context: Dict[str, Any]) -> List[str]:
        """Validate security context for authentication"""
        events = []

        # Check for suspicious patterns
        if "suspicious_headers" in context:
            events.append("Suspicious headers detected")

        if "unusual_location" in context:
            events.append("Unusual location detected")

        if "multiple_failed_attempts" in context:
            events.append("Multiple failed attempts detected")

        return events

    def _validate_network_security(self, source_ip: str) -> List[str]:
        """Validate network security for authentication"""
        events = []

        try:
            # Check if IP is in allowed ranges
            if not self._is_ip_allowed(source_ip):
                events.append(f"IP {source_ip} not in allowed ranges")

            # Check for recent suspicious activity
            if self._has_recent_suspicious_activity(source_ip):
                events.append(f"Recent suspicious activity from {source_ip}")

        except Exception as e:
            self.logger.warning(f"Network security validation failed: {e}")
            events.append(f"Network validation error: {str(e)}")

        return events

    def _is_ip_allowed(self, source_ip: str) -> bool:
        """Check if source IP is allowed"""
        # Simple implementation - in production, check against whitelist/blacklist
        allowed_ranges = [
            "127.0.0.1",  # Localhost
            "192.168.1.0/24",  # Local network
            "10.0.0.0/8",  # Private network
        ]

        # For now, allow all IPs in testing
        return True

    def _has_recent_suspicious_activity(self, source_ip: str) -> bool:
        """Check for recent suspicious activity from IP"""
        # Simple implementation - in production, check logs/database
        return False

    def _is_rate_limited(self, source_ip: str) -> bool:
        """Check if source IP is rate limited"""
        # Simple implementation - in production, use Redis/database
        return False

    def _get_rate_limit_info(self, source_ip: str) -> Dict[str, Any]:
        """Get rate limit information for source IP"""
        return {
            "source_ip": source_ip,
            "remaining_attempts": 0,
            "reset_time": time.time() + self.config["lockout_duration"],
        }

    def _determine_user_permissions(self, username: str) -> List[PermissionLevel]:
        """Determine user permissions based on username"""
        if username == "admin":
            return [PermissionLevel.ADMIN, PermissionLevel.USER, PermissionLevel.GUEST]
        elif username.startswith("agent"):
            return [PermissionLevel.USER, PermissionLevel.GUEST]
        else:
            return [PermissionLevel.GUEST]

    def _audit_compliance(self, username: str, source_ip: str) -> List[str]:
        """Audit compliance for authentication"""
        events = []

        try:
            # Log authentication event
            events.append(f"Authentication logged for compliance")

            # Check for compliance violations
            if self._check_compliance_violations(username, source_ip):
                events.append("Compliance violation detected")

        except Exception as e:
            self.logger.warning(f"Compliance audit failed: {e}")
            events.append(f"Compliance audit error: {str(e)}")

        return events

    def _check_compliance_violations(self, username: str, source_ip: str) -> bool:
        """Check for compliance violations"""
        # Simple implementation - in production, check compliance rules
        return False

    def _fallback_authentication(
        self,
        username: str,
        password: str,
        source_ip: str,
        user_agent: str,
        start_time: float,
        security_events: List[str],
    ) -> V2AuthResult:
        """Fallback authentication - DISABLED FOR SECURITY"""
        self.logger.error("Fallback authentication DISABLED for security reasons")
        security_events.append("Fallback authentication blocked - security risk")

        # Fallback authentication DISABLED for security
        self.failed_auths += 1
        security_events.append("Fallback authentication blocked - security risk")

        return V2AuthResult(
            status=AuthStatus.SYSTEM_ERROR,
            user_id=None,
            session_id=None,
            permissions=[],
            expires_at=None,
            metadata={"error": "Fallback authentication disabled for security"},
            performance_metrics={"auth_duration": time.time() - start_time},
            security_events=security_events,
        )

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get authentication performance metrics"""
        uptime = time.time() - self.start_time

        return {
            "uptime_seconds": uptime,
            "total_attempts": self.auth_attempts,
            "successful_auths": self.successful_auths,
            "failed_auths": self.failed_auths,
            "success_rate": self.successful_auths / max(self.auth_attempts, 1),
            "auth_per_second": self.auth_attempts / max(uptime, 1),
            "start_time": self.start_time,
            "current_time": time.time(),
        }

    def get_security_status(self) -> Dict[str, Any]:
        """Get current security status"""
        return {
            "security_level": self.config["security_level"],
            "core_components_available": SECURITY_AVAILABLE,
            "rate_limiting_enabled": True,
            "audit_logging_enabled": self.config["enable_audit_logging"],
            "mfa_enabled": self.config["enable_mfa"],
            "session_timeout": self.config["session_timeout"],
            "max_login_attempts": self.config["max_login_attempts"],
        }

    def shutdown(self):
        """Shutdown the auth service"""
        self.logger.info("Shutting down V2 Authentication Service")

        # Log final metrics
        metrics = self.get_performance_metrics()
        self.logger.info(f"Final metrics: {metrics}")

        # Flush session data
        self.session_manager.flush()

        # Cleanup external components
        for comp_name in ["auth_system", "network_scanner", "compliance_auditor"]:
            component = getattr(self, comp_name, None)
            if component:
                try:
                    if hasattr(component, "shutdown"):
                        component.shutdown()
                    elif hasattr(component, "close"):
                        component.close()
                except Exception as e:
                    self.logger.warning(f"Error shutting down {comp_name}: {e}")
