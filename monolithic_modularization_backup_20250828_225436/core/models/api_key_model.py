"""Data model for API key management."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class APIKey:
    """Unified API key representation."""

    key_id: str
    service: str
    description: str
    key_hash: str
    permissions: List[str]
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool = True
    usage_count: int = 0
    last_used: Optional[datetime] = None
