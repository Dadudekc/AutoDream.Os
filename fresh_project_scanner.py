#!/usr/bin/env python3
"""
Fresh Project Scanner - Robust Analysis Without Dependencies
Generates comprehensive project analysis without external dependencies.
"""

import ast
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class FreshProjectScanner:
    """Robust project scanner that works without external dependencies."""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.analysis_timestamp = datetime.now().isoformat()
        self.results = {}
        self.stats = {
            "total_files": 0,
            "total_dirs": 0,
            "file_types": Counter(),
            "languages": Counter(),
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "lines": 0,
            "complexity": 0
        }

    def analyze_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze Python file with robust error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if not content.strip():
                return self._empty_analysis(".py")

            tree = ast.parse(content)
            
            functions = []
            classes = {}
            imports = []
            complexity = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                    complexity += 1
                    # Count nested structures for complexity
                    for child in ast.walk(node):
                        if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                            complexity += 1
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes[node.name] = {
                        "methods": methods,
                        "line_count": len(node.body),
                        "base_classes": [base.id for base in node.bases if isinstance(base, ast.Name)]
                    }
                    complexity += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    else:
                        module = node.module or ""
                        imports.extend([f"{module}.{alias.name}" for alias in node.names])

            lines = content.splitlines()
            non_empty_lines = [line for line in lines if line.strip()]
            comment_lines = [line for line in lines if line.strip().startswith('#')]

            return {
                "language": ".py",
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "line_count": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "comment_lines": len(comment_lines),
                "complexity": complexity,
                "file_size": file_path.stat().st_size,
                "function_count": len(functions),
                "class_count": len(classes),
                "import_count": len(imports),
                "has_main": "__main__" in content,
                "has_tests": any(keyword in content.lower() for keyword in ["test", "pytest", "unittest"]),
                "has_async": "async" in content,
                "has_type_hints": ":" in content and "->" in content,
                "error": None
            }
        except Exception as e:
            return {
                "language": ".py",
                "functions": [],
                "classes": {},
                "imports": [],
                "line_count": 0,
                "non_empty_lines": 0,
                "comment_lines": 0,
                "complexity": 0,
                "file_size": 0,
                "function_count": 0,
                "class_count": 0,
                "import_count": 0,
                "has_main": False,
                "has_tests": False,
                "has_async": False,
                "has_type_hints": False,
                "error": str(e)
            }

    def analyze_js_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze JavaScript file with robust error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if not content.strip():
                return self._empty_analysis(".js")

            # Simple regex-based analysis
            functions = re.findall(r'function\s+(\w+)\s*\(', content)
            classes = re.findall(r'class\s+(\w+)', content)
            imports = re.findall(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', content)
            exports = re.findall(r'export\s+(?:default\s+)?(?:function\s+(\w+)|const\s+(\w+)|class\s+(\w+))', content)
            async_functions = re.findall(r'async\s+function\s+(\w+)', content)
            arrow_functions = re.findall(r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>', content)

            lines = content.splitlines()
            non_empty_lines = [line for line in lines if line.strip()]
            comment_lines = [line for line in lines if line.strip().startswith(('//', '/*', '*'))]

            return {
                "language": ".js",
                "functions": functions,
                "classes": {cls: {"methods": []} for cls in classes},
                "imports": imports,
                "exports": [exp for exp in exports if exp],
                "async_functions": async_functions,
                "arrow_functions": arrow_functions,
                "line_count": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "comment_lines": len(comment_lines),
                "complexity": len(functions) + len(classes),
                "file_size": file_path.stat().st_size,
                "function_count": len(functions),
                "class_count": len(classes),
                "import_count": len(imports),
                "has_async": len(async_functions) > 0,
                "has_arrow_functions": len(arrow_functions) > 0,
                "has_es6": "=>" in content or "class " in content,
                "has_jquery": "$" in content,
                "has_react": "React" in content or "useState" in content,
                "error": None
            }
        except Exception as e:
            return {
                "language": ".js",
                "functions": [],
                "classes": {},
                "imports": [],
                "exports": [],
                "async_functions": [],
                "arrow_functions": [],
                "line_count": 0,
                "non_empty_lines": 0,
                "comment_lines": 0,
                "complexity": 0,
                "file_size": 0,
                "function_count": 0,
                "class_count": 0,
                "import_count": 0,
                "has_async": False,
                "has_arrow_functions": False,
                "has_es6": False,
                "has_jquery": False,
                "has_react": False,
                "error": str(e)
            }

    def analyze_md_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze Markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if not content.strip():
                return self._empty_analysis(".md")

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
                "file_size": file_path.stat().st_size,
                "header_count": len(headers),
                "has_toc": "Table of Contents" in content or "## Contents" in content,
                "has_code": len(code_blocks) > 0,
                "has_images": len(images) > 0,
                "has_links": len(links) > 0,
                "error": None
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
                "has_toc": False,
                "has_code": False,
                "has_images": False,
                "has_links": False,
                "error": str(e)
            }

    def _empty_analysis(self, language: str) -> Dict[str, Any]:
        """Return empty analysis for empty files."""
        return {
            "language": language,
            "functions": [],
            "classes": {},
            "line_count": 0,
            "complexity": 0,
            "file_size": 0,
            "error": "Empty file"
        }

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze file based on extension."""
        suffix = file_path.suffix.lower()
        
        if suffix == '.py':
            return self.analyze_python_file(file_path)
        elif suffix == '.js':
            return self.analyze_js_file(file_path)
        elif suffix == '.md':
            return self.analyze_md_file(file_path)
        else:
            # Basic analysis for other file types
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                lines = content.splitlines()
                return {
                    "language": suffix,
                    "functions": [],
                    "classes": {},
                    "line_count": len(lines),
                    "complexity": 0,
                    "file_size": file_path.stat().st_size,
                    "error": None
                }
            except Exception as e:
                return {
                    "language": suffix,
                    "functions": [],
                    "classes": {},
                    "line_count": 0,
                    "complexity": 0,
                    "file_size": 0,
                    "error": str(e)
                }

    def scan_project(self) -> None:
        """Scan the entire project."""
        print("🚀 Starting fresh project scan...")
        
        # Directories to skip
        skip_dirs = {
            '__pycache__', '.git', 'node_modules', 'venv', '.venv', 'env',
            '.pytest_cache', '.mypy_cache', '.coverage', 'htmlcov',
            'dist', 'build', '.tox', '.eggs', '*.egg-info'
        }
        
        # File extensions to analyze
        analyze_extensions = {'.py', '.js', '.ts', '.md', '.json', '.yaml', '.yml', '.css', '.html'}
        
        for root, dirs, files in os.walk(self.project_root):
            # Filter out skip directories
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            rel_root = os.path.relpath(root, self.project_root)
            if rel_root == '.':
                rel_root = ''
            
            self.stats["total_dirs"] += 1
            
            for file in files:
                file_path = Path(root) / file
                suffix = file_path.suffix.lower()
                
                # Skip certain files
                if file.startswith('.') or file.endswith('.pyc') or file.endswith('.pyo'):
                    continue
                
                self.stats["total_files"] += 1
                self.stats["file_types"][suffix] += 1
                
                # Analyze file if it's a supported type
                if suffix in analyze_extensions:
                    rel_path = str(file_path.relative_to(self.project_root))
                    print(f"  📄 Analyzing: {rel_path}")
                    
                    analysis = self.analyze_file(file_path)
                    self.results[rel_path] = analysis
                    
                    # Update stats
                    self.stats["languages"][analysis["language"]] += 1
                    self.stats["functions"] += analysis.get("function_count", 0)
                    self.stats["classes"] += analysis.get("class_count", 0)
                    self.stats["imports"] += analysis.get("import_count", 0)
                    self.stats["lines"] += analysis.get("line_count", 0)
                    self.stats["complexity"] += analysis.get("complexity", 0)

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report."""
        # Calculate averages
        analyzed_files = len(self.results)
        avg_complexity = self.stats["complexity"] / analyzed_files if analyzed_files > 0 else 0
        avg_lines = self.stats["lines"] / analyzed_files if analyzed_files > 0 else 0
        
        # Find most complex files
        complex_files = []
        for file_path, analysis in self.results.items():
            if analysis.get("complexity", 0) > 10:
                complex_files.append({
                    "file": file_path,
                    "complexity": analysis.get("complexity", 0),
                    "functions": analysis.get("function_count", 0),
                    "classes": analysis.get("class_count", 0)
                })
        
        complex_files.sort(key=lambda x: x["complexity"], reverse=True)
        
        # Find files with errors
        error_files = []
        for file_path, analysis in self.results.items():
            if analysis.get("error"):
                error_files.append({
                    "file": file_path,
                    "error": analysis["error"]
                })
        
        return {
            "analysis_timestamp": self.analysis_timestamp,
            "project_root": str(self.project_root),
            "summary": {
                "total_files": self.stats["total_files"],
                "total_dirs": self.stats["total_dirs"],
                "analyzed_files": analyzed_files,
                "file_types": dict(self.stats["file_types"]),
                "languages": dict(self.stats["languages"]),
                "total_functions": self.stats["functions"],
                "total_classes": self.stats["classes"],
                "total_imports": self.stats["imports"],
                "total_lines": self.stats["lines"],
                "total_complexity": self.stats["complexity"],
                "avg_complexity": round(avg_complexity, 2),
                "avg_lines_per_file": round(avg_lines, 2)
            },
            "complex_files": complex_files[:20],  # Top 20 most complex
            "error_files": error_files,
            "detailed_results": self.results
        }

    def save_results(self, output_file: str = "fresh_project_analysis.json") -> None:
        """Save analysis results to file."""
        report = self.generate_report()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Analysis saved to: {output_file}")
        
        # Print summary
        print("\n📊 FRESH PROJECT SCAN SUMMARY")
        print("=" * 50)
        print(f"📁 Total Files: {self.stats['total_files']}")
        print(f"📂 Total Directories: {self.stats['total_dirs']}")
        print(f"🔍 Analyzed Files: {len(self.results)}")
        print(f"🐍 Python Files: {self.stats['languages']['.py']}")
        print(f"🌐 JavaScript Files: {self.stats['languages']['.js']}")
        print(f"📝 Markdown Files: {self.stats['languages']['.md']}")
        print(f"⚙️ Total Functions: {self.stats['functions']}")
        print(f"🏗️ Total Classes: {self.stats['classes']}")
        print(f"📦 Total Imports: {self.stats['imports']}")
        print(f"📏 Total Lines: {self.stats['lines']:,}")
        print(f"🧩 Total Complexity: {self.stats['complexity']}")
        print(f"⚠️ Files with Errors: {len([f for f in self.results.values() if f.get('error')])}")
        print("=" * 50)


def main():
    """Main function to run the fresh project scan."""
    scanner = FreshProjectScanner()
    scanner.scan_project()
    scanner.save_results()
    print("\n🐝 WE ARE SWARM - Fresh project scan completed successfully!")


if __name__ == "__main__":
    main()