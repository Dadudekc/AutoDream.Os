#!/usr/bin/env python3
"""
Fix ManagerResult calls in modular components
"""

import os
import re

def fix_file(filepath):
    """Fix ManagerResult calls in a file."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix message parameter to metrics
    content = re.sub(r'message=([^,)]+)', r'metrics={"message": \1}', content)
    
    # Ensure data parameter is always present
    content = re.sub(r'ManagerResult\(\s*success=False,\s*error=([^,)]+),\s*metrics=', 
                     r'ManagerResult(\n                success=False,\n                error=\1,\n                data={},\n                metrics=', content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"Fixed: {filepath}")

# Fix all three files
files = [
    'src/core/managers/onboarding_manager.py',
    'src/core/managers/error_recovery_manager.py', 
    'src/core/managers/results_manager.py'
]

for filepath in files:
    fix_file(filepath)

print("All files fixed!")
