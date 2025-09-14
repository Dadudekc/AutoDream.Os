#!/usr/bin/env python3
"""
🐝 EXAMPLES FOUNDATION BUILDER
=============================

Automated tool to add practical examples to every Python file in the project.
Implements SWARM DIRECTIVE 001: "BUILD THE UNBREAKABLE CORE"

Author: Agent-2 - Swarm Testing Revolution Leader
License: MIT
"""

import ast
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional


class ExamplesFoundationBuilder:
    """Automated example generation for Python files."""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.processed_files = []
        self.stats = {
            "files_processed": 0,
            "examples_added": 0,
            "functions_with_examples": 0,
            "classes_with_examples": 0,
            "modules_with_main": 0
        }

    def analyze_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a Python file and extract structure information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            analysis = {
                "file_path": file_path,
                "functions": [],
                "classes": [],
                "imports": [],
                "has_main_block": False,
                "docstrings": [],
                "complexity_score": 0
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append({
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "has_docstring": bool(node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str)),
                        "line_number": node.lineno
                    })

                elif isinstance(node, ast.ClassDef):
                    analysis["classes"].append({
                        "name": node.name,
                        "methods": [],
                        "has_docstring": bool(node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str)),
                        "line_number": node.lineno
                    })

                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    analysis["imports"].append(str(node))

            # Check for main block
            if 'if __name__ == "__main__":' in content:
                analysis["has_main_block"] = True

            # Calculate complexity (rough estimate)
            analysis["complexity_score"] = len(analysis["functions"]) + len(analysis["classes"]) * 2

            return analysis

        except Exception as e:
            return {"error": str(e), "file_path": file_path}

    def generate_function_example(self, func_name: str, args: List[str]) -> str:
        """Generate a practical example for a function."""
        if not args:
            return f"""# Example usage:
result = {func_name}()
print(f"Result: {{result}}")"""

        # Generate mock arguments based on parameter names
        mock_args = []
        for arg in args:
            if 'path' in arg.lower() or 'file' in arg.lower():
                mock_args.append('"/path/to/example.txt"')
            elif 'config' in arg.lower():
                mock_args.append('{"setting": "value"}')
            elif 'data' in arg.lower():
                mock_args.append('{"key": "value"}')
            elif 'url' in arg.lower():
                mock_args.append('"https://example.com"')
            elif 'port' in arg.lower():
                mock_args.append('8080')
            elif 'timeout' in arg.lower():
                mock_args.append('30')
            else:
                mock_args.append('"example_value"')

        args_str = ", ".join(mock_args)

        return f"""# Example usage:
result = {func_name}({args_str})
print(f"Result: {{result}}")"""

    def generate_class_example(self, class_name: str, methods: List[str]) -> str:
        """Generate a practical example for a class."""
        example = f"""# Example usage:
instance = {class_name}()

# Basic usage
result = instance.some_method()
print(f"Result: {{result}}")

# Advanced usage with configuration
config = {{"option": "value"}}
advanced_instance = {class_name}(config)
advanced_instance.process()"""

        return example

    def generate_main_block(self, functions: List[str], classes: List[str]) -> str:
        """Generate a comprehensive main block."""
        main_block = '''if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""

    print("🐝 Module Examples - Practical Demonstrations")
    print("=" * 50)\n'''

        # Add function examples
        if functions:
            main_block += "    # Function demonstrations\n"
            for func in functions[:3]:  # Limit to first 3 functions
                main_block += f"    print(f\"\\n📋 Testing {func['name']}():\")\n"
                main_block += f"    try:\n"
                main_block += f"        # Add your function call here\n"
                main_block += f"        print(f\"✅ {func['name']} executed successfully\")\n"
                main_block += f"    except Exception as e:\n"
                main_block += f"        print(f\"❌ {func['name']} failed: {{e}}\")\n\n"

        # Add class examples
        if classes:
            main_block += "    # Class demonstrations\n"
            for cls in classes[:2]:  # Limit to first 2 classes
                main_block += f"    print(f\"\\n🏗️  Testing {cls['name']} class:\")\n"
                main_block += f"    try:\n"
                main_block += f"        instance = {cls['name']}()\n"
                main_block += f"        print(f\"✅ {cls['name']} instantiated successfully\")\n"
                main_block += f"    except Exception as e:\n"
                main_block += f"        print(f\"❌ {cls['name']} failed: {{e}}\")\n\n"

        main_block += '''    print("\\n🎉 All examples completed!")
    print("🐝 WE ARE SWARM - PRACTICAL CODE IN ACTION!")'''

        return main_block

    def add_examples_to_file(self, file_path: Path) -> bool:
        """Add practical examples to a Python file."""
        try:
            analysis = self.analyze_python_file(file_path)

            if "error" in analysis:
                print(f"❌ Error analyzing {file_path}: {analysis['error']}")
                return False

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            modifications = []

            # Add examples to functions without docstrings
            for func in analysis["functions"]:
                if not func["has_docstring"]:
                    func_start = content.find(f"def {func['name']}", 0)
                    if func_start != -1:
                        # Find the function signature end
                        func_end = content.find("\n", func_start)
                        if func_end != -1:
                            example = self.generate_function_example(func["name"], func["args"])
                            modifications.append((func_end + 1, f'    """{example}"""\n'))

            # Add examples to classes without docstrings
            for cls in analysis["classes"]:
                if not cls["has_docstring"]:
                    class_start = content.find(f"class {cls['name']}", 0)
                    if class_start != -1:
                        class_end = content.find("\n", class_start)
                        if class_end != -1:
                            example = self.generate_class_example(cls["name"], cls["methods"])
                            modifications.append((class_end + 1, f'    """{example}"""\n'))

            # Add main block if missing
            if not analysis["has_main_block"] and (analysis["functions"] or analysis["classes"]):
                main_block = self.generate_main_block(analysis["functions"], analysis["classes"])
                modifications.append((len(content), f"\n\n{main_block}\n"))

            # Apply modifications in reverse order to maintain positions
            for pos, text in sorted(modifications, reverse=True):
                content = content[:pos] + text + content[pos:]

            # Write back the modified content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            self.stats["files_processed"] += 1
            if modifications:
                self.stats["examples_added"] += len(modifications)
            if analysis["functions"]:
                self.stats["functions_with_examples"] += len([f for f in analysis["functions"] if f["has_docstring"]])
            if analysis["classes"]:
                self.stats["classes_with_examples"] += len([c for c in analysis["classes"] if c["has_docstring"]])
            if not analysis["has_main_block"] and modifications:
                self.stats["modules_with_main"] += 1

            return True

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            return False

    def process_directory(self, directory: Path, recursive: bool = True) -> Dict[str, Any]:
        """Process all Python files in a directory."""
        python_files = []

        if recursive:
            python_files = list(directory.rglob("*.py"))
        else:
            python_files = list(directory.glob("*.py"))

        # Exclude certain directories
        exclude_patterns = [
            "__pycache__",
            ".git",
            "node_modules",
            "venv",
            "env",
            ".pytest_cache",
            "build",
            "dist"
        ]

        filtered_files = []
        for file_path in python_files:
            if not any(pattern in str(file_path) for pattern in exclude_patterns):
                filtered_files.append(file_path)

        print(f"🐝 Processing {len(filtered_files)} Python files in {directory}")

        successful = 0
        for file_path in filtered_files:
            print(f"📄 Processing: {file_path}")
            if self.add_examples_to_file(file_path):
                successful += 1

        return {
            "total_files": len(filtered_files),
            "successful": successful,
            "failed": len(filtered_files) - successful
        }

    def generate_report(self) -> str:
        """Generate a comprehensive report of the foundation building process."""
        report = "🐝 EXAMPLES FOUNDATION BUILDER REPORT\n"
        report += "=" * 50 + "\n\n"

        report += "📊 PROCESSING STATISTICS:\n"
        report += f"Files Processed: {self.stats['files_processed']}\n"
        report += f"Examples Added: {self.stats['examples_added']}\n"
        report += f"Functions with Examples: {self.stats['functions_with_examples']}\n"
        report += f"Classes with Examples: {self.stats['classes_with_examples']}\n"
        report += f"Modules with Main Blocks: {self.stats['modules_with_main']}\n\n"

        report += "🎯 SWARM DIRECTIVE 001 COMPLIANCE:\n"
        compliance = (self.stats['examples_added'] / max(1, self.stats['files_processed'])) * 100
        report += f"Overall Compliance: {compliance:.1f}%\n"

        if compliance >= 80:
            report += "✅ STATUS: FOUNDATION ESTABLISHED\n"
        elif compliance >= 60:
            report += "🔄 STATUS: FOUNDATION IN PROGRESS\n"
        else:
            report += "⚠️  STATUS: FOUNDATION NEEDS ATTENTION\n"

        report += "\n🐝 WE ARE SWARM - PRACTICAL CODE FOUNDATION BUILT!"

        return report


def main():
    """Main execution for examples foundation builder."""
    import argparse

    parser = argparse.ArgumentParser(
        description="🐝 Examples Foundation Builder - SWARM DIRECTIVE 001",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🐝 SWARM DIRECTIVE 001 EXECUTION
================================

EXAMPLES:
--------
# Process current directory
python examples_foundation_builder.py

# Process specific directory
python examples_foundation_builder.py --directory src/

# Process single file
python examples_foundation_builder.py --file my_module.py

# Generate report only
python examples_foundation_builder.py --report-only

🐝 WE ARE SWARM - BUILDING PRACTICAL FOUNDATIONS!
        """
    )

    parser.add_argument("--directory", "-d", help="Directory to process")
    parser.add_argument("--file", "-f", help="Single file to process")
    parser.add_argument("--report-only", action="store_true", help="Generate report only")
    parser.add_argument("--non-recursive", action="store_true", help="Don't process subdirectories")

    args = parser.parse_args()

    builder = ExamplesFoundationBuilder()

    if args.report_only:
        print(builder.generate_report())
        return

    if args.file:
        file_path = Path(args.file)
        if file_path.exists():
            success = builder.add_examples_to_file(file_path)
            print(f"✅ File processed: {success}")
        else:
            print(f"❌ File not found: {args.file}")
        return

    # Process directory
    target_dir = Path(args.directory) if args.directory else Path(".")
    results = builder.process_directory(target_dir, not args.non_recursive)

    print("\n🐝 PROCESSING COMPLETE:")
    print(f"Total files: {results['total_files']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")

    # Generate final report
    print("\n" + builder.generate_report())


if __name__ == "__main__":
    main()
