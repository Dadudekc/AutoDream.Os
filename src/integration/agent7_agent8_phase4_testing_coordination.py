"""
Agent-7 & Agent-8 Phase 4 Testing Coordination System
Agent-8 Integration Specialist + Agent-7 Testing Specialist
5-Agent Testing Mode - Phase 4 Validation Preparation
Refactored into modular components for V2 compliance
"""

# Import all components from refactored modules
from .agent7_agent8_phase4_testing_coordination_core import (
    CoordinationSession,
    CoordinationStatus,
    TestCase,
    TestPriority,
    TestStatus,
    TestSuite,
    TestingCore,
    TestingMetrics,
    TestingPhase
)
from .agent7_agent8_phase4_testing_coordination_utils import (
    CoordinationTimer,
    TestingAnalyzer,
    TestingReporter,
    TestingValidator,
    create_test_case,
    format_execution_time
)
from .agent7_agent8_phase4_testing_coordination_main import (
    Agent7Agent8Phase4TestingCoordination,
    TestingCoordinationManager,
    create_phase4_testing_coordination,
    run_phase4_testing_coordination
)

# Re-export main classes for backward compatibility
__all__ = [
    'TestingPhase',
    'TestPriority',
    'TestStatus',
    'CoordinationStatus',
    'TestCase',
    'TestSuite',
    'CoordinationSession',
    'TestingMetrics',
    'TestingCore',
    'TestingValidator',
    'TestingAnalyzer',
    'TestingReporter',
    'CoordinationTimer',
    'Agent7Agent8Phase4TestingCoordination',
    'TestingCoordinationManager',
    'create_test_case',
    'create_phase4_testing_coordination',
    'run_phase4_testing_coordination',
    'format_execution_time'
]
