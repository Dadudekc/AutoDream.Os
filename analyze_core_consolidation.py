#!/usr/bin/env python3
"""
Core Directory Consolidation Analysis - Chunk 001
================================================

Analyzes src/core directory for consolidation opportunities.
Target: 358 → ~107 files (70% reduction)

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import ast
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple


def analyze_python_file(file_path: str) -> Dict[str, Any]:
    """Analyze a Python file and extract metadata."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Parse AST
        tree = ast.parse(content)

        functions = []
        classes = {}
        imports = []
        lines_of_code = len(content.splitlines())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                classes[node.name] = {
                    "methods": methods,
                    "line_count": len(node.body)
                }
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                else:
                    module = node.module or ""
                    imports.extend([f"{module}.{alias.name}" for alias in node.names])

        return {
            "file_path": file_path,
            "relative_path": str(Path(file_path).relative_to("src/core")),
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "line_count": lines_of_code,
            "complexity": len(functions) + len(classes),
            "file_size": os.path.getsize(file_path),
            "is_main_module": "__main__" in content,
            "has_tests": "test" in file_path.lower() or "Test" in content
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "relative_path": str(Path(file_path).relative_to("src/core")),
            "functions": [],
            "classes": {},
            "imports": [],
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "is_main_module": False,
            "has_tests": False,
            "error": str(e)
        }


def categorize_file(file_path: str, analysis: Dict[str, Any]) -> str:
    """Categorize a file based on its path and content."""
    relative_path = analysis.get("relative_path", "")
    
    # Main categories
    if "analytics" in relative_path:
        return "analytics"
    elif "coordination" in relative_path or "coordinator" in relative_path:
        return "coordination"
    elif "engine" in relative_path.lower():
        return "engines"
    elif "manager" in relative_path.lower():
        return "managers"
    elif "validation" in relative_path:
        return "validation"
    elif "error_handling" in relative_path or "error" in relative_path:
        return "error_handling"
    elif "messaging" in relative_path:
        return "messaging"
    elif "fsm" in relative_path.lower():
        return "fsm"
    elif "performance" in relative_path:
        return "performance"
    elif "integration" in relative_path:
        return "integration"
    elif "orchestration" in relative_path:
        return "orchestration"
    elif "refactoring" in relative_path:
        return "refactoring"
    elif "deployment" in relative_path:
        return "deployment"
    elif "emergency" in relative_path:
        return "emergency"
    elif "data_optimization" in relative_path:
        return "data_optimization"
    elif "dry_eliminator" in relative_path:
        return "dry_elimination"
    elif "file_locking" in relative_path:
        return "file_locking"
    elif "import_system" in relative_path:
        return "import_system"
    elif "pattern_analysis" in relative_path:
        return "pattern_analysis"
    elif "vector" in relative_path:
        return "vector"
    elif "ssot" in relative_path:
        return "ssot"
    elif "unified" in relative_path:
        return "unified_systems"
    elif "utils" in relative_path:
        return "utilities"
    elif "constants" in relative_path:
        return "constants"
    elif "config" in relative_path:
        return "configuration"
    else:
        return "core"


def find_consolidation_opportunities(analyses: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Find consolidation opportunities by category."""
    categorized = {}
    
    for analysis in analyses:
        category = categorize_file(analysis["file_path"], analysis)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(analysis)
    
    # Sort by complexity and size for consolidation prioritization
    for category in categorized:
        categorized[category].sort(key=lambda x: (x["complexity"], x["line_count"]), reverse=True)
    
    return categorized


def generate_consolidation_plan(categorized: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Generate consolidation plan with specific recommendations."""
    plan = {
        "consolidation_targets": {},
        "high_priority_consolidations": [],
        "low_priority_consolidations": [],
        "preserve_as_is": [],
        "total_files": sum(len(files) for files in categorized.values()),
        "target_reduction": 0.70
    }
    
    for category, files in categorized.items():
        file_count = len(files)
        target_count = max(1, int(file_count * (1 - plan["target_reduction"])))
        
        # Calculate consolidation ratio
        consolidation_ratio = file_count / target_count if target_count > 0 else 1
        
        plan["consolidation_targets"][category] = {
            "current_files": file_count,
            "target_files": target_count,
            "reduction_percentage": round((1 - target_count / file_count) * 100, 1),
            "consolidation_ratio": round(consolidation_ratio, 1),
            "files": files
        }
        
        # Prioritize consolidations
        if file_count > 10 and consolidation_ratio > 2:
            plan["high_priority_consolidations"].append({
                "category": category,
                "files": file_count,
                "target": target_count,
                "ratio": consolidation_ratio
            })
        elif file_count > 5:
            plan["low_priority_consolidations"].append({
                "category": category,
                "files": file_count,
                "target": target_count,
                "ratio": consolidation_ratio
            })
        else:
            plan["preserve_as_is"].append({
                "category": category,
                "files": file_count
            })
    
    return plan


def main():
    """Main analysis function."""
    print("🔍 Analyzing src/core directory for consolidation opportunities...")
    
    # Find all Python files in src/core
    core_files = []
    for root, dirs, files in os.walk("src/core"):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                core_files.append(file_path)
    
    print(f"📊 Found {len(core_files)} Python files in src/core")
    
    # Analyze each file
    analyses = []
    for file_path in core_files:
        print(f"Analyzing: {file_path}")
        analysis = analyze_python_file(file_path)
        analyses.append(analysis)
    
    # Categorize files
    categorized = find_consolidation_opportunities(analyses)
    
    # Generate consolidation plan
    plan = generate_consolidation_plan(categorized)
    
    # Print summary
    print(f"\n📋 CONSOLIDATION ANALYSIS SUMMARY:")
    print(f"   Total files: {plan['total_files']}")
    print(f"   Target reduction: {plan['target_reduction']*100}%")
    print(f"   Target files: {int(plan['total_files'] * (1 - plan['target_reduction']))}")
    
    print(f"\n🎯 HIGH PRIORITY CONSOLIDATIONS:")
    for item in plan["high_priority_consolidations"]:
        print(f"   {item['category']}: {item['files']} → {item['target']} files (ratio: {item['ratio']:.1f})")
    
    print(f"\n📝 LOW PRIORITY CONSOLIDATIONS:")
    for item in plan["low_priority_consolidations"]:
        print(f"   {item['category']}: {item['files']} → {item['target']} files (ratio: {item['ratio']:.1f})")
    
    print(f"\n✅ PRESERVE AS IS:")
    for item in plan["preserve_as_is"]:
        print(f"   {item['category']}: {item['files']} files")
    
    # Save detailed analysis
    with open("core_consolidation_analysis.json", "w", encoding="utf-8") as f:
        json.dump({
            "plan": plan,
            "categorized_files": categorized,
            "individual_analyses": analyses
        }, f, indent=2)
    
    print(f"\n📁 Detailed analysis saved: core_consolidation_analysis.json")
    
    return plan


if __name__ == "__main__":
    exit_code = main()
    print()  
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    exit(exit_code)
