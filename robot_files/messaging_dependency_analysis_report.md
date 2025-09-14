# Messaging Service Dependency Analysis Report
==================================================

**Files Analyzed:** 31

## Most Common Imports
```
src.services.consolidated_messaging_service.ConsolidatedMessagingService: 31 files
services.consolidated_messaging_service.ConsolidatedMessagingService: 8 files
services.consolidated_messaging_service.SWARM_AGENTS: 3 files
services.consolidated_messaging_service.MESSAGING_AVAILABLE: 2 files
services.consolidated_messaging_service.PYAUTOGUI_AVAILABLE: 2 files
services.consolidated_messaging_service.PYPERCLIP_AVAILABLE: 2 files
services.consolidated_messaging_service.parse_arguments: 2 files
src.services.messaging.consolidated_messaging_service.ConsolidatedMessagingService: 2 files
src.services.consolidated_messaging_service.get_messaging_service: 1 files
src.services.messaging.consolidated_messaging_service.get_consolidated_messaging_service: 1 files
```

## Most Common Method Calls
```
send_message_pyautogui: 16 calls
broadcast_message: 9 calls
list_agents: 8 calls
load_coordinates_from_json: 8 calls
send_message: 5 calls
show_message_history: 5 calls
process_message: 1 calls
determine_coordination_strategy: 1 calls
process_bulk_messages: 1 calls
get_command_stats: 1 calls
```

## Duplication Candidates
### High Priority
**Files (14):**
- messaging_dependency_analysis.py
- tests\__init__.py
- tests\agent2_critical_issue_solutions.py
- src\services\__init__.py
- src\services\messaging\__init__.py
- src\services\messaging\consolidated_messaging_service.py
- src\services\messaging\consolidated_messaging_service_v2.py
- src\services\messaging\cli\messaging_cli.py
- src\services\messaging\cli\messaging_cli_clean.py
- src\services\messaging\core\messaging_factory.py
- src\services\messaging\core\__init__.py
- src\integration\messaging_gateway.py
- tools\test_coverage_improvement.py
- scripts\consolidated_messaging_utility.py

## Consolidation Recommendations

### 1. Create Shared Utility Functions
- `send_message_pyautogui`: Used in 16 places - good candidate for shared utility
- `broadcast_message`: Used in 9 places - good candidate for shared utility
- `list_agents`: Used in 8 places - good candidate for shared utility
- `load_coordinates_from_json`: Used in 8 places - good candidate for shared utility

### 2. Consolidate Similar Files
- 14 files with similar patterns could be consolidated
