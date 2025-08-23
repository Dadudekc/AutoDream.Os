#!/usr/bin/env python3
"""Check line counts of refactored workflow modules"""

import os

files = [
    'src/core/workflow/workflow_types.py',
    'src/core/workflow/workflow_core.py', 
    'src/core/workflow/workflow_execution.py',
    'src/core/workflow/workflow_cli.py'
]

print("📊 Workflow Module Line Counts:")
print("=" * 40)

total_lines = 0
for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            lines = len(f.readlines())
            total_lines += lines
            status = "✅" if lines <= 300 else "❌"
            print(f"{status} {file_path}: {lines} lines")
    else:
        print(f"❌ {file_path}: File not found")

print("=" * 40)
print(f"📈 Total Lines: {total_lines}")
print(f"📉 Original File: 861 lines")
print(f"🎯 Reduction: {861 - total_lines} lines ({((861 - total_lines) / 861 * 100):.1f}% reduction)")
