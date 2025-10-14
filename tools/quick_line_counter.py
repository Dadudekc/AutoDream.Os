#!/usr/bin/env python3
"""
Quick Line Counter - Essential Tool
===================================

Quickly count lines in files - needed constantly for V2 compliance checks.

Author: Agent-8 (Quality Assurance) - Thread Experience Tool
Created: 2025-10-14
"""

import sys
from pathlib import Path


def count_lines(file_path: str) -> int:
    """Count lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python quick_line_counter.py <file1> [file2] [file3] ...")
        print("\nQuickly count lines in files for V2 compliance checks")
        return 1
    
    files = sys.argv[1:]
    results = []
    
    for file_path in files:
        if Path(file_path).exists():
            count = count_lines(file_path)
            status = "✅" if count <= 400 else "⚠️" if count <= 600 else "🔴"
            results.append((file_path, count, status))
        else:
            results.append((file_path, 0, "❌"))
    
    # Print results
    print("\n" + "="*80)
    print("📊 LINE COUNT REPORT")
    print("="*80)
    
    for file_path, count, status in results:
        compliance = ""
        if count > 0:
            if count <= 400:
                compliance = "COMPLIANT"
            elif count <= 600:
                compliance = "MAJOR VIOLATION"
            else:
                compliance = "CRITICAL VIOLATION"
        else:
            compliance = "NOT FOUND"
            
        print(f"{status} {file_path}: {count} lines - {compliance}")
    
    print("="*80)
    print(f"\nV2 Limits: ≤400 lines (compliant), 401-600 (major), >600 (critical)")
    print("="*80 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

