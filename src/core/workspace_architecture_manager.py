#!/usr/bin/env python3
"""
Workspace Architecture Manager - V2 Workspace Architecture Components

This module manages the modular architecture for agent workspaces.
Follows Single Responsibility Principle - only workspace architecture management.
Architecture: Single Responsibility Principle - workspace architecture only
LOC: Target 350 lines (under 350 limit)
"""

import os
import json
import shutil
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

from .workspace_config import (
    WorkspaceType,
    WorkspaceStatus,
    WorkspaceConfig,
    WorkspaceInfo,
    WorkspaceConfigManager,
)
from .workspace_structure import WorkspaceStructureManager

logger = logging.getLogger(__name__)


class WorkspaceArchitectureManager:
    """
    Manages modular architecture for agent workspaces

    Responsibilities:
    - Workspace creation and configuration
    - Architecture enforcement
    - Workspace isolation and security
    - Resource management
    """

    def __init__(self, base_workspace_dir: str = "agent_workspaces"):
        self.base_workspace_dir = Path(base_workspace_dir)
        self.workspaces: Dict[str, WorkspaceInfo] = {}
        self.configs: Dict[str, WorkspaceConfig] = {}
        self.logger = logging.getLogger(f"{__name__}.WorkspaceArchitectureManager")

        # Initialize component managers
        self.config_manager = WorkspaceConfigManager(self.base_workspace_dir)
        self.structure_manager = WorkspaceStructureManager(self.base_workspace_dir)

        # Ensure base directory exists
        self.base_workspace_dir.mkdir(exist_ok=True)

        # Load existing workspaces
        self._discover_existing_workspaces()

    def _discover_existing_workspaces(self):
        """Discover existing workspaces in the base directory"""
        try:
            for workspace_dir in self.base_workspace_dir.iterdir():
                if workspace_dir.is_dir():
                    workspace_name = workspace_dir.name
                    if workspace_name.startswith("Agent-"):
                        self._load_workspace_info(workspace_name, workspace_dir)
        except Exception as e:
            self.logger.error(f"Failed to discover existing workspaces: {e}")

    def _load_workspace_info(self, name: str, path: Path):
        """Load information about an existing workspace"""
        try:
            # Calculate workspace size
            size_mb = sum(f.stat().st_size for f in path.rglob("*") if f.is_file()) / (
                1024 * 1024
            )

            # Create workspace info
            workspace_info = WorkspaceInfo(
                name=name,
                workspace_type=WorkspaceType.AGENT,
                status=WorkspaceStatus.ACTIVE,
                path=str(path),
                size_mb=round(size_mb, 2),
                created_at="unknown",
                last_accessed="unknown",
                agent_count=1,
                resource_usage={
                    "files": len(list(path.rglob("*"))),
                    "size_mb": size_mb,
                },
            )

            self.workspaces[name] = workspace_info
            self.logger.info(f"Loaded existing workspace: {name}")

        except Exception as e:
            self.logger.error(f"Failed to load workspace info for {name}: {e}")

    def create_workspace(
        self,
        name: str,
        workspace_type: WorkspaceType,
        permissions: List[str] = None,
        isolation_level: str = "standard",
    ) -> bool:
        """Create a new agent workspace with modular architecture"""
        try:
            if name in self.workspaces:
                self.logger.warning(f"Workspace {name} already exists")
                return False

            # Create workspace directory
            workspace_path = self.base_workspace_dir / name
            workspace_path.mkdir(exist_ok=True)

            # Create modular structure using component manager
            success = self.structure_manager.create_workspace_structure(
                workspace_path, workspace_type
            )
            if not success:
                return False

            # Create workspace config
            config = WorkspaceConfig(
                name=name,
                workspace_type=workspace_type,
                base_path=str(workspace_path),
                permissions=permissions or ["read", "write"],
                isolation_level=isolation_level,
                max_size_mb=100,
                auto_cleanup=True,
                backup_enabled=True,
            )

            # Create workspace info
            workspace_info = WorkspaceInfo(
                name=name,
                workspace_type=workspace_type,
                status=WorkspaceStatus.ACTIVE,
                path=str(workspace_path),
                size_mb=0.0,
                created_at=self.config_manager.get_current_timestamp(),
                last_accessed=self.config_manager.get_current_timestamp(),
                agent_count=0,
                resource_usage={"files": 0, "size_mb": 0.0},
            )

            # Save configurations using component manager
            self.configs[name] = config
            self.workspaces[name] = workspace_info

            # Save config to file using component manager
            self.config_manager.save_workspace_config(name, config)

            self.logger.info(
                f"Created workspace: {name} with type {workspace_type.value}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to create workspace {name}: {e}")
            return False

    def get_workspace_info(self, name: str) -> Optional[WorkspaceInfo]:
        """Get information about a specific workspace"""
        return self.workspaces.get(name)

    def list_workspaces(self) -> List[WorkspaceInfo]:
        """List all workspaces"""
        return list(self.workspaces.values())

    def update_workspace_status(self, name: str, status: WorkspaceStatus) -> bool:
        """Update the status of a workspace"""
        try:
            if name in self.workspaces:
                self.workspaces[name].status = status
                self.workspaces[
                    name
                ].last_accessed = self.config_manager.get_current_timestamp()
                self.logger.info(f"Updated workspace {name} status to {status.value}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to update workspace status: {e}")
            return False

    def get_architecture_summary(self) -> Dict[str, Any]:
        """Get summary of workspace architecture"""
        try:
            total_workspaces = len(self.workspaces)
            active_workspaces = len(
                [
                    w
                    for w in self.workspaces.values()
                    if w.status == WorkspaceStatus.ACTIVE
                ]
            )
            total_size_mb = sum(w.size_mb for w in self.workspaces.values())

            return {
                "total_workspaces": total_workspaces,
                "active_workspaces": active_workspaces,
                "total_size_mb": round(total_size_mb, 2),
                "workspace_types": {
                    wt.value: len(
                        [w for w in self.workspaces.values() if w.workspace_type == wt]
                    )
                    for wt in WorkspaceType
                },
                "isolation_levels": list(
                    set(c.isolation_level for c in self.configs.values())
                ),
            }
        except Exception as e:
            self.logger.error(f"Failed to get architecture summary: {e}")
            return {"error": str(e)}

    def run_smoke_test(self) -> bool:
        """Run basic functionality test for this instance"""
        try:
            # Test workspace creation
            test_name = "smoke_test_workspace"
            success = self.create_workspace(test_name, WorkspaceType.TEMPORARY)
            if not success:
                return False

            # Test workspace info retrieval
            info = self.get_workspace_info(test_name)
            if not info or info.name != test_name:
                return False

            # Test status update
            success = self.update_workspace_status(
                test_name, WorkspaceStatus.MAINTENANCE
            )
            if not success:
                return False

            # Test listing workspaces
            workspaces = self.list_workspaces()
            if len(workspaces) == 0:
                return False

            # Test architecture summary
            summary = self.get_architecture_summary()
            if "total_workspaces" not in summary:
                return False

            # Cleanup test workspace using component manager
            test_path = self.base_workspace_dir / test_name
            if test_path.exists():
                self.structure_manager.cleanup_workspace_structure(test_path)
                # Remove from internal tracking
                if test_name in self.workspaces:
                    del self.workspaces[test_name]
                if test_name in self.configs:
                    del self.configs[test_name]

            return True

        except Exception as e:
            self.logger.error(f"Smoke test failed: {e}")
            return False


def run_smoke_test():
    """Run basic functionality test for WorkspaceArchitectureManager"""
    print("🧪 Running WorkspaceArchitectureManager Smoke Test...")

    try:
        # Test with temporary directory
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            manager = WorkspaceArchitectureManager(temp_dir)

            # Test workspace creation
            success = manager.create_workspace("test_agent", WorkspaceType.AGENT)
            assert success

            # Test workspace info retrieval
            info = manager.get_workspace_info("test_agent")
            assert info is not None
            assert info.name == "test_agent"

            # Test status update
            success = manager.update_workspace_status(
                "test_agent", WorkspaceStatus.MAINTENANCE
            )
            assert success

            # Test listing workspaces
            workspaces = manager.list_workspaces()
            assert len(workspaces) == 1

            # Test architecture summary
            summary = manager.get_architecture_summary()
            assert "total_workspaces" in summary

        print("✅ WorkspaceArchitectureManager Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ WorkspaceArchitectureManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for WorkspaceArchitectureManager testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Workspace Architecture Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--create", nargs=2, metavar=("NAME", "TYPE"), help="Create workspace"
    )
    parser.add_argument("--list", action="store_true", help="List all workspaces")
    parser.add_argument("--info", help="Get workspace info")
    parser.add_argument(
        "--status", nargs=2, metavar=("NAME", "STATUS"), help="Update workspace status"
    )
    parser.add_argument(
        "--summary", action="store_true", help="Show architecture summary"
    )

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    manager = WorkspaceArchitectureManager()

    if args.create:
        name, workspace_type = args.create
        try:
            ws_type = WorkspaceType(workspace_type)
            success = manager.create_workspace(name, ws_type)
            print(f"Workspace creation: {'✅ Success' if success else '❌ Failed'}")
        except ValueError:
            print(f"❌ Invalid workspace type: {workspace_type}")
            print(f"Valid types: {[t.value for t in WorkspaceType]}")
    elif args.list:
        workspaces = manager.list_workspaces()
        print("Workspaces:")
        for ws in workspaces:
            print(f"  {ws.name}: {ws.status.value} ({ws.size_mb} MB)")
    elif args.info:
        info = manager.get_workspace_info(args.info)
        if info:
            print(f"Workspace: {info.name}")
            print(f"  Type: {info.workspace_type.value}")
            print(f"  Status: {info.status.value}")
            print(f"  Size: {info.size_mb} MB")
        else:
            print(f"Workspace '{args.info}' not found")
    elif args.status:
        name, status = args.status
        try:
            ws_status = WorkspaceStatus(status)
            success = manager.update_workspace_status(name, ws_status)
            print(f"Status update: {'✅ Success' if success else '❌ Failed'}")
        except ValueError:
            print(f"❌ Invalid status: {status}")
            print(f"Valid statuses: {[s.value for s in WorkspaceStatus]}")
    elif args.summary:
        summary = manager.get_architecture_summary()
        print("Architecture Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
