#!/usr/bin/env python3
"""
DRY Elimination Code Analysis Engine
====================================

Code analysis engine for DRY elimination system.
Handles AST parsing, pattern extraction, and code structure analysis.
V2 COMPLIANT: Focused code analysis under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR CODE ANALYSIS
@license MIT
"""

import ast
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict

from ..dry_eliminator_models import DRYEliminatorConfig


class CodeAnalysisEngine:
    """Code analysis engine for DRY elimination system"""
    
    def __init__(self, config: DRYEliminatorConfig):
        """Initialize code analysis engine with configuration"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.parsed_files: Dict[str, ast.AST] = {}
        self.analysis_cache: Dict[str, Dict[str, Any]] = {}
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file and extract patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            self.parsed_files[str(file_path)] = tree
            
            # Extract patterns
            patterns = self._extract_patterns(tree, file_path)
            
            # Cache analysis results
            self.analysis_cache[str(file_path)] = patterns
            
            return patterns
            
        except SyntaxError as e:
            self.logger.warning(f"Syntax error in {file_path}: {e}")
            return {"error": f"Syntax error: {e}"}
        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")
            return {"error": str(e)}
    
    def _extract_patterns(self, tree: ast.AST, file_path: Path) -> Dict[str, Any]:
        """Extract code patterns from AST"""
        patterns = {
            'imports': [],
            'functions': [],
            'classes': [],
            'constants': [],
            'variables': [],
            'method_calls': [],
            'string_literals': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    patterns['imports'].append({
                        'name': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno,
                        'type': 'import'
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    patterns['imports'].append({
                        'name': f"{module}.{alias.name}" if module else alias.name,
                        'alias': alias.asname,
                        'line': node.lineno,
                        'type': 'from_import'
                    })
            elif isinstance(node, ast.FunctionDef):
                patterns['functions'].append({
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'body_lines': len(node.body),
                    'docstring': ast.get_docstring(node)
                })
            elif isinstance(node, ast.ClassDef):
                patterns['classes'].append({
                    'name': node.name,
                    'line': node.lineno,
                    'bases': [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases],
                    'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                })
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        patterns['variables'].append({
                            'name': target.id,
                            'line': node.lineno,
                            'value_type': type(node.value).__name__
                        })
            elif isinstance(node, ast.Constant):
                if isinstance(node.value, str) and len(node.value) > 10:
                    patterns['string_literals'].append({
                        'value': node.value,
                        'line': node.lineno,
                        'length': len(node.value)
                    })
        
        return patterns
    
    def analyze_multiple_files(self, file_paths: List[Path]) -> Dict[str, Dict[str, Any]]:
        """Analyze multiple files and return combined results"""
        results = {}
        
        for file_path in file_paths:
            try:
                analysis = self.analyze_file(file_path)
                results[str(file_path)] = analysis
            except Exception as e:
                self.logger.error(f"Failed to analyze {file_path}: {e}")
                results[str(file_path)] = {"error": str(e)}
        
        return results
    
    def get_import_patterns(self, file_paths: List[Path]) -> Dict[str, List[Tuple[Path, int]]]:
        """Extract import patterns across multiple files"""
        import_patterns = defaultdict(list)
        
        for file_path in file_paths:
            analysis = self.analysis_cache.get(str(file_path), {})
            imports = analysis.get('imports', [])
            
            for imp in imports:
                import_name = imp['name']
                line_number = imp['line']
                import_patterns[import_name].append((file_path, line_number))
        
        return dict(import_patterns)
    
    def get_function_patterns(self, file_paths: List[Path]) -> Dict[str, List[Tuple[Path, int, str]]]:
        """Extract function patterns across multiple files"""
        function_patterns = defaultdict(list)
        
        for file_path in file_paths:
            analysis = self.analysis_cache.get(str(file_path), {})
            functions = analysis.get('functions', [])
            
            for func in functions:
                func_name = func['name']
                line_number = func['line']
                # Create a simple signature
                args = func.get('args', [])
                signature = f"{func_name}({', '.join(args)})"
                function_patterns[func_name].append((file_path, line_number, signature))
        
        return dict(function_patterns)
    
    def get_constant_patterns(self, file_paths: List[Path]) -> Dict[str, List[Tuple[Path, int, str]]]:
        """Extract constant patterns across multiple files"""
        constant_patterns = defaultdict(list)
        
        for file_path in file_paths:
            analysis = self.analysis_cache.get(str(file_path), {})
            variables = analysis.get('variables', [])
            
            for var in variables:
                var_name = var['name']
                line_number = var['line']
                # Only consider uppercase variables as constants
                if var_name.isupper():
                    constant_patterns[var_name].append((file_path, line_number, var_name))
        
        return dict(constant_patterns)
    
    def find_duplicate_code_blocks(self, file_paths: List[Path], min_lines: int = 5) -> List[Dict[str, Any]]:
        """Find duplicate code blocks across files"""
        code_blocks = []
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Look for duplicate blocks
                for i in range(len(lines) - min_lines + 1):
                    block = ''.join(lines[i:i + min_lines])
                    block_hash = hash(block.strip())
                    
                    code_blocks.append({
                        'file_path': file_path,
                        'start_line': i + 1,
                        'end_line': i + min_lines,
                        'content': block.strip(),
                        'hash': block_hash
                    })
            except Exception as e:
                self.logger.warning(f"Could not analyze {file_path} for duplicate blocks: {e}")
        
        # Group by hash to find duplicates
        duplicate_groups = defaultdict(list)
        for block in code_blocks:
            duplicate_groups[block['hash']].append(block)
        
        # Return only groups with duplicates
        duplicates = []
        for group in duplicate_groups.values():
            if len(group) > 1:
                duplicates.append(group)
        
        return duplicates
    
    def get_file_complexity_metrics(self, file_path: Path) -> Dict[str, Any]:
        """Calculate complexity metrics for a file"""
        analysis = self.analysis_cache.get(str(file_path), {})
        
        functions = analysis.get('functions', [])
        classes = analysis.get('classes', [])
        imports = analysis.get('imports', [])
        
        # Calculate cyclomatic complexity (simplified)
        complexity = 0
        for func in functions:
            # Basic complexity based on function body length
            body_lines = func.get('body_lines', 0)
            complexity += max(1, body_lines // 5)  # Rough estimate
        
        return {
            'function_count': len(functions),
            'class_count': len(classes),
            'import_count': len(imports),
            'complexity_score': complexity,
            'lines_per_function': sum(f.get('body_lines', 0) for f in functions) / len(functions) if functions else 0
        }
    
    def get_analysis_summary(self, file_paths: List[Path]) -> Dict[str, Any]:
        """Get summary of analysis across all files"""
        total_functions = 0
        total_classes = 0
        total_imports = 0
        total_complexity = 0
        
        for file_path in file_paths:
            analysis = self.analysis_cache.get(str(file_path), {})
            if 'error' not in analysis:
                total_functions += len(analysis.get('functions', []))
                total_classes += len(analysis.get('classes', []))
                total_imports += len(analysis.get('imports', []))
                
                metrics = self.get_file_complexity_metrics(file_path)
                total_complexity += metrics.get('complexity_score', 0)
        
        return {
            'total_files_analyzed': len(file_paths),
            'total_functions': total_functions,
            'total_classes': total_classes,
            'total_imports': total_imports,
            'total_complexity': total_complexity,
            'avg_functions_per_file': total_functions / len(file_paths) if file_paths else 0,
            'avg_classes_per_file': total_classes / len(file_paths) if file_paths else 0
        }
    
    def clear_cache(self):
        """Clear analysis cache"""
        self.parsed_files.clear()
        self.analysis_cache.clear()


# Factory function for dependency injection
def create_code_analysis_engine(config: DRYEliminatorConfig) -> CodeAnalysisEngine:
    """Factory function to create code analysis engine with configuration"""
    return CodeAnalysisEngine(config)


# Export for DI
__all__ = ['CodeAnalysisEngine', 'create_code_analysis_engine']
