from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """User account information"""
    user_id: str
    username: str
    email: str
    password_hash: str
    role: str
    is_active: bool
    created_at: str
    last_login: Optional[str] = None
    failed_attempts: int = 0
    locked_until: Optional[str] = None


@dataclass
class UserSession:
    """User session information"""
    session_id: str
    user_id: str
    is_active: bool
    created_at: str
    last_activity: str
    ip_address: str
    user_agent: str
