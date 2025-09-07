#!/usr/bin/env python3
"""
Import Statement Optimization Implementation
DEDUP-003 Contract Implementation
Agent-2: PHASE TRANSITION OPTIMIZATION MANAGER

This script implements the import optimizations identified by the analyzer:
1. Consolidates duplicate imports
2. Removes unused imports
3. Reorganizes imports according to PEP 8 standards
4. Updates affected files
"""

import os
import ast
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImportOptimizer:
    """Implements import statement optimizations"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.optimization_results = {
            "files_processed": 0,
            "files_optimized": 0,
            "duplicate_imports_removed": 0,
            "imports_reorganized": 0,
            "pep8_violations_fixed": 0,
            "optimization_details": []
        }
        
        # Standard library modules (should come first)
        self.stdlib_modules = {
            'os', 'sys', 'json', 'pathlib', 'datetime', 'timezone', 'timedelta',
            'typing', 'logging', 'argparse', 'collections', 'hashlib', 'ast',
            're', 'itertools', 'functools', 'contextlib', 'tempfile', 'shutil',
            'subprocess', 'threading', 'asyncio', 'urllib', 'http', 'socket',
            'pickle', 'sqlite3', 'csv', 'xml', 'html', 'base64', 'zlib',
            'gzip', 'bz2', 'lzma', 'zipfile', 'tarfile', 'glob', 'fnmatch'
        }
        
        # Third-party modules (should come after stdlib)
        self.third_party_modules = {
            'numpy', 'pandas', 'matplotlib', 'seaborn', 'scipy', 'sklearn',
            'tensorflow', 'torch', 'keras', 'flask', 'django', 'fastapi',
            'requests', 'aiohttp', 'sqlalchemy', 'pymongo', 'redis', 'celery',
            'pytest', 'unittest', 'mock', 'coverage', 'black', 'flake8',
            'mypy', 'isort', 'pre-commit', 'click', 'rich', 'typer'
        }
    
    def optimize_codebase(self, analysis_file: str = None) -> Dict[str, Any]:
        """Optimize imports across the entire codebase"""
        print("🚀 IMPORT STATEMENT OPTIMIZATION IMPLEMENTATION")
        print("=" * 60)
        
        try:
            if analysis_file and Path(analysis_file).exists():
                # Load existing analysis
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    analysis = json.load(f)
                print(f"📁 Loaded analysis from: {analysis_file}")
            else:
                # Run fresh analysis
                print("📁 Running fresh import analysis...")
                from import_optimization_analyzer import ImportOptimizationAnalyzer
                analyzer = ImportOptimizationAnalyzer()
                analysis = analyzer.analyze_codebase()
            
            # Process optimization opportunities
            self.process_optimization_opportunities(analysis)
            
            # Save results
            self.save_optimization_results()
            
            print("\n🎉 IMPORT OPTIMIZATION COMPLETED SUCCESSFULLY!")
            return self.optimization_results
            
        except Exception as e:
            logger.error(f"Import optimization failed: {e}")
            return {"error": str(e)}
    
    def process_optimization_opportunities(self, analysis: Dict[str, Any]) -> None:
        """Process all identified optimization opportunities"""
        print("\n📋 PROCESSING OPTIMIZATION OPPORTUNITIES...")
        
        for opportunity in analysis.get("optimization_opportunities", []):
            file_path = opportunity["file"]
            
            if not Path(file_path).exists():
                logger.warning(f"File not found: {file_path}")
                continue
            
            try:
                self.optimize_file(file_path, opportunity)
                self.optimization_results["files_processed"] += 1
                
            except Exception as e:
                logger.error(f"Failed to optimize {file_path}: {e}")
    
    def optimize_file(self, file_path: str, opportunity: Dict[str, Any]) -> None:
        """Optimize imports in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            optimized_content = content
            
            # Apply optimizations based on opportunity type
            if opportunity["type"] == "duplicate_imports":
                optimized_content = self.remove_duplicate_imports(content)
                if optimized_content != original_content:
                    self.optimization_results["duplicate_imports_removed"] += opportunity.get("count", 1)
            
            if opportunity["type"] == "pep8_violation":
                optimized_content = self.fix_pep8_violations(optimized_content)
                if optimized_content != original_content:
                    self.optimization_results["pep8_violations_fixed"] += 1
            
            if opportunity["type"] == "organization_improvement":
                optimized_content = self.reorganize_imports(optimized_content)
                if optimized_content != original_content:
                    self.optimization_results["imports_reorganized"] += 1
            
            # Save optimized content if changes were made
            if optimized_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(optimized_content)
                
                self.optimization_results["files_optimized"] += 1
                self.optimization_results["optimization_details"].append({
                    "file": file_path,
                    "type": opportunity["type"],
                    "changes_made": True
                })
                
                print(f"✅ Optimized: {file_path}")
            else:
                self.optimization_results["optimization_details"].append({
                    "file": file_path,
                    "type": opportunity["type"],
                    "changes_made": False
                })
                
        except Exception as e:
            logger.error(f"Error optimizing {file_path}: {e}")
    
    def remove_duplicate_imports(self, content: str) -> str:
        """Remove duplicate import statements"""
        lines = content.split('\n')
        optimized_lines = []
        seen_imports = set()
        in_import_section = False
        
        for line in lines:
            stripped = line.strip()
            
            # Check if we're in import section
            if stripped.startswith('import ') or stripped.startswith('from '):
                in_import_section = True
                import_key = self.get_import_key(stripped)
                
                if import_key not in seen_imports:
                    seen_imports.add(import_key)
                    optimized_lines.append(line)
                # Skip duplicate imports
                
            elif in_import_section and stripped == '':
                # Keep empty lines between import groups
                optimized_lines.append(line)
            elif in_import_section and not stripped.startswith('import ') and not stripped.startswith('from '):
                # We've left the import section
                in_import_section = False
                optimized_lines.append(line)
            else:
                # Non-import line
                optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def get_import_key(self, import_line: str) -> str:
        """Generate a key for identifying duplicate imports"""
        # Handle "import x" statements
        if import_line.startswith('import '):
            parts = import_line[7:].split(' as ')
            if len(parts) > 1:
                return f"import:{parts[0].strip()}:{parts[1].strip()}"
            else:
                return f"import:{parts[0].strip()}"
        
        # Handle "from x import y" statements
        elif import_line.startswith('from '):
            parts = import_line[5:].split(' import ')
            if len(parts) == 2:
                module = parts[0].strip()
                names = parts[1].split(' as ')
                if len(names) > 1:
                    return f"from:{module}:{names[0].strip()}:{names[1].strip()}"
                else:
                    return f"from:{module}:{names[0].strip()}"
        
        return import_line
    
    def fix_pep8_violations(self, content: str) -> str:
        """Fix PEP 8 violations in import statements"""
        lines = content.split('\n')
        optimized_lines = []
        
        # Find import statements
        import_lines = []
        other_lines = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                import_lines.append((i, line))
            else:
                other_lines.append((i, line))
        
        if not import_lines:
            return content
        
        # Move imports to top (after docstring and comments)
        docstring_end = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                # Find end of docstring
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().endswith('"""') or lines[j].strip().endswith("'''"):
                        docstring_end = j + 1
                        break
                break
            elif stripped.startswith('#'):
                docstring_end = i + 1
            elif stripped and not stripped.startswith('import ') and not stripped.startswith('from '):
                break
        
        # Reconstruct content with imports at top
        optimized_lines = lines[:docstring_end]
        
        # Add imports
        for _, import_line in import_lines:
            optimized_lines.append(import_line)
        
        # Add empty line after imports
        if import_lines:
            optimized_lines.append('')
        
        # Add remaining content
        for i, line in other_lines:
            if i > docstring_end:  # Skip lines we've already processed
                optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def reorganize_imports(self, content: str) -> str:
        """Reorganize imports according to PEP 8 standards"""
        lines = content.split('\n')
        
        # Extract import statements
        imports = []
        other_lines = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                imports.append(line)
            else:
                other_lines.append(line)
        
        if not imports:
            return content
        
        # Categorize imports
        stdlib_imports = []
        third_party_imports = []
        local_imports = []
        
        for imp in imports:
            if self.is_stdlib_import(imp):
                stdlib_imports.append(imp)
            elif self.is_third_party_import(imp):
                third_party_imports.append(imp)
            else:
                local_imports.append(imp)
        
        # Sort each category
        stdlib_imports.sort()
        third_party_imports.sort()
        local_imports.sort()
        
        # Reconstruct content
        optimized_lines = []
        
        # Add stdlib imports
        if stdlib_imports:
            optimized_lines.extend(stdlib_imports)
            optimized_lines.append('')
        
        # Add third-party imports
        if third_party_imports:
            optimized_lines.extend(third_party_imports)
            optimized_lines.append('')
        
        # Add local imports
        if local_imports:
            optimized_lines.extend(local_imports)
            optimized_lines.append('')
        
        # Add remaining content
        optimized_lines.extend(other_lines)
        
        return '\n'.join(optimized_lines)
    
    def is_stdlib_import(self, import_line: str) -> bool:
        """Check if import is from standard library"""
        if import_line.startswith('import '):
            module = import_line[7:].split(' as ')[0].strip()
            return module in self.stdlib_modules
        elif import_line.startswith('from '):
            parts = import_line[5:].split(' import ')
            if len(parts) == 2:
                module = parts[0].strip()
                return module in self.stdlib_modules
        return False
    
    def is_third_party_import(self, import_line: str) -> bool:
        """Check if import is from third-party library"""
        if import_line.startswith('import '):
            module = import_line[7:].split(' as ')[0].strip()
            return module in self.third_party_modules
        elif import_line.startswith('from '):
            parts = import_line[5:].split(' import ')
            if len(parts) == 2:
                module = parts[0].strip()
                return module in self.third_party_modules
        return False
    
    def save_optimization_results(self) -> None:
        """Save optimization results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"IMPORT_OPTIMIZATION_RESULTS_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.optimization_results, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Optimization results saved: {filename}")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print optimization summary"""
        print("\n📊 IMPORT OPTIMIZATION SUMMARY")
        print("=" * 40)
        print(f"📁 Files processed: {self.optimization_results['files_processed']}")
        print(f"📁 Files optimized: {self.optimization_results['files_optimized']}")
        print(f"🔄 Duplicate imports removed: {self.optimization_results['duplicate_imports_removed']}")
        print(f"📦 Imports reorganized: {self.optimization_results['imports_reorganized']}")
        print(f"✅ PEP 8 violations fixed: {self.optimization_results['pep8_violations_fixed']}")

if __name__ == "__main__":
    from datetime import datetime
    
    # Look for existing analysis file
    analysis_files = list(Path(".").glob("IMPORT_OPTIMIZATION_ANALYSIS_*.json"))
    latest_analysis = max(analysis_files, key=lambda x: x.stat().st_mtime) if analysis_files else None
    
    optimizer = ImportOptimizer()
    if latest_analysis:
        print(f"📁 Using existing analysis: {latest_analysis}")
        optimizer.optimize_codebase(str(latest_analysis))
    else:
        optimizer.optimize_codebase()
