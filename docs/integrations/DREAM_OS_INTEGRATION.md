# Dream.OS Integration

## Overview

Dream.OS provides MMORPG-style gamification for agent task workflows through a Finite State Machine (FSM) orchestrator. The integration includes FSM task state management, atomic file operations for safe workflow execution, and UI components for visualizing agent progress through XP, skills, and quests.

**Integrated Files**: 4 files (fsm_orchestrator.py, atomic_file_manager.py, ui_integration.py, gamification UI)  
**Target Location**: `src/gaming/dreamos/`  
**V2 Compliance**: All files V2 compliant

## Setup Requirements

### Dependencies
```bash
# Dream.OS core
pyyaml>=6.0
python-dotenv>=1.0.0

# Gamification UI (optional)
flask>=2.0.0  # For API endpoints
```

### Installation
```bash
# Automated setup
python scripts/setup_dream_os_dreamvault.py

# Manual installation
pip install pyyaml>=6.0 python-dotenv>=1.0.0
```

### Runtime Directories
```bash
runtime/dreamos/
├── fsm_data/      # Task state storage
├── workflows/     # Workflow definitions
└── tasks/         # Active task data
```

## Integration Steps

### 1. Verify Source Location
```bash
Test-Path "D:\Agent_Cellphone\dreamos"
# Expected: True
```

### 2. Create Target Directory
```bash
New-Item -ItemType Directory -Path "src\gaming\dreamos" -Force
New-Item -ItemType Directory -Path "src\gaming\dreamos\resumer_v2" -Force
```

### 3. Copy Core Files
```bash
# FSM Orchestrator
Copy-Item "D:\Agent_Cellphone\dreamos\core\fsm_orchestrator.py" `
    -Destination "src\gaming\dreamos\fsm_orchestrator.py"

# Atomic File Manager
Copy-Item "D:\Agent_Cellphone\dreamos\core\resumer_v2\atomic_file_manager.py" `
    -Destination "src\gaming\dreamos\resumer_v2\atomic_file_manager.py"
```

### 4. Create Public API
Create `src/gaming/dreamos/__init__.py`:
```python
from .fsm_orchestrator import FSMOrchestrator, TaskState, Task, AgentReport

__all__ = ['FSMOrchestrator', 'TaskState', 'Task', 'AgentReport']
```

### 5. Create Flask API Integration
Create `src/gaming/dreamos/ui_integration.py` with gamification endpoints

### 6. Create Gamification UI
- `src/web/static/js/gaming/gamification-ui.js` - UI controller
- `src/web/static/css/gamification.css` - Styling
- `src/web/templates/gamification_demo.html` - Demo page

## Testing Approach

### Import Validation
```python
# Test basic import
import sys
sys.path.insert(0, 'src')
from gaming.dreamos import FSMOrchestrator, TaskState, Task, AgentReport
print('✅ Dream.OS: All imports working')
```

### Component Testing
```python
# Test FSMOrchestrator instantiation
from pathlib import Path
orchestrator = FSMOrchestrator(
    fsm_root=Path("runtime/dreamos/fsm_data"),
    inbox_root=Path("agent_workspaces"),
    outbox_root=Path("agent_workspaces")
)
```

### UI Testing
```bash
# Open demo page
# Navigate to: src/web/templates/gamification_demo.html
# Verify: XP bars, skills grid, quest tracker, achievements display
```

## Lessons Learned

### What Worked
- **Small scope**: Only 2 core files from dreamos (focused integration)
- **Clean API**: `__init__.py` provides simple imports
- **UI integration**: Gamification UI makes system visible and engaging
- **Testing early**: Import tests caught issues immediately

### Challenges
- **Syntax errors**: Original files had syntax issues (fixed during port)
- **Dependencies**: Custom utility calls needed V2 adaptation
- **Integration complexity**: UI required Flask backend coordination

### Solutions
- **V2 adaptation**: Applied patterns during porting, not after
- **Testing approach**: Simple Python import tests for quick validation
- **Documentation**: Created comprehensive guide for team

## Troubleshooting

### Issue: "SyntaxError in fsm_orchestrator.py"
**Cause**: Original file had invalid method definition syntax  
**Solution**: Fix syntax errors during porting, test import immediately

### Issue: "FSM import fails"
**Cause**: Missing `__init__.py` in dreamos directory  
**Solution**: Create `__init__.py` with clean exports

### Issue: "UI not displaying"
**Cause**: Flask blueprint not registered  
**Solution**: Call `register_gamification_blueprint(app)` in Flask app setup

---

## SSOT References

- **V2 Compliance**: All Dream.OS files maintain V2 standards (files <400 lines)
- **Logging**: Uses `logging.getLogger(__name__)` pattern (SSOT logging)
- **Configuration**: Future integration with `src/core/unified_config.py`
- **Directory Structure**: Follows V2 `src/gaming/` convention

---

**Created By**: Agent-7 - Repository Cloning Specialist  
**For**: Swarm Knowledge Sharing  
**Status**: Ready for Agent-8 SSOT Integration  
**Date**: 2025-10-09



