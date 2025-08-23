#!/usr/bin/env python3
"""
Workspace Structure Module - V2 Workspace Structure Components

This module manages workspace structure creation and management.
Follows Single Responsibility Principle - only workspace structure.
Architecture: Single Responsibility Principle - workspace structure only
LOC: Target 100 lines (under 200 limit)
"""

from pathlib import Path
from typing import List
import logging
from .workspace_config import WorkspaceType

logger = logging.getLogger(__name__)


class WorkspaceStructureManager:
    """Manages workspace structure creation and management"""

    def __init__(self, base_workspace_dir: Path):
        self.base_workspace_dir = base_workspace_dir
        self.logger = logging.getLogger(f"{__name__}.WorkspaceStructureManager")

    def create_workspace_structure(
        self, workspace_path: Path, workspace_type: WorkspaceType
    ) -> bool:
        """Create the modular structure for a workspace"""
        try:
            # Common directories
            common_dirs = ["data", "logs", "temp", "backups"]

            # Type-specific directories
            if workspace_type == WorkspaceType.AGENT:
                type_dirs = ["personal", "shared", "work", "archive"]
            elif workspace_type == WorkspaceType.COORDINATION:
                type_dirs = ["coordination", "shared", "monitoring", "reports"]
            elif workspace_type == WorkspaceType.SHARED:
                type_dirs = ["public", "restricted", "templates", "examples"]
            else:
                type_dirs = ["general"]

            # Create all directories
            for dir_name in common_dirs + type_dirs:
                (workspace_path / dir_name).mkdir(exist_ok=True)

            # Create README file
            readme_content = f"# {workspace_path.name} Workspace\n\nType: {workspace_type.value}\nCreated: {self._get_current_timestamp()}\n"
            with open(workspace_path / "README.md", "w") as f:
                f.write(readme_content)

            self.logger.info(f"Created workspace structure for {workspace_path.name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create workspace structure: {e}")
            return False

    def _get_current_timestamp(self) -> str:
        """Get current timestamp string"""
        from datetime import datetime

        return datetime.now().isoformat()

    def cleanup_workspace_structure(self, workspace_path: Path) -> bool:
        """Clean up workspace structure"""
        try:
            if workspace_path.exists():
                import shutil

                shutil.rmtree(workspace_path)
                self.logger.info(f"Cleaned up workspace structure: {workspace_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to cleanup workspace structure: {e}")
            return False


def run_smoke_test():
    """Run basic functionality test for WorkspaceStructure"""
    print("🧪 Running WorkspaceStructure Smoke Test...")

    try:
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            manager = WorkspaceStructureManager(temp_path)

            # Test structure creation
            test_workspace = temp_path / "test_workspace"
            test_workspace.mkdir()

            success = manager.create_workspace_structure(
                test_workspace, WorkspaceType.AGENT
            )
            assert success

            # Verify directories were created
            assert (test_workspace / "data").exists()
            assert (test_workspace / "personal").exists()
            assert (test_workspace / "README.md").exists()

            # Test cleanup
            success = manager.cleanup_workspace_structure(test_workspace)
            assert success

        print("✅ WorkspaceStructure Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ WorkspaceStructure Smoke Test FAILED: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
