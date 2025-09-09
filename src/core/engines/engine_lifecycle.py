"""
Engine Lifecycle Management - V2 Compliance Module
=================================================

Manages engine lifecycle following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional
from .contracts import EngineContext, EngineResult


class EngineLifecycleManager:
    """Manages engine lifecycle operations."""

    def __init__(self, engine_id: str):
        """Initialize lifecycle manager."""
        self.engine_id = engine_id
        self.initialized_at: Optional[datetime] = None
        self.last_operation_at: Optional[datetime] = None

    def initialize_engine(self, context: EngineContext) -> EngineResult:
        """Initialize the engine."""
        try:
            self.initialized_at = datetime.now()
            self.last_operation_at = datetime.now()

            return EngineResult(
                success=True,
                engine_id=self.engine_id,
                operation="initialize",
                data={"initialized_at": self.initialized_at.isoformat()},
                metadata={"lifecycle": "initialized"}
            )
        except Exception as e:
            return EngineResult(
                success=False,
                engine_id=self.engine_id,
                operation="initialize",
                error=str(e),
                metadata={"lifecycle": "failed"}
            )

    def shutdown_engine(self) -> EngineResult:
        """Shutdown the engine."""
        try:
            self.last_operation_at = datetime.now()

            return EngineResult(
                success=True,
                engine_id=self.engine_id,
                operation="shutdown",
                data={"shutdown_at": datetime.now().isoformat()},
                metadata={"lifecycle": "shutdown"}
            )
        except Exception as e:
            return EngineResult(
                success=False,
                engine_id=self.engine_id,
                operation="shutdown",
                error=str(e),
                metadata={"lifecycle": "shutdown_failed"}
            )

    def update_last_operation(self):
        """Update the last operation timestamp."""
        self.last_operation_at = datetime.now()

    def get_lifecycle_status(self) -> dict[str, Any]:
        """Get lifecycle status information."""
        return {
            "engine_id": self.engine_id,
            "initialized_at": self.initialized_at.isoformat() if self.initialized_at else None,
            "last_operation_at": self.last_operation_at.isoformat() if self.last_operation_at else None,
            "uptime_seconds": (
                datetime.now() - self.initialized_at
            ).total_seconds() if self.initialized_at else 0
        }
