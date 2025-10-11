# Priority 1 Features - Implementation Guide

## Overview

This document describes the Priority 1 features ported to Agent_Cellphone_V2 from the analysis of the old Agent_Cellphone system. All implementations follow V2 compliance standards (≤400 lines per file, SOLID principles, comprehensive error handling).

## Features Implemented

### 1. Advanced Workflows System (`src/workflows/`)

**Purpose:** Production-grade workflow orchestration for multi-agent coordination.

**Components:**
- `models.py` - Workflow data models with V2 cycle-based tracking
- `engine.py` - Core workflow execution engine
- `steps.py` - Workflow step builders (conversation loops, multi-agent orchestration, decision trees, autonomous loops)
- `strategies.py` - Coordination strategies (parallel, sequential, decision tree, autonomous)
- `cli.py` - Command-line interface

**Configuration:** `config/workflows.yml`

**CLI Usage:**
```bash
# Create a conversation loop workflow
python -m src.workflows.cli create --name my_workflow --type conversation \
  --agent-a Agent-1 --agent-b Agent-2 --topic "code review" --iterations 3

# Execute a workflow
python -m src.workflows.cli execute --name my_workflow

# List all workflows
python -m src.workflows.cli list
```

**Integration Points:**
- Uses `src.core.messaging_pyautogui` for agent communication
- Uses `src.core.coordinate_loader` for agent targeting
- Integrates with orchestration registry

### 2. Vision System (`src/vision/`)

**Purpose:** Screen capture, OCR, and visual analysis for agent automation.

**Components:**
- `capture.py` - Screen capture with coordinate-based agent regions
- `ocr.py` - Text extraction with pytesseract integration
- `analysis.py` - Visual analysis (UI elements, edges, colors, layout)
- `integration.py` - Main vision system coordinating all components
- `cli.py` - Command-line interface

**Configuration:** `config/vision.yml`

**CLI Usage:**
```bash
# Capture screen for an agent
python -m src.vision.cli capture --agent Agent-1 --output agent1.png --ocr --analyze

# Extract text from image
python -m src.vision.cli ocr --input screenshot.png --language eng

# Start continuous monitoring
python -m src.vision.cli monitor --agent Agent-1 --duration 60

# Show vision capabilities
python -m src.vision.cli info
```

**Integration Points:**
- Uses `src.core.coordinate_loader` for screen regions
- Optional integration with workflow engine
- Optional monitoring for overnight runner

**Dependencies:**
```bash
pip install pytesseract opencv-python pillow
# Also requires Tesseract binary to be installed
```

### 3. ChatGPT Integration (`src/services/chatgpt/`)

**Purpose:** Browser automation for ChatGPT interaction and conversation management.

**Components:**
- `navigator.py` - Browser navigation using Playwright
- `session.py` - Session management with cookie persistence
- `extractor.py` - Conversation extraction and storage
- `cli.py` - Command-line interface

**Configuration:** `config/chatgpt.yml`

**CLI Usage:**
```bash
# Navigate to ChatGPT
python -m src.services.chatgpt.cli navigate

# Send a message
python -m src.services.chatgpt.cli send --message "Hello ChatGPT" --wait

# Extract conversation
python -m src.services.chatgpt.cli extract --url "https://chat.openai.com/c/xyz" --output conversation.json

# List saved conversations
python -m src.services.chatgpt.cli list

# Manage session
python -m src.services.chatgpt.cli session --action info
```

**Integration Points:**
- Extends `src.infrastructure.browser` infrastructure
- Uses Playwright for async browser control
- Integrates with messaging system

**Dependencies:**
```bash
pip install playwright
playwright install chromium
```

### 4. Overnight Runner (`src/orchestrators/overnight/`)

**Purpose:** 24/7 autonomous execution with cycle-based scheduling.

**Components:**
- `orchestrator.py` - Main overnight coordinator (extends CoreOrchestrator)
- `scheduler.py` - Cycle-based task scheduling with priority queues
- `monitor.py` - Progress monitoring and health tracking
- `recovery.py` - Automatic recovery and agent rescue
- `cli.py` - Command-line interface

**Configuration:** `config/orchestration.yml`

**CLI Usage:**
```bash
# Start overnight operations
python -m src.orchestrators.overnight.cli start --cycles 60 --interval 10 --workflow

# Monitor progress
python -m src.orchestrators.overnight.cli monitor --interval 60

# Check status
python -m src.orchestrators.overnight.cli status

# View recovery status
python -m src.orchestrators.overnight.cli recovery

# Show capabilities
python -m src.orchestrators.overnight.cli info
```

**Integration Points:**
- Extends `src.core.orchestration.core_orchestrator.CoreOrchestrator`
- Uses `src.core.messaging_pyautogui` for agent coordination
- Uses workflow engine for complex tasks
- Optional vision system integration

### 5. GUI System (`src/gui/`)

**Purpose:** Optional desktop interface for visual agent management.

**Components:**
- `app.py` - Main GUI application (QMainWindow-based)
- `controllers/base.py` - Base GUI controller with PyAutoGUI integration
- `components/agent_card.py` - Agent status widget
- `components/status_panel.py` - Log and status display
- `styles/themes.py` - Theme management (dark/light)

**Configuration:** `config/gui.yml`

**Usage:**
```bash
# Start GUI application
python -m src.gui.app

# Or programmatically:
from src.gui import DreamOSGUI
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
gui = DreamOSGUI()
gui.show()
sys.exit(app.exec_())
```

**Integration Points:**
- Uses `src.core.messaging_cli` for all commands
- Uses `src.core.coordinate_loader` for agent positioning
- Uses `src.core.messaging_pyautogui` for direct automation
- Completely optional - V2 remains CLI-first

**Dependencies:**
```bash
pip install PyQt5
```

## V2 Compliance

All Priority 1 features follow V2 standards:

- ✅ **File Size:** All files ≤400 lines
- ✅ **SOLID Principles:** Single responsibility, proper abstraction
- ✅ **Type Hints:** Comprehensive type annotations
- ✅ **Error Handling:** Try/except blocks throughout
- ✅ **Logging:** Uses unified logging system
- ✅ **Configuration:** Uses unified config system
- ✅ **Cycle-Based Tracking:** Not time-based (per V2 memory)
- ✅ **Documentation:** Docstrings for all public methods
- ✅ **Testing:** Comprehensive test coverage

## Installation

Install all dependencies for Priority 1 features:

```bash
# Core dependencies
pip install -r requirements.txt

# Vision system dependencies
pip install pytesseract opencv-python pillow

# ChatGPT integration dependencies
pip install playwright
playwright install chromium

# GUI dependencies (optional)
pip install PyQt5
```

## Testing

Run tests for Priority 1 features:

```bash
# Run all tests
pytest tests/test_workflows.py tests/test_vision.py tests/test_chatgpt_integration.py tests/test_overnight_runner.py

# Run with coverage
pytest --cov=src.workflows --cov=src.vision --cov=src.services.chatgpt --cov=src.orchestrators.overnight

# Run specific feature tests
pytest tests/test_workflows.py -v
```

## Next Steps

After implementing Priority 1 features, consider:

1. **Priority 2 Features:** Collaborative Knowledge, Advanced FSM, Health Monitoring
2. **Priority 3 Features:** Campaign System, AI/ML Environment, Security Framework
3. **Documentation Port:** PRD system and comprehensive documentation
4. **Service Audit:** Compare and merge with old system's 80+ services

## Support

For issues or questions about Priority 1 features:
1. Check feature-specific documentation
2. Run CLI `info` commands for capabilities
3. Review configuration files in `config/`
4. Check test files for usage examples

**WE ARE SWARM** 🐝

