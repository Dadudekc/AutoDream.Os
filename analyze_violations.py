#!/usr/bin/env python3
"""
V2 Coding Standards Violation Analyzer
Agent-2 Emergency Response Tool
"""

import os
import sys
from pathlib import Path

def analyze_violations():
    """Analyze all Python files for V2 coding standards violations."""
    violations = []
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                    
                    if lines > 300:
                        violations.append((file_path, lines))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    # Sort by line count (descending)
    violations.sort(key=lambda x: x[1], reverse=True)
    
    print("🚨 V2 CODING STANDARDS VIOLATIONS DETECTED")
    print("=" * 60)
    
    # Critical violations (1000+ lines)
    critical = [v for v in violations if v[1] >= 1000]
    if critical:
        print(f"\n🔴 CRITICAL VIOLATIONS (1000+ lines): {len(critical)} files")
        for file_path, lines in critical:
            print(f"  {lines:>4} lines: {file_path}")
    
    # Major violations (500-999 lines)
    major = [v for v in violations if 500 <= v[1] < 1000]
    if major:
        print(f"\n⚠️  MAJOR VIOLATIONS (500-999 lines): {len(major)} files")
        for file_path, lines in major[:10]:  # Show top 10
            print(f"  {lines:>4} lines: {file_path}")
        if len(major) > 10:
            print(f"  ... and {len(major) - 10} more files")
    
    # Moderate violations (300-499 lines)
    moderate = [v for v in violations if 300 < v[1] < 500]
    if moderate:
        print(f"\n🟡 MODERATE VIOLATIONS (300-499 lines): {len(moderate)} files")
        for file_path, lines in moderate[:10]:  # Show top 10
            print(f"  {lines:>4} lines: {file_path}")
        if len(moderate) > 10:
            print(f"  ... and {len(moderate) - 10} more files")
    
    print(f"\n📊 SUMMARY:")
    print(f"  Total violations: {len(violations)} files")
    print(f"  Critical (1000+): {len(critical)} files")
    print(f"  Major (500-999): {len(major)} files")
    print(f"  Moderate (300-499): {len(moderate)} files")
    
    return violations

if __name__ == "__main__":
    violations = analyze_violations()
