"""
Design Authority Knowledge Base
================================

Knowledge base data for Design Authority agent.
Modular split from design_authority.py for V2 compliance.

Author: Agent-7 (Web Development Expert)
License: MIT
V2 Compliance: ≤400 lines
"""

from typing import Any


def get_design_knowledge_base() -> dict[str, Any]:
    """Get the design authority knowledge base."""
    return {
        "principles": {
            "KISS": {
                "description": "Keep It Simple, Stupid",
                "guidelines": [
                    "Prefer simple functions over complex classes",
                    "Use built-in types when possible",
                    "Avoid premature abstractions",
                    "Choose clarity over cleverness",
                ],
                "red_flags": [
                    "complex",
                    "advanced",
                    "sophisticated",
                    "enterprise",
                    "framework",
                    "architecture",
                    "pattern",
                    "design",
                ],
            },
            "YAGNI": {
                "description": "You Aren't Gonna Need It",
                "guidelines": [
                    "Build only what you need right now",
                    "Avoid speculative features",
                    "Start simple, add complexity when required",
                    "Prefer composition over inheritance",
                ],
                "red_flags": [
                    "future-proof",
                    "extensible",
                    "scalable",
                    "generic",
                    "reusable",
                    "flexible",
                    "configurable",
                ],
            },
            "Single_Responsibility": {
                "description": "One component, one purpose",
                "guidelines": [
                    "Each function should do one thing well",
                    "Separate concerns clearly",
                    "Avoid god classes or functions",
                    "Keep modules focused",
                ],
                "red_flags": [
                    "manager",
                    "handler",
                    "controller",
                    "processor",
                    "service",
                    "facade",
                    "adapter",
                ],
            },
        },
        "anti_patterns": [
            "Creating interfaces before understanding requirements",
            "Building generic solutions for specific problems",
            "Over-engineering simple data structures",
            "Premature optimization",
            "Complex inheritance hierarchies",
            "Deeply nested conditional logic",
            "Functions with too many parameters",
            "Classes with too many responsibilities",
        ],
        "preferred_alternatives": {
            "complex_class": "simple_function",
            "inheritance": "composition",
            "interface": "concrete_type",
            "factory": "direct_instantiation",
            "builder": "constructor",
            "strategy": "if_statement",
            "observer": "callback_function",
        },
    }


__all__ = ['get_design_knowledge_base']

