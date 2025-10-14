#!/usr/bin/env python3
"""
Comprehensive Project Analyzer - Modular Chunked Analysis
Generates manageable analysis chunks for consolidation efforts.
"""

import ast
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


class ProjectAnalyzer:
    """Comprehensive project analyzer with chunked output."""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.analysis_timestamp = datetime.now().isoformat()
        self.chunk_size = 50  # Files per chunk
        self.output_dir = Path("analysis_chunks")
        self.output_dir.mkdir(exist_ok=True)

    def analyze_python_file(self, file_path: str) -> dict[str, Any]:
        """Analyze a Python file with comprehensive metadata."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            functions = []
            classes = {}
            imports = []
            decorators = []
            docstrings = []
            complexity_indicators = 0
            lines = content.splitlines()

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                    complexity_indicators += 1
                    # Count nested structures
                    for child in ast.walk(node):
                        if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                            complexity_indicators += 1
                elif isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes[node.name] = {
                        "methods": methods,
                        "line_count": len(node.body),
                        "base_classes": [
                            base.id for base in node.bases if isinstance(base, ast.Name)
                        ],
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
                elif (
                    isinstance(node, ast.Expr)
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                ):
                    if node.value.value.strip().startswith(('"""', "'''")):
                        docstrings.append(node.value.value.strip())

            non_empty_lines = [line for line in lines if line.strip()]
            comment_lines = [line for line in lines if line.strip().startswith("#")]

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
                "class_count": len(classes),
                "has_main": "__main__" in content,
                "has_tests": any(
                    keyword in content.lower() for keyword in ["test", "pytest", "unittest"]
                ),
                "has_async": "async" in content,
                "has_type_hints": ":" in content and "->" in content,
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
                "has_main": False,
                "has_tests": False,
                "has_async": False,
                "has_type_hints": False,
                "error": str(e),
            }

    def analyze_js_file(self, file_path: str) -> dict[str, Any]:
        """Analyze a JavaScript file with enhanced metadata."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            functions = re.findall(r"function\s+(\w+)\s*\(", content)
            classes = re.findall(r"class\s+(\w+)", content)
            imports = re.findall(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', content)
            exports = re.findall(
                r"export\s+(?:default\s+)?(?:function\s+(\w+)|const\s+(\w+)|class\s+(\w+))", content
            )
            async_functions = re.findall(r"async\s+function\s+(\w+)", content)
            arrow_functions = re.findall(r"const\s+(\w+)\s*=\s*\([^)]*\)\s*=>", content)

            lines = content.splitlines()
            non_empty_lines = [line for line in lines if line.strip()]
            comment_lines = [line for line in lines if line.strip().startswith(("//", "/*", "*"))]

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
                "file_size": os.path.getsize(file_path),
                "import_count": len(imports),
                "function_count": len(functions),
                "class_count": len(classes),
                "has_async": len(async_functions) > 0,
                "has_arrow_functions": len(arrow_functions) > 0,
                "has_es6": "=>" in content or "class " in content,
                "has_jquery": "$" in content,
                "has_react": "React" in content or "useState" in content,
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
                "import_count": 0,
                "function_count": 0,
                "class_count": 0,
                "has_async": False,
                "has_arrow_functions": False,
                "has_es6": False,
                "has_jquery": False,
                "has_react": False,
                "error": str(e),
            }

    def analyze_md_file(self, file_path: str) -> dict[str, Any]:
        """Analyze a Markdown file with comprehensive metadata."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            headers = re.findall(r"^#+\s+(.+)$", content, re.MULTILINE)
            code_blocks = re.findall(r"```(\w+)?\n(.*?)```", content, re.DOTALL)
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
            images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", content)
            tables = re.findall(r"\|.*\|", content)

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
                "tables": len(tables),
                "line_count": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "complexity": len(headers),
                "file_size": os.path.getsize(file_path),
                "header_count": len(headers),
                "has_toc": "Table of Contents" in content or "## Contents" in content,
                "has_code": len(code_blocks) > 0,
                "has_images": len(images) > 0,
                "has_links": len(links) > 0,
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
                "tables": 0,
                "line_count": 0,
                "non_empty_lines": 0,
                "complexity": 0,
                "file_size": 0,
                "header_count": 0,
                "has_toc": False,
                "has_code": False,
                "has_images": False,
                "has_links": False,
                "error": str(e),
            }

    def analyze_yaml_file(self, file_path: str) -> dict[str, Any]:
        """Analyze a YAML file with comprehensive metadata."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()
            keys = [
                line.split(":")[0].strip()
                for line in lines
                if ":" in line and not line.startswith("#")
            ]
            comments = [line for line in lines if line.strip().startswith("#")]
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
                "key_count": len(keys),
                "has_comments": len(comments) > 0,
                "is_config": any(
                    keyword in content.lower() for keyword in ["config", "settings", "default"]
                ),
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
                "has_comments": False,
                "is_config": False,
                "error": str(e),
            }

    def analyze_file(self, file_path: str) -> dict[str, Any]:
        """Analyze a file based on its extension."""
        ext = Path(file_path).suffix.lower()

        if ext == ".py":
            return self.analyze_python_file(file_path)
        elif ext == ".js":
            return self.analyze_js_file(file_path)
        elif ext == ".md":
            return self.analyze_md_file(file_path)
        elif ext in [".yml", ".yaml"]:
            return self.analyze_yaml_file(file_path)
        else:
            return {
                "language": ext,
                "functions": [],
                "classes": {},
                "line_count": 0,
                "complexity": 0,
                "file_size": 0,
                "error": "Unsupported file type",
            }

    def get_project_structure(self) -> dict[str, Any]:
        """Get comprehensive project structure."""
        structure = {}
        total_files = 0
        total_dirs = 0
        file_types = Counter()

        for root, dirs, files in os.walk(self.project_root):
            rel_path = os.path.relpath(root, self.project_root)
            if rel_path == ".":
                rel_path = ""

            # Skip certain directories
            skip_dirs = ["__pycache__", ".git", "node_modules", "venv", ".venv", "env"]
            dirs[:] = [d for d in dirs if d not in skip_dirs]

            file_counts = Counter(Path(f).suffix.lower() for f in files)

            structure[rel_path or "."] = {
                "files": file_counts,
                "file_count": len(files),
                "subdirs": len(dirs),
                "total_files": len(files),
            }

            total_files += len(files)
            total_dirs += len(dirs)
            file_types.update(file_counts)

        return {
            "structure": structure,
            "total_files": total_files,
            "total_dirs": total_dirs,
            "file_types": dict(file_types),
        }

    def analyze_directory_chunk(self, directory: str, chunk_id: int) -> dict[str, Any]:
        """Analyze a directory chunk for consolidation."""
        if not os.path.exists(directory):
            return {"error": f"Directory not found: {directory}"}

        print(f"🔍 Analyzing directory chunk {chunk_id}: {directory}")

        files_analyzed = []
        total_files = 0
        total_lines = 0
        total_functions = 0
        total_classes = 0
        total_imports = 0
        file_types = Counter()
        complexity_by_type = defaultdict(list)
        imports_by_file = defaultdict(list)
        consolidation_opportunities = []

        for root, dirs, files in os.walk(directory):
            # Skip certain directories
            skip_dirs = ["__pycache__", ".git", "node_modules", "venv", ".venv", "env"]
            dirs[:] = [d for d in dirs if d not in skip_dirs]

            for file in files:
                if total_files >= self.chunk_size:
                    break

                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.project_root)

                print(f"  📄 Analyzing: {rel_path}")
                analysis = self.analyze_file(file_path)

                files_analyzed.append({"file_path": rel_path, "analysis": analysis})

                # Update totals
                total_files += 1
                total_lines += analysis.get("line_count", 0)
                total_functions += analysis.get("function_count", 0)
                total_classes += analysis.get("class_count", 0)
                total_imports += analysis.get("import_count", 0)

                # Track file types
                file_type = analysis.get("language", "unknown")
                file_types[file_type] += 1

                # Track complexity
                complexity_by_type[file_type].append(analysis.get("complexity", 0))

                # Track imports
                if analysis.get("imports"):
                    imports_by_file[rel_path] = analysis["imports"]

                # Identify consolidation opportunities
                if self.identify_consolidation_opportunity(analysis, rel_path):
                    consolidation_opportunities.append(
                        {
                            "file_path": rel_path,
                            "reason": self.get_consolidation_reason(analysis),
                            "priority": self.get_consolidation_priority(analysis),
                        }
                    )

            if total_files >= self.chunk_size:
                break

        # Calculate averages
        avg_complexity_by_type = {}
        for file_type, complexities in complexity_by_type.items():
            avg_complexity_by_type[file_type] = (
                sum(complexities) / len(complexities) if complexities else 0
            )

        return {
            "chunk_id": chunk_id,
            "directory": directory,
            "files_analyzed": files_analyzed,
            "summary": {
                "total_files": total_files,
                "total_lines": total_lines,
                "total_functions": total_functions,
                "total_classes": total_classes,
                "total_imports": total_imports,
                "file_types": dict(file_types),
                "avg_complexity_by_type": avg_complexity_by_type,
            },
            "consolidation_opportunities": consolidation_opportunities,
            "imports_analysis": dict(imports_by_file),
        }

    def identify_consolidation_opportunity(self, analysis: dict[str, Any], file_path: str) -> bool:
        """Identify if a file is a consolidation opportunity."""
        # Small files with few functions
        if analysis.get("line_count", 0) < 50 and analysis.get("function_count", 0) < 3:
            return True

        # Files with no functions or classes
        if analysis.get("function_count", 0) == 0 and analysis.get("class_count", 0) == 0:
            return True

        # Duplicate patterns
        if "messaging_pyautogui" in file_path or "config" in file_path:
            return True

        # Very small files
        if analysis.get("file_size", 0) < 1000:
            return True

        return False

    def get_consolidation_reason(self, analysis: dict[str, Any]) -> str:
        """Get reason for consolidation."""
        if analysis.get("line_count", 0) < 50:
            return "Small file - potential merge candidate"
        elif analysis.get("function_count", 0) == 0:
            return "No functions - utility or config file"
        elif "messaging_pyautogui" in str(analysis):
            return "Duplicate PyAutoGUI module"
        elif "config" in str(analysis):
            return "Configuration file - consolidate with unified config"
        else:
            return "Low complexity - consolidation candidate"

    def get_consolidation_priority(self, analysis: dict[str, Any]) -> str:
        """Get consolidation priority."""
        if "messaging_pyautogui" in str(analysis):
            return "HIGH"
        elif "config" in str(analysis):
            return "HIGH"
        elif analysis.get("line_count", 0) < 30:
            return "MEDIUM"
        else:
            return "LOW"

    def generate_chunk_reports(self, directories: list[str]) -> None:
        """Generate chunked analysis reports."""
        print("🚀 Starting comprehensive project analysis with chunked output...")

        # Get project structure
        structure = self.get_project_structure()

        # Generate master index
        master_index = {
            "analysis_timestamp": self.analysis_timestamp,
            "project_root": str(self.project_root),
            "chunk_size": self.chunk_size,
            "total_directories": len(directories),
            "project_structure": structure,
            "chunks": [],
        }

        chunk_id = 1
        for directory in directories:
            if not os.path.exists(directory):
                print(f"⚠️ Directory not found: {directory}")
                continue

            # Analyze directory chunk
            chunk_analysis = self.analyze_directory_chunk(directory, chunk_id)

            # Save chunk file
            chunk_file = self.output_dir / f"chunk_{chunk_id:03d}_{Path(directory).name}.json"
            with open(chunk_file, "w", encoding="utf-8") as f:
                json.dump(chunk_analysis, f, indent=2)

            # Add to master index
            master_index["chunks"].append(
                {
                    "chunk_id": chunk_id,
                    "directory": directory,
                    "file_path": str(chunk_file),
                    "files_analyzed": chunk_analysis["summary"]["total_files"],
                    "consolidation_opportunities": len(
                        chunk_analysis["consolidation_opportunities"]
                    ),
                }
            )

            print(f"✅ Chunk {chunk_id} saved: {chunk_file}")
            chunk_id += 1

        # Save master index
        master_file = self.output_dir / "master_index.json"
        with open(master_file, "w", encoding="utf-8") as f:
            json.dump(master_index, f, indent=2)

        # Generate consolidation summary
        self.generate_consolidation_summary(master_index)

        print("\n🎉 Analysis complete!")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📊 Total chunks generated: {chunk_id - 1}")
        print(f"📋 Master index: {master_file}")

    def generate_consolidation_summary(self, master_index: dict[str, Any]) -> None:
        """Generate consolidation summary report."""
        total_files = sum(chunk["files_analyzed"] for chunk in master_index["chunks"])
        total_opportunities = sum(
            chunk["consolidation_opportunities"] for chunk in master_index["chunks"]
        )

        summary = f"""# 📊 **COMPREHENSIVE PROJECT ANALYSIS - CONSOLIDATION SUMMARY**

**Generated by:** Agent-2 (Architecture & Design Specialist)  
**Analysis Date:** {self.analysis_timestamp}  
**Project Root:** {self.project_root}  
**Analysis Type:** Chunked Comprehensive Analysis  

---

## 📈 **ANALYSIS OVERVIEW**

### **Total Analysis:**
- **Chunks Generated:** {len(master_index["chunks"])}
- **Total Files Analyzed:** {total_files}
- **Consolidation Opportunities:** {total_opportunities}
- **Chunk Size:** {self.chunk_size} files per chunk

### **Project Structure:**
- **Total Directories:** {master_index["project_structure"]["total_dirs"]}
- **Total Files:** {master_index["project_structure"]["total_files"]}
- **File Types:** {master_index["project_structure"]["file_types"]}

---

## 🎯 **CONSOLIDATION OPPORTUNITIES BY CHUNK**

"""

        for chunk in master_index["chunks"]:
            summary += f"""
### **Chunk {chunk["chunk_id"]:03d}: {Path(chunk["directory"]).name}**
- **Files Analyzed:** {chunk["files_analyzed"]}
- **Consolidation Opportunities:** {chunk["consolidation_opportunities"]}
- **File:** `{chunk["file_path"]}`

"""

        summary += """
---

## 📁 **GENERATED FILES**

### **Master Index:**
- **`master_index.json`** - Complete project analysis index
- **`consolidation_summary.md`** - This summary report

### **Chunk Files:**
"""

        for chunk in master_index["chunks"]:
            summary += f"- **`{Path(chunk['file_path']).name}`** - {chunk['directory']} analysis\n"

        summary += """
---

## 🚀 **CONSOLIDATION STRATEGY**

### **High-Priority Chunks:**
Focus on chunks with the most consolidation opportunities for maximum impact.

### **Chunk Processing Order:**
1. **Core Modules** - Foundation consolidation
2. **Services** - Business logic optimization  
3. **Web Interface** - Frontend consolidation
4. **Utilities** - Common functionality unification
5. **Configuration** - Settings consolidation

### **Expected Results:**
- **Target File Reduction:** 60-70%
- **Maintenance Improvement:** Significant
- **Development Velocity:** Enhanced
- **Code Quality:** SOLID principles compliance

---

**🐝 WE ARE SWARM - Chunked analysis complete and ready for consolidation execution!**
"""

        # Save summary
        summary_file = self.output_dir / "consolidation_summary.md"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"📋 Consolidation summary: {summary_file}")


def main():
    """Main analysis function."""
    # Define analysis directories in manageable chunks
    analysis_directories = [
        "src/core",
        "src/services",
        "src/web",
        "src/utils",
        "src/infrastructure",
        "src/gaming",
        "src/trading_robot",
        "src/domain",
        "src/application",
        "src/architecture",
        "tests",
        "docs",
        "scripts",
        "tools",
    ]

    # Initialize analyzer
    analyzer = ProjectAnalyzer()

    # Generate chunked reports
    analyzer.generate_chunk_reports(analysis_directories)


if __name__ == "__main__":
    main()
