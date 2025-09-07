#!/usr/bin/env python3
"""
Simple V2 Compliance Checker
Quick check of current compliance status
"""
import os

def check_compliance():
    """Check current V2 compliance status"""
    print("🔍 V2 COMPLIANCE STATUS CHECK")
    print("=" * 50)
    
    total_files = 0
    compliant_files = 0
    violations = []
    
    # Scan for Python files
    for root, dirs, files in os.walk('.'):
        if 'backups' in root or '__pycache__' in root or '.git' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                total_files += 1
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        line_count = len(lines)
                        
                        if line_count <= 250:  # V2 compliant
                            compliant_files += 1
                        else:
                            violations.append((file_path, line_count))
                except Exception as e:
                    continue
    
    # Calculate compliance percentage
    compliance_percentage = (compliant_files / total_files * 100) if total_files > 0 else 0
    
    print(f"📊 Total Python Files: {total_files}")
    print(f"✅ Compliant Files: {compliant_files}")
    print(f"🚨 Violation Files: {len(violations)}")
    print(f"🎯 Overall Compliance: {compliance_percentage:.1f}%")
    
    if violations:
        print(f"\n🚨 Violations Found:")
        for file_path, line_count in violations[:10]:  # Show first 10
            print(f"  - {file_path} ({line_count} lines)")
        if len(violations) > 10:
            print(f"  ... and {len(violations) - 10} more")
    else:
        print("\n🎉 100% V2 COMPLIANCE ACHIEVED!")
    
    return compliance_percentage

if __name__ == "__main__":
    check_compliance()
