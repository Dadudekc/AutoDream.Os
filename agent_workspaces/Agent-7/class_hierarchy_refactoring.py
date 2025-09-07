#!/usr/bin/env python3
"""
Class Hierarchy Refactoring - MODULAR-002 Mission
================================================

Refactor class hierarchies to improve code organization and maintainability.
Implements advanced class analysis, hierarchy optimization, and refactoring tools.

Author: Agent-7 - Quality Completion Optimization Manager
Mission: MODULAR-002 - Class Hierarchy Refactoring
Priority: CRITICAL - Captain's Directive
"""

import ast
import json
import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from datetime import datetime
import inspect


@dataclass
class ClassInfo:
    """Represents information about a class"""
    name: str
    file_path: str
    line_number: int
    base_classes: List[str]
    methods: List[str]
    attributes: List[str]
    docstring: str
    complexity: int
    inheritance_depth: int
    dependencies: List[str]


@dataclass
class HierarchyNode:
    """Represents a node in the class hierarchy"""
    class_name: str
    file_path: str
    base_classes: List[str]
    derived_classes: List[str]
    level: int
    methods_count: int
    attributes_count: int
    complexity_score: float


@dataclass
class RefactoringRecommendation:
    """Represents a refactoring recommendation"""
    type: str  # EXTRACT, MERGE, SPLIT, SIMPLIFY, REORGANIZE
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    description: str
    target_classes: List[str]
    benefits: List[str]
    implementation_steps: List[str]
    estimated_effort: str


class ClassHierarchyAnalyzer:
    """Analyzes class hierarchies and identifies refactoring opportunities"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.classes = {}
        self.hierarchy_graph = {}
        self.inheritance_chains = {}
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for class analysis"""
        logger = logging.getLogger("ClassHierarchyAnalyzer")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def analyze_file(self, file_path: str) -> List[ClassInfo]:
        """Analyze a Python file for class definitions"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = self._extract_class_info(node, file_path)
                    classes.append(class_info)
                    self.classes[class_info.name] = class_info
            
            self.logger.info(f"Analyzed {len(classes)} classes in {file_path}")
            return classes
            
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {e}")
            return []
    
    def _extract_class_info(self, class_node: ast.ClassDef, file_path: str) -> ClassInfo:
        """Extract detailed information about a class"""
        # Get base classes
        base_classes = []
        for base in class_node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_classes.append(self._get_attribute_name(base))
        
        # Get methods
        methods = []
        for item in class_node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
        
        # Get attributes
        attributes = []
        for item in class_node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)
        
        # Get docstring
        docstring = ast.get_docstring(class_node) or ""
        
        # Calculate complexity
        complexity = self._calculate_complexity(class_node)
        
        # Calculate inheritance depth
        inheritance_depth = len(base_classes)
        
        # Get dependencies
        dependencies = self._extract_dependencies(class_node)
        
        return ClassInfo(
            name=class_node.name,
            file_path=file_path,
            line_number=class_node.lineno,
            base_classes=base_classes,
            methods=methods,
            attributes=attributes,
            docstring=docstring,
            complexity=complexity,
            inheritance_depth=inheritance_depth,
            dependencies=dependencies
        )
    
    def _get_attribute_name(self, attr_node: ast.Attribute) -> str:
        """Get the full name of an attribute node"""
        if isinstance(attr_node.value, ast.Name):
            return f"{attr_node.value.id}.{attr_node.attr}"
        elif isinstance(attr_node.value, ast.Attribute):
            return f"{self._get_attribute_name(attr_node.value)}.{attr_node.attr}"
        else:
            return attr_node.attr
    
    def _calculate_complexity(self, class_node: ast.ClassDef) -> int:
        """Calculate cyclomatic complexity of a class"""
        complexity = 1  # Base complexity
        
        for item in class_node.body:
            if isinstance(item, ast.If):
                complexity += 1
            elif isinstance(item, ast.For):
                complexity += 1
            elif isinstance(item, ast.While):
                complexity += 1
            elif isinstance(item, ast.Try):
                complexity += 1
            elif isinstance(item, ast.FunctionDef):
                complexity += self._calculate_function_complexity(item)
        
        return complexity
    
    def _calculate_function_complexity(self, func_node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1
        
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
        
        return complexity
    
    def _extract_dependencies(self, class_node: ast.ClassDef) -> List[str]:
        """Extract dependencies from a class"""
        dependencies = set()
        
        for node in ast.walk(class_node):
            if isinstance(node, ast.Name):
                if node.id not in ['self', 'cls'] and not node.id.startswith('_'):
                    dependencies.add(node.id)
            elif isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name) and node.value.id not in ['self', 'cls']:
                    dependencies.add(node.value.id)
        
        return list(dependencies)
    
    def build_hierarchy_graph(self) -> Dict[str, HierarchyNode]:
        """Build the complete class hierarchy graph"""
        self.logger.info("Building class hierarchy graph")
        
        # Initialize hierarchy nodes
        for class_name, class_info in self.classes.items():
            self.hierarchy_graph[class_name] = HierarchyNode(
                class_name=class_name,
                file_path=class_info.file_path,
                base_classes=class_info.base_classes.copy(),
                derived_classes=[],
                level=0,
                methods_count=len(class_info.methods),
                attributes_count=len(class_info.attributes),
                complexity_score=class_info.complexity
            )
        
        # Build inheritance relationships
        for class_name, class_info in self.classes.items():
            for base_class in class_info.base_classes:
                if base_class in self.hierarchy_graph:
                    self.hierarchy_graph[base_class].derived_classes.append(class_name)
        
        # Calculate hierarchy levels
        self._calculate_hierarchy_levels()
        
        return self.hierarchy_graph
    
    def _calculate_hierarchy_levels(self):
        """Calculate the level of each class in the hierarchy"""
        # Find root classes (no base classes)
        root_classes = [name for name, node in self.hierarchy_graph.items() 
                       if not node.base_classes]
        
        # Assign levels starting from roots
        for root in root_classes:
            self._assign_level_recursive(root, 0)
    
    def _assign_level_recursive(self, class_name: str, level: int):
        """Recursively assign levels to classes in the hierarchy"""
        if class_name in self.hierarchy_graph:
            self.hierarchy_graph[class_name].level = level
            
            # Assign levels to derived classes
            for derived in self.hierarchy_graph[class_name].derived_classes:
                self._assign_level_recursive(derived, level + 1)
    
    def identify_refactoring_opportunities(self) -> List[RefactoringRecommendation]:
        """Identify refactoring opportunities in the class hierarchy"""
        recommendations = []
        
        # Analyze inheritance depth
        deep_inheritance = [name for name, node in self.hierarchy_graph.items() 
                           if node.level > 3]
        if deep_inheritance:
            recommendations.append(RefactoringRecommendation(
                type="SIMPLIFY",
                priority="HIGH",
                description="Deep inheritance hierarchy detected",
                target_classes=deep_inheritance,
                benefits=["Reduced coupling", "Improved maintainability", "Easier testing"],
                implementation_steps=[
                    "Review inheritance relationships",
                    "Consider composition over inheritance",
                    "Extract common functionality to mixins",
                    "Flatten hierarchy where possible"
                ],
                estimated_effort="2-4 hours"
            ))
        
        # Analyze large classes
        large_classes = [name for name, node in self.hierarchy_graph.items() 
                        if node.methods_count > 10 or node.attributes_count > 15]
        if large_classes:
            recommendations.append(RefactoringRecommendation(
                type="SPLIT",
                priority="CRITICAL",
                description="Large classes detected - violate Single Responsibility Principle",
                target_classes=large_classes,
                benefits=["Better separation of concerns", "Easier maintenance", "Improved testability"],
                implementation_steps=[
                    "Identify distinct responsibilities",
                    "Extract related methods to new classes",
                    "Use composition to delegate functionality",
                    "Apply Single Responsibility Principle"
                ],
                estimated_effort="3-6 hours"
            ))
        
        # Analyze complex classes
        complex_classes = [name for name, node in self.hierarchy_graph.items() 
                          if node.complexity_score > 20]
        if complex_classes:
            recommendations.append(RefactoringRecommendation(
                type="SIMPLIFY",
                priority="HIGH",
                description="High complexity classes detected",
                target_classes=complex_classes,
                benefits=["Improved readability", "Easier debugging", "Better maintainability"],
                implementation_steps=[
                    "Extract complex methods to helper classes",
                    "Simplify conditional logic",
                    "Break down large methods",
                    "Use strategy pattern for complex behavior"
                ],
                estimated_effort="2-4 hours"
            ))
        
        # Analyze inheritance chains
        long_chains = self._identify_long_inheritance_chains()
        if long_chains:
            recommendations.append(RefactoringRecommendation(
                type="REORGANIZE",
                priority="MEDIUM",
                description="Long inheritance chains detected",
                target_classes=long_chains,
                benefits=["Reduced coupling", "Improved flexibility", "Better testability"],
                implementation_steps=[
                    "Review inheritance relationships",
                    "Consider using interfaces",
                    "Implement composition patterns",
                    "Break long chains into smaller hierarchies"
                ],
                estimated_effort="2-3 hours"
            ))
        
        return recommendations
    
    def _identify_long_inheritance_chains(self) -> List[str]:
        """Identify classes in long inheritance chains"""
        long_chains = []
        
        for class_name, node in self.hierarchy_graph.items():
            if node.level > 2:  # More than 2 levels deep
                # Check if this class has many derived classes
                if len(node.derived_classes) > 2:
                    long_chains.append(class_name)
        
        return long_chains
    
    def generate_refactoring_plan(self, recommendations: List[RefactoringRecommendation]) -> str:
        """Generate a comprehensive refactoring plan"""
        output = []
        
        # Header
        output.append("=" * 80)
        output.append("CLASS HIERARCHY REFACTORING PLAN - MODULAR-002")
        output.append("=" * 80)
        output.append(f"Generated: {datetime.now().isoformat()}")
        output.append(f"Total Classes Analyzed: {len(self.classes)}")
        output.append(f"Refactoring Opportunities: {len(recommendations)}")
        
        # Summary
        output.append("")
        output.append("REFACTORING SUMMARY:")
        output.append("-" * 40)
        
        priority_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for rec in recommendations:
            priority_counts[rec.priority] += 1
        
        for priority, count in priority_counts.items():
            if count > 0:
                output.append(f"{priority}: {count} opportunities")
        
        # Detailed Recommendations
        output.append("")
        output.append("DETAILED RECOMMENDATIONS:")
        output.append("-" * 40)
        
        for i, rec in enumerate(recommendations, 1):
            output.append(f"\n{i}. {rec.type.upper()} - {rec.priority} Priority")
            output.append(f"   Description: {rec.description}")
            output.append(f"   Target Classes: {', '.join(rec.target_classes)}")
            output.append(f"   Benefits:")
            for benefit in rec.benefits:
                output.append(f"     • {benefit}")
            output.append(f"   Implementation Steps:")
            for step in rec.implementation_steps:
                output.append(f"     • {step}")
            output.append(f"   Estimated Effort: {rec.estimated_effort}")
        
        # Implementation Priority
        output.append("")
        output.append("IMPLEMENTATION PRIORITY:")
        output.append("-" * 40)
        output.append("1. CRITICAL - Address immediately")
        output.append("2. HIGH - Address within current sprint")
        output.append("3. MEDIUM - Plan for next sprint")
        output.append("4. LOW - Consider for future iterations")
        
        return "\n".join(output)


class ClassHierarchyRefactoringEngine:
    """Main engine for class hierarchy refactoring"""
    
    def __init__(self):
        self.analyzer = ClassHierarchyAnalyzer()
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for refactoring engine"""
        logger = logging.getLogger("ClassHierarchyRefactoringEngine")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def refactor_class_hierarchy(self, target_directory: str) -> str:
        """Main method to refactor class hierarchies in a directory"""
        self.logger.info(f"Starting class hierarchy refactoring in: {target_directory}")
        
        # Find Python files
        python_files = list(Path(target_directory).rglob("*.py"))
        self.logger.info(f"Found {len(python_files)} Python files to analyze")
        
        # Analyze all files
        all_classes = []
        for file_path in python_files:
            classes = self.analyzer.analyze_file(str(file_path))
            all_classes.extend(classes)
        
        # Build hierarchy graph
        hierarchy_graph = self.analyzer.build_hierarchy_graph()
        
        # Identify refactoring opportunities
        recommendations = self.analyzer.identify_refactoring_opportunities()
        
        # Generate refactoring plan
        refactoring_plan = self.analyzer.generate_refactoring_plan(recommendations)
        
        self.logger.info(f"Class hierarchy analysis complete. Found {len(recommendations)} refactoring opportunities")
        
        return refactoring_plan


def main():
    """Main entry point for class hierarchy refactoring"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Class Hierarchy Refactoring - MODULAR-002 Mission",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python class_hierarchy_refactoring.py --target agent_workspaces/Agent-7
  python class_hierarchy_refactoring.py --target . --output plan.txt
  python class_hierarchy_refactoring.py --help
        """
    )
    
    parser.add_argument(
        "--target", "-t",
        default=".",
        help="Target directory to analyze (default: current directory)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file for the refactoring plan"
    )
    
    args = parser.parse_args()
    
    # Initialize refactoring engine
    refactoring_engine = ClassHierarchyRefactoringEngine()
    
    # Generate refactoring plan
    try:
        plan = refactoring_engine.refactor_class_hierarchy(args.target)
        
        # Save to file if specified
        if args.output:
            try:
                with open(args.output, 'w') as f:
                    f.write(plan)
                print(f"Refactoring plan saved to: {args.output}")
            except Exception as e:
                print(f"Error saving plan: {e}")
        
        print(plan)
    except Exception as e:
        print(f"Error generating refactoring plan: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
