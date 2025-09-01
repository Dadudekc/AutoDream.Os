# Coordination Systems User Guide

## Quick Start Guide

This guide provides practical examples and step-by-step instructions for using the enhanced coordination and communication systems.

## Prerequisites

- Python 3.8+
- Required packages: `pyyaml`, `psutil` (optional)
- Access to the coordination systems modules

## Installation and Setup

### 1. Basic Setup

```python
# Import required modules
from src.core.validation.coordination_validator import CoordinationValidator
from src.core.error_handling.coordination_error_handler import CoordinationErrorHandler
from src.core.performance.coordination_performance_monitor import CoordinationPerformanceMonitor

# Initialize components
validator = CoordinationValidator()
error_handler = CoordinationErrorHandler()
performance_monitor = CoordinationPerformanceMonitor()
```

### 2. Configuration

```python
# Configure error handling
error_handler.configure_retry(
    max_retries=3,
    base_delay=1.0,
    backoff_multiplier=2.0
)

# Configure performance monitoring
performance_monitor.configure_monitoring(
    collection_interval=5.0,
    max_data_points=1000
)
```

## Practical Examples

### Example 1: Message Validation

#### Scenario: Validating User Input

```python
def validate_user_message(user_input):
    """Validate user message before processing"""
    
    # Define message structure
    message_data = {
        "content": user_input.get("message", ""),
        "user_id": user_input.get("user_id"),
        "timestamp": user_input.get("timestamp"),
        "priority": user_input.get("priority", "normal")
    }
    
    # Validate message structure
    validation_result = validator.validate_message_structure(message_data)
    
    if not validation_result.is_valid:
        print(f"❌ Validation failed: {validation_result.score}%")
        print(f"Errors: {validation_result.errors}")
        return False
    
    print(f"✅ Validation passed: {validation_result.score}%")
    return True

# Usage
user_input = {
    "message": "Hello, world!",
    "user_id": "user_123",
    "timestamp": "2024-01-01T12:00:00Z",
    "priority": "high"
}

is_valid = validate_user_message(user_input)
```

#### Scenario: Batch Validation

```python
def validate_multiple_messages(messages):
    """Validate multiple messages and generate report"""
    
    results = []
    for i, message in enumerate(messages):
        result = validator.validate_message_structure(message)
        results.append({
            "message_id": i,
            "is_valid": result.is_valid,
            "score": result.score,
            "errors": result.errors
        })
    
    # Generate comprehensive report
    report = validator.get_validation_report()
    
    print(f"📊 Batch Validation Report")
    print(f"Total messages: {len(messages)}")
    print(f"Valid messages: {sum(1 for r in results if r['is_valid'])}")
    print(f"Overall compliance: {report['compliance_score']}%")
    
    return results, report
```

### Example 2: Error Handling with Retry

#### Scenario: API Call with Retry

```python
def fetch_user_data(user_id):
    """Fetch user data from external API with retry logic"""
    
    def api_call():
        # Simulate API call
        import random
        if random.random() < 0.3:  # 30% failure rate
            raise ConnectionError("API connection failed")
        return {"user_id": user_id, "name": "John Doe"}
    
    # Execute with error handling
    result = error_handler.execute_with_error_handling(
        operation=api_call,
        max_retries=3,
        error_severity="MEDIUM"
    )
    
    return result

# Usage
try:
    user_data = fetch_user_data("user_123")
    print(f"✅ User data: {user_data}")
except Exception as e:
    print(f"❌ Failed to fetch user data: {e}")
```

#### Scenario: Database Operation with Circuit Breaker

```python
def execute_database_query(query):
    """Execute database query with circuit breaker protection"""
    
    def db_operation():
        # Simulate database operation
        import random
        if random.random() < 0.2:  # 20% failure rate
            raise Exception("Database connection failed")
        return {"result": "query executed successfully"}
    
    # Execute with circuit breaker protection
    result = error_handler.execute_with_error_handling(
        operation=db_operation,
        max_retries=2,
        error_severity="HIGH"
    )
    
    return result

# Usage
try:
    result = execute_database_query("SELECT * FROM users")
    print(f"✅ Query result: {result}")
except Exception as e:
    print(f"❌ Database operation failed: {e}")
    
    # Check circuit breaker status
    health = error_handler.get_error_report()
    print(f"Circuit breaker status: {health['circuit_breaker_status']}")
```

### Example 3: Performance Monitoring

#### Scenario: API Endpoint Performance Tracking

```python
def api_endpoint_handler(request_data):
    """Handle API endpoint with performance monitoring"""
    
    # Start performance monitoring
    performance_monitor.start_monitoring()
    
    try:
        # Record operation start
        with performance_monitor.record_operation("api_request"):
            
            # Process request
            result = process_request(request_data)
            
            # Record success
            performance_monitor.record_success("api_request")
            
            return result
            
    except Exception as e:
        # Record failure
        performance_monitor.record_failure("api_request", str(e))
        raise
    finally:
        # Stop monitoring
        performance_monitor.stop_monitoring()

# Usage
request_data = {"action": "create_user", "data": {"name": "John"}}
try:
    result = api_endpoint_handler(request_data)
    print(f"✅ API response: {result}")
    
    # Get performance report
    report = performance_monitor.get_performance_report()
    print(f"📊 Performance: {report['response_times']['mean']:.2f}ms avg")
    
except Exception as e:
    print(f"❌ API error: {e}")
```

#### Scenario: System Health Monitoring

```python
def monitor_system_health():
    """Monitor system health and performance"""
    
    # Start background monitoring
    performance_monitor.start_monitoring()
    
    # Record system health
    performance_monitor.record_system_health()
    
    # Get health assessment
    health = performance_monitor.get_system_health()
    
    print(f"🏥 System Health Report")
    print(f"Status: {health['health_status']}")
    print(f"Performance Score: {health['performance_score']:.1f}/100")
    print(f"CPU Usage: {health['cpu_usage']:.1f}%")
    print(f"Memory Usage: {health['memory_usage']:.1f}%")
    
    # Stop monitoring
    performance_monitor.stop_monitoring()
    
    return health

# Usage
health_status = monitor_system_health()
```

### Example 4: Integration in Service Layer

#### Scenario: Complete Service with All Systems

```python
class EnhancedUserService:
    """User service with enhanced coordination capabilities"""
    
    def __init__(self):
        self.validator = CoordinationValidator()
        self.error_handler = CoordinationErrorHandler()
        self.performance_monitor = CoordinationPerformanceMonitor()
        
        # Configure components
        self.error_handler.configure_retry(max_retries=3)
        self.performance_monitor.start_monitoring()
    
    def create_user(self, user_data):
        """Create user with full validation and monitoring"""
        
        # Validate input
        validation_result = self.validator.validate_message_structure(user_data)
        if not validation_result.is_valid:
            raise ValueError(f"Invalid user data: {validation_result.errors}")
        
        # Execute with error handling and performance monitoring
        with self.performance_monitor.record_operation("create_user"):
            result = self.error_handler.execute_with_error_handling(
                operation=self._create_user_internal,
                args=[user_data],
                error_severity="MEDIUM"
            )
        
        return result
    
    def _create_user_internal(self, user_data):
        """Internal user creation logic"""
        # Simulate user creation
        import time
        time.sleep(0.1)  # Simulate processing time
        
        return {
            "user_id": f"user_{int(time.time())}",
            "status": "created",
            "data": user_data
        }
    
    def get_performance_report(self):
        """Get service performance report"""
        return self.performance_monitor.get_performance_report()
    
    def get_health_status(self):
        """Get service health status"""
        return self.error_handler.get_error_report()

# Usage
service = EnhancedUserService()

# Create user
user_data = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "age": 30
}

try:
    user = service.create_user(user_data)
    print(f"✅ User created: {user}")
    
    # Check performance
    perf_report = service.get_performance_report()
    print(f"📊 Performance: {perf_report['response_times']['mean']:.2f}ms avg")
    
    # Check health
    health = service.get_health_status()
    print(f"🏥 Health: {health['health_status']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

## Advanced Usage Patterns

### Custom Error Handling

```python
from src.core.error_handling.models import ErrorSeverity, ErrorContext

def custom_error_handler(operation, *args, **kwargs):
    """Custom error handling with specific logic"""
    
    # Create custom error context
    context = ErrorContext(
        operation_name="custom_operation",
        severity=ErrorSeverity.HIGH,
        retry_strategy="exponential_backoff",
        max_retries=5
    )
    
    # Execute with custom context
    result = error_handler.execute_with_error_handling(
        operation=operation,
        args=args,
        kwargs=kwargs,
        error_context=context
    )
    
    return result
```

### Performance Monitoring Decorators

```python
from src.core.performance.coordination_performance_monitor import track_performance

@track_performance("database_operation")
def database_operation():
    """Database operation with automatic performance tracking"""
    import time
    time.sleep(0.05)  # Simulate database operation
    return {"status": "success"}

# Usage
result = database_operation()
```

### Validation Rule Customization

```python
def create_custom_validation_rules():
    """Create custom validation rules for specific use cases"""
    
    custom_rules = {
        "user_profile": {
            "required_fields": ["name", "email", "age"],
            "field_validations": {
                "email": {"type": "email", "required": True},
                "age": {"type": "integer", "min": 18, "max": 120},
                "name": {"type": "string", "min_length": 2, "max_length": 50}
            }
        }
    }
    
    # Load custom rules
    validator.load_custom_rules(custom_rules)
    
    return validator
```

## Troubleshooting Common Issues

### Issue 1: Validation Failures

**Problem**: Messages failing validation with low scores

**Solution**:
```python
# Check validation rules
rules = validator.get_loaded_rules()
print(f"Loaded rules: {list(rules.keys())}")

# Validate specific message
result = validator.validate_message_structure(message_data)
print(f"Validation details: {result.errors}")
```

### Issue 2: Circuit Breaker Always Open

**Problem**: Circuit breaker not recovering from failures

**Solution**:
```python
# Check circuit breaker status
health = error_handler.get_error_report()
print(f"Circuit breaker: {health['circuit_breaker_status']}")

# Reset circuit breaker if needed
error_handler.reset_circuit_breaker()
```

### Issue 3: Performance Monitoring Not Working

**Problem**: No performance data being collected

**Solution**:
```python
# Check if monitoring is active
is_active = performance_monitor.is_monitoring_active()
print(f"Monitoring active: {is_active}")

# Start monitoring if not active
if not is_active:
    performance_monitor.start_monitoring()
```

## Best Practices Summary

1. **Always validate input data** before processing
2. **Use appropriate error severity levels** for different failure types
3. **Start performance monitoring early** in the application lifecycle
4. **Monitor circuit breaker status** for external dependencies
5. **Use meaningful operation names** for better tracking
6. **Regularly review performance reports** and optimize bottlenecks
7. **Implement proper error recovery strategies** for transient failures
8. **Keep validation rules updated** with changing requirements

## Next Steps

- Review the technical documentation for detailed API references
- Explore the test suite for additional usage examples
- Check the validation rules configuration for customization options
- Monitor system performance and adjust thresholds as needed

For additional support or advanced usage scenarios, please refer to the technical documentation or contact the development team.
