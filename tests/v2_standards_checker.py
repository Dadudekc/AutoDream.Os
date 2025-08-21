#!/usr/bin/env python3
"""
🧪 V2 STANDARDS CHECKER - AGENT_CELLPHONE_V2
Foundation & Testing Specialist - TDD Integration Project

V2 coding standards compliance checker for pre-commit hooks and quality assurance.
This tool validates all components meet V2 standards requirements.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import ast

# Add tests to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from conftest import TestConfig


class V2StandardsChecker:
    """V2 coding standards compliance checker."""
    
    def __init__(self, config: TestConfig):
        """Initialize V2 standards checker."""
        self.config = config
        self.violations = []
        self.checked_files = 0
        self.compliant_files = 0
        
        # V2 standards requirements
        self.standards = {
            'loc_compliance': {
                'core': self.config.MAX_LOC_CORE,
                'services': self.config.MAX_LOC_CORE,
                'launchers': self.config.MAX_LOC_CORE,
                'utils': self.config.MAX_LOC_CORE,
                'web': self.config.MAX_LOC_GUI,
                'standard': self.config.MAX_LOC_STANDARD
            },
            'oop_requirements': [
                'must_have_classes',
                'no_functions_outside_classes',
                'proper_inheritance'
            ],
            'cli_requirements': [
                'must_have_argparse',
                'must_have_main_function',
                'must_have_help_documentation'
            ],
            'srp_requirements': [
                'single_responsibility',
                'focused_imports',
                'clean_architecture'
            ]
        }
    
    def check_all_standards(self) -> Dict[str, Any]:
        """Check all V2 coding standards compliance."""
        print("🔍 V2 CODING STANDARDS COMPREHENSIVE CHECK")
        print("=" * 50)
        
        results = {
            'total_files': 0,
            'compliant_files': 0,
            'non_compliant_files': 0,
            'loc_violations': 0,
            'oop_violations': 0,
            'cli_violations': 0,
            'srp_violations': 0,
            'overall_compliance': 0.0
        }
        
        # Check each component category
        for category, description in self.config.COMPONENTS.items():
            category_dir = Path(f"src/{category}")
            if category_dir.exists():
                print(f"🔬 Checking {category.title()} Components...")
                category_results = self._check_component_category(category_dir, category)
                self._update_results(results, category_results)
                print(f"  ✅ {category.title()} check completed")
        
        # Calculate overall compliance
        if results['total_files'] > 0:
            results['overall_compliance'] = (results['compliant_files'] / results['total_files']) * 100
        
        # Print summary
        self._print_compliance_summary(results)
        
        return results
    
    def check_loc_compliance(self) -> Dict[str, Any]:
        """Check line count compliance for all components."""
        print("📏 V2 LOC COMPLIANCE CHECK")
        print("=" * 30)
        
        results = {
            'total_files': 0,
            'compliant_files': 0,
            'non_compliant_files': 0,
            'violations': []
        }
        
        # Check each component category
        for category, description in self.config.COMPONENTS.items():
            category_dir = Path(f"src/{category}")
            if category_dir.exists():
                print(f"🔬 Checking {category.title()} Components...")
                category_results = self._check_category_loc_compliance(category_dir, category)
                self._update_loc_results(results, category_results)
        
        # Print results
        self._print_loc_results(results)
        
        return results
    
    def check_oop_compliance(self) -> Dict[str, Any]:
        """Check OOP design compliance for all components."""
        print("🏗️  V2 OOP DESIGN COMPLIANCE CHECK")
        print("=" * 35)
        
        results = {
            'total_files': 0,
            'compliant_files': 0,
            'non_compliant_files': 0,
            'violations': []
        }
        
        # Check each component category
        for category, description in self.config.COMPONENTS.items():
            category_dir = Path(f"src/{category}")
            if category_dir.exists():
                print(f"🔬 Checking {category.title()} Components...")
                category_results = self._check_category_oop_compliance(category_dir, category)
                self._update_oop_results(results, category_results)
        
        # Print results
        self._print_oop_results(results)
        
        return results
    
    def check_cli_compliance(self) -> Dict[str, Any]:
        """Check CLI interface compliance for all components."""
        print("🖥️  V2 CLI INTERFACE COMPLIANCE CHECK")
        print("=" * 40)
        
        results = {
            'total_files': 0,
            'compliant_files': 0,
            'non_compliant_files': 0,
            'violations': []
        }
        
        # Check each component category
        for category, description in self.config.COMPONENTS.items():
            category_dir = Path(f"src/{category}")
            if category_dir.exists():
                print(f"🔬 Checking {category.title()} Components...")
                category_results = self._check_category_cli_compliance(category_dir, category)
                self._update_cli_results(results, category_results)
        
        # Print results
        self._print_cli_results(results)
        
        return results
    
    def check_srp_compliance(self) -> Dict[str, Any]:
        """Check single responsibility principle compliance for all components."""
        print("🎯 V2 SINGLE RESPONSIBILITY COMPLIANCE CHECK")
        print("=" * 45)
        
        results = {
            'total_files': 0,
            'compliant_files': 0,
            'non_compliant_files': 0,
            'violations': []
        }
        
        # Check each component category
        for category, description in self.config.COMPONENTS.items():
            category_dir = Path(f"src/{category}")
            if category_dir.exists():
                print(f"🔬 Checking {category.title()} Components...")
                category_results = self._check_category_srp_compliance(category_dir, category)
                self._update_srp_results(results, category_results)
        
        # Print results
        self._print_srp_results(results)
        
        return results
    
    def _check_component_category(self, category_dir: Path, category: str) -> Dict[str, Any]:
        """Check V2 standards compliance for a specific component category."""
        results = {
            'category': category,
            'files_checked': 0,
            'compliant_files': 0,
            'loc_violations': 0,
            'oop_violations': 0,
            'cli_violations': 0,
            'srp_violations': 0
        }
        
        # Check each Python file in category
        for py_file in category_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files
            
            results['files_checked'] += 1
            
            # Check LOC compliance
            if not self._check_file_loc_compliance(py_file, category):
                results['loc_violations'] += 1
            
            # Check OOP compliance
            if not self._check_file_oop_compliance(py_file):
                results['oop_violations'] += 1
            
            # Check CLI compliance
            if not self._check_file_cli_compliance(py_file):
                results['cli_violations'] += 1
            
            # Check SRP compliance
            if not self._check_file_srp_compliance(py_file):
                results['srp_violations'] += 1
            
            # File is compliant if no violations
            if (results['loc_violations'] == 0 and results['oop_violations'] == 0 and
                results['cli_violations'] == 0 and results['srp_violations'] == 0):
                results['compliant_files'] += 1
        
        return results
    
    def _check_category_loc_compliance(self, category_dir: Path, category: str) -> Dict[str, Any]:
        """Check LOC compliance for a specific component category."""
        results = {
            'category': category,
            'files_checked': 0,
            'compliant_files': 0,
            'violations': []
        }
        
        # Check each Python file in category
        for py_file in category_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files
            
            results['files_checked'] += 1
            
            if self._check_file_loc_compliance(py_file, category):
                results['compliant_files'] += 1
            else:
                # Get actual LOC count
                loc_count = self._count_file_loc(py_file)
                max_loc = self.standards['loc_compliance'].get(category, self.config.MAX_LOC_STANDARD)
                
                violation = {
                    'file': str(py_file),
                    'category': category,
                    'current_loc': loc_count,
                    'max_loc': max_loc,
                    'message': f"File exceeds {max_loc} LOC limit: {loc_count} lines"
                }
                results['violations'].append(violation)
        
        return results
    
    def _check_category_oop_compliance(self, category_dir: Path, category: str) -> Dict[str, Any]:
        """Check OOP compliance for a specific component category."""
        results = {
            'category': category,
            'files_checked': 0,
            'compliant_files': 0,
            'violations': []
        }
        
        # Check each Python file in category
        for py_file in category_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files
            
            results['files_checked'] += 1
            
            if self._check_file_oop_compliance(py_file):
                results['compliant_files'] += 1
            else:
                violation = {
                    'file': str(py_file),
                    'category': category,
                    'message': "File does not follow OOP design principles"
                }
                results['violations'].append(violation)
        
        return results
    
    def _check_category_cli_compliance(self, category_dir: Path, category: str) -> Dict[str, Any]:
        """Check CLI compliance for a specific component category."""
        results = {
            'category': category,
            'files_checked': 0,
            'compliant_files': 0,
            'violations': []
        }
        
        # Check each Python file in category
        for py_file in category_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files
            
            results['files_checked'] += 1
            
            if self._check_file_cli_compliance(py_file):
                results['compliant_files'] += 1
            else:
                violation = {
                    'file': str(py_file),
                    'category': category,
                    'message': "File does not have proper CLI interface"
                }
                results['violations'].append(violation)
        
        return results
    
    def _check_category_srp_compliance(self, category_dir: Path, category: str) -> Dict[str, Any]:
        """Check SRP compliance for a specific component category."""
        results = {
            'category': category,
            'files_checked': 0,
            'compliant_files': 0,
            'violations': []
        }
        
        # Check each Python file in category
        for py_file in category_dir.glob("*.py"):
            if py_file.name == "__init__.py":
                continue  # Skip init files
            
            results['files_checked'] += 1
            
            if self._check_file_srp_compliance(py_file):
                results['compliant_files'] += 1
            else:
                violation = {
                    'file': str(py_file),
                    'category': category,
                    'message': "File violates single responsibility principle"
                }
                results['violations'].append(violation)
        
        return results
    
    def _check_file_loc_compliance(self, file_path: Path, category: str) -> bool:
        """Check if file meets LOC requirements."""
        try:
            loc_count = self._count_file_loc(file_path)
            max_loc = self.standards['loc_compliance'].get(category, self.config.MAX_LOC_STANDARD)
            return loc_count <= max_loc
        except Exception:
            return False
    
    def _count_file_loc(self, file_path: Path) -> int:
        """Count actual lines of code in file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Filter out empty lines and comments
                code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
                return len(code_lines)
        except Exception:
            return 0
    
    def _check_file_oop_compliance(self, file_path: Path) -> bool:
        """Check if file follows OOP design principles."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Must have class definitions
                if 'class ' not in content:
                    return False
                
                # Check for functions outside classes (should be minimal)
                lines = content.split('\n')
                in_class = False
                functions_outside_classes = 0
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('class '):
                        in_class = True
                    elif line.startswith('def ') and not in_class:
                        functions_outside_classes += 1
                    elif line == '' or line.startswith('#'):
                        continue
                    elif line.startswith('if __name__'):
                        break
                
                # Allow main function and minimal utility functions
                return functions_outside_classes <= 2
                
        except Exception:
            return False
    
    def _check_file_cli_compliance(self, file_path: Path) -> bool:
        """Check if file has CLI interface."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Must have argparse usage
                if 'argparse' not in content:
                    return False
                
                # Must have main function or entry point
                if not ('def main(' in content or 'if __name__' in content):
                    return False
                
                # Must have help documentation
                if 'help=' not in content:
                    return False
                
                return True
                
        except Exception:
            return False
    
    def _check_file_srp_compliance(self, file_path: Path) -> bool:
        """Check if file follows single responsibility principle."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Count different types of operations
                operations = {
                    'file_ops': content.count('open(') + content.count('Path('),
                    'network_ops': content.count('requests.') + content.count('urllib.'),
                    'db_ops': content.count('sqlite') + content.count('database'),
                    'gui_ops': content.count('tkinter') + content.count('PyQt'),
                    'cli_ops': content.count('argparse') + content.count('click'),
                }
                
                # Should have primary focus on one area
                active_ops = sum(1 for count in operations.values() if count > 0)
                return active_ops <= 2
                
        except Exception:
            return False
    
    def _update_results(self, overall_results: Dict[str, Any], 
                       category_results: Dict[str, Any]) -> None:
        """Update overall results with category results."""
        overall_results['total_files'] += category_results['files_checked']
        overall_results['compliant_files'] += category_results['compliant_files']
        overall_results['non_compliant_files'] += (
            category_results['files_checked'] - category_results['compliant_files']
        )
        overall_results['loc_violations'] += category_results['loc_violations']
        overall_results['oop_violations'] += category_results['oop_violations']
        overall_results['cli_violations'] += category_results['cli_violations']
        overall_results['srp_violations'] += category_results['srp_violations']
    
    def _update_loc_results(self, overall_results: Dict[str, Any], 
                           category_results: Dict[str, Any]) -> None:
        """Update LOC results with category results."""
        overall_results['total_files'] += category_results['files_checked']
        overall_results['compliant_files'] += category_results['compliant_files']
        overall_results['non_compliant_files'] += (
            category_results['files_checked'] - category_results['compliant_files']
        )
        overall_results['violations'].extend(category_results['violations'])
    
    def _update_oop_results(self, overall_results: Dict[str, Any], 
                           category_results: Dict[str, Any]) -> None:
        """Update OOP results with category results."""
        overall_results['total_files'] += category_results['files_checked']
        overall_results['compliant_files'] += category_results['compliant_files']
        overall_results['non_compliant_files'] += (
            category_results['files_checked'] - category_results['compliant_files']
        )
        overall_results['violations'].extend(category_results['violations'])
    
    def _update_cli_results(self, overall_results: Dict[str, Any], 
                           category_results: Dict[str, Any]) -> None:
        """Update CLI results with category results."""
        overall_results['total_files'] += category_results['files_checked']
        overall_results['compliant_files'] += category_results['compliant_files']
        overall_results['non_compliant_files'] += (
            category_results['files_checked'] - category_results['compliant_files']
        )
        overall_results['violations'].extend(category_results['violations'])
    
    def _update_srp_results(self, overall_results: Dict[str, Any], 
                           category_results: Dict[str, Any]) -> None:
        """Update SRP results with category results."""
        overall_results['total_files'] += category_results['files_checked']
        overall_results['compliant_files'] += category_results['compliant_files']
        overall_results['non_compliant_files'] += (
            category_results['files_checked'] - category_results['compliant_files']
        )
        overall_results['violations'].extend(category_results['violations'])
    
    def _print_compliance_summary(self, results: Dict[str, Any]) -> None:
        """Print comprehensive compliance summary."""
        print("\n📊 V2 STANDARDS COMPLIANCE SUMMARY")
        print("=" * 40)
        
        print(f"📁 Total Files: {results['total_files']}")
        print(f"✅ Compliant Files: {results['compliant_files']}")
        print(f"❌ Non-Compliant Files: {results['non_compliant_files']}")
        print()
        
        print(f"📏 LOC Violations: {results['loc_violations']}")
        print(f"🏗️  OOP Violations: {results['oop_violations']}")
        print(f"🖥️  CLI Violations: {results['cli_violations']}")
        print(f"🎯 SRP Violations: {results['srp_violations']}")
        print()
        
        print(f"📈 Overall Compliance: {results['overall_compliance']:.1f}%")
        
        if results['overall_compliance'] >= 90:
            print("🏆 EXCELLENT - High V2 standards compliance!")
        elif results['overall_compliance'] >= 80:
            print("👍 GOOD - Solid V2 standards compliance")
        elif results['overall_compliance'] >= 70:
            print("⚠️  FAIR - Some V2 standards issues")
        else:
            print("🚨 POOR - Significant V2 standards violations")
        
        print("=" * 40)
    
    def _print_loc_results(self, results: Dict[str, Any]) -> None:
        """Print LOC compliance results."""
        print(f"\n📊 LOC Compliance Results")
        print(f"📁 Total Files: {results['total_files']}")
        print(f"✅ Compliant Files: {results['compliant_files']}")
        print(f"❌ Non-Compliant Files: {results['non_compliant_files']}")
        
        if results['violations']:
            print(f"\n🚨 LOC Violations:")
            for violation in results['violations']:
                print(f"  - {violation['file']}: {violation['message']}")
        
        print("=" * 30)
    
    def _print_oop_results(self, results: Dict[str, Any]) -> None:
        """Print OOP compliance results."""
        print(f"\n📊 OOP Design Compliance Results")
        print(f"📁 Total Files: {results['total_files']}")
        print(f"✅ Compliant Files: {results['compliant_files']}")
        print(f"❌ Non-Compliant Files: {results['non_compliant_files']}")
        
        if results['violations']:
            print(f"\n🚨 OOP Violations:")
            for violation in results['violations']:
                print(f"  - {violation['file']}: {violation['message']}")
        
        print("=" * 35)
    
    def _print_cli_results(self, results: Dict[str, Any]) -> None:
        """Print CLI compliance results."""
        print(f"\n📊 CLI Interface Compliance Results")
        print(f"📁 Total Files: {results['total_files']}")
        print(f"✅ Compliant Files: {results['compliant_files']}")
        print(f"❌ Non-Compliant Files: {results['non_compliant_files']}")
        
        if results['violations']:
            print(f"\n🚨 CLI Violations:")
            for violation in results['violations']:
                print(f"  - {violation['file']}: {violation['message']}")
        
        print("=" * 40)
    
    def _print_srp_results(self, results: Dict[str, Any]) -> None:
        """Print SRP compliance results."""
        print(f"\n📊 Single Responsibility Compliance Results")
        print(f"📁 Total Files: {results['total_files']}")
        print(f"✅ Compliant Files: {results['compliant_files']}")
        print(f"❌ Non-Compliant Files: {results['non_compliant_files']}")
        
        if results['violations']:
            print(f"\n🚨 SRP Violations:")
            for violation in results['violations']:
                print(f"  - {violation['file']}: {violation['message']}")
        
        print("=" * 45)


def main():
    """Main entry point for V2 standards checker."""
    parser = argparse.ArgumentParser(
        description="🧪 V2 Standards Checker - Agent_Cellphone_V2"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Check all V2 standards compliance"
    )
    
    parser.add_argument(
        "--loc-check", "-l",
        action="store_true",
        help="Check LOC compliance only"
    )
    
    parser.add_argument(
        "--oop-check", "-o",
        action="store_true",
        help="Check OOP design compliance only"
    )
    
    parser.add_argument(
        "--cli-check", "-c",
        action="store_true",
        help="Check CLI interface compliance only"
    )
    
    parser.add_argument(
        "--srp-check", "-s",
        action="store_true",
        help="Check single responsibility principle only"
    )
    
    args = parser.parse_args()
    
    # Initialize checker
    config = TestConfig()
    checker = V2StandardsChecker(config)
    
    try:
        if args.all:
            # Check all standards
            results = checker.check_all_standards()
            exit_code = 0 if results['overall_compliance'] >= 80 else 1
        elif args.loc_check:
            # Check LOC compliance only
            results = checker.check_loc_compliance()
            exit_code = 0 if results['non_compliant_files'] == 0 else 1
        elif args.oop_check:
            # Check OOP compliance only
            results = checker.check_oop_compliance()
            exit_code = 0 if results['non_compliant_files'] == 0 else 1
        elif args.cli_check:
            # Check CLI compliance only
            results = checker.check_cli_compliance()
            exit_code = 0 if results['non_compliant_files'] == 0 else 1
        elif args.srp_check:
            # Check SRP compliance only
            results = checker.check_srp_compliance()
            exit_code = 0 if results['non_compliant_files'] == 0 else 1
        else:
            # Default: check all standards
            results = checker.check_all_standards()
            exit_code = 0 if results['overall_compliance'] >= 80 else 1
        
        # Exit with appropriate code
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"💥 V2 standards check failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
