# Unified Configuration Management System - Design Document

## System Overview
The Unified Configuration Management System consolidates all scattered configuration files into a hierarchical, maintainable structure that eliminates SSOT violations and provides a single source of truth for all system configuration.

## Architecture Design

### 1. Configuration Hierarchy
```
config/
├── system/
│   ├── core.yaml          # Core system constants and paths
│   ├── logging.yaml       # Unified logging configuration
│   ├── agents.yaml        # Agent lifecycle and coordination
│   └── services.yaml      # Service configuration with inheritance
├── development/
│   ├── testing.yaml       # Testing and coverage configuration
│   └── ci_cd.yaml        # CI/CD and build automation
└── runtime/
    ├── emergency.yaml     # Emergency response protocols
    └── monitoring.yaml    # Health monitoring and metrics
```

### 2. Configuration Inheritance System
- **Base Configuration**: Common settings shared across all components
- **Category Configuration**: Settings specific to a category (system, development, runtime)
- **Component Configuration**: Settings specific to individual components
- **Environment Overrides**: Environment-specific configuration values

### 3. Configuration Schema
```yaml
# config/system/core.yaml
system:
  version: "2.0.0"
  environment: "development"
  debug: false
  
  paths:
    root_dir: "${ROOT_DIR}"
    agent_workspaces: "agent_workspaces"
    health_reports: "health_reports"
    health_charts: "health_charts"
    
  constants:
    task_id_format: "%Y%m%d_%H%M%S_%f"
    clipboard_poll_ms: 500
    ocr_language: "eng"
    ocr_psm: 6

# config/system/logging.yaml
logging:
  level: "${LOG_LEVEL:INFO}"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  handlers:
    console:
      enabled: true
      level: "INFO"
    file:
      enabled: true
      level: "DEBUG"
      filename: "${LOG_FILE:logs/app.log}"
      max_bytes: 10485760
      backup_count: 5

# config/system/agents.yaml
agents:
  count: 8
  captain_id: "Agent-4"
  default_lifecycle_state: "initialized"
  default_coordination_strategy: "round_robin"
  metrics_poll_interval: 60
  
  messaging:
    system: "v2_message_queue"
    coordinate_mode: "8-agent"
    default_mode: "pyautogui"

# config/system/services.yaml
services:
  base:
    timeout: 30
    retry_attempts: 3
    enable_monitoring: true
    
  messaging:
    extends: "base"
    queue_size: 1000
    message_ttl: 3600
    
  orchestration:
    extends: "base"
    max_concurrent_tasks: 10
    task_timeout: 300
    
  quality:
    extends: "base"
    enable_validation: true
    validation_timeout: 60
    
  refactoring:
    extends: "base"
    max_workers: 4
    enable_parallel_processing: true
```

## Implementation Components

### 1. Configuration Manager Class
```python
class UnifiedConfigManager:
    """Unified configuration management system"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_cache = {}
        self.environment = os.getenv("ENVIRONMENT", "development")
        
    def load_config(self, category: str, component: str = None) -> Dict[str, Any]:
        """Load configuration for a category and optional component"""
        
    def get_config(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'system.core.version')"""
        
    def set_config(self, key_path: str, value: Any) -> bool:
        """Set configuration value using dot notation"""
        
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration against schema"""
        
    def reload_config(self) -> bool:
        """Reload all configuration files"""
```

### 2. Configuration Loader
```python
class ConfigLoader:
    """Load configuration files with support for multiple formats"""
    
    def load_yaml(self, filepath: Path) -> Dict[str, Any]:
        """Load YAML configuration file"""
        
    def load_json(self, filepath: Path) -> Dict[str, Any]:
        """Load JSON configuration file"""
        
    def load_env_overrides(self) -> Dict[str, Any]:
        """Load environment variable overrides"""
        
    def resolve_variables(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve variable references in configuration"""
```

### 3. Configuration Validator
```python
class ConfigValidator:
    """Validate configuration against schemas"""
    
    def validate_schema(self, config: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """Validate configuration against JSON schema"""
        
    def validate_required_fields(self, config: Dict[str, Any], required: List[str]) -> bool:
        """Validate required fields are present"""
        
    def validate_field_types(self, config: Dict[str, Any], type_map: Dict[str, str]) -> bool:
        """Validate field types match expected types"""
```

## Migration Strategy

### Phase 1: Schema Creation
1. Create unified configuration schema
2. Define configuration inheritance rules
3. Create validation schemas

### Phase 2: Core System Migration
1. Migrate system core configuration
2. Migrate logging configuration
3. Migrate agent configuration
4. Migrate service configuration

### Phase 3: Development Configuration
1. Migrate testing configuration
2. Migrate CI/CD configuration
3. Update build scripts

### Phase 4: Runtime Configuration
1. Migrate emergency response configuration
2. Migrate monitoring configuration
3. Update runtime scripts

### Phase 5: Import Updates
1. Update all import statements
2. Replace scattered config imports
3. Test configuration loading

### Phase 6: Validation & Testing
1. Validate all configurations
2. Test system functionality
3. Update documentation

## Configuration Access Patterns

### 1. Direct Access
```python
from config.unified_config import config_manager

# Get system version
version = config_manager.get_config("system.core.version")

# Get agent count
agent_count = config_manager.get_config("system.agents.count")
```

### 2. Service-Specific Access
```python
from config.unified_config import get_service_config

# Get messaging service config
messaging_config = get_service_config("messaging")

# Get orchestration config with inheritance
orchestration_config = get_service_config("orchestration")
```

### 3. Environment-Specific Access
```python
from config.unified_config import get_env_config

# Get environment-specific configuration
env_config = get_env_config("production")
```

## Benefits

### 1. SSOT Compliance
- Single source of truth for all configuration
- Eliminates configuration duplication
- Consistent configuration across components

### 2. Maintainability
- Centralized configuration management
- Easy to update and modify
- Clear configuration hierarchy

### 3. Flexibility
- Environment-specific overrides
- Configuration inheritance
- Runtime configuration updates

### 4. Validation
- Schema-based validation
- Type checking
- Required field validation

## Risk Mitigation

### 1. Backup Strategy
- Preserve original configuration files
- Create configuration snapshots
- Implement rollback procedures

### 2. Testing Strategy
- Comprehensive configuration testing
- Integration testing with all services
- Performance testing for configuration loading

### 3. Rollback Plan
- Quick rollback to original configurations
- Service restart procedures
- Configuration validation checks

## Success Criteria
1. All configuration files consolidated into unified structure
2. Zero SSOT violations
3. All services successfully load unified configuration
4. Configuration validation passes
5. System functionality maintained
6. Documentation updated
7. Performance maintained or improved
