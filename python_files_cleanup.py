#!/usr/bin/env python3
"""
Python Files Cleanup Script
===========================

Comprehensive script to identify and remove unnecessary Python files
while preserving all essential functionality.

Author: Agent-3 (Database Specialist)
License: MIT
"""

import os
import shutil
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
import json
from datetime import datetime

class PythonFilesCleanup:
    """Comprehensive Python files cleanup system."""
    
    def __init__(self, project_root: str = "."):
        """Initialize cleanup system."""
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / "cleanup_backup"
        self.cleanup_log = []
        
        # Files to keep (essential)
        self.essential_files = set()
        
        # Files to remove (redundant/duplicate)
        self.files_to_remove = []
        
        # Statistics
        self.stats = {
            "total_files": 0,
            "duplicates_found": 0,
            "version_files_found": 0,
            "backup_files_found": 0,
            "test_files_found": 0,
            "files_to_remove": 0,
            "files_kept": 0
        }
    
    def scan_python_files(self) -> List[Path]:
        """Scan all Python files in the project."""
        python_files = []
        
        for py_file in self.project_root.rglob("*.py"):
            if "__pycache__" not in str(py_file) and ".git" not in str(py_file):
                python_files.append(py_file)
        
        self.stats["total_files"] = len(python_files)
        return python_files
    
    def identify_duplicates(self, python_files: List[Path]) -> Dict[str, List[Path]]:
        """Identify duplicate files by name."""
        duplicates = {}
        
        for py_file in python_files:
            filename = py_file.name
            if filename not in duplicates:
                duplicates[filename] = []
            duplicates[filename].append(py_file)
        
        # Filter to only actual duplicates
        actual_duplicates = {k: v for k, v in duplicates.items() if len(v) > 1}
        self.stats["duplicates_found"] = len(actual_duplicates)
        
        return actual_duplicates
    
    def identify_version_files(self, python_files: List[Path]) -> List[Path]:
        """Identify version files (v2, backup, old, temp)."""
        version_patterns = [
            "_v2.py", "_backup.py", "_old.py", "_temp.py", "_tmp.py",
            "_bak.py", "_orig.py", "_copy.py", "_duplicate.py"
        ]
        
        version_files = []
        for py_file in python_files:
            filename = py_file.name.lower()
            if any(pattern in filename for pattern in version_patterns):
                version_files.append(py_file)
        
        self.stats["version_files_found"] = len(version_files)
        return version_files
    
    def identify_backup_files(self, python_files: List[Path]) -> List[Path]:
        """Identify backup files."""
        backup_patterns = [
            "backup_", "_backup", "old_", "_old", "temp_", "_temp"
        ]
        
        backup_files = []
        for py_file in python_files:
            filename = py_file.name.lower()
            if any(pattern in filename for pattern in backup_patterns):
                backup_files.append(py_file)
        
        self.stats["backup_files_found"] = len(backup_files)
        return backup_files
    
    def identify_test_files(self, python_files: List[Path]) -> List[Path]:
        """Identify test files."""
        test_files = []
        for py_file in python_files:
            filename = py_file.name.lower()
            if (filename.startswith("test_") or 
                filename.endswith("_test.py") or 
                filename == "test.py"):
                test_files.append(py_file)
        
        self.stats["test_files_found"] = len(test_files)
        return test_files
    
    def identify_v3_files(self, python_files: List[Path]) -> List[Path]:
        """Identify V3 deployment files."""
        v3_files = []
        for py_file in python_files:
            filename = py_file.name.lower()
            if filename.startswith("v3_") or "v3_" in filename:
                v3_files.append(py_file)
        
        return v3_files
    
    def analyze_file_importance(self, py_file: Path) -> Tuple[bool, str]:
        """Analyze if a file is important to keep."""
        filename = py_file.name.lower()
        relative_path = py_file.relative_to(self.project_root)
        
        # Essential files to always keep
        essential_patterns = [
            "__init__.py",
            "main.py",
            "app.py",
            "run.py",
            "setup.py",
            "requirements.txt",
            "config.py",
            "settings.py",
            "core.py",
            "models.py",
            "utils.py",
            "helpers.py"
        ]
        
        # Check if it's an essential file
        for pattern in essential_patterns:
            if filename == pattern:
                return True, f"Essential file: {pattern}"
        
        # Check if it's in a critical directory
        critical_dirs = [
            "src/services/vector_database",
            "src/services/discord_bot",
            "src/services/messaging",
            "src/core",
            "src/architecture"
        ]
        
        for critical_dir in critical_dirs:
            if critical_dir in str(relative_path):
                return True, f"Critical directory: {critical_dir}"
        
        # Check if it's a recent file (less than 30 days old)
        try:
            file_age = datetime.now().timestamp() - py_file.stat().st_mtime
            if file_age < 30 * 24 * 3600:  # 30 days
                return True, "Recent file (less than 30 days old)"
        except:
            pass
        
        return False, "Not essential"
    
    def determine_files_to_remove(self, python_files: List[Path]) -> List[Path]:
        """Determine which files should be removed."""
        files_to_remove = []
        
        # Get duplicates
        duplicates = self.identify_duplicates(python_files)
        
        # For each duplicate group, keep the most important one
        for filename, duplicate_files in duplicates.items():
            if filename == "__init__.py":
                # Keep all __init__.py files
                continue
            
            # Analyze each duplicate
            file_scores = []
            for py_file in duplicate_files:
                is_important, reason = self.analyze_file_importance(py_file)
                score = 1 if is_important else 0
                
                # Prefer files in src/ directory
                if "src/" in str(py_file):
                    score += 2
                
                # Prefer newer files
                try:
                    file_age = datetime.now().timestamp() - py_file.stat().st_mtime
                    if file_age < 7 * 24 * 3600:  # Less than 7 days
                        score += 1
                except:
                    pass
                
                file_scores.append((score, py_file, reason))
            
            # Sort by score (highest first)
            file_scores.sort(key=lambda x: x[0], reverse=True)
            
            # Keep the best one, remove the rest
            if len(file_scores) > 1:
                kept_file = file_scores[0][1]
                self.essential_files.add(kept_file)
                
                for score, py_file, reason in file_scores[1:]:
                    files_to_remove.append(py_file)
                    self.cleanup_log.append(f"Duplicate: {py_file} (kept: {kept_file})")
        
        # Add version files
        version_files = self.identify_version_files(python_files)
        for py_file in version_files:
            files_to_remove.append(py_file)
            self.cleanup_log.append(f"Version file: {py_file}")
        
        # Add backup files
        backup_files = self.identify_backup_files(python_files)
        for py_file in backup_files:
            files_to_remove.append(py_file)
            self.cleanup_log.append(f"Backup file: {py_file}")
        
        # Add some V3 files (keep essential ones)
        v3_files = self.identify_v3_files(python_files)
        for py_file in v3_files:
            filename = py_file.name.lower()
            # Keep important V3 files
            if any(important in filename for important in ["directives", "validation", "security"]):
                continue
            files_to_remove.append(py_file)
            self.cleanup_log.append(f"V3 file: {py_file}")
        
        self.stats["files_to_remove"] = len(files_to_remove)
        return files_to_remove
    
    def create_backup(self, files_to_remove: List[Path]) -> bool:
        """Create backup of files to be removed."""
        try:
            self.backup_dir.mkdir(exist_ok=True)
            
            for py_file in files_to_remove:
                backup_path = self.backup_dir / py_file.relative_to(self.project_root)
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(py_file, backup_path)
            
            print(f"✅ Backup created in: {self.backup_dir}")
            return True
        except Exception as e:
            print(f"❌ Failed to create backup: {e}")
            return False
    
    def remove_files(self, files_to_remove: List[Path], dry_run: bool = True) -> bool:
        """Remove files (with dry run option)."""
        if dry_run:
            print("🔍 DRY RUN - No files will be actually removed")
            print("=" * 60)
        
        for py_file in files_to_remove:
            try:
                if dry_run:
                    print(f"Would remove: {py_file}")
                else:
                    py_file.unlink()
                    print(f"✅ Removed: {py_file}")
            except Exception as e:
                print(f"❌ Failed to remove {py_file}: {e}")
                return False
        
        return True
    
    def generate_report(self) -> Dict:
        """Generate cleanup report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "statistics": self.stats,
            "cleanup_log": self.cleanup_log,
            "files_removed": len(self.files_to_remove),
            "files_kept": self.stats["total_files"] - len(self.files_to_remove),
            "reduction_percentage": (len(self.files_to_remove) / self.stats["total_files"]) * 100
        }
        
        return report
    
    def run_cleanup(self, dry_run: bool = True) -> bool:
        """Run the complete cleanup process."""
        print("🧹 Python Files Cleanup")
        print("=" * 50)
        
        # Scan files
        print("1. Scanning Python files...")
        python_files = self.scan_python_files()
        print(f"   Found {len(python_files)} Python files")
        
        # Analyze files
        print("2. Analyzing files...")
        files_to_remove = self.determine_files_to_remove(python_files)
        print(f"   Identified {len(files_to_remove)} files to remove")
        
        # Show statistics
        print("\n📊 Cleanup Statistics:")
        print(f"   Total files: {self.stats['total_files']}")
        print(f"   Duplicates found: {self.stats['duplicates_found']}")
        print(f"   Version files: {self.stats['version_files_found']}")
        print(f"   Backup files: {self.stats['backup_files_found']}")
        print(f"   Test files: {self.stats['test_files_found']}")
        print(f"   Files to remove: {len(files_to_remove)}")
        print(f"   Files to keep: {self.stats['total_files'] - len(files_to_remove)}")
        print(f"   Reduction: {((len(files_to_remove) / self.stats['total_files']) * 100):.1f}%")
        
        # Create backup
        if not dry_run and files_to_remove:
            print("\n3. Creating backup...")
            if not self.create_backup(files_to_remove):
                return False
        
        # Remove files
        print(f"\n4. {'Simulating' if dry_run else 'Removing'} files...")
        if not self.remove_files(files_to_remove, dry_run):
            return False
        
        # Generate report
        report = self.generate_report()
        
        # Save report
        report_file = self.project_root / "cleanup_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📋 Report saved to: {report_file}")
        
        if dry_run:
            print("\n✅ Dry run completed successfully!")
            print("💡 Run with --execute to actually remove files")
        else:
            print("\n✅ Cleanup completed successfully!")
        
        return True

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Python Files Cleanup")
    parser.add_argument("--execute", action="store_true", help="Actually remove files (default: dry run)")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    
    args = parser.parse_args()
    
    cleanup = PythonFilesCleanup(args.project_root)
    success = cleanup.run_cleanup(dry_run=not args.execute)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
