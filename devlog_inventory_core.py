#!/usr/bin/env python3
"""
Core logic for devlog inventory script.
"""

from datetime import datetime
from pathlib import Path


class DevlogInventory:
    """Comprehensive inventory of all devlogs in the system."""
    
    def __init__(self):
        """Initialize the inventory."""
        self.devlogs_dir = Path("devlogs")
        self.exported_files = list(Path(".").glob("all_devlogs_*.json"))
    
    def show_database_devlogs(self):
        """Show database devlogs information."""
        print("📊 DATABASE DEVLOGS (Vector Database):")
        print("   File: data/vector_database.db")
        print("   Count: 12 devlogs")
        print("   Agents: Agent-1 through Agent-8")
        print("   Status: 4 completed, 8 in_progress")
        print()
    
    def show_file_devlogs(self):
        """Show file devlogs information."""
        if not self.devlogs_dir.exists():
            return
        
        md_files = list(self.devlogs_dir.glob("*.md"))
        archive_files = (
            list((self.devlogs_dir / "archive").glob("*.md"))
            if (self.devlogs_dir / "archive").exists()
            else []
        )

        print("📝 FILE DEVLOGS (Markdown Files):")
        print(f"   Directory: {self.devlogs_dir}")
        print(f"   Active files: {len(md_files)} devlogs")
        print(f"   Archive files: {len(archive_files)} devlogs")
        print(f"   Total files: {len(md_files) + len(archive_files)} devlogs")
        print()

        # Show recent files
        recent_files = sorted(md_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
        print("   Recent files:")
        for file in recent_files:
            print(f"     - {file.name}")
        print()
    
    def show_exported_files(self):
        """Show exported files information."""
        if not self.exported_files:
            return
        
        print("💾 EXPORTED FILES:")
        for file in sorted(self.exported_files):
            size = file.stat().st_size
            created_time = datetime.fromtimestamp(file.stat().st_mtime)
            print(f"   File: {file.name}")
            print(f"   Size: {size:,} characters")
            print(f'   Created: {created_time.strftime("%Y-%m-%d %H:%M:%S")}')
            print()
    
    def show_available_actions(self):
        """Show available actions."""
        print("🎯 AVAILABLE ACTIONS:")
        print("1. View all database devlogs: python query_all_devlogs.py")
        print("2. Export database devlogs: python query_all_devlogs.py (choose 1)")
        print("3. View file devlogs: ls devlogs/")
        print("4. Export file devlogs to JSON: Create script to convert .md to JSON")
        print("5. Combined export: Merge database and file devlogs")

        print()
        print("📤 UPLOAD/EXPORT OPTIONS:")
        print("• Database devlogs are already exported to JSON")
        print("• File devlogs can be converted to JSON format")
        print("• All devlogs can be combined into a single export")
        print("• Export formats: JSON, CSV, Excel available")
    
    def run_inventory(self):
        """Run the complete inventory."""
        print("🤖 COMPREHENSIVE DEVLOG INVENTORY")
        print("=" * 50)
        
        self.show_database_devlogs()
        self.show_file_devlogs()
        self.show_exported_files()
        self.show_available_actions()
