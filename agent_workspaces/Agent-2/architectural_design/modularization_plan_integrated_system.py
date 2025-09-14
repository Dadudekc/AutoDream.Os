# Modularization Plan: integrated_onboarding_coordination_system.py (906 lines)

## 🎯 **CRITICAL FILE MODULARIZATION PLAN**

**Target File:** `integrated_onboarding_coordination_system.py`  
**Current Size:** 906 lines (CRITICAL V2 VIOLATION)  
**Target:** ≤400 lines per module  
**Strategy:** Extract 5 major components into separate modules  

## 📊 **Component Analysis**

### **1. Agent State Management (Lines 51-62)**
- **Component:** `AgentState` enum
- **Size:** ~12 lines
- **Extract to:** `src/core/fsm/agent_state.py`

### **2. Contract System (Lines 63-100)**
- **Components:** `ContractType` enum, `AgentContract` class
- **Size:** ~38 lines
- **Extract to:** `src/core/contracts/agent_contract.py`

### **3. FSM System (Lines 101-133)**
- **Component:** `AgentFSM` class
- **Size:** ~33 lines
- **Extract to:** `src/core/fsm/agent_fsm.py`

### **4. Main System Class (Lines 134-943)**
- **Component:** `IntegratedOnboardingCoordinationSystem` class
- **Size:** ~810 lines (STILL TOO LARGE)
- **Strategy:** Further decompose into multiple services

### **5. Main Function (Lines 944-906)**
- **Component:** `main()` function and CLI interface
- **Size:** ~60 lines
- **Extract to:** `src/services/integrated_system_runner.py`

## 🏗️ **Modularization Strategy**

### **Phase 1: Extract Core Components**
1. **Agent State Enum** → `src/core/fsm/agent_state.py`
2. **Contract System** → `src/core/contracts/agent_contract.py`
3. **FSM System** → `src/core/fsm/agent_fsm.py`
4. **Main Function** → `src/services/integrated_system_runner.py`

### **Phase 2: Decompose Main System Class**
The `IntegratedOnboardingCoordinationSystem` class (810 lines) needs further decomposition:

#### **2.1 Onboarding Service (Lines 134-300)**
- **Extract to:** `src/services/onboarding/onboarding_service.py`
- **Responsibilities:** Agent onboarding, workspace initialization

#### **2.2 Contract Management Service (Lines 301-500)**
- **Extract to:** `src/services/contracts/contract_management_service.py`
- **Responsibilities:** Contract creation, tracking, completion

#### **2.3 FSM Management Service (Lines 501-700)**
- **Extract to:** `src/services/fsm/fsm_management_service.py`
- **Responsibilities:** State transitions, FSM coordination

#### **2.4 Cycle Coordination Service (Lines 701-900)**
- **Extract to:** `src/services/coordination/cycle_coordination_service.py`
- **Responsibilities:** Cycle management, agent coordination

#### **2.5 PyAutoGUI Integration Service (Lines 901-943)**
- **Extract to:** `src/services/automation/pyautogui_service.py`
- **Responsibilities:** PyAutoGUI automation, coordinate management

### **Phase 3: Create Integration Layer**
- **Main System** → `src/services/integrated_system.py` (≤200 lines)
- **Responsibilities:** Service orchestration, dependency injection

## 📋 **File Structure After Modularization**

```
src/
├── core/
│   ├── fsm/
│   │   ├── __init__.py
│   │   ├── agent_state.py          # AgentState enum (≤50 lines)
│   │   └── agent_fsm.py            # AgentFSM class (≤100 lines)
│   └── contracts/
│       ├── __init__.py
│       └── agent_contract.py       # ContractType, AgentContract (≤100 lines)
├── services/
│   ├── onboarding/
│   │   ├── __init__.py
│   │   └── onboarding_service.py   # Onboarding logic (≤300 lines)
│   ├── contracts/
│   │   ├── __init__.py
│   │   └── contract_management_service.py  # Contract management (≤300 lines)
│   ├── fsm/
│   │   ├── __init__.py
│   │   └── fsm_management_service.py       # FSM management (≤300 lines)
│   ├── coordination/
│   │   ├── __init__.py
│   │   └── cycle_coordination_service.py   # Cycle coordination (≤300 lines)
│   ├── automation/
│   │   ├── __init__.py
│   │   └── pyautogui_service.py            # PyAutoGUI integration (≤200 lines)
│   ├── integrated_system.py                # Main orchestration (≤200 lines)
│   └── integrated_system_runner.py         # CLI interface (≤100 lines)
```

## 🎯 **V2 Compliance Targets**

### **File Size Compliance**
- **All modules:** ≤400 lines ✅
- **Most modules:** ≤300 lines ✅
- **Core components:** ≤100 lines ✅

### **Design Pattern Implementation**
1. **Service Layer Pattern** - Each service has single responsibility
2. **Factory Pattern** - Service creation and dependency injection
3. **Repository Pattern** - Contract and state persistence
4. **Observer Pattern** - State change notifications
5. **Strategy Pattern** - Different coordination strategies

### **SSOT Compliance**
- **Single Source of Truth** for each component
- **Clear interfaces** between modules
- **Dependency injection** for loose coupling
- **Configuration management** centralized

## 📊 **Implementation Priority**

### **Priority 1: Core Components (Immediate)**
1. Extract `AgentState` enum
2. Extract `ContractType` and `AgentContract`
3. Extract `AgentFSM` class

### **Priority 2: Service Decomposition (Next)**
1. Extract onboarding service
2. Extract contract management service
3. Extract FSM management service

### **Priority 3: Integration & Testing (Final)**
1. Create integration layer
2. Implement dependency injection
3. Add comprehensive tests

## 🚀 **Expected Outcomes**

### **V2 Compliance Achievement**
- **Original:** 1 file, 906 lines (CRITICAL VIOLATION)
- **After Modularization:** 11 files, all ≤400 lines (V2 COMPLIANT)

### **Architectural Benefits**
- **Single Responsibility** - Each module has one clear purpose
- **Loose Coupling** - Services communicate through interfaces
- **High Cohesion** - Related functionality grouped together
- **Testability** - Each component can be tested independently
- **Maintainability** - Changes isolated to specific modules

**Status:** Ready for immediate implementation

---
*Generated by Agent-2 - Architecture & Design Specialist*  
*Critical File Modularization Plan - V2 Compliance Mission*