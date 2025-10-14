#!/usr/bin/env python3
"""
Source Directory File Analyzers
Extracted from analyze_src_directories.py for V2 compliance.
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, Any
from collections import Counter


def analyze_python_file(file_path: str) -> Dict[str, Any]:
    """Analyze a Python file and extract comprehensive metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
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
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                if isinstance(node.value.value, str) and node.value.value.strip().startswith(('"""', "'''")):
                    docstrings.append(node.value.value.strip())
        
        lines = content.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        comment_lines = [line for line in lines if line.strip().startswith('#')]
        
        return {
            "language": ".py", "functions": functions, "classes": classes,
            "imports": imports, "decorators": decorators, "docstrings": len(docstrings),
            "line_count": len(lines), "non_empty_lines": len(non_empty_lines),
            "comment_lines": len(comment_lines), "complexity": complexity_indicators,
            "file_size": os.path.getsize(file_path), "import_count": len(imports),
            "function_count": len(functions), "class_count": len(classes)
        }
    except Exception as e:
        return {
            "language": ".py", "functions": [], "classes": {}, "imports": [],
            "decorators": [], "docstrings": 0, "line_count": 0, "non_empty_lines": 0,
            "comment_lines": 0, "complexity": 0, "file_size": 0, "import_count": 0,
            "function_count": 0, "class_count": 0, "error": str(e)
        }


def analyze_js_file(file_path: str) -> Dict[str, Any]:
    """Analyze a JavaScript file and extract metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        functions = re.findall(r'function\s+(\w+)\s*\(', content)
        classes = re.findall(r'class\s+(\w+)', content)
        imports = re.findall(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', content)
        exports = re.findall(r'export\s+(?:default\s+)?(?:function\s+(\w+)|const\s+(\w+)|class\s+(\w+))', content)
        
        lines = content.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        comment_lines = [line for line in lines if line.strip().startswith(('//', '/*', '*'))]
        
        return {
            "language": ".js", "functions": functions,
            "classes": {cls: {"methods": []} for cls in classes},
            "imports": imports, "exports": [exp for exp in exports if exp],
            "line_count": len(lines), "non_empty_lines": len(non_empty_lines),
            "comment_lines": len(comment_lines), "complexity": len(functions) + len(classes),
            "file_size": os.path.getsize(file_path), "import_count": len(imports),
            "function_count": len(functions), "class_count": len(classes)
        }
    except Exception as e:
        return {
            "language": ".js", "functions": [], "classes": {}, "imports": [],
            "exports": [], "line_count": 0, "non_empty_lines": 0, "comment_lines": 0,
            "complexity": 0, "file_size": 0, "import_count": 0, "function_count": 0,
            "class_count": 0, "error": str(e)
        }


def analyze_md_file(file_path: str) -> Dict[str, Any]:
    """Analyze a Markdown file and extract metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        code_blocks = re.findall(r'```(\w+)?\n(.*?)```', content, re.DOTALL)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
        
        lines = content.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "language": ".md", "functions": [], "classes": {}, "headers": headers,
            "code_blocks": len(code_blocks), "links": len(links), "images": len(images),
            "line_count": len(lines), "non_empty_lines": len(non_empty_lines),
            "complexity": len(headers), "file_size": os.path.getsize(file_path),
            "header_count": len(headers)
        }
    except Exception as e:
        return {
            "language": ".md", "functions": [], "classes": {}, "headers": [],
            "code_blocks": 0, "links": 0, "images": 0, "line_count": 0,
            "non_empty_lines": 0, "complexity": 0, "file_size": 0,
            "header_count": 0, "error": str(e)
        }


def analyze_yaml_file(file_path: str) -> Dict[str, Any]:
    """Analyze a YAML file and extract metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.splitlines()
        keys = [line.split(':')[0].strip() for line in lines if ':' in line and not line.startswith('#')]
        comments = [line for line in lines if line.strip().startswith('#')]
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            "language": ".yml", "functions": [], "classes": {}, "keys": keys,
            "line_count": len(lines), "non_empty_lines": len(non_empty_lines),
            "comment_lines": len(comments), "complexity": len(keys),
            "file_size": os.path.getsize(file_path), "key_count": len(keys)
        }
    except Exception as e:
        return {
            "language": ".yml", "functions": [], "classes": {}, "keys": [],
            "line_count": 0, "non_empty_lines": 0, "comment_lines": 0,
            "complexity": 0, "file_size": 0, "key_count": 0, "error": str(e)
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
            "language": ext, "functions": [], "classes": {},
            "line_count": 0, "complexity": 0, "file_size": 0,
            "error": "Unsupported file type"
        }

