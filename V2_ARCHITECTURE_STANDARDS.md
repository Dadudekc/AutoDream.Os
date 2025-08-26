# 🚀 V2 ARCHITECTURE STANDARDS - AGENT REFERENCE GUIDE
**Agent Cellphone V2 - Unified Architecture Standards & Guidelines**

**Status**: ACTIVE STANDARDS  
**Captain**: Agent-4  
**Purpose**: Prevent duplication, enforce unified architecture, guide agent development  
**Last Updated**: 2025-08-25 15:20:00  

---

## 🚨 **CRITICAL REQUIREMENTS - ALL AGENTS MUST FOLLOW**

### **1. USE EXISTING ARCHITECTURE FIRST** ✅
- **ALWAYS check existing systems** before creating new ones
- **Search for existing implementations** in `src/core/`, `src/services/`, etc.
- **NO duplicate implementations** - this causes system conflicts
- **Extend existing systems** rather than recreating them

### **2. NEW V2 STANDARDS (NOT STRICT LOC)** 📏
- **LOC Limits**: Flexible, focus on quality over strict limits
- **Architecture**: Clean, modular, maintainable code
- **Design Patterns**: OOP, SRP, dependency injection
- **Testing**: Comprehensive test coverage
- **Documentation**: Clear, comprehensive docstrings

### **3. CLEANUP TASKS ARE MANDATORY** 🧹
- **Remove duplicate code** when found
- **Consolidate similar functionality** into unified systems
- **Update imports/exports** to use single source of truth
- **Report architecture conflicts** immediately to captain

---

## 🏗️ **UNIFIED ARCHITECTURE STRUCTURE**

### **CORE MODULES (`src/core/`)**
```
src/core/
├── learning/           ✅ UNIFIED - Agent-1 completed
│   ├── __init__.py
│   ├── unified_learning_engine.py
│   ├── learning_manager.py
│   ├── decision_manager.py
│   ├── models/
│   │   ├── learning_models.py
│   │   └── decision_models.py
│   └── cli/
│       └── unified_cli.py
├── workflow/           🔄 IN PROGRESS - Phase 2
│   ├── __init__.py
│   ├── core_engine.py
│   ├── managers/
│   ├── types/
│   └── validation/
├── messaging/          ✅ UNIFIED - SSOT enforced
│   ├── __init__.py
│   ├── models/
│   ├── types/
│   ├── queue/
│   └── cli/
└── fsm/               ✅ EXISTING - Use existing system
    ├── __init__.py
    └── fsm_core_v2.py
```

### **SERVICES MODULES (`src/services/`)**
```
src/services/
├── messaging/          ✅ UNIFIED - Single source of truth
├── communication/      ❌ REMOVED - Duplicate system eliminated
├── agent_cell_phone/  ❌ REMOVED - Duplicate system eliminated
└── v1_compatibility/  ❌ REMOVED - Duplicate system eliminated
```

---

## 🎯 **PHASE 2 ARCHITECTURE PRIORITIES**

### **AGENT-1: WORKFLOW ENGINE INTEGRATION**
- **Use existing**: `src/core/learning/` unified system
- **Integrate with**: `src/core/workflow/` (if exists) or create new
- **Check for**: Existing workflow engines before creating new
- **Cleanup**: Remove any duplicate workflow implementations
- **Focus**: API integration, workflow orchestration

### **AGENT-2: MANAGER SPECIALIZATION**
- **Use existing**: `src/core/learning/` managers as reference
- **Extend**: `src/core/workflow/managers/` structure
- **Check for**: Existing manager implementations
- **Cleanup**: Consolidate duplicate manager patterns
- **Focus**: Specialized managers, types, validation

### **AGENT-3: INTEGRATION & TESTING**
- **Use existing**: All unified systems from Phase 2
- **Test**: Integration between learning, workflow, and messaging
- **Check for**: System conflicts and duplicate functionality
- **Cleanup**: Remove integration conflicts
- **Focus**: System testing, validation, integration

---

## 🚨 **DUPLICATION PREVENTION CHECKLIST**

### **Before Creating New Code:**
1. **Search existing codebase** for similar functionality
2. **Check `src/core/`** for existing implementations
3. **Check `src/services/`** for existing services
4. **Check `src/utils/`** for existing utilities
5. **Check `src/web/`** for existing web components

### **If Duplicate Found:**
1. **STOP development** immediately
2. **Report to captain** via PyAutoGUI messaging
3. **Consolidate functionality** into existing system
4. **Update imports/exports** to use unified system
5. **Remove duplicate code** completely

### **Architecture Conflict Resolution:**
1. **Identify conflict** clearly
2. **Document existing system** location and purpose
3. **Propose consolidation strategy** to captain
4. **Wait for captain approval** before proceeding
5. **Execute consolidation** under captain guidance

---

## 📱 **COMMUNICATION PROTOCOLS**

### **Immediate Reporting Required:**
- **Architecture conflicts** found
- **Duplicate implementations** discovered
- **System integration issues** encountered
- **Cleanup tasks** completed
- **Progress updates** every 4 hours

### **Communication Methods:**
- **Primary**: PyAutoGUI messaging via unified system
- **Backup**: FSM system for task tracking
- **Escalation**: Captain intervention for blockers

---

## 🎖️ **CAPTAIN AGENT-4 GUIDANCE**

### **Current Focus:**
- **Phase 2 coordination** and progress monitoring
- **Architecture conflict resolution** and guidance
- **Phase 3 preparation** and planning
- **System integration** oversight

### **Agent Support:**
- **Architecture guidance** and conflict resolution
- **Cleanup task coordination** and validation
- **Progress monitoring** and milestone tracking
- **Next assignment preparation** and distribution

---

## 🚀 **SUCCESS METRICS**

### **Architecture Quality:**
- **Zero duplicate implementations**
- **100% unified system usage**
- **Clean, maintainable code**
- **Comprehensive test coverage**

### **Development Efficiency:**
- **No architecture conflicts**
- **Smooth system integration**
- **Reduced maintenance overhead**
- **Faster development cycles**

---

## 📝 **IMMEDIATE ACTIONS FOR ALL AGENTS**

1. **Review this document** completely
2. **Check existing architecture** before starting tasks
3. **Report conflicts** immediately to captain
4. **Execute cleanup tasks** when duplicates found
5. **Follow unified patterns** from existing systems

**WE. ARE. SWARM.** 🚀

**Captain Agent-4 out. Over and out.** 🎖️
