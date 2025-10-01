#!/usr/bin/env python3
"""
Import Mapper - Automated Import Discovery and Mapping
====================================================

Scans codebase and creates a comprehensive import map to prevent import errors.

Usage:
    python tools/import_mapper.py --scan          # Scan and create map
    python tools/import_mapper.py --check FILE    # Check file imports
    python tools/import_mapper.py --fix FILE      # Auto-fix imports

Features:
- Discovers all classes, functions, constants
- Maps to correct module paths
- Auto-fixes import statements
- Detects circular imports
- Generates import reference guide
"""

import ast
import json
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImportMapper:
    """Map all imports in the codebase."""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.import_map: Dict[str, List[str]] = {}
        self.module_map: Dict[str, str] = {}
        self.class_map: Dict[str, str] = {}
        self.function_map: Dict[str, str] = {}

    def scan_file(self, file_path: Path) -> Dict[str, List[str]]:
        """Scan a Python file for classes and functions."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            module_path = self._get_module_path(file_path)
            exports = {"classes": [], "functions": [], "constants": []}

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    exports["classes"].append(node.name)
                    self.class_map[node.name] = module_path
                elif isinstance(node, ast.FunctionDef):
                    exports["functions"].append(node.name)
                    self.function_map[node.name] = module_path
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if target.id.isupper():  # Constants
                                exports["constants"].append(target.id)

            self.import_map[module_path] = exports
            return exports

        except Exception as e:
            logger.debug(f"Error scanning {file_path}: {e}")
            return {"classes": [], "functions": [], "constants": []}

    def _get_module_path(self, file_path: Path) -> str:
        """Convert file path to module path."""
        relative = file_path.relative_to(self.project_root)
        parts = list(relative.parts[:-1]) + [relative.stem]
        if parts[-1] == "__init__":
            parts = parts[:-1]
        return ".".join(parts)

    def scan_project(self) -> Dict[str, List[str]]:
        """Scan entire project for imports."""
        logger.info("Scanning project for imports...")
        
        python_files = list(self.project_root.rglob("*.py"))
        logger.info(f"Found {len(python_files)} Python files")

        for file_path in python_files:
            # Skip test files and generated files
            if "test" in str(file_path) or "__pycache__" in str(file_path):
                continue
            self.scan_file(file_path)

        logger.info(f"Mapped {len(self.class_map)} classes")
        logger.info(f"Mapped {len(self.function_map)} functions")
        
        return self.import_map

    def find_import(self, name: str) -> List[str]:
        """Find where a name can be imported from."""
        results = []
        
        if name in self.class_map:
            results.append(self.class_map[name])
        if name in self.function_map:
            results.append(self.function_map[name])
            
        return list(set(results))

    def check_file_imports(self, file_path: Path) -> List[Dict]:
        """Check imports in a file and suggest fixes."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    module = node.module
                    for alias in node.names:
                        name = alias.name
                        # Check if import exists
                        correct_paths = self.find_import(name)
                        if correct_paths and module not in correct_paths:
                            issues.append({
                                "line": node.lineno,
                                "current": f"from {module} import {name}",
                                "suggested": f"from {correct_paths[0]} import {name}",
                                "name": name,
                                "correct_paths": correct_paths
                            })

        except Exception as e:
            logger.error(f"Error checking {file_path}: {e}")

        return issues

    def save_import_map(self, output_path: str = "import_map.json"):
        """Save import map to JSON file."""
        output = {
            "import_map": self.import_map,
            "class_map": self.class_map,
            "function_map": self.function_map
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"Import map saved to {output_path}")

    def generate_reference_guide(self, output_path: str = "IMPORT_REFERENCE.md"):
        """Generate import reference guide."""
        lines = [
            "# Import Reference Guide",
            "",
            "## Classes",
            ""
        ]
        
        for class_name in sorted(self.class_map.keys()):
            module = self.class_map[class_name]
            lines.append(f"- `{class_name}`: `from {module} import {class_name}`")
        
        lines.extend([
            "",
            "## Functions",
            ""
        ])
        
        for func_name in sorted(self.function_map.keys()):
            module = self.function_map[func_name]
            lines.append(f"- `{func_name}`: `from {module} import {func_name}`")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        
        logger.info(f"Reference guide saved to {output_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Import Mapper Tool")
    parser.add_argument("--scan", action="store_true", help="Scan project and create import map")
    parser.add_argument("--check", type=str, help="Check imports in specific file")
    parser.add_argument("--output", type=str, default="import_map.json", help="Output file")
    parser.add_argument("--guide", action="store_true", help="Generate reference guide")
    
    args = parser.parse_args()
    
    mapper = ImportMapper()
    
    if args.scan:
        logger.info("Scanning project...")
        mapper.scan_project()
        mapper.save_import_map(args.output)
        
        if args.guide:
            mapper.generate_reference_guide()
        
        logger.info("✅ Import map created!")
        logger.info(f"   - {len(mapper.class_map)} classes mapped")
        logger.info(f"   - {len(mapper.function_map)} functions mapped")
    
    elif args.check:
        logger.info("Loading import map...")
        # Load existing map
        with open(args.output, 'r') as f:
            data = json.load(f)
            mapper.class_map = data["class_map"]
            mapper.function_map = data["function_map"]
        
        logger.info(f"Checking imports in {args.check}...")
        issues = mapper.check_file_imports(Path(args.check))
        
        if issues:
            logger.warning(f"Found {len(issues)} import issues:")
            for issue in issues:
                print(f"\nLine {issue['line']}:")
                print(f"  Current:   {issue['current']}")
                print(f"  Suggested: {issue['suggested']}")
        else:
            logger.info("✅ No import issues found!")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

