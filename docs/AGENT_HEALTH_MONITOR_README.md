# Agent Health Monitoring System

## Overview

The Agent Health Monitoring System is a comprehensive solution for monitoring, analyzing, and managing the health of agents within the Agent Cellphone V2 ecosystem. It provides real-time health metrics collection, automated issue detection, proactive alerting, and health recommendations.

## Features

### Core Health Monitoring
- **Real-time Health Metrics Collection**: Continuous monitoring of agent performance metrics
- **Automated Issue Detection**: Intelligent threshold-based alerting system
- **Health Scoring**: 0-100 health score calculation with intelligent algorithms
- **Proactive Recommendations**: Automated health improvement suggestions
- **Multi-metric Support**: Response time, memory usage, CPU usage, error rates, and more

### Alert Management
- **Multi-level Alerting**: Info, Warning, Critical, and Emergency severity levels
- **Smart Alert Resolution**: Automatic resolution when conditions improve
- **Alert Acknowledgment**: Team collaboration and alert tracking
- **Customizable Thresholds**: Configurable warning and critical thresholds per metric type

### Web Interface
- **Real-time Dashboard**: Live health monitoring with WebSocket updates
- **Interactive Charts**: Visual representation of health trends and status distribution
- **Alert Management**: Web-based alert acknowledgment and resolution
- **Responsive Design**: Modern Bootstrap 5 interface with mobile support

### Integration Capabilities
- **Core System Integration**: Seamless integration with agent management systems
- **Callback System**: Subscribe to health updates and notifications
- **RESTful API**: Comprehensive API for external system integration
- **WebSocket Support**: Real-time bidirectional communication

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Health Monitor                     │
├─────────────────────────────────────────────────────────────┤
│  Core Health Monitor  │  Web Interface  │  Demo System    │
│  • Metrics Collection │  • Flask App    │  • Test Suite   │
│  • Health Scoring    │  • Socket.IO     │  • Scenarios    │
│  • Alert Management  │  • REST API      │  • Validation   │
│  • Thresholds        │  • Real-time UI  │                 │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Metrics Collection**: Agents report health metrics to the monitor
2. **Health Analysis**: Metrics are analyzed against configured thresholds
3. **Alert Generation**: Alerts are created when thresholds are exceeded
4. **Health Scoring**: Overall health scores are calculated for each agent
5. **Recommendations**: Health improvement suggestions are generated
6. **Real-time Updates**: Web interface and subscribers receive live updates

### Health Metrics

| Metric Type | Description | Default Warning | Default Critical | Unit |
|-------------|-------------|-----------------|------------------|------|
| Response Time | Agent response latency | 1000ms | 5000ms | ms |
| Memory Usage | Memory consumption | 80% | 95% | % |
| CPU Usage | CPU utilization | 85% | 95% | % |
| Error Rate | Error frequency | 5% | 15% | % |
| Task Completion Rate | Success rate of tasks | 90% | 75% | % |
| Heartbeat Frequency | Agent heartbeat interval | 120s | 300s | seconds |
| Contract Success Rate | Contract completion rate | 85% | 70% | % |
| Communication Latency | Inter-agent communication delay | 500ms | 2000ms | ms |

## Installation

### Prerequisites

- Python 3.8+
- Flask 2.3.0+
- Flask-SocketIO 5.3.0+
- Flask-CORS 4.0.0+

### Dependencies

```bash
# Install web interface dependencies
pip install -r requirements_web.txt

# Or install manually
pip install Flask Flask-SocketIO Flask-CORS python-socketio python-engineio
```

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd Agent_Cellphone_V2

# Run the health monitor demo
python examples/demo_agent_health_monitor.py

# Start the web interface
python src/web/health_monitor_web.py --host 0.0.0.0 --port 5001
```

## Usage

### Core Health Monitor

#### Basic Usage

```python
from src.core.agent_health_monitor import AgentHealthMonitor, HealthMetricType

# Initialize the health monitor
monitor = AgentHealthMonitor()

# Start monitoring
monitor.start()

# Record health metrics
monitor.record_health_metric(
    agent_id="agent_001",
    metric_type=HealthMetricType.RESPONSE_TIME,
    value=500.0,
    unit="ms"
)

# Get health summary
summary = monitor.get_health_summary()
print(f"Total agents: {summary['total_agents']}")
print(f"Active alerts: {summary['active_alerts']}")

# Stop monitoring
monitor.stop()
```

#### Health Metrics Recording

```python
# Record multiple metrics for an agent
agent_id = "agent_001"

# Response time
monitor.record_health_metric(
    agent_id, HealthMetricType.RESPONSE_TIME, 1200.0, "ms"
)

# Memory usage
monitor.record_health_metric(
    agent_id, HealthMetricType.MEMORY_USAGE, 85.0, "%"
)

# CPU usage
monitor.record_health_metric(
    agent_id, HealthMetricType.CPU_USAGE, 90.0, "%"
)

# Error rate
monitor.record_health_metric(
    agent_id, HealthMetricType.ERROR_RATE, 8.0, "%"
)
```

#### Alert Management

```python
# Get all active alerts
alerts = monitor.get_health_alerts()

# Filter alerts by severity
critical_alerts = monitor.get_health_alerts(severity="critical")
warning_alerts = monitor.get_health_alerts(severity="warning")

# Filter alerts by agent
agent_alerts = monitor.get_health_alerts(agent_id="agent_001")

# Acknowledge an alert
if alerts:
    monitor.acknowledge_alert(alerts[0].alert_id)

# Resolve an alert
if alerts:
    monitor.resolve_alert(alerts[0].alert_id)
```

#### Health Subscriptions

```python
def health_update_callback(health_data, alerts):
    print(f"Health update: {len(health_data)} agents, {len(alerts)} alerts")
    
    # Process health data
    for agent_id, health in health_data.items():
        print(f"{agent_id}: {health.overall_status.value} (Score: {health.health_score})")

# Subscribe to health updates
monitor.subscribe_to_health_updates(health_update_callback)

# Unsubscribe when done
monitor.unsubscribe_from_health_updates(health_update_callback)
```

#### Custom Thresholds

```python
# Set custom thresholds for response time
monitor.set_health_threshold(
    HealthMetricType.RESPONSE_TIME,
    warning_threshold=800.0,    # 800ms
    critical_threshold=3000.0,  # 3 seconds
    unit="ms",
    description="Custom response time threshold for high-performance agents"
)
```

### Web Interface

#### Starting the Web Interface

```python
from src.web.health_monitor_web import HealthMonitorWebInterface

# Initialize with health monitor
web_interface = HealthMonitorWebInterface(
    health_monitor=monitor,
    config={
        'debug': False,
        'secret_key': 'your-secret-key',
        'update_interval': 5
    }
)

# Start the interface
web_interface.start()

# Run the Flask app
web_interface.run(host='0.0.0.0', port=5001)
```

#### API Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Main health dashboard | HTML dashboard |
| `/api/health/summary` | GET | Health summary data | JSON summary |
| `/api/health/agents` | GET | All agent health data | JSON agents |
| `/api/health/alerts` | GET | Health alerts | JSON alerts |
| `/api/health/alerts/{id}/acknowledge` | POST | Acknowledge alert | JSON result |
| `/api/health/alerts/{id}/resolve` | POST | Resolve alert | JSON result |
| `/api/health/metrics/{agent_id}` | GET | Agent-specific metrics | JSON metrics |
| `/api/health/thresholds` | GET | Health thresholds | JSON thresholds |
| `/api/health/status` | GET | Monitoring status | JSON status |

#### WebSocket Events

| Event | Direction | Description | Data |
|-------|-----------|-------------|------|
| `connect` | Client → Server | Client connection | Connection data |
| `disconnect` | Client → Server | Client disconnection | Disconnect data |
| `subscribe_to_health_updates` | Client → Server | Subscribe to updates | Subscription data |
| `request_health_update` | Client → Server | Request manual update | Request data |
| `health_update` | Server → Client | Health data update | Health data |
| `periodic_update` | Server → Client | Periodic health update | Health summary |
| `error` | Server → Client | Error notification | Error data |

### Demo System

#### Running the Demo

```bash
# Run comprehensive demo
python examples/demo_agent_health_monitor.py

# Run realistic scenario
python examples/demo_agent_health_monitor.py --scenario

# Run quick tests only
python examples/demo_agent_health_monitor.py --quick
```

#### Demo Features

1. **Core Health Monitoring Test**: Basic functionality validation
2. **Health Metrics Collection Test**: Metrics recording and retrieval
3. **Alert Management Test**: Alert generation and management
4. **Health Scoring Test**: Score calculation and recommendations
5. **Real-time Monitoring Test**: Callback system validation
6. **Web Interface Test**: Web interface functionality
7. **Performance Test**: Load testing and performance validation
8. **Integration Test**: Core system integration validation

## Configuration

### Health Monitor Configuration

```python
config = {
    'metrics_interval': 30,        # Metrics collection interval (seconds)
    'health_check_interval': 60,   # Health check interval (seconds)
    'alert_check_interval': 15,    # Alert check interval (seconds)
}

monitor = AgentHealthMonitor(config=config)
```

### Web Interface Configuration

```python
config = {
    'secret_key': 'your-secret-key-here',
    'debug': False,
    'update_interval': 5,          # Update interval (seconds)
    'host': '0.0.0.0',
    'port': 5001
}

web_interface = HealthMonitorWebInterface(
    health_monitor=monitor,
    config=config
)
```

### Environment Variables

```bash
# Health Monitor
HEALTH_MONITOR_DEBUG=true
HEALTH_MONITOR_METRICS_INTERVAL=30
HEALTH_MONITOR_HEALTH_CHECK_INTERVAL=60

# Web Interface
HEALTH_WEB_SECRET_KEY=your-secret-key
HEALTH_WEB_DEBUG=false
HEALTH_WEB_PORT=5001
```

## Health Scoring Algorithm

### Score Calculation

The health score (0-100) is calculated using a sophisticated algorithm:

1. **Metric Scoring**: Each metric is scored based on threshold proximity
   - Below warning threshold: 100 points
   - Between warning and critical: Linear interpolation (100-75 points)
   - Above critical threshold: Exponential penalty (75-0 points)

2. **Alert Penalties**: Active alerts reduce the score
   - Critical alerts: -20 points each
   - Warning alerts: -10 points each

3. **Final Score**: Average metric score minus alert penalties, clamped to 0-100

### Status Determination

| Health Score | Status | Description |
|--------------|--------|-------------|
| 90-100 | Excellent | Optimal performance |
| 75-89 | Good | Good performance with minor issues |
| 50-74 | Warning | Performance issues requiring attention |
| 25-49 | Critical | Serious issues requiring immediate action |
| 0-24 | Offline | Agent unavailable or severely degraded |

## Alert System

### Alert Severity Levels

1. **Info**: Informational messages, no action required
2. **Warning**: Performance degradation, monitor closely
3. **Critical**: Serious issues, immediate attention required
4. **Emergency**: System failure, urgent intervention needed

### Alert Lifecycle

1. **Detection**: Metric exceeds threshold
2. **Generation**: Alert created with severity and details
3. **Notification**: Alert sent to subscribers and web interface
4. **Acknowledgment**: Team member acknowledges the alert
5. **Resolution**: Issue resolved or alert manually resolved
6. **Auto-resolution**: Alert automatically resolved when conditions improve

### Alert Management

- **Automatic Resolution**: Alerts resolve when metrics return to normal
- **Manual Resolution**: Team members can manually resolve alerts
- **Acknowledgment Tracking**: Track who has seen and acknowledged alerts
- **Alert History**: Maintain alert history for analysis and reporting

## Integration

### Core Agent Management Systems

```python
# Integration with AgentManager
from src.core.agent_manager import AgentManager
from src.core.agent_health_monitor import AgentHealthMonitor

agent_manager = AgentManager()
health_monitor = AgentHealthMonitor()

# Subscribe to agent status changes
def on_agent_status_change(agent_id, status):
    # Record health metrics based on status
    if status == "active":
        health_monitor.record_health_metric(
            agent_id, "heartbeat_frequency", 0, "seconds"
        )

agent_manager.subscribe_to_status_changes(on_agent_status_change)
```

### Message Router Integration

```python
# Integration with MessageRouter
from src.core.message_router import MessageRouter

message_router = MessageRouter()

# Monitor communication latency
def on_message_sent(message):
    start_time = time.time()
    
    def on_message_delivered(delivery_result):
        latency = (time.time() - start_time) * 1000  # Convert to ms
        health_monitor.record_health_metric(
            message.sender_id,
            "communication_latency",
            latency,
            "ms"
        )
    
    message_router.on_delivery(message.message_id, on_message_delivered)
```

### Performance Tracker Integration

```python
# Integration with PerformanceTracker
from src.core.performance_tracker import PerformanceTracker

performance_tracker = PerformanceTracker()

# Record performance metrics as health metrics
def on_performance_metric(metric):
    health_monitor.record_health_metric(
        metric.agent_id,
        "task_completion_rate",
        metric.value,
        "%"
    )

performance_tracker.subscribe_to_metrics(on_performance_metric)
```

## Testing

### Smoke Tests

```python
# Test core functionality
monitor = AgentHealthMonitor()
success = monitor.run_smoke_test()
assert success, "Smoke test failed"

# Test web interface
web_interface = HealthMonitorWebInterface()
success = web_interface.run_smoke_test()
assert success, "Web interface smoke test failed"
```

### Comprehensive Testing

```python
# Run full test suite
demo = AgentHealthMonitorDemo()
demo.run_comprehensive_demo()
```

### Performance Testing

```python
# Test under load
demo = AgentHealthMonitorDemo()
demo._test_performance_under_load()
```

## Monitoring and Maintenance

### Health Check Monitoring

- **System Health**: Monitor the health monitor itself
- **Performance Metrics**: Track response times and throughput
- **Resource Usage**: Monitor memory and CPU consumption
- **Alert Volume**: Track alert generation rates

### Maintenance Tasks

- **Threshold Review**: Regularly review and adjust health thresholds
- **Alert Tuning**: Fine-tune alert sensitivity to reduce false positives
- **Performance Optimization**: Optimize monitoring intervals and algorithms
- **Data Cleanup**: Clean up old health data and resolved alerts

### Troubleshooting

#### Common Issues

1. **High Alert Volume**
   - Review threshold settings
   - Check for metric anomalies
   - Adjust monitoring intervals

2. **Performance Degradation**
   - Reduce monitoring frequency
   - Optimize health scoring algorithms
   - Check resource usage

3. **Web Interface Issues**
   - Verify Flask and Socket.IO versions
   - Check network connectivity
   - Review error logs

#### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable web interface debug mode
web_interface = HealthMonitorWebInterface(config={'debug': True})
```

## Security

### Access Control

- **API Authentication**: Implement authentication for API endpoints
- **Web Interface Security**: Secure web interface access
- **Data Encryption**: Encrypt sensitive health data
- **Audit Logging**: Log all health monitoring activities

### Best Practices

- **Secure Configuration**: Use environment variables for sensitive data
- **Input Validation**: Validate all metric inputs
- **Rate Limiting**: Implement rate limiting for API endpoints
- **Regular Updates**: Keep dependencies updated

## Performance

### Optimization Strategies

1. **Asynchronous Processing**: Use async/await for I/O operations
2. **Batch Processing**: Process metrics in batches
3. **Caching**: Cache frequently accessed health data
4. **Connection Pooling**: Reuse database connections

### Scaling Considerations

- **Horizontal Scaling**: Deploy multiple health monitor instances
- **Load Balancing**: Distribute monitoring load across instances
- **Database Scaling**: Use scalable database solutions
- **Message Queues**: Implement message queues for high-volume scenarios

## Roadmap

### Future Enhancements

1. **Machine Learning Integration**: AI-powered health prediction
2. **Advanced Analytics**: Deep health trend analysis
3. **Mobile Application**: Mobile health monitoring app
4. **Integration APIs**: Third-party system integration
5. **Advanced Reporting**: Comprehensive health reports and dashboards

### Planned Features

- **Predictive Health**: Predict potential health issues
- **Automated Remediation**: Automatic issue resolution
- **Health Forecasting**: Long-term health trend prediction
- **Advanced Notifications**: Multi-channel alert delivery

## Support

### Documentation

- **API Reference**: Complete API documentation
- **User Guide**: Step-by-step usage instructions
- **Developer Guide**: Integration and development guide
- **FAQ**: Frequently asked questions

### Community

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Community discussions and support
- **Contributions**: Guidelines for contributing to the project

### Contact

- **Maintainer**: Agent-1
- **Repository**: [GitHub Repository URL]
- **Issues**: [GitHub Issues URL]

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Agent Cellphone V2 Team**: Core system development
- **Flask Community**: Web framework and extensions
- **Bootstrap Team**: Modern UI components
- **Chart.js Team**: Data visualization library

---

*Last updated: December 2024*
*Version: 1.0.0*
