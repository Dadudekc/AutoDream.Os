#!/usr/bin/env python3
"""
Quick Broken Tools Audit - Fast Syntax-Only Check
=================================================

Quickly identifies tools with syntax errors or obvious import issues.
Fast execution for immediate quarantine decisions.

USAGE:
    python tools/quick_broken_tools_audit.py
"""

import ast
import sys
from pathlib import Path
from collections import defaultdict


def check_syntax(file_path: Path) -> tuple[bool, str]:
    """Quick syntax check"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            ast.parse(f.read())
        return True, ""
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)[:100]


def audit_tools():
    """Quick audit of tools directory"""
    tools_dir = Path("tools")
    tools_v2_dir = Path("tools_v2")
    
    results = defaultdict(list)
    
    print("\n🔍 QUICK BROKEN TOOLS AUDIT\n" + "="*70)
    
    # Audit both directories
    for directory in [tools_dir, tools_v2_dir]:
        if not directory.exists():
            continue
        
        print(f"\nAuditing: {directory}/")
        files = list(directory.rglob("*.py"))
        files = [f for f in files if '__pycache__' not in str(f)]
        
        for file_path in files:
            ok, error = check_syntax(file_path)
            rel_path = str(file_path)
            
            if ok:
                results['working'].append(rel_path)
            else:
                results['broken'].append((rel_path, error))
                print(f"  ❌ {file_path.name}: {error[:50]}")
    
    return results


def main():
    results = audit_tools()
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    working = len(results['working'])
    broken = len(results['broken'])
    total = working + broken
    
    print(f"Total: {total}")
    print(f"✅ Working: {working} ({working/total*100:.1f}%)")
    print(f"❌ Broken: {broken} ({broken/total*100:.1f}%)\n")
    
    if broken > 0:
        print(f"Broken tools:")
        for file_path, error in results['broken']:
            print(f"  - {file_path}")
            print(f"    Error: {error[:80]}")
    
    # Save to file
    with open("BROKEN_TOOLS_QUICK_AUDIT.txt", 'w') as f:
        f.write(f"BROKEN TOOLS QUICK AUDIT\n")
        f.write(f"Date: {Path('').absolute()}\n")
        f.write(f"Total: {total}, Working: {working}, Broken: {broken}\n\n")
        f.write("BROKEN TOOLS:\n")
        for file_path, error in results['broken']:
            f.write(f"\n{file_path}\n")
            f.write(f"  Error: {error}\n")
    
    print(f"\n✅ Saved to: BROKEN_TOOLS_QUICK_AUDIT.txt")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

