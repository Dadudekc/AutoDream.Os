#!/usr/bin/env python3
"""
Remove Remaining Duplicates
===========================

Script to remove remaining duplicate and version files that were missed.
"""

import os
import shutil
from pathlib import Path

def remove_remaining_duplicates():
    """Remove remaining duplicate files."""
    
    print("🔍 Removing Remaining Duplicates")
    print("=" * 50)
    
    # Files to remove (remaining duplicates/versions)
    files_to_remove = [
        # Vector database version files
        "src/services/vector_database/status_indexer_v2.py",
        "src/services/vector_database/vector_database_monitoring_v2.py", 
        "src/services/vector_database/vector_database_orchestrator_v2.py",
        
        # Other version files that might remain
        "src/services/vector_database/v3_contract_execution_system.py",  # This was created by Agent-3, might be duplicate
    ]
    
    removed_count = 0
    
    for file_path in files_to_remove:
        full_path = Path(file_path)
        if full_path.exists():
            try:
                # Create backup
                backup_dir = Path("cleanup_backup")
                backup_dir.mkdir(exist_ok=True)
                backup_path = backup_dir / full_path.name
                shutil.copy2(full_path, backup_path)
                
                # Remove file
                full_path.unlink()
                print(f"✅ Removed: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {file_path}: {e}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print(f"\n📊 Removed {removed_count} additional duplicate files")
    return removed_count

def check_final_duplicates():
    """Check for any remaining duplicates."""
    
    print("\n🔍 Final Duplicate Check")
    print("=" * 50)
    
    # Get all Python files
    python_files = []
    for py_file in Path(".").rglob("*.py"):
        if "__pycache__" not in str(py_file) and ".git" not in str(py_file) and "cleanup" not in str(py_file):
            python_files.append(py_file)
    
    # Group by name
    duplicates = {}
    for py_file in python_files:
        filename = py_file.name
        if filename not in duplicates:
            duplicates[filename] = []
        duplicates[filename].append(py_file)
    
    # Find actual duplicates (excluding __init__.py)
    actual_duplicates = {k: v for k, v in duplicates.items() if len(v) > 1 and k != "__init__.py"}
    
    if actual_duplicates:
        print("⚠️  Remaining duplicates found:")
        for filename, files in actual_duplicates.items():
            print(f"  {filename} ({len(files)} files):")
            for file in files:
                print(f"    {file}")
    else:
        print("✅ No remaining duplicates found!")
    
    return len(actual_duplicates)

def main():
    """Main function."""
    print("🧹 Removing Remaining Duplicates")
    print("=" * 50)
    
    # Remove remaining duplicates
    removed = remove_remaining_duplicates()
    
    # Check final state
    remaining = check_final_duplicates()
    
    # Final count
    python_files = list(Path(".").rglob("*.py"))
    python_files = [f for f in python_files if "__pycache__" not in str(f) and ".git" not in str(f) and "cleanup" not in str(f)]
    
    print(f"\n📊 Final Statistics:")
    print(f"  Total Python files: {len(python_files)}")
    print(f"  Additional files removed: {removed}")
    print(f"  Remaining duplicates: {remaining}")
    
    if remaining == 0:
        print("\n🎉 All duplicates successfully removed!")
    else:
        print(f"\n⚠️  {remaining} duplicate groups still remain")

if __name__ == "__main__":
    main()
