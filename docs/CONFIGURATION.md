# Configuration System Documentation - V2 Compliance

## Overview

The Agent Cellphone V2 project uses a unified configuration system that consolidates all configuration management into a single, maintainable system. This system eliminates redundancy, provides a Single Source of Truth (SSOT), and supports environment-specific configurations.

## Architecture

### Unified Configuration System

The configuration system is built around `src/core/unified_config.py`, which provides:

- **Centralized Configuration**: All settings in one place
- **Type Safety**: Dataclass-based configuration with type hints
- **Validation**: Runtime validation of critical settings
- **Environment Support**: Integration with `.env` files
- **Backward Compatibility**: Existing imports continue to work

### Configuration Classes

#### 1. TimeoutConfig
Manages all timeout-related settings across the system.

```python
@dataclass
class TimeoutConfig:
    scrape_timeout: float = 30.0
    response_wait_timeout: float = 120.0
    quality_check_interval: float = 30.0
    metrics_collection_interval: float = 60.0
    # ... test timeouts
```

#### 2. AgentConfig
Centralizes agent-related configuration.

```python
@dataclass
class AgentConfig:
    agent_count: int = 8
    captain_id: str = "Agent-4"
    default_mode: str = "pyautogui"
    coordinate_mode: str = "8-agent"
    
    @property
    def agent_ids(self) -> List[str]:
        return [f"Agent-{i}" for i in range(1, self.agent_count + 1)]
```

#### 3. FilePatternConfig
Manages file pattern regexes for project analysis.

```python
@dataclass
class FilePatternConfig:
    test_file_pattern: str = "test_*.py"
    architecture_files: str = r'\.(py|js|ts|java|cpp|h|md)$'
    config_files: str = r'(config|settings|env|yml|yaml|json|toml|ini)$'
    # ... other patterns
```

#### 4. ThresholdConfig
Centralizes performance thresholds and alert rules.

```python
@dataclass
class ThresholdConfig:
    coverage_threshold: float = 80.0
    response_time_target: float = 100.0
    throughput_target: float = 1000.0
    reliability_target: float = 99.9
    # ... other thresholds
```

#### 5. BrowserConfig
Manages browser interaction settings.

```python
@dataclass
class BrowserConfig:
    gpt_url: str = "https://chatgpt.com/g/..."
    conversation_url: str = "https://chatgpt.com/c/..."
    input_selector: str = "textarea[data-testid='prompt-textarea']"
    # ... other selectors
```

#### 6. TestConfig
Centralizes test configuration and categories.

```python
@dataclass
class TestConfig:
    test_categories: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {...})
    coverage_report_precision: int = 2
    history_window: int = 100
```

#### 7. ReportConfig
Manages reporting configuration.

```python
@dataclass
class ReportConfig:
    reports_dir: Path = Path("reports")
    default_format: ReportFormat = ReportFormat.JSON
    include_metadata: bool = True
    include_recommendations: bool = True
```

## Environment Configuration

### Environment Variables

The system supports environment-specific configuration through `.env` files. Copy `env.example` to `.env` and modify as needed.

#### Key Environment Variables

```bash
# Agent Configuration
AGENT_COUNT=8
CAPTAIN_ID=Agent-4
DEFAULT_MODE=pyautogui
COORDINATE_MODE=8-agent

# Timeout Configuration
SCRAPE_TIMEOUT=30.0
RESPONSE_WAIT_TIMEOUT=120.0
QUALITY_CHECK_INTERVAL=30.0
METRICS_COLLECTION_INTERVAL=60.0

# Threshold Configuration
COVERAGE_THRESHOLD=80.0
RESPONSE_TIME_TARGET=100.0
THROUGHPUT_TARGET=1000.0
RELIABILITY_TARGET=99.9

# Browser Configuration
GPT_URL=https://chatgpt.com/g/...
CONVERSATION_URL=https://chatgpt.com/c/...
INPUT_SELECTOR=textarea[data-testid='prompt-textarea']
```

### Environment Loading

The system automatically loads environment variables using `src/core/env_loader.py`:

```python
from src.core.env_loader import load_environment_config

# Load environment configuration
success = load_environment_config()
if not success:
    print("Failed to load environment configuration")
```

## Usage

### Basic Usage

```python
from src.core.unified_config import get_unified_config

# Get the unified configuration
config = get_unified_config()

# Access specific configurations
print(f"Agent count: {config.agents.agent_count}")
print(f"Scrape timeout: {config.timeouts.scrape_timeout}")
print(f"Coverage threshold: {config.thresholds.coverage_threshold}")
```

### Convenience Functions

```python
from src.core.unified_config import (
    get_timeout_config, get_agent_config, get_threshold_config,
    get_browser_config, get_test_config, get_file_pattern_config,
    get_report_config
)

# Get specific configuration objects
timeout_config = get_timeout_config()
agent_config = get_agent_config()
threshold_config = get_threshold_config()
```

### Migrated Config Files

The following config files have been migrated to use the unified system:

- `src/services/config.py` - Messaging services
- `src/services/quality/config.py` - Quality monitoring
- `src/core/refactoring/config.py` - Refactoring toolkit
- `src/reporting/config.py` - Error reporting
- `tests/runners/config.py` - Test categories
- `tests/infrastructure/config.py` - Test infrastructure
- `src/core/performance/metrics/config.py` - Performance metrics
- `tests/messaging/fixtures/config.py` - Test fixtures
- `src/infrastructure/browser/thea_modules/config.py` - Browser interactions

## Validation

### Runtime Validation

The system includes comprehensive runtime validation:

```python
from src.core.unified_config import get_unified_config

config = get_unified_config()
issues = config.validate()

if issues:
    print("Configuration validation failed:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("Configuration is valid")
```

### Validation Rules

- **Timeouts**: Must be positive values
- **Agent Count**: Must be between 1 and 20
- **Captain ID**: Must start with "Agent-"
- **URLs**: Must be valid HTTPS URLs
- **Thresholds**: Must be within valid ranges (0-100 for percentages)
- **File Patterns**: Cannot be empty
- **Coverage Precision**: Must be between 0 and 10

## Migration Guide

### From Individual Config Files

If you have code using individual config files, the migration is straightforward:

```python
# Before
from src.services.config import AGENT_COUNT, CAPTAIN_ID

# After (still works)
from src.services.config import AGENT_COUNT, CAPTAIN_ID

# Or use unified config directly
from src.core.unified_config import get_agent_config
agent_config = get_agent_config()
agent_count = agent_config.agent_count
captain_id = agent_config.captain_id
```

### Adding New Configuration

To add new configuration values:

1. Add to the appropriate config class in `unified_config.py`
2. Add environment variable to `env.example`
3. Update the environment loader in `env_loader.py`
4. Add validation rules if needed
5. Update tests

## Testing

### Running Configuration Tests

```bash
# Run all configuration tests
python -m pytest tests/core/test_unified_config.py -v

# Run specific test categories
python -m pytest tests/core/test_unified_config.py::TestTimeoutConfig -v
python -m pytest tests/core/test_unified_config.py::TestValidation -v
```

### Test Coverage

The configuration system includes comprehensive tests for:

- Default value initialization
- Custom value setting
- Type conversion
- Validation rules
- Environment loading
- Integration testing
- Error handling

## Best Practices

### 1. Use Environment Variables for Deployment-Specific Values

```python
# Good: Use environment variables
AGENT_COUNT = get_config("AGENT_COUNT", 8)

# Avoid: Hardcoded values
AGENT_COUNT = 8
```

### 2. Validate Configuration at Startup

```python
def startup_validation():
    config = get_unified_config()
    issues = config.validate()
    if issues:
        raise ConfigurationError(f"Invalid configuration: {issues}")
```

### 3. Use Type Hints

```python
# Good: Type hints
def process_config(config: UnifiedConfig) -> None:
    pass

# Avoid: No type hints
def process_config(config):
    pass
```

### 4. Document Configuration Changes

When adding new configuration values, update:

- This documentation
- `env.example`
- Configuration tests
- Migration notes if needed

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `src` is in your Python path
2. **Environment Loading**: Check that `.env` file exists and is readable
3. **Validation Failures**: Review validation rules and fix invalid values
4. **Type Conversion**: Ensure environment variables match expected types

### Debug Mode

Enable debug logging to troubleshoot configuration issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from src.core.unified_config import get_unified_config
config = get_unified_config()
```

## Future Enhancements

- **Configuration Hot Reloading**: Reload configuration without restart
- **Configuration UI**: Web interface for configuration management
- **Configuration Templates**: Predefined configurations for different environments
- **Configuration Encryption**: Encrypt sensitive configuration values
- **Configuration Backup**: Automatic backup of configuration changes

## Contributing

When contributing to the configuration system:

1. Follow the existing patterns
2. Add comprehensive tests
3. Update documentation
4. Ensure backward compatibility
5. Validate all changes

## License

This configuration system is part of the Agent Cellphone V2 project and is licensed under the MIT License.
