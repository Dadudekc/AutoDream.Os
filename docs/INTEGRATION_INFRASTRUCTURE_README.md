# Integration Infrastructure Documentation

## Overview

The Integration Infrastructure for Agent_Cellphone_V2_Repository provides a comprehensive foundation for building scalable, maintainable, and performant integration systems. This infrastructure follows modern software engineering principles including Test-Driven Development (TDD), dependency injection, and event-driven architecture.

## Architecture

The integration infrastructure consists of five core components:

1. **API Manager** - Handles HTTP API endpoints, middleware, and request routing
2. **Middleware Orchestrator** - Manages data flow through middleware components
3. **Service Registry** - Provides service discovery and health monitoring
4. **Configuration Manager** - Manages configuration values and validation
5. **Integration Coordinator** - Orchestrates all components and provides unified interface

## Quick Start

### Installation

1. Install the required dependencies:
```bash
pip install -r requirements_integration.txt
```

2. Run the smoke tests to verify installation:
```bash
python tests/smoke/test_integration_smoke.py
```

### Basic Usage

```python
import asyncio
from src.services.integration_coordinator import IntegrationCoordinator

async def main():
    # Create and start the integration coordinator
    coordinator = IntegrationCoordinator("config")
    await coordinator.start()

    # Your integration logic here

    # Stop the coordinator
    await coordinator.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## Component Details

### 1. API Manager

The API Manager provides a flexible HTTP API framework with middleware support.

#### Features
- RESTful API endpoint management
- Middleware pipeline for request/response processing
- Built-in authentication and rate limiting
- Service dependency injection
- Request/response logging

#### Example Usage

```python
from src.services.api_manager import APIManager, APIEndpoint, APIMethod

# Create API manager
api_manager = APIManager()

# Define API endpoint
async def user_handler(request, context):
    return {
        'status_code': 200,
        'data': {'message': 'Hello, User!'}
    }

# Register endpoint
endpoint = APIEndpoint(
    path="/api/users",
    method=APIMethod.GET,
    handler=user_handler,
    description="Get user information"
)
api_manager.add_endpoint(endpoint)

# Start the manager
await api_manager.start()
```

#### Built-in Middleware

- **LoggingMiddleware**: Logs all requests and responses
- **RateLimitMiddleware**: Implements rate limiting per client
- **AuthenticationMiddleware**: Handles API key authentication

### 2. Middleware Orchestrator

The Middleware Orchestrator manages data flow through configurable middleware chains.

#### Features
- Configurable middleware chains
- Priority-based processing
- Conditional middleware execution
- Performance metrics collection
- Error handling and recovery

#### Example Usage

```python
from src.services.middleware_orchestrator import (
    MiddlewareOrchestrator,
    DataTransformationMiddleware,
    ValidationMiddleware
)

# Create orchestrator
orchestrator = MiddlewareOrchestrator()

# Register middleware components
transformer = DataTransformationMiddleware({
    'transformations': {
        'json': 'json_to_dict',
        'string': 'string_uppercase'
    }
})
orchestrator.register_middleware(transformer)

# Create middleware chain
chain = MiddlewareChain(
    name="data_processing",
    middleware_list=["DataTransformationMiddleware"],
    description="Process incoming data"
)
orchestrator.create_chain(chain)

# Process data packets
data_packet = DataPacket(
    id="packet-1",
    data='{"message": "hello world"}',
    tags={"json", "string"}
)

result = await orchestrator.process_data_packet(data_packet)
```

#### Built-in Middleware Types

- **DataTransformationMiddleware**: Transforms data formats
- **ValidationMiddleware**: Validates data against rules
- **RoutingMiddleware**: Routes data to appropriate destinations

### 3. Service Registry

The Service Registry provides service discovery and health monitoring capabilities.

#### Features
- Service registration and discovery
- Health check strategies (HTTP, TCP, Custom)
- Service metadata and capabilities
- Automatic health monitoring
- Event callbacks for service lifecycle

#### Example Usage

```python
from src.services.service_registry import (
    ServiceRegistry, ServiceInfo, ServiceType, ServiceMetadata, ServiceEndpoint
)

# Create registry
registry = ServiceRegistry()

# Define service
service = ServiceInfo(
    id="user-api",
    name="user-api",
    service_type=ServiceType.API,
    endpoints=[
        ServiceEndpoint(
            host="localhost",
            port=8001,
            health_check_path="/health"
        )
    ],
    metadata=ServiceMetadata(
        version="1.0.0",
        description="User management API",
        tags={"user", "management"},
        capabilities={"create", "read", "update", "delete"}
    )
)

# Register service
registry.register_service(service)

# Start registry
await registry.start()

# Find services
api_services = registry.find_services(service_type=ServiceType.API)
healthy_services = registry.get_healthy_services()
```

#### Health Check Strategies

- **HTTPHealthCheck**: Checks HTTP endpoints
- **TCPHealthCheck**: Checks TCP connections
- **CustomHealthCheck**: Custom health check functions

### 4. Configuration Manager

The Configuration Manager handles configuration values with validation and hot-reloading.

#### Features
- Multiple configuration sources (environment, files, API)
- Configuration validation rules
- Hot-reloading of configuration files
- Hierarchical configuration structure
- Change event callbacks

#### Example Usage

```python
from src.services.integration_config_manager import (
    IntegrationConfigManager, ConfigSource, ConfigScope
)

# Create config manager
config_manager = IntegrationConfigManager("config")

# Add validation rules
config_manager.add_validation_rules('api.port', {
    'type': 'integer',
    'range': {'min': 1, 'max': 65535}
})

# Set configuration values
config_manager.set_config_value(
    'api.host',
    'localhost',
    ConfigSource.FILE,
    ConfigScope.GLOBAL,
    'API server hostname'
)

# Get configuration values
host = config_manager.get_config_value('api.host')
port = config_manager.get_config_value('api.port', 8000)  # with default

# Get configuration sections
api_config = config_manager.get_config_section('api')

# Start file watching
config_manager.start_file_watching()
```

#### Configuration File Formats

- YAML (.yaml, .yml)
- JSON (.json)
- INI (.ini)

#### Built-in Validators

- **TypeValidator**: Validates data types
- **RangeValidator**: Validates numeric ranges
- **RequiredValidator**: Ensures required fields
- **PatternValidator**: Validates against regex patterns

### 5. Integration Coordinator

The Integration Coordinator orchestrates all components and provides a unified interface.

#### Features
- Component lifecycle management
- Unified API for all components
- System health monitoring
- Performance metrics collection
- Graceful shutdown handling

#### Example Usage

```python
from src.services.integration_coordinator import IntegrationCoordinator

# Create coordinator
coordinator = IntegrationCoordinator("config")

# Add event callbacks
def on_status_change(old_status, new_status):
    print(f"Status changed: {old_status.value} -> {new_status.value}")

def on_error(context, error):
    print(f"Error in {context}: {str(error)}")

coordinator.add_status_change_callback(on_status_change)
coordinator.add_error_callback(on_error)

# Start the system
await coordinator.start()

# Check system health
health = coordinator.get_system_health()
print(f"System healthy: {health['healthy']}")

# Get system metrics
metrics = coordinator.get_system_metrics()
print(f"Uptime: {metrics['coordinator']['uptime_seconds']} seconds")

# Process API requests
response = await coordinator.process_api_request({
    'path': '/api/health',
    'method': 'GET',
    'headers': {},
    'client_id': 'client-1'
})

# Stop the system
await coordinator.stop()
```

## Configuration

### Environment Variables

Set these environment variables to configure the system:

```bash
# Configuration prefix
export AGENT_CELLPHONE_CONFIG_PREFIX=AGENT_CELLPHONE_

# API configuration
export AGENT_CELLPHONE_API_HOST=0.0.0.0
export AGENT_CELLPHONE_API_PORT=8000
export AGENT_CELLPHONE_API_DEBUG=true

# Database configuration
export AGENT_CELLPHONE_DATABASE_HOST=localhost
export AGENT_CELLPHONE_DATABASE_PORT=5432
export AGENT_CELLPHONE_DATABASE_NAME=agent_cellphone

# Logging configuration
export AGENT_CELLPHONE_LOGGING_LEVEL=INFO
```

### Configuration Files

Create configuration files in the `config` directory:

```yaml
# config/api.yaml
api:
  host: localhost
  port: 8000
  debug: false
  timeout: 30

# config/database.yaml
database:
  host: localhost
  port: 5432
  name: agent_cellphone
  pool_size: 10

# config/middleware.yaml
middleware:
  enabled: true
  timeout: 60
  rate_limit: 100
```

## Testing

### Running Tests

1. **Unit Tests**: Test individual components
```bash
pytest tests/test_integration_infrastructure.py -v
```

2. **Smoke Tests**: Quick verification of basic functionality
```bash
python tests/smoke/test_integration_smoke.py
```

3. **Coverage Report**: Generate test coverage report
```bash
pytest tests/test_integration_infrastructure.py --cov=src --cov-report=html
```

### Test Structure

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Smoke Tests**: Quick verification of basic functionality
- **Performance Tests**: Test system performance under load

## Performance Monitoring

### Built-in Metrics

The system provides comprehensive performance metrics:

- **API Manager**: Request count, response times, error rates
- **Middleware Orchestrator**: Packet processing rates, chain performance
- **Service Registry**: Service health, discovery performance
- **Configuration Manager**: Configuration load times, validation performance

### Accessing Metrics

```python
# Get system-wide metrics
metrics = coordinator.get_system_metrics()

# Get component-specific metrics
api_metrics = coordinator.api_manager.get_endpoints_summary()
middleware_metrics = coordinator.middleware_orchestrator.get_performance_metrics()
registry_metrics = coordinator.service_registry.get_registry_summary()
```

### Health Monitoring

```python
# Check system health
health = coordinator.get_system_health()

if health['healthy']:
    print("System is healthy")
else:
    print("System has issues:")
    for component, status in health['components'].items():
        if not status['healthy']:
            print(f"  - {component}: {status}")
```

## Error Handling

### Error Callbacks

Register callbacks to handle errors:

```python
def error_handler(context, error):
    logger.error(f"Error in {context}: {str(error)}")
    # Send alerts, log to external systems, etc.

coordinator.add_error_callback(error_handler)
```

### Graceful Degradation

The system is designed to continue operating even when individual components fail:

- Failed middleware components are skipped
- Unhealthy services are marked but don't stop the system
- Configuration errors fall back to defaults
- API endpoints return appropriate error responses

## Best Practices

### 1. Component Design

- Keep components focused on single responsibilities
- Use dependency injection for loose coupling
- Implement proper error handling and logging
- Follow async/await patterns consistently

### 2. Configuration Management

- Use environment variables for sensitive data
- Validate configuration values at startup
- Provide sensible defaults for all settings
- Use configuration files for complex settings

### 3. Testing

- Write tests for all components
- Use mocks for external dependencies
- Test error conditions and edge cases
- Maintain high test coverage

### 4. Monitoring

- Monitor system health continuously
- Track performance metrics
- Set up alerts for critical failures
- Log all important events

### 5. Security

- Validate all inputs
- Use authentication for sensitive endpoints
- Implement rate limiting
- Log security-related events

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Configuration Errors**: Check configuration file syntax and validation rules
3. **Service Registration Failures**: Verify service endpoints are accessible
4. **Performance Issues**: Monitor metrics and adjust configuration

### Debug Mode

Enable debug mode for detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Health Checks

Use the built-in health endpoints to diagnose issues:

```bash
# Check system health
curl http://localhost:8000/api/health

# Get system metrics
curl http://localhost:8000/api/metrics

# Check configuration
curl http://localhost:8000/api/config

# Check services
curl http://localhost:8000/api/services
```

## Contributing

### Development Setup

1. Clone the repository
2. Install development dependencies
3. Run tests to verify setup
4. Make changes following the coding standards
5. Add tests for new functionality
6. Submit pull request

### Coding Standards

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Maintain test coverage above 90%
- Use async/await for I/O operations

## License

This integration infrastructure is part of the Agent_Cellphone_V2_Repository project and follows the same licensing terms.

## Support

For questions and support:

1. Check the documentation
2. Review the test examples
3. Check existing issues
4. Create a new issue with detailed information

---

**Note**: This infrastructure is designed to be production-ready but should be thoroughly tested in your specific environment before deployment.
