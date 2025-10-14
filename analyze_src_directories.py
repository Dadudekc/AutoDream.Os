#!/usr/bin/env python3
"""
Comprehensive Source Directory Analysis Tool
Analyzes src/ and services/ directories and generates detailed reports.

V2 COMPLIANT: Refactored to ≤400 lines by extracting:
- File analyzers → src_directory_analyzers.py
- Report generation → src_directory_report_generator.py
"""

import os
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict, Counter

from src_directory_analyzers import analyze_file
from src_directory_report_generator import save_analysis_results, print_analysis_summary


def get_directory_structure(root_path: str, max_depth: int = 3) -> Dict[str, Any]:
    """Get directory structure with file counts."""
    structure = {}
    total_files = 0
    total_dirs = 0
    
    for root, dirs, files in os.walk(root_path):
        rel_path = os.path.relpath(root, root_path)
        if rel_path == '.':
            rel_path = ''
        
        file_counts = Counter(Path(f).suffix.lower() for f in files)
        
        structure[rel_path or '.'] = {
            "files": file_counts,
            "file_count": len(files),
            "subdirs": len(dirs),
            "total_files": len(files)
        }
        
        total_files += len(files)
        total_dirs += len(dirs)
        
        if root.count(os.sep) - root_path.count(os.sep) >= max_depth:
            dirs[:] = []
    
    return {
        "structure": structure,
        "total_files": total_files,
        "total_dirs": total_dirs
    }


def analyze_directories(directories: List[str]) -> Dict[str, Any]:
    """Analyze multiple directories comprehensively."""
    all_analysis = {}
    total_files = 0
    total_lines = 0
    total_functions = 0
    total_classes = 0
    total_imports = 0
    file_types = Counter()
    complexity_by_type = defaultdict(list)
    imports_by_file = defaultdict(list)
    
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            continue
            
        print(f"Analyzing directory: {directory}")
        directory_analysis = {}
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                
                print(f"  Analyzing: {rel_path}")
                analysis = analyze_file(file_path)
                directory_analysis[rel_path] = analysis
                
                total_files += 1
                total_lines += analysis.get('line_count', 0)
                total_functions += analysis.get('function_count', 0)
                total_classes += analysis.get('class_count', 0)
                total_imports += analysis.get('import_count', 0)
                
                file_type = analysis.get('language', 'unknown')
                file_types[file_type] += 1
                
                complexity_by_type[file_type].append(analysis.get('complexity', 0))
                
                if analysis.get('imports'):
                    imports_by_file[rel_path] = analysis['imports']
        
        all_analysis[directory] = directory_analysis
    
    avg_complexity_by_type = {}
    for file_type, complexities in complexity_by_type.items():
        avg_complexity_by_type[file_type] = sum(complexities) / len(complexities) if complexities else 0
    
    return {
        "directories": all_analysis,
        "summary": {
            "total_files": total_files,
            "total_lines": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "total_imports": total_imports,
            "file_types": dict(file_types),
            "avg_complexity_by_type": avg_complexity_by_type,
            "total_directories": len(directories)
        },
        "imports_analysis": dict(imports_by_file)
    }


def main():
    """Main analysis function."""
    directories_to_analyze = ["src", "src/services"]
    
    print("🔍 Starting comprehensive source directory analysis...")
    
    analysis_results = analyze_directories(directories_to_analyze)
    
    directory_structures = {}
    for directory in directories_to_analyze:
        if os.path.exists(directory):
            directory_structures[directory] = get_directory_structure(directory)
    
    save_analysis_results(analysis_results, directory_structures, directories_to_analyze)
    print_analysis_summary(analysis_results)


if __name__ == "__main__":
    main()
