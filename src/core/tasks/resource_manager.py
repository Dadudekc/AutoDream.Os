#!/usr/bin/env python3
"""
Resource Manager - Agent Cellphone V2
=====================================

Handles task resource allocation and management.
Single responsibility: Manage resources assigned to tasks.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .logger import get_task_logger


@dataclass
class ResourceAllocation:
    """Represents resources allocated to a task."""

    task_id: str
    resources: Dict[str, Any]
    allocated: bool = True


class ResourceManager:
    """Manages resource allocation for tasks."""

    def __init__(self) -> None:
        self.logger = get_task_logger("ResourceManager")
        self._allocations: Dict[str, ResourceAllocation] = {}

    def allocate(self, task_id: str, resources: Dict[str, Any]) -> None:
        """Allocate resources to a task."""
        self._allocations[task_id] = ResourceAllocation(task_id, resources)
        self.logger.debug(f"Resources allocated to {task_id}: {resources}")

    def release(self, task_id: str) -> None:
        """Release resources for a task."""
        allocation = self._allocations.get(task_id)
        if allocation:
            allocation.allocated = False
            self.logger.debug(f"Resources released for {task_id}")

    def get_allocation(self, task_id: str) -> Optional[ResourceAllocation]:
        """Get resource allocation for a task."""
        return self._allocations.get(task_id)


__all__ = ["ResourceManager", "ResourceAllocation"]
