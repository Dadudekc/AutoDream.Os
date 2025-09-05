#!/usr/bin/env python3
"""
Utility Consolidation Engine - V2 Compliance Module
==================================================

Core business logic for utility function analysis and consolidation.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import os
import re
import ast
from typing import Dict, List, Set, Tuple
from difflib import SequenceMatcher

from .utility_consolidation_models import (
    ConsolidationType,
    UtilityFunction,
    ConsolidationOpportunity,
    ConsolidationResult,
    ConsolidationConfig,
)


class UtilityConsolidationEngine:
    """Core engine for utility function consolidation."""

    def __init__(self, config: ConsolidationConfig = None):
        """Initialize consolidation engine."""
        self.config = config or ConsolidationConfig()
        self.utility_functions: Dict[str, List[UtilityFunction]] = {}
        self.consolidation_opportunities: List[ConsolidationOpportunity] = []

    def analyze_codebase(self, source_directory: str) -> Dict[str, any]:
        """Analyze codebase for utility function consolidation opportunities."""
        self.utility_functions.clear()
        self.consolidation_opportunities.clear()

        # Scan all Python files
        for root, dirs, files in os.walk(source_directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self._analyze_file(file_path)

        # Identify consolidation opportunities
        self._identify_consolidation_opportunities()

        return self._generate_analysis_summary()

    def _analyze_file(self, file_path: str) -> None:
        """Analyze a single file for utility functions."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Find function definitions
            for i, line in enumerate(lines):
                if self._is_utility_function(line, content):
                    func_name = self._extract_function_name(line)
                    if func_name:
                        self._extract_function_metadata(
                            func_name, file_path, i, lines, content
                        )

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

    def _is_utility_function(self, line: str, content: str) -> bool:
        """Check if line contains a utility function definition."""
        # Check for function definition
        if not re.match(r'^\s*def\s+\w+', line):
            return False

        # Extract function name
        func_name = self._extract_function_name(line)
        if not func_name:
            return False

        # Check for utility indicators
        utility_indicators = [
            "util", "helper", "helper", "common", "shared",
            "format", "parse", "validate", "convert", "transform",
            "process", "clean", "normalize",
        ]

        func_lower = func_name.lower()
        if any(indicator in func_lower for indicator in utility_indicators):
            return True

        # Check for utility class patterns
        if re.search(r"class\s+\w*Util\w*", content):
            return True

        return False

    def _extract_function_name(self, line: str) -> str:
        """Extract function name from definition line."""
        match = re.match(r'^\s*def\s+(\w+)', line)
        return match.group(1) if match else None

    def _extract_function_metadata(
        self,
        func_name: str,
        file_path: str,
        line_index: int,
        lines: List[str],
        content: str,
    ) -> None:
        """Extract metadata for a utility function."""
        # Find function end
        end_line = self._find_function_end(lines, line_index)

        # Extract function content
        func_content = "\n".join(lines[line_index : end_line + 1])

        # Extract parameters
        params = self._extract_parameters(func_content)

        # Calculate complexity
        complexity = self._calculate_complexity(func_content)

        utility_func = UtilityFunction(
            name=func_name,
            file_path=file_path,
            line_start=line_index + 1,
            line_end=end_line + 1,
            content=func_content,
            parameters=params,
            complexity_score=complexity,
        )

        # Group by function name
        if func_name not in self.utility_functions:
            self.utility_functions[func_name] = []
        self.utility_functions[func_name].append(utility_func)

    def _find_function_end(self, lines: List[str], start_line: int) -> int:
        """Find the end line of a function."""
        indent_level = len(lines[start_line]) - len(lines[start_line].lstrip())
        
        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            if line.strip() == "":
                continue
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= indent_level:
                return i - 1
        
        return len(lines) - 1

    def _extract_parameters(self, func_content: str) -> List[str]:
        """Extract function parameters."""
        try:
            tree = ast.parse(func_content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    return [arg.arg for arg in node.args.args]
        except:
            pass
        return []

    def _calculate_complexity(self, func_content: str) -> int:
        """Calculate function complexity score."""
        complexity = 1  # Base complexity
        
        # Count control structures
        complexity += func_content.count('if ')
        complexity += func_content.count('for ')
        complexity += func_content.count('while ')
        complexity += func_content.count('try:')
        complexity += func_content.count('except')
        
        return complexity

    def _identify_consolidation_opportunities(self) -> None:
        """Identify consolidation opportunities."""
        for func_name, functions in self.utility_functions.items():
            if len(functions) > 1:
                # Group by similarity
                groups = self._group_similar_functions(functions)
                
                for group in groups:
                    if len(group) > 1:
                        primary = max(group, key=lambda f: f.complexity_score)
                        duplicates = [f for f in group if f != primary]
                        
                        opportunity = ConsolidationOpportunity(
                            consolidation_type=ConsolidationType.DUPLICATE_ELIMINATION,
                            primary_function=primary,
                            duplicate_functions=duplicates,
                            consolidation_strategy="Replace duplicates with primary function",
                            estimated_reduction=sum(len(f.content.split('\n')) for f in duplicates),
                            priority="HIGH" if len(duplicates) > 2 else "MEDIUM"
                        )
                        
                        self.consolidation_opportunities.append(opportunity)

    def _group_similar_functions(self, functions: List[UtilityFunction]) -> List[List[UtilityFunction]]:
        """Group functions by similarity."""
        groups = []
        used = set()
        
        for i, func1 in enumerate(functions):
            if i in used:
                continue
                
            group = [func1]
            used.add(i)
            
            for j, func2 in enumerate(functions[i+1:], i+1):
                if j in used:
                    continue
                    
                similarity = self._calculate_similarity(func1.content, func2.content)
                if similarity >= self.config.min_similarity_threshold:
                    group.append(func2)
                    used.add(j)
            
            groups.append(group)
        
        return groups

    def _calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two function contents."""
        return SequenceMatcher(None, content1, content2).ratio()

    def _generate_analysis_summary(self) -> Dict[str, any]:
        """Generate analysis summary."""
        total_functions = sum(len(funcs) for funcs in self.utility_functions.values())
        duplicate_functions = sum(len(funcs) - 1 for funcs in self.utility_functions.values() if len(funcs) > 1)
        total_reduction = sum(opp.estimated_reduction for opp in self.consolidation_opportunities)

        return {
            "utility_functions_found": total_functions,
            "duplicate_functions": duplicate_functions,
            "consolidation_opportunities": len(self.consolidation_opportunities),
            "estimated_reduction": total_reduction,
            "analysis_details": {
                "function_groups": len(self.utility_functions),
                "high_priority_opportunities": len([
                    opp for opp in self.consolidation_opportunities
                    if opp.priority == "HIGH"
                ]),
                "medium_priority_opportunities": len([
                    opp for opp in self.consolidation_opportunities
                    if opp.priority == "MEDIUM"
                ]),
                "low_priority_opportunities": len([
                    opp for opp in self.consolidation_opportunities
                    if opp.priority == "LOW"
                ]),
            },
        }
