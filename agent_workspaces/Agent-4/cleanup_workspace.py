#!/usr/bin/env python3
"""
Agent-4 Workspace Cleanup Script
================================

Automatically organizes and cleans up Agent-4's workspace inbox.
Moves files to appropriate archive folders based on content and naming patterns.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

class WorkspaceCleanup:
    """Clean up and organize Agent-4's workspace."""

    def __init__(self, workspace_path):
        self.workspace_path = Path(workspace_path)
        self.inbox_path = self.workspace_path / "inbox"
        self.archive_path = self.workspace_path / "archive"

        # Create archive subdirectories if they don't exist
        self.archive_dirs = {
            'acknowledgments': self.archive_path / 'acknowledgments',
            'progress_reports': self.archive_path / 'progress_reports',
            'consolidation': self.archive_path / 'consolidation',
            'agent_communications': self.archive_path / 'agent_communications',
            'duplicate_reports': self.archive_path / 'duplicate_reports',
            'mission_reports': self.archive_path / 'mission_reports',
            'system_reports': self.archive_path / 'system_reports',
            'processed': self.archive_path / 'processed'
        }

        for dir_path in self.archive_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

    def categorize_file(self, filename):
        """Categorize a file based on its name and content."""
        name_lower = filename.lower()

        # Agent communications
        if 'co_captain_message' in name_lower:
            return 'agent_communications'
        if 'agent_' in name_lower and ('ack' in name_lower or 'acknowledgment' in name_lower):
            return 'agent_communications'

        # Duplicate reports
        if 'duplicate' in name_lower and 'agent_8' in name_lower:
            return 'duplicate_reports'

        # Progress reports
        if 'progress_report' in name_lower or 'hourly' in name_lower:
            return 'progress_reports'

        # Acknowledgments
        if any(keyword in name_lower for keyword in ['acknowledgment', 'ack', 'confirmed', 'responded']):
            return 'acknowledgments'

        # Consolidation
        if any(keyword in name_lower for keyword in ['consolidation', 'assignment', 'mission']):
            return 'consolidation'

        # System reports
        if any(keyword in name_lower for keyword in ['system', 'activation', 'pytest', 'emergency']):
            return 'system_reports'

        # Default to processed
        return 'processed'

    def move_file(self, file_path, category):
        """Move a file to the appropriate archive category."""
        if category in self.archive_dirs:
            dest_dir = self.archive_dirs[category]
            try:
                shutil.move(str(file_path), str(dest_dir / file_path.name))
                print(f"📁 Moved {file_path.name} → {category}/")
                return True
            except Exception as e:
                print(f"❌ Failed to move {file_path.name}: {e}")
                return False
        return False

    def cleanup_inbox(self):
        """Clean up the inbox by organizing files into categories."""
        if not self.inbox_path.exists():
            print("❌ Inbox directory not found!")
            return

        print("🧹 Starting Agent-4 workspace cleanup...")
        print(f"📂 Processing inbox: {self.inbox_path}")

        moved_count = 0
        processed_count = 0

        # Process each file in inbox
        for file_path in self.inbox_path.iterdir():
            if file_path.is_file():
                processed_count += 1
                category = self.categorize_file(file_path.name)

                if self.move_file(file_path, category):
                    moved_count += 1

        print("\n✅ Cleanup Summary:")
        print(f"   📊 Files processed: {processed_count}")
        print(f"   📁 Files moved: {moved_count}")
        print(f"   📂 Files remaining: {processed_count - moved_count}")

        # Show archive organization
        print("\n📂 Archive Organization:")
        for category, dir_path in self.archive_dirs.items():
            if dir_path.exists():
                file_count = len(list(dir_path.glob('*')))
                if file_count > 0:
                    print(f"   {category}: {file_count} files")

    def show_workspace_status(self):
        """Show the current workspace status."""
        print("\n📊 Current Workspace Status:")
        print(f"📂 Workspace: {self.workspace_path.name}")

        # Count files in inbox
        inbox_files = list(self.inbox_path.glob('*')) if self.inbox_path.exists() else []
        print(f"📬 Inbox: {len(inbox_files)} files")

        # Count files in each archive category
        for category, dir_path in self.archive_dirs.items():
            if dir_path.exists():
                file_count = len(list(dir_path.glob('*')))
                if file_count > 0:
                    print(f"📁 {category}: {file_count} files")

def main():
    """Main cleanup function."""
    workspace_path = Path(__file__).parent

    cleanup = WorkspaceCleanup(workspace_path)
    cleanup.show_workspace_status()
    cleanup.cleanup_inbox()
    cleanup.show_workspace_status()

    print("\n🎉 Agent-4 workspace cleanup complete!")
    print("💡 Workspace is now organized and ready for new messages!")

if __name__ == "__main__":
    main()
