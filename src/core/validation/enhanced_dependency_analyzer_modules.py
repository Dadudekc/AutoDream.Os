#!/usr/bin/env python3
"""
Enhanced Dependency Analyzer - Modular Components
=================================================

Split from enhanced_dependency_analyzer.py (831 lines) to achieve V2 compliance.
This module contains the core dependency analysis components.

Author: Agent-1 (PERPETUAL MOTION LEADER - V2 COMPLIANCE SPECIALIST)
Mission: V2 COMPLIANCE OPTIMIZATION - File Size Reduction
License: MIT
"""

import ast
import os
import logging
from typing import Dict, List, Set, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class DependencyConfig:
    """Dependency analyzer configuration"""
    analyze_imports: bool = True
    analyze_functions: bool = True
    analyze_classes: bool = True
    analyze_variables: bool = True
    max_depth: int = 10
    ignore_patterns: List[str] = field(default_factory=lambda: ['__pycache__', '.git', 'venv'])


@dataclass
class DependencyNode:
    """Represents a dependency node"""
    name: str
    type: str  # 'module', 'function', 'class', 'variable'
    file_path: str
    line_number: int
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)


class ImportAnalyzer:
    """Analyzes import statements in Python files"""
    
    def __init__(self, config: DependencyConfig):
        self.config = config
        
    def analyze_imports(self, file_path: str) -> List[str]:
        """Extract all imports from a Python file"""
        if not self.config.analyze_imports:
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        if module:
                            imports.append(f"{module}.{alias.name}")
                        else:
                            imports.append(alias.name)
                            
            return imports
        except Exception as e:
            logger.error(f"Failed to analyze imports in {file_path}: {e}")
            return []


class FunctionAnalyzer:
    """Analyzes function definitions and calls"""
    
    def __init__(self, config: DependencyConfig):
        self.config = config
        
    def analyze_functions(self, file_path: str) -> List[DependencyNode]:
        """Extract function definitions and their dependencies"""
        if not self.config.analyze_functions:
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_node = DependencyNode(
                        name=node.name,
                        type='function',
                        file_path=file_path,
                        line_number=node.lineno,
                        dependencies=self._extract_function_dependencies(node)
                    )
                    functions.append(func_node)
                    
            return functions
        except Exception as e:
            logger.error(f"Failed to analyze functions in {file_path}: {e}")
            return []
    
    def _extract_function_dependencies(self, node: ast.FunctionDef) -> List[str]:
        """Extract dependencies from function body"""
        dependencies = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    dependencies.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    dependencies.append(child.func.attr)
        return dependencies


class ClassAnalyzer:
    """Analyzes class definitions and their dependencies"""
    
    def __init__(self, config: DependencyConfig):
        self.config = config
        
    def analyze_classes(self, file_path: str) -> List[DependencyNode]:
        """Extract class definitions and their dependencies"""
        if not self.config.analyze_classes:
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_node = DependencyNode(
                        name=node.name,
                        type='class',
                        file_path=file_path,
                        line_number=node.lineno,
                        dependencies=self._extract_class_dependencies(node)
                    )
                    classes.append(class_node)
                    
            return classes
        except Exception as e:
            logger.error(f"Failed to analyze classes in {file_path}: {e}")
            return []
    
    def _extract_class_dependencies(self, node: ast.ClassDef) -> List[str]:
        """Extract dependencies from class body"""
        dependencies = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    dependencies.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    dependencies.append(child.func.attr)
        return dependencies


class DependencyGraphBuilder:
    """Builds dependency graphs from analysis results"""
    
    def __init__(self):
        self.nodes: Dict[str, DependencyNode] = {}
        self.graph: Dict[str, List[str]] = defaultdict(list)
        
    def add_node(self, node: DependencyNode) -> None:
        """Add a dependency node to the graph"""
        self.nodes[node.name] = node
        
    def add_dependency(self, from_node: str, to_node: str) -> None:
        """Add a dependency relationship"""
        self.graph[from_node].append(to_node)
        
    def get_dependencies(self, node_name: str) -> List[str]:
        """Get all dependencies for a node"""
        return self.graph.get(node_name, [])
        
    def get_dependents(self, node_name: str) -> List[str]:
        """Get all dependents for a node"""
        dependents = []
        for node, deps in self.graph.items():
            if node_name in deps:
                dependents.append(node)
        return dependents
        
    def find_cycles(self) -> List[List[str]]:
        """Find circular dependencies"""
        cycles = []
        visited = set()
        
        def dfs(node: str, path: List[str]) -> None:
            if node in path:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
                
            if node in visited:
                return
                
            visited.add(node)
            path.append(node)
            
            for dep in self.graph.get(node, []):
                dfs(dep, path.copy())
                
        for node in self.nodes:
            if node not in visited:
                dfs(node, [])
                
        return cycles


# Main analyzer class that orchestrates all components
class EnhancedDependencyAnalyzer:
    """Enhanced dependency analyzer - main orchestrator"""
    
    def __init__(self, config: DependencyConfig = None):
        self.config = config or DependencyConfig()
        self.import_analyzer = ImportAnalyzer(self.config)
        self.function_analyzer = FunctionAnalyzer(self.config)
        self.class_analyzer = ClassAnalyzer(self.config)
        self.graph_builder = DependencyGraphBuilder()
        
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze dependencies in a single file"""
        if not file_path.endswith('.py'):
            return {}
            
        try:
            # Analyze imports
            imports = self.import_analyzer.analyze_imports(file_path)
            
            # Analyze functions
            functions = self.function_analyzer.analyze_functions(file_path)
            
            # Analyze classes
            classes = self.class_analyzer.analyze_classes(file_path)
            
            # Build graph
            for func in functions:
                self.graph_builder.add_node(func)
                for dep in func.dependencies:
                    self.graph_builder.add_dependency(func.name, dep)
                    
            for cls in classes:
                self.graph_builder.add_node(cls)
                for dep in cls.dependencies:
                    self.graph_builder.add_dependency(cls.name, dep)
                    
            return {
                'file_path': file_path,
                'imports': imports,
                'functions': [{'name': f.name, 'line': f.line_number, 'dependencies': f.dependencies} for f in functions],
                'classes': [{'name': c.name, 'line': c.line_number, 'dependencies': c.dependencies} for c in classes]
            }
        except Exception as e:
            logger.error(f"Failed to analyze file {file_path}: {e}")
            return {}
    
    def analyze_directory(self, directory_path: str) -> Dict[str, Any]:
        """Analyze dependencies in a directory"""
        results = {}
        
        for root, dirs, files in os.walk(directory_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.config.ignore_patterns]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    results[file_path] = self.analyze_file(file_path)
                    
        return results
    
    def find_circular_dependencies(self) -> List[List[str]]:
        """Find circular dependencies in the analyzed code"""
        return self.graph_builder.find_cycles()
    
    def get_dependency_report(self) -> Dict[str, Any]:
        """Generate a comprehensive dependency report"""
        return {
            'total_files': len(self.graph_builder.nodes),
            'total_dependencies': sum(len(deps) for deps in self.graph_builder.graph.values()),
            'circular_dependencies': self.find_circular_dependencies(),
            'nodes': {name: {'type': node.type, 'file': node.file_path} for name, node in self.graph_builder.nodes.items()}
        }


if __name__ == "__main__":
    # Test the modularized dependency analyzer
    analyzer = EnhancedDependencyAnalyzer()
    
    # Test with a simple file
    test_file = "test_dependency.py"
    test_content = '''
import os
import json

def test_function():
    return os.path.exists("test")

class TestClass:
    def __init__(self):
        self.data = json.loads('{"test": true}')
'''
    
    # Create test file
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    # Analyze
    result = analyzer.analyze_file(test_file)
    print(f"✅ Dependency analyzer test successful")
    print(f"Analysis result: {result}")
    
    # Get report
    report = analyzer.get_dependency_report()
    print(f"Dependency report: {report}")
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
