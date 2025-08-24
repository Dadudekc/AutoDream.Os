#!/usr/bin/env python3
"""Network security data models and policy definitions."""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class NetworkDevice:
    """Network device information."""

    ip_address: str
    mac_address: Optional[str]
    hostname: Optional[str]
    is_active: bool
    last_seen: float
    open_ports: List[int]
    services: List[str]


@dataclass
class SecurityEvent:
    """Security event data structure."""

    source_ip: str
    event_type: str
    severity: str
    timestamp: float
    details: Dict
    source: str


__all__ = ["NetworkDevice", "SecurityEvent"]
