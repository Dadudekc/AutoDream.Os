#!/usr/bin/env python3
"""
CLI Refactoring Utils - Agent Cellphone V2
=========================================

Utility functions for CLI modular refactoring validation.
Extracted from cli_modular_refactoring_validator.py for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import re
import os
import ast
from typing import Dict, Any, List, Optional, Tuple, Set
from .models.cli_refactoring_models import (
    CLIRefactoringPattern, CLIModuleProfile, CLIRefactoringResult,
    CLIRefactoringThresholds, CLIPatternIndicators
)

class CLIRefactoringUtils:
    """Utility functions for CLI refactoring validation."""
    
    def __init__(self):
        """Initialize CLI refactoring utilities."""
        self.thresholds = CLIRefactoringThresholds()
        self.pattern_indicators = CLIPatternIndicators()
    
    def analyze_file_structure(self, file_path: str) -> Dict[str, Any]:
        """Analyze file structure for refactoring opportunities."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Parse AST
            tree = ast.parse(content)
            
            # Analyze structure
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
            
            return {
                "total_lines": len(lines),
                "classes": classes,
                "functions": functions,
                "imports": imports,
                "complexity_score": self._calculate_complexity_score(tree),
                "refactoring_opportunities": self._identify_refactoring_opportunities(tree, lines)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_complexity_score(self, tree: ast.AST) -> int:
        """Calculate complexity score for the AST."""
        complexity = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(node, ast.FunctionDef):
                complexity += len([n for n in ast.walk(node) if isinstance(n, (ast.If, ast.While, ast.For))])
        
        return complexity
    
    def _identify_refactoring_opportunities(self, tree: ast.AST, lines: List[str]) -> List[Dict[str, Any]]:
        """Identify refactoring opportunities in the code."""
        opportunities = []
        
        # Check for large functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 20:  # Large function
                    opportunities.append({
                        "type": "large_function",
                        "name": node.name,
                        "lines": len(node.body),
                        "recommendation": "Extract into smaller functions"
                    })
        
        # Check for large classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if len(node.body) > 15:  # Large class
                    opportunities.append({
                        "type": "large_class",
                        "name": node.name,
                        "lines": len(node.body),
                        "recommendation": "Extract into separate modules"
                    })
        
        return opportunities
    
    def detect_refactoring_patterns(self, file_path: str) -> List[CLIRefactoringPattern]:
        """Detect refactoring patterns in the file."""
        patterns = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for component extraction patterns
            if any(keyword in content for keyword in self.pattern_indicators.component_keywords):
                patterns.append(CLIRefactoringPattern.COMPONENT_EXTRACTION)
            
            # Check for factory patterns
            if any(keyword in content for keyword in self.pattern_indicators.factory_keywords):
                patterns.append(CLIRefactoringPattern.FACTORY_PATTERN)
            
            # Check for service layer patterns
            if any(keyword in content for keyword in self.pattern_indicators.service_keywords):
                patterns.append(CLIRefactoringPattern.SERVICE_LAYER)
            
            # Check for dependency injection patterns
            if any(keyword in content for keyword in self.pattern_indicators.dependency_keywords):
                patterns.append(CLIRefactoringPattern.DEPENDENCY_INJECTION)
            
            # Check for modular refactoring patterns
            if any(keyword in content for keyword in self.pattern_indicators.modular_keywords):
                patterns.append(CLIRefactoringPattern.MODULAR_REFACTORING)
            
        except Exception as e:
            pass
        
        return patterns
    
    def calculate_refactoring_score(self, file_path: str, patterns: List[CLIRefactoringPattern]) -> float:
        """Calculate refactoring score based on patterns and file structure."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            
            # Base score from line count
            if lines <= self.thresholds.max_file_lines:
                base_score = 100.0
            else:
                base_score = max(0, 100 - (lines - self.thresholds.max_file_lines) * 2)
            
            # Pattern bonus
            pattern_bonus = len(patterns) * 10
            
            # Complexity penalty
            structure = self.analyze_file_structure(file_path)
            complexity_penalty = min(20, structure.get("complexity_score", 0) * 2)
            
            final_score = base_score + pattern_bonus - complexity_penalty
            return max(0, min(100, final_score))
            
        except Exception:
            return 0.0
    
    def generate_refactoring_recommendations(self, file_path: str, patterns: List[CLIRefactoringPattern]) -> List[str]:
        """Generate refactoring recommendations based on analysis."""
        recommendations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            
            if lines > self.thresholds.max_file_lines:
                recommendations.append(f"Reduce file size from {lines} to {self.thresholds.max_file_lines} lines")
            
            if CLIRefactoringPattern.COMPONENT_EXTRACTION not in patterns:
                recommendations.append("Implement component extraction pattern")
            
            if CLIRefactoringPattern.FACTORY_PATTERN not in patterns:
                recommendations.append("Implement factory pattern for object creation")
            
            if CLIRefactoringPattern.SERVICE_LAYER not in patterns:
                recommendations.append("Implement service layer separation")
            
            if CLIRefactoringPattern.DEPENDENCY_INJECTION not in patterns:
                recommendations.append("Implement dependency injection pattern")
            
            if CLIRefactoringPattern.MODULAR_REFACTORING not in patterns:
                recommendations.append("Implement modular refactoring approach")
            
        except Exception as e:
            recommendations.append(f"Error analyzing file: {str(e)}")
        
        return recommendations
    
    def estimate_refactoring_effort(self, file_path: str, patterns: List[CLIRefactoringPattern]) -> int:
        """Estimate refactoring effort in cycles."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            
            # Base effort from file size
            if lines <= 200:
                base_effort = 1
            elif lines <= 400:
                base_effort = 2
            elif lines <= 600:
                base_effort = 3
            else:
                base_effort = 4
            
            # Pattern complexity adjustment
            pattern_effort = len(patterns) * 0.5
            
            return int(base_effort + pattern_effort)
            
        except Exception:
            return 1
