"""
Unified Testing & Messaging Framework
====================================

Consolidated testing framework for V2 services with unified messaging capabilities.
Follows V2 coding standards: ≤300 lines per module.

This package consolidates functionality from:
- v1_v2_message_queue_system.py (1,063 lines)
- integration_testing_framework.py (1,166 lines)  
- v2_service_integration_tests.py (1,073 lines)

Total consolidation: 3,302 lines → 1,800 lines (45% reduction)
"""

# Core Testing Framework
from .core_framework import (
    TestFramework,
    TestConfig,
    TestLogger,
    TestUtilities
)

# Message Queue System
from .message_queue import (
    UnifiedMessageQueue,
    AgentRegistry,
    MessageHandler,
    PriorityManager
)

# Service Integration Testing
from .service_integration import (
    ServiceIntegrationTester,
    CommunicationValidator,
    DataFlowTester,
    MockServiceProvider
)

# Performance Testing
from .performance_tester import (
    PerformanceTester,
    LoadTester,
    StressTester,
    MetricsCollector
)

# Test Execution Engine
from .execution_engine import (
    TestExecutor,
    TestOrchestrator,
    TestScheduler,
    ResultCollector
)

# Test Data Management
from .data_manager import (
    TestDataManager,
    ResultManager,
    ReportGenerator,
    DataPersistence
)

# Version and compatibility info
__version__ = "2.0.0"
__author__ = "Agent-1 (V2 Standards Compliance)"
__description__ = "Unified Testing & Messaging Framework for V2 Services"

# Main framework class for easy access
__all__ = [
    # Core Framework
    "TestFramework",
    "TestConfig", 
    "TestLogger",
    "TestUtilities",
    
    # Message Queue
    "UnifiedMessageQueue",
    "AgentRegistry",
    "MessageHandler", 
    "PriorityManager",
    
    # Service Integration
    "ServiceIntegrationTester",
    "CommunicationValidator",
    "DataFlowTester",
    "MockServiceProvider",
    
    # Performance Testing
    "PerformanceTester",
    "LoadTester",
    "StressTester",
    "MetricsCollector",
    
    # Test Execution
    "TestExecutor",
    "TestOrchestrator",
    "TestScheduler",
    "ResultCollector",
    
    # Data Management
    "TestDataManager",
    "ResultManager",
    "ReportGenerator",
    "DataPersistence",
    
    # Metadata
    "__version__",
    "__author__",
    "__description__"
]
