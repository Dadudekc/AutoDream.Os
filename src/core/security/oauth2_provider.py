# V3-001: Cloud Infrastructure Setup - OAuth2 Provider
# Agent-1: Architecture Foundation Specialist
# 
# OAuth2 authentication provider for the V2_SWARM system

import os
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from dataclasses import dataclass
import jwt
from cryptography.fernet import Fernet


@dataclass
class OAuth2Client:
    """OAuth2 client configuration."""
    client_id: str
    client_secret: str
    redirect_uris: List[str]
    scopes: List[str]
    grant_types: List[str]
    created_at: datetime
    is_active: bool = True


@dataclass
class AccessToken:
    """OAuth2 access token."""
    token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    scope: str = "read write"
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class OAuth2Provider:
    """OAuth2 authentication provider for V2_SWARM system."""
    
    def __init__(self):
        self.jwt_secret = os.getenv("JWT_SECRET", Fernet.generate_key().decode())
        self.encryption_key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
        self.clients: Dict[str, OAuth2Client] = {}
        self.tokens: Dict[str, AccessToken] = {}
        self._initialize_default_client()
    
    def _initialize_default_client(self) -> None:
        """Initialize default OAuth2 client for the system."""
        default_client = OAuth2Client(
            client_id="swarm-v3-client",
            client_secret=secrets.token_urlsafe(32),
            redirect_uris=["http://localhost:8000/callback"],
            scopes=["read", "write", "admin"],
            grant_types=["authorization_code", "client_credentials"],
            created_at=datetime.utcnow()
        )
        self.clients[default_client.client_id] = default_client
    
    def create_client(self, client_id: str, redirect_uris: List[str], 
                     scopes: List[str] = None) -> OAuth2Client:
        """Create a new OAuth2 client."""
        if scopes is None:
            scopes = ["read", "write"]
        
        client = OAuth2Client(
            client_id=client_id,
            client_secret=secrets.token_urlsafe(32),
            redirect_uris=redirect_uris,
            scopes=scopes,
            grant_types=["authorization_code"],
            created_at=datetime.utcnow()
        )
        
        self.clients[client_id] = client
        return client
    
    def validate_client(self, client_id: str, client_secret: str) -> bool:
        """Validate OAuth2 client credentials."""
        client = self.clients.get(client_id)
        if not client or not client.is_active:
            return False
        return client.client_secret == client_secret
    
    def generate_authorization_code(self, client_id: str, user_id: str, 
                                  redirect_uri: str, scope: str) -> str:
        """Generate authorization code for OAuth2 flow."""
        payload = {
            "client_id": client_id,
            "user_id": user_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "exp": datetime.utcnow() + timedelta(minutes=10)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")
    
    def exchange_code_for_token(self, code: str, client_id: str, 
                              client_secret: str) -> Optional[AccessToken]:
        """Exchange authorization code for access token."""
        try:
            payload = jwt.decode(code, self.jwt_secret, algorithms=["HS256"])
            
            if payload["client_id"] != client_id:
                return None
            
            if not self.validate_client(client_id, client_secret):
                return None
            
            # Generate access token
            access_token = self._generate_access_token(
                client_id, payload["user_id"], payload["scope"]
            )
            
            return access_token
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def _generate_access_token(self, client_id: str, user_id: str, 
                             scope: str) -> AccessToken:
        """Generate JWT access token."""
        payload = {
            "client_id": client_id,
            "user_id": user_id,
            "scope": scope,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow(),
            "iss": "swarm-v3-oauth2"
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
        
        access_token = AccessToken(
            token=token,
            expires_in=3600,
            scope=scope
        )
        
        self.tokens[token] = access_token
        return access_token
    
    def validate_token(self, token: str) -> Optional[Dict]:
        """Validate and decode access token."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            
            # Check if token exists in our store
            if token not in self.tokens:
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def revoke_token(self, token: str) -> bool:
        """Revoke access token."""
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False
    
    def get_client_info(self, client_id: str) -> Optional[OAuth2Client]:
        """Get OAuth2 client information."""
        return self.clients.get(client_id)
    
    def list_clients(self) -> List[OAuth2Client]:
        """List all OAuth2 clients."""
        return list(self.clients.values())
    
    def deactivate_client(self, client_id: str) -> bool:
        """Deactivate OAuth2 client."""
        client = self.clients.get(client_id)
        if client:
            client.is_active = False
            return True
        return False



