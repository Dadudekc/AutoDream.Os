"""
Resource CRUD Operations Helper
================================

Extracted CRUD operations from CoreResourceManager for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

import os
import shutil
from typing import Any

from .contracts import ManagerContext, ManagerResult


class ResourceCRUDOperations:
    """Handles CRUD operations for resources."""

    def __init__(self, file_ops, lock_ops, context_ops):
        """Initialize with operation handlers."""
        self.file_ops = file_ops
        self.lock_ops = lock_ops
        self.context_ops = context_ops

    def create_resource(
        self, context: ManagerContext, resource_type: str, data: dict[str, Any]
    ) -> ManagerResult:
        """Create a resource."""
        try:
            if resource_type == "file":
                return self.file_ops.create_file(
                    context, data.get("file_path", ""), data.get("content", "")
                )
            elif resource_type == "directory":
                return self.file_ops.create_directory(context, data.get("dir_path", ""))
            elif resource_type == "context":
                return self.context_ops.create_context(
                    context, data.get("agent_id", ""), data.get("context_data", {})
                )
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown resource type: {resource_type}",
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def get_resource(self, context: ManagerContext, resource_id: str) -> ManagerResult:
        """Get a resource."""
        try:
            # Try file first
            if os.path.exists(resource_id):
                if os.path.isfile(resource_id):
                    content = self.file_ops.read_file(resource_id)
                    return ManagerResult(
                        success=True,
                        data={"type": "file", "content": content, "path": resource_id},
                        metrics={"file_size": len(content)},
                    )
                elif os.path.isdir(resource_id):
                    files = os.listdir(resource_id)
                    return ManagerResult(
                        success=True,
                        data={"type": "directory", "files": files, "path": resource_id},
                        metrics={"file_count": len(files)},
                    )

            # Try context
            agent_context = self.context_ops.get_context_if_exists(resource_id)
            if agent_context:
                return ManagerResult(
                    success=True,
                    data={"type": "context", "context": agent_context},
                    metrics={"context_keys": len(agent_context)},
                )

            return ManagerResult(
                success=False,
                data={},
                metrics={},
                error=f"Resource not found: {resource_id}",
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def update_resource(
        self, context: ManagerContext, resource_id: str, updates: dict[str, Any]
    ) -> ManagerResult:
        """Update a resource."""
        try:
            # Try file update
            if os.path.exists(resource_id) and os.path.isfile(resource_id):
                if "content" in updates:
                    self.file_ops.write_file(resource_id, updates["content"])
                    return ManagerResult(
                        success=True,
                        data={"type": "file", "path": resource_id, "updated": True},
                        metrics={"file_size": len(updates["content"])},
                    )

            # Try context update
            updated_context = self.context_ops.update_context_direct(resource_id, updates)
            if updated_context:
                return ManagerResult(
                    success=True,
                    data={"type": "context", "context": updated_context},
                    metrics={"context_keys": len(updated_context)},
                )

            return ManagerResult(
                success=False,
                data={},
                metrics={},
                error=f"Resource not found or cannot be updated: {resource_id}",
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def delete_resource(self, context: ManagerContext, resource_id: str) -> ManagerResult:
        """Delete a resource."""
        try:
            # Try file deletion
            if os.path.exists(resource_id):
                if os.path.isfile(resource_id):
                    os.remove(resource_id)
                    return ManagerResult(
                        success=True,
                        data={"type": "file", "path": resource_id, "deleted": True},
                        metrics={},
                    )
                elif os.path.isdir(resource_id):
                    shutil.rmtree(resource_id)
                    return ManagerResult(
                        success=True,
                        data={"type": "directory", "path": resource_id, "deleted": True},
                        metrics={},
                    )

            # Try context deletion
            if self.context_ops.delete_context_if_exists(resource_id):
                return ManagerResult(
                    success=True,
                    data={"type": "context", "context_id": resource_id, "deleted": True},
                    metrics={},
                )

            return ManagerResult(
                success=False,
                data={},
                metrics={},
                error=f"Resource not found: {resource_id}",
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))
