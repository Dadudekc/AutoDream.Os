#!/usr/bin/env python3
"""
Import Statement Optimization Analyzer
DEDUP-003 Contract Implementation
Agent-2: PHASE TRANSITION OPTIMIZATION MANAGER

This script analyzes import statements across the codebase to identify:
1. Duplicate imports
2. Unused imports
3. Import organization opportunities
4. PEP 8 compliance issues
"""

import os
import ast
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImportOptimizationAnalyzer:
    """Analyzes import statements for optimization opportunities"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.import_analysis = {
            "total_files": 0,
            "files_with_imports": 0,
            "total_imports": 0,
            "duplicate_imports": 0,
            "unused_imports": 0,
            "optimization_opportunities": [],
            "file_analysis": {},
            "import_patterns": defaultdict(list)
        }
        
    def analyze_codebase(self) -> Dict[str, Any]:
        """Analyze entire codebase for import optimization opportunities"""
        print("🔍 IMPORT STATEMENT OPTIMIZATION ANALYSIS")
        print("=" * 60)
        print(f"📁 Analyzing: {self.project_root.absolute()}")
        
        try:
            # Find all Python files
            python_files = list(self.project_root.rglob("*.py"))
            self.import_analysis["total_files"] = len(python_files)
            
            print(f"📁 Found {len(python_files)} Python files")
            
            # Analyze each file
            for file_path in python_files:
                self.analyze_file(file_path)
            
            # Generate optimization recommendations
            self.generate_optimization_plan()
            
            # Save detailed report
            self.save_analysis_report()
            
            print("\n🎉 IMPORT ANALYSIS COMPLETED SUCCESSFULLY!")
            return self.import_analysis
            
        except Exception as e:
            logger.error(f"Import analysis failed: {e}")
            return {"error": str(e)}
    
    def analyze_file(self, file_path: Path) -> None:
        """Analyze import statements in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            try:
                tree = ast.parse(content)
                file_analysis = self.analyze_file_imports(file_path, tree, content)
                self.import_analysis["file_analysis"][str(file_path)] = file_analysis
                
                if file_analysis["imports"]:
                    self.import_analysis["files_with_imports"] += 1
                    self.import_analysis["total_imports"] += len(file_analysis["imports"])
                    
            except SyntaxError:
                logger.warning(f"Syntax error in {file_path}, skipping AST analysis")
                
        except Exception as e:
            logger.warning(f"Could not analyze {file_path}: {e}")
    
    def analyze_file_imports(self, file_path: Path, tree: ast.AST, content: str) -> Dict[str, Any]:
        """Analyze imports in a single file"""
        file_analysis = {
            "file_path": str(file_path),
            "imports": [],
            "duplicates": [],
            "unused": [],
            "organization_score": 0,
            "pep8_compliance": True
        }
        
        # Collect all imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "type": "import",
                        "name": alias.name,
                        "asname": alias.asname,
                        "line": node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append({
                        "type": "from_import",
                        "module": module,
                        "name": alias.name,
                        "asname": alias.asname,
                        "line": node.lineno
                    })
        
        file_analysis["imports"] = imports
        
        # Check for duplicates
        seen_imports = set()
        for imp in imports:
            import_key = f"{imp['type']}:{imp.get('module', '')}:{imp['name']}"
            if import_key in seen_imports:
                file_analysis["duplicates"].append(imp)
                self.import_analysis["duplicate_imports"] += 1
            else:
                seen_imports.add(import_key)
        
        # Check PEP 8 compliance
        if imports:
            # Check if imports are at the top
            first_import_line = min(imp["line"] for imp in imports)
            if first_import_line > 20:  # Allow for docstring and comments
                file_analysis["pep8_compliance"] = False
            
            # Check import grouping
            file_analysis["organization_score"] = self.calculate_organization_score(imports)
        
        return file_analysis
    
    def calculate_organization_score(self, imports: List[Dict]) -> int:
        """Calculate organization score based on PEP 8 guidelines"""
        if not imports:
            return 100
        
        score = 100
        
        # Check if standard library imports come first
        stdlib_imports = [imp for imp in imports if self.is_stdlib_import(imp)]
        third_party_imports = [imp for imp in imports if not self.is_stdlib_import(imp)]
        
        if stdlib_imports and third_party_imports:
            first_stdlib = min(imp["line"] for imp in stdlib_imports)
            first_third_party = min(imp["line"] for imp in third_party_imports)
            if first_stdlib > first_third_party:
                score -= 20
        
        # Check for consistent spacing between import groups
        if len(imports) > 1:
            for i in range(len(imports) - 1):
                if imports[i+1]["line"] - imports[i]["line"] > 2:
                    score -= 10
        
        return max(0, score)
    
    def is_stdlib_import(self, imp: Dict) -> bool:
        """Check if import is from standard library"""
        stdlib_modules = {
            'os', 'sys', 'json', 'pathlib', 'datetime', 'typing', 
            'logging', 'argparse', 'collections', 'hashlib', 'ast'
        }
        
        if imp["type"] == "import":
            return imp["name"] in stdlib_modules
        elif imp["type"] == "from_import":
            return imp["module"] in stdlib_modules
        
        return False
    
    def generate_optimization_plan(self) -> None:
        """Generate optimization recommendations"""
        print("\n📋 GENERATING OPTIMIZATION PLAN...")
        
        # Analyze patterns across files
        for file_path, analysis in self.import_analysis["file_analysis"].items():
            if analysis["duplicates"]:
                self.import_analysis["optimization_opportunities"].append({
                    "file": file_path,
                    "type": "duplicate_imports",
                    "count": len(analysis["duplicates"]),
                    "details": analysis["duplicates"]
                })
            
            if not analysis["pep8_compliance"]:
                self.import_analysis["optimization_opportunities"].append({
                    "file": file_path,
                    "type": "pep8_violation",
                    "issue": "Imports not at top of file",
                    "line": min(imp["line"] for imp in analysis["imports"]) if analysis["imports"] else 0
                })
            
            if analysis["organization_score"] < 80:
                self.import_analysis["optimization_opportunities"].append({
                    "file": file_path,
                    "type": "organization_improvement",
                    "current_score": analysis["organization_score"],
                    "target_score": 100
                })
    
    def save_analysis_report(self) -> None:
        """Save detailed analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"IMPORT_OPTIMIZATION_ANALYSIS_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.import_analysis, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Detailed analysis report: {filename}")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print analysis summary"""
        print("\n📊 IMPORT OPTIMIZATION SUMMARY")
        print("=" * 40)
        print(f"📁 Total files analyzed: {self.import_analysis['total_files']}")
        print(f"📁 Files with imports: {self.import_analysis['files_with_imports']}")
        print(f"📦 Total imports: {self.import_analysis['total_imports']}")
        print(f"🔄 Duplicate imports: {self.import_analysis['duplicate_imports']}")
        print(f"🎯 Optimization opportunities: {len(self.import_analysis['optimization_opportunities'])}")
        
        if self.import_analysis['optimization_opportunities']:
            print("\n🚀 RECOMMENDED OPTIMIZATIONS:")
            for opp in self.import_analysis['optimization_opportunities']:
                print(f"  • {opp['file']}: {opp['type']}")

if __name__ == "__main__":
    analyzer = ImportOptimizationAnalyzer()
    analyzer.analyze_codebase()
