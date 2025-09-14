#!/usr/bin/env python3
"""
Messaging Files Analysis Tool
Analyzes all messaging-related files and generates ChatGPT context and project analysis.
"""

import ast
import json
import os
import re
from pathlib import Path
from typing import Any


def analyze_python_file(file_path: str) -> dict[str, Any]:
    """Analyze a Python file and extract metadata."""
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.read()

        # Parse AST
        tree = ast.parse(content)

        functions = []
        classes = {}
        imports = []

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
            "language": ".py",
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "line_count": len(content.splitlines()),
            "complexity": len(functions) + len(classes),
            "file_size": os.path.getsize(file_path)
        }
    except Exception as e:
        return {
            "language": ".py",
            "functions": [],
            "classes": {},
            "imports": [],
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": str(e)
        }

def analyze_js_file(file_path: str) -> dict[str, Any]:
    """Analyze a JavaScript file and extract metadata."""
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.read()

        # Simple regex-based analysis for JS
        functions = re.findall(r'function\s+(\w+)\s*\(', content)
        classes = re.findall(r'class\s+(\w+)', content)

        return {
            "language": ".js",
            "functions": functions,
            "classes": {cls: {"methods": []} for cls in classes},
            "line_count": len(content.splitlines()),
            "complexity": len(functions) + len(classes),
            "file_size": os.path.getsize(file_path)
        }
    except Exception as e:
        return {
            "language": ".js",
            "functions": [],
            "classes": {},
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": str(e)
        }

def analyze_md_file(file_path: str) -> dict[str, Any]:
    """Analyze a Markdown file and extract metadata."""
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.read()

        # Extract headers
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)

        return {
            "language": ".md",
            "functions": [],
            "classes": {},
            "headers": headers,
            "line_count": len(content.splitlines()),
            "complexity": len(headers),
            "file_size": os.path.getsize(file_path)
        }
    except Exception as e:
        return {
            "language": ".md",
            "functions": [],
            "classes": {},
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": str(e)
        }

def analyze_yaml_file(file_path: str) -> dict[str, Any]:
    """Analyze a YAML file and extract metadata."""
    try:
        with open(file_path, encoding='utf-8') as f:
            content = f.read()

        # Simple YAML analysis
        lines = content.splitlines()
        keys = [line.split(':')[0].strip() for line in lines if ':' in line and not line.startswith('#')]

        return {
            "language": ".yml",
            "functions": [],
            "classes": {},
            "keys": keys,
            "line_count": len(lines),
            "complexity": len(keys),
            "file_size": os.path.getsize(file_path)
        }
    except Exception as e:
        return {
            "language": ".yml",
            "functions": [],
            "classes": {},
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": str(e)
        }

def analyze_file(file_path: str) -> dict[str, Any]:
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

def main():
    """Main analysis function."""
    # Messaging-related files
    messaging_files = [
        "src/core/messaging_pyautogui.py",
        "src/services/messaging_core.py",
        "src/core/messaging_core.py",
        "src/services/messaging_pyautogui.py",
        "scripts/messaging_cli_completion.sh",
        "docs/specifications/MESSAGING_SYSTEM_V2_ENHANCED_TYPES.md",
        "docs/specifications/MESSAGING_SYSTEM_PRD.md",
        "docs/specifications/MESSAGING_DEPLOYMENT_STRATEGY.md",
        "docs/specifications/MESSAGING_ARCHITECTURE_DIAGRAM.md",
        "docs/specifications/MESSAGING_API_SPECIFICATIONS.md",
        "config/messaging.yml"
    ]

    # Analyze each file
    analysis_results = {}
    total_files = 0
    total_lines = 0
    total_functions = 0
    total_classes = 0

    for file_path in messaging_files:
        if os.path.exists(file_path):
            print(f"Analyzing: {file_path}")
            analysis = analyze_file(file_path)
            analysis_results[file_path] = analysis

            total_files += 1
            total_lines += analysis.get('line_count', 0)
            total_functions += len(analysis.get('functions', []))
            total_classes += len(analysis.get('classes', {}))
        else:
            print(f"File not found: {file_path}")

    # Generate project analysis JSON
    project_analysis = {
        "messaging_files_analysis": analysis_results,
        "summary": {
            "total_files": total_files,
            "total_lines": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "average_complexity": sum(analysis.get('complexity', 0) for analysis in analysis_results.values()) / max(total_files, 1)
        }
    }

    # Save project analysis
    with open('messaging_project_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(project_analysis, f, indent=2)

    # Generate ChatGPT context
    chatgpt_context = {
        "project_root": os.getcwd(),
        "analysis_type": "messaging_files_focused",
        "num_files_analyzed": total_files,
        "analysis_details": analysis_results,
        "summary": {
            "total_files": total_files,
            "total_lines": total_lines,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "file_types": {
                "python": len([f for f in analysis_results.values() if f.get('language') == '.py']),
                "markdown": len([f for f in analysis_results.values() if f.get('language') == '.md']),
                "yaml": len([f for f in analysis_results.values() if f.get('language') == '.yml']),
                "javascript": len([f for f in analysis_results.values() if f.get('language') == '.js'])
            }
        }
    }

    # Save ChatGPT context
    with open('messaging_chatgpt_context.json', 'w', encoding='utf-8') as f:
        json.dump(chatgpt_context, f, indent=2)

    print("\n✅ Analysis complete!")
    print(f"📊 Files analyzed: {total_files}")
    print(f"📝 Total lines: {total_lines}")
    print(f"🔧 Total functions: {total_functions}")
    print(f"🏗️ Total classes: {total_classes}")
    print("📁 Generated files:")
    print("   - messaging_project_analysis.json")
    print("   - messaging_chatgpt_context.json")

if __name__ == "__main__":
    main()
