"""
Core Resource Manager - Phase-2 Manager Consolidation
====================================================

Consolidates FileManager, FileLockManager, and AgentContextManager.
Handles all resource operations: files, locks, and agent contexts.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Refactored by: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

from __future__ import annotations

import os
import shutil
from typing import Any

from .contracts import ManagerContext, ManagerResult, ResourceManager
from .resource_context_operations import ContextOperations
from .resource_file_operations import FileOperations
from .resource_lock_operations import LockOperations


class CoreResourceManager(ResourceManager):
    """Core resource manager - consolidates file, lock, and context operations."""

    def __init__(self):
        """Initialize core resource manager."""
        self.file_ops = FileOperations()
        self.lock_ops = LockOperations()
        self.context_ops = ContextOperations()

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize resource manager."""
        try:
            # Ensure runtime directory exists
            os.makedirs("runtime", exist_ok=True)

            # Load existing locks
            self.lock_ops.load_locks()

            context.logger("Core Resource Manager initialized")
            return True
        except Exception as e:
            context.logger(f"Failed to initialize Core Resource Manager: {e}")
            return False

    def execute(
        self, context: ManagerContext, operation: str, payload: dict[str, Any]
    ) -> ManagerResult:
        """Execute resource operation."""
        try:
            if operation == "create_resource":
                return self.create_resource(
                    context, payload.get("resource_type", ""), payload
                )
            elif operation == "get_resource":
                return self.get_resource(context, payload.get("resource_id", ""))
            elif operation == "update_resource":
                return self.update_resource(
                    context, payload.get("resource_id", ""), payload
                )
            elif operation == "delete_resource":
                return self.delete_resource(context, payload.get("resource_id", ""))
            elif operation == "file_operation":
                return self.file_ops.handle_operation(context, payload)
            elif operation == "lock_operation":
                return self.lock_ops.handle_operation(context, payload)
            elif operation == "context_operation":
                return self.context_ops.handle_operation(context, payload)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown operation: {operation}",
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

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
                return self.file_ops.create_directory(
                    context, data.get("dir_path", "")
                )
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

    def get_resource(
        self, context: ManagerContext, resource_id: str
    ) -> ManagerResult:
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
                        data={
                            "type": "directory",
                            "files": files,
                            "path": resource_id,
                        },
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
                        data={
                            "type": "file",
                            "path": resource_id,
                            "updated": True,
                        },
                        metrics={"file_size": len(updates["content"])},
                    )

            # Try context update
            updated_context = self.context_ops.update_context_direct(
                resource_id, updates
            )
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

    def delete_resource(
        self, context: ManagerContext, resource_id: str
    ) -> ManagerResult:
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
                        data={
                            "type": "directory",
                            "path": resource_id,
                            "deleted": True,
                        },
                        metrics={},
                    )

            # Try context deletion
            if self.context_ops.delete_context_if_exists(resource_id):
                return ManagerResult(
                    success=True,
                    data={
                        "type": "context",
                        "context_id": resource_id,
                        "deleted": True,
                    },
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

    def cleanup(self, context: ManagerContext) -> bool:
        """Cleanup resource manager."""
        try:
            # Save locks
            self.lock_ops.save_locks()

            # Clear contexts
            self.context_ops.clear_contexts()

            # Clear locks
            self.lock_ops.clear_locks()

            context.logger("Core Resource Manager cleaned up")
            return True
        except Exception as e:
            context.logger(f"Failed to cleanup Core Resource Manager: {e}")
            return False

    def get_status(self) -> dict[str, Any]:
        """Get resource manager status."""
        return {
            "file_operations": self.file_ops.operations_count,
            "lock_operations": self.lock_ops.operations_count,
            "context_operations": self.context_ops.operations_count,
            "active_locks": self.lock_ops.get_lock_count(),
            "agent_contexts": self.context_ops.get_context_count(),
            "context_ids": self.context_ops.get_context_ids(),
        }
