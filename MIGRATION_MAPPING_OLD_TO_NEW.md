# Migration Mapping: Old Monolith Files to New Modular Components

## Overview
This document maps the old monolith file imports to the new modular testing framework components.

## File: src/services/v1_v2_message_queue_system.py → src/services/testing/

### Classes to Replace:
- `V1V2MessageQueueSystem` → `UnifiedMessageQueue` (from message_queue.py)
- `MessageQueueManager` → `UnifiedMessageQueue` (from message_queue.py)
- `MessageQueuePriority` → `MessagePriority` (from message_queue.py)

### Enums to Replace:
- `MessageQueuePriority` → `MessagePriority` (from message_queue.py)

### Functions to Replace:
- All message queue operations → Use `UnifiedMessageQueue` methods

## File: src/services/integration_testing_framework.py → src/services/testing/

### Classes to Replace:
- `IntegrationTestRunner` → `TestExecutor` (from execution_engine.py)
- `IntegrationTestSuite` → `TestOrchestrator` (from execution_engine.py)
- `BaseIntegrationTest` → `TestFramework` (from core_framework.py)
- `CrossSystemCommunicationTest` → `ServiceIntegrationTester` (from service_integration.py)
- `APIIntegrationTest` → `ServiceIntegrationTester` (from service_integration.py)
- `MiddlewareIntegrationTest` → `ServiceIntegrationTester` (from service_integration.py)

### Enums to Replace:
- `TestStatus` → `TestStatus` (from core_framework.py)
- `TestType` → `TestType` (from core_framework.py)
- `TestPriority` → `TestPriority` (from core_framework.py)

### Dataclasses to Replace:
- `TestResult` → `TestResult` (from core_framework.py)
- `TestScenario` → `TestConfig` (from core_framework.py)
- `TestEnvironment` → `TestConfig` (from core_framework.py)

## File: src/services/v2_service_integration_tests.py → src/services/testing/

### Classes to Replace:
- All testing classes → Use appropriate modules from testing framework
- Performance testing → `PerformanceTester` (from performance_tester.py)
- Data management → `TestDataManager` (from data_manager.py)

## Import Pattern Changes

### Old Pattern:
```python
from src.services.v1_v2_message_queue_system import (
    V1V2MessageQueueSystem,
    MessageQueueManager,
    MessageQueuePriority,
)
```

### New Pattern:
```python
from src.services.testing import (
    UnifiedMessageQueue,
    MessagePriority,
)
```

### Old Pattern:
```python
from src.services.integration_testing_framework import (
    IntegrationTestRunner,
    IntegrationTestSuite,
    TestStatus,
    TestType,
    TestPriority,
)
```

### New Pattern:
```python
from src.services.testing import (
    TestExecutor,
    TestOrchestrator,
    TestStatus,
    TestType,
    TestPriority,
)
```

## Migration Steps
1. Update all import statements to use new modular components
2. Replace class instantiations with new class names
3. Update method calls to match new API signatures
4. Test functionality after migration
5. Delete old monolith files

