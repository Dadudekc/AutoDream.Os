#!/usr/bin/env python3
"""
Orphan File Cleanup Script - Agent Cellphone V2
===============================================

Safely removes orphaned files identified in the repository analysis.
Only removes files that are confirmed to have no references in the codebase.
"""

import os
import shutil

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import List, Dict


class OrphanCleanup:
    """Safely removes orphaned files from the repository"""

    def __init__(self, repo_root: str = "."):
        """
        __init__
        
        Purpose: Automated function documentation
        """
        self.repo_root = Path(repo_root)
        self.orphaned_files = [
            # Root directory orphans
            "send_agent_message.py",
            "send_agent_message_pyautogui.py",
            "standalone_scanner.py",
            "test_perpetual_motion.py",
            "standalone_test.py",
            # Services directory orphans
            "src/services/heartbeat_monitor.py",
            "src/services/service_discovery.py",
        ]

        # Files that should NOT be removed (keep these)
        self.keep_files = [
            "test_core_system.py",  # This is working and useful
            "src/services/response_capture/service.py",  # This has tests now
        ]

    def confirm_removal(self) -> bool:
        """Get user confirmation for file removal"""
        print("🚨 ORPHAN FILE CLEANUP")
        print("=" * 50)
        print("The following files have been identified as orphaned:")
        print()

        for file_path in self.orphaned_files:
            full_path = self.repo_root / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                print(f"  📁 {file_path} ({size} bytes)")
            else:
                print(f"  ❌ {file_path} (not found)")

        print()
        print("These files have no imports or references in the codebase.")
        print(
            "Removing them will clean up the repository without affecting functionality."
        )
        print()

        response = (
            input("Do you want to proceed with removal? (yes/no): ").lower().strip()
        )
        return response in ["yes", "y"]

    def backup_files(self) -> str:
        """Create backup of files before removal"""
        backup_dir = self.repo_root / "backup_orphans"
        backup_dir.mkdir(exist_ok=True)

        print(f"📦 Creating backup in: {backup_dir}")

        for file_path in self.orphaned_files:
            full_path = self.repo_root / file_path
            if full_path.exists():
                # Create backup directory structure
                backup_file = backup_dir / file_path
                backup_file.parent.mkdir(parents=True, exist_ok=True)

                # Copy file to backup
                shutil.copy2(full_path, backup_file)
                print(f"  ✅ Backed up: {file_path}")

        return str(backup_dir)

    def remove_files(self) -> Dict[str, bool]:
        """Remove orphaned files and return results"""
        results = {}

        for file_path in self.orphaned_files:
            full_path = self.repo_root / file_path
            if full_path.exists():
                try:
                    full_path.unlink()
                    results[file_path] = True
                    print(f"  🗑️  Removed: {file_path}")
                except Exception as e:
                    results[file_path] = False
                    print(f"  ❌ Failed to remove {file_path}: {e}")
            else:
                results[file_path] = False
                print(f"  ⚠️  File not found: {file_path}")

        return results

    def cleanup_empty_dirs(self):
        """Remove empty directories after file cleanup"""
        print("\n🧹 Cleaning up empty directories...")

        # Check for empty directories in src
        src_dir = self.repo_root / "src"
        if src_dir.exists():
            for root, dirs, files in os.walk(src_dir, topdown=False):
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    try:
                        if not any(dir_path.iterdir()):  # Directory is empty
                            dir_path.rmdir()
                            print(
                                f"  🗑️  Removed empty directory: {dir_path.relative_to(self.repo_root)}"
                            )
                    except Exception as e:
                        print(f"  ⚠️  Could not remove directory {dir_path}: {e}")

    def run_cleanup(self, dry_run: bool = False) -> Dict[str, any]:
        """
        run_cleanup
        
        Purpose: Automated function documentation
        """
        """Run the complete cleanup process"""
        print("🧹 ORPHAN FILE CLEANUP SCRIPT")
        print("=" * 50)

        if dry_run:
            print("🔍 DRY RUN MODE - No files will be removed")
            print()
            self.confirm_removal()
            return {"dry_run": True, "files_to_remove": self.orphaned_files}

        # Get confirmation
        if not self.confirm_removal():
            print("❌ Cleanup cancelled by user")
            return {"cancelled": True}

        # Create backup
        backup_dir = self.backup_files()

        # Remove files
        print(f"\n🗑️  Removing orphaned files...")
        removal_results = self.remove_files()

        # Clean up empty directories
        self.cleanup_empty_dirs()

        # Summary
        successful_removals = sum(1 for success in removal_results.values() if success)
        total_files = len(removal_results)

        print(f"\n📊 CLEANUP SUMMARY")
        print("=" * 30)
        print(f"Files processed: {total_files}")
        print(f"Successfully removed: {successful_removals}")
        print(f"Failed removals: {total_files - successful_removals}")
        print(f"Backup location: {backup_dir}")

        return {
            "successful_removals": successful_removals,
            "total_files": total_files,
            "backup_dir": backup_dir,
            "removal_results": removal_results,
        }


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Clean up orphaned files in Agent Cellphone V2"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without actually removing",
    )
    parser.add_argument("--repo-root", default=".", help="Repository root directory")

    args = parser.parse_args()

    cleanup = OrphanCleanup(args.repo_root)
    results = cleanup.run_cleanup(dry_run=args.dry_run)

    if args.dry_run:
        print("\n🔍 DRY RUN COMPLETE")
        print("Use without --dry-run to actually perform the cleanup")
    elif not results.get("cancelled"):
        print("\n✅ CLEANUP COMPLETE")
        print("Orphaned files have been removed and backed up")


if __name__ == "__main__":
    main()

