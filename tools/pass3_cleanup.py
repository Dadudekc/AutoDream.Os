#!/usr/bin/env python3
"""
Pass-3 Aggressive Repository Cleanup Tool
========================================

Main orchestration script for aggressive file reduction:
- Archive deletion (git history as backup)
- Devlog deletion (fresh start)
- Agent workspace tool extraction
- Workspace file cleanup
- Empty directory removal

Author: Agent-4 (Captain)
License: MIT
V2 Compliance: ≤400 lines, modular design
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parents[1]


class Pass3Cleanup:
    """Main cleanup orchestration class"""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.reports_dir = ROOT / "runtime" / "pass3" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.stats = {
            "archives_deleted": 0,
            "devlogs_deleted": 0,
            "agent_tools_extracted": 0,
            "workspace_files_deleted": 0,
            "empty_dirs_removed": 0,
            "space_reclaimed": 0
        }

    def delete_archives(self) -> None:
        """Phase 1: Delete all archive directories"""
        print("🗑️  Phase 1: Deleting archive directories...")
        
        archive_targets = [
            ROOT / "archive",
            ROOT / "runtime" / "consolidation" / "backups",
            ROOT / "agent_workspaces" / "planning_archive"
        ]
        
        for archive_path in archive_targets:
            if archive_path.exists():
                if self.dry_run:
                    size = sum(f.stat().st_size for f in archive_path.rglob('*') if f.is_file())
                    print(f"  [DRY-RUN] Would delete: {archive_path} ({size:,} bytes)")
                    self.stats["space_reclaimed"] += size
                else:
                    size = sum(f.stat().st_size for f in archive_path.rglob('*') if f.is_file())
                    shutil.rmtree(archive_path)
                    print(f"  ✅ Deleted: {archive_path} ({size:,} bytes)")
                    self.stats["space_reclaimed"] += size
                self.stats["archives_deleted"] += 1

    def delete_devlogs(self) -> None:
        """Phase 2: Delete entire devlogs directory"""
        print("📝 Phase 2: Deleting devlogs directory...")
        
        devlogs_path = ROOT / "devlogs"
        if devlogs_path.exists():
            if self.dry_run:
                file_count = len(list(devlogs_path.rglob('*')))
                size = sum(f.stat().st_size for f in devlogs_path.rglob('*') if f.is_file())
                print(f"  [DRY-RUN] Would delete: {file_count} files in devlogs/ ({size:,} bytes)")
                self.stats["devlogs_deleted"] = file_count
                self.stats["space_reclaimed"] += size
            else:
                file_count = len(list(devlogs_path.rglob('*')))
                size = sum(f.stat().st_size for f in devlogs_path.rglob('*') if f.is_file())
                shutil.rmtree(devlogs_path)
                print(f"  ✅ Deleted devlogs/ ({file_count} files, {size:,} bytes)")
                self.stats["devlogs_deleted"] = file_count
                self.stats["space_reclaimed"] += size

    def extract_agent_tools(self) -> List[Dict[str, Any]]:
        """Phase 3: Extract unique agent-built tools"""
        print("🔧 Phase 3: Extracting agent workspace tools...")
        
        extracted_tools = []
        agent_workspaces = ROOT / "agent_workspaces"
        tools_dir = ROOT / "tools"
        
        if not agent_workspaces.exists():
            print("  ⚠️  No agent_workspaces directory found")
            return extracted_tools

        # Get existing tools for comparison
        existing_tools = set()
        if tools_dir.exists():
            existing_tools = {f.name for f in tools_dir.rglob("*.py")}

        # Scan agent workspaces for Python files
        for agent_dir in agent_workspaces.iterdir():
            if not agent_dir.is_dir():
                continue
                
            for py_file in agent_dir.rglob("*.py"):
                if py_file.name in existing_tools:
                    continue
                    
                # Check if it's a utility/tool (not core agent code)
                if any(keyword in py_file.name.lower() for keyword in 
                      ['util', 'tool', 'helper', 'script', 'cli', 'manager']):
                    
                    new_name = f"agent_{agent_dir.name.lower()}_{py_file.name}"
                    new_path = tools_dir / new_name
                    
                    if self.dry_run:
                        print(f"  [DRY-RUN] Would extract: {py_file} → {new_path}")
                    else:
                        shutil.copy2(py_file, new_path)
                        print(f"  ✅ Extracted: {py_file} → {new_path}")
                    
                    extracted_tools.append({
                        "source": str(py_file.relative_to(ROOT)),
                        "target": str(new_path.relative_to(ROOT)),
                        "agent": agent_dir.name
                    })
                    self.stats["agent_tools_extracted"] += 1

        return extracted_tools

    def cleanup_workspaces(self) -> None:
        """Phase 4: Clean up agent workspace files"""
        print("🧹 Phase 4: Cleaning agent workspaces...")
        
        agent_workspaces = ROOT / "agent_workspaces"
        if not agent_workspaces.exists():
            print("  ⚠️  No agent_workspaces directory found")
            return

        deleted_count = 0
        for agent_dir in agent_workspaces.iterdir():
            if not agent_dir.is_dir():
                continue
                
            # Delete .md files (status reports)
            for md_file in agent_dir.rglob("*.md"):
                if self.dry_run:
                    print(f"  [DRY-RUN] Would delete: {md_file}")
                else:
                    md_file.unlink()
                    print(f"  🗑️  Deleted: {md_file}")
                deleted_count += 1
            
            # Delete .txt files (processed logs)
            for txt_file in agent_dir.rglob("*.txt"):
                if self.dry_run:
                    print(f"  [DRY-RUN] Would delete: {txt_file}")
                else:
                    txt_file.unlink()
                    print(f"  🗑️  Deleted: {txt_file}")
                deleted_count += 1

        self.stats["workspace_files_deleted"] = deleted_count
        print(f"  📊 Total files {'would be' if self.dry_run else ''} deleted: {deleted_count}")

    def remove_empty_dirs(self) -> None:
        """Phase 6: Remove empty directories"""
        print("📁 Phase 6: Removing empty directories...")
        
        target_roots = ["src", "tools", "scripts", "agent_workspaces"]
        removed_count = 0
        
        for root_name in target_roots:
            root_path = ROOT / root_name
            if not root_path.exists():
                continue
                
            # Bottom-up traversal (deepest first)
            dirs = sorted([d for d in root_path.rglob("*") if d.is_dir()], 
                         key=lambda p: len(str(p)), reverse=True)
            
            for dir_path in dirs:
                try:
                    if not any(dir_path.iterdir()):  # Empty directory
                        if self.dry_run:
                            print(f"  [DRY-RUN] Would remove empty dir: {dir_path}")
                        else:
                            dir_path.rmdir()
                            print(f"  🗑️  Removed empty dir: {dir_path}")
                        removed_count += 1
                except (OSError, PermissionError):
                    pass  # Skip if can't remove

        self.stats["empty_dirs_removed"] = removed_count

    def generate_report(self, extracted_tools: List[Dict[str, Any]]) -> None:
        """Generate cleanup report"""
        report_path = self.reports_dir / "pass3_cleanup_report.md"
        
        report_content = f"""# Pass-3 Cleanup Report

**Date**: {datetime.now().isoformat()}
**Mode**: {'DRY-RUN' if self.dry_run else 'APPLIED'}

## Summary
- Archives deleted: {self.stats['archives_deleted']}
- Devlogs deleted: {self.stats['devlogs_deleted']}
- Agent tools extracted: {self.stats['agent_tools_extracted']}
- Workspace files deleted: {self.stats['workspace_files_deleted']}
- Empty directories removed: {self.stats['empty_dirs_removed']}
- Space reclaimed: {self.stats['space_reclaimed']:,} bytes

## Extracted Agent Tools
"""
        
        if extracted_tools:
            for tool in extracted_tools:
                report_content += f"- **{tool['agent']}**: `{tool['source']}` → `{tool['target']}`\n"
        else:
            report_content += "- No unique tools found\n"
        
        report_content += f"""
## Next Steps
1. Review extracted tools for usefulness
2. Run duplicate analysis: `python tools/dup_review.py`
3. Apply duplicate consolidation after approval
4. Run validation: `python tools/loc_report.py`
"""
        
        report_path.write_text(report_content, encoding="utf-8")
        print(f"📊 Report generated: {report_path}")

    def run(self) -> None:
        """Execute full cleanup process"""
        print(f"🚀 Pass-3 Aggressive Cleanup ({'DRY-RUN' if self.dry_run else 'APPLY'})")
        print("=" * 60)
        
        # Execute phases
        self.delete_archives()
        self.delete_devlogs()
        extracted_tools = self.extract_agent_tools()
        self.cleanup_workspaces()
        self.remove_empty_dirs()
        
        # Generate report
        self.generate_report(extracted_tools)
        
        print("\n" + "=" * 60)
        print(f"✅ Pass-3 cleanup {'simulation' if self.dry_run else 'completed'}")
        if self.dry_run:
            print("🔍 Review the report and run with --apply to execute")


def main():
    parser = argparse.ArgumentParser(description="Pass-3 Aggressive Repository Cleanup")
    parser.add_argument("--apply", action="store_true", 
                       help="Apply changes (default is dry-run)")
    parser.add_argument("--phase", choices=["1", "2", "3", "4", "6"], 
                       help="Run specific phase only")
    
    args = parser.parse_args()
    
    cleanup = Pass3Cleanup(dry_run=not args.apply)
    
    if args.phase:
        if args.phase == "1":
            cleanup.delete_archives()
        elif args.phase == "2":
            cleanup.delete_devlogs()
        elif args.phase == "3":
            cleanup.extract_agent_tools()
        elif args.phase == "4":
            cleanup.cleanup_workspaces()
        elif args.phase == "6":
            cleanup.remove_empty_dirs()
    else:
        cleanup.run()


if __name__ == "__main__":
    sys.exit(main())

