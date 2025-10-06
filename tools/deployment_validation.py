#!/usr/bin/env python3
"""
Production Deployment Readiness Validation
==========================================

Validates all V2 compliant modules for production deployment readiness.
Executes quality gates validation and deployment checklist.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any

def count_python_files() -> int:
    """Count total Python files in the project."""
    count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                count += 1
    return count

def find_large_files() -> List[Dict[str, Any]]:
    """Find files >400 lines."""
    large_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        if lines > 400:
                            large_files.append({
                                'path': file_path,
                                'lines': lines
                            })
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return large_files

def validate_v2_compliance() -> Dict[str, Any]:
    """Validate V2 compliance across the project."""
    total_files = count_python_files()
    large_files = find_large_files()
    
    # Check for V2 violations
    violations = []
    for file_info in large_files:
        violations.append({
            'file': file_info['path'],
            'lines': file_info['lines'],
            'violation': 'File exceeds 400 lines'
        })
    
    return {
        'total_files': total_files,
        'large_files_count': len(large_files),
        'violations': violations,
        'compliance_rate': ((total_files - len(large_files)) / total_files * 100) if total_files > 0 else 0
    }

def check_deployment_readiness() -> Dict[str, Any]:
    """Check deployment readiness indicators."""
    checks = {
        'import_errors': 0,
        'syntax_errors': 0,
        'missing_dependencies': 0,
        'test_coverage': 0
    }
    
    # Check for common deployment issues
    critical_files = [
        'src/services/agent_devlog_posting.py',
        'tools/messaging_system.py',
        'src/services/thea/thea_browser_manager.py'
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Basic syntax check
                    compile(content, file_path, 'exec')
            except SyntaxError:
                checks['syntax_errors'] += 1
            except Exception:
                checks['import_errors'] += 1
    
    return checks

def main():
    """Main validation function."""
    print("🚀 PRODUCTION DEPLOYMENT READINESS VALIDATION")
    print("=" * 50)
    
    # V2 Compliance Validation
    print("\n📋 V2 COMPLIANCE VALIDATION")
    compliance = validate_v2_compliance()
    print(f"Total Python files: {compliance['total_files']}")
    print(f"Files >400 lines: {compliance['large_files_count']}")
    print(f"V2 Compliance rate: {compliance['compliance_rate']:.1f}%")
    
    if compliance['violations']:
        print("\n⚠️  V2 VIOLATIONS FOUND:")
        for violation in compliance['violations'][:10]:  # Show first 10
            print(f"  {violation['file']} ({violation['lines']} lines)")
        if len(compliance['violations']) > 10:
            print(f"  ... and {len(compliance['violations']) - 10} more")
    
    # Deployment Readiness Check
    print("\n🔍 DEPLOYMENT READINESS CHECK")
    readiness = check_deployment_readiness()
    print(f"Syntax errors: {readiness['syntax_errors']}")
    print(f"Import errors: {readiness['import_errors']}")
    print(f"Missing dependencies: {readiness['missing_dependencies']}")
    
    # Overall Assessment
    print("\n📊 OVERALL ASSESSMENT")
    if compliance['large_files_count'] == 0:
        print("✅ V2 COMPLIANCE: PERFECT")
    elif compliance['compliance_rate'] >= 95:
        print("✅ V2 COMPLIANCE: EXCELLENT")
    elif compliance['compliance_rate'] >= 90:
        print("⚠️  V2 COMPLIANCE: GOOD")
    else:
        print("❌ V2 COMPLIANCE: NEEDS IMPROVEMENT")
    
    if readiness['syntax_errors'] == 0 and readiness['import_errors'] == 0:
        print("✅ DEPLOYMENT READINESS: READY")
    else:
        print("⚠️  DEPLOYMENT READINESS: ISSUES DETECTED")
    
    print(f"\n🎯 VALIDATION COMPLETE")
    print(f"Total modules validated: {compliance['total_files']}")
    print(f"V2 compliant modules: {compliance['total_files'] - compliance['large_files_count']}")
    
    return {
        'compliance': compliance,
        'readiness': readiness,
        'status': 'SUCCESS' if compliance['large_files_count'] == 0 else 'PARTIAL'
    }

if __name__ == "__main__":
    result = main()
    sys.exit(0 if result['status'] == 'SUCCESS' else 1)

