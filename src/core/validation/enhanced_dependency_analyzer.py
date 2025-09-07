#!/usr/bin/env python3
"""
Enhanced Dependency Analyzer - Agent Cellphone V2
================================================

Advanced dependency analysis with circular dependency detection, dependency
visualization, and architectural impact analysis.

Follows V2 coding standards: ≤400 lines per module, OOP design, SRP.
"""

import ast
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple, DefaultDict
from dataclasses import dataclass
from collections import defaultdict
import json
import networkx as nx
from datetime import datetime


@dataclass
class DependencyInfo:
    """Information about a dependency."""
    module_name: str
    import_type: str  # 'import', 'from_import', 'relative_import'
    import_path: str
    line_number: int
    is_internal: bool
    is_external: bool


@dataclass
class CircularDependency:
    """Information about a circular dependency."""
    cycle: List[str]
    severity: str  # 'critical', 'high', 'medium', 'low'
    impact_score: float
    affected_modules: List[str]


@dataclass
class DependencyMetrics:
    """Dependency analysis metrics."""
    total_dependencies: int
    internal_dependencies: int
    external_dependencies: int
    circular_dependencies: int
    max_dependency_depth: int
    average_dependencies_per_module: float
    dependency_complexity_score: float


class EnhancedDependencyAnalyzer:
    """
    Enhanced dependency analyzer with circular dependency detection.
    
    Provides comprehensive dependency analysis, circular dependency detection,
    dependency visualization, and architectural impact assessment.
    """
    
    def __init__(self):
        """Initialize Enhanced Dependency Analyzer."""
        self.logger = logging.getLogger(__name__)
        self.dependency_graph = defaultdict(set)
        self.reverse_dependency_graph = defaultdict(set)
        self.module_info = {}
        self.circular_dependencies = []
        self.dependency_metrics = None
        
    def analyze_dependencies(self, target_path: str) -> Dict[str, Any]:
        """
        Analyze dependencies for a target path (file or directory).
        
        Args:
            target_path: Path to analyze
            
        Returns:
            Comprehensive dependency analysis results
        """
        self.logger.info(f"Starting enhanced dependency analysis for: {target_path}")
        
        target_path_obj = Path(target_path)
        
        if target_path_obj.is_file():
            return self._analyze_single_file(target_path_obj)
        elif target_path_obj.is_dir():
            return self._analyze_directory(target_path_obj)
        else:
            return {
                "error": f"Invalid path: {target_path}",
                "status": "FAILED"
            }
    
    def _analyze_single_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze dependencies for a single file."""
        if file_path.suffix != '.py':
            return {"error": "Not a Python file", "status": "SKIPPED"}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST
            tree = ast.parse(content)
            
            # Extract dependencies
            dependencies = self._extract_dependencies(file_path, tree, content)
            
            # Build dependency graph
            self._build_dependency_graph(file_path, dependencies)
            
            # Analyze for circular dependencies
            circular_deps = self._detect_circular_dependencies()
            
            # Calculate metrics
            metrics = self._calculate_dependency_metrics()
            
            return {
                "file_path": str(file_path),
                "dependencies": dependencies,
                "circular_dependencies": circular_deps,
                "metrics": metrics,
                "status": "COMPLETED"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to analyze file {file_path}: {e}")
            return {
                "file_path": str(file_path),
                "error": str(e),
                "status": "FAILED"
            }
    
    def _analyze_directory(self, dir_path: Path) -> Dict[str, Any]:
        """Analyze dependencies for a directory recursively."""
        python_files = list(dir_path.rglob("*.py"))
        
        self.logger.info(f"Found {len(python_files)} Python files to analyze")
        
        all_results = []
        for file_path in python_files:
            result = self._analyze_single_file(file_path)
            all_results.append(result)
        
        # Build comprehensive dependency graph
        self._build_comprehensive_dependency_graph()
        
        # Detect circular dependencies across the entire codebase
        circular_deps = self._detect_circular_dependencies()
        
        # Calculate overall metrics
        overall_metrics = self._calculate_overall_metrics()
        
        # Generate dependency visualization data
        visualization_data = self._generate_visualization_data()
        
        return {
            "directory_path": str(dir_path),
            "file_count": len(python_files),
            "file_results": all_results,
            "circular_dependencies": circular_deps,
            "overall_metrics": overall_metrics,
            "visualization_data": visualization_data,
            "status": "COMPLETED"
        }
    
    def _extract_dependencies(self, file_path: Path, tree: ast.AST, content: str) -> List[DependencyInfo]:
        """Extract all dependencies from a Python file."""
        dependencies = []
        lines = content.splitlines()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                # Handle 'import module' statements
                for alias in node.names:
                    dep_info = DependencyInfo(
                        module_name=alias.name,
                        import_type="import",
                        import_path=alias.name,
                        line_number=getattr(node, 'lineno', 0),
                        is_internal=self._is_internal_module(alias.name, file_path),
                        is_external=self._is_external_module(alias.name)
                    )
                    dependencies.append(dep_info)
                    
            elif isinstance(node, ast.ImportFrom):
                # Handle 'from module import item' statements
                module_name = node.module or ""
                if module_name:
                    dep_info = DependencyInfo(
                        module_name=module_name,
                        import_type="from_import",
                        import_path=module_name,
                        line_number=getattr(node, 'lineno', 0),
                        is_internal=self._is_internal_module(module_name, file_path),
                        is_external=self._is_external_module(module_name)
                    )
                    dependencies.append(dep_info)
        
        # Also check for relative imports in the content
        relative_imports = self._extract_relative_imports(content, file_path)
        dependencies.extend(relative_imports)
        
        return dependencies
    
    def _extract_relative_imports(self, content: str, file_path: Path) -> List[DependencyInfo]:
        """Extract relative imports from content."""
        relative_imports = []
        lines = content.splitlines()
        
        for line_num, line in enumerate(lines, 1):
            # Look for relative import patterns
            relative_patterns = [
                r'from \.(\w+) import',
                r'from \.\.(\w+) import',
                r'from \.\.\.(\w+) import'
            ]
            
            for pattern in relative_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    dep_info = DependencyInfo(
                        module_name=match,
                        import_type="relative_import",
                        import_path=f".{match}",
                        line_number=line_num,
                        is_internal=True,
                        is_external=False
                    )
                    relative_imports.append(dep_info)
        
        return relative_imports
    
    def _is_internal_module(self, module_name: str, current_file: Path) -> bool:
        """Check if a module is internal to the project."""
        # Check if it's a relative import
        if module_name.startswith('.'):
            return True
        
        # Check if it's a project module
        project_modules = [
            'src', 'agent_workspaces', 'config', 'tests', 'docs'
        ]
        
        for project_module in project_modules:
            if module_name.startswith(project_module):
                return True
        
        return False
    
    def _is_external_module(self, module_name: str) -> bool:
        """Check if a module is external (third-party)."""
        # Common external modules
        external_modules = [
            'os', 'sys', 'pathlib', 'json', 'logging', 'datetime',
            'typing', 'dataclasses', 'collections', 're', 'ast',
            'networkx', 'numpy', 'pandas', 'requests', 'flask'
        ]
        
        return module_name in external_modules
    
    def _build_dependency_graph(self, file_path: Path, dependencies: List[DependencyInfo]):
        """Build dependency graph for a single file."""
        module_name = self._get_module_name(file_path)
        
        for dep in dependencies:
            self.dependency_graph[module_name].add(dep.import_path)
            self.reverse_dependency_graph[dep.import_path].add(module_name)
    
    def _build_comprehensive_dependency_graph(self):
        """Build comprehensive dependency graph across all analyzed files."""
        # This method would be called after analyzing all files
        # to build the complete dependency graph
        pass
    
    def _get_module_name(self, file_path: Path) -> str:
        """Get module name from file path."""
        # Convert file path to module name
        parts = file_path.parts
        
        # Find the project root (assuming we're in the project directory)
        try:
            project_root_index = parts.index('src') if 'src' in parts else 0
            module_parts = parts[project_root_index:]
            
            # Remove .py extension and convert to module notation
            if module_parts[-1].endswith('.py'):
                module_parts[-1] = module_parts[-1][:-3]
            
            # Convert to module notation
            module_name = '.'.join(module_parts)
            
            # Handle __init__.py files
            if '__init__.py' in module_parts:
                module_name = '.'.join(module_parts[:-1])
            
            return module_name
            
        except (ValueError, IndexError):
            # Fallback to file name without extension
            return file_path.stem
    
    def _detect_circular_dependencies(self) -> List[CircularDependency]:
        """Detect circular dependencies in the dependency graph."""
        circular_deps = []
        
        # Use NetworkX for cycle detection
        try:
            G = nx.DiGraph()
            
            # Add edges to the graph
            for module, deps in self.dependency_graph.items():
                for dep in deps:
                    G.add_edge(module, dep)
            
            # Find all cycles
            cycles = list(nx.simple_cycles(G))
            
            for cycle in cycles:
                # Calculate impact score based on cycle length and module importance
                impact_score = self._calculate_cycle_impact(cycle)
                
                # Determine severity
                severity = self._determine_cycle_severity(cycle, impact_score)
                
                # Get affected modules
                affected_modules = self._get_affected_modules(cycle)
                
                circular_dep = CircularDependency(
                    cycle=cycle,
                    severity=severity,
                    impact_score=impact_score,
                    affected_modules=affected_modules
                )
                
                circular_deps.append(circular_dep)
                
        except ImportError:
            self.logger.warning("NetworkX not available, using fallback cycle detection")
            circular_deps = self._fallback_cycle_detection()
        
        self.circular_dependencies = circular_deps
        return circular_deps
    
    def _fallback_cycle_detection(self) -> List[CircularDependency]:
        """Fallback cycle detection without NetworkX."""
        # Simple depth-first search for cycles
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(node, path):
            if node in rec_stack:
                # Found a cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:]
                cycles.append(cycle)
                return
            
            if node in visited:
                return
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.dependency_graph.get(node, set()):
                dfs(neighbor, path + [neighbor])
            
            rec_stack.remove(node)
        
        # Check each node for cycles
        for node in self.dependency_graph:
            if node not in visited:
                dfs(node, [node])
        
        # Convert to CircularDependency objects
        circular_deps = []
        for cycle in cycles:
            impact_score = self._calculate_cycle_impact(cycle)
            severity = self._determine_cycle_severity(cycle, impact_score)
            affected_modules = self._get_affected_modules(cycle)
            
            circular_dep = CircularDependency(
                cycle=cycle,
                severity=severity,
                impact_score=impact_score,
                affected_modules=affected_modules
            )
            circular_deps.append(circular_dep)
        
        return circular_deps
    
    def _calculate_cycle_impact(self, cycle: List[str]) -> float:
        """Calculate impact score for a dependency cycle."""
        # Impact factors:
        # - Cycle length (longer cycles = higher impact)
        # - Module importance (core modules = higher impact)
        # - Dependency depth (deeper dependencies = higher impact)
        
        cycle_length = len(cycle)
        length_factor = min(cycle_length / 5.0, 1.0)  # Normalize to 0-1
        
        # Check if cycle involves core modules
        core_modules = ['src', 'core', 'main', 'app']
        core_involvement = any(any(core in module for core in core_modules) for module in cycle)
        core_factor = 1.5 if core_involvement else 1.0
        
        # Calculate dependency depth
        depth_factor = self._calculate_dependency_depth(cycle)
        
        # Combine factors
        impact_score = (length_factor * 0.4 + depth_factor * 0.4 + core_factor * 0.2) * 10
        
        return round(impact_score, 2)
    
    def _calculate_dependency_depth(self, cycle: List[str]) -> float:
        """Calculate dependency depth for a cycle."""
        # This is a simplified calculation
        # In a real implementation, you'd analyze the actual dependency tree
        
        total_depth = 0
        for module in cycle:
            # Count how many modules depend on this one
            dependents = len(self.reverse_dependency_graph.get(module, set()))
            total_depth += dependents
        
        # Normalize to 0-1 range
        max_possible_depth = len(self.dependency_graph) * 10  # Arbitrary max
        depth_factor = min(total_depth / max_possible_depth, 1.0)
        
        return depth_factor
    
    def _determine_cycle_severity(self, cycle: List[str], impact_score: float) -> str:
        """Determine severity level for a dependency cycle."""
        if impact_score >= 8.0:
            return "critical"
        elif impact_score >= 6.0:
            return "high"
        elif impact_score >= 4.0:
            return "medium"
        else:
            return "low"
    
    def _get_affected_modules(self, cycle: List[str]) -> List[str]:
        """Get list of modules affected by a dependency cycle."""
        affected = set(cycle)
        
        # Add modules that depend on any module in the cycle
        for module in cycle:
            dependents = self.reverse_dependency_graph.get(module, set())
            affected.update(dependents)
        
        return list(affected)
    
    def _calculate_dependency_metrics(self) -> DependencyMetrics:
        """Calculate comprehensive dependency metrics."""
        total_deps = sum(len(deps) for deps in self.dependency_graph.values())
        internal_deps = sum(
            sum(1 for dep in deps if self._is_internal_module(dep, Path("dummy")))
            for deps in self.dependency_graph.values()
        )
        external_deps = total_deps - internal_deps
        
        circular_count = len(self.circular_dependencies)
        
        # Calculate max dependency depth
        max_depth = self._calculate_max_dependency_depth()
        
        # Calculate average dependencies per module
        module_count = len(self.dependency_graph)
        avg_deps = total_deps / module_count if module_count > 0 else 0
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity_score()
        
        self.dependency_metrics = DependencyMetrics(
            total_dependencies=total_deps,
            internal_dependencies=internal_deps,
            external_dependencies=external_deps,
            circular_dependencies=circular_count,
            max_dependency_depth=max_depth,
            average_dependencies_per_module=round(avg_deps, 2),
            dependency_complexity_score=round(complexity_score, 2)
        )
        
        return self.dependency_metrics
    
    def _calculate_max_dependency_depth(self) -> int:
        """Calculate maximum dependency depth."""
        # This is a simplified calculation
        # In a real implementation, you'd traverse the dependency tree
        
        max_depth = 0
        for module in self.dependency_graph:
            depth = self._calculate_module_depth(module, set())
            max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _calculate_module_depth(self, module: str, visited: Set[str]) -> int:
        """Calculate dependency depth for a specific module."""
        if module in visited:
            return 0  # Avoid infinite recursion
        
        visited.add(module)
        max_depth = 0
        
        for dep in self.dependency_graph.get(module, set()):
            if dep in self.dependency_graph:
                depth = self._calculate_module_depth(dep, visited) + 1
                max_depth = max(max_depth, depth)
        
        visited.remove(module)
        return max_depth
    
    def _calculate_complexity_score(self) -> float:
        """Calculate overall dependency complexity score."""
        # Factors: number of dependencies, circular dependencies, depth
        total_deps = sum(len(deps) for deps in self.dependency_graph.values())
        module_count = len(self.dependency_graph)
        circular_count = len(self.circular_dependencies)
        
        # Handle edge case when no modules exist
        if module_count == 0:
            return 0.0
        
        # Normalize factors
        deps_factor = min(total_deps / (module_count * 10), 1.0)  # Normalize to 0-1
        circular_factor = min(circular_count / 10, 1.0)  # Normalize to 0-1
        
        # Calculate complexity score (0-10)
        complexity_score = (deps_factor * 0.6 + circular_factor * 0.4) * 10
        
        return complexity_score
    
    def _calculate_overall_metrics(self) -> Dict[str, Any]:
        """Calculate overall metrics for the entire codebase."""
        if not self.dependency_metrics:
            self._calculate_dependency_metrics()
        
        # Additional overall metrics
        total_modules = len(self.dependency_graph)
        
        # Module distribution by dependency count
        dependency_distribution = defaultdict(int)
        for deps in self.dependency_graph.values():
            dep_count = len(deps)
            if dep_count <= 5:
                dependency_distribution["low"] += 1
            elif dep_count <= 15:
                dependency_distribution["medium"] += 1
            else:
                dependency_distribution["high"] += 1
        
        # Circular dependency analysis
        critical_cycles = [cd for cd in self.circular_dependencies if cd.severity == "critical"]
        high_cycles = [cd for cd in self.circular_dependencies if cd.severity == "high"]
        
        return {
            "total_modules": total_modules,
            "dependency_distribution": dict(dependency_distribution),
            "circular_dependency_breakdown": {
                "critical": len(critical_cycles),
                "high": len(high_cycles),
                "medium": len([cd for cd in self.circular_dependencies if cd.severity == "medium"]),
                "low": len([cd for cd in self.circular_dependencies if cd.severity == "low"])
            },
            "overall_health_score": self._calculate_health_score(),
            "recommendations": self._generate_recommendations()
        }
    
    def _calculate_health_score(self) -> float:
        """Calculate overall dependency health score."""
        if not self.dependency_metrics:
            return 0.0
        
        # Health factors (0-100 scale)
        circular_penalty = self.dependency_metrics.circular_dependencies * 10
        complexity_penalty = self.dependency_metrics.dependency_complexity_score * 5
        depth_penalty = min(self.dependency_metrics.max_dependency_depth * 2, 20)
        
        # Base score
        base_score = 100
        
        # Apply penalties
        health_score = max(0, base_score - circular_penalty - complexity_penalty - depth_penalty)
        
        return round(health_score, 1)
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for improving dependency health."""
        recommendations = []
        
        if self.dependency_metrics.circular_dependencies > 0:
            recommendations.append("Resolve circular dependencies to improve system stability")
        
        if self.dependency_metrics.dependency_complexity_score > 7:
            recommendations.append("Reduce dependency complexity by consolidating imports")
        
        if self.dependency_metrics.max_dependency_depth > 5:
            recommendations.append("Reduce dependency depth by flattening the dependency tree")
        
        if self.dependency_metrics.average_dependencies_per_module > 15:
            recommendations.append("Reduce average dependencies per module for better maintainability")
        
        if not recommendations:
            recommendations.append("Dependency structure is healthy - maintain current practices")
        
        return recommendations
    
    def _generate_visualization_data(self) -> Dict[str, Any]:
        """Generate data for dependency visualization."""
        # Node data for graph visualization
        nodes = []
        for module in self.dependency_graph:
            node_data = {
                "id": module,
                "label": module.split('.')[-1],  # Use last part as label
                "group": self._get_module_group(module),
                "dependency_count": len(self.dependency_graph[module]),
                "is_circular": any(module in cycle.cycle for cycle in self.circular_dependencies)
            }
            nodes.append(node_data)
        
        # Edge data for graph visualization
        edges = []
        for module, deps in self.dependency_graph.items():
            for dep in deps:
                edge_data = {
                    "from": module,
                    "to": dep,
                    "is_circular": any(module in cycle.cycle and dep in cycle.cycle for cycle in self.circular_dependencies)
                }
                edges.append(edge_data)
        
        return {
            "nodes": nodes,
            "edges": edges,
            "circular_dependencies": [
                {
                    "cycle": cycle.cycle,
                    "severity": cycle.severity,
                    "impact_score": cycle.impact_score
                }
                for cycle in self.circular_dependencies
            ]
        }
    
    def _get_module_group(self, module: str) -> str:
        """Get module group for visualization."""
        if module.startswith('src.core'):
            return "core"
        elif module.startswith('src.services'):
            return "services"
        elif module.startswith('agent_workspaces'):
            return "agents"
        elif module.startswith('tests'):
            return "tests"
        elif module.startswith('config'):
            return "config"
        else:
            return "other"
    
    def export_results(self, output_path: str, format_type: str = "json") -> bool:
        """
        Export analysis results to file.
        
        Args:
            output_path: Path to output file
            format_type: Output format ('json', 'html', 'csv')
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            if format_type == "json":
                return self._export_json(output_path)
            elif format_type == "html":
                return self._export_html(output_path)
            elif format_type == "csv":
                return self._export_csv(output_path)
            else:
                self.logger.error(f"Unsupported format: {format_type}")
                return False
                
        except Exception as e:
            self.logger.error(f"Export failed: {e}")
            return False
    
    def _export_json(self, output_path: str) -> bool:
        """Export results to JSON format."""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "dependency_graph": dict(self.dependency_graph),
            "circular_dependencies": [
                {
                    "cycle": cd.cycle,
                    "severity": cd.severity,
                    "impact_score": cd.impact_score,
                    "affected_modules": cd.affected_modules
                }
                for cd in self.circular_dependencies
            ],
            "metrics": vars(self.dependency_metrics) if self.dependency_metrics else None,
            "overall_metrics": self._calculate_overall_metrics(),
            "visualization_data": self._generate_visualization_data()
        }
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return True
    
    def _export_html(self, output_path: str) -> bool:
        """Export results to HTML format."""
        # This would generate an interactive HTML report
        # For now, just create a basic HTML structure
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dependency Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .metric {{ margin: 10px 0; padding: 10px; border: 1px solid #ccc; }}
                .critical {{ background-color: #ffebee; }}
                .high {{ background-color: #fff3e0; }}
                .medium {{ background-color: #f3e5f5; }}
                .low {{ background-color: #e8f5e8; }}
            </style>
        </head>
        <body>
            <h1>Dependency Analysis Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>Summary</h2>
            <div class="metric">
                <strong>Total Modules:</strong> {len(self.dependency_graph)}<br>
                <strong>Circular Dependencies:</strong> {len(self.circular_dependencies)}<br>
                <strong>Health Score:</strong> {self._calculate_health_score()}/100
            </div>
            
            <h2>Circular Dependencies</h2>
            {self._generate_html_circular_deps()}
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return True
    
    def _generate_html_circular_deps(self) -> str:
        """Generate HTML for circular dependencies section."""
        if not self.circular_dependencies:
            return "<p>No circular dependencies found.</p>"
        
        html = ""
        for cd in self.circular_dependencies:
            severity_class = cd.severity
            html += f"""
            <div class="metric {severity_class}">
                <strong>Cycle ({cd.severity.upper()}):</strong><br>
                {' → '.join(cd.cycle)}<br>
                <strong>Impact Score:</strong> {cd.impact_score}/10<br>
                <strong>Affected Modules:</strong> {', '.join(cd.affected_modules)}
            </div>
            """
        
        return html
    
    def _export_csv(self, output_path: str) -> bool:
        """Export results to CSV format."""
        # This would export dependency data in CSV format
        # For now, just create a placeholder
        csv_content = "Module,Dependencies,Circular,Severity\n"
        
        for module, deps in self.dependency_graph.items():
            is_circular = any(module in cycle.cycle for cycle in self.circular_dependencies)
            severity = "none"
            if is_circular:
                for cycle in self.circular_dependencies:
                    if module in cycle.cycle:
                        severity = cycle.severity
                        break
            
            csv_content += f"{module},{len(deps)},{is_circular},{severity}\n"
        
        with open(output_path, 'w') as f:
            f.write(csv_content)
        
        return True


# CLI interface for testing
def main():
    """CLI interface for enhanced dependency analysis."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Dependency Analyzer CLI")
    parser.add_argument("--analyze", required=True, help="Path to analyze (file or directory)")
    parser.add_argument("--output", "-o", help="Output file for results")
    parser.add_argument("--format", choices=["json", "html", "csv"], default="json", help="Output format")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run analysis
    analyzer = EnhancedDependencyAnalyzer()
    results = analyzer.analyze_dependencies(args.analyze)
    
    # Output results
    if args.output:
        if analyzer.export_results(args.output, args.format):
            print(f"Results exported to: {args.output}")
        else:
            print("Export failed")
    else:
        # Print summary to console
        print(f"\n📊 Dependency Analysis Summary:")
        print(f"Status: {results.get('status', 'UNKNOWN')}")
        
        if 'overall_metrics' in results:
            metrics = results['overall_metrics']
            print(f"Total Modules: {metrics.get('total_modules', 0)}")
            print(f"Circular Dependencies: {len(analyzer.circular_dependencies)}")
            print(f"Health Score: {analyzer._calculate_health_score()}/100")
        
        if analyzer.circular_dependencies:
            print(f"\n🚨 Circular Dependencies Found:")
            for cd in analyzer.circular_dependencies:
                print(f"  {cd.severity.upper()}: {' → '.join(cd.cycle)} (Impact: {cd.impact_score}/10)")


if __name__ == "__main__":
    main()
