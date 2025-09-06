#!/usr/bin/env python3
"""
Architectural Onboarding Demo - Agent Cellphone V2
==================================================

Demonstration of the architectural onboarding system with principle-based
agent onboarding and TDD architectural proof.
"""

import os
import tempfile
import subprocess
from pathlib import Path

from src.services.architectural_onboarding import (
    architectural_manager,
    ArchitecturalPrinciple,
    ArchitecturalOnboardingManager
)


def demo_architectural_principles():
    """Demonstrate architectural principle assignments and guidance."""
    print("🎯 ARCHITECTURAL ONBOARDING SYSTEM DEMO")
    print("=" * 60)

    print("\n📋 Agent Principle Assignments:")
    print("-" * 40)

    for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]:
        principle = architectural_manager.get_agent_principle(agent_id)
        guidance = architectural_manager.get_principle_guidance(principle)
        print(f"{agent_id}: {guidance.display_name}")

    print("\n📚 Sample Architectural Guidance (SRP):")
    print("-" * 40)

    srp_guidance = architectural_manager.get_principle_guidance(ArchitecturalPrinciple.SINGLE_RESPONSIBILITY)
    print(f"Principle: {srp_guidance.display_name}")
    print(f"Description: {srp_guidance.description}")
    print(f"Key Responsibilities: {srp_guidance.responsibilities[0]}")
    print(f"Validation Rules: {srp_guidance.validation_rules[0]}")


def demo_onboarding_messages():
    """Demonstrate customized onboarding messages."""
    print("\n💬 Customized Onboarding Messages:")
    print("-" * 40)

    for agent_id in ["Agent-1", "Agent-2", "Agent-3"]:
        message = architectural_manager.create_onboarding_message(agent_id)
        print(f"\n{agent_id} Onboarding Message:")
        print("-" * 30)
        # Show first few lines of the message
        lines = message.split('\n')[:5]
        for line in lines:
            print(f"  {line}")
        print("  ...")


def demo_compliance_validation():
    """Demonstrate agent compliance validation."""
    print("\n✅ Compliance Validation Demo:")
    print("-" * 40)

    # Mock code changes for different agents
    test_cases = [
        ("Agent-1", ["class BigClass:", "    def method1(self): pass", "    def method2(self): pass", "    def method3(self): pass", "    def method4(self): pass"]),
        ("Agent-7", ["def func1(): pass", "def func1(): pass", "def func1(): pass"]),  # DRY violation
        ("Agent-8", ["def complex_function(param1, param2, param3, param4, param5):", "    " * 100 + "pass"]),  # KISS violation
    ]

    for agent_id, changes in test_cases:
        result = architectural_manager.validate_agent_compliance(agent_id, changes)
        print(f"\n{agent_id} Compliance Check:")
        print(f"  Principle: {result['principle']}")
        print(f"  Compliant: {result['compliant']}")
        if result['issues']:
            print(f"  Issues: {len(result['issues'])}")
            for issue in result['issues'][:2]:  # Show first 2 issues
                print(f"    - {issue}")


def demo_cli_integration():
    """Demonstrate CLI integration with architectural onboarding."""
    print("\n🖥️  CLI Integration Demo:")
    print("-" * 40)

    print("Available CLI commands:")
    print("  --onboarding --onboarding-style architectural")
    print("  --onboard --agent Agent-1 --onboarding-style architectural")
    print("  --onboard --agent Agent-1 --onboarding-style architectural --architectural-principle TDD")

    print("\nExample usage:")
    print("  python -m src.services.messaging_cli --onboard --agent Agent-1 --onboarding-style architectural")


def demo_principle_queries():
    """Demonstrate principle-based queries."""
    print("\n🔍 Principle-Based Queries:")
    print("-" * 40)

    # Show agents by principle
    for principle in [ArchitecturalPrinciple.SINGLE_RESPONSIBILITY, ArchitecturalPrinciple.DONT_REPEAT_YOURSELF]:
        agents = architectural_manager.get_agents_by_principle(principle)
        guidance = architectural_manager.get_principle_guidance(principle)
        print(f"{guidance.display_name}: {', '.join(agents)}")


def demo_architecture_validation():
    """Demonstrate architectural validation capabilities."""
    print("\n🏗️  Architectural Validation:")
    print("-" * 40)

    from tests.test_architectural_compliance import CodeAnalyzer, ArchitecturalValidator

    # Analyze current codebase
    analyzer = CodeAnalyzer()
    validator = ArchitecturalValidator(analyzer)

    print(f"Analyzed {len(analyzer.files)} Python files")

    # Check for basic architectural metrics
    total_lines = sum(analyzer.analyze_file(f)["line_count"] for f in analyzer.files[:5])  # Sample first 5
    print(f"Sample code metrics: ~{total_lines} lines analyzed")

    print("\nArchitectural validation capabilities:")
    print("  ✅ Single Responsibility Principle validation")
    print("  ✅ Open-Closed Principle validation")
    print("  ✅ DRY principle validation")
    print("  ✅ KISS principle validation")
    print("  ✅ Code complexity analysis")
    print("  ✅ Duplication detection")


def main():
    """Run the architectural onboarding demonstration."""
    print("🏛️  PROFESSIONAL ARCHITECTURAL ONBOARDING SYSTEM")
    print("Built with SOLID principles, SSOT, DRY, KISS, and TDD architectural proof")
    print("=" * 80)

    demo_architectural_principles()
    demo_onboarding_messages()
    demo_compliance_validation()
    demo_cli_integration()
    demo_principle_queries()
    demo_architecture_validation()

    print("\n🎉 ARCHITECTURAL ONBOARDING SYSTEM DEMO COMPLETE")
    print("=" * 80)
    print("\nKey Achievements:")
    print("  ✅ Principle-based agent onboarding")
    print("  ✅ Comprehensive TDD architectural validation")
    print("  ✅ Automated compliance checking")
    print("  ✅ CLI integration for production use")
    print("  ✅ Extensible architecture for future principles")
    print("  ✅ Professional code quality assurance")


if __name__ == "__main__":
    main()
