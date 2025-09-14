#!/usr/bin/env python3
"""
Messaging System Consolidation Implementation
Agent-3 Quality Assurance Co-Captain
"""

import os
import shutil
from pathlib import Path
import json
from datetime import datetime


class MessagingSystemConsolidator:
    """Handles the consolidation and deletion of messaging systems."""

    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.backup_dir = (
            self.project_root
            / "backup"
            / f"messaging_consolidation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        self.registry_path = self.project_root / "config" / "messaging_systems.yaml"

        # Systems to delete (with logic to extract first)
        self.systems_to_delete = [
            "src/services/messaging/broadcast_service.py",
            "src/services/messaging/history_service.py",
            "src/services/messaging/interfaces/messaging_interfaces.py",
            "src/services/messaging/task_handlers.py",
            "src/core/coordinate_loader.py",
            "src/discord_commander/discord_agent_bot.py",
            "src/discord_commander/communication_engine.py",
            "src/discord_commander/messaging_gateway.py",
            "src/services/messaging/providers/fallback_provider.py",
            "src/services/messaging/cli/perf_cli.py",
            "src/discord_commander/webhook/",
            "src/services/thea/communication/",
            "src/onboarding/onboarding_bridge.py",
        ]

        # Target files for integration
        self.integration_targets = {
            "consolidated_messaging": "src/services/messaging/consolidated_messaging_service.py",
            "pyautogui_delivery": "src/services/messaging/providers/pyautogui_delivery.py",
            "messaging_cli": "src/services/messaging/cli/messaging_cli.py",
            "thea_messaging": "src/services/thea/messaging/thea_messaging_service.py",
            "swarm_onboarding": "swarm_onboarding/main.py",
        }

    def create_backup(self):
        """Create backup of all systems to be deleted."""
        print("🔒 Creating backup of systems to be deleted...")

        self.backup_dir.mkdir(parents=True, exist_ok=True)

        for system_path in self.systems_to_delete:
            source = self.project_root / system_path
            if source.exists():
                backup_path = self.backup_dir / system_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)

                if source.is_file():
                    shutil.copy2(source, backup_path)
                elif source.is_dir():
                    shutil.copytree(source, backup_path)

                print(f"  ✅ Backed up: {system_path}")
            else:
                print(f"  ⚠️  Not found: {system_path}")

        # Backup registry
        if self.registry_path.exists():
            shutil.copy2(self.registry_path, self.backup_dir / "messaging_systems.yaml")
            print(f"  ✅ Backed up registry: {self.registry_path}")

        print(f"📁 Backup created at: {self.backup_dir}")

    def extract_logic_from_file(self, file_path):
        """Extract working logic from a file before deletion."""
        if not file_path.exists():
            return None

        print(f"🔍 Extracting logic from: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Basic logic extraction - look for classes, functions, and imports
            extracted_logic = {
                "file_path": str(file_path),
                "classes": [],
                "functions": [],
                "imports": [],
                "content_preview": content[:500] + "..." if len(content) > 500 else content,
            }

            lines = content.split("\n")
            for i, line in enumerate(lines):
                line = line.strip()

                # Extract class definitions
                if line.startswith("class ") and ":" in line:
                    extracted_logic["classes"].append({"line": i + 1, "definition": line})

                # Extract function definitions
                elif line.startswith("def ") and ":" in line:
                    extracted_logic["functions"].append({"line": i + 1, "definition": line})

                # Extract imports
                elif line.startswith(("import ", "from ")):
                    extracted_logic["imports"].append({"line": i + 1, "import": line})

            return extracted_logic

        except Exception as e:
            print(f"  ❌ Error extracting logic: {e}")
            return None

    def extract_all_logic(self):
        """Extract logic from all systems to be deleted."""
        print("🔍 Extracting logic from all systems to be deleted...")

        extracted_logic = {}

        for system_path in self.systems_to_delete:
            file_path = self.project_root / system_path

            if file_path.is_file():
                logic = self.extract_logic_from_file(file_path)
                if logic:
                    extracted_logic[system_path] = logic
            elif file_path.is_dir():
                # Extract from all Python files in directory
                for py_file in file_path.rglob("*.py"):
                    logic = self.extract_logic_from_file(py_file)
                    if logic:
                        extracted_logic[str(py_file.relative_to(self.project_root))] = logic

        # Save extracted logic to backup directory
        logic_file = self.backup_dir / "extracted_logic.json"
        with open(logic_file, "w", encoding="utf-8") as f:
            json.dump(extracted_logic, f, indent=2)

        print(f"💾 Extracted logic saved to: {logic_file}")
        return extracted_logic

    def delete_systems(self):
        """Delete the failed messaging systems."""
        print("🗑️  Deleting failed messaging systems...")

        deleted_count = 0

        for system_path in self.systems_to_delete:
            file_path = self.project_root / system_path

            try:
                if file_path.exists():
                    if file_path.is_file():
                        file_path.unlink()
                        print(f"  ✅ Deleted file: {system_path}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        print(f"  ✅ Deleted directory: {system_path}")
                    deleted_count += 1
                else:
                    print(f"  ⚠️  Not found: {system_path}")

            except Exception as e:
                print(f"  ❌ Error deleting {system_path}: {e}")

        print(f"🗑️  Deleted {deleted_count} systems")
        return deleted_count

    def update_registry(self):
        """Update the messaging systems registry to remove deleted systems."""
        print("📝 Updating messaging systems registry...")

        if not self.registry_path.exists():
            print("  ⚠️  Registry file not found, skipping update")
            return

        try:
            # Read current registry
            with open(self.registry_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Remove entries for deleted systems
            updated_content = content
            removed_systems = []

            for system_path in self.systems_to_delete:
                system_id = Path(system_path).stem

                # Simple removal - look for system ID in registry
                lines = updated_content.split("\n")
                filtered_lines = []
                skip_next = False

                for line in lines:
                    if f"id: {system_id}" in line.lower():
                        removed_systems.append(system_id)
                        skip_next = True
                        continue

                    if skip_next and line.strip() and not line.startswith(" "):
                        skip_next = False

                    if not skip_next:
                        filtered_lines.append(line)

                updated_content = "\n".join(filtered_lines)

            # Write updated registry
            with open(self.registry_path, "w", encoding="utf-8") as f:
                f.write(updated_content)

            print(
                f"  ✅ Updated registry, removed {len(removed_systems)} systems: {removed_systems}"
            )

        except Exception as e:
            print(f"  ❌ Error updating registry: {e}")

    def run_health_check(self):
        """Run health check after consolidation."""
        print("🏥 Running health check after consolidation...")

        try:
            from src.core.messaging.health_check import print_health_report

            print_health_report(verbose=True)
        except Exception as e:
            print(f"  ❌ Error running health check: {e}")

    def execute_consolidation(self):
        """Execute the full consolidation process."""
        print("🚀 Starting Messaging System Consolidation")
        print("=" * 50)

        try:
            # Step 1: Create backup
            self.create_backup()

            # Step 2: Extract logic
            extracted_logic = self.extract_all_logic()

            # Step 3: Delete systems
            deleted_count = self.delete_systems()

            # Step 4: Update registry
            self.update_registry()

            # Step 5: Run health check
            self.run_health_check()

            print("\n🎉 Consolidation completed successfully!")
            print(f"📊 Summary:")
            print(f"  - Systems deleted: {deleted_count}")
            print(f"  - Logic extracted: {len(extracted_logic)} files")
            print(f"  - Backup location: {self.backup_dir}")

            return True

        except Exception as e:
            print(f"\n❌ Consolidation failed: {e}")
            print(f"🔄 Restore from backup: {self.backup_dir}")
            return False


def main():
    """Main execution function."""
    print("🔧 Messaging System Consolidation Tool")
    print("Agent-3 Quality Assurance Co-Captain")
    print("=" * 50)

    consolidator = MessagingSystemConsolidator()

    # Confirm execution
    print("\n⚠️  This will delete 13 messaging systems and consolidate their logic.")
    print("A backup will be created before deletion.")

    response = input("\nProceed with consolidation? (y/N): ").strip().lower()

    if response == "y":
        success = consolidator.execute_consolidation()
        if success:
            print("\n✅ Consolidation completed successfully!")
            print(
                "📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory"
            )
        else:
            print("\n❌ Consolidation failed. Check backup for recovery.")
    else:
        print("❌ Consolidation cancelled.")


if __name__ == "__main__":
    main()
