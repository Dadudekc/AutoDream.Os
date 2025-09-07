import json
import time
import hmac
import hashlib
import base64
from typing import Optional


class AuthenticationManager:
    """Manages authentication and authorization for cross-agent communication"""

    def __init__(self, secret_key: str | None = None):
        self.secret_key = secret_key or "default-secret-key-change-in-production"
        self.agent_tokens: dict[str, str] = {}
        self.token_expiry: dict[str, int] = {}

    def generate_agent_token(self, agent_id: str, expires_in: int = 3600) -> str:
        """Generate authentication token for an agent"""
        payload = {
            "agent_id": agent_id,
            "exp": int(time.time()) + expires_in,
            "iat": int(time.time()),
        }

        # Create JWT-like token (simplified)
        header = base64.b64encode(
            json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
        ).decode()
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode()

        # Create signature
        message = f"{header}.{payload_b64}"
        signature = hmac.new(
            self.secret_key.encode(), message.encode(), hashlib.sha256
        ).hexdigest()

        token = f"{header}.{payload_b64}.{signature}"

        # Store token
        self.agent_tokens[agent_id] = token
        self.token_expiry[agent_id] = payload["exp"]

        return token

    def validate_agent_token(self, token: str) -> Optional[str]:
        """Validate authentication token and return agent_id if valid"""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None

            header_b64, payload_b64, signature = parts

            # Verify signature
            message = f"{header_b64}.{payload_b64}"
            expected_signature = hmac.new(
                self.secret_key.encode(), message.encode(), hashlib.sha256
            ).hexdigest()

            if signature != expected_signature:
                return None

            # Decode payload
            payload = json.loads(base64.b64decode(payload_b64).decode())

            # Check expiration and that the token matches the stored token
            agent_id = payload["agent_id"]
            if payload["exp"] < int(time.time()):
                return None
            if self.agent_tokens.get(agent_id) != token:
                return None

            return agent_id
        except Exception:
            return None

    def revoke_agent_token(self, agent_id: str) -> bool:
        """Revoke authentication token for an agent"""
        if agent_id in self.agent_tokens:
            del self.agent_tokens[agent_id]
            if agent_id in self.token_expiry:
                del self.token_expiry[agent_id]
            return True
        return False
