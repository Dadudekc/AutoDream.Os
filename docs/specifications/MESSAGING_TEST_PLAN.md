# 🧪 Messaging System Test Plan

**Comprehensive Testing Strategy for Enhanced Messaging Components**

---

## **📋 TEST PLAN OVERVIEW**

### **Test Objectives**
- Validate adaptive timing engine accuracy and performance
- Verify resilient error handling and recovery mechanisms
- Confirm comprehensive flag validation prevents invalid operations
- Ensure intelligent agent ordering works correctly
- Validate parallel delivery system stability
- Confirm observability and monitoring accuracy

### **Test Coverage Goals**
- **Unit Tests**: ≥ 85% coverage for all new components
- **Integration Tests**: End-to-end workflow validation
- **Load Tests**: Performance under stress conditions
- **Chaos Tests**: Failure scenario simulation

### **Test Environment Requirements**
- 8 agent swarm simulation environment
- Performance benchmarking hardware
- Network latency simulation tools
- GUI automation test framework
- Load testing infrastructure

---

## **🎯 UNIT TEST SPECIFICATIONS**

### **1. Adaptive Timing Engine Tests**

#### **Performance Detection Tests**
```python
# test_timing_engine_performance_detection.py

def test_cpu_speed_detection():
    """Verify CPU performance detection accuracy."""
    engine = AdaptiveTimingEngine()
    metrics = engine.detect_performance()

    assert metrics.cpu_speed > 0
    assert isinstance(metrics.cpu_speed, float)
    assert 0.5 <= metrics.cpu_speed <= 10.0  # Reasonable CPU score range

def test_memory_detection():
    """Verify memory availability detection."""
    engine = AdaptiveTimingEngine()
    metrics = engine.detect_performance()

    assert metrics.memory_mb > 0
    assert isinstance(metrics.memory_mb, int)
    assert metrics.memory_mb >= 1024  # Minimum 1GB

def test_network_latency_detection():
    """Verify network latency measurement."""
    engine = AdaptiveTimingEngine()
    metrics = engine.detect_performance()

    assert metrics.network_latency_ms >= 0
    assert isinstance(metrics.network_latency_ms, float)
    assert metrics.network_latency_ms <= 1000  # Maximum 1 second
```

#### **Delay Calculation Tests**
```python
# test_timing_engine_calculations.py

def test_typing_interval_calculation():
    """Verify typing interval calculation based on performance."""
    engine = AdaptiveTimingEngine()

    # High performance system
    high_perf = PerformanceMetrics(cpu_speed=5.0, memory_mb=16384)
    interval = engine.calculate_typing_interval(high_perf)
    assert 0.005 <= interval <= 0.015

    # Low performance system
    low_perf = PerformanceMetrics(cpu_speed=1.0, memory_mb=2048)
    interval = engine.calculate_typing_interval(low_perf)
    assert 0.02 <= interval <= 0.05

def test_gui_focus_delay_calculation():
    """Verify GUI focus delay calculation."""
    engine = AdaptiveTimingEngine()

    fast_system = PerformanceMetrics(gui_response_time_ms=200)
    delay = engine.calculate_gui_focus_delay(fast_system)
    assert delay <= 0.5

    slow_system = PerformanceMetrics(gui_response_time_ms=800)
    delay = engine.calculate_gui_focus_delay(slow_system)
    assert delay >= 1.0
```

### **2. Error Handling & Retry Tests**

#### **Retry Logic Tests**
```python
# test_retry_engine.py

def test_successful_delivery_no_retry():
    """Verify no retry on successful delivery."""
    retry_engine = RetryEngine()
    mock_delivery = Mock(return_value=True)

    result = retry_engine.execute_with_retry(mock_delivery)
    assert result is True
    assert mock_delivery.call_count == 1

def test_retry_on_failure():
    """Verify retry on delivery failure."""
    retry_engine = RetryEngine(max_retries=3)
    mock_delivery = Mock(side_effect=[False, False, True])

    result = retry_engine.execute_with_retry(mock_delivery)
    assert result is True
    assert mock_delivery.call_count == 3

def test_max_retries_exceeded():
    """Verify proper handling when max retries exceeded."""
    retry_engine = RetryEngine(max_retries=2)
    mock_delivery = Mock(return_value=False)

    with pytest.raises(MaxRetriesExceededError):
        retry_engine.execute_with_retry(mock_delivery)

    assert mock_delivery.call_count == 3  # Initial + 2 retries
```

#### **Exponential Backoff Tests**
```python
# test_exponential_backoff.py

def test_backoff_delays():
    """Verify exponential backoff timing."""
    backoff = ExponentialBackoff(base_delay=1.0, multiplier=2.0)

    delays = []
    for attempt in range(4):
        delay = backoff.calculate_delay(attempt)
        delays.append(delay)

    expected = [1.0, 2.0, 4.0, 8.0]  # 1 * 2^(attempt)
    assert delays == expected

def test_backoff_with_jitter():
    """Verify jitter prevents thundering herd."""
    backoff = ExponentialBackoff(base_delay=1.0, jitter=True)

    delays = []
    for _ in range(10):
        delay = backoff.calculate_delay(1)
        delays.append(delay)

    # All delays should be different due to jitter
    assert len(set(delays)) == len(delays)
    # All should be within reasonable bounds
    assert all(1.0 <= d <= 3.0 for d in delays)
```

### **3. Flag Validation Tests**

#### **CLI Flag Validation Tests**
```python
# test_flag_validation.py

def test_mutually_exclusive_flags():
    """Verify --bulk and --agent cannot be used together."""
    parser = create_parser()

    # Should fail with both flags
    with pytest.raises(SystemExit):
        args = parser.parse_args(['--bulk', '--agent', 'Agent-1', '--message', 'test'])

    # Should succeed with only one
    args = parser.parse_args(['--bulk', '--message', 'test'])
    assert args.bulk is True
    assert args.agent is None

def test_required_flags():
    """Verify required flags are enforced."""
    parser = create_parser()

    # Should fail without --message
    with pytest.raises(SystemExit):
        args = parser.parse_args(['--agent', 'Agent-1'])

    # Should succeed with --message
    args = parser.parse_args(['--agent', 'Agent-1', '--message', 'test'])
    assert args.message == 'test'

def test_get_next_task_requires_agent():
    """Verify --get-next-task requires --agent."""
    parser = create_parser()

    # Should fail without --agent
    with pytest.raises(SystemExit):
        args = parser.parse_args(['--get-next-task'])

    # Should succeed with --agent
    args = parser.parse_args(['--agent', 'Agent-7', '--get-next-task'])
    assert args.agent == 'Agent-7'
    assert args.get_next_task is True
```

#### **Priority Override Tests**
```python
# test_priority_override.py

def test_high_priority_override():
    """Verify --high-priority overrides --priority."""
    parser = create_parser()

    # --high-priority should force urgent regardless of --priority
    args = parser.parse_args([
        '--message', 'test',
        '--priority', 'normal',
        '--high-priority'
    ])

    assert args.high_priority is True
    # Priority should be normalized to urgent in processing logic
    processor = MessageProcessor()
    priority = processor.resolve_priority(args)
    assert priority == UnifiedMessagePriority.URGENT
```

### **4. Agent Ordering Tests**

#### **Priority-Based Ordering Tests**
```python
# test_agent_ordering.py

def test_urgent_message_ordering():
    """Verify urgent messages prioritize Captain Agent-4."""
    ordering_engine = AgentOrderingEngine()

    urgent_message = create_message(priority=UnifiedMessagePriority.URGENT)
    order = ordering_engine.calculate_order(urgent_message)

    # Agent-4 should be first for urgent messages
    assert order[0] == 'Agent-4'

def test_normal_message_ordering():
    """Verify normal messages maintain standard order."""
    ordering_engine = AgentOrderingEngine()

    normal_message = create_message(priority=UnifiedMessagePriority.NORMAL)
    order = ordering_engine.calculate_order(normal_message)

    # Standard order for normal messages
    expected_order = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-5',
                     'Agent-6', 'Agent-7', 'Agent-8', 'Agent-4']
    assert order == expected_order

def test_custom_ordering():
    """Verify custom ordering override works."""
    ordering_engine = AgentOrderingEngine()

    custom_order = ['Agent-7', 'Agent-1', 'Agent-4']
    ordering_engine.set_custom_order(custom_order)

    order = ordering_engine.calculate_order()
    assert order[:3] == custom_order
```

---

## **🔗 INTEGRATION TEST SPECIFICATIONS**

### **1. End-to-End Message Delivery**

#### **PyAutoGUI Mode Integration Test**
```python
# test_e2e_pyautogui_delivery.py

@pytest.mark.integration
def test_complete_message_delivery_pyautogui():
    """Test complete message delivery workflow via PyAutoGUI."""
    # Setup
    messaging_service = UnifiedMessagingCore()
    test_message = UnifiedMessage(
        content="Integration test message",
        sender="Test Agent",
        recipient="Agent-1",
        message_type=UnifiedMessageType.TEXT,
        priority=UnifiedMessagePriority.NORMAL
    )

    # Execute delivery
    start_time = time.time()
    result = messaging_service.send_message_via_pyautogui(test_message)
    end_time = time.time()

    # Verify delivery
    assert result is True
    delivery_time = end_time - start_time
    assert delivery_time <= 5.0  # Should complete within 5 seconds

    # Verify message appears in agent inbox
    inbox_path = "agent_workspaces/Agent-1/inbox"
    message_files = list(Path(inbox_path).glob("CAPTAIN_MESSAGE_*.md"))
    assert len(message_files) >= 1

    # Verify message content
    latest_message = max(message_files, key=lambda p: p.stat().st_mtime)
    content = latest_message.read_text()
    assert "Integration test message" in content
    assert "Test Agent" in content
```

#### **Inbox Mode Integration Test**
```python
# test_e2e_inbox_delivery.py

@pytest.mark.integration
def test_complete_message_delivery_inbox():
    """Test complete message delivery workflow via inbox."""
    messaging_service = UnifiedMessagingCore()
    test_message = UnifiedMessage(
        content="Inbox integration test",
        sender="Test Agent",
        recipient="Agent-2",
        message_type=UnifiedMessageType.TEXT,
        priority=UnifiedMessagePriority.NORMAL
    )

    # Execute delivery
    result = messaging_service.send_message_to_inbox(test_message)

    # Verify delivery
    assert result is True

    # Verify file creation
    inbox_path = Path("agent_workspaces/Agent-2/inbox")
    message_files = list(inbox_path.glob("CAPTAIN_MESSAGE_*.md"))
    assert len(message_files) >= 1

    # Verify message format
    latest_message = max(message_files, key=lambda p: p.stat().st_mtime)
    content = latest_message.read_text()

    # Check required headers
    assert "# 🚨 CAPTAIN MESSAGE - TEXT" in content
    assert "**From**: Test Agent" in content
    assert "**To**: Agent-2" in content
    assert "**Priority**: normal" in content
    assert "Inbox integration test" in content
```

### **2. Bulk Operations Integration Test**

```python
# test_bulk_operations.py

@pytest.mark.integration
def test_bulk_message_delivery():
    """Test bulk message delivery to all agents."""
    messaging_service = UnifiedMessagingCore()
    test_content = "Bulk integration test message"

    # Send to all agents
    results = messaging_service.send_to_all_agents(
        content=test_content,
        sender="Test Agent",
        message_type=UnifiedMessageType.BROADCAST,
        priority=UnifiedMessagePriority.NORMAL
    )

    # Verify all deliveries succeeded
    assert all(results)

    # Verify Agent-4 was processed last
    agent_order = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-5',
                   'Agent-6', 'Agent-7', 'Agent-8', 'Agent-4']

    # Check timestamps to verify order
    message_timestamps = {}
    for agent_id in agent_order:
        inbox_path = Path(f"agent_workspaces/{agent_id}/inbox")
        message_files = list(inbox_path.glob("CAPTAIN_MESSAGE_*.md"))
        if message_files:
            latest = max(message_files, key=lambda p: p.stat().st_mtime)
            message_timestamps[agent_id] = latest.stat().st_mtime

    # Verify Agent-4 has the latest timestamp (processed last)
    if 'Agent-4' in message_timestamps:
        agent_4_time = message_timestamps['Agent-4']
        for agent_id, timestamp in message_timestamps.items():
            if agent_id != 'Agent-4':
                assert timestamp <= agent_4_time
```

---

## **🔥 LOAD TEST SPECIFICATIONS**

### **1. Concurrent Delivery Load Test**

```python
# test_load_concurrent_deliveries.py

@pytest.mark.load
def test_concurrent_delivery_capacity():
    """Test system capacity under concurrent delivery load."""
    messaging_service = UnifiedMessagingCore()

    # Generate multiple messages
    messages = []
    for i in range(50):  # Test with 50 concurrent messages
        message = UnifiedMessage(
            content=f"Load test message {i}",
            sender="Load Test Agent",
            recipient=f"Agent-{(i % 8) + 1}",  # Distribute across 8 agents
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.NORMAL
        )
        messages.append(message)

    # Execute concurrent deliveries
    start_time = time.time()

    # Use thread pool for concurrent execution
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(messaging_service.send_message_via_pyautogui, msg)
                  for msg in messages]
        results = [future.result() for future in futures]

    end_time = time.time()

    # Verify performance
    total_time = end_time - start_time
    success_rate = sum(results) / len(results)

    # Performance requirements
    assert success_rate >= 0.95  # 95% success rate
    assert total_time <= 120.0   # Complete within 2 minutes
    assert total_time / len(messages) <= 3.0  # Average < 3s per message

    # Verify no GUI conflicts (check for error patterns)
    error_logs = get_recent_error_logs()
    gui_conflicts = [log for log in error_logs if 'gui_conflict' in log.lower()]
    assert len(gui_conflicts) == 0
```

### **2. Memory and Resource Usage Test**

```python
# test_load_resource_usage.py

@pytest.mark.load
def test_memory_usage_under_load():
    """Test memory usage patterns under sustained load."""
    import psutil
    import tracemalloc

    # Start memory tracing
    tracemalloc.start()
    process = psutil.Process()

    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    # Generate sustained load
    messaging_service = UnifiedMessagingCore()

    for batch in range(10):  # 10 batches
        messages = []
        for i in range(20):  # 20 messages per batch
            message = UnifiedMessage(
                content=f"Memory test message {batch}-{i}",
                sender="Memory Test Agent",
                recipient=f"Agent-{(i % 8) + 1}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.NORMAL
            )
            messages.append(message)

        # Send batch
        for msg in messages:
            messaging_service.send_message_via_pyautogui(msg)

        # Small delay between batches
        time.sleep(1)

    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory

    # Verify memory usage stays within bounds
    assert memory_increase <= 100  # Max 100MB increase

    # Check for memory leaks
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    assert peak / 1024 / 1024 <= 200  # Peak memory < 200MB
    assert current / 1024 / 1024 <= 50  # Current memory < 50MB after cleanup
```

---

## **🎭 CHAOS TEST SPECIFICATIONS**

### **1. Network Failure Simulation**

```python
# test_chaos_network_failure.py

@pytest.mark.chaos
def test_network_failure_recovery():
    """Test system behavior during network failures."""
    messaging_service = UnifiedMessagingCore()

    # Simulate network failure
    with network_failure_simulation():
        message = UnifiedMessage(
            content="Network failure test",
            sender="Chaos Test Agent",
            recipient="Agent-1",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.URGENT
        )

        # Attempt delivery during network failure
        result = messaging_service.send_message_via_pyautogui(message)

        # Should either fail gracefully or retry
        if not result:
            # Verify retry attempts were made
            retry_logs = get_retry_logs(message.message_id)
            assert len(retry_logs) >= 3  # At least 3 retry attempts

            # Verify exponential backoff
            delays = [log['delay'] for log in retry_logs]
            assert delays[1] >= delays[0] * 1.5  # Increasing delays

    # After network recovery, verify eventual delivery
    time.sleep(5)  # Allow time for retry
    inbox_files = list(Path("agent_workspaces/Agent-1/inbox").glob("*.md"))
    chaos_messages = [f for f in inbox_files if "Network failure test" in f.read_text()]
    assert len(chaos_messages) >= 1
```

### **2. GUI Focus Loss Simulation**

```python
# test_chaos_gui_focus_loss.py

@pytest.mark.chaos
def test_gui_focus_loss_recovery():
    """Test recovery from GUI focus loss scenarios."""
    messaging_service = UnifiedMessagingCore()

    # Simulate focus loss during delivery
    with gui_focus_loss_simulation():
        message = UnifiedMessage(
            content="GUI focus loss test",
            sender="Chaos Test Agent",
            recipient="Agent-2",
            message_type=UnifiedMessageType.TEXT,
            priority=UnifiedMessagePriority.NORMAL
        )

        result = messaging_service.send_message_via_pyautogui(message)

        # Should handle focus loss gracefully
        assert isinstance(result, bool)  # Should not crash

        if not result:
            # Verify recovery attempts
            recovery_logs = get_recovery_logs(message.message_id)
            assert len(recovery_logs) >= 1

            # Verify focus reacquisition attempts
            focus_attempts = [log for log in recovery_logs
                            if 'focus' in log['action'].lower()]
            assert len(focus_attempts) >= 1

    # Verify message eventually delivered or properly failed
    final_status = get_message_status(message.message_id)
    assert final_status in ['delivered', 'permanently_failed']
```

---

## **📊 PERFORMANCE BENCHMARKS**

### **Baseline Performance Requirements**

| Metric | Current Target | Chaos Test Target | Notes |
|--------|----------------|-------------------|-------|
| Success Rate | ≥ 99.5% | ≥ 95% | Under normal conditions |
| Urgent Latency | ≤ 2s | ≤ 5s | Captain Agent-4 priority |
| Normal Latency | ≤ 5s | ≤ 10s | Standard agent delivery |
| Concurrent Capacity | 3+ agents | 2+ agents | Parallel delivery limit |
| Memory Usage | ≤ 100MB increase | ≤ 150MB increase | After feature activation |
| CPU Usage | ≤ 70% | ≤ 85% | During peak load |
| Error Recovery | ≤ 30s | ≤ 60s | From transient failure |

### **Regression Test Requirements**

```python
# test_performance_regression.py

def test_performance_regression():
    """Ensure new features don't degrade existing performance."""
    baseline_metrics = load_baseline_performance()

    # Run current performance tests
    current_metrics = run_performance_tests()

    # Verify no significant regression
    for metric, baseline_value in baseline_metrics.items():
        current_value = current_metrics[metric]
        regression_threshold = get_regression_threshold(metric)

        if metric in ['latency', 'memory_usage']:
            # Lower is better
            assert current_value <= baseline_value * (1 + regression_threshold)
        elif metric in ['success_rate', 'throughput']:
            # Higher is better
            assert current_value >= baseline_value * (1 - regression_threshold)

        print(f"✅ {metric}: {baseline_value} → {current_value}")
```

---

## **🔧 TEST AUTOMATION FRAMEWORK**

### **Test Configuration**

```python
# conftest.py
@pytest.fixture(scope="session")
def messaging_service():
    """Provide configured messaging service for tests."""
    service = UnifiedMessagingCore()
    # Configure for testing
    service.enable_test_mode()
    return service

@pytest.fixture
def mock_agent_coordinates():
    """Mock agent coordinates for testing."""
    return {
        'Agent-1': (100, 100),
        'Agent-2': (200, 200),
        # ... other agents
    }

@pytest.fixture
def performance_baseline():
    """Load performance baseline data."""
    return load_performance_baseline()
```

### **Custom Test Markers**

```python
# pytest.ini
[tool:pytest]
markers =
    integration: marks tests as integration tests (deselect with '-m "not integration"')
    load: marks tests as load tests
    chaos: marks tests as chaos engineering tests
    performance: marks tests as performance tests
    slow: marks tests as slow running
```

### **Test Data Management**

```python
# test_data.py
TEST_MESSAGES = {
    'simple': "Simple test message",
    'complex': "Complex test message with special characters: àáâãäåæçèéêë",
    'long': "A" * 1000,  # 1000 character message
    'urgent': "URGENT: System critical message",
    'multiline': "Line 1\nLine 2\nLine 3"
}

TEST_AGENTS = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5',
               'Agent-6', 'Agent-7', 'Agent-8']
```

---

## **📈 TEST EXECUTION STRATEGY**

### **CI/CD Pipeline Integration**

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run unit tests
        run: |
          pytest tests/unit/ -v --cov=src --cov-report=xml
          coverage report --fail-under=85

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/checkout@v2
      - name: Setup test environment
        run: ./scripts/setup_test_env.sh
      - name: Run integration tests
        run: pytest tests/integration/ -v -m "not slow"

  load-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      - name: Run load tests
        run: pytest tests/load/ -v --durations=10
```

### **Test Reporting**

```python
# test_reporting.py
def generate_test_report(results):
    """Generate comprehensive test report."""
    report = {
        'summary': {
            'total_tests': len(results),
            'passed': len([r for r in results if r['status'] == 'passed']),
            'failed': len([r for r in results if r['status'] == 'failed']),
            'skipped': len([r for r in results if r['status'] == 'skipped']),
            'duration_seconds': sum(r['duration'] for r in results)
        },
        'coverage': calculate_coverage(results),
        'performance': extract_performance_metrics(results),
        'failures': [r for r in results if r['status'] == 'failed'],
        'regressions': detect_performance_regressions(results)
    }

    return report
```

---

## **🎯 TEST COMPLETION CRITERIA**

### **Unit Test Completion**
- [ ] All new functions have ≥ 85% coverage
- [ ] All error paths tested
- [ ] All flag validation edge cases covered
- [ ] All timing calculations validated

### **Integration Test Completion**
- [ ] End-to-end workflows validated
- [ ] Multi-agent scenarios tested
- [ ] Error recovery flows verified
- [ ] Performance benchmarking completed

### **Load Test Completion**
- [ ] Concurrent delivery capacity tested
- [ ] Resource usage monitored under load
- [ ] Failure recovery times measured
- [ ] Memory and CPU usage profiled

### **Chaos Test Completion**
- [ ] Network failure scenarios tested
- [ ] GUI focus loss recovery validated
- [ ] System overload handling verified
- [ ] Recovery time objectives met

---

**Test Plan Version**: 1.0
**Last Updated**: Current Date
**Test Strategy Author**: Agent-7 (Web Development Specialist)

---

**WE. ARE. SWARM.** ⚡🔥
