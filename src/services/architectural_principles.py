"""
Architectural Principles Data - V2 Compliance Module
====================================================

Centralized data definitions for architectural principles following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from enum import Enum
from typing import Dict
from .architectural_models import ArchitecturalPrinciple, ArchitecturalGuidance


class PrincipleDefinitions:
    """Centralized definitions for all architectural principles."""

    @staticmethod
    def get_all_principles() -> Dict[ArchitecturalPrinciple, ArchitecturalGuidance]:
        """Get all architectural principle definitions."""
        return {
            ArchitecturalPrinciple.SINGLE_RESPONSIBILITY: ArchitecturalGuidance(
                principle=ArchitecturalPrinciple.SINGLE_RESPONSIBILITY,
                display_name="Single Responsibility Principle (SRP)",
                description="A class should have only one reason to change",
                responsibilities=[
                    "Ensure each class/module has single, well-defined purpose",
                    "Identify and eliminate classes with multiple responsibilities",
                    "Create focused, cohesive units of functionality",
                    "Maintain clear separation of concerns",
                ],
                guidelines=[
                    "Classes should have 1-3 public methods maximum",
                    "Methods should perform one specific task",
                    "Avoid 'God classes' that do everything",
                    "Use composition over inheritance for complex behaviors",
                ],
                examples=[
                    "Separate data access from business logic",
                    "Extract validation logic into dedicated classes",
                    "Create specific handlers for different message types",
                    "Isolate configuration from application logic",
                ],
                validation_rules=[
                    "No class should have more than 3 public methods",
                    "Methods should be under 30 lines",
                    "Classes should be under 200 lines",
                    "Circular dependencies must be eliminated",
                ],
            ),
            ArchitecturalPrinciple.OPEN_CLOSED: ArchitecturalGuidance(
                principle=ArchitecturalPrinciple.OPEN_CLOSED,
                display_name="Open-Closed Principle (OCP)",
                description="Software entities should be open for extension but closed for modification",
                responsibilities=[
                    "Design extensible systems without modifying existing code",
                    "Implement plugin architectures and extension points",
                    "Use abstraction to enable future enhancements",
                    "Create frameworks that support new features",
                ],
                guidelines=[
                    "Use abstract base classes for extension points",
                    "Implement strategy pattern for algorithm variations",
                    "Create configuration-driven behavior",
                    "Use dependency injection for flexibility",
                ],
                examples=[
                    "Message handlers that can be extended without modification",
                    "Plugin system for different delivery backends",
                    "Configurable validation rules",
                    "Extensible command pattern implementation",
                ],
                validation_rules=[
                    "New features should not require code changes",
                    "Extension points must be clearly defined",
                    "Configuration should drive behavior, not code",
                    "Abstract interfaces must be stable",
                ],
            ),
            ArchitecturalPrinciple.LISKOV_SUBSTITUTION: ArchitecturalGuidance(
                principle=ArchitecturalPrinciple.LISKOV_SUBSTITUTION,
                display_name="Liskov Substitution Principle (LSP)",
                description="Subtypes must be substitutable for their base types",
                responsibilities=[
                    "Ensure inheritance hierarchies maintain behavioral contracts",
                    "Validate that derived classes can replace base classes",
                    "Maintain consistent interfaces across inheritance",
                    "Prevent violation of expected behavior in subtypes",
                ],
                guidelines=[
                    "Derived classes must implement all base class methods",
                    "Method signatures must remain compatible",
                    "Preconditions cannot be strengthened in subtypes",
                    "Postconditions cannot be weakened in subtypes",
                ],
                examples=[
                    "Message types that can be used interchangeably",
                    "Handler implementations that maintain base contracts",
                    "Repository implementations with consistent interfaces",
                    "Service classes with substitutable behavior",
                ],
                validation_rules=[
                    "All inherited methods must be implemented",
                    "Method signatures must match base class",
                    "Behavioral contracts must be preserved",
                    "Subtypes must be usable wherever base types are expected",
                ],
            ),
            ArchitecturalPrinciple.INTERFACE_SEGREGATION: ArchitecturalGuidance(
                principle=ArchitecturalPrinciple.INTERFACE_SEGREGATION,
                display_name="Interface Segregation Principle (ISP)",
                description="Clients should not be forced to depend on interfaces they don't use",
                responsibilities=[
                    "Create small, specific interfaces for different clients",
                    "Avoid 'fat' interfaces that serve multiple purposes",
                    "Design interfaces that match client needs",
                    "Prevent coupling between unrelated functionality",
                ],
                guidelines=[
                    "One interface per responsibility",
                    "Separate read and write operations",
                    "Create role-specific interfaces",
                    "Use composition for complex interface requirements",
                ],
                examples=[
                    "Separate repository interfaces for different operations",
                    "Specific interfaces for different service consumers",
                    "Command and query separation",
                    "Plugin interfaces with minimal surface area",
                ],
                validation_rules=[
                    "Interfaces should have 3-5 methods maximum",
                    "No interface should force implementation of unused methods",
                    "Client classes should implement only relevant interfaces",
                    "Interface dependencies should be minimal",
                ],
            ),
            ArchitecturalPrinciple.DEPENDENCY_INVERSION: ArchitecturalGuidance(
                principle=ArchitecturalPrinciple.DEPENDENCY_INVERSION,
                display_name="Dependency Inversion Principle (DIP)",
                description="Depend on abstractions, not concretions",
                responsibilities=[
                    "Design systems that depend on abstractions",
                    "Create stable interfaces that don't change frequently",
                    "Use dependency injection to provide implementations",
                    "Invert the direction of dependencies",
                ],
                guidelines=[
                    "Program to interfaces, not implementations",
                    "Use constructor injection for dependencies",
                    "Create abstractions that don't depend on details",
                    "Make concrete classes depend on abstractions",
                ],
                examples=[
                    "Service classes that accept interface dependencies",
                    "Repository interfaces used by business logic",
                    "Plugin systems with abstract extension points",
                    "Configuration systems with abstract providers",
                ],
                validation_rules=[
                    "High-level modules should not depend on low-level modules",
                    "Both should depend on abstractions",
                    "Abstractions should not depend on details",
                    "Details should depend on abstractions",
                ],
            ),
            ArchitecturalPrinciple.SINGLE_SOURCE_OF_TRUTH: ArchitecturalGuidance(
                principle=ArchitecturalPrinciple.SINGLE_SOURCE_OF_TRUTH,
                display_name="Single Source of Truth (SSOT)",
                description="Each piece of data should have a single, authoritative source",
                responsibilities=[
                    "Identify authoritative sources for all data",
                    "Eliminate data duplication across the system",
                    "Create centralized configuration management",
                    "Maintain data consistency through single sources",
                ],
                guidelines=[
                    "Create centralized configuration files",
                    "Use environment variables for deployment-specific data",
                    "Implement configuration inheritance",
                    "Validate data integrity at single sources",
                ],
                examples=[
                    "Centralized agent configuration files",
                    "Single source for coordinate definitions",
                    "Unified logging configuration",
                    "Centralized validation rules",
                ],
                validation_rules=[
                    "No duplicate configuration values",
                    "Single authoritative source per data element",
                    "Configuration changes should be centralized",
                    "Data synchronization should be automatic",
                ],
            ),
            ArchitecturalPrinciple.DONT_REPEAT_YOURSELF: ArchitecturalGuidance(
                principle=ArchitecturalPrinciple.DONT_REPEAT_YOURSELF,
                display_name="Don't Repeat Yourself (DRY)",
                description="Every piece of knowledge should have a single representation",
                responsibilities=[
                    "Identify and eliminate code duplication",
                    "Create reusable abstractions for common patterns",
                    "Maintain consistency across similar implementations",
                    "Reduce maintenance burden through centralization",
                ],
                guidelines=[
                    "Extract common functionality into shared modules",
                    "Use inheritance and composition appropriately",
                    "Create utility classes for repeated operations",
                    "Implement template patterns for similar workflows",
                ],
                examples=[
                    "Shared validation utility functions",
                    "Common base classes for similar entities",
                    "Reusable configuration loading patterns",
                    "Standardized error handling patterns",
                ],
                validation_rules=[
                    "Similar code blocks should be abstracted",
                    "No duplicate business logic implementations",
                    "Common patterns should be centralized",
                    "Changes should only need to be made in one place",
                ],
            ),
            ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID: ArchitecturalGuidance(
                principle=ArchitecturalPrinciple.KEEP_IT_SIMPLE_STUPID,
                display_name="Keep It Simple, Stupid (KISS)",
                description="Most systems work best when kept simple rather than made complex",
                responsibilities=[
                    "Prioritize simple solutions over complex ones",
                    "Avoid over-engineering and unnecessary complexity",
                    "Create maintainable and understandable code",
                    "Focus on essential functionality",
                ],
                guidelines=[
                    "Prefer simple algorithms over complex ones",
                    "Avoid premature optimization",
                    "Use clear, descriptive naming",
                    "Write self-documenting code",
                ],
                examples=[
                    "Simple validation over complex rule engines",
                    "Clear function names over abbreviated ones",
                    "Readable code over clever optimizations",
                    "Straightforward data structures",
                ],
                validation_rules=[
                    "Code should be understandable by new team members",
                    "Complex logic should be well-documented",
                    "Performance optimizations should be justified",
                    "Simple solutions should be preferred when adequate",
                ],
            ),
            ArchitecturalPrinciple.TEST_DRIVEN_DEVELOPMENT: ArchitecturalGuidance(
                principle=ArchitecturalPrinciple.TEST_DRIVEN_DEVELOPMENT,
                display_name="Test-Driven Development (TDD)",
                description="Write tests before implementing functionality",
                responsibilities=[
                    "Create comprehensive test suites for all functionality",
                    "Implement red-green-refactor development cycle",
                    "Maintain high test coverage (>85%)",
                    "Ensure tests validate architectural decisions",
                ],
                guidelines=[
                    "Write tests before implementation",
                    "Create tests for all public methods",
                    "Implement comprehensive edge case testing",
                    "Maintain test documentation and examples",
                ],
                examples=[
                    "Unit tests for all business logic",
                    "Integration tests for system components",
                    "Architecture validation tests",
                    "Comprehensive test documentation",
                ],
                validation_rules=[
                    "All public methods must have tests",
                    "Test coverage must be >85%",
                    "Tests must validate architectural contracts",
                    "Edge cases must be covered",
                ],
            ),
        }
