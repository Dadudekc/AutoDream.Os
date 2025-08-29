#!/usr/bin/env python3
"""
DUPLICATION ANALYSIS & CLEANUP SCRIPT
Captain Agent-3: Addressing Critical Duplication Issues in AI/ML Core
"""

import os
import json
import hashlib
from pathlib import Path
from collections import defaultdict

def analyze_file_content(file_path):
    """Analyze file content for duplication patterns"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments and whitespace for comparison
        lines = [line.strip() for line in content.split('\n') 
                if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('"""')]
        
        return {
            'path': str(file_path),
            'size': len(content),
            'lines': len(lines),
            'content_hash': hashlib.md5(content.encode()).hexdigest(),
            'function_names': extract_function_names(content),
            'class_names': extract_class_names(content)
        }
    except Exception as e:
        return {'path': str(file_path), 'error': str(e)}

def extract_function_names(content):
    """Extract function names from Python code"""
    import re
    function_pattern = r'def\s+(\w+)\s*\('
    return re.findall(function_pattern, content)

def extract_class_names(content):
    """Extract class names from Python code"""
    class_pattern = r'class\s+(\w+)'
    return re.findall(class_pattern, content)

def find_duplications(ai_ml_path):
    """Find duplication patterns in AI/ML core"""
    print("🔍 ANALYZING AI/ML CORE FOR DUPLICATIONS...")
    print("=" * 60)
    
    files = []
    for file_path in Path(ai_ml_path).rglob("*.py"):
        if file_path.is_file():
            analysis = analyze_file_content(file_path)
            files.append(analysis)
    
    # Find duplicate content hashes
    content_hashes = defaultdict(list)
    for file_info in files:
        if 'content_hash' in file_info:
            content_hashes[file_info['content_hash']].append(file_info['path'])
    
    # Find duplicate function names
    function_names = defaultdict(list)
    for file_info in files:
        if 'function_names' in file_info:
            for func_name in file_info['function_names']:
                function_names[func_name].append(file_info['path'])
    
    # Find duplicate class names
    class_names = defaultdict(list)
    for file_info in files:
        if 'class_names' in file_info:
            for class_name in file_info['class_names']:
                class_names[class_name].append(file_info['path'])
    
    # Find similar file names
    file_names = defaultdict(list)
    for file_info in files:
        if 'path' in file_info:
            filename = Path(file_info['path']).name
            file_names[filename].append(file_info['path'])
    
    return {
        'total_files': len(files),
        'duplicate_content': {k: v for k, v in content_hashes.items() if len(v) > 1},
        'duplicate_functions': {k: v for k, v in function_names.items() if len(v) > 1},
        'duplicate_classes': {k: v for k, v in class_names.items() if len(v) > 1},
        'duplicate_filenames': {k: v for k, v in file_names.items() if len(v) > 1}
    }

def generate_cleanup_plan(duplication_data):
    """Generate cleanup plan based on duplication analysis"""
    print("\n📋 DUPLICATION CLEANUP PLAN")
    print("=" * 60)
    
    plan = {
        'critical_issues': [],
        'moderate_issues': [],
        'minor_issues': [],
        'recommendations': []
    }
    
    # Critical: Exact content duplicates
    if duplication_data['duplicate_content']:
        plan['critical_issues'].append({
            'type': 'EXACT_CONTENT_DUPLICATES',
            'description': f"Found {len(duplication_data['duplicate_content'])} files with identical content",
            'files': duplication_data['duplicate_content']
        })
    
    # Critical: Duplicate class names
    if duplication_data['duplicate_classes']:
        plan['critical_issues'].append({
            'type': 'DUPLICATE_CLASS_NAMES',
            'description': f"Found {len(duplication_data['duplicate_classes'])} classes with duplicate names",
            'classes': duplication_data['duplicate_classes']
        })
    
    # Moderate: Duplicate function names
    if duplication_data['duplicate_functions']:
        plan['moderate_issues'].append({
            'type': 'DUPLICATE_FUNCTION_NAMES',
            'description': f"Found {len(duplication_data['duplicate_functions'])} functions with duplicate names",
            'functions': duplication_data['duplicate_functions']
        })
    
    # Moderate: Similar file names
    if duplication_data['duplicate_filenames']:
        plan['moderate_issues'].append({
            'type': 'SIMILAR_FILENAMES',
            'description': f"Found {len(duplication_data['duplicate_filenames'])} files with similar names",
            'files': duplication_data['duplicate_filenames']
        })
    
    # Recommendations
    plan['recommendations'] = [
        "Implement proper modular architecture with clear separation of concerns",
        "Create unified interfaces for common functionality",
        "Consolidate duplicate managers into single, well-defined modules",
        "Establish naming conventions to prevent future duplication",
        "Implement automated duplication detection in CI/CD pipeline"
    ]
    
    return plan

def print_duplication_report(duplication_data, cleanup_plan):
    """Print comprehensive duplication report"""
    print("\n📊 DUPLICATION ANALYSIS REPORT")
    print("=" * 60)
    print(f"Total AI/ML Core Files: {duplication_data['total_files']}")
    
    if cleanup_plan['critical_issues']:
        print("\n🚨 CRITICAL ISSUES:")
        for issue in cleanup_plan['critical_issues']:
            print(f"  • {issue['description']}")
            if 'files' in issue:
                for hash_val, file_list in list(issue['files'].items())[:3]:  # Show first 3
                    print(f"    - {len(file_list)} duplicate files")
                    for file_path in file_list[:2]:  # Show first 2 files
                        print(f"      {file_path}")
    
    if cleanup_plan['moderate_issues']:
        print("\n⚠️  MODERATE ISSUES:")
        for issue in cleanup_plan['moderate_issues']:
            print(f"  • {issue['description']}")
    
    print("\n💡 RECOMMENDATIONS:")
    for rec in cleanup_plan['recommendations']:
        print(f"  • {rec}")

def main():
    """Main duplication analysis and cleanup execution"""
    print("🏆 CAPTAIN AGENT-3: DUPLICATION ANALYSIS & CLEANUP EXCELLENCE 🏆")
    print("=" * 70)
    
    ai_ml_path = "src/ai_ml"
    
    if not os.path.exists(ai_ml_path):
        print(f"❌ AI/ML path not found: {ai_ml_path}")
        return False
    
    # Analyze duplications
    duplication_data = find_duplications(ai_ml_path)
    
    # Generate cleanup plan
    cleanup_plan = generate_cleanup_plan(duplication_data)
    
    # Print report
    print_duplication_report(duplication_data, cleanup_plan)
    
    # Save detailed report
    report = {
        'timestamp': '2025-08-28T22:10:00.000000Z',
        'captain_agent': 'Agent-3',
        'duplication_analysis': duplication_data,
        'cleanup_plan': cleanup_plan,
        'status': 'ANALYSIS_COMPLETE'
    }
    
    timestamp = '20250828_221000'
    filename = f"DUPLICATION_ANALYSIS_REPORT_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Detailed report saved: {filename}")
    print("\n🎯 NEXT STEPS:")
    print("  1. Review critical duplication issues")
    print("  2. Implement cleanup plan")
    print("  3. Restructure AI/ML core with proper modularization")
    print("  4. Establish duplication prevention protocols")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Duplication Analysis: COMPLETE")
    else:
        print("\n❌ Duplication Analysis: FAILED")
