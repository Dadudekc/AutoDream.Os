#!/usr/bin/env python3
"""
Consolidation Execution Script
==============================

Automated script to execute the consolidation roadmap plan.
Performs safe deletions and generates consolidation commands.

Usage:
    python consolidation_execution_script.py --phase <phase_number>
    python consolidation_execution_script.py --dry-run
    python consolidation_execution_script.py --status

Author: V2_SWARM_CAPTAIN
"""

import os
import shutil
import argparse
from pathlib import Path
from typing import List, Dict, Any

class ConsolidationExecutor:
    """Execute consolidation plan phases."""

    def __init__(self):
        self.src_path = Path("src")
        self.backup_path = Path("backups/consolidation_backup")
        self.dry_run = False

    def set_dry_run(self, dry_run: bool):
        """Set dry run mode."""
        self.dry_run = dry_run
        print(f"🔍 DRY RUN MODE: {'ENABLED' if dry_run else 'DISABLED'}")

    def create_backup(self, files_to_backup: List[str]):
        """Create backup of files before modification."""
        if self.dry_run:
            print(f"📋 Would create backup of {len(files_to_backup)} files")
            return

        self.backup_path.mkdir(parents=True, exist_ok=True)

        for file_path in files_to_backup:
            src_file = Path(file_path)
            if src_file.exists():
                # Create relative backup path
                rel_path = src_file.relative_to(self.src_path)
                backup_file = self.backup_path / rel_path

                # Ensure backup directory exists
                backup_file.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                shutil.copy2(src_file, backup_file)
                print(f"📋 Backed up: {file_path} → {backup_file}")

    def execute_phase_1_safe_deletions(self):
        """Execute Phase 1: Safe deletions."""
        print("🗑️  PHASE 1: SAFE DELETIONS")
        print("-" * 40)

        files_to_delete = [
            "src/agent_registry.py",
            "src/swarmstatus.py",
            "src/commandresult.py"
        ]

        # Find all __pycache__ directories
        pycache_dirs = []
        for root, dirs, files in os.walk("src"):
            if "__pycache__" in dirs:
                pycache_dirs.append(os.path.join(root, "__pycache__"))

        files_to_delete.extend(pycache_dirs)

        # Find all .pyc files
        pyc_files = []
        for root, dirs, files in os.walk("src"):
            for file in files:
                if file.endswith('.pyc'):
                    pyc_files.append(os.path.join(root, file))

        files_to_delete.extend(pyc_files)

        print(f"📋 Found {len(files_to_delete)} items to delete")

        # Create backup
        self.create_backup([f for f in files_to_delete if not f.endswith('__pycache__')])

        # Execute deletions
        deleted_count = 0
        for item in files_to_delete:
            if os.path.exists(item):
                if self.dry_run:
                    print(f"🗑️  Would delete: {item}")
                else:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                    else:
                        os.remove(item)
                    print(f"🗑️  Deleted: {item}")
                deleted_count += 1

        print(f"✅ Phase 1 Complete: {deleted_count} items removed")
        return deleted_count

    def execute_phase_2_managers_consolidation(self):
        """Execute Phase 2: Managers consolidation."""
        print("🔧 PHASE 2: MANAGERS CONSOLIDATION")
        print("-" * 40)

        managers_dir = self.src_path / "core" / "managers"

        if not managers_dir.exists():
            print("❌ Managers directory not found")
            return 0

        # Get all manager files
        manager_files = []
        for root, dirs, files in os.walk(managers_dir):
            for file in files:
                if file.endswith('.py'):
                    manager_files.append(Path(root) / file)

        print(f"📋 Found {len(manager_files)} manager files to consolidate")

        if self.dry_run:
            print("📋 Would consolidate into:")
            print("   • src/core/managers/manager_core.py")
            print("   • src/core/managers/agent_managers.py")
            print("   • src/core/managers/system_managers.py")
            return len(manager_files)

        # Create consolidation target files
        consolidation_targets = {
            managers_dir / "manager_core.py": [],
            managers_dir / "agent_managers.py": [],
            managers_dir / "system_managers.py": []
        }

        # Read and categorize manager files
        for file_path in manager_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Simple categorization logic
                if 'agent' in file_path.name.lower() or 'coordination' in content.lower():
                    consolidation_targets[managers_dir / "agent_managers.py"].append((file_path, content))
                elif 'system' in file_path.name.lower() or 'config' in content.lower():
                    consolidation_targets[managers_dir / "system_managers.py"].append((file_path, content))
                else:
                    consolidation_targets[managers_dir / "manager_core.py"].append((file_path, content))

            except Exception as e:
                print(f"⚠️  Error reading {file_path}: {e}")

        # Create consolidated files
        consolidated_count = 0
        for target_file, source_files in consolidation_targets.items():
            if source_files:
                consolidated_content = f'''"""
Consolidated Manager Module
===========================

Consolidated from {len(source_files)} manager files.

Generated by consolidation script.
"""

'''

                for source_file, content in source_files:
                    consolidated_content += f'''
# === FROM: {source_file.name} ===
{content}
'''

                # Write consolidated file
                target_file.parent.mkdir(parents=True, exist_ok=True)
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(consolidated_content)

                print(f"📝 Created: {target_file} ({len(source_files)} files consolidated)")
                consolidated_count += len(source_files)

        # Backup and remove original files
        original_files = [str(f) for f, _ in sum(consolidation_targets.values(), [])]
        self.create_backup(original_files)

        for file_path in original_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️  Removed original: {file_path}")

        print(f"✅ Phase 2 Complete: {consolidated_count} files consolidated into {len([t for t in consolidation_targets.values() if t])} modules")
        return consolidated_count

    def generate_consolidation_report(self):
        """Generate comprehensive consolidation report."""
        print("📊 CONSOLIDATION STATUS REPORT")
        print("=" * 50)

        # Count current files
        total_files = 0
        for root, dirs, files in os.walk("src"):
            total_files += len([f for f in files if f.endswith('.py')])

        print(f"📁 Current src/ structure: {total_files} Python files")

        # Check consolidation status
        consolidation_checks = {
            "Empty stubs removed": not any(
                os.path.exists(f"src/{f}") for f in
                ["agent_registry.py", "swarmstatus.py", "commandresult.py"]
            ),
            "Cache files cleaned": not any(
                "__pycache__" in str(p) for p in Path("src").rglob("*")
            ),
            "Managers consolidated": (self.src_path / "core" / "managers" / "manager_core.py").exists(),
            "Analytics restructured": len(list((self.src_path / "core" / "analytics").glob("*.py"))) <= 5
        }

        print("
✅ COMPLETION STATUS:"        for check, completed in consolidation_checks.items():
            status = "✅" if completed else "❌"
            print(f"   {status} {check}")

        completed_count = sum(consolidation_checks.values())
        print(f"\n📈 Progress: {completed_count}/{len(consolidation_checks)} phases completed")

        return consolidation_checks

def main():
    """Main consolidation execution."""
    parser = argparse.ArgumentParser(description="Consolidation Execution Script")
    parser.add_argument("--phase", type=int, choices=range(1, 9),
                       help="Execute specific consolidation phase")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be done without executing")
    parser.add_argument("--status", action="store_true",
                       help="Show consolidation status report")

    args = parser.parse_args()

    executor = ConsolidationExecutor()
    executor.set_dry_run(args.dry_run)

    if args.status:
        executor.generate_consolidation_report()
        return

    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        print()

    if args.phase == 1:
        executor.execute_phase_1_safe_deletions()
    elif args.phase == 2:
        executor.execute_phase_2_managers_consolidation()
    else:
        print("🎯 CONSOLIDATION EXECUTION SCRIPT")
        print("=" * 50)
        print("Available phases:")
        print("  --phase 1: Safe deletions (empty stubs, cache files)")
        print("  --phase 2: Managers consolidation")
        print("  --phase 3: Analytics consolidation")
        print("  --phase 4: Integration consolidation")
        print("  --phase 5: Orchestration consolidation")
        print("  --phase 6: Emergency consolidation")
        print("  --phase 7: Frontend streamlining")
        print("  --phase 8: Phase6 cleanup")
        print()
        print("Usage examples:")
        print("  python consolidation_execution_script.py --phase 1 --dry-run")
        print("  python consolidation_execution_script.py --status")
        print("  python consolidation_execution_script.py --phase 2")

if __name__ == "__main__":
    main()
