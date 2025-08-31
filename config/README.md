# Configuration Directory - Organized Structure

## Overview
This directory contains all configuration files organized in a clean, logical structure. The previous messy config/ and configs/ directories have been consolidated and organized.

## Directory Structure

### system/ - System-Level Configurations
- performance.json - Performance monitoring configuration
- integration.json - System integration settings
- communication.json - Cross-system communication
- endpoints.json - System endpoints and URLs

### services/ - Service-Specific Configurations
- financial.yaml - Financial services configuration
- portal.yaml - Portal services configuration
- broadcast.yaml - Broadcasting services
- message_queue.json - Message queuing configuration
- unified.yaml - Unified service configuration

### agents/ - Agent-Related Configurations
- agent_config.json - Main agent configuration
- coordinates.json - Agent coordinate mappings
- stall_prevention.json - Stall prevention settings
- modes.json - Runtime mode configurations
- fsm_communication.json - FSM communication settings

### development/ - Development & Testing
- pytest.ini - PyTest configuration
- coverage.ini - Coverage configuration
- test.yaml - Test configuration
- requirements.txt - Consolidated requirements (SSOT)

### ci_cd/ - CI/CD Configurations
- jenkins.groovy - Jenkins pipeline configuration
- gitlab-ci.yml - GitLab CI configuration
- docker-compose.yml - Docker compose for CI
- Makefile - Build automation
- nginx.conf - Nginx configuration

### ai_ml/ - AI/ML Configurations
- ai_ml.json - AI/ML service configuration
- api_keys.template.json - API key templates

### contracts/ - Contract Files
- contract_input.txt - Contract input data

## Usage

### Using the Configuration Loader
```python
from config.config_loader import get_config, get_system_config

# Load specific configuration
performance_config = get_config("system/performance.json")

# Load system configuration
system_config = get_system_config()

# Load service configuration
financial_config = get_config("services/financial.yaml")
```

### Direct File Access
```python
import json
from pathlib import Path

# Load JSON configuration
with open("config/system/performance.json", "r") as f:
    config = json.load(f)
```

## Migration Notes

### Old Structure (Removed)
- ~~config/~~ - Scattered configuration files (REMOVED)
- ~~configs/~~ - CI/CD and infrastructure configs (REMOVED)

### New Structure (Current)
- config/ - Organized, logical structure
- Clear separation of concerns
- Consistent naming conventions
- Easy to navigate and maintain

## Benefits

1. Organization: Logical grouping by purpose
2. Maintainability: Easy to find and update configurations
3. Consistency: Standardized naming and structure
4. Scalability: Easy to add new configuration categories
5. Documentation: Clear structure with README

## Cleanup

✅ **COMPLETED**: 
1. ✅ Updated all import statements in code
2. ✅ Tested all configurations load properly
3. ✅ Removed old config/ and configs/ directories
4. ✅ Renamed config_new/ to config/

---
Last Updated: August 23, 2025
Status: ✅ REORGANIZATION COMPLETE - PRODUCTION READY
