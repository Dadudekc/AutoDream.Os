# AutoDream OS
AutoDream OS is a modular, V2 standards compliant platform for building agent-driven applications. It enforces strict coding standards and provides convenient command line interfaces for development and testing.

## Features
- **V2 coding standards** with line-count limits and object-oriented design
- **Modular architecture** for core systems, services, launchers, utilities and web components
- **CLI interfaces** for every module to assist quick experimentation
- **Smoke tests and test suites** to validate components
- **Structured logging and error handling**
- **Terminal completion monitor** detects SSOT `COMPLETION_SIGNAL` and cross-checks tasks via `CURSOR_DB_PATH`
- **CI/CD templates** for Jenkins, GitLab CI and Docker
- **Refactored middleware pipeline** split into SRP modules under `src/services/middleware`
- **Unified workspace management** via `UnifiedWorkspaceSystem`
- **Base engine abstraction** centralizing initialization, status reporting, and cleanup
- **Overnight consistency enhancements** with rotating validation prompts,
  optional QA agent, and completion signals
  ([spec](docs/specifications/OVERNIGHT_CONSISTENCY_ENHANCEMENTS_PRD.md))
## Middleware Execution Order
Middleware chains process packets sequentially in the order that middleware
components are listed. Each component receives the `DataPacket` returned by the
previous one, allowing earlier middleware to mutate the packet before later
components execute. Disabled middleware or components whose conditions fail are
skipped.
## Getting Started
### Installation
```bash
pip install -r requirements.txt
```

### Quick status check
```bash
# Run comprehensive TDD tests
python tests/test_messaging_system_tdd.py

# Run quick smoke tests
python tests/smoke_test_messaging_system.py
```

### Launch web module
```bash
python -m src.web --start
```

### Running Tests
```bash
pytest
```

## Agent Cellphone V2 - Unified Coordinate Architecture
**WE. ARE. SWARM.**

### Project Overview
Agent Cellphone V2 is a sophisticated multi-agent communication system with a **unified coordinate architecture** that eliminates duplicate code and provides a single source of truth for all agent operations.

### 🎯 **Coding Standards & Compliance**
- **Unified Standards**: See `UNIFIED_CODING_STANDARDS_AND_COMPLIANCE_2024.md` for complete coding standards and compliance requirements
- **Agent Workflow**: See `AGENT_WORKFLOW_CHECKLIST.md` for automated development guidelines
- **Agent Onboarding**: See `src/launchers/unified_onboarding_launcher.py` for unified onboarding system
- **Captain Coordination Training**: See `docs/onboarding/CAPTAIN_COORDINATION_TRAINING.md` for coordination training
- **Current Compliance**: 93.0% (targeting 97.2% by end of Phase 3)
- **Architecture**: FSM-driven development with contract system for task management

### Key Features
- **Unified Coordinate Management** - Single source of truth for all agent coordinates
- **Modular Messaging System** - Clean, V2-compliant architecture following OOP and SRP principles
- **Multi-Mode Support** - 2-agent, 4-agent, 5-agent, and 8-agent configurations
- **Advanced Coordinate Features** - Mapping, calibration, consolidation, and validation
- **Fallback Compatibility** - Graceful degradation for legacy systems
- **100% V2 Compliance** - Clean, modular, production-grade code

## New Unified Architecture
### Core Components
```
src/services/messaging/
├── interfaces.py                    # Abstract interfaces and contracts
├── coordinate_manager.py            # Unified coordinate management
├── pyautogui_messaging.py           # PyAutoGUI-based messaging
├── campaign_messaging.py            # Campaign and broadcast messaging
├── yolo_messaging.py                # YOLO automatic activation
├── unified_messaging_service.py     # Main orchestrator
├── cli_interface.py                 # Command-line interface
├── __init__.py                      # Package initialization
└── __main__.py                      # Module entry point
```

### Legacy Integration
All legacy files have been updated to use the unified coordinate manager:
- `real_agent_communication_system_v2.py` ✅ Updated
- `src/services/v2_message_delivery_service.py` ✅ Updated
- `core/real_agent_communication_system.py` ✅ Updated

## Quick Start
### 1. Coordinate Management
```bash
# View coordinate mapping
python -m src.services.messaging --coordinates

# Consolidate coordinate files
python -m src.services.messaging --consolidate

# Calibrate specific agent coordinates
python -m src.services.messaging --calibrate Agent-1 -1399 486 -1306 180
```

### 2. Messaging Operations
```bash
# Send message to specific agent
python -m src.services.messaging --mode pyautogui --agent Agent-1 --message "Hello Agent-1!"

# Broadcast to all agents
python -m src.services.messaging --mode campaign --message "System broadcast"

# Activate YOLO mode
python -m src.services.messaging --mode yolo --message "YOLO activation"
```

### 3. System Status
```bash
# Validate coordinates
python -m src.services.messaging --validate

# View available modes
python -m src.services.messaging --help
```

## Coordinate System
### Supported Modes
- **2-agent**: Simple setups
- **4-agent**: Medium complexity
- **5-agent**: Specialized workflows
- **8-agent**: Full swarm operations (default)

### Coordinate Operations
- **Mapping**: Visual coordinate display and validation
- **Calibration**: Update agent coordinates in real-time
- **Consolidation**: Merge coordinate files from multiple sources
- **Validation**: Comprehensive coordinate integrity checking

### File Locations
- **Primary**: `config/cursor_agent_coords.json`
- **Fallback**: `runtime/agent_comms/cursor_agent_coords.json`
- **Automatic Detection**: Intelligent fallback mechanisms

## Development & Testing
### Testing Suite
The project includes comprehensive TDD tests and smoke tests for validation (see the quick status check commands above).

### Code Quality
- **TDD Approach**: Test-Driven Development implemented
- **V2 Standards**: OOP, SRP, clean modular production-grade code
- **Interface Design**: Abstract base classes with dependency injection
- **Error Handling**: Comprehensive exception handling with graceful fallbacks

## Documentation
### Architecture Documents
- [`docs/V2_COMPLIANT_MESSAGING_ARCHITECTURE.md`](docs/V2_COMPLIANT_MESSAGING_ARCHITECTURE.md) - Complete architecture overview
- [`docs/COORDINATE_MAPPING_CONSOLIDATION_COMPLETE.md`](docs/COORDINATE_MAPPING_CONSOLIDATION_COMPLETE.md) - Coordinate system details
- [`docs/LEGACY_FILES_COORDINATE_UPDATE_COMPLETE.md`](docs/LEGACY_FILES_COORDINATE_UPDATE_COMPLETE.md) - Legacy integration status

### System Status
- **Coordinate System**: ✅ 100% Complete and Unified
- **Legacy Integration**: ✅ All Files Updated
- **Testing**: ✅ TDD and Smoke Tests Implemented
- **Documentation**: ✅ Comprehensive Coverage

## Usage Examples
### Basic Coordinate Operations
```python
from src.services.messaging import CoordinateManager

# Initialize coordinate manager
cm = CoordinateManager()

# Get available modes
modes = cm.get_available_modes()  # ['2-agent', '4-agent', '5-agent', '8-agent']

# Get agents in 8-agent mode
agents = cm.get_agents_in_mode("8-agent")  # ['Agent-1', 'Agent-2', ...]

# Get specific agent coordinates
coords = cm.get_agent_coordinates("Agent-1", "8-agent")
print(f"Input: {coords.input_box}, Starter: {coords.starter_location}")

# Validate all coordinates
validation = cm.validate_coordinates()
print(f"Valid: {validation['valid_coordinates']}/{validation['total_agents']}")
```

### Messaging Operations
```python
from src.services.messaging import UnifiedMessagingService

# Initialize unified service
service = UnifiedMessagingService()

# Send message to specific agent
success = service.send_message(
    recipient="Agent-1",
    message_content="Hello from unified system!",
    mode=MessagingMode.PYAUTOGUI
)

# Broadcast campaign message
results = service.send_message(
    recipient=None,
    message_content="Campaign broadcast",
    mode=MessagingMode.CAMPAIGN
)
```

## Repository Structure
```
src/      # application source
tests/    # test suites
docs/     # additional documentation
examples/ # examples and demos
```

## Recent Major Refactoring Achievements

### 🧪 **Frontend Testing Infrastructure** (V2 Compliant)
- **Modular Testing Framework**: Refactored from monolithic to modular architecture
- **Comprehensive Test Suites**: Component, routing, and integration testing
- **Mock Data Generation**: Realistic test data for consistent testing
- **Assertion Helpers**: Standardized testing utilities
- **Documentation**: [Frontend Testing Guide](docs/features/frontend_testing_infrastructure.md)

### 🏥 **Health Monitoring System** (V2 Compliant)
- **Eliminated Critical Violation**: Refactored 950+ line monolithic file
- **Modular Architecture**: Clean separation of concerns
- **Focused Responsibilities**: Each module under 300 lines
- **Improved Maintainability**: Easier testing and debugging
- **Documentation**: [Health Monitoring Guide](docs/features/health_monitoring_refactoring.md)

### 📊 **V2 Compliance Progress**
- **Current Status**: 72.9% compliant (433/594 files)
- **Major Milestone**: ✅ **ZERO files over 800 lines remaining!**
- **Focus Strategy**: Targeting 350+ LOC files for meaningful modularization
- **Progress Tracker**: [V2 Compliance Progress](V2_COMPLIANCE_PROGRESS_TRACKER.md)

## Contributing
- Follow the [V2 coding standards](V2_CODING_STANDARDS.md)
- Keep files within the specified line-count limits
- Provide CLI entrypoints and smoke tests for new modules

## Links
- [Examples](examples/)
- [Tests](tests/)
- [Configuration](config/)

## Examples & Case Studies
- [Vector Database Integration](docs/case-studies/vector-database.md)

## Achievements
### What's Been Accomplished
- 180+ lines of duplicate code eliminated
- 3 legacy files successfully updated
- Unified coordinate manager implemented
- Advanced coordinate features added
- 100% V2 coding standards compliance
- Comprehensive testing implemented
- Full documentation coverage

### Architecture Benefits
- Single Source of Truth: All coordinates managed in one place
- Eliminated Duplication: No more scattered coordinate logic
- Improved Maintainability: Clean, modular architecture
- Better Performance: Optimized coordinate loading and caching
- Future-Proof Design: Easy to extend and modify


## License
MIT License - See [LICENSE](LICENSE) file for details.

---

**The Agent Cellphone V2 coordinate system is now completely unified, efficient, and ready for production deployment!**

**WE. ARE. SWARM.** 🚀

---

This repository is the single source of truth for AutoDream OS. It maintains V2 standards to ensure high-quality, agent-friendly code.

## Logging

Use the unified logging manager to configure loggers:

```python
from src.utils.unified_logging_manager import get_logger

logger = get_logger(__name__)
```

This centralizes configuration and removes the need for module-level `logging.basicConfig` calls.

