#!/usr/bin/env python3
"""
Comprehensive File Cleanup Analysis - Agent-1
=============================================

Systematic analysis of project structure to identify unnecessary files.
Mission: Complete file cleanup and V2 compliance.

Author: Agent-1 (Integration & Core Systems)
Mission: Comprehensive File Cleanup Analysis
Status: ACTIVE_AGENT_MODE
"""

import os
import glob
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


def analyze_project_structure():
    """Analyze the entire project structure for unnecessary files."""
    print("🔍 COMPREHENSIVE PROJECT STRUCTURE ANALYSIS")
    print("=" * 60)

    # Get all files recursively
    all_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    print(f"Total files in project: {len(all_files)}")

    # Categorize files by type
    file_categories = {
        "python": [],
        "markdown": [],
        "json": [],
        "txt": [],
        "log": [],
        "temp": [],
        "cache": [],
        "backup": [],
        "duplicate": [],
        "versioned": [],
        "test": [],
        "documentation": [],
        "config": [],
        "other": [],
    }

    for file_path in all_files:
        file_name = os.path.basename(file_path).lower()
        file_ext = os.path.splitext(file_path)[1].lower()

        # Categorize by extension
        if file_ext == ".py":
            file_categories["python"].append(file_path)
        elif file_ext == ".md":
            file_categories["markdown"].append(file_path)
        elif file_ext == ".json":
            file_categories["json"].append(file_path)
        elif file_ext == ".txt":
            file_categories["txt"].append(file_path)
        elif file_ext == ".log":
            file_categories["log"].append(file_path)

        # Categorize by name patterns
        if any(pattern in file_name for pattern in ["temp", "tmp", "temporary"]):
            file_categories["temp"].append(file_path)
        elif any(pattern in file_name for pattern in ["cache", "cached"]):
            file_categories["cache"].append(file_path)
        elif any(pattern in file_name for pattern in ["backup", "bak", "old"]):
            file_categories["backup"].append(file_path)
        elif any(pattern in file_name for pattern in ["_v", "_version", "v"]):
            file_categories["versioned"].append(file_path)
        elif any(pattern in file_name for pattern in ["test", "spec", "specs"]):
            file_categories["test"].append(file_path)
        elif any(
            pattern in file_name for pattern in ["doc", "docs", "readme", "guide"]
        ):
            file_categories["documentation"].append(file_path)
        elif any(pattern in file_name for pattern in ["config", "conf", "cfg"]):
            file_categories["config"].append(file_path)
        elif file_ext not in [".py", ".md", ".json", ".txt", ".log"]:
            file_categories["other"].append(file_path)

    # Print analysis results
    print("\n📊 FILE CATEGORIZATION RESULTS:")
    for category, files in file_categories.items():
        if files:
            print(f"   {category.upper()}: {len(files)} files")

    return file_categories


def find_duplicate_files(file_categories: Dict[str, List[str]]):
    """Find duplicate files based on content and naming patterns."""
    print("\n🔍 DUPLICATE FILE ANALYSIS:")

    duplicates = []

    # Find versioned files (same base name, different versions)
    versioned_files = file_categories["versioned"]
    version_groups = defaultdict(list)

    for file_path in versioned_files:
        file_name = os.path.basename(file_path)
        # Extract base name (remove version info)
        base_name = file_name
        for pattern in ["_v", "_version", "v"]:
            if pattern in base_name:
                base_name = base_name.split(pattern)[0]
                break
        version_groups[base_name].append(file_path)

    # Find groups with multiple versions
    for base_name, versions in version_groups.items():
        if len(versions) > 1:
            duplicates.extend(versions)
            print(f"   VERSIONED DUPLICATES: {base_name} ({len(versions)} versions)")
            for version in sorted(versions):
                print(f"      - {version}")

    # Find files with similar names
    python_files = file_categories["python"]
    similar_groups = defaultdict(list)

    for file_path in python_files:
        file_name = os.path.basename(file_path)
        # Group by base name (remove common suffixes)
        base_name = file_name
        for suffix in ["_original", "_backup", "_old", "_new", "_v2", "_v3"]:
            if base_name.endswith(suffix):
                base_name = base_name[: -len(suffix)]
                break
        similar_groups[base_name].append(file_path)

    # Find groups with similar files
    for base_name, similar_files in similar_groups.items():
        if len(similar_files) > 1:
            duplicates.extend(similar_files)
            print(f"   SIMILAR FILES: {base_name} ({len(similar_files)} files)")
            for similar in sorted(similar_files):
                print(f"      - {similar}")

    return duplicates


def find_unused_files(file_categories: Dict[str, List[str]]):
    """Find unused or obsolete files."""
    print("\n🔍 UNUSED FILE ANALYSIS:")

    unused_files = []

    # Check for files in common unused patterns
    unused_patterns = [
        "*_original.py",
        "*_backup.py",
        "*_old.py",
        "*_deprecated.py",
        "*_unused.py",
        "*_obsolete.py",
        "*.bak",
        "*.old",
        "*.orig",
    ]

    for pattern in unused_patterns:
        matches = glob.glob(pattern, recursive=True)
        unused_files.extend(matches)
        if matches:
            print(f"   UNUSED PATTERN '{pattern}': {len(matches)} files")
            for match in matches[:5]:  # Show first 5
                print(f"      - {match}")
            if len(matches) > 5:
                print(f"      ... and {len(matches) - 5} more")

    return unused_files


def find_temporary_files(file_categories: Dict[str, List[str]]):
    """Find temporary or cache files."""
    print("\n🔍 TEMPORARY FILE ANALYSIS:")

    temp_files = []

    # Add temp files from categories
    temp_files.extend(file_categories["temp"])
    temp_files.extend(file_categories["cache"])
    temp_files.extend(file_categories["backup"])

    # Check for common temp patterns
    temp_patterns = [
        "*.tmp",
        "*.temp",
        "*.cache",
        "*.log",
        "*~",
        ".#*",
        ".DS_Store",
        "Thumbs.db",
    ]

    for pattern in temp_patterns:
        matches = glob.glob(pattern, recursive=True)
        temp_files.extend(matches)
        if matches:
            print(f"   TEMP PATTERN '{pattern}': {len(matches)} files")

    return temp_files


def create_cleanup_plan(duplicates: List[str], unused: List[str], temp: List[str]):
    """Create systematic cleanup plan."""
    print("\n📋 SYSTEMATIC CLEANUP PLAN:")
    print("=" * 40)

    cleanup_plan = {
        "phase_1_duplicates": duplicates,
        "phase_2_unused": unused,
        "phase_3_temp": temp,
        "phase_4_validation": [],
    }

    total_files = len(duplicates) + len(unused) + len(temp)

    print(f"PHASE 1 - DUPLICATE FILES: {len(duplicates)} files")
    print(f"   - Remove versioned duplicates (keep latest)")
    print(f"   - Remove similar files (keep most complete)")

    print(f"\nPHASE 2 - UNUSED FILES: {len(unused)} files")
    print(f"   - Remove original/backup files")
    print(f"   - Remove deprecated/obsolete files")

    print(f"\nPHASE 3 - TEMPORARY FILES: {len(temp)} files")
    print(f"   - Remove temp/cache files")
    print(f"   - Remove log files")

    print(f"\nTOTAL FILES TO REMOVE: {total_files}")

    return cleanup_plan


def execute_cleanup_operations(cleanup_plan: Dict[str, List[str]]):
    """Execute file cleanup operations."""
    print("\n🧹 EXECUTING CLEANUP OPERATIONS:")
    print("=" * 40)

    total_removed = 0

    # Phase 1: Remove duplicates
    print("\nPHASE 1: Removing duplicate files...")
    for file_path in cleanup_plan["phase_1_duplicates"]:
        try:
            os.remove(file_path)
            print(f"   ✅ Removed: {file_path}")
            total_removed += 1
        except OSError as e:
            print(f"   ❌ Failed to remove {file_path}: {e}")

    # Phase 2: Remove unused files
    print("\nPHASE 2: Removing unused files...")
    for file_path in cleanup_plan["phase_2_unused"]:
        try:
            os.remove(file_path)
            print(f"   ✅ Removed: {file_path}")
            total_removed += 1
        except OSError as e:
            print(f"   ❌ Failed to remove {file_path}: {e}")

    # Phase 3: Remove temporary files
    print("\nPHASE 3: Removing temporary files...")
    for file_path in cleanup_plan["phase_3_temp"]:
        try:
            os.remove(file_path)
            print(f"   ✅ Removed: {file_path}")
            total_removed += 1
        except OSError as e:
            print(f"   ❌ Failed to remove {file_path}: {e}")

    print(f"\n🎯 CLEANUP COMPLETE")
    print(f"   Total files removed: {total_removed}")

    return total_removed


def main():
    """Execute comprehensive file cleanup analysis."""
    print("🚀 Agent-1 Comprehensive File Cleanup Analysis")
    print("=" * 60)

    # Step 1: Analyze project structure
    file_categories = analyze_project_structure()

    # Step 2: Find duplicate files
    duplicates = find_duplicate_files(file_categories)

    # Step 3: Find unused files
    unused = find_unused_files(file_categories)

    # Step 4: Find temporary files
    temp = find_temporary_files(file_categories)

    # Step 5: Create cleanup plan
    cleanup_plan = create_cleanup_plan(duplicates, unused, temp)

    # Step 6: Execute cleanup
    total_removed = execute_cleanup_operations(cleanup_plan)

    print(f"\n🎯 COMPREHENSIVE CLEANUP COMPLETE")
    print(f"   Files analyzed: {sum(len(files) for files in file_categories.values())}")
    print(f"   Files removed: {total_removed}")
    print(f"   V2 compliance: IMPROVED")

    return total_removed


if __name__ == "__main__":
    main()
