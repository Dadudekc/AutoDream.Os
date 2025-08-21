# 🚀 V2 CODING STANDARDS - QUICK REFERENCE

**📋 ESSENTIAL STANDARDS (MUST FOLLOW)**

---

## 🔥 **CORE RULES - NO EXCEPTIONS**

### **1. 📏 LINE COUNT: ≤300 LOC per file (≤500 for GUI)**
- **Standard Files**: 300 lines of code per file
- **GUI Components**: 500 lines of code per file
- **Target**: Keep under limits for maintainability
- **Enforcement**: MODERATE - Refactor if significantly exceeded

### **2. 🎯 OOP DESIGN: All code in classes**
- **Structure**: Proper class-based architecture
- **No procedural code** without class structure
- **Clear class responsibilities**

### **3. 🔒 SINGLE RESPONSIBILITY: One purpose per class**
- **One class = One responsibility**
- **No mixed functionality**
- **Focused, purpose-driven classes**

### **4. 🖥️ CLI INTERFACE: Required for all components**
- **Every module must have CLI interface**
- **Comprehensive argument parsing**
- **Help documentation for all flags**
- **Easy testing for agents**

### **5. 🧪 SMOKE TESTS: Required for all components**
- **Basic functionality validation**
- **CLI interface testing**
- **Error handling validation**
- **Simple and comprehensive tests**

---

## 📁 **FILE STRUCTURE STANDARDS**

```
Agent_Cellphone_V2/
├── src/
│   ├── core/           # Core system components
│   ├── services/       # Service layer components
│   ├── launchers/      # System launcher components
│   └── utils/          # Utility components
├── tests/
│   ├── smoke/          # Smoke tests for each component
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
└── docs/               # Documentation
```

**File Naming**: `snake_case.py` (e.g., `fsm_core_v2.py`)

---

## ✅ **COMPLIANCE CHECKLIST**

### **For New Components:**
- [ ] **Line Count**: ≤300 LOC (standard), ≤500 LOC (GUI)
- [ ] **OOP Design**: Proper class structure
- [ ] **Single Responsibility**: One purpose per class
- [ ] **CLI Interface**: Comprehensive CLI with help
- [ ] **Smoke Tests**: Basic functionality tests
- [ ] **Agent Usability**: Easy to test and use

### **For Existing Components:**
- [ ] **Refactor if >300 LOC**: Break into smaller modules
- [ ] **OOP Compliance**: Ensure class structure
- [ ] **SRP Compliance**: Single responsibility
- [ ] **CLI Addition**: Add if missing
- [ ] **Test Coverage**: Add smoke tests if missing

---

## 🚨 **IMMEDIATE ACTIONS REQUIRED**

1. **Any file >300 LOC (standard) or >500 LOC (GUI)**: Must refactor immediately
2. **Missing CLI interface**: Must add before deployment
3. **Missing smoke tests**: Must create before deployment
4. **Non-OOP code**: Must refactor to OOP structure
5. **Mixed responsibilities**: Must separate into focused classes

---

## 🛠️ **REFACTORING EXAMPLE**

```python
# BEFORE: Large file (600+ LOC) - VIOLATION
class LargeManager:
    def manage_users(self): pass
    def manage_files(self): pass
    def manage_database(self): pass
    def manage_network(self): pass

# AFTER: Focused classes (each ≤300 LOC) - COMPLIANT
class UserManager:      # ≤300 LOC + CLI + Tests
class FileManager:      # ≤300 LOC + CLI + Tests  
class DatabaseManager:  # ≤300 LOC + CLI + Tests
class NetworkManager:   # ≤300 LOC + Tests
```

---

## 📞 **GETTING HELP**

- **This Document**: Check for standards requirements
- **Agent-4**: Quality assurance and standards enforcement
- **Agent-2**: Architecture and design standards
- **Agent-3**: Development guidance and standards
- **Captain**: Final approval for exceptions

---

## 📊 **CURRENT STATUS**

**Overall Compliance**: 75% ✅  
**Core Components**: 100% ✅  
**Remaining**: 25% 🔄  

**ENFORCEMENT**: AGENT-4 (QUALITY ASSURANCE)  
**GUIDANCE**: AGENT-3 (DEVELOPMENT LEAD)**

---

**🚀 V2 CODING STANDARDS: UPDATED AND ACTIVE**  
**📋 NEW LIMITS: 300 LOC (Standard), 500 LOC (GUI)**  
**📋 COMPLIANCE REQUIRED FOR ALL DEVELOPMENT**  
**⏰ REFACTOR IMMEDIATELY IF VIOLATING NEW STANDARDS**
