#!/usr/bin/env python3
"""
Validation Duplicates Scanner - Agent-5
Scans Files 61-123 for validation function duplicates
"""

from pathlib import Path
import re
from collections import defaultdict

def scan_validation_duplicates():
    """Scan all Python files for validation function duplicates."""
    
    # Get all Python files
    all_files = sorted(Path('src').rglob('*.py'))
    
    # Extract validation functions
    validation_data = {}
    
    for filepath in all_files:
        try:
            content = filepath.read_text(encoding='utf-8')
            
            # Find all validation functions
            validate_funcs = re.findall(r'def (validate_?\w+)\(', content)
            
            if validate_funcs:
                validation_data[str(filepath)] = {
                    'count': len(validate_funcs),
                    'functions': validate_funcs,
                    'file_size': len(content.split('\n'))
                }
        except Exception as e:
            pass
    
    # Sort by count
    sorted_files = sorted(validation_data.items(), key=lambda x: x[1]['count'], reverse=True)
    
    # Print results
    print("=" * 80)
    print("VALIDATION DUPLICATES SCAN - AGENT-5")
    print("=" * 80)
    print(f"\nTotal files with validation functions: {len(validation_data)}")
    print(f"Total validation functions found: {sum(d['count'] for d in validation_data.values())}")
    
    print("\n📊 TOP 30 FILES BY VALIDATION COUNT:")
    print("-" * 80)
    
    for i, (filepath, data) in enumerate(sorted_files[:30], 1):
        print(f"\n{i}. {filepath}")
        print(f"   Count: {data['count']} functions")
        print(f"   Size: {data['file_size']} lines")
        print(f"   Functions: {', '.join(data['functions'][:5])}")
        if len(data['functions']) > 5:
            print(f"              ... and {len(data['functions']) - 5} more")
    
    # Group by pattern
    print("\n\n📋 FUNCTION PATTERNS:")
    print("-" * 80)
    
    all_functions = []
    for data in validation_data.values():
        all_functions.extend(data['functions'])
    
    # Count duplicates
    function_counts = defaultdict(int)
    for func in all_functions:
        function_counts[func] += 1
    
    duplicates = [(func, count) for func, count in function_counts.items() if count > 1]
    duplicates.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nDuplicate validation functions (appears >1 file):")
    for i, (func, count) in enumerate(duplicates[:20], 1):
        print(f"{i}. {func}: {count} occurrences")
    
    print(f"\n✅ Scan complete! Found {len(duplicates)} duplicate validation patterns!")
    print("=" * 80)
    
    return validation_data, duplicates

if __name__ == '__main__':
    scan_validation_duplicates()

