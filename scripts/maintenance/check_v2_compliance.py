#!/usr/bin/env python3
"""
V2 Compliance Checker
====================

Check for V2 compliance violations in the project.
"""

from pathlib import Path

def check_v2_compliance():
    """Check for V2 compliance violations."""
    violations = []
    
    for py_file in Path('.').rglob('*.py'):
        # Skip test files and __pycache__ directories
        if any(x in str(py_file) for x in ['test', '__pycache__', '.git']):
            continue
        
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                line_count = len(lines)
                
                if line_count > 400:
                    violations.append({
                        'file': str(py_file),
                        'lines': line_count,
                        'excess': line_count - 400
                    })
        except Exception as e:
            print(f"Error reading {py_file}: {e}")
            continue
    
    # Sort by line count (descending)
# SECURITY: Key placeholder - replace with environment variable
    
    print("V2 Compliance Violations:")
    print("=" * 50)
    
    if violations:
        for violation in violations:
            print(f"  {violation['file']}: {violation['lines']} lines ({violation['excess']} over limit)")
    else:
        print("  ✅ No V2 compliance violations found!")
    
    return violations

if __name__ == "__main__":
    violations = check_v2_compliance()
    print(f"\nTotal violations: {len(violations)}")


