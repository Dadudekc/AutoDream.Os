#!/usr/bin/env python3
"""
Professional Code Reduction Analyzer
===================================

Analyzes the codebase for opportunities to reduce code without losing functionality.
Focuses on professional software engineering practices.

Author: Agent-3 (Database Specialist)
License: MIT
"""

import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, Counter
import json

class CodeReductionAnalyzer:
    """Professional code reduction analyzer."""
    
    def __init__(self, project_root: str = "."):
        """Initialize analyzer."""
        self.project_root = Path(project_root)
        self.analysis_results = {
            "duplicate_functions": [],
            "duplicate_classes": [],
            "redundant_imports": [],
            "unused_imports": [],
            "duplicate_code_blocks": [],
            "overly_complex_functions": [],
            "redundant_data_structures": [],
            "optimization_opportunities": [],
            "statistics": {}
        }
    
    def analyze_python_files(self) -> List[Path]:
        """Get all Python files for analysis."""
        python_files = []
        for py_file in self.project_root.rglob("*.py"):
            if "__pycache__" not in str(py_file) and ".git" not in str(py_file):
                python_files.append(py_file)
        return python_files
    
    def extract_functions(self, file_path: Path) -> List[Dict]:
        """Extract function information from Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Get function signature
                    args = [arg.arg for arg in node.args.args]
                    
                    # Get function body (simplified)
                    body_lines = []
                    for stmt in node.body:
                        if isinstance(stmt, ast.Return):
                            body_lines.append("return")
                        elif isinstance(stmt, ast.Assign):
                            for target in stmt.targets:
                                if isinstance(target, ast.Name):
                                    body_lines.append(f"assign_{target.id}")
                        elif isinstance(stmt, ast.Expr):
                            if isinstance(stmt.value, ast.Call):
                                if isinstance(stmt.value.func, ast.Name):
                                    body_lines.append(f"call_{stmt.value.func.id}")
                    
                    functions.append({
                        "name": node.name,
                        "file": str(file_path),
                        "args": args,
                        "body_signature": "|".join(body_lines),
                        "line_count": len(node.body),
                        "complexity": self._calculate_complexity(node)
                    })
            
            return functions
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return []
    
    def _calculate_complexity(self, node) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
        return complexity
    
    def find_duplicate_functions(self, python_files: List[Path]) -> List[Dict]:
        """Find duplicate or very similar functions."""
        all_functions = []
        
        for py_file in python_files:
            functions = self.extract_functions(py_file)
            all_functions.extend(functions)
        
        # Group functions by signature similarity
        function_groups = defaultdict(list)
        for func in all_functions:
            # Create a signature based on name, args, and body
            signature = f"{func['name']}_{len(func['args'])}_{func['body_signature']}"
            function_groups[signature].append(func)
        
        duplicates = []
        for signature, functions in function_groups.items():
            if len(functions) > 1:
                duplicates.append({
                    "signature": signature,
                    "functions": functions,
                    "reduction_potential": len(functions) - 1
                })
        
        return duplicates
    
    def find_redundant_imports(self, python_files: List[Path]) -> List[Dict]:
        """Find redundant or unused imports."""
        redundant_imports = []
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                # Get all imports
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            for alias in node.names:
                                imports.append(f"{node.module}.{alias.name}")
                
                # Get all used names
                used_names = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Name):
                        used_names.add(node.id)
                
                # Find unused imports
                unused = []
                for imp in imports:
                    if imp.split('.')[-1] not in used_names:
                        unused.append(imp)
                
                if unused:
                    redundant_imports.append({
                        "file": str(py_file),
                        "unused_imports": unused,
                        "reduction_potential": len(unused)
                    })
            
            except Exception as e:
                print(f"Error analyzing imports in {py_file}: {e}")
        
        return redundant_imports
    
    def find_duplicate_code_blocks(self, python_files: List[Path]) -> List[Dict]:
        """Find duplicate code blocks."""
        code_blocks = []
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Look for repeated patterns
                for i in range(len(lines) - 5):  # Minimum 5 lines for a block
                    block = lines[i:i+5]
                    block_text = ''.join(block).strip()
                    
                    # Check if this block appears elsewhere
                    occurrences = []
                    for j in range(len(lines) - 5):
                        if j != i:
                            other_block = lines[j:j+5]
                            other_text = ''.join(other_block).strip()
                            if block_text == other_text and len(block_text) > 50:
                                occurrences.append(j)
                    
                    if occurrences:
                        code_blocks.append({
                            "file": str(py_file),
                            "block": block_text,
                            "line_start": i + 1,
                            "occurrences": occurrences,
                            "reduction_potential": len(occurrences)
                        })
            
            except Exception as e:
                print(f"Error analyzing code blocks in {py_file}: {e}")
        
        return code_blocks
    
    def find_overly_complex_functions(self, python_files: List[Path]) -> List[Dict]:
        """Find functions that are overly complex."""
        complex_functions = []
        
        for py_file in python_files:
            functions = self.extract_functions(py_file)
            for func in functions:
                if func['complexity'] > 10 or func['line_count'] > 50:
                    complex_functions.append({
                        "file": str(py_file),
                        "function": func['name'],
                        "complexity": func['complexity'],
                        "line_count": func['line_count'],
                        "reduction_potential": "High - refactor needed"
                    })
        
        return complex_functions
    
    def find_redundant_data_structures(self, python_files: List[Path]) -> List[Dict]:
        """Find redundant data structures and configurations."""
        redundant_structures = []
        
        # Look for duplicate dictionaries, lists, and configurations
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find large data structures
                if '= {' in content and content.count('= {') > 3:
                    # Look for similar dictionary patterns
                    dict_patterns = re.findall(r'(\w+)\s*=\s*\{[^}]+\}', content)
                    if len(set(dict_patterns)) < len(dict_patterns):
                        redundant_structures.append({
                            "file": str(py_file),
                            "type": "duplicate_dictionaries",
                            "reduction_potential": "Medium"
                        })
            
            except Exception as e:
                print(f"Error analyzing data structures in {py_file}: {e}")
        
        return redundant_structures
    
    def analyze_optimization_opportunities(self, python_files: List[Path]) -> List[Dict]:
        """Find general optimization opportunities."""
        opportunities = []
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for common inefficiencies
                if content.count('import ') > 20:
                    opportunities.append({
                        "file": str(py_file),
                        "type": "too_many_imports",
                        "count": content.count('import '),
                        "reduction_potential": "High"
                    })
                
                if content.count('class ') > 10:
                    opportunities.append({
                        "file": str(py_file),
                        "type": "too_many_classes",
                        "count": content.count('class '),
                        "reduction_potential": "Medium"
                    })
                
                if content.count('def ') > 20:
                    opportunities.append({
                        "file": str(py_file),
                        "type": "too_many_functions",
                        "count": content.count('def '),
                        "reduction_potential": "Medium"
                    })
            
            except Exception as e:
                print(f"Error analyzing optimization opportunities in {py_file}: {e}")
        
        return opportunities
    
    def run_analysis(self) -> Dict:
        """Run complete code reduction analysis."""
        print("🔍 Professional Code Reduction Analysis")
        print("=" * 50)
        
        # Get Python files
        python_files = self.analyze_python_files()
        print(f"Analyzing {len(python_files)} Python files...")
        
        # Run all analyses
        print("1. Finding duplicate functions...")
        self.analysis_results["duplicate_functions"] = self.find_duplicate_functions(python_files)
        
        print("2. Finding redundant imports...")
        self.analysis_results["redundant_imports"] = self.find_redundant_imports(python_files)
        
        print("3. Finding duplicate code blocks...")
        self.analysis_results["duplicate_code_blocks"] = self.find_duplicate_code_blocks(python_files)
        
        print("4. Finding overly complex functions...")
        self.analysis_results["overly_complex_functions"] = self.find_overly_complex_functions(python_files)
        
        print("5. Finding redundant data structures...")
        self.analysis_results["redundant_data_structures"] = self.find_redundant_data_structures(python_files)
        
        print("6. Finding optimization opportunities...")
        self.analysis_results["optimization_opportunities"] = self.analyze_optimization_opportunities(python_files)
        
        # Calculate statistics
        self.analysis_results["statistics"] = {
            "total_files": len(python_files),
            "duplicate_functions": len(self.analysis_results["duplicate_functions"]),
            "redundant_imports": len(self.analysis_results["redundant_imports"]),
            "duplicate_code_blocks": len(self.analysis_results["duplicate_code_blocks"]),
            "complex_functions": len(self.analysis_results["overly_complex_functions"]),
            "redundant_structures": len(self.analysis_results["redundant_data_structures"]),
            "optimization_opportunities": len(self.analysis_results["optimization_opportunities"])
        }
        
        return self.analysis_results
    
    def generate_report(self) -> str:
        """Generate comprehensive analysis report."""
        report = []
        report.append("# Professional Code Reduction Analysis Report")
        report.append("=" * 60)
        report.append("")
        
        # Statistics
        stats = self.analysis_results["statistics"]
        report.append("## 📊 Analysis Statistics")
        report.append(f"- **Total Python Files**: {stats['total_files']}")
        report.append(f"- **Duplicate Functions**: {stats['duplicate_functions']}")
        report.append(f"- **Files with Redundant Imports**: {stats['redundant_imports']}")
        report.append(f"- **Duplicate Code Blocks**: {stats['duplicate_code_blocks']}")
        report.append(f"- **Overly Complex Functions**: {stats['complex_functions']}")
        report.append(f"- **Redundant Data Structures**: {stats['redundant_structures']}")
        report.append(f"- **Optimization Opportunities**: {stats['optimization_opportunities']}")
        report.append("")
        
        # Detailed findings
        if self.analysis_results["duplicate_functions"]:
            report.append("## 🔄 Duplicate Functions")
            for dup in self.analysis_results["duplicate_functions"][:5]:  # Top 5
                report.append(f"- **{dup['signature']}**: {dup['reduction_potential']} functions can be consolidated")
            report.append("")
        
        if self.analysis_results["redundant_imports"]:
            report.append("## 📦 Redundant Imports")
            for imp in self.analysis_results["redundant_imports"][:5]:  # Top 5
                report.append(f"- **{Path(imp['file']).name}**: {imp['reduction_potential']} unused imports")
            report.append("")
        
        if self.analysis_results["overly_complex_functions"]:
            report.append("## 🧩 Overly Complex Functions")
            for func in self.analysis_results["overly_complex_functions"][:5]:  # Top 5
                report.append(f"- **{Path(func['file']).name}::{func['function']}**: Complexity {func['complexity']}, {func['line_count']} lines")
            report.append("")
        
        # Recommendations
        report.append("## 🎯 Professional Recommendations")
        report.append("")
        report.append("### High Impact Optimizations:")
        report.append("1. **Consolidate Duplicate Functions** - Create shared utility modules")
        report.append("2. **Remove Unused Imports** - Clean up import statements")
        report.append("3. **Refactor Complex Functions** - Break down into smaller, focused functions")
        report.append("4. **Extract Common Code Blocks** - Create reusable components")
        report.append("5. **Optimize Data Structures** - Use more efficient data representations")
        report.append("")
        
        report.append("### Code Quality Improvements:")
        report.append("- Implement consistent error handling patterns")
        report.append("- Use type hints consistently")
        report.append("- Create shared configuration modules")
        report.append("- Implement common logging patterns")
        report.append("- Use dependency injection for shared services")
        report.append("")
        
        return "\n".join(report)

def main():
    """Main function."""
    analyzer = CodeReductionAnalyzer()
    results = analyzer.run_analysis()
    
    # Generate and save report
    report = analyzer.generate_report()
    
    with open("code_reduction_analysis_report.md", "w") as f:
        f.write(report)
    
    # Save detailed results
    with open("code_reduction_analysis.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n📋 Analysis Complete!")
    print(f"Report saved to: code_reduction_analysis_report.md")
    print(f"Detailed results saved to: code_reduction_analysis.json")
    
    # Print summary
    stats = results["statistics"]
    total_issues = (stats["duplicate_functions"] + stats["redundant_imports"] + 
                   stats["duplicate_code_blocks"] + stats["complex_functions"])
    
    print(f"\n🎯 Summary:")
    print(f"Found {total_issues} optimization opportunities")
    print(f"Potential for significant code reduction while maintaining functionality")

if __name__ == "__main__":
    main()
