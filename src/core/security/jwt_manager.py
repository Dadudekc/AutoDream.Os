# V3-001: Cloud Infrastructure Setup - JWT Manager
# Agent-1: Architecture Foundation Specialist
#
# JWT token management for the V2_SWARM system

import os
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

import jwt


@dataclass
class TokenPayload:
    """JWT token payload structure."""

    user_id: str
    agent_id: str | None = None
    roles: list = None
    permissions: list = None
    exp: datetime | None = None
    iat: datetime | None = None
    iss: str = "swarm-v3"
    aud: str = "swarm-agents"

    def __post_init__(self):
        if self.roles is None:
            self.roles = []
        if self.permissions is None:
            self.permissions = []
        if self.iat is None:
            self.iat = datetime.utcnow()
        if self.exp is None:
            self.exp = self.iat + timedelta(hours=1)


class JWTManager:
    """JWT token management for V2_SWARM system."""

    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", self._generate_secret())
        self.algorithm = "HS256"
        self.access_token_expiry = timedelta(hours=1)
        self.refresh_token_expiry = timedelta(days=7)
        self.issuer = "swarm-v3"
        self.audience = "swarm-agents"

    def _generate_secret(self) -> str:
        """Generate a secure secret key."""
        return secrets.token_urlsafe(32)

    def create_access_token(
        self,
        user_id: str,
        agent_id: str = None,
        roles: list = None,
        permissions: list = None,
        custom_claims: dict[str, Any] = None,
    ) -> str:
        """Create JWT access token."""
        payload = TokenPayload(
            user_id=user_id,
            agent_id=agent_id,
            roles=roles or [],
            permissions=permissions or [],
            exp=datetime.utcnow() + self.access_token_expiry,
        )

        # Convert to dict for JWT encoding
        token_data = {
            "user_id": payload.user_id,
            "agent_id": payload.agent_id,
            "roles": payload.roles,
            "permissions": payload.permissions,
            "exp": payload.exp,
            "iat": payload.iat,
            "iss": payload.iss,
            "aud": payload.aud,
        }

        # Add custom claims if provided
        if custom_claims:
            token_data.update(custom_claims)

        return jwt.encode(token_data, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token."""
        payload = {
            "user_id": user_id,
            "type": "refresh",
            "exp": datetime.utcnow() + self.refresh_token_expiry,
            "iat": datetime.utcnow(),
            "iss": self.issuer,
            "aud": self.audience,
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict[str, Any] | None:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                issuer=self.issuer,
                audience=self.audience,
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except jwt.InvalidIssuerError:
            return None
        except jwt.InvalidAudienceError:
            return None

    def refresh_access_token(self, refresh_token: str) -> str | None:
        """Generate new access token from refresh token."""
        payload = self.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        user_id = payload.get("user_id")
        if not user_id:
            return None

        # Create new access token
        return self.create_access_token(user_id)

    def get_token_info(self, token: str) -> dict[str, Any] | None:
        """Get token information without verification."""
        try:
            # Decode without verification to get payload
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except jwt.InvalidTokenError:
            return None

    def is_token_expired(self, token: str) -> bool:
        """Check if token is expired."""
        payload = self.get_token_info(token)
        if not payload:
            return True

        exp_timestamp = payload.get("exp")
        if not exp_timestamp:
            return True

        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        return exp_datetime < datetime.utcnow()

    def extract_user_id(self, token: str) -> str | None:
        """Extract user ID from token."""
        payload = self.verify_token(token)
        return payload.get("user_id") if payload else None

    def extract_agent_id(self, token: str) -> str | None:
        """Extract agent ID from token."""
        payload = self.verify_token(token)
        return payload.get("agent_id") if payload else None

    def extract_roles(self, token: str) -> list:
        """Extract roles from token."""
        payload = self.verify_token(token)
        return payload.get("roles", []) if payload else []

    def extract_permissions(self, token: str) -> list:
        """Extract permissions from token."""
        payload = self.verify_token(token)
        return payload.get("permissions", []) if payload else []

    def has_role(self, token: str, role: str) -> bool:
        """Check if token has specific role."""
        roles = self.extract_roles(token)
        return role in roles

    def has_permission(self, token: str, permission: str) -> bool:
        """Check if token has specific permission."""
        permissions = self.extract_permissions(token)
        return permission in permissions

    def create_agent_token(self, agent_id: str, permissions: list = None) -> str:
        """Create token for agent authentication."""
        return self.create_access_token(
            user_id=f"agent-{agent_id}",
            agent_id=agent_id,
            roles=["agent"],
            permissions=permissions or ["read", "write", "coordinate"],
        )

    def validate_agent_token(self, token: str) -> str | None:
        """Validate agent token and return agent ID."""
        payload = self.verify_token(token)
        if not payload:
            return None

        if "agent" not in payload.get("roles", []):
            return None

        return payload.get("agent_id")
