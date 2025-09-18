# V2_SWARM Test Suite

Comprehensive test suite for the V2_SWARM project, ensuring code quality, V2 compliance, and system reliability.

## 🧪 Test Structure

```
tests/
├── conftest.py                    # Global pytest configuration and fixtures
├── run_tests.py                   # Test runner script
├── README.md                      # This documentation
├── unit/                          # Unit tests for individual components
│   ├── test_messaging_system.py   # Messaging system unit tests
│   ├── test_discord_commander.py  # Discord commander unit tests
│   └── test_v2_compliance.py      # V2 compliance validation tests
├── integration/                   # Integration tests for system components
│   └── test_messaging_integration.py  # Messaging system integration tests
└── performance/                   # Performance and load tests
    └── test_messaging_performance.py  # Messaging system performance tests
```

## 🚀 Quick Start

### Install Test Dependencies
```bash
pip install -r requirements-test.txt
```

### Run All Tests
```bash
python tests/run_tests.py
```

### Run Specific Test Types
```bash
# Unit tests only
python tests/run_tests.py --type unit

# Integration tests
python tests/run_tests.py --type integration

# Performance tests
python tests/run_tests.py --type performance

# V2 compliance tests
python tests/run_tests.py --type v2_compliance

# Messaging system tests
python tests/run_tests.py --type messaging

# Discord commander tests
python tests/run_tests.py --type discord
```

### Quick Test Run
```bash
# Fast unit tests without coverage
python tests/run_tests.py --quick
```

## 📊 Test Categories

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual components in isolation
- **Coverage**: All core modules and services
- **Markers**: `@pytest.mark.unit`

#### Key Test Files:
- `test_messaging_system.py`: Messaging service, status monitor, onboarding service
- `test_discord_commander.py`: Discord bot commands and functionality
- `test_v2_compliance.py`: V2 compliance validation and enforcement

### Integration Tests (`tests/integration/`)
- **Purpose**: Test component interactions and system workflows
- **Coverage**: End-to-end functionality and data flow
- **Markers**: `@pytest.mark.integration`

#### Key Test Files:
- `test_messaging_integration.py`: Complete messaging workflows and system integration

### Performance Tests (`tests/performance/`)
- **Purpose**: Validate performance characteristics and scalability
- **Coverage**: Response times, memory usage, concurrent operations
- **Markers**: `@pytest.mark.performance`

#### Key Test Files:
- `test_messaging_performance.py`: Performance benchmarks and load testing

## 🎯 Test Markers

Tests are categorized using pytest markers:

- `unit`: Unit tests for individual components
- `integration`: Integration tests for system components
- `messaging`: Tests for messaging system functionality
- `discord`: Tests for Discord commander functionality
- `database`: Tests for database integration
- `v2_compliance`: Tests for V2 compliance validation
- `performance`: Performance and load tests
- `slow`: Tests that take longer to run
- `requires_selenium`: Tests requiring Selenium WebDriver
- `requires_discord`: Tests requiring Discord bot token
- `requires_pyautogui`: Tests requiring PyAutoGUI

## 🔧 Configuration

### pytest.ini
Main pytest configuration with:
- Test discovery patterns
- Coverage settings (85% minimum)
- Custom markers
- Timeout settings (300 seconds)
- Warning filters

### conftest.py
Global fixtures and configuration:
- Mock coordinates and configuration files
- PyAutoGUI and Pyperclip mocks
- Selenium WebDriver mocks
- Discord bot mocks
- Test data management

## 📈 Coverage Requirements

- **Minimum Coverage**: 85%
- **Coverage Reports**: 
  - Terminal output with missing lines
  - HTML report in `htmlcov/`
  - XML report for CI/CD integration

### Coverage Scope
- `src/`: All source code modules
- `thea_auth/`: Thea authentication modules
- Excludes: Test files, `__pycache__`, temporary files

## 🏃‍♂️ Running Tests

### Command Line Options

```bash
python tests/run_tests.py [OPTIONS]

Options:
  --type {all,unit,integration,performance,v2_compliance,messaging,discord,slow}
                        Type of tests to run (default: all)
  --verbose, -v         Verbose output
  --no-coverage         Disable coverage reporting
  --parallel, -p        Run tests in parallel
  --quick               Quick test run (unit tests only, no coverage)
```

### Direct pytest Usage

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov=thea_auth --cov-report=html

# Run specific test file
pytest tests/unit/test_messaging_system.py

# Run tests with specific marker
pytest -m "unit and not slow"

# Run tests in parallel
pytest -n auto
```

## 🧩 Test Fixtures

### Core Fixtures
- `mock_coordinates_file`: Mock agent coordinates for testing
- `mock_pyautogui`: Mock PyAutoGUI operations
- `mock_pyperclip`: Mock clipboard operations
- `mock_selenium`: Mock Selenium WebDriver
- `mock_discord_bot`: Mock Discord bot instance
- `mock_discord_context`: Mock Discord command context

### Data Fixtures
- `mock_agent_workspace`: Mock agent workspace structure
- `mock_fsm_status`: Mock FSM status files
- `mock_project_analysis`: Mock project analysis data
- `mock_cookies`: Mock authentication cookies

## 🔍 V2 Compliance Testing

The test suite includes comprehensive V2 compliance validation:

### File Size Compliance
- All Python files must be ≤400 lines
- Automatic detection of violations
- Detailed violation reporting

### Modular Architecture Compliance
- Import structure validation
- Component separation verification
- Dependency management testing

### Code Quality Compliance
- Function length limits (≤50 lines)
- Class length limits (≤200 lines)
- Code organization validation

## 📊 Performance Benchmarks

### Messaging System Performance
- Message sending: <0.1s (mocked)
- Broadcast operations: <0.2s (mocked)
- Status retrieval: <0.5s
- Onboarding: <0.3s (mocked)

### Memory Usage
- Service instances: <5MB per instance
- Bulk operations: <100MB total
- Resource cleanup: <10MB increase

### Concurrent Operations
- 10 concurrent messages: <1.0s total
- High frequency: >100 operations/second
- Linear scalability validation

## 🐛 Debugging Tests

### Verbose Output
```bash
pytest -v -s
```

### Specific Test Debugging
```bash
pytest tests/unit/test_messaging_system.py::TestMessagingService::test_send_message_success -v -s
```

### Coverage Debugging
```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```

## 🔄 Continuous Integration

### GitHub Actions Integration
```yaml
- name: Run Tests
  run: |
    pip install -r requirements-test.txt
    python tests/run_tests.py --type all --coverage
```

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Run tests before commit
pre-commit run --all-files
```

## 📝 Writing New Tests

### Test Structure
```python
class TestNewComponent:
    """Test cases for NewComponent."""
    
    def test_initialization(self, mock_fixture):
        """Test component initialization."""
        component = NewComponent(mock_fixture)
        assert component is not None
    
    def test_functionality(self, mock_fixture):
        """Test component functionality."""
        component = NewComponent(mock_fixture)
        result = component.do_something()
        assert result is True
```

### Best Practices
1. Use descriptive test names
2. Test one thing per test method
3. Use appropriate fixtures
4. Mock external dependencies
5. Include both positive and negative test cases
6. Add performance tests for critical paths

## 🚨 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure project root is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Missing Dependencies
```bash
# Install all test requirements
pip install -r requirements-test.txt
```

#### Coverage Issues
```bash
# Check coverage configuration
pytest --cov=src --cov-report=term-missing
```

#### Performance Test Failures
```bash
# Run performance tests with more tolerance
pytest tests/performance/ -v -s
```

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Python Testing Best Practices](https://docs.python.org/3/library/unittest.html)
- [V2_SWARM Project Documentation](../README.md)

## 🤝 Contributing

When adding new tests:

1. Follow the existing test structure
2. Add appropriate markers
3. Update this documentation
4. Ensure V2 compliance
5. Add performance tests for critical paths
6. Update coverage requirements if needed

---

**Test Suite Maintained by**: Agent-2 (Architecture & Design Specialist)  
**Last Updated**: 2025-01-14  
**Version**: 1.0.0


