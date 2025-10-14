#!/usr/bin/env python3
"""
File Size Cap Enforcer (Lean Excellence Framework)
Checks that Python files don't exceed 600 lines
"""
import sys
import os

MAX_LINES = 600

def check_file_size(filepath):
    """Check if file exceeds line limit."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            line_count = sum(1 for _ in f)
        return line_count, line_count <= MAX_LINES
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")
        return 0, True

def main():
    """Check all provided files."""
    files = [f for f in sys.argv[1:] if os.path.isfile(f)]
    
    if not files:
        sys.exit(0)
    
    violations = []
    for filepath in files:
        line_count, compliant = check_file_size(filepath)
        if not compliant:
            violations.append((filepath, line_count))
    
    if violations:
        print("\n❌ File Size Cap Violations (Lean Excellence Framework):")
        for filepath, line_count in violations:
            print(f"   ERROR: {filepath} has {line_count} lines (max {MAX_LINES})")
        print(f"\n   Please refactor files to ≤{MAX_LINES} lines per STANDARDS.md\n")
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()

