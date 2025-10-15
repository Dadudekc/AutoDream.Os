#!/usr/bin/env python3
"""
Pattern Extractor - Semi-Automated Code Pattern Extraction
Agent-8 (QA & Autonomous Systems Specialist)

Purpose: Assist in extracting code patterns from source repos
Impact: 30 min manual → 5 min semi-automated!
"""

import argparse
import ast
import shutil
from pathlib import Path
from typing import List, Dict, Any


class PatternAnalyzer(ast.NodeVisitor):
    """Analyze Python file for extractable patterns."""
    
    def __init__(self):
        self.classes = []
        self.functions = []
        self.imports = []
    
    def visit_ClassDef(self, node):
        """Extract class information."""
        self.classes.append({
            "name": node.name,
            "lineno": node.lineno,
            "end_lineno": node.end_lineno,
            "lines": node.end_lineno - node.lineno + 1 if node.end_lineno else 0,
            "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
        })
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        """Extract function information."""
        # Only top-level functions (not methods)
        if not isinstance(getattr(node, 'parent', None), ast.ClassDef):
            self.functions.append({
                "name": node.name,
                "lineno": node.lineno,
                "end_lineno": node.end_lineno,
                "lines": node.end_lineno - node.lineno + 1 if node.end_lineno else 0
            })
        self.generic_visit(node)
    
    def visit_Import(self, node):
        """Extract import statements."""
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Extract from-imports."""
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)


def analyze_file(filepath: Path) -> Dict[str, Any]:
    """Analyze a Python file for extractable patterns."""
    try:
        content = filepath.read_text(encoding='utf-8')
        tree = ast.parse(content)
        
        analyzer = PatternAnalyzer()
        analyzer.visit(tree)
        
        return {
            "file": str(filepath),
            "classes": analyzer.classes,
            "functions": analyzer.functions,
            "imports": list(set(analyzer.imports)),
            "total_lines": len(content.splitlines())
        }
    except SyntaxError as e:
        return {"file": str(filepath), "error": f"Syntax error: {e}"}
    except Exception as e:
        return {"file": str(filepath), "error": str(e)}


def extract_class(source_file: Path, class_name: str, dest_file: Path, dry_run: bool = False):
    """Extract a specific class to destination file."""
    analysis = analyze_file(source_file)
    
    if "error" in analysis:
        print(f"❌ Cannot extract: {analysis['error']}")
        return False
    
    # Find the class
    target_class = None
    for cls in analysis['classes']:
        if cls['name'] == class_name:
            target_class = cls
            break
    
    if not target_class:
        print(f"❌ Class '{class_name}' not found in {source_file.name}")
        print(f"   Available: {', '.join([c['name'] for c in analysis['classes']])}")
        return False
    
    print(f"\n📦 Extracting Class: {class_name}")
    print(f"   From: {source_file}")
    print(f"   To: {dest_file}")
    print(f"   Lines: {target_class['lines']}")
    print(f"   Methods: {', '.join(target_class['methods'][:5])}")
    
    if dry_run:
        print(f"\n🔍 DRY RUN - Not actually extracting")
        return False
    
    # Read source
    lines = source_file.read_text(encoding='utf-8').splitlines()
    
    # Extract class lines
    start = target_class['lineno'] - 1  # 0-indexed
    end = target_class['end_lineno']
    class_lines = lines[start:end]
    
    # Extract necessary imports (simple approach)
    import_lines = [line for line in lines[:target_class['lineno']] if line.strip().startswith('import') or line.strip().startswith('from')]
    
    # Create destination file
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write extracted code
    output = []
    output.append(f'"""')
    output.append(f'Extracted from {source_file.name}')
    output.append(f'Class: {class_name}')
    output.append(f'Extracted by: Agent-8')
    output.append(f'Date: {datetime.now().strftime("%Y-%m-%d")}')
    output.append(f'"""')
    output.append('')
    output.extend(import_lines)
    output.append('')
    output.extend(class_lines)
    
    dest_file.write_text('\n'.join(output), encoding='utf-8')
    
    print(f"\n✅ Class extracted successfully!")
    print(f"   Created: {dest_file}")
    return True


def list_extractables(source_file: Path):
    """List all extractable patterns in a file."""
    analysis = analyze_file(source_file)
    
    if "error" in analysis:
        print(f"❌ Error: {analysis['error']}")
        return
    
    print(f"\n📋 EXTRACTABLE PATTERNS IN {source_file.name}")
    print(f"="*70)
    print(f"Total Lines: {analysis['total_lines']}")
    
    print(f"\n🏛️  CLASSES ({len(analysis['classes'])}):")
    for cls in analysis['classes']:
        print(f"  - {cls['name']} ({cls['lines']} lines, {len(cls['methods'])} methods)")
        print(f"    Lines: {cls['lineno']}-{cls['end_lineno']}")
    
    print(f"\n🔧 FUNCTIONS ({len(analysis['functions'])}):")
    for func in analysis['functions']:
        print(f"  - {func['name']} ({func['lines']} lines)")
    
    print(f"\n📦 IMPORTS ({len(analysis['imports'])}):")
    for imp in analysis['imports'][:10]:
        print(f"  - {imp}")
    if len(analysis['imports']) > 10:
        print(f"  ... and {len(analysis['imports']) - 10} more")
    
    print(f"="*70)


def main():
    parser = argparse.ArgumentParser(
        description="Pattern Extractor - Semi-automated code extraction",
        epilog="Examples:\n"
               "  List: python tools/pattern_extractor.py --list source.py\n"
               "  Extract class: python tools/pattern_extractor.py --extract-class MyClass --from source.py --to dest.py\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--list', type=Path, help='List extractable patterns in file')
    parser.add_argument('--extract-class', help='Class name to extract')
    parser.add_argument('--from', dest='source', type=Path, help='Source file')
    parser.add_argument('--to', dest='dest', type=Path, help='Destination file')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    
    args = parser.parse_args()
    
    if args.list:
        list_extractables(args.list)
    elif args.extract_class:
        if not args.source or not args.dest:
            print("❌ --from and --to required for extraction!")
            parser.print_help()
            sys.exit(1)
        extract_class(args.source, args.extract_class, args.dest, args.dry_run)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

