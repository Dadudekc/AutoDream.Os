# Testing Playbook (Agent-Readable)

## 🎯 **Testing Strategy**

### **Core Principles**
- **Fast**: Unit suite ≤ 90s on CI; integration ≤ 3m
- **Reliable**: Deterministic across 3 re-runs
- **Readable**: Clear names and AAA pattern
- **Minimal**: One behavior per test

### **Coverage Targets**
- **Global**: ≥ 85% line coverage
- **Changed Files**: ≥ 95% line coverage
- **Branch**: ≥ 70% branch coverage
- **Mutation**: ≥ 60% mutation score (optional)

## 📝 **Test Naming Convention**

```python
def test_<module>__<behavior>__<expectation>():
    """Test that <module> <behavior> <expectation>."""
    # Arrange
    # Act  
    # Assert
```

**Examples:**
```python
def test_parser__valid_input__returns_parsed_data():
def test_auth__invalid_token__raises_unauthorized():
def test_cache__expired_entry__returns_none():
```

## 🏗️ **Test Structure (AAA Pattern)**

```python
def test_example__happy_path__returns_expected():
    """Test that example happy path returns expected result."""
    # Arrange
    input_data = {"key": "value"}
    expected = {"processed": True}
    
    # Act
    result = process_data(input_data)
    
    # Assert
    assert result == expected
    assert result["processed"] is True
```

## 🚫 **Anti-Patterns to Avoid**

### **Forbidden in Unit Tests:**
- ❌ Network calls (use fakes/mocks)
- ❌ Sleep statements (use event/condition awaits)
- ❌ Shared global state
- ❌ File system operations (use tmp_path)
- ❌ Random data without seeding
- ❌ Time-dependent logic (freeze time)

### **Mock Guidelines:**
- ✅ Mock only external boundaries (APIs, databases, file system)
- ✅ Prefer real domain objects over mocks
- ✅ Use dependency injection for testability

## 🧪 **Test Types**

### **1. Unit Tests (Primary)**
```python
def test_calculator__add_positive_numbers__returns_sum():
    """Test basic addition functionality."""
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5
```

### **2. Property-Based Tests (Hypothesis)**
```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_calculator__add_commutative__order_independent(a, b):
    """Test that addition is commutative."""
    calc = Calculator()
    assert calc.add(a, b) == calc.add(b, a)

@given(st.text(min_size=0, max_size=64))
def test_parser__never_raises__on_any_text(s):
    """Test that parser never crashes on any text input."""
    result = parse(s)  # Should not raise
    assert isinstance(result, dict)
```

### **3. Integration Tests (Lightweight)**
```python
def test_api__create_user__persists_to_database():
    """Test user creation through API."""
    # Use test database
    response = client.post("/users", json={"name": "test"})
    assert response.status_code == 201
    
    # Verify persistence
    user = db.get_user(response.json()["id"])
    assert user.name == "test"
```

### **4. Contract Tests**
```python
def test_external_api__contract__returns_expected_schema():
    """Test external API contract compliance."""
    with mock_external_api() as mock_api:
        mock_api.return_value = {"id": 1, "name": "test"}
        result = fetch_user_data(1)
        assert "id" in result
        assert "name" in result
```

## 🔧 **Test Utilities**

### **Time Freezing**
```python
from freezegun import freeze_time

@freeze_time("2025-01-18 12:00:00")
def test_scheduler__at_noon__triggers_event():
    """Test time-dependent behavior."""
    scheduler = EventScheduler()
    events = scheduler.get_events_at_current_time()
    assert len(events) > 0
```

### **Random Seed**
```python
import random

def test_random_generator__with_seed__produces_deterministic():
    """Test deterministic random behavior."""
    random.seed(42)
    values = [random.randint(1, 100) for _ in range(5)]
    expected = [82, 15, 3, 35, 59]  # Known with seed 42
    assert values == expected
```

### **Temporary Files**
```python
def test_file_processor__valid_file__processes_content(tmp_path):
    """Test file processing with temporary file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    processor = FileProcessor()
    result = processor.process_file(str(test_file))
    
    assert result.success is True
    assert result.content == "test content"
```

## 🐛 **Regression Testing**

### **Bug-First Approach**
```python
def test_parser__regression_issue_123__handles_malformed_input():
    """Regression test for issue #123: parser crashes on malformed input."""
    # This test should FAIL initially (red)
    malformed_input = "invalid{json"
    
    # Should not raise exception
    result = parse_json(malformed_input)
    assert result.error is not None
    assert "malformed" in result.error.lower()
```

## 📊 **Coverage Commands**

### **Local Development Loop**
```bash
# Run tests with coverage
coverage run -m pytest -q

# Show coverage report
coverage report --show-missing

# Check changed files coverage
python tools/coverage/changed_file_report.py --base HEAD~1 --min 95 --strict

# Generate HTML report
coverage html -d .coverage_html
```

### **CI Pipeline**
```bash
# Full coverage run
coverage run -m pytest -q
coverage xml -o coverage.xml
coverage report --fail-under=85

# Changed file gate
python tools/coverage/changed_file_report.py --base origin/main --min 95 --strict
```

## 🎯 **Risk-Based Testing Priority**

### **High Priority (Test First)**
1. **Public APIs** - External interfaces
2. **State Machines (FSM)** - Complex state transitions
3. **Parsers/Serializers** - Data transformation
4. **Error Handling** - Exception paths
5. **Security-Critical** - Authentication, authorization

### **Medium Priority**
1. **Business Logic** - Core domain rules
2. **Data Validation** - Input sanitization
3. **Configuration** - Settings and defaults

### **Lower Priority**
1. **Utility Functions** - Simple helpers
2. **Logging** - Non-critical paths
3. **Metrics** - Observability code

## 🚀 **Getting Started**

### **1. Bootstrap Environment**
```bash
pip install pytest pytest-cov hypothesis mutmut coverage diff-cover
```

### **2. Run Initial Coverage**
```bash
coverage run -m pytest -q
coverage report --show-missing
```

### **3. Identify Gaps**
```bash
coverage html -d .coverage_html
open .coverage_html/index.html
```

### **4. Add Tests for Low Coverage**
Focus on files with:
- Coverage < 85%
- High complexity (cyclomatic)
- Recent changes (high churn)
- Public APIs

### **5. Verify Improvements**
```bash
coverage run -m pytest -q
coverage report --fail-under=85
python tools/coverage/changed_file_report.py --base HEAD~1 --min 95 --strict
```

## 📈 **Success Metrics**

- ✅ **Global Coverage**: ≥ 85%
- ✅ **Changed Files**: ≥ 95%
- ✅ **Zero Flaky Tests**: Deterministic across 3 runs
- ✅ **Fast Execution**: Unit suite ≤ 90s
- ✅ **Regression Coverage**: All bugfixes have tests

---

*This playbook ensures reliable, fast, and comprehensive test coverage for the V2 Swarm project.*