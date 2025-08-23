#!/usr/bin/env python3
"""
Workspace Manager - Agent Cellphone V2
=====================================

Manages individual agent workspaces with strict OOP design.
Follows Single Responsibility Principle with 200 LOC limit.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class WorkspaceConfig:
    """Workspace configuration data."""

    agent_id: str
    workspace_path: str
    inbox_path: str
    tasks_path: str
    responses_path: str
    created_at: str
    last_accessed: str


class WorkspaceManager:
    """
    Workspace Manager - Single responsibility: Agent workspace management.

    This service manages:
    - Individual agent workspace directories
    - Workspace configuration and metadata
    - Workspace health monitoring
    - Workspace cleanup and maintenance
    """

    def __init__(self, base_path: str = "agent_workspaces"):
        """Initialize Workspace Manager with base path."""
        self.base_path = Path(base_path)
        self.logger = self._setup_logging()
        self.workspaces: Dict[str, WorkspaceConfig] = {}
        self.status = "initialized"

        # Ensure base directory exists
        self.base_path.mkdir(exist_ok=True)

        # Initialize existing workspaces
        self._discover_workspaces()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("WorkspaceManager")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _discover_workspaces(self):
        """Discover existing workspaces."""
        try:
            for workspace_dir in self.base_path.iterdir():
                if workspace_dir.is_dir() and workspace_dir.name.startswith("Agent-"):
                    agent_id = workspace_dir.name
                    self._load_workspace_config(agent_id)

            self.logger.info(f"Discovered {len(self.workspaces)} existing workspaces")
        except Exception as e:
            self.logger.error(f"Failed to discover workspaces: {e}")

    def _load_workspace_config(self, agent_id: str):
        """Load workspace configuration."""
        try:
            config_file = self.base_path / agent_id / "workspace.json"
            if config_file.exists():
                with open(config_file, "r") as f:
                    config_data = json.load(f)
                    self.workspaces[agent_id] = WorkspaceConfig(**config_data)
            else:
                # Create default config
                self._create_workspace_config(agent_id)
        except Exception as e:
            self.logger.error(f"Failed to load workspace config for {agent_id}: {e}")

    def _create_workspace_config(self, agent_id: str):
        """Create default workspace configuration."""
        try:
            workspace_path = self.base_path / agent_id
            inbox_path = workspace_path / "inbox"
            tasks_path = workspace_path / "tasks"
            responses_path = workspace_path / "responses"

            # Create directories
            inbox_path.mkdir(exist_ok=True)
            tasks_path.mkdir(exist_ok=True)
            responses_path.mkdir(exist_ok=True)

            # Create config
            config = WorkspaceConfig(
                agent_id=agent_id,
                workspace_path=str(workspace_path),
                inbox_path=str(inbox_path),
                tasks_path=str(tasks_path),
                responses_path=str(responses_path),
                created_at=datetime.now().isoformat(),
                last_accessed=datetime.now().isoformat(),
            )

            # Save config
            config_file = workspace_path / "workspace.json"
            with open(config_file, "w") as f:
                json.dump(config.__dict__, f, indent=2)

            self.workspaces[agent_id] = config
            self.logger.info(f"Created workspace configuration for {agent_id}")

        except Exception as e:
            self.logger.error(f"Failed to create workspace config for {agent_id}: {e}")

    def create_workspace(self, agent_id: str) -> bool:
        """Create a new agent workspace."""
        try:
            if agent_id in self.workspaces:
                self.logger.warning(f"Workspace for {agent_id} already exists")
                return True

            self._create_workspace_config(agent_id)
            self.logger.info(f"Workspace created successfully for {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create workspace for {agent_id}: {e}")
            return False

    def get_workspace_info(self, agent_id: str) -> Optional[WorkspaceConfig]:
        """Get workspace information for an agent."""
        return self.workspaces.get(agent_id)

    def get_all_workspaces(self) -> List[WorkspaceConfig]:
        """Get all workspace configurations."""
        return list(self.workspaces.values())

    def update_workspace_access(self, agent_id: str) -> bool:
        """Update last accessed timestamp for a workspace."""
        try:
            if agent_id in self.workspaces:
                config = self.workspaces[agent_id]
                config.last_accessed = datetime.now().isoformat()

                # Save updated config
                config_file = Path(config.workspace_path) / "workspace.json"
                with open(config_file, "w") as f:
                    json.dump(config.__dict__, f, indent=2)

                self.logger.debug(f"Updated access time for {agent_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update access time for {agent_id}: {e}")
            return False

    def cleanup_workspace(self, agent_id: str) -> bool:
        """Clean up a workspace (remove old files, etc.)."""
        try:
            if agent_id not in self.workspaces:
                return False

            config = self.workspaces[agent_id]

            # Clean old response files
            responses_path = Path(config.responses_path)
            for response_file in responses_path.glob("*.txt"):
                if response_file.stat().st_mtime < (
                    datetime.now().timestamp() - 86400
                ):  # 24 hours
                    response_file.unlink()
                    self.logger.debug(f"Cleaned up old response file: {response_file}")

            # Clean old task files
            tasks_path = Path(config.tasks_path)
            for task_file in tasks_path.glob("*.json"):
                if task_file.stat().st_mtime < (
                    datetime.now().timestamp() - 86400
                ):  # 24 hours
                    task_file.unlink()
                    self.logger.debug(f"Cleaned up old task file: {task_file}")

            self.logger.info(f"Workspace cleanup completed for {agent_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to cleanup workspace for {agent_id}: {e}")
            return False

    def get_workspace_status(self) -> Dict[str, Any]:
        """Get overall workspace system status."""
        try:
            total_workspaces = len(self.workspaces)
            active_workspaces = sum(
                1 for w in self.workspaces.values() if Path(w.workspace_path).exists()
            )

            workspace_details = {}
            for agent_id, config in self.workspaces.items():
                workspace_path = Path(config.workspace_path)
                workspace_details[agent_id] = {
                    "exists": workspace_path.exists(),
                    "inbox_files": len(list(Path(config.inbox_path).glob("*"))),
                    "task_files": len(list(Path(config.tasks_path).glob("*"))),
                    "response_files": len(list(Path(config.responses_path).glob("*"))),
                    "last_accessed": config.last_accessed,
                }

            return {
                "status": self.status,
                "total_workspaces": total_workspaces,
                "active_workspaces": active_workspaces,
                "base_path": str(self.base_path),
                "workspace_details": workspace_details,
            }

        except Exception as e:
            self.logger.error(f"Failed to get workspace status: {e}")
            return {"status": "error", "error": str(e)}

    def get_sprints_path(self) -> Path:
        """Get the sprints directory path for the workspace."""
        sprints_path = self.base_path / "sprints"
        sprints_path.mkdir(parents=True, exist_ok=True)
        return sprints_path

    def shutdown_manager(self) -> bool:
        """Shutdown the workspace manager."""
        try:
            self.logger.info("Shutting down Workspace Manager...")
            self.status = "shutdown"

            # Cleanup all workspaces
            for agent_id in list(self.workspaces.keys()):
                self.cleanup_workspace(agent_id)

            self.logger.info("Workspace Manager shutdown complete")
            return True

        except Exception as e:
            self.logger.error(f"Workspace Manager shutdown failed: {e}")
            return False


def main():
    """CLI interface for Workspace Manager testing."""
    import argparse

    parser = argparse.ArgumentParser(description="Workspace Manager Testing Interface")
    parser.add_argument(
        "--init", action="store_true", help="Initialize workspace manager"
    )
    parser.add_argument(
        "--create", metavar="AGENT_ID", help="Create workspace for agent"
    )
    parser.add_argument("--status", action="store_true", help="Show workspace status")
    parser.add_argument(
        "--cleanup", metavar="AGENT_ID", help="Cleanup workspace for agent"
    )
    parser.add_argument(
        "--test", action="store_true", help="Run workspace manager tests"
    )

    args = parser.parse_args()

    # Create manager instance
    manager = WorkspaceManager()

    if args.init or not any(
        [args.init, args.create, args.status, args.cleanup, args.test]
    ):
        print("🏢 Workspace Manager - Agent Cellphone V2")
        print("Manager initialized successfully")

    if args.create:
        success = manager.create_workspace(args.create)
        print(f"Workspace creation: {'✅ Success' if success else '❌ Failed'}")

    if args.status:
        print("📊 Workspace Status:")
        status = manager.get_workspace_status()
        for key, value in status.items():
            if key != "workspace_details":
                print(f"  {key}: {value}")

        if "workspace_details" in status:
            print("\nWorkspace Details:")
            for agent_id, details in status["workspace_details"].items():
                print(f"  {agent_id}: {details}")

    if args.cleanup:
        success = manager.cleanup_workspace(args.cleanup)
        print(f"Workspace cleanup: {'✅ Success' if success else '❌ Failed'}")

    if args.test:
        print("🧪 Running workspace manager tests...")
        try:
            # Test workspace creation
            test_agent = "TestAgent"
            success = manager.create_workspace(test_agent)
            print(f"Workspace creation test: {'✅ Success' if success else '❌ Failed'}")

            # Test status retrieval
            status = manager.get_workspace_status()
            print(
                f"Status retrieval test: {'✅ Success' if 'total_workspaces' in status else '❌ Failed'}"
            )

            # Test cleanup
            success = manager.cleanup_workspace(test_agent)
            print(f"Cleanup test: {'✅ Success' if success else '❌ Failed'}")

        except Exception as e:
            print(f"❌ Workspace manager test failed: {e}")


if __name__ == "__main__":
    main()
