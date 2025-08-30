#!/usr/bin/env python3
"""
V2 Compliance Task 007: Enhanced Dependency Analyzer
====================================================

Advanced dependency analysis with circular dependency detection,
visualization, and optimization recommendations.

Agent: Agent-8 (Integration Enhancement Manager)
Task: V2-COMPLIANCE-007: Architecture Validation Implementation
Priority: CRITICAL - V2 Compliance Phase Finale
Status: IMPLEMENTATION PHASE 1 - Enhanced Dependency Analysis
"""

import ast
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, deque
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DependencyInfo:
    """Information about a dependency relationship."""
    source_file: str
    target_file: str
    import_type: str  # 'from', 'import', 'relative'
    line_number: int
    module_name: str
    is_circular: bool = False
    dependency_depth: int = 0


@dataclass
class CircularDependency:
    """Information about a circular dependency."""
    cycle: List[str]
    cycle_length: int
    severity: str
    affected_files: List[str]
    resolution_suggestions: List[str]


class EnhancedDependencyAnalyzer:
    """
    Enhanced dependency analyzer with advanced features.
    
    Provides:
    - Comprehensive dependency mapping
    - Circular dependency detection
    - Dependency depth analysis
    - Optimization recommendations
    - Visualization capabilities
    """
    
    def __init__(self):
        """Initialize enhanced dependency analyzer."""
        self.logger = logging.getLogger(f"{__name__}.EnhancedDependencyAnalyzer")
        
        # Dependency storage
        self.dependencies: List[DependencyInfo] = []
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)
        
        # Analysis results
        self.circular_dependencies: List[CircularDependency] = []
        self.dependency_depth_map: Dict[str, int] = {}
        self.import_statistics: Dict[str, int] = defaultdict(int)
        
        # Configuration
        self.ignore_patterns = [
            r'__pycache__',
            r'\.pyc$',
            r'\.pyo$',
            r'\.pyd$',
            r'\.egg-info$',
            r'\.git',
            r'\.venv',
            r'venv',
            r'env'
        ]
        
        self.logger.info("✅ Enhanced Dependency Analyzer initialized")
    
    def analyze_dependencies(self, source_directory: str = "src/") -> Dict[str, Any]:
        """
        Perform comprehensive dependency analysis.
        
        Args:
            source_directory: Directory to analyze
            
        Returns:
            Analysis results and statistics
        """
        self.logger.info(f"🔍 Starting comprehensive dependency analysis of {source_directory}")
        
        # Clear previous results
        self.dependencies.clear()
        self.dependency_graph.clear()
        self.reverse_dependencies.clear()
        self.circular_dependencies.clear()
        self.dependency_depth_map.clear()
        self.import_statistics.clear()
        
        # Scan for Python files
        python_files = self._find_python_files(source_directory)
        self.logger.info(f"📁 Found {len(python_files)} Python files to analyze")
        
        # Analyze each file
        for file_path in python_files:
            self._analyze_file_dependencies(file_path)
        
        # Perform advanced analysis
        self._detect_circular_dependencies()
        self._calculate_dependency_depths()
        self._analyze_import_patterns()
        self._generate_optimization_recommendations()
        
        # Generate comprehensive report
        analysis_results = self._generate_analysis_report()
        
        self.logger.info(f"✅ Dependency analysis complete: {len(self.dependencies)} dependencies found")
        return analysis_results
    
    def _find_python_files(self, source_directory: str) -> List[Path]:
        """Find all Python files in the source directory."""
        python_files = []
        
        for pattern in self.ignore_patterns:
            if re.search(pattern, source_directory):
                return []
        
        try:
            for file_path in Path(source_directory).rglob("*.py"):
                # Check if file should be ignored
                should_ignore = False
                for pattern in self.ignore_patterns:
                    if re.search(pattern, str(file_path)):
                        should_ignore = True
                        break
                
                if not should_ignore:
                    python_files.append(file_path)
                    
        except Exception as e:
            self.logger.error(f"Error finding Python files in {source_directory}: {e}")
        
        return python_files
    
    def _analyze_file_dependencies(self, file_path: Path):
        """Analyze dependencies for a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the file content
            tree = ast.parse(content)
            
            # Extract imports
            imports = self._extract_imports_from_ast(tree)
            
            # Process each import
            for import_info in imports:
                dependency = DependencyInfo(
                    source_file=str(file_path),
                    target_file=import_info['target'],
                    import_type=import_info['type'],
                    line_number=import_info['line'],
                    module_name=import_info['module']
                )
                
                self.dependencies.append(dependency)
                
                # Update dependency graphs
                self.dependency_graph[str(file_path)].add(import_info['target'])
                self.reverse_dependencies[import_info['target']].add(str(file_path))
                
                # Update import statistics
                self.import_statistics[import_info['type']] += 1
                
        except Exception as e:
            self.logger.error(f"Error analyzing dependencies in {file_path}: {e}")
    
    def _extract_imports_from_ast(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract import information from AST."""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                # Handle: import module
                for alias in node.names:
                    imports.append({
                        'type': 'import',
                        'module': alias.name,
                        'target': self._resolve_import_target(alias.name),
                        'line': node.lineno
                    })
            
            elif isinstance(node, ast.ImportFrom):
                # Handle: from module import name
                module_name = node.module or ''
                for alias in node.names:
                    full_name = f"{module_name}.{alias.name}" if module_name else alias.name
                    imports.append({
                        'type': 'from',
                        'module': full_name,
                        'target': self._resolve_import_target(module_name),
                        'line': node.lineno
                    })
        
        return imports
    
    def _resolve_import_target(self, module_name: str) -> str:
        """Resolve import target to file path."""
        # Simplified resolution - can be enhanced
        if module_name.startswith('src.'):
            return module_name.replace('.', '/') + '.py'
        elif module_name.startswith('src/'):
            return module_name + '.py'
        else:
            return f"src/{module_name.replace('.', '/')}.py"
    
    def _detect_circular_dependencies(self):
        """Detect circular dependencies using depth-first search."""
        self.logger.info("🔍 Detecting circular dependencies...")
        
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]):
            """Depth-first search to detect cycles."""
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                
                if len(cycle) > 1:  # Valid cycle
                    circular_dep = CircularDependency(
                        cycle=cycle[:-1],  # Remove duplicate end
                        cycle_length=len(cycle) - 1,
                        severity=self._calculate_cycle_severity(cycle),
                        affected_files=cycle[:-1],
                        resolution_suggestions=self._generate_resolution_suggestions(cycle)
                    )
                    
                    self.circular_dependencies.append(circular_dep)
                    
                    # Mark dependencies as circular
                    for i in range(len(cycle) - 1):
                        source = cycle[i]
                        target = cycle[i + 1]
                        for dep in self.dependencies:
                            if (dep.source_file == source and 
                                dep.target_file == target):
                                dep.is_circular = True
                
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            # Visit all dependencies
            for dependency in self.dependency_graph.get(node, []):
                dfs(dependency, path.copy())
            
            rec_stack.remove(node)
            path.pop()
        
        # Check each node for cycles
        for node in self.dependency_graph:
            if node not in visited:
                dfs(node, [])
        
        self.logger.info(f"🚨 Found {len(self.circular_dependencies)} circular dependencies")
    
    def _calculate_cycle_severity(self, cycle: List[str]) -> str:
        """Calculate severity of a circular dependency cycle."""
        cycle_length = len(cycle)
        
        if cycle_length <= 2:
            return "LOW"
        elif cycle_length <= 4:
            return "MEDIUM"
        elif cycle_length <= 6:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _generate_resolution_suggestions(self, cycle: List[str]) -> List[str]:
        """Generate suggestions for resolving circular dependencies."""
        suggestions = []
        
        if len(cycle) == 2:
            suggestions.append("Consider merging the two modules into one")
            suggestions.append("Extract common functionality to a shared module")
            suggestions.append("Use dependency injection to break the cycle")
        
        elif len(cycle) == 3:
            suggestions.append("Introduce an interface layer between modules")
            suggestions.append("Extract shared functionality to a utility module")
            suggestions.append("Restructure the dependency hierarchy")
        
        else:
            suggestions.append("Review the overall architecture design")
            suggestions.append("Consider breaking into smaller, focused modules")
            suggestions.append("Implement a facade pattern to simplify dependencies")
        
        return suggestions
    
    def _calculate_dependency_depths(self):
        """Calculate dependency depth for each file."""
        self.logger.info("🔍 Calculating dependency depths...")
        
        # Initialize depths
        for file_path in self.dependency_graph:
            self.dependency_depth_map[file_path] = 0
        
        # Calculate depths using topological sort approach
        in_degree = defaultdict(int)
        for file_path, dependencies in self.dependency_graph.items():
            for dep in dependencies:
                in_degree[dep] += 1
        
        # Find files with no incoming dependencies (depth 0)
        queue = deque([file_path for file_path in self.dependency_graph if in_degree[file_path] == 0])
        
        while queue:
            current_file = queue.popleft()
            current_depth = self.dependency_depth_map[current_file]
            
            # Update depths of dependent files
            for dependent in self.reverse_dependencies[current_file]:
                new_depth = current_depth + 1
                if new_depth > self.dependency_depth_map[dependent]:
                    self.dependency_depth_map[dependent] = new_depth
                
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
    
    def _analyze_import_patterns(self):
        """Analyze import patterns and identify optimization opportunities."""
        self.logger.info("🔍 Analyzing import patterns...")
        
        # Analyze import frequency
        module_imports = defaultdict(int)
        for dep in self.dependencies:
            module_imports[dep.module_name] += 1
        
        # Identify most imported modules
        most_imported = sorted(module_imports.items(), key=lambda x: x[1], reverse=True)[:10]
        
        self.logger.info("📊 Most imported modules:")
        for module, count in most_imported:
            self.logger.info(f"  {module}: {count} imports")
    
    def _generate_optimization_recommendations(self):
        """Generate optimization recommendations based on analysis."""
        self.logger.info("🔍 Generating optimization recommendations...")
        
        recommendations = []
        
        # Circular dependency recommendations
        if self.circular_dependencies:
            recommendations.append({
                "type": "circular_dependencies",
                "priority": "HIGH",
                "description": f"Resolve {len(self.circular_dependencies)} circular dependencies",
                "impact": "High - affects build and runtime stability"
            })
        
        # Deep dependency recommendations
        deep_dependencies = [f for f, d in self.dependency_depth_map.items() if d > 5]
        if deep_dependencies:
            recommendations.append({
                "type": "deep_dependencies",
                "priority": "MEDIUM",
                "description": f"Reduce dependency depth for {len(deep_dependencies)} files",
                "impact": "Medium - affects build time and maintainability"
            })
        
        # Import optimization recommendations
        if self.import_statistics.get('from', 0) > self.import_statistics.get('import', 0) * 2:
            recommendations.append({
                "type": "import_optimization",
                "priority": "LOW",
                "description": "Consider using more specific imports to reduce memory usage",
                "impact": "Low - minor performance improvement"
            })
        
        return recommendations
    
    def _generate_analysis_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report."""
        total_files = len(self.dependency_graph)
        total_dependencies = len(self.dependencies)
        circular_count = len(self.circular_dependencies)
        
        # Calculate statistics
        avg_dependencies_per_file = total_dependencies / total_files if total_files > 0 else 0
        max_depth = max(self.dependency_depth_map.values()) if self.dependency_depth_map else 0
        
        report = {
            "summary": {
                "total_files_analyzed": total_files,
                "total_dependencies": total_dependencies,
                "circular_dependencies": circular_count,
                "average_dependencies_per_file": round(avg_dependencies_per_file, 2),
                "maximum_dependency_depth": max_depth
            },
            "circular_dependencies": [
                {
                    "cycle": cd.cycle,
                    "cycle_length": cd.cycle_length,
                    "severity": cd.severity,
                    "affected_files": cd.affected_files,
                    "resolution_suggestions": cd.resolution_suggestions
                }
                for cd in self.circular_dependencies
            ],
            "dependency_depth_analysis": {
                "depth_distribution": self._get_depth_distribution(),
                "files_by_depth": self._get_files_by_depth()
            },
            "import_statistics": dict(self.import_statistics),
            "optimization_recommendations": self._generate_optimization_recommendations()
        }
        
        return report
    
    def _get_depth_distribution(self) -> Dict[int, int]:
        """Get distribution of files by dependency depth."""
        depth_dist = defaultdict(int)
        for depth in self.dependency_depth_map.values():
            depth_dist[depth] += 1
        return dict(depth_dist)
    
    def _get_files_by_depth(self) -> Dict[int, List[str]]:
        """Get files grouped by dependency depth."""
        files_by_depth = defaultdict(list)
        for file_path, depth in self.dependency_depth_map.items():
            files_by_depth[depth].append(file_path)
        return dict(files_by_depth)
    
    def export_analysis_results(self, output_file: str = "dependency_analysis_results.json"):
        """Export analysis results to JSON file."""
        try:
            results = self._generate_analysis_report()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"✅ Analysis results exported to {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting results: {e}")
            return False


def main():
    """Main entry point for dependency analysis."""
    logger.info("🚀 Starting V2 Compliance Task 007: Enhanced Dependency Analysis")
    
    # Initialize analyzer
    analyzer = EnhancedDependencyAnalyzer()
    
    # Perform analysis
    results = analyzer.analyze_dependencies()
    
    # Export results
    analyzer.export_analysis_results()
    
    # Display summary
    summary = results['summary']
    logger.info(f"✅ Dependency analysis complete:")
    logger.info(f"  Files analyzed: {summary['total_files_analyzed']}")
    logger.info(f"  Dependencies found: {summary['total_dependencies']}")
    logger.info(f"  Circular dependencies: {summary['circular_dependencies']}")
    logger.info(f"  Max dependency depth: {summary['maximum_dependency_depth']}")
    
    return results


if __name__ == "__main__":
    main()
