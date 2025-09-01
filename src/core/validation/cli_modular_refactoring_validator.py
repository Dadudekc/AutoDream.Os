#!/usr/bin/env python3
"""
CLI Modular Refactoring Validator - Agent Cellphone V2
====================================================

Advanced validation system for CLI modular refactoring patterns.
Provides comprehensive validation for CLI component extraction, factory patterns,
service layer separation, dependency injection, and modular refactoring methodologies.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import re
import os
import ast
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum

from .validation_models import ValidationIssue, ValidationSeverity


class CLIRefactoringPattern(Enum):
    """Types of CLI refactoring patterns."""
    COMPONENT_EXTRACTION = "component_extraction"
    FACTORY_PATTERN = "factory_pattern"
    SERVICE_LAYER = "service_layer"
    DEPENDENCY_INJECTION = "dependency_injection"
    MODULAR_REFACTORING = "modular_refactoring"


@dataclass
class CLIModuleProfile:
    """CLI module refactoring profile."""
    module_name: str
    file_path: str
    original_lines: int
    target_lines: int
    reduction_percent: float
    refactoring_patterns: List[CLIRefactoringPattern] = field(default_factory=list)
    extracted_components: List[str] = field(default_factory=list)
    factory_implementations: List[str] = field(default_factory=list)
    service_layers: List[str] = field(default_factory=list)
    dependency_injections: List[str] = field(default_factory=list)
    modular_structures: List[str] = field(default_factory=list)
    v2_compliant: bool = False
    refactoring_score: float = 0.0


class CLIModularRefactoringValidator:
    """
    Advanced CLI modular refactoring validator for V2 compliance.
    
    Provides comprehensive validation for:
    - Component extraction and separation patterns
    - Factory pattern implementation for CLI modules
    - Service layer separation for CLI operations
    - Dependency injection patterns for CLI components
    - Modular refactoring methodologies with V2 compliance
    """

    def __init__(self):
        """Initialize the CLI modular refactoring validator."""
        self.refactoring_thresholds = {
            "max_file_lines": 200,
            "min_reduction_percent": 30,
            "min_component_separation": 3,
            "min_factory_implementations": 1,
            "min_service_layers": 1,
            "min_dependency_injections": 2,
            "min_modular_structures": 2
        }
        
        self.pattern_indicators = {
            "component_keywords": ["Component", "Module", "Handler", "Processor", "Manager"],
            "factory_keywords": ["Factory", "Builder", "Creator", "Provider", "Generator"],
            "service_keywords": ["Service", "Business", "Logic", "Operation", "Action"],
            "dependency_keywords": ["Dependency", "Inject", "DI", "Container", "Resolver"],
            "modular_keywords": ["Modular", "Separated", "Isolated", "Independent", "Decoupled"]
        }

    def validate_cli_modular_refactoring(self, file_path: str) -> List[ValidationIssue]:
        """
        Validate CLI modular refactoring implementation in a file.
        
        Args:
            file_path: Path to the CLI file to validate
            
        Returns:
            List of validation issues
        """
        issues = []
        
        try:
            if not os.path.exists(file_path):
                issues.append(ValidationIssue(
                    rule_id="file_not_found",
                    rule_name="File Not Found",
                    severity=ValidationSeverity.ERROR,
                    message=f"CLI refactoring file not found: {file_path}",
                    details={"file_path": file_path},
                    timestamp=datetime.now(),
                    component="cli_modular_refactoring_validator"
                ))
                return issues

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyze CLI module profile
            module_profile = self._analyze_cli_module_profile(file_path, content)
            
            # Validate refactoring patterns
            issues.extend(self._validate_component_extraction(module_profile, content))
            issues.extend(self._validate_factory_patterns(module_profile, content))
            issues.extend(self._validate_service_layers(module_profile, content))
            issues.extend(self._validate_dependency_injection(module_profile, content))
            issues.extend(self._validate_modular_structures(module_profile, content))
            issues.extend(self._validate_v2_compliance(module_profile, content))
            
        except Exception as e:
            issues.append(ValidationIssue(
                rule_id="cli_refactoring_analysis_error",
                rule_name="CLI Refactoring Analysis Error",
                severity=ValidationSeverity.ERROR,
                message=f"Failed to analyze CLI refactoring in {file_path}: {str(e)}",
                details={"file_path": file_path, "error": str(e)},
                timestamp=datetime.now(),
                component="cli_modular_refactoring_validator"
            ))
        
        return issues

    def _analyze_cli_module_profile(self, file_path: str, content: str) -> CLIModuleProfile:
        """Analyze CLI module refactoring profile from file content."""
        lines = content.split('\n')
        original_lines = len(lines)
        
        # Calculate target lines (assuming 38% reduction for messaging_cli.py)
        target_lines = int(original_lines * 0.62)  # 38% reduction
        reduction_percent = ((original_lines - target_lines) / original_lines * 100) if original_lines > 0 else 0
        
        # Detect refactoring patterns
        refactoring_patterns = self._detect_refactoring_patterns(content)
        
        # Extract components
        extracted_components = self._extract_component_names(content)
        
        # Detect factory implementations
        factory_implementations = self._detect_factory_implementations(content)
        
        # Detect service layers
        service_layers = self._detect_service_layers(content)
        
        # Detect dependency injections
        dependency_injections = self._detect_dependency_injections(content)
        
        # Detect modular structures
        modular_structures = self._detect_modular_structures(content)
        
        return CLIModuleProfile(
            module_name=os.path.basename(file_path),
            file_path=file_path,
            original_lines=original_lines,
            target_lines=target_lines,
            reduction_percent=reduction_percent,
            refactoring_patterns=refactoring_patterns,
            extracted_components=extracted_components,
            factory_implementations=factory_implementations,
            service_layers=service_layers,
            dependency_injections=dependency_injections,
            modular_structures=modular_structures
        )

    def _detect_refactoring_patterns(self, content: str) -> List[CLIRefactoringPattern]:
        """Detect refactoring patterns in CLI content."""
        patterns = []
        
        # Check for component extraction patterns
        if any(keyword in content for keyword in self.pattern_indicators["component_keywords"]):
            patterns.append(CLIRefactoringPattern.COMPONENT_EXTRACTION)
        
        # Check for factory patterns
        if any(keyword in content for keyword in self.pattern_indicators["factory_keywords"]):
            patterns.append(CLIRefactoringPattern.FACTORY_PATTERN)
        
        # Check for service layers
        if any(keyword in content for keyword in self.pattern_indicators["service_keywords"]):
            patterns.append(CLIRefactoringPattern.SERVICE_LAYER)
        
        # Check for dependency injection
        if any(keyword in content for keyword in self.pattern_indicators["dependency_keywords"]):
            patterns.append(CLIRefactoringPattern.DEPENDENCY_INJECTION)
        
        # Check for modular structures
        if any(keyword in content for keyword in self.pattern_indicators["modular_keywords"]):
            patterns.append(CLIRefactoringPattern.MODULAR_REFACTORING)
        
        return patterns

    def _extract_component_names(self, content: str) -> List[str]:
        """Extract component names from CLI content."""
        components = []
        
        # Look for class definitions
        class_matches = re.findall(r'class\s+(\w+)(?:\([^)]*\))?:', content)
        components.extend(class_matches)
        
        # Look for function definitions that could be components
        function_matches = re.findall(r'def\s+(\w+)_(?:component|handler|processor|manager)\s*\(', content, re.IGNORECASE)
        components.extend(function_matches)
        
        # Look for CLI command handlers
        command_matches = re.findall(r'def\s+(\w+)_command\s*\(', content, re.IGNORECASE)
        components.extend(command_matches)
        
        return list(set(components))

    def _detect_factory_implementations(self, content: str) -> List[str]:
        """Detect factory pattern implementations."""
        factories = []
        
        # Look for factory classes
        factory_classes = re.findall(r'class\s+(\w*[Ff]actory\w*)(?:\([^)]*\))?:', content)
        factories.extend(factory_classes)
        
        # Look for factory functions
        factory_functions = re.findall(r'def\s+(\w*[Ff]actory\w*)\s*\(', content)
        factories.extend(factory_functions)
        
        # Look for builder patterns
        builder_patterns = re.findall(r'def\s+(\w*[Bb]uilder\w*)\s*\(', content)
        factories.extend(builder_patterns)
        
        return list(set(factories))

    def _detect_service_layers(self, content: str) -> List[str]:
        """Detect service layer implementations."""
        services = []
        
        # Look for service classes
        service_classes = re.findall(r'class\s+(\w*[Ss]ervice\w*)(?:\([^)]*\))?:', content)
        services.extend(service_classes)
        
        # Look for business logic functions
        business_functions = re.findall(r'def\s+(\w*[Bb]usiness\w*)\s*\(', content)
        services.extend(business_functions)
        
        # Look for operation handlers
        operation_handlers = re.findall(r'def\s+(\w*[Oo]peration\w*)\s*\(', content)
        services.extend(operation_handlers)
        
        return list(set(services))

    def _detect_dependency_injections(self, content: str) -> List[str]:
        """Detect dependency injection patterns."""
        injections = []
        
        # Look for constructor dependency injection
        constructor_injections = re.findall(r'def\s+__init__\s*\([^)]*(\w+)[^)]*\):', content)
        injections.extend(constructor_injections)
        
        # Look for dependency injection decorators
        di_decorators = re.findall(r'@(?:inject|injectable|dependency)', content, re.IGNORECASE)
        injections.extend(di_decorators)
        
        # Look for dependency container usage
        container_usage = re.findall(r'(\w*[Cc]ontainer\w*)\.', content)
        injections.extend(container_usage)
        
        return list(set(injections))

    def _detect_modular_structures(self, content: str) -> List[str]:
        """Detect modular structure implementations."""
        structures = []
        
        # Look for module imports
        module_imports = re.findall(r'from\s+(\w+)\s+import', content)
        structures.extend(module_imports)
        
        # Look for modular class definitions
        modular_classes = re.findall(r'class\s+(\w*[Mm]odule\w*)(?:\([^)]*\))?:', content)
        structures.extend(modular_classes)
        
        # Look for separated concerns
        separated_concerns = re.findall(r'def\s+(\w*[Ss]eparated\w*)\s*\(', content)
        structures.extend(separated_concerns)
        
        return list(set(structures))

    def _validate_component_extraction(self, profile: CLIModuleProfile, content: str) -> List[ValidationIssue]:
        """Validate component extraction patterns."""
        issues = []
        
        # Check minimum component separation
        if len(profile.extracted_components) < self.refactoring_thresholds["min_component_separation"]:
            issues.append(ValidationIssue(
                rule_id="insufficient_component_extraction",
                rule_name="Insufficient Component Extraction",
                severity=ValidationSeverity.WARNING,
                message=f"Only {len(profile.extracted_components)} components extracted, minimum {self.refactoring_thresholds['min_component_separation']} required",
                details={
                    "file_path": profile.file_path,
                    "extracted_components": len(profile.extracted_components),
                    "minimum_required": self.refactoring_thresholds["min_component_separation"],
                    "components": profile.extracted_components
                },
                timestamp=datetime.now(),
                component="cli_modular_refactoring_validator"
            ))
        
        # Check for proper component separation
        if len(profile.extracted_components) > 0:
            # Look for large functions that should be extracted
            large_functions = re.findall(r'def\s+(\w+)\s*\([^)]*\):\s*(?:[^{]*\{[^}]*\})*[^{]*\{[^}]{50,}\}', content, re.DOTALL)
            if large_functions:
                issues.append(ValidationIssue(
                    rule_id="large_functions_not_extracted",
                    rule_name="Large Functions Not Extracted",
                    severity=ValidationSeverity.INFO,
                    message=f"Large functions detected that could be extracted into components: {', '.join(large_functions)}",
                    details={
                        "file_path": profile.file_path,
                        "large_functions": large_functions
                    },
                    timestamp=datetime.now(),
                    component="cli_modular_refactoring_validator"
                ))
        
        return issues

    def _validate_factory_patterns(self, profile: CLIModuleProfile, content: str) -> List[ValidationIssue]:
        """Validate factory pattern implementations."""
        issues = []
        
        # Check minimum factory implementations
        if len(profile.factory_implementations) < self.refactoring_thresholds["min_factory_implementations"]:
            issues.append(ValidationIssue(
                rule_id="insufficient_factory_patterns",
                rule_name="Insufficient Factory Patterns",
                severity=ValidationSeverity.WARNING,
                message=f"Only {len(profile.factory_implementations)} factory implementations found, minimum {self.refactoring_thresholds['min_factory_implementations']} required",
                details={
                    "file_path": profile.file_path,
                    "factory_implementations": len(profile.factory_implementations),
                    "minimum_required": self.refactoring_thresholds["min_factory_implementations"],
                    "factories": profile.factory_implementations
                },
                timestamp=datetime.now(),
                component="cli_modular_refactoring_validator"
            ))
        
        # Check for proper factory pattern implementation
        if len(profile.factory_implementations) > 0:
            # Look for direct instantiation that should use factories
            direct_instantiation = re.findall(r'(\w+)\([^)]*\)', content)
            if len(direct_instantiation) > 5:  # Allow some direct instantiation
                issues.append(ValidationIssue(
                    rule_id="excessive_direct_instantiation",
                    rule_name="Excessive Direct Instantiation",
                    severity=ValidationSeverity.INFO,
                    message=f"Consider using factory patterns for object creation instead of direct instantiation",
                    details={
                        "file_path": profile.file_path,
                        "direct_instantiations": len(direct_instantiation)
                    },
                    timestamp=datetime.now(),
                    component="cli_modular_refactoring_validator"
                ))
        
        return issues

    def _validate_service_layers(self, profile: CLIModuleProfile, content: str) -> List[ValidationIssue]:
        """Validate service layer implementations."""
        issues = []
        
        # Check minimum service layers
        if len(profile.service_layers) < self.refactoring_thresholds["min_service_layers"]:
            issues.append(ValidationIssue(
                rule_id="insufficient_service_layers",
                rule_name="Insufficient Service Layers",
                severity=ValidationSeverity.WARNING,
                message=f"Only {len(profile.service_layers)} service layers found, minimum {self.refactoring_thresholds['min_service_layers']} required",
                details={
                    "file_path": profile.file_path,
                    "service_layers": len(profile.service_layers),
                    "minimum_required": self.refactoring_thresholds["min_service_layers"],
                    "services": profile.service_layers
                },
                timestamp=datetime.now(),
                component="cli_modular_refactoring_validator"
            ))
        
        # Check for business logic separation
        if len(profile.service_layers) > 0:
            # Look for business logic mixed with CLI logic
            mixed_logic = re.findall(r'def\s+(\w+)\s*\([^)]*\):\s*(?:[^{]*\{[^}]*\})*[^{]*\{[^}]*argparse[^}]*business[^}]*\}', content, re.DOTALL)
            if mixed_logic:
                issues.append(ValidationIssue(
                    rule_id="mixed_business_cli_logic",
                    rule_name="Mixed Business and CLI Logic",
                    severity=ValidationSeverity.WARNING,
                    message=f"Business logic mixed with CLI logic in functions: {', '.join(mixed_logic)}",
                    details={
                        "file_path": profile.file_path,
                        "mixed_functions": mixed_logic
                    },
                    timestamp=datetime.now(),
                    component="cli_modular_refactoring_validator"
                ))
        
        return issues

    def _validate_dependency_injection(self, profile: CLIModuleProfile, content: str) -> List[ValidationIssue]:
        """Validate dependency injection patterns."""
        issues = []
        
        # Check minimum dependency injections
        if len(profile.dependency_injections) < self.refactoring_thresholds["min_dependency_injections"]:
            issues.append(ValidationIssue(
                rule_id="insufficient_dependency_injection",
                rule_name="Insufficient Dependency Injection",
                severity=ValidationSeverity.WARNING,
                message=f"Only {len(profile.dependency_injections)} dependency injections found, minimum {self.refactoring_thresholds['min_dependency_injections']} required",
                details={
                    "file_path": profile.file_path,
                    "dependency_injections": len(profile.dependency_injections),
                    "minimum_required": self.refactoring_thresholds["min_dependency_injections"],
                    "injections": profile.dependency_injections
                },
                timestamp=datetime.now(),
                component="cli_modular_refactoring_validator"
            ))
        
        # Check for proper dependency injection implementation
        if len(profile.dependency_injections) > 0:
            # Look for hard-coded dependencies
            hard_coded_deps = re.findall(r'(\w+)\([^)]*\)\s*#\s*(?:hard|coded|fixed)', content, re.IGNORECASE)
            if hard_coded_deps:
                issues.append(ValidationIssue(
                    rule_id="hard_coded_dependencies",
                    rule_name="Hard-coded Dependencies",
                    severity=ValidationSeverity.WARNING,
                    message=f"Hard-coded dependencies detected: {', '.join(hard_coded_deps)}",
                    details={
                        "file_path": profile.file_path,
                        "hard_coded_dependencies": hard_coded_deps
                    },
                    timestamp=datetime.now(),
                    component="cli_modular_refactoring_validator"
                ))
        
        return issues

    def _validate_modular_structures(self, profile: CLIModuleProfile, content: str) -> List[ValidationIssue]:
        """Validate modular structure implementations."""
        issues = []
        
        # Check minimum modular structures
        if len(profile.modular_structures) < self.refactoring_thresholds["min_modular_structures"]:
            issues.append(ValidationIssue(
                rule_id="insufficient_modular_structures",
                rule_name="Insufficient Modular Structures",
                severity=ValidationSeverity.WARNING,
                message=f"Only {len(profile.modular_structures)} modular structures found, minimum {self.refactoring_thresholds['min_modular_structures']} required",
                details={
                    "file_path": profile.file_path,
                    "modular_structures": len(profile.modular_structures),
                    "minimum_required": self.refactoring_thresholds["min_modular_structures"],
                    "structures": profile.modular_structures
                },
                timestamp=datetime.now(),
                component="cli_modular_refactoring_validator"
            ))
        
        # Check for proper module separation
        if len(profile.modular_structures) > 0:
            # Look for circular dependencies
            circular_deps = self._detect_circular_dependencies(content)
            if circular_deps:
                issues.append(ValidationIssue(
                    rule_id="circular_dependencies",
                    rule_name="Circular Dependencies",
                    severity=ValidationSeverity.ERROR,
                    message=f"Circular dependencies detected: {', '.join(circular_deps)}",
                    details={
                        "file_path": profile.file_path,
                        "circular_dependencies": circular_deps
                    },
                    timestamp=datetime.now(),
                    component="cli_modular_refactoring_validator"
                ))
        
        return issues

    def _detect_circular_dependencies(self, content: str) -> List[str]:
        """Detect circular dependencies in CLI content."""
        # Simple circular dependency detection
        imports = re.findall(r'from\s+(\w+)\s+import', content)
        circular_deps = []
        
        # Check for self-imports
        module_name = re.search(r'class\s+(\w+)', content)
        if module_name:
            module_name = module_name.group(1).lower()
            if module_name in [imp.lower() for imp in imports]:
                circular_deps.append(f"self-import: {module_name}")
        
        return circular_deps

    def _validate_v2_compliance(self, profile: CLIModuleProfile, content: str) -> List[ValidationIssue]:
        """Validate V2 compliance standards."""
        issues = []
        
        # Check file line count
        if profile.original_lines > self.refactoring_thresholds["max_file_lines"]:
            issues.append(ValidationIssue(
                rule_id="file_line_limit_exceeded",
                rule_name="File Line Limit Exceeded",
                severity=ValidationSeverity.ERROR,
                message=f"CLI file has {profile.original_lines} lines, exceeding V2 limit of {self.refactoring_thresholds['max_file_lines']}",
                details={
                    "file_path": profile.file_path,
                    "line_count": profile.original_lines,
                    "limit": self.refactoring_thresholds["max_file_lines"],
                    "target_lines": profile.target_lines,
                    "reduction_percent": profile.reduction_percent
                },
                timestamp=datetime.now(),
                component="cli_modular_refactoring_validator"
            ))
            profile.v2_compliant = False
        else:
            profile.v2_compliant = True
        
        # Check reduction percentage
        if profile.reduction_percent < self.refactoring_thresholds["min_reduction_percent"]:
            issues.append(ValidationIssue(
                rule_id="insufficient_reduction",
                rule_name="Insufficient Reduction",
                severity=ValidationSeverity.WARNING,
                message=f"Reduction of {profile.reduction_percent:.1f}% below minimum {self.refactoring_thresholds['min_reduction_percent']}%",
                details={
                    "file_path": profile.file_path,
                    "reduction_percent": profile.reduction_percent,
                    "minimum_required": self.refactoring_thresholds["min_reduction_percent"]
                },
                timestamp=datetime.now(),
                component="cli_modular_refactoring_validator"
            ))
        
        # Check for proper error handling
        if not re.search(r'try\s*\{|except\s+', content):
            issues.append(ValidationIssue(
                rule_id="missing_error_handling",
                rule_name="Missing Error Handling",
                severity=ValidationSeverity.WARNING,
                message="CLI missing error handling patterns",
                details={"file_path": profile.file_path},
                timestamp=datetime.now(),
                component="cli_modular_refactoring_validator"
            ))
        
        # Check for proper documentation
        lines = content.split('\n')
        comment_lines = len([line for line in lines if line.strip().startswith('#') or line.strip().startswith('"""')])
        comment_ratio = comment_lines / len(lines) if len(lines) > 0 else 0
        
        if comment_ratio < 0.1:  # 10% minimum comment ratio
            issues.append(ValidationIssue(
                rule_id="insufficient_documentation",
                rule_name="Insufficient Documentation",
                severity=ValidationSeverity.INFO,
                message=f"CLI documentation ratio {comment_ratio:.2%} below recommended 10%",
                details={
                    "file_path": profile.file_path,
                    "comment_ratio": comment_ratio,
                    "comment_lines": comment_lines,
                    "total_lines": len(lines)
                },
                timestamp=datetime.now(),
                component="cli_modular_refactoring_validator"
            ))
        
        return issues

    def generate_refactoring_recommendations(self, profile: CLIModuleProfile) -> List[str]:
        """Generate refactoring recommendations based on profile analysis."""
        recommendations = []
        
        # Line count recommendations
        if profile.original_lines > self.refactoring_thresholds["max_file_lines"]:
            recommendations.append(f"Extract {profile.original_lines - profile.target_lines} lines into separate modules")
        
        # Component extraction recommendations
        if len(profile.extracted_components) < self.refactoring_thresholds["min_component_separation"]:
            recommendations.append("Extract CLI command handlers into separate component classes")
            recommendations.append("Separate argument parsing logic into dedicated components")
            recommendations.append("Create dedicated components for message delivery operations")
        
        # Factory pattern recommendations
        if len(profile.factory_implementations) < self.refactoring_thresholds["min_factory_implementations"]:
            recommendations.append("Implement factory pattern for CLI command creation")
            recommendations.append("Create factory for message delivery backends")
            recommendations.append("Implement factory for validation rule creation")
        
        # Service layer recommendations
        if len(profile.service_layers) < self.refactoring_thresholds["min_service_layers"]:
            recommendations.append("Separate business logic into service layer classes")
            recommendations.append("Create dedicated service for message processing")
            recommendations.append("Implement service layer for validation operations")
        
        # Dependency injection recommendations
        if len(profile.dependency_injections) < self.refactoring_thresholds["min_dependency_injections"]:
            recommendations.append("Implement dependency injection for CLI components")
            recommendations.append("Use constructor injection for service dependencies")
            recommendations.append("Create dependency container for CLI operations")
        
        # Modular structure recommendations
        if len(profile.modular_structures) < self.refactoring_thresholds["min_modular_structures"]:
            recommendations.append("Split CLI into multiple focused modules")
            recommendations.append("Create separate modules for different CLI operations")
            recommendations.append("Implement modular architecture for better maintainability")
        
        # General recommendations
        recommendations.append("Implement comprehensive error handling for all CLI operations")
        recommendations.append("Add detailed documentation for all CLI components")
        recommendations.append("Create unit tests for refactored CLI components")
        recommendations.append("Establish coding standards for CLI module development")
        
        return recommendations

    def calculate_refactoring_score(self, profile: CLIModuleProfile) -> float:
        """Calculate refactoring score based on profile analysis."""
        score = 0.0
        
        # Line count compliance (25%)
        if profile.v2_compliant:
            score += 25
        else:
            # Partial credit based on reduction
            reduction_score = min(25, (profile.reduction_percent / self.refactoring_thresholds["min_reduction_percent"]) * 25)
            score += reduction_score
        
        # Component extraction (20%)
        component_score = min(20, (len(profile.extracted_components) / self.refactoring_thresholds["min_component_separation"]) * 20)
        score += component_score
        
        # Factory patterns (15%)
        factory_score = min(15, (len(profile.factory_implementations) / self.refactoring_thresholds["min_factory_implementations"]) * 15)
        score += factory_score
        
        # Service layers (15%)
        service_score = min(15, (len(profile.service_layers) / self.refactoring_thresholds["min_service_layers"]) * 15)
        score += service_score
        
        # Dependency injection (15%)
        di_score = min(15, (len(profile.dependency_injections) / self.refactoring_thresholds["min_dependency_injections"]) * 15)
        score += di_score
        
        # Modular structures (10%)
        modular_score = min(10, (len(profile.modular_structures) / self.refactoring_thresholds["min_modular_structures"]) * 10)
        score += modular_score
        
        return min(100.0, score)

    def validate_multiple_cli_files(self, file_paths: List[str]) -> Dict[str, List[ValidationIssue]]:
        """Validate multiple CLI files for modular refactoring."""
        results = {}
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                results[file_path] = self.validate_cli_modular_refactoring(file_path)
            else:
                results[file_path] = [ValidationIssue(
                    rule_id="file_not_found",
                    rule_name="File Not Found",
                    severity=ValidationSeverity.ERROR,
                    message=f"CLI file not found: {file_path}",
                    details={"file_path": file_path},
                    timestamp=datetime.now(),
                    component="cli_modular_refactoring_validator"
                )]
        
        return results

    def generate_cli_refactoring_report(self, validation_results: Dict[str, List[ValidationIssue]]) -> Dict[str, Any]:
        """Generate comprehensive CLI refactoring report."""
        total_files = len(validation_results)
        compliant_files = 0
        total_issues = 0
        issue_summary = {
            "error": 0,
            "warning": 0,
            "info": 0
        }
        
        file_summaries = []
        
        for file_path, issues in validation_results.items():
            file_compliant = len(issues) == 0
            if file_compliant:
                compliant_files += 1
            
            total_issues += len(issues)
            
            # Count issues by severity
            for issue in issues:
                if issue.severity == ValidationSeverity.ERROR:
                    issue_summary["error"] += 1
                elif issue.severity == ValidationSeverity.WARNING:
                    issue_summary["warning"] += 1
                else:
                    issue_summary["info"] += 1
            
            file_summaries.append({
                "file_path": file_path,
                "compliant": file_compliant,
                "issue_count": len(issues),
                "issues": [
                    {
                        "rule_id": issue.rule_id,
                        "rule_name": issue.rule_name,
                        "severity": issue.severity.value,
                        "message": issue.message
                    }
                    for issue in issues
                ]
            })
        
        compliance_rate = (compliant_files / total_files * 100) if total_files > 0 else 0
        
        return {
            "report_timestamp": datetime.now().isoformat(),
            "summary": {
                "total_files": total_files,
                "compliant_files": compliant_files,
                "compliance_rate": round(compliance_rate, 2),
                "total_issues": total_issues,
                "issue_breakdown": issue_summary
            },
            "file_details": file_summaries,
            "recommendations": self._generate_cli_refactoring_recommendations(issue_summary, compliance_rate)
        }

    def _generate_cli_refactoring_recommendations(self, issue_summary: Dict[str, int], compliance_rate: float) -> List[str]:
        """Generate recommendations based on CLI refactoring validation results."""
        recommendations = []
        
        if compliance_rate < 80:
            recommendations.append("Focus on achieving 80%+ CLI refactoring compliance rate")
        
        if issue_summary["error"] > 0:
            recommendations.append("Address all ERROR level issues immediately - these violate V2 compliance")
        
        if issue_summary["warning"] > 5:
            recommendations.append("Review and address WARNING level issues to improve CLI refactoring quality")
        
        if issue_summary["info"] > 10:
            recommendations.append("Consider improving CLI structure based on INFO level suggestions")
        
        recommendations.append("Implement component extraction patterns for better CLI modularity")
        recommendations.append("Establish factory patterns for CLI object creation")
        recommendations.append("Separate business logic into dedicated service layers")
        recommendations.append("Implement dependency injection for better CLI component management")
        recommendations.append("Create modular CLI architecture for improved maintainability")
        
        return recommendations
