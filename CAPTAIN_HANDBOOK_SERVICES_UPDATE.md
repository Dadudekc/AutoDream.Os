# 🔧 **CAPTAIN'S HANDBOOK - CONSOLIDATED SERVICES SECTION**

## **Core Messaging & Communication Services**

### **1. Consolidated Messaging Service (`src/services/consolidated_messaging_service.py`)**
```bash
# Primary messaging service for swarm communication
python src/services/consolidated_messaging_service.py --help

# Key Commands:
# Send individual message
python src/services/consolidated_messaging_service.py --agent Agent-2 --message "Architectural review complete" --priority HIGH --tag COORDINATION

# Broadcast to all agents
python src/services/consolidated_messaging_service.py --broadcast --message "Phase 2 consolidation initiated" --priority URGENT --tag COORDINATION

# Show message history
python src/services/consolidated_messaging_service.py --history

# List all agents
python src/services/consolidated_messaging_service.py --list-agents

# Features:
# - Unified messaging interface
# - PyAutoGUI coordinate-based delivery
# - Message priority system (LOW, NORMAL, HIGH, URGENT)
# - Tag-based organization (GENERAL, COORDINATION, TASK, STATUS)
# - Broadcast capabilities
# - Message history tracking
```

### **2. Consolidated Agent Management Service (`src/services/consolidated_agent_management_service.py`)**
```bash
# Agent lifecycle and status management
python src/services/consolidated_agent_management_service.py --agent Agent-2 --action status

# Key Commands:
# Get agent status
python src/services/consolidated_agent_management_service.py --agent Agent-2 --action status

# Update agent assignment
python src/services/consolidated_agent_management_service.py --agent Agent-2 --action assign --role "Architecture & Design Specialist"

# Vector integration status
python src/services/consolidated_agent_management_service.py --agent Agent-2 --action vector-status

# Features:
# - Agent status tracking
# - Role assignment management
# - Vector database integration
# - Workspace management
# - Performance monitoring
```

## **System Integration & Migration Services**

### **3. Final Consolidation Migration (`src/services/final_consolidation_migration.py`)**
```bash
# Final consolidation of remaining services
python src/services/final_consolidation_migration.py

# Features:
# - Automated service consolidation
# - Backup creation before migration
# - File reduction tracking (60% target)
# - Consolidation verification
# - Rollback capabilities
```

### **4. Consolidated Onboarding Service (`src/services/consolidated_onboarding_service.py`)**
```bash
# Phase 2 status and coordination tracking
python src/services/consolidated_onboarding_service.py

# Key Commands:
# Get Phase 2 status
python src/services/consolidated_onboarding_service.py --status

# Get agent assignments
python src/services/consolidated_onboarding_service.py --assignments

# Check Phase 2 activity
python src/services/consolidated_onboarding_service.py --active

# Features:
# - Phase 2 status tracking
# - Agent assignment management
# - Target monitoring
# - Coordination status
# - Discord integration tracking
```

### **5. Consolidated Handler Service (`src/services/consolidated_handler_service.py`)**
```bash
# Unified handler service for various system operations
python src/services/consolidated_handler_service.py --help

# Key Commands:
# Command handling
python src/services/consolidated_handler_service.py --command "status" --agent Agent-2

# Contract management
python src/services/consolidated_handler_service.py --contract "review" --agent Agent-2

# Coordinate operations
python src/services/consolidated_handler_service.py --coordinate "validate" --agent Agent-2

# Onboarding operations
python src/services/consolidated_handler_service.py --onboarding "status" --agent Agent-2

# Utility operations
python src/services/consolidated_handler_service.py --utility "catalog" --agent Agent-2

# Features:
# - Command handler integration
# - Contract management
# - Coordinate validation
# - Onboarding workflows
# - Utility operations
```

## **Migration & Legacy Services**

### **6. Migrate Consolidated Services (`src/services/migrate_consolidated_services.py`)**
```bash
# Service migration and consolidation management
python src/services/migrate_consolidated_services.py

# Features:
# - Automated service migration
# - Consolidation tracking
# - Legacy service cleanup
# - Migration verification
# - Rollback support
```

### **7. Migrate Onboarding Services (`src/services/migrate_onboarding_services.py`)**
```bash
# Onboarding service migration management
python src/services/migrate_onboarding_services.py

# Features:
# - Onboarding service migration
# - Legacy cleanup
# - Integration verification
# - Status tracking
```

## **Library Services (No CLI - Import Only)**

### **8. Consolidated Architectural Service (`src/services/consolidated_architectural_service.py`)**
```python
# Import for architectural operations
from src.services.consolidated_architectural_service import ArchitecturalPrinciple, ConsolidatedArchitecturalService

# Usage:
architectural_service = ConsolidatedArchitecturalService()
principles = architectural_service.get_principles()
```

### **9. Consolidated Vector Service (`src/services/consolidated_vector_service.py`)**
```python
# Import for vector database operations
from src.services.consolidated_vector_service import ConsolidatedVectorService

# Usage:
vector_service = ConsolidatedVectorService()
vector_service.ingest_data(data)
```

### **10. Consolidated Miscellaneous Service (`src/services/consolidated_miscellaneous_service.py`)**
```python
# Import for miscellaneous operations
from src.services.consolidated_miscellaneous_service import ConsolidatedMiscellaneousService

# Usage:
misc_service = ConsolidatedMiscellaneousService()
misc_service.perform_operation()
```

---

## **Consolidated Services Quick Reference**

```bash
# 📨 MESSAGING & COMMUNICATION
python src/services/consolidated_messaging_service.py --broadcast --message "..." --priority URGENT
python src/services/consolidated_messaging_service.py --agent Agent-2 --message "..." --priority HIGH
python src/services/consolidated_messaging_service.py --history
python src/services/consolidated_messaging_service.py --list-agents

# 👥 AGENT MANAGEMENT
python src/services/consolidated_agent_management_service.py --agent Agent-2 --action status
python src/services/consolidated_agent_management_service.py --agent Agent-2 --action assign --role "..."

# 🔄 MIGRATION & CONSOLIDATION
python src/services/final_consolidation_migration.py
python src/services/migrate_consolidated_services.py
python src/services/migrate_onboarding_services.py

# 📊 STATUS & COORDINATION
python src/services/consolidated_onboarding_service.py --status
python src/services/consolidated_onboarding_service.py --assignments
python src/services/consolidated_onboarding_service.py --active

# 🎛️ HANDLER OPERATIONS
python src/services/consolidated_handler_service.py --command "status" --agent Agent-2
python src/services/consolidated_handler_service.py --contract "review" --agent Agent-2
python src/services/consolidated_handler_service.py --coordinate "validate" --agent Agent-2
```

---

## **Service Integration Architecture**

### **Primary Service Dependencies**
```python
# Core dependencies for all services:
from src.core.messaging_core import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageTag
from src.core.coordinate_loader import get_coordinate_loader
from src.services.consolidated_architectural_service import ArchitecturalPrinciple

# PyAutoGUI integration:
import pyautogui
import pyperclip
```

### **Service Communication Flow**
```
Captain Command → Consolidated Messaging Service → PyAutoGUI Delivery → Agent Reception
                      ↓
               Agent Response → Status Update → Consolidated Agent Management
                      ↓
               Coordination → Swarm Intelligence → Task Assignment
```

### **Error Handling & Resilience**
```python
# All services include:
- Comprehensive logging
- Error recovery mechanisms
- Graceful degradation
- Status tracking and reporting
- Rollback capabilities
```

---

## **Captain Workflow with Consolidated Services**

### **Emergency Response Workflow**
```bash
# 1. Assess situation
python src/services/consolidated_agent_management_service.py --agent all --action status

# 2. Broadcast emergency
python src/services/consolidated_messaging_service.py --broadcast --message "EMERGENCY PROTOCOL ACTIVATED" --priority URGENT

# 3. Coordinate response
python src/services/consolidated_onboarding_service.py --status
python src/services/consolidated_handler_service.py --coordinate "emergency" --agent all
```

### **Phase Transition Workflow**
```bash
# 1. Verify readiness
python src/services/consolidated_agent_management_service.py --agent all --action status

# 2. Announce transition
python src/services/consolidated_messaging_service.py --broadcast --message "PHASE TRANSITION INITIATED" --priority HIGH

# 3. Execute migration
python src/services/final_consolidation_migration.py

# 4. Verify completion
python src/services/consolidated_onboarding_service.py --status
```

### **Quality Assurance Workflow**
```bash
# 1. Check compliance
python src/services/consolidated_architectural_service.py  # Import for validation

# 2. Review agent performance
python src/services/consolidated_agent_management_service.py --agent all --action performance

# 3. Update status
python src/services/consolidated_onboarding_service.py --assignments
```

---

## **Service Health Monitoring**

### **Automated Health Checks**
```bash
# Daily health verification:
python src/services/consolidated_messaging_service.py --health-check
python src/services/consolidated_agent_management_service.py --system-health
python src/services/consolidated_onboarding_service.py --status

# Weekly comprehensive audit:
python src/services/final_consolidation_migration.py  # Verify consolidation
python src/services/consolidated_handler_service.py --audit --agent all
```

### **Performance Metrics**
```python
# Key metrics tracked:
- Message delivery success rate (>99%)
- Agent response time (<30 seconds)
- System uptime (>99.9%)
- Consolidation progress (target: 60% reduction)
- V2 compliance violations (<5%)
```

---

**🐝 CONSOLIDATED SERVICES - UNIFIED SWARM CAPABILITIES!** ⚡🚀
