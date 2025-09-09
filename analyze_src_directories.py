#!/usr/bin/env python3
"""
Comprehensive Source Directory Analysis Tool
Analyzes src/ and services/ directories and generates detailed reports.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Set
import ast
import re
from collections import defaultdict, Counter

def analyze_python_file(file_path: str) -> Dict[str, Any]:
    """Analyze a Python file and extract comprehensive metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse AST
        tree = ast.parse(content)
        
        functions = []
        classes = {}
        imports = []
        decorators = []
        docstrings = []
        complexity_indicators = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
                complexity_indicators += 1
                # Count nested structures for complexity
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                        complexity_indicators += 1
            elif isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                classes[node.name] = {
                    "methods": methods,
                    "line_count": len(node.body),
                    "base_classes": [base.id for base in node.bases if isinstance(base, ast.Name)]
                }
                complexity_indicators += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                else:
                    module = node.module or ""
                    imports.extend([f"{module}.{alias.name}" for alias in node.names])
            elif isinstance(node, ast.Decorator):
                if isinstance(node.decorator, ast.Name):
                    decorators.append(node.decorator.id)
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                if node.value.value.strip().startswith(('"""', "'''")):
                    docstrings.append(node.value.value.strip())
        
        # Calculate additional metrics
        lines = content.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        comment_lines = [line for line in lines if line.strip().startswith('#')]
        
        return {
            "language": ".py",
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "decorators": decorators,
            "docstrings": len(docstrings),
            "line_count": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "comment_lines": len(comment_lines),
            "complexity": complexity_indicators,
            "file_size": os.path.getsize(file_path),
            "import_count": len(imports),
            "function_count": len(functions),
            "class_count": len(classes)
        }
    except Exception as e:
        return {
            "language": ".py",
            "functions": [],
            "classes": {},
            "imports": [],
            "decorators": [],
            "docstrings": 0,
            "line_count": 0,
            "non_empty_lines": 0,
            "comment_lines": 0,
            "complexity": 0,
            "file_size": 0,
            "import_count": 0,
            "function_count": 0,
            "class_count": 0,
            "error": str(e)
        }

def analyze_js_file(file_path: str) -> Dict[str, Any]:
    """Analyze a JavaScript file and extract metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Enhanced regex-based analysis for JS
        functions = re.findall(r'function\s+(\w+)\s*\(', content)
        classes = re.findall(r'class\s+(\w+)', content)
        imports = re.findall(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', content)
        exports = re.findall(r'export\s+(?:default\s+)?(?:function\s+(\w+)|const\s+(\w+)|class\s+(\w+))', content)
        
        lines = content.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        comment_lines = [line for line in lines if line.strip().startswith(('//', '/*', '*'))]
        
        return {
            "language": ".js",
            "functions": functions,
            "classes": {cls: {"methods": []} for cls in classes},
            "imports": imports,
            "exports": [exp for exp in exports if exp],
            "line_count": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "comment_lines": len(comment_lines),
            "complexity": len(functions) + len(classes),
            "file_size": os.path.getsize(file_path),
            "import_count": len(imports),
            "function_count": len(functions),
            "class_count": len(classes)
        }
    except Exception as e:
        return {
            "language": ".js",
            "functions": [],
            "classes": {},
            "imports": [],
            "exports": [],
            "line_count": 0,
            "non_empty_lines": 0,
            "comment_lines": 0,
            "complexity": 0,
            "file_size": 0,
            "import_count": 0,
            "function_count": 0,
            "class_count": 0,
            "error": str(e)
        }

def analyze_md_file(file_path: str) -> Dict[str, Any]:
    """Analyze a Markdown file and extract metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract headers, code blocks, links
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        code_blocks = re.findall(r'```(\w+)?\n(.*?)```', content, re.DOTALL)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
        
        lines = content.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "language": ".md",
            "functions": [],
            "classes": {},
            "headers": headers,
            "code_blocks": len(code_blocks),
            "links": len(links),
            "images": len(images),
            "line_count": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "complexity": len(headers),
            "file_size": os.path.getsize(file_path),
            "header_count": len(headers)
        }
    except Exception as e:
        return {
            "language": ".md",
            "functions": [],
            "classes": {},
            "headers": [],
            "code_blocks": 0,
            "links": 0,
            "images": 0,
            "line_count": 0,
            "non_empty_lines": 0,
            "complexity": 0,
            "file_size": 0,
            "header_count": 0,
            "error": str(e)
        }

def analyze_yaml_file(file_path: str) -> Dict[str, Any]:
    """Analyze a YAML file and extract metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Enhanced YAML analysis
        lines = content.splitlines()
        keys = [line.split(':')[0].strip() for line in lines if ':' in line and not line.startswith('#')]
        comments = [line for line in lines if line.strip().startswith('#')]
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "language": ".yml",
            "functions": [],
            "classes": {},
            "keys": keys,
            "line_count": len(lines),
            "non_empty_lines": len(non_empty_lines),
            "comment_lines": len(comments),
            "complexity": len(keys),
            "file_size": os.path.getsize(file_path),
            "key_count": len(keys)
        }
    except Exception as e:
        return {
            "language": ".yml",
            "functions": [],
            "classes": {},
            "keys": [],
            "line_count": 0,
            "non_empty_lines": 0,
            "comment_lines": 0,
            "complexity": 0,
            "file_size": 0,
            "key_count": 0,
            "error": str(e)
        }

def analyze_file(file_path: str) -> Dict[str, Any]:
    """Analyze a file based on its extension."""
    ext = Path(file_path).suffix.lower()
    
    if ext == '.py':
        return analyze_python_file(file_path)
    elif ext == '.js':
        return analyze_js_file(file_path)
    elif ext == '.md':
        return analyze_md_file(file_path)
    elif ext in ['.yml', '.yaml']:
        return analyze_yaml_file(file_path)
    else:
        return {
            "language": ext,
            "functions": [],
            "classes": {},
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": "Unsupported file type"
        }

def get_directory_structure(root_path: str, max_depth: int = 3) -> Dict[str, Any]:
    """Get directory structure with file counts."""
    structure = {}
    total_files = 0
    total_dirs = 0
    
    for root, dirs, files in os.walk(root_path):
        rel_path = os.path.relpath(root, root_path)
        if rel_path == '.':
            rel_path = ''
        
        # Count files by extension
        file_counts = Counter(Path(f).suffix.lower() for f in files)
        
        structure[rel_path or '.'] = {
            "files": file_counts,
            "file_count": len(files),
            "subdirs": len(dirs),
            "total_files": len(files)
        }
        
        total_files += len(files)
        total_dirs += len(dirs)
        
        # Limit depth
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
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                
                print(f"  Analyzing: {rel_path}")
                analysis = analyze_file(file_path)
                directory_analysis[rel_path] = analysis
                
                # Update totals
                total_files += 1
                total_lines += analysis.get('line_count', 0)
                total_functions += analysis.get('function_count', 0)
                total_classes += analysis.get('class_count', 0)
                total_imports += analysis.get('import_count', 0)
                
                # Track file types
                file_type = analysis.get('language', 'unknown')
                file_types[file_type] += 1
                
                # Track complexity by type
                complexity_by_type[file_type].append(analysis.get('complexity', 0))
                
                # Track imports
                if analysis.get('imports'):
                    imports_by_file[rel_path] = analysis['imports']
        
        all_analysis[directory] = directory_analysis
    
    # Calculate averages
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
    # Directories to analyze
    directories_to_analyze = [
        "src",
        "src/services"
    ]
    
    print("🔍 Starting comprehensive source directory analysis...")
    
    # Analyze directories
    analysis_results = analyze_directories(directories_to_analyze)
    
    # Get directory structures
    directory_structures = {}
    for directory in directories_to_analyze:
        if os.path.exists(directory):
            directory_structures[directory] = get_directory_structure(directory)
    
    # Generate comprehensive project analysis
    project_analysis = {
        "analysis_timestamp": str(Path().cwd()),
        "directories_analyzed": directories_to_analyze,
        "directory_structures": directory_structures,
        "file_analysis": analysis_results["directories"],
        "summary": analysis_results["summary"],
        "imports_analysis": analysis_results["imports_analysis"]
    }
    
    # Save project analysis
    with open('src_directories_project_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(project_analysis, f, indent=2)
    
    # Generate ChatGPT context
    chatgpt_context = {
        "project_root": os.getcwd(),
        "analysis_type": "src_directories_comprehensive",
        "directories_analyzed": directories_to_analyze,
        "num_files_analyzed": analysis_results["summary"]["total_files"],
        "analysis_details": analysis_results["directories"],
        "summary": analysis_results["summary"],
        "directory_structures": directory_structures,
        "imports_analysis": analysis_results["imports_analysis"]
    }
    
    # Save ChatGPT context
    with open('src_directories_chatgpt_context.json', 'w', encoding='utf-8') as f:
        json.dump(chatgpt_context, f, indent=2)
    
    # Generate detailed summary report
    summary_report = f"""# 📊 **SRC DIRECTORIES COMPREHENSIVE ANALYSIS REPORT**

**Generated by:** Agent-2 (Architecture & Design Specialist)  
**Analysis Date:** {Path().cwd()}  
**Analysis Type:** Comprehensive Source Directory Analysis  
**Directories Analyzed:** {', '.join(directories_to_analyze)}

---

## 📈 **ANALYSIS SUMMARY**

### **Files Analyzed:**
- **Total Files:** {analysis_results["summary"]["total_files"]}
- **Total Lines:** {analysis_results["summary"]["total_lines"]:,}
- **Total Functions:** {analysis_results["summary"]["total_functions"]}
- **Total Classes:** {analysis_results["summary"]["total_classes"]}
- **Total Imports:** {analysis_results["summary"]["total_imports"]}

### **File Type Distribution:**
"""
    
    for file_type, count in analysis_results["summary"]["file_types"].items():
        percentage = (count / analysis_results["summary"]["total_files"]) * 100
        summary_report += f"- **{file_type}:** {count} files ({percentage:.1f}%)\n"
    
    summary_report += f"""
### **Average Complexity by File Type:**
"""
    
    for file_type, avg_complexity in analysis_results["summary"]["avg_complexity_by_type"].items():
        summary_report += f"- **{file_type}:** {avg_complexity:.2f}\n"
    
    summary_report += f"""
---

## 🏗️ **DIRECTORY STRUCTURE ANALYSIS**

### **Directory Breakdown:**
"""
    
    for directory, structure in directory_structures.items():
        summary_report += f"""
#### **{directory}/**
- **Total Files:** {structure["total_files"]}
- **Total Directories:** {structure["total_dirs"]}
- **File Distribution:** {dict(structure["structure"]['.']["files"]) if '.' in structure["structure"] else 'N/A'}
"""
    
    summary_report += f"""
---

## 🔧 **TECHNICAL METRICS**

### **Code Quality Indicators:**
- **Average Lines per File:** {analysis_results["summary"]["total_lines"] / max(analysis_results["summary"]["total_files"], 1):.1f}
- **Average Functions per File:** {analysis_results["summary"]["total_functions"] / max(analysis_results["summary"]["total_files"], 1):.1f}
- **Average Classes per File:** {analysis_results["summary"]["total_classes"] / max(analysis_results["summary"]["total_files"], 1):.1f}
- **Average Imports per File:** {analysis_results["summary"]["total_imports"] / max(analysis_results["summary"]["total_files"], 1):.1f}

### **Complexity Analysis:**
- **Most Complex File Type:** {max(analysis_results["summary"]["avg_complexity_by_type"].items(), key=lambda x: x[1])[0] if analysis_results["summary"]["avg_complexity_by_type"] else 'N/A'}
- **Least Complex File Type:** {min(analysis_results["summary"]["avg_complexity_by_type"].items(), key=lambda x: x[1])[0] if analysis_results["summary"]["avg_complexity_by_type"] else 'N/A'}

---

## 📁 **GENERATED FILES**

### **Analysis Artifacts:**
- **`src_directories_project_analysis.json`:** Detailed technical analysis
- **`src_directories_chatgpt_context.json`:** ChatGPT-ready context
- **`SRC_DIRECTORIES_ANALYSIS_SUMMARY.md`:** This summary report

---

## 🎯 **CONSOLIDATION INSIGHTS**

This analysis provides the foundation for our **Option 2 (Balanced Consolidation)** strategy, identifying:
1. **File Distribution Patterns:** Understanding code organization
2. **Complexity Hotspots:** Areas requiring attention
3. **Import Dependencies:** Module relationship mapping
4. **Consolidation Opportunities:** Files that can be merged

---

**🐝 WE ARE SWARM - Comprehensive source directory analysis complete!**
"""
    
    # Save summary report
    with open('SRC_DIRECTORIES_ANALYSIS_SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write(summary_report)
    
    print(f"\n✅ Analysis complete!")
    print(f"📊 Files analyzed: {analysis_results['summary']['total_files']}")
    print(f"📝 Total lines: {analysis_results['summary']['total_lines']:,}")
    print(f"🔧 Total functions: {analysis_results['summary']['total_functions']}")
    print(f"🏗️ Total classes: {analysis_results['summary']['total_classes']}")
    print(f"📦 Total imports: {analysis_results['summary']['total_imports']}")
    print(f"📁 Generated files:")
    print(f"   - src_directories_project_analysis.json")
    print(f"   - src_directories_chatgpt_context.json")
    print(f"   - SRC_DIRECTORIES_ANALYSIS_SUMMARY.md")

if __name__ == "__main__":
    main()
