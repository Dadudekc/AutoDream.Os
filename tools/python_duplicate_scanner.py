#!/usr/bin/env python3
"""
Python Duplicate Scanner Tool
============================

Scans Python files for duplicate content and consolidation opportunities.

Author: Agent-4 (Captain)
License: MIT
V2 Compliance: ≤400 lines, modular design
"""

import argparse
import ast
import hashlib
import sys
from pathlib import Path
from typing import Dict, List, Set, Any

ROOT = Path(__file__).resolve().parents[1]


def normalize_python_content(content: str) -> str:
    """Normalize Python content for comparison"""
    try:
        # Parse AST and convert back to string (normalizes formatting)
        tree = ast.parse(content)
        normalized = ast.unparse(tree)
        
        # Remove imports and comments for better comparison
        lines = []
        for line in normalized.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('import') and not line.startswith('from'):
                lines.append(line)
        
        return '\n'.join(lines).strip()
    except SyntaxError:
        # If parsing fails, just normalize whitespace
        return ' '.join(content.split()).strip()


def extract_functions_and_classes(content: str) -> Dict[str, List[str]]:
    """Extract function and class definitions from Python content"""
    try:
        tree = ast.parse(content)
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        return {"functions": functions, "classes": classes}
    except SyntaxError:
        return {"functions": [], "classes": []}


def analyze_python_files() -> Dict[str, Any]:
    """Analyze Python files for duplicates and consolidation opportunities"""
    print("🔍 Scanning Python files for consolidation opportunities...")
    
    python_files = list(ROOT.rglob("*.py"))
    print(f"Found {len(python_files)} Python files")
    
    analysis = {
        "total_files": len(python_files),
        "content_duplicates": [],
        "function_duplicates": [],
        "class_duplicates": [],
        "small_files": [],
        "utility_files": [],
        "test_files": [],
        "service_files": [],
        "consolidation_candidates": []
    }
    
    content_hashes = {}
    function_registry = {}
    class_registry = {}
    
    for py_file in python_files:
        rel_path = str(py_file.relative_to(ROOT))
        
        try:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            file_size = py_file.stat().st_size
            
            # Normalize content and check for duplicates
            normalized_content = normalize_python_content(content)
            content_hash = hashlib.sha256(normalized_content.encode()).hexdigest()
            
            if content_hash in content_hashes:
                content_hashes[content_hash].append(rel_path)
            else:
                content_hashes[content_hash] = [rel_path]
            
            # Extract functions and classes
            code_analysis = extract_functions_and_classes(content)
            
            # Register functions
            for func_name in code_analysis["functions"]:
                if func_name not in function_registry:
                    function_registry[func_name] = []
                function_registry[func_name].append(rel_path)
            
            # Register classes
            for class_name in code_analysis["classes"]:
                if class_name not in class_registry:
                    class_registry[class_name] = []
                class_registry[class_name].append(rel_path)
            
            # Categorize files
            if file_size < 1000:  # Less than 1KB
                analysis["small_files"].append({
                    "path": rel_path,
                    "size": file_size
                })
            
            if "util" in rel_path.lower() or "helper" in rel_path.lower():
                analysis["utility_files"].append(rel_path)
            
            if "test" in rel_path.lower():
                analysis["test_files"].append(rel_path)
            
            if "service" in rel_path.lower():
                analysis["service_files"].append(rel_path)
            
            # Check for consolidation candidates
            if any(keyword in rel_path.lower() for keyword in ["duplicate", "copy", "backup", "old"]):
                analysis["consolidation_candidates"].append(rel_path)
                
        except Exception as e:
            print(f"Warning: Could not analyze {rel_path}: {e}")
    
    # Identify content duplicates
    for hash_val, files in content_hashes.items():
        if len(files) > 1:
            analysis["content_duplicates"].append(files)
    
    # Identify function duplicates
    for func_name, files in function_registry.items():
        if len(files) > 1:
            analysis["function_duplicates"].append({
                "function": func_name,
                "files": files
            })
    
    # Identify class duplicates
    for class_name, files in class_registry.items():
        if len(files) > 1:
            analysis["class_duplicates"].append({
                "class": class_name,
                "files": files
            })
    
    return analysis


def generate_python_report(analysis: Dict[str, Any]) -> None:
    """Generate Python consolidation report"""
    reports_dir = ROOT / "runtime" / "pass4" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    report_content = f"""# Python Consolidation Analysis

## Summary
- **Total Python files**: {analysis['total_files']}
- **Content duplicates**: {len(analysis['content_duplicates'])}
- **Function duplicates**: {len(analysis['function_duplicates'])}
- **Class duplicates**: {len(analysis['class_duplicates'])}
- **Small files (<1KB)**: {len(analysis['small_files'])}
- **Utility files**: {len(analysis['utility_files'])}
- **Test files**: {len(analysis['test_files'])}
- **Service files**: {len(analysis['service_files'])}
- **Consolidation candidates**: {len(analysis['consolidation_candidates'])}

## Content Duplicates
"""
    
    for i, dup_group in enumerate(analysis['content_duplicates'], 1):
        report_content += f"\n### Group {i} ({len(dup_group)} files)\n"
        for file_path in dup_group:
            report_content += f"- `{file_path}`\n"
        report_content += f"\n**Action**: Keep `{dup_group[0]}` (canonical), delete others\n"
    
    report_content += f"""
## Function Duplicates
"""
    for dup_info in analysis['function_duplicates'][:10]:  # Show first 10
        report_content += f"\n### Function: `{dup_info['function']}`\n"
        for file_path in dup_info['files']:
            report_content += f"- `{file_path}`\n"
    
    if len(analysis['function_duplicates']) > 10:
        report_content += f"\n... and {len(analysis['function_duplicates']) - 10} more function duplicates\n"
    
    report_content += f"""
## Class Duplicates
"""
    for dup_info in analysis['class_duplicates'][:10]:  # Show first 10
        report_content += f"\n### Class: `{dup_info['class']}`\n"
        for file_path in dup_info['files']:
            report_content += f"- `{file_path}`\n"
    
    if len(analysis['class_duplicates']) > 10:
        report_content += f"\n... and {len(analysis['class_duplicates']) - 10} more class duplicates\n"
    
    report_content += f"""
## Small Files ({len(analysis['small_files'])} files)
Files smaller than 1KB that could be merged:
"""
    for file_info in analysis['small_files'][:20]:  # Show first 20
        report_content += f"- `{file_info['path']}` ({file_info['size']} bytes)\n"
    if len(analysis['small_files']) > 20:
        report_content += f"- ... and {len(analysis['small_files']) - 20} more\n"
    
    report_content += f"""
## Consolidation Candidates ({len(analysis['consolidation_candidates'])} files)
Files that appear to be duplicates or backups:
"""
    for file_path in analysis['consolidation_candidates']:
        report_content += f"- `{file_path}`\n"
    
    report_content += """
## Recommended Actions

1. **Delete content duplicates** - Remove all but canonical versions
2. **Merge function duplicates** - Consolidate duplicate function implementations
3. **Merge class duplicates** - Consolidate duplicate class definitions
4. **Combine small files** - Merge small utility files
5. **Remove consolidation candidates** - Delete obvious duplicates/backups

## Target Reduction
- **Current**: 738 Python files
- **Target**: ~600 files (19% reduction)
- **Files to remove**: ~138 files
"""
    
    report_path = reports_dir / "python_consolidation_analysis.md"
    report_path.write_text(report_content, encoding="utf-8")
    
    # Save JSON data
    import json
    json_path = reports_dir / "python_analysis.json"
    json_path.write_text(json.dumps(analysis, indent=2, default=str), encoding="utf-8")
    
    print(f"📊 Python analysis complete:")
    print(f"   - Total files: {analysis['total_files']}")
    print(f"   - Content duplicates: {len(analysis['content_duplicates'])}")
    print(f"   - Function duplicates: {len(analysis['function_duplicates'])}")
    print(f"   - Class duplicates: {len(analysis['class_duplicates'])}")
    print(f"   - Report: {report_path}")


def consolidate_python_files(analysis: Dict[str, Any], dry_run: bool = True) -> None:
    """Consolidate Python files based on analysis"""
    if dry_run:
        print("🔍 DRY RUN - Python consolidation actions:")
    else:
        print("🗑️ APPLYING - Python consolidation:")
    
    deleted_count = 0
    
    # Delete content duplicates (keep first file as canonical)
    for dup_group in analysis['content_duplicates']:
        canonical = dup_group[0]
        duplicates = dup_group[1:]
        
        for dup_file in duplicates:
            file_path = ROOT / dup_file
            if file_path.exists():
                if dry_run:
                    print(f"  [DRY-RUN] Would delete content duplicate: {dup_file}")
                else:
                    file_path.unlink()
                    print(f"  🗑️ Deleted content duplicate: {dup_file}")
                deleted_count += 1
    
    # Delete consolidation candidates (obvious duplicates/backups)
    for file_path in analysis['consolidation_candidates']:
        full_path = ROOT / file_path
        if full_path.exists():
            if dry_run:
                print(f"  [DRY-RUN] Would delete consolidation candidate: {file_path}")
            else:
                full_path.unlink()
                print(f"  🗑️ Deleted consolidation candidate: {file_path}")
            deleted_count += 1
    
    # Delete very small files (likely empty or minimal)
    for file_info in analysis['small_files']:
        if file_info['size'] < 100:  # Less than 100 bytes
            file_path = ROOT / file_info['path']
            if file_path.exists():
                if dry_run:
                    print(f"  [DRY-RUN] Would delete very small file: {file_info['path']}")
                else:
                    file_path.unlink()
                    print(f"  🗑️ Deleted very small file: {file_info['path']}")
                deleted_count += 1
    
    print(f"📊 {'Would delete' if dry_run else 'Deleted'} {deleted_count} Python files")


def main():
    parser = argparse.ArgumentParser(description="Consolidate Python files")
    parser.add_argument("--apply", action="store_true", help="Apply consolidation (default is dry-run)")
    parser.add_argument("--report-only", action="store_true", help="Generate report only")
    
    args = parser.parse_args()
    
    # Create runtime directory
    (ROOT / "runtime" / "pass4" / "reports").mkdir(parents=True, exist_ok=True)
    
    # Analyze Python files
    analysis = analyze_python_files()
    
    # Generate report
    generate_python_report(analysis)
    
    if not args.report_only:
        # Apply consolidation
        consolidate_python_files(analysis, dry_run=not args.apply)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

