from src.utils.config_core import get_config
#!/usr/bin/env python3
"""
Duplicate Elimination Executor
Execute comprehensive duplicate elimination across the entire project.
"""

import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Direct import
sys.path.insert(0, str(Path(__file__).parent / "src" / "core" / "duplicate_elimination"))

from consolidated_duplicate_elimination_system import (
    duplicate_elimination_system
)


def main():
    """Execute duplicate elimination."""
    print("🚨 **DUPLICATE ELIMINATION MISSION EXECUTOR** 🚨")
    print("=" * 60)
    
    # Initialize system
    config = {
        "chunk_size": 8192,
        "similarity_threshold": 0.8
    }
    
    print("🔧 Initializing duplicate elimination system...")
    duplicate_elimination_system.initialize(config)
    print("✅ System initialized successfully")
    
    # Scan for duplicates
    print("\n🔍 Scanning for duplicates...")
    duplicates = duplicate_elimination_system.scan_for_duplicates(".")
    
    if not duplicates:
        print("✅ No duplicates found!")
        return
    
    print(f"🔍 Found {len(duplicates)} duplicate groups")
    
    # Display duplicates found
    print("\n📋 DUPLICATES FOUND:")
    print("-" * 40)
    for i, duplicate in enumerate(duplicates, 1):
        print(f"{i}. Type: {duplicate.duplicate_type.value}")
        print(f"   Files: {len(duplicate.file_paths)}")
        print(f"   Priority Score: {duplicate.priority_score:.2f}")
        for path in duplicate.file_paths:
            print(f"     - {path}")
        print()
    
    # Eliminate duplicates
    print("🗑️ Eliminating duplicates...")
    results = duplicate_elimination_system.eliminate_duplicates(duplicates)
    
    # Generate report
    report = duplicate_elimination_system.generate_report(duplicates, results)
    
    # Display results
    print("\n📊 ELIMINATION RESULTS:")
    print("-" * 40)
    summary = report["summary"]
    print(f"Total duplicates found: {summary['total_duplicates_found']}")
    print(f"Total files affected: {summary['total_files_affected']}")
    print(f"Files eliminated: {summary['files_eliminated']}")
    print(f"Successful eliminations: {summary['successful_eliminations']}")
    print(f"Elimination rate: {summary['elimination_rate']:.2%}")
    
    # Save detailed report
    report_path = "duplicate_elimination_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_path}")
    print("\n✅ Duplicate elimination completed successfully!")


if __name__ == "__main__":
    main()
