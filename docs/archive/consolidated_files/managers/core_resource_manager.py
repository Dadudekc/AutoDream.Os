"""
Core Resource Manager - Phase-2 Manager Consolidation
====================================================

Consolidates FileManager, FileLockManager, and AgentContextManager.
Handles all resource operations: files, locks, and agent contexts.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations

import json
import os
import shutil
import threading
from datetime import datetime
from typing import Any

from .contracts import ManagerContext, ManagerResult, ResourceManager


class CoreResourceManager(ResourceManager):
    """Core resource manager - consolidates file, lock, and context operations."""

    def __init__(self):
        """Initialize core resource manager."""
        self.file_operations_count = 0
        self.lock_operations_count = 0
        self.context_operations_count = 0
        self._locks: dict[str, threading.Lock] = {}
        self._agent_contexts: dict[str, dict[str, Any]] = {}
        self._lock_file = "runtime/resource_locks.json"

    def initialize(self, context: ManagerContext) -> bool:
        """Initialize resource manager."""
        try:
            # Ensure runtime directory exists
            os.makedirs("runtime", exist_ok=True)

            # Load existing locks
            self._load_locks()

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
                return self.create_resource(context, payload.get("resource_type", ""), payload)
            elif operation == "get_resource":
                return self.get_resource(context, payload.get("resource_id", ""))
            elif operation == "update_resource":
                return self.update_resource(context, payload.get("resource_id", ""), payload)
            elif operation == "delete_resource":
                return self.delete_resource(context, payload.get("resource_id", ""))
            elif operation == "file_operation":
                return self._handle_file_operation(context, payload)
            elif operation == "lock_operation":
                return self._handle_lock_operation(context, payload)
            elif operation == "context_operation":
                return self._handle_context_operation(context, payload)
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
                return self._create_file(context, data)
            elif resource_type == "directory":
                return self._create_directory(context, data)
            elif resource_type == "context":
                return self._create_context(context, data)
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
                    content = self._read_file(resource_id)
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
            if resource_id in self._agent_contexts:
                return ManagerResult(
                    success=True,
                    data={
                        "type": "context",
                        "context": self._agent_contexts[resource_id],
                    },
                    metrics={"context_keys": len(self._agent_contexts[resource_id])},
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
                    self._write_file(resource_id, updates["content"])
                    return ManagerResult(
                        success=True,
                        data={"type": "file", "path": resource_id, "updated": True},
                        metrics={"file_size": len(updates["content"])},
                    )

            # Try context update
            if resource_id in self._agent_contexts:
                self._agent_contexts[resource_id].update(updates)
                self._agent_contexts[resource_id]["last_updated"] = datetime.now().isoformat()
                return ManagerResult(
                    success=True,
                    data={
                        "type": "context",
                        "context": self._agent_contexts[resource_id],
                    },
                    metrics={"context_keys": len(self._agent_contexts[resource_id])},
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
                        data={
                            "type": "directory",
                            "path": resource_id,
                            "deleted": True,
                        },
                        metrics={},
                    )

            # Try context deletion
            if resource_id in self._agent_contexts:
                del self._agent_contexts[resource_id]
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
            self._save_locks()

            # Clear contexts
            self._agent_contexts.clear()

            # Clear locks
            self._locks.clear()

            context.logger("Core Resource Manager cleaned up")
            return True
        except Exception as e:
            context.logger(f"Failed to cleanup Core Resource Manager: {e}")
            return False

    def get_status(self) -> dict[str, Any]:
        """Get resource manager status."""
        return {
            "file_operations": self.file_operations_count,
            "lock_operations": self.lock_operations_count,
            "context_operations": self.context_operations_count,
            "active_locks": len(self._locks),
            "agent_contexts": len(self._agent_contexts),
            "context_ids": list(self._agent_contexts.keys()),
        }

    def _handle_file_operation(
        self, context: ManagerContext, payload: dict[str, Any]
    ) -> ManagerResult:
        """Handle file operations."""
        operation = payload.get("file_operation", "")
        file_path = payload.get("file_path", "")

        try:
            if operation == "read":
                content = self._read_file(file_path)
                self.file_operations_count += 1
                return ManagerResult(
                    success=True,
                    data={"content": content, "path": file_path},
                    metrics={"file_size": len(content)},
                )
            elif operation == "write":
                content = payload.get("content", "")
                self._write_file(file_path, content)
                self.file_operations_count += 1
                return ManagerResult(
                    success=True,
                    data={"path": file_path, "written": True},
                    metrics={"file_size": len(content)},
                )
            elif operation == "copy":
                dest = payload.get("destination", "")
                shutil.copy2(file_path, dest)
                self.file_operations_count += 1
                return ManagerResult(
                    success=True,
                    data={"source": file_path, "destination": dest, "copied": True},
                    metrics={},
                )
            elif operation == "move":
                dest = payload.get("destination", "")
                shutil.move(file_path, dest)
                self.file_operations_count += 1
                return ManagerResult(
                    success=True,
                    data={"source": file_path, "destination": dest, "moved": True},
                    metrics={},
                )
            elif operation == "delete":
                os.remove(file_path)
                self.file_operations_count += 1
                return ManagerResult(
                    success=True, data={"path": file_path, "deleted": True}, metrics={}
                )
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown file operation: {operation}",
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _handle_lock_operation(
        self, context: ManagerContext, payload: dict[str, Any]
    ) -> ManagerResult:
        """Handle lock operations."""
        operation = payload.get("lock_operation", "")
        lock_id = payload.get("lock_id", "")

        try:
            if operation == "acquire":
                if lock_id not in self._locks:
                    self._locks[lock_id] = threading.Lock()

                acquired = self._locks[lock_id].acquire(blocking=False)
                self.lock_operations_count += 1
                return ManagerResult(
                    success=acquired,
                    data={"lock_id": lock_id, "acquired": acquired},
                    metrics={},
                )
            elif operation == "release":
                if lock_id in self._locks:
                    self._locks[lock_id].release()
                    self.lock_operations_count += 1
                    return ManagerResult(
                        success=True,
                        data={"lock_id": lock_id, "released": True},
                        metrics={},
                    )
                else:
                    return ManagerResult(
                        success=False,
                        data={},
                        metrics={},
                        error=f"Lock not found: {lock_id}",
                    )
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown lock operation: {operation}",
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _handle_context_operation(
        self, context: ManagerContext, payload: dict[str, Any]
    ) -> ManagerResult:
        """Handle context operations."""
        operation = payload.get("context_operation", "")
        agent_id = payload.get("agent_id", "")

        try:
            if operation == "set":
                context_data = payload.get("context_data", {})
                self._agent_contexts[agent_id] = {
                    **context_data,
                    "last_updated": datetime.now().isoformat(),
                }
                self.context_operations_count += 1
                return ManagerResult(
                    success=True,
                    data={
                        "agent_id": agent_id,
                        "context": self._agent_contexts[agent_id],
                    },
                    metrics={"context_keys": len(context_data)},
                )
            elif operation == "get":
                if agent_id in self._agent_contexts:
                    return ManagerResult(
                        success=True,
                        data={
                            "agent_id": agent_id,
                            "context": self._agent_contexts[agent_id],
                        },
                        metrics={"context_keys": len(self._agent_contexts[agent_id])},
                    )
                else:
                    return ManagerResult(
                        success=False,
                        data={},
                        metrics={},
                        error=f"Context not found for agent: {agent_id}",
                    )
            elif operation == "update":
                updates = payload.get("updates", {})
                if agent_id in self._agent_contexts:
                    self._agent_contexts[agent_id].update(updates)
                    self._agent_contexts[agent_id]["last_updated"] = datetime.now().isoformat()
                    self.context_operations_count += 1
                    return ManagerResult(
                        success=True,
                        data={
                            "agent_id": agent_id,
                            "context": self._agent_contexts[agent_id],
                        },
                        metrics={"context_keys": len(self._agent_contexts[agent_id])},
                    )
                else:
                    return ManagerResult(
                        success=False,
                        data={},
                        metrics={},
                        error=f"Context not found for agent: {agent_id}",
                    )
            elif operation == "delete":
                if agent_id in self._agent_contexts:
                    del self._agent_contexts[agent_id]
                    self.context_operations_count += 1
                    return ManagerResult(
                        success=True,
                        data={"agent_id": agent_id, "deleted": True},
                        metrics={},
                    )
                else:
                    return ManagerResult(
                        success=False,
                        data={},
                        metrics={},
                        error=f"Context not found for agent: {agent_id}",
                    )
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown context operation: {operation}",
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _create_file(self, context: ManagerContext, data: dict[str, Any]) -> ManagerResult:
        """Create a file."""
        file_path = data.get("file_path", "")
        content = data.get("content", "")

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            self._write_file(file_path, content)
            self.file_operations_count += 1
            return ManagerResult(
                success=True,
                data={"type": "file", "path": file_path, "created": True},
                metrics={"file_size": len(content)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _create_directory(self, context: ManagerContext, data: dict[str, Any]) -> ManagerResult:
        """Create a directory."""
        dir_path = data.get("dir_path", "")

        try:
            os.makedirs(dir_path, exist_ok=True)
            self.file_operations_count += 1
            return ManagerResult(
                success=True,
                data={"type": "directory", "path": dir_path, "created": True},
                metrics={},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _create_context(self, context: ManagerContext, data: dict[str, Any]) -> ManagerResult:
        """Create an agent context."""
        agent_id = data.get("agent_id", "")
        context_data = data.get("context_data", {})

        try:
            self._agent_contexts[agent_id] = {
                **context_data,
                "last_updated": datetime.now().isoformat(),
            }
            self.context_operations_count += 1
            return ManagerResult(
                success=True,
                data={"type": "context", "agent_id": agent_id, "created": True},
                metrics={"context_keys": len(context_data)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _read_file(self, file_path: str) -> str:
        """Read file content."""
        with open(file_path, encoding="utf-8") as f:
            return f.read()

    def _write_file(self, file_path: str, content: str) -> None:
        """Write file content."""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _load_locks(self) -> None:
        """Load locks from file."""
        try:
            if os.path.exists(self._lock_file):
                with open(self._lock_file, encoding="utf-8") as f:
                    lock_data = json.load(f)
                    # Note: We can't restore actual Lock objects, just track them
                    self._locks = {k: threading.Lock() for k in lock_data.get("locks", [])}
        except Exception:
            pass  # Ignore lock loading errors

    def _save_locks(self) -> None:
        """Save locks to file."""
        try:
            lock_data = {"locks": list(self._locks.keys())}
            with open(self._lock_file, "w", encoding="utf-8") as f:
                json.dump(lock_data, f, indent=2)
        except Exception:
            pass  # Ignore lock saving errors
