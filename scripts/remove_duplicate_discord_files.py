#!/usr/bin/env python3
"""
Remove Duplicate Discord Bot Files - V2 Compliant
===============================================

Safely removes duplicate Discord bot files after consolidation.
Creates backup and validates before deletion.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Any

# V2 Compliance: File under 400 lines, functions under 30 lines


class DuplicateFileRemover:
    """Safely remove duplicate Discord bot files."""

    def __init__(self):
        """Initialize duplicate file remover."""
        self.logger = logging.getLogger(__name__)
        self.project_root = Path(__file__).parent.parent
        self.backup_dir = self.project_root / "backups" / "discord_duplicates"

    def get_files_to_remove(self) -> dict[str, list[str]]:
        """Get files that should be removed after consolidation."""
        return {
            "old_discord_commander": [
                "src/discord/discord_commander.py",
                "src/discord/enhanced_discord.py",
            ],
            "old_discord_bot_system": [
                "src/services/discord_bot/commands/agent_commands.py",
                "src/services/discord_bot/commands/basic_commands.py",
                "src/services/discord_bot/commands/devlog_commands.py",
                "src/services/discord_bot/commands/messaging_advanced_commands.py",
                "src/services/discord_bot/commands/messaging_commands.py",
                "src/services/discord_bot/commands/onboarding_commands.py",
                "src/services/discord_bot/commands/project_update_core_commands.py",
                "src/services/discord_bot/commands/project_update_management_commands.py",
                "src/services/discord_bot/commands/project_update_specialized_commands.py",
                "src/services/discord_bot/commands/stall_commands.py",
                "src/services/discord_bot/commands/system_commands.py",
                "src/services/discord_bot/core/agent_communication_engine.py",
                "src/services/discord_bot/core/command_router.py",
                "src/services/discord_bot/core/discord_bot.py",
                "src/services/discord_bot/core/security_manager.py",
                "src/services/discord_bot/core/ui_embeds_v2.py",
                "src/services/discord_bot/core/ui_embeds.py",
                "src/services/discord_bot/ui/embed_builder.py",
                "src/services/discord_bot/ui/embed_types.py",
                "src/services/discord_bot/ui/interaction_handlers.py",
            ],
        }

    def create_backup(self) -> bool:
        """Create backup of files before removal."""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)

            files_to_backup = []
            file_map = self.get_files_to_remove()

            for category, files in file_map.items():
                for file_path in files:
                    full_path = self.project_root / file_path
                    if full_path.exists():
                        files_to_backup.append(full_path)

            if not files_to_backup:
                self.logger.info("✅ No files to backup")
                return True

            backup_count = 0
            for file_path in files_to_backup:
                backup_path = self.backup_dir / file_path.name
                shutil.copy2(file_path, backup_path)
                backup_count += 1

            self.logger.info(f"✅ Created backup of {backup_count} files in {self.backup_dir}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to create backup: {e}")
            return False

    def validate_removal_safety(self) -> list[str]:
        """Validate that removal is safe."""
        issues = []

        # Check if unified bot exists and works
        unified_bot_path = self.project_root / "src/services/discord_bot_unified.py"
        if not unified_bot_path.exists():
            issues.append("Unified Discord bot does not exist")

        # Check if command registry exists
        command_registry_path = self.project_root / "src/services/discord_commands.py"
        if not command_registry_path.exists():
            issues.append("Discord command registry does not exist")

        # Check if UI components exist
        ui_components_path = self.project_root / "src/services/discord_ui.py"
        if not ui_components_path.exists():
            issues.append("Discord UI components do not exist")

        return issues

    def remove_files(self) -> dict[str, Any]:
        """Remove duplicate files."""
        results = {"removed": [], "failed": [], "skipped": [], "total": 0}

        # Validate safety first
        issues = self.validate_removal_safety()
        if issues:
            self.logger.error(f"❌ Cannot remove files - safety issues: {issues}")
            return results

        # Create backup first
        if not self.create_backup():
            self.logger.error("❌ Cannot remove files - backup failed")
            return results

        file_map = self.get_files_to_remove()
        results["total"] = sum(len(files) for files in file_map.values())

        for category, files in file_map.items():
            self.logger.info(f"🗑️ Removing files in category: {category}")

            for file_path in files:
                full_path = self.project_root / file_path

                if not full_path.exists():
                    self.logger.warning(f"⚠️ File not found: {file_path}")
                    results["skipped"].append(file_path)
                    continue

                try:
                    # Double-check it's not our new unified files
                    if any(
                        new_file in file_path
                        for new_file in [
                            "discord_bot_unified.py",
                            "discord_commands.py",
                            "discord_config.py",
                            "discord_ui.py",
                        ]
                    ):
                        self.logger.warning(f"⚠️ Skipping new unified file: {file_path}")
                        results["skipped"].append(file_path)
                        continue

                    os.remove(full_path)
                    self.logger.info(f"✅ Removed: {file_path}")
                    results["removed"].append(file_path)

                except Exception as e:
                    self.logger.error(f"❌ Failed to remove {file_path}: {e}")
                    results["failed"].append(file_path)

        return results

    def clean_empty_directories(self) -> int:
        """Clean up empty directories after file removal."""
        cleaned_count = 0

        # Directories to check for emptiness
        dirs_to_check = [
            "src/discord",
            "src/services/discord_bot/commands",
            "src/services/discord_bot/core",
            "src/services/discord_bot/ui",
            "src/services/discord_bot",
        ]

        for dir_path_str in dirs_to_check:
            dir_path = self.project_root / dir_path_str

            if dir_path.exists() and dir_path.is_dir():
                try:
                    # Check if directory is empty
                    contents = list(dir_path.glob("*"))
                    if not contents:
                        dir_path.rmdir()
                        self.logger.info(f"✅ Removed empty directory: {dir_path_str}")
                        cleaned_count += 1

                except Exception as e:
                    self.logger.error(f"❌ Failed to remove directory {dir_path_str}: {e}")

        return cleaned_count

    def run_cleanup(self) -> dict[str, Any]:
        """Run the complete cleanup process."""
        self.logger.info("🚀 Starting Discord bot duplicate file cleanup...")

        results = {
            "backup_created": False,
            "files_removed": 0,
            "directories_cleaned": 0,
            "errors": [],
        }

        # Create backup
        if not self.create_backup():
            results["errors"].append("Backup creation failed")
            return results

        results["backup_created"] = True

        # Remove files
        removal_results = self.remove_files()
        results["files_removed"] = len(removal_results["removed"])
        results["errors"].extend([f"Failed to remove {f}" for f in removal_results["failed"]])

        # Clean empty directories
        results["directories_cleaned"] = self.clean_empty_directories()

        self.logger.info("✅ Discord bot cleanup completed!")
        self.logger.info(f"   Files removed: {results['files_removed']}")
        self.logger.info(f"   Directories cleaned: {results['directories_cleaned']}")
        self.logger.info(f"   Backup location: {self.backup_dir}")

        return results


def main():
    """Main function to run cleanup."""
    print("🧹 Discord Bot Duplicate File Cleanup")
    print("=" * 50)

    remover = DuplicateFileRemover()
    results = remover.run_cleanup()

    if results["errors"]:
        print(f"❌ Cleanup completed with {len(results['errors'])} errors:")
        for error in results["errors"]:
            print(f"   - {error}")
        return 1

    print("✅ Cleanup completed successfully!")
    print(f"   Files removed: {results['files_removed']}")
    print(f"   Directories cleaned: {results['directories_cleaned']}")
    print(f"   Backup created: {'✅ Yes' if results['backup_created'] else '❌ No'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
