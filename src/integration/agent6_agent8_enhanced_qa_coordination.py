#!/usr/bin/env python3
"""
Agent-6 & Agent-8 Enhanced Quality Assurance Coordination
=========================================================

REFACTORED: Now uses modular design with focused components
V2 Compliant: ≤400 lines, imports from qa_coordination package

This file now serves as the main entry point and maintains backward compatibility
while delegating to the modular qa_coordination package.
"""

# Import all functionality from the modular package
from .qa_coordination import (
    Agent6Agent8EnhancedQACoordination,
    create_advanced_validation_protocols,
    create_agent6_agent8_enhanced_qa_coordination,
    create_performance_validation_enhancement,
    create_testing_framework_integration,
    integrate_vector_database_with_qa,
)

# Re-export for backward compatibility
__all__ = [
    "Agent6Agent8EnhancedQACoordination",
    "create_agent6_agent8_enhanced_qa_coordination",
    "integrate_vector_database_with_qa",
    "create_advanced_validation_protocols",
    "create_testing_framework_integration",
    "create_performance_validation_enhancement",
]


# Main execution function for backward compatibility
def main():
    """Main execution function"""
    print("🤖 Agent-6 & Agent-8 Enhanced QA Coordination (Refactored)")
    print("📦 Using modular qa_coordination package")

    # Create coordination system
    coordination = create_agent6_agent8_enhanced_qa_coordination()

    # Generate report
    report = coordination.generate_enhanced_qa_report()

    print(f"✅ QA Coordination Status: {report['coordination_status']}")
    print(f"📊 QA Enhancements: {len(report['qa_enhancements'])}")
    print(
        f"🔗 Vector Database: {report['vector_database_integration']['vector_database_integration']}"
    )

    return coordination


if __name__ == "__main__":
    main()
