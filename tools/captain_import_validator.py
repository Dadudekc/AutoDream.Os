#!/usr/bin/env python3
"""
Import Validator - Detect Missing Imports Before Runtime
Validates all imports in a file or directory to prevent runtime errors.
"""

import sys
import ast
from pathlib import Path
from typing import List, Tuple

repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))


def extract_imports(file_path: Path) -> List[Tuple[str, int]]:
    """Extract all import statements from a file."""
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(file_path))
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((alias.name, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append((f"{module}.{alias.name}" if module else alias.name, node.lineno))
    except Exception as e:
        print(f"⚠️  Could not parse {file_path}: {e}")
    
    return imports


def validate_import(import_name: str) -> Tuple[bool, str]:
    """Validate if an import is available."""
    try:
        parts = import_name.split('.')
        module_name = parts[0]
        
        # Try to import the module
        __import__(module_name)
        return True, "✅ Valid"
    except ImportError as e:
        return False, f"❌ Missing: {e}"
    except Exception as e:
        return False, f"⚠️  Error: {e}"


def validate_file_imports(file_path: Path) -> dict:
    """Validate all imports in a file."""
    imports = extract_imports(file_path)
    results = {
        'file': str(file_path),
        'total_imports': len(imports),
        'valid': [],
        'invalid': []
    }
    
    for import_name, line_no in imports:
        is_valid, message = validate_import(import_name)
        
        if is_valid:
            results['valid'].append({
                'import': import_name,
                'line': line_no,
                'status': message
            })
        else:
            results['invalid'].append({
                'import': import_name,
                'line': line_no,
                'status': message
            })
    
    return results


def main():
    """Validate imports in specified file or directory."""
    
    if len(sys.argv) < 2:
        print("Usage: python captain_import_validator.py <file-or-directory>")
        print("\nExamples:")
        print("  python captain_import_validator.py src/core/messaging_pyautogui.py")
        print("  python captain_import_validator.py src/services/")
        return 1
    
    target = Path(sys.argv[1])
    
    if not target.exists():
        print(f"❌ Path not found: {target}")
        return 1
    
    # Collect files to validate
    files_to_check = []
    if target.is_file():
        files_to_check.append(target)
    else:
        files_to_check.extend(target.rglob("*.py"))
    
    print(f"🔍 IMPORT VALIDATION")
    print(f"=" * 60)
    print(f"Target: {target}")
    print(f"Files to check: {len(files_to_check)}")
    print(f"=" * 60)
    print()
    
    total_issues = 0
    files_with_issues = 0
    
    for file_path in files_to_check:
        results = validate_file_imports(file_path)
        
        if results['invalid']:
            files_with_issues += 1
            print(f"\n⚠️  {file_path.relative_to(repo_root)}")
            print(f"   Total imports: {results['total_imports']}")
            print(f"   Valid: {len(results['valid'])}")
            print(f"   Invalid: {len(results['invalid'])}")
            print()
            
            for issue in results['invalid']:
                total_issues += 1
                print(f"   Line {issue['line']}: {issue['import']}")
                print(f"      {issue['status']}")
            print()
    
    print(f"=" * 60)
    print(f"📊 SUMMARY")
    print(f"=" * 60)
    print(f"Files checked: {len(files_to_check)}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Total import issues: {total_issues}")
    
    if total_issues == 0:
        print("\n✅ All imports are valid!")
        return 0
    else:
        print(f"\n❌ Found {total_issues} import issues in {files_with_issues} files!")
        return 1

if __name__ == "__main__":
    sys.exit(main())

