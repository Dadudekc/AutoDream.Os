#!/usr/bin/env python3
"""
Compliance Check Script

Simple script to verify refactoring compliance and line count reductions.
"""

import os
import json
from pathlib import Path

def check_file_line_count(file_path):
    """Check line count of a specific file"""
    try:
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return len(lines)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def main():
    """Main compliance check"""
    print("🔍 COMPLIANCE CHECK - Refactoring Validation")
    print("=" * 50)
    
    # Check refactored files
    refactored_files = [
        "src/core/v2_comprehensive_messaging_system.py",
        "src/core/autonomous_development.py"
    ]
    
    for file_path in refactored_files:
        current_lines = check_file_line_count(file_path)
        if current_lines is not None:
            print(f"\n📁 {file_path}")
            print(f"   Current lines: {current_lines}")
            
            # Check if it meets compliance
            if current_lines <= 500:
                print("   ✅ COMPLIANT - Under 500 line limit")
            else:
                print("   ❌ NON-COMPLIANT - Over 500 line limit")
    
    # Check extracted modules exist
    print(f"\n🔧 EXTRACTED MODULES CHECK")
    print("=" * 30)
    
    extracted_modules = [
        "src/core/messaging/router.py",
        "src/core/messaging/validator.py", 
        "src/core/messaging/formatter.py",
        "src/core/messaging/storage.py",
        "src/autonomous_development/workflow/engine.py",
        "src/autonomous_development/tasks/manager.py",
        "src/autonomous_development/code/generator.py",
        "src/autonomous_development/testing/orchestrator.py"
    ]
    
    for module_path in extracted_modules:
        if os.path.exists(module_path):
            lines = check_file_line_count(module_path)
            print(f"   ✅ {module_path} - {lines} lines")
        else:
            print(f"   ❌ {module_path} - NOT FOUND")
    
    # Check __init__.py files
    print(f"\n📦 PACKAGE INIT FILES")
    print("=" * 25)
    
    init_files = [
        "src/core/messaging/__init__.py",
        "src/autonomous_development/__init__.py"
    ]
    
    for init_file in init_files:
        if os.path.exists(init_file):
            print(f"   ✅ {init_file}")
        else:
            print(f"   ❌ {init_file} - MISSING")
    
    print(f"\n🎯 COMPLIANCE CHECK COMPLETE")

if __name__ == "__main__":
    main()
