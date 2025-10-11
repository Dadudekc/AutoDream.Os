#!/usr/bin/env python3
"""
__init__.py Files Analysis Tool
===============================

Analyzes all __init__.py files in the project for consolidation planning.

Author: Agent-3 (Infrastructure & DevOps) - C-005
"""

import os
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import json


def analyze_init_files(root_dir: str = "src") -> Dict:
    """Analyze all __init__.py files in the directory."""
    
    init_files = []
    
    # Find all __init__.py files
    for root, dirs, files in os.walk(root_dir):
        if "__init__.py" in files:
            file_path = os.path.join(root, "__init__.py")
            init_files.append(file_path)
    
    print(f"📁 Found {len(init_files)} __init__.py files\n")
    
    # Analyze each file
    file_data = []
    content_hashes = defaultdict(list)
    
    for file_path in sorted(init_files):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        size = os.path.getsize(file_path)
        lines = len(content.splitlines())
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Analyze content
        is_empty = size == 0 or content.strip() == ""
        has_imports = "import " in content or "from " in content
        has_all = "__all__" in content
        has_comments_only = content.strip().startswith("#") and not has_imports
        
        data = {
            "path": file_path,
            "size": size,
            "lines": lines,
            "hash": content_hash,
            "is_empty": is_empty,
            "has_imports": has_imports,
            "has_all": has_all,
            "has_comments_only": has_comments_only,
            "content_preview": content[:200] if content else ""
        }
        
        file_data.append(data)
        content_hashes[content_hash].append(file_path)
    
    # Find duplicates
    duplicates = {h: paths for h, paths in content_hashes.items() if len(paths) > 1}
    
    # Categorize files
    empty_files = [f for f in file_data if f["is_empty"]]
    tiny_files = [f for f in file_data if f["size"] < 50 and not f["is_empty"]]
    simple_imports = [f for f in file_data if f["has_imports"] and not f["has_all"] and f["lines"] < 10]
    complex_files = [f for f in file_data if f["lines"] > 50]
    
    analysis = {
        "total_files": len(init_files),
        "file_data": file_data,
        "duplicates": duplicates,
        "categories": {
            "empty": len(empty_files),
            "tiny": len(tiny_files),
            "simple_imports": len(simple_imports),
            "complex": len(complex_files)
        },
        "empty_files": [f["path"] for f in empty_files],
        "tiny_files": [f["path"] for f in tiny_files],
        "complex_files": [f["path"] for f in complex_files]
    }
    
    return analysis


def print_analysis(analysis: Dict):
    """Print analysis results."""
    
    print("=" * 80)
    print("📊 __INIT__.PY FILES ANALYSIS")
    print("=" * 80)
    print()
    
    print(f"📁 Total Files: {analysis['total_files']}")
    print()
    
    print("📂 Categories:")
    print(f"  • Empty files: {analysis['categories']['empty']}")
    print(f"  • Tiny files (<50 bytes): {analysis['categories']['tiny']}")
    print(f"  • Simple imports (<10 lines): {analysis['categories']['simple_imports']}")
    print(f"  • Complex files (>50 lines): {analysis['categories']['complex']}")
    print()
    
    print(f"🔄 Duplicate Content Groups: {len(analysis['duplicates'])}")
    if analysis['duplicates']:
        print("\nDuplicate groups:")
        for i, (hash_val, paths) in enumerate(analysis['duplicates'].items(), 1):
            print(f"\n  Group {i}: {len(paths)} files with identical content")
            for path in paths:
                print(f"    - {path}")
    print()
    
    if analysis['complex_files']:
        print(f"📋 Complex Files (>50 lines): {len(analysis['complex_files'])}")
        for path in analysis['complex_files']:
            file_data = next(f for f in analysis['file_data'] if f['path'] == path)
            print(f"  • {path} ({file_data['lines']} lines)")
        print()
    
    # Consolidation potential
    total_removable = (
        analysis['categories']['empty'] + 
        len([p for group in analysis['duplicates'].values() for p in group[1:]]) +
        int(analysis['categories']['simple_imports'] * 0.7)  # Estimate 70% of simple imports can be consolidated
    )
    
    print("🎯 Consolidation Potential:")
    print(f"  • Current: {analysis['total_files']} files")
    print(f"  • Removable: ~{total_removable} files")
    print(f"  • Target: ~{analysis['total_files'] - total_removable} files")
    print(f"  • Reduction: ~{total_removable / analysis['total_files'] * 100:.1f}%")
    print()


def generate_consolidation_plan(analysis: Dict) -> Dict:
    """Generate consolidation plan."""
    
    plan = {
        "phase_1_remove_empty": analysis['empty_files'],
        "phase_2_remove_duplicates": [],
        "phase_3_consolidate_simple": [],
        "estimated_reduction": 0
    }
    
    # Phase 2: Remove duplicate files (keep one from each group)
    for hash_val, paths in analysis['duplicates'].items():
        # Keep the first file, remove the rest
        plan['phase_2_remove_duplicates'].extend(paths[1:])
    
    # Phase 3: Identify simple imports that can be consolidated
    simple_imports = [
        f for f in analysis['file_data'] 
        if f['has_imports'] and not f['has_all'] and f['lines'] < 10 and not f['is_empty']
    ]
    
    # Group by parent directory
    by_parent = defaultdict(list)
    for f in simple_imports:
        parent = str(Path(f['path']).parent.parent)
        by_parent[parent].append(f['path'])
    
    # Consolidate groups with 3+ simple imports
    for parent, paths in by_parent.items():
        if len(paths) >= 3:
            plan['phase_3_consolidate_simple'].extend(paths)
    
    total_removable = (
        len(plan['phase_1_remove_empty']) +
        len(plan['phase_2_remove_duplicates']) +
        int(len(plan['phase_3_consolidate_simple']) * 0.7)  # 70% of simple imports
    )
    
    plan['estimated_reduction'] = total_removable
    plan['target_files'] = analysis['total_files'] - total_removable
    plan['reduction_percentage'] = (total_removable / analysis['total_files'] * 100)
    
    return plan


def main():
    """Main execution."""
    
    print("🚀 Starting __init__.py files analysis...\n")
    
    # Analyze files
    analysis = analyze_init_files("src")
    
    # Print results
    print_analysis(analysis)
    
    # Generate consolidation plan
    plan = generate_consolidation_plan(analysis)
    
    print("=" * 80)
    print("📋 CONSOLIDATION PLAN")
    print("=" * 80)
    print()
    
    print(f"Phase 1: Remove Empty Files")
    print(f"  • Count: {len(plan['phase_1_remove_empty'])} files")
    if plan['phase_1_remove_empty'][:5]:
        print(f"  • Examples:")
        for path in plan['phase_1_remove_empty'][:5]:
            print(f"    - {path}")
        if len(plan['phase_1_remove_empty']) > 5:
            print(f"    ... and {len(plan['phase_1_remove_empty']) - 5} more")
    print()
    
    print(f"Phase 2: Remove Duplicate Files")
    print(f"  • Count: {len(plan['phase_2_remove_duplicates'])} files")
    if plan['phase_2_remove_duplicates'][:5]:
        print(f"  • Examples:")
        for path in plan['phase_2_remove_duplicates'][:5]:
            print(f"    - {path}")
        if len(plan['phase_2_remove_duplicates']) > 5:
            print(f"    ... and {len(plan['phase_2_remove_duplicates']) - 5} more")
    print()
    
    print(f"Phase 3: Consolidate Simple Imports")
    print(f"  • Count: ~{int(len(plan['phase_3_consolidate_simple']) * 0.7)} files (70% of {len(plan['phase_3_consolidate_simple'])})")
    print()
    
    print("📊 Summary:")
    print(f"  • Current: {analysis['total_files']} files")
    print(f"  • Target: ~{plan['target_files']} files")
    print(f"  • Reduction: ~{plan['estimated_reduction']} files ({plan['reduction_percentage']:.1f}%)")
    print()
    
    # Save analysis
    output_file = "docs/AGENT-3_INIT_FILES_ANALYSIS.json"
    with open(output_file, 'w') as f:
        json.dump({
            "analysis": analysis,
            "plan": plan
        }, f, indent=2)
    
    print(f"✅ Analysis saved to: {output_file}")
    print()
    print("🐝 WE ARE SWARM - Analysis complete!")


if __name__ == "__main__":
    main()

