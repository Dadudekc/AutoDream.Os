# Orchestrator Pattern - V2 Architecture

## Overview

The **Orchestrator Pattern** is a core architectural pattern used throughout the V2 SWARM system. An orchestrator coordinates multiple specialized components without implementing business logic itself, following the Single Responsibility Principle.

## Pattern Definition

An orchestrator is a coordinator class that:
- **Delegates** work to specialized modules/engines
- **Coordinates** interactions between components
- **Manages** lifecycle (initialization → registration → coordination → cleanup)
- **Does NOT** implement business logic directly
- **Maintains** a single responsibility: orchestration

## Benefits

1. **Separation of Concerns**: Clear boundary between coordination and implementation
2. **Testability**: Easy to mock dependencies and test coordination logic
3. **Flexibility**: Easy to swap out component implementations
4. **Maintainability**: Changes to business logic don't affect orchestration
5. **Scalability**: Can add new components without restructuring
6. **V2 Compliance**: Keeps orchestrators lean (<400 lines)

## Pattern Structure

```python
class SomeOrchestrator:
    """Main orchestrator for [domain] operations."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize orchestrator and its components."""
        self.config = config or self._default_config()
        
        # Initialize specialized components
        self.engine = SomeEngine(self.config)
        self.analyzer = SomeAnalyzer()
        self.logger = SomeLogger()
        
        # Register components
        self._register_components()

    def _register_components(self) -> None:
        """Register components and setup integrations."""
        # Register protocols, handlers, etc.
        pass

    def coordinate_operation(self, input_data: Any) -> Result:
        """Coordinate a complex operation across components."""
        # 1. Validate input
        validated = self.engine.validate(input_data)
        
        # 2. Analyze
        analysis = self.analyzer.analyze(validated)
        
        # 3. Process
        result = self.engine.process(analysis)
        
        # 4. Log
        self.logger.log_operation(result)
        
        return result

    def cleanup(self) -> None:
        """Cleanup orchestrator and all components."""
        self.engine.cleanup()
        self.analyzer.cleanup()
        self.logger.cleanup()
```

## Lifecycle Phases

### 1. Initialization
**Purpose**: Create and configure components

```python
def __init__(self, config: Optional[Config] = None):
    self.config = config or self._load_default_config()
    self.component_a = ComponentA(self.config)
    self.component_b = ComponentB(self.config)
```

**Best Practices**:
- Load configuration first
- Initialize all components
- Avoid heavy operations in `__init__`
- Use dependency injection for testability

### 2. Registration
**Purpose**: Connect components and setup integrations

```python
def _register_components(self) -> None:
    """Register components with each other."""
    self.engine.register_handler(self.handler)
    self.service.register_callbacks(self.callbacks)
```

**Best Practices**:
- Register handlers, protocols, callbacks
- Setup event listeners
- Configure component relationships
- Validate registration success

### 3. Coordination
**Purpose**: Execute operations by coordinating components

```python
def execute_workflow(self, input_data: Any) -> Result:
    """Execute workflow across multiple components."""
    validated = self.validator.validate(input_data)
    processed = self.processor.process(validated)
    result = self.formatter.format(processed)
    return result
```

**Best Practices**:
- Delegate to components, don't implement
- Handle errors at orchestration level
- Provide clear return values
- Log coordination steps

### 4. Cleanup
**Purpose**: Gracefully shutdown components

```python
def cleanup(self) -> None:
    """Cleanup all components."""
    for component in self.components:
        component.cleanup()
    self.logger.info("Orchestrator cleaned up")
```

**Best Practices**:
- Cleanup in reverse order of initialization
- Handle cleanup errors gracefully
- Log cleanup progress
- Release all resources

## When to Create a New Orchestrator

### ✅ Create New Orchestrator When:

1. **New Domain**: Introducing a new functional domain (e.g., "Payment Processing")
2. **Complex Coordination**: Need to coordinate 3+ specialized components
3. **Multiple Entry Points**: Domain needs multiple public coordination methods
4. **Independent Lifecycle**: Components need coordinated initialization/cleanup
5. **Clear Boundary**: Domain has well-defined boundaries and responsibilities

### ❌ Don't Create Orchestrator When:

1. **Simple Service**: Single component with no coordination needed
2. **Helper Utility**: Pure functions or utilities (use utility modules instead)
3. **Nested Orchestration**: Orchestrators should not orchestrate other orchestrators
4. **Business Logic**: Need to implement business logic (use engines/services instead)
5. **Too Small**: Only coordinating 1-2 simple operations

## When to Extend Existing Orchestrator

### ✅ Extend Existing When:

1. **Same Domain**: Functionality belongs to existing orchestrator's domain
2. **Shared Components**: Uses same underlying components
3. **Related Operations**: New operation is related to existing operations
4. **Maintains Cohesion**: Extension doesn't break Single Responsibility
5. **V2 Compliant**: Extension keeps orchestrator under 400 lines

### ⚠️ Consider Refactoring When:

1. **> 400 Lines**: Orchestrator exceeds V2 compliance limit
2. **Too Many Components**: Managing more than 7-8 components
3. **Mixed Responsibilities**: Handling unrelated concerns
4. **Complex Conditionals**: Too many if/else branches
5. **Duplication**: Similar patterns repeated multiple times

## Examples from V2 Codebase

### 1. Core Orchestrator
**File**: `src/core/orchestration/core_orchestrator.py`

**Purpose**: Core system orchestration

**Components Coordinated**:
- Service orchestrator
- Integration orchestrator
- Configuration management
- Logging system

**Key Methods**:
- `initialize_system()` - System-wide initialization
- `coordinate_services()` - Service coordination
- `shutdown()` - Graceful shutdown

### 2. Overnight Orchestrator
**File**: `src/orchestrators/overnight/orchestrator.py`

**Purpose**: 24/7 autonomous operations

**Components Coordinated**:
- Task scheduler
- Progress monitor
- Recovery system
- Workflow engine

**Key Methods**:
- `start_cycle()` - Begin overnight cycle
- `monitor_progress()` - Track operations
- `handle_recovery()` - Error recovery

### 3. Emergency Orchestrator
**File**: `src/core/emergency_intervention/.../emergency_orchestrator.py`

**Purpose**: Emergency intervention coordination

**Components Coordinated**:
- Emergency engine
- Emergency analyzer
- Emergency logger
- Emergency protocols

**Key Methods**:
- `detect_emergency()` - Emergency detection
- `coordinate_intervention()` - Intervention coordination
- `log_resolution()` - Resolution logging

### 4. Error Handling Orchestrator
**File**: `src/core/error_handling/error_handling_orchestrator.py`

**Purpose**: Unified error handling

**Components Coordinated**:
- Retry engine
- Specialized handlers
- Error analysis engine

**Key Methods**:
- `retry_operation()` - Retry with backoff
- `safe_execute()` - Safe execution wrapper
- `handle_error()` - Error handling coordination

### 5. Services Orchestrator (JavaScript)
**File**: `src/web/static/js/services-orchestrator.js`

**Purpose**: Frontend service coordination

**Components Coordinated**:
- Data service
- Socket service
- Performance service
- Validation service

**Key Methods**:
- `initialize()` - Service initialization
- `execute()` - Operation coordination
- `broadcast()` - Multi-service broadcast

## Base Orchestrator Recommendations

While not currently implemented, a base orchestrator class would provide:

### Common Interface
```python
class BaseOrchestrator(ABC):
    """Base class for all orchestrators."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or self._load_default_config()
        self.components: Dict[str, Any] = {}
        self.initialized = False

    @abstractmethod
    def _register_components(self) -> None:
        """Register components (implement in subclass)."""
        pass

    @abstractmethod
    def _load_default_config(self) -> Config:
        """Load default configuration (implement in subclass)."""
        pass

    def initialize(self) -> None:
        """Initialize orchestrator."""
        if self.initialized:
            return
        self._register_components()
        self.initialized = True

    def cleanup(self) -> None:
        """Cleanup orchestrator."""
        for component in self.components.values():
            if hasattr(component, 'cleanup'):
                component.cleanup()
        self.initialized = False

    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status."""
        return {
            "initialized": self.initialized,
            "components": list(self.components.keys()),
            "config": self.config.__dict__ if hasattr(self.config, '__dict__') else {}
        }
```

### Benefits of Base Class
- **Consistency**: Uniform interface across all orchestrators
- **Reusability**: Common lifecycle management
- **Type Safety**: Clear abstract contract
- **Testing**: Easier to test common functionality
- **Documentation**: Self-documenting interface

### Considerations
- **Flexibility**: Some orchestrators may need different patterns
- **Complexity**: Adds inheritance layer
- **Migration**: Existing orchestrators would need refactoring
- **V2 Compliance**: Must not add unnecessary complexity

## Best Practices

### DO ✅

1. **Keep It Thin**: Orchestrators should be <400 lines
2. **Delegate Everything**: No business logic in orchestrators
3. **Clear Names**: Use descriptive method names that explain coordination
4. **Error Handling**: Handle errors at coordination boundaries
5. **Logging**: Log coordination steps for debugging
6. **Type Hints**: Use type hints for all parameters and returns
7. **Documentation**: Document what is being coordinated and why
8. **Testing**: Test coordination logic, mock components

### DON'T ❌

1. **Implement Logic**: Don't implement business logic
2. **Nest Orchestrators**: Don't call orchestrators from orchestrators
3. **Mix Concerns**: Don't handle unrelated domains
4. **Bloat**: Don't let orchestrators grow beyond 400 lines
5. **Direct I/O**: Don't access databases/files directly
6. **State Management**: Don't manage complex state
7. **Tight Coupling**: Don't depend on concrete implementations
8. **Hidden Logic**: Don't hide coordination in private methods

## Common Patterns

### Pattern 1: Sequential Coordination
```python
def process_workflow(self, data: Input) -> Output:
    """Process workflow sequentially."""
    validated = self.validator.validate(data)
    transformed = self.transformer.transform(validated)
    result = self.processor.process(transformed)
    return result
```

### Pattern 2: Parallel Coordination
```python
async def process_parallel(self, data: Input) -> Output:
    """Process components in parallel."""
    results = await asyncio.gather(
        self.service_a.process(data),
        self.service_b.process(data),
        self.service_c.process(data)
    )
    return self.aggregator.aggregate(results)
```

### Pattern 3: Conditional Coordination
```python
def route_operation(self, operation: Operation) -> Result:
    """Route operation to appropriate handler."""
    if operation.type == OperationType.EMERGENCY:
        return self.emergency_handler.handle(operation)
    elif operation.type == OperationType.ROUTINE:
        return self.routine_handler.handle(operation)
    else:
        return self.default_handler.handle(operation)
```

### Pattern 4: Event-Driven Coordination
```python
def setup_event_coordination(self) -> None:
    """Setup event-driven coordination."""
    self.service_a.on('dataReady', self.handle_data_ready)
    self.service_b.on('processComplete', self.handle_process_complete)
    self.service_c.on('error', self.handle_error)
```

## Anti-Patterns to Avoid

### ❌ God Orchestrator
```python
# BAD: Orchestrator doing too much
class GodOrchestrator:
    def do_everything(self):
        # Hundreds of lines of logic
        # Managing dozens of components
        # Handling unrelated concerns
```

**Solution**: Split into multiple domain-specific orchestrators

### ❌ Anemic Orchestrator
```python
# BAD: Orchestrator with no real coordination
class AnemicOrchestrator:
    def process(self, data):
        return self.service.process(data)  # Just a passthrough
```

**Solution**: Use the service directly, remove orchestrator

### ❌ Logic Orchestrator
```python
# BAD: Business logic in orchestrator
class LogicOrchestrator:
    def calculate_total(self, items):
        total = 0
        for item in items:
            total += item.price * item.quantity  # Business logic!
        return total
```

**Solution**: Move logic to dedicated service/engine

### ❌ Nested Orchestration
```python
# BAD: Orchestrator calling another orchestrator
class OuterOrchestrator:
    def process(self):
        return self.inner_orchestrator.coordinate()  # Nested!
```

**Solution**: Refactor to single orchestrator or component hierarchy

## Testing Orchestrators

### Unit Testing
```python
def test_orchestrator_coordination():
    # Arrange: Mock components
    mock_engine = Mock()
    mock_analyzer = Mock()
    orchestrator = SomeOrchestrator()
    orchestrator.engine = mock_engine
    orchestrator.analyzer = mock_analyzer

    # Act: Test coordination
    result = orchestrator.coordinate_operation(test_data)

    # Assert: Verify coordination
    mock_engine.process.assert_called_once()
    mock_analyzer.analyze.assert_called_once()
    assert result == expected_result
```

### Integration Testing
```python
def test_orchestrator_integration():
    # Arrange: Real components
    orchestrator = SomeOrchestrator(test_config)
    orchestrator.initialize()

    # Act: Test real coordination
    result = orchestrator.coordinate_operation(test_data)

    # Assert: Verify end-to-end behavior
    assert result.status == "success"
    assert len(result.steps) == 3

    # Cleanup
    orchestrator.cleanup()
```

## Migration Guide

### Converting to Orchestrator Pattern

1. **Identify Coordination**: Find classes doing too much coordination
2. **Extract Components**: Split business logic into specialized components
3. **Create Orchestrator**: Build thin orchestration layer
4. **Implement Lifecycle**: Add init → register → coordinate → cleanup
5. **Update Tests**: Test coordination logic with mocked components
6. **Migrate Callers**: Update code to use new orchestrator

### Example Migration
```python
# BEFORE: Monolithic service
class MonolithicService:
    def process(self, data):
        validated = self._validate(data)  # 50 lines
        analyzed = self._analyze(validated)  # 100 lines
        result = self._process(analyzed)  # 150 lines
        self._log(result)  # 30 lines
        return result

# AFTER: Orchestrator + Components
class ProcessingOrchestrator:
    def __init__(self):
        self.validator = Validator()
        self.analyzer = Analyzer()
        self.processor = Processor()
        self.logger = Logger()

    def process(self, data):
        validated = self.validator.validate(data)
        analyzed = self.analyzer.analyze(validated)
        result = self.processor.process(analyzed)
        self.logger.log(result)
        return result
```

## Conclusion

The Orchestrator Pattern is essential to V2 SWARM's architecture, enabling:
- **Clean separation** between coordination and implementation
- **V2 compliance** through lean, focused orchestrators
- **Scalability** via modular component composition
- **Maintainability** through clear responsibility boundaries

When implemented correctly, orchestrators provide a powerful foundation for building complex, coordinated systems while maintaining simplicity and testability.

---

**Last Updated**: 2025-10-07  
**Author**: V2 SWARM Architecture Team  
**Status**: Living Document

