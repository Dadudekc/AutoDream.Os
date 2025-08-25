from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class SecurityLevel(Enum):
    PUBLIC = "public"
    RESTRICTED = "restricted"
    PRIVATE = "private"
    ISOLATED = "isolated"
    SECURE = "secure"


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    SHARE = "share"


@dataclass
class SecurityPolicy:
    workspace_name: str
    security_level: SecurityLevel
    allowed_agents: List[str]
    permissions: Dict[str, List[Permission]]
    isolation_rules: List[str]
    encryption_enabled: bool
    audit_logging: bool
    max_access_attempts: int


@dataclass
class AccessLog:
    timestamp: str
    agent_id: str
    action: str
    resource: str
    success: bool
    ip_address: str = "unknown"


__all__ = [
    "SecurityLevel",
    "Permission",
    "SecurityPolicy",
    "AccessLog",
]
