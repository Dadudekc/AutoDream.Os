#!/usr/bin/env python3
"""
Simplified V2 Coding Standards Checker
======================================

This version doesn't depend on pytest or conftest.py
"""

import os
import sys
import ast
import argparse

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import List, Dict, Tuple


class V2StandardsChecker:
    """Simplified V2 coding standards checker"""
    
    def __init__(self):
        # Updated LOC restrictions - balanced approach for maintainability
        self.max_loc_standard = 400  # Good balance for standard files
        self.max_loc_gui = 600       # Generous for UI code while maintaining structure
        self.max_loc_core = 400      # Keep core logic focused and testable
        
    def check_file(self, file_path: Path) -> Dict[str, any]:
        """Check a single file for V2 standards compliance"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # LOC check
            loc_count = len(lines)
            loc_compliant = loc_count <= self.max_loc_standard
            
            # OOP check - improved version
            try:
                tree = ast.parse(content)
                has_classes = any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
                has_functions_outside_classes = False
                
                # Track class context
                class_stack = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        class_stack.append(node)
                    elif isinstance(node, ast.FunctionDef):
                        # Check if this function is inside a class
                        in_class = False
                        for class_node in class_stack:
                            if (hasattr(node, 'lineno') and hasattr(class_node, 'lineno') and
                                hasattr(node, 'end_lineno') and hasattr(class_node, 'end_lineno')):
                                if (node.lineno >= class_node.lineno and 
                                    node.end_lineno <= class_node.end_lineno):
                                    in_class = True
                                    break
                        
                        if not in_class:
                            has_functions_outside_classes = True
                            break
                
                # If we have classes, functions should be inside them
                oop_compliant = has_classes and not has_functions_outside_classes
                
            except:
                oop_compliant = False
                
            # CLI check
            has_main = "if __name__ == '__main__'" in content or "def main()" in content
            has_argparse = "argparse" in content or "ArgumentParser" in content
            cli_compliant = not has_main or has_argparse
            
            return {
                'file_path': str(file_path),
                'loc_count': loc_count,
                'loc_compliant': loc_compliant,
                'oop_compliant': oop_compliant,
                'cli_compliant': cli_compliant,
                'overall_compliant': loc_compliant and oop_compliant and cli_compliant
            }
            
        except Exception as e:
            return {
                'file_path': str(file_path),
                'error': str(e),
                'overall_compliant': False
            }
    
    def check_directory(self, root_path: str) -> List[Dict[str, any]]:
        """Check all Python files in a directory"""
        results = []
        root = Path(root_path)
        
        for py_file in root.rglob("*.py"):
            if py_file.is_file():
                result = self.check_file(py_file)
                results.append(result)
                
        return results
    
    def generate_report(self, results: List[Dict[str, any]]) -> str:
        """Generate a compliance report"""
        total_files = len(results)
        compliant_files = sum(1 for r in results if r.get('overall_compliant', False))
        compliance_rate = (compliant_files / total_files * 100) if total_files > 0 else 0
        
        report = []
        report.append("V2 CODING STANDARDS COMPLIANCE REPORT")
        report.append("=" * 50)
        report.append(f"Total Files: {total_files}")
        report.append(f"Compliant Files: {compliant_files}")
        report.append(f"Compliance Rate: {compliance_rate:.1f}%")
        report.append("")
        
        # Group by compliance status
        compliant = [r for r in results if r.get('overall_compliant', False)]
        non_compliant = [r for r in results if not r.get('overall_compliant', False)]
        
        if compliant:
            report.append("COMPLIANT FILES:")
            for r in compliant[:10]:  # Show first 10
                report.append(f"  {r['file_path']}")
            if len(compliant) > 10:
                report.append(f"  ... and {len(compliant) - 10} more")
            report.append("")
            
        if non_compliant:
            report.append("NON-COMPLIANT FILES:")
            for r in non_compliant[:10]:  # Show first 10
                report.append(f"  {r['file_path']}")
                if 'error' in r:
                    report.append(f"    Error: {r['error']}")
                else:
                    issues = []
                    if not r.get('loc_compliant', True):
                        issues.append(f"LOC: {r.get('loc_count', 'N/A')} lines")
                    if not r.get('oop_compliant', True):
                        issues.append("OOP: Functions outside classes")
                    if not r.get('cli_compliant', True):
                        issues.append("CLI: Missing argparse")
                    if issues:
                        report.append(f"    Issues: {', '.join(issues)}")
            if len(non_compliant) > 10:
                report.append(f"  ... and {len(non_compliant) - 10} more")
                
        return '\n'.join(report)


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="V2 Coding Standards Checker")
    parser.add_argument('--path', default='.', help='Path to check (default: current directory)')
    parser.add_argument('--all', action='store_true', help='Check all files')
    
    args = parser.parse_args()
    
    checker = V2StandardsChecker()
    results = checker.check_directory(args.path)
    
    report = checker.generate_report(results)
    print(report)
    
    # Exit with appropriate code
    compliant_count = sum(1 for r in results if r.get('overall_compliant', False))
    if compliant_count == len(results):
        sys.exit(0)  # All compliant
    else:
        sys.exit(1)  # Some non-compliant


if __name__ == "__main__":
    main()
