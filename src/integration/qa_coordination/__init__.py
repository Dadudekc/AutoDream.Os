#!/usr/bin/env python3
"""
QA Coordination Package
======================

Agent-6 & Agent-8 Enhanced Quality Assurance Coordination Package
V2 Compliant: Modular design with focused components
"""

from .core_coordination import (
    Agent6Agent8EnhancedQACoordination,
    create_agent6_agent8_enhanced_qa_coordination,
)
from .models import (
    EnhancementPriority,
    PerformanceMetrics,
    Phase3ConsolidationStatus,
    QAEnhancement,
    QAEnhancementArea,
    QAStatus,
    QualityGate,
    ValidationResult,
)
from .performance_validation import (
    PerformanceValidationEnhancement,
    create_performance_validation_enhancement,
)
from .testing_framework_integration import (
    TestingFrameworkIntegration,
    create_testing_framework_integration,
)
from .validation_protocols import AdvancedValidationProtocols, create_advanced_validation_protocols
from .vector_database_integration import (
    VectorDatabaseQAIntegration,
    integrate_vector_database_with_qa,
)

__all__ = [
    # Core coordination
    "Agent6Agent8EnhancedQACoordination",
    "create_agent6_agent8_enhanced_qa_coordination",
    # Models
    "QAEnhancementArea",
    "QAStatus",
    "EnhancementPriority",
    "QAEnhancement",
    "Phase3ConsolidationStatus",
    "ValidationResult",
    "PerformanceMetrics",
    "QualityGate",
    # Vector database integration
    "VectorDatabaseQAIntegration",
    "integrate_vector_database_with_qa",
    # Validation protocols
    "AdvancedValidationProtocols",
    "create_advanced_validation_protocols",
    # Testing framework integration
    "TestingFrameworkIntegration",
    "create_testing_framework_integration",
    # Performance validation
    "PerformanceValidationEnhancement",
    "create_performance_validation_enhancement",
]
