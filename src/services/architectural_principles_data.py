"""
Architectural Principles Data Definitions
==========================================

Individual principle definitions extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

from .architectural_models import ArchitecturalGuidance, ArchitecturalPrinciple


def get_srp_guidance() -> ArchitecturalGuidance:
    """Get Single Responsibility Principle guidance."""
    return ArchitecturalGuidance(
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
    )


def get_ocp_guidance() -> ArchitecturalGuidance:
    """Get Open-Closed Principle guidance."""
    return ArchitecturalGuidance(
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
    )
