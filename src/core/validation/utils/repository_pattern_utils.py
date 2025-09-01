#!/usr/bin/env python3
"""
Repository Pattern Utils - Agent Cellphone V2
============================================

Utility functions for repository pattern validation.
Extracted from repository_pattern_validator.py for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import re
import os
import ast
from typing import Dict, Any, List, Optional, Tuple, Set
from .models.repository_pattern_models import (
    RepositoryPatternType, RepositoryPatternProfile, RepositoryPatternResult,
    RepositoryPatternConfig, RepositoryPatternThresholds
)

class RepositoryPatternUtils:
    """Utility functions for repository pattern validation."""
    
    def __init__(self):
        """Initialize repository pattern utilities."""
        self.config = RepositoryPatternConfig()
        self.thresholds = RepositoryPatternThresholds()
    
    def analyze_repository_pattern(self, file_path: str) -> RepositoryPatternProfile:
        """Analyze repository pattern implementation in a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Parse AST
            tree = ast.parse(content)
            
            # Analyze structure
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            
            # Detect interfaces
            interfaces = self._detect_interfaces(content, classes)
            
            # Detect repository methods
            repository_methods = self._detect_repository_methods(content, functions)
            
            # Determine pattern type
            pattern_type = self._determine_pattern_type(content, classes, interfaces)
            
            # Calculate scores
            pattern_score = self._calculate_pattern_score(content, classes, interfaces, repository_methods)
            implementation_quality = self._calculate_implementation_quality(content, classes, interfaces)
            separation_score = self._calculate_separation_score(content, classes, interfaces)
            
            # Check V2 compliance
            v2_compliant = len(lines) <= self.config.max_file_lines
            
            profile = RepositoryPatternProfile(
                file_path=file_path,
                pattern_type=pattern_type,
                classes_found=classes,
                interfaces_found=interfaces,
                methods_found=repository_methods,
                v2_compliant=v2_compliant,
                pattern_score=pattern_score,
                implementation_quality=implementation_quality,
                separation_score=separation_score
            )
            
            return profile
            
        except Exception as e:
            # Return default profile on error
            return RepositoryPatternProfile(
                file_path=file_path,
                pattern_type=RepositoryPatternType.GENERIC_REPOSITORY,
                classes_found=[],
                interfaces_found=[],
                methods_found=[],
                v2_compliant=False,
                pattern_score=0.0,
                implementation_quality=0.0,
                separation_score=0.0
            )
    
    def _detect_interfaces(self, content: str, classes: List[str]) -> List[str]:
        """Detect interface implementations."""
        interfaces = []
        
        # Look for interface-like classes
        for class_name in classes:
            if any(keyword in class_name for keyword in self.config.pattern_indicators["interface_keywords"]):
                interfaces.append(class_name)
        
        # Look for abstract classes
        if "abstract" in content.lower() or "ABC" in content:
            abstract_classes = re.findall(r'class\s+(\w+).*?ABC', content)
            interfaces.extend(abstract_classes)
        
        return list(set(interfaces))
    
    def _detect_repository_methods(self, content: str, functions: List[str]) -> List[str]:
        """Detect repository pattern methods."""
        repository_methods = []
        
        # Look for CRUD operations
        crud_patterns = [
            r'def\s+(get|find|retrieve)_\w+',
            r'def\s+(add|create|insert)_\w+',
            r'def\s+(update|modify|edit)_\w+',
            r'def\s+(delete|remove|destroy)_\w+',
            r'def\s+(save|persist)_\w+'
        ]
        
        for pattern in crud_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            repository_methods.extend(matches)
        
        # Look for specific repository methods
        for method in self.config.required_methods:
            if method.lower() in [f.lower() for f in functions]:
                repository_methods.append(method)
        
        return list(set(repository_methods))
    
    def _determine_pattern_type(self, content: str, classes: List[str], interfaces: List[str]) -> RepositoryPatternType:
        """Determine the type of repository pattern implemented."""
        content_lower = content.lower()
        
        # Check for CQRS pattern
        if any(keyword in content_lower for keyword in ["command", "query", "cqrs"]):
            return RepositoryPatternType.CQRS_PATTERN
        
        # Check for Unit of Work pattern
        if any(keyword in content_lower for keyword in ["unitofwork", "unit_of_work", "transaction"]):
            return RepositoryPatternType.UNIT_OF_WORK
        
        # Check for Specification pattern
        if any(keyword in content_lower for keyword in ["specification", "criteria", "predicate"]):
            return RepositoryPatternType.SPECIFICATION_PATTERN
        
        # Check for specific repository
        if any(keyword in content_lower for keyword in ["user", "product", "order", "customer"]):
            return RepositoryPatternType.SPECIFIC_REPOSITORY
        
        # Default to generic repository
        return RepositoryPatternType.GENERIC_REPOSITORY
    
    def _calculate_pattern_score(self, content: str, classes: List[str], 
                               interfaces: List[str], methods: List[str]) -> float:
        """Calculate repository pattern implementation score."""
        score = 0.0
        
        # Base score from interfaces
        if interfaces:
            score += min(30, len(interfaces) * 10)
        
        # Score from repository methods
        if methods:
            score += min(40, len(methods) * 8)
        
        # Score from classes
        if classes:
            score += min(20, len(classes) * 5)
        
        # Bonus for required interfaces
        required_interfaces_found = sum(1 for req in self.config.required_interfaces 
                                      if any(req.lower() in interface.lower() for interface in interfaces))
        score += min(10, required_interfaces_found * 5)
        
        return min(100, score)
    
    def _calculate_implementation_quality(self, content: str, classes: List[str], interfaces: List[str]) -> float:
        """Calculate implementation quality score."""
        quality = 0.0
        
        # Check for proper separation
        if interfaces and classes:
            quality += 30
        
        # Check for dependency injection
        if "inject" in content.lower() or "di" in content.lower():
            quality += 20
        
        # Check for proper naming conventions
        proper_naming = sum(1 for cls in classes if cls[0].isupper())
        quality += min(20, proper_naming * 5)
        
        # Check for documentation
        if '"""' in content or "'''" in content:
            quality += 15
        
        # Check for error handling
        if "try" in content.lower() and "except" in content.lower():
            quality += 15
        
        return min(100, quality)
    
    def _calculate_separation_score(self, content: str, classes: List[str], interfaces: List[str]) -> float:
        """Calculate separation of concerns score."""
        separation = 0.0
        
        # Check for interface separation
        if interfaces:
            separation += 40
        
        # Check for class separation
        if len(classes) > 1:
            separation += 30
        
        # Check for method separation
        methods = re.findall(r'def\s+\w+', content)
        if len(methods) > 5:
            separation += 20
        
        # Check for import separation
        imports = re.findall(r'^import\s+\w+', content, re.MULTILINE)
        if len(imports) > 3:
            separation += 10
        
        return min(100, separation)
    
    def generate_recommendations(self, profile: RepositoryPatternProfile) -> List[str]:
        """Generate recommendations for repository pattern improvement."""
        recommendations = []
        
        # V2 compliance recommendations
        if not profile.v2_compliant:
            recommendations.append("Reduce file size to meet V2 compliance standards")
        
        # Pattern score recommendations
        if profile.pattern_score < self.thresholds.acceptable_score:
            recommendations.append("Improve repository pattern implementation")
        
        # Implementation quality recommendations
        if profile.implementation_quality < self.thresholds.acceptable_quality:
            recommendations.append("Enhance implementation quality with proper separation")
        
        # Interface recommendations
        if not profile.interfaces_found:
            recommendations.append("Implement repository interfaces for better abstraction")
        
        # Method recommendations
        missing_methods = [method for method in self.config.required_methods 
                          if method.lower() not in [m.lower() for m in profile.methods_found]]
        if missing_methods:
            recommendations.append(f"Implement missing repository methods: {', '.join(missing_methods)}")
        
        # Separation recommendations
        if profile.separation_score < self.thresholds.acceptable_score:
            recommendations.append("Improve separation of concerns")
        
        return recommendations
    
    def estimate_refactoring_effort(self, profile: RepositoryPatternProfile) -> int:
        """Estimate refactoring effort in cycles."""
        effort = 1
        
        # Base effort from file size
        try:
            with open(profile.file_path, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            
            if lines > 400:
                effort += 2
            elif lines > 300:
                effort += 1
        except Exception:
            pass
        
        # Effort from pattern complexity
        if profile.pattern_type in [RepositoryPatternType.CQRS_PATTERN, RepositoryPatternType.UNIT_OF_WORK]:
            effort += 2
        elif profile.pattern_type == RepositoryPatternType.SPECIFICATION_PATTERN:
            effort += 1
        
        # Effort from missing components
        if not profile.interfaces_found:
            effort += 1
        
        missing_methods = len([method for method in self.config.required_methods 
                              if method.lower() not in [m.lower() for m in profile.methods_found]])
        effort += missing_methods // 2
        
        return min(5, effort)
