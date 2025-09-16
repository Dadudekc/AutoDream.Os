#!/usr/bin/env python3
"""
Data Processing Interfaces - Data Processing Protocol Definitions
==============================================================

Data processing interface definitions for system components.
Part of the modularization of unified_core_interfaces.py for V2 compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol


class IDataProcessor(Protocol):
    """Interface for data processing components."""

    def process(self, data: Any) -> Any:
        """Process input data and return result."""
        ...

    def can_process(self, data_type: str) -> bool:
        """Check if processor can handle data type."""
        ...

    def get_supported_types(self) -> List[str]:
        """Get list of supported data types."""
        ...

    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        ...


class IDataValidator(Protocol):
    """Interface for data validation components."""

    def validate(self, data: Any) -> bool:
        """Validate input data."""
        ...

    def get_validation_errors(self) -> List[str]:
        """Get list of validation errors."""
        ...

    def clear_errors(self) -> None:
        """Clear validation errors."""
        ...

    def is_valid(self, data: Any) -> bool:
        """Check if data is valid."""
        ...


class IAsyncTask(Protocol):
    """Interface for asynchronous task components."""

    def execute_async(self, task_data: Any) -> Any:
        """Execute task asynchronously."""
        ...

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task."""
        ...

    def get_task_status(self, task_id: str) -> str:
        """Get status of a task."""
        ...

    def is_task_complete(self, task_id: str) -> bool:
        """Check if task is complete."""
        ...


class IAsyncTaskManager(Protocol):
    """Interface for asynchronous task management."""

    def submit_task(self, task: IAsyncTask, task_data: Any) -> str:
        """Submit a task for execution."""
        ...

    def get_task_result(self, task_id: str) -> Optional[Any]:
        """Get result of completed task."""
        ...

    def get_active_tasks(self) -> List[str]:
        """Get list of active task IDs."""
        ...

    def get_completed_tasks(self) -> List[str]:
        """Get list of completed task IDs."""
        ...

    def cleanup_completed_tasks(self) -> int:
        """Clean up completed tasks and return count."""
        ...





