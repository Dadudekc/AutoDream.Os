#!/usr/bin/env python3
"""
Refactor Analyzer - Smart Refactoring Suggestions
=================================================

Analyzes files and suggests optimal refactoring strategies.
Based on experience with swarm systems refactoring.

Author: Agent-8 (Quality Assurance) - Thread Experience Tool
Created: 2025-10-14
"""

import argparse
import ast
import sys
from pathlib import Path
from typing import List, Dict


def analyze_file(file_path: Path) -> Dict:
    """Analyze a file for refactoring opportunities."""
    analysis = {
        "file": str(file_path),
        "total_lines": 0,
        "functions": [],
        "classes": [],
        "imports": [],
        "suggestions": []
    }
    
    try:
        content = file_path.read_text(encoding='utf-8')
        analysis["total_lines"] = len(content.split('\n'))
        
        tree = ast.parse(content)
        
        # Analyze functions and classes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                lines = node.end_lineno - node.lineno + 1
                analysis["functions"].append({
                    "name": node.name,
                    "lines": lines,
                    "private": node.name.startswith('_'),
                    "start": node.lineno
                })
            
            elif isinstance(node, ast.ClassDef) and node.col_offset == 0:
                lines = node.end_lineno - node.lineno + 1
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                analysis["classes"].append({
                    "name": node.name,
                    "lines": lines,
                    "methods": len(methods),
                    "start": node.lineno
                })
            
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.ImportFrom):
                    analysis["imports"].append(f"from {node.module} import ...")
                else:
                    for alias in node.names:
                        analysis["imports"].append(f"import {alias.name}")
        
    except Exception as e:
        analysis["error"] = str(e)
        return analysis
    
    # Generate suggestions
    if analysis["total_lines"] > 400:
        total = analysis["total_lines"]
        analysis["suggestions"].append({
            "priority": "CRITICAL" if total > 600 else "MAJOR",
            "type": "file_size",
            "message": f"File has {total} lines (target: ≤400)"
        })
        
        # Suggest function extraction
        large_functions = [f for f in analysis["functions"] if f["lines"] > 30 and f["private"]]
        if large_functions:
            analysis["suggestions"].append({
                "priority": "HIGH",
                "type": "extract_functions",
                "message": f"Extract {len(large_functions)} large private functions",
                "candidates": [f["name"] for f in large_functions[:3]]
            })
        
        # Suggest scanner/helper extraction
        scanner_funcs = [f for f in analysis["functions"] if "scan" in f["name"].lower() or "check" in f["name"].lower()]
        if len(scanner_funcs) > 3:
            analysis["suggestions"].append({
                "priority": "HIGH",
                "type": "extract_scanners",
                "message": f"Extract {len(scanner_funcs)} scanner functions to separate module",
                "candidates": [f["name"] for f in scanner_funcs]
            })
    
    return analysis


def print_report(analysis: Dict):
    """Print analysis report."""
    print(f"\n🔍 REFACTOR ANALYSIS: {analysis['file']}")
    print("="*80)
    
    print(f"\n📊 METRICS:")
    print(f"   Total Lines: {analysis['total_lines']}")
    print(f"   Functions: {len(analysis['functions'])}")
    print(f"   Classes: {len(analysis['classes'])}")
    print(f"   Imports: {len(analysis['imports'])}")
    
    # V2 Compliance
    status = "✅ COMPLIANT" if analysis['total_lines'] <= 400 else "⚠️ VIOLATION"
    print(f"\n   V2 Status: {status}")
    
    if analysis.get("suggestions"):
        print(f"\n💡 REFACTORING SUGGESTIONS ({len(analysis['suggestions'])}):")
        for i, sug in enumerate(analysis['suggestions'], 1):
            print(f"\n   {i}. [{sug['priority']}] {sug['type'].upper()}")
            print(f"      {sug['message']}")
            if sug.get('candidates'):
                print(f"      Candidates: {', '.join(sug['candidates'][:5])}")
    else:
        print(f"\n✅ NO REFACTORING NEEDED - File is well-structured!")
    
    print("="*80 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Refactor Analyzer - Smart refactoring suggestions"
    )
    parser.add_argument("file", help="Python file to analyze")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: {args.file} not found")
        return 1
    
    analysis = analyze_file(file_path)
    
    if args.json:
        import json
        print(json.dumps(analysis, indent=2))
    else:
        print_report(analysis)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

