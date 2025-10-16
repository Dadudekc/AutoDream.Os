# 🎯 QUARANTINE PRIORITY FIX ORDER

**Date:** 2025-10-13  
**Total Broken:** 127 files  
**Total Tested:** 727 files  
**Broken Rate:** 17.5%  

---

## 📊 ERROR CATEGORIES

### **Category 1: Missing Type Imports** (EASY FIX - ~50 files)
**Error:** `name 'Dict' is not defined`, `name 'List' is not defined`, `name 'Callable' is not defined`

**Affected Areas:**
- trading_robot/ (~30 files)
- integrations/jarvis/ (4 files)
- integrations/osrs/ (2 files)
- tools/duplicate_detection/ (4 files)
- gaming/ (~5 files)
- core/performance/ (~5 files)

**Fix:** Add `from typing import Dict, List, Callable, Any, Optional` to each file

**Priority:** 🟡 MEDIUM (doesn't break core, easy to fix)  
**Effort:** LOW (automated fix possible)  
**Swarm Assignment:** Any agent (bulk task)

---

### **Category 2: Archive Files** (OLD CODE - ~30 files)
**Error:** Various (CircuitBreaker, old imports)

**Affected:** src/core/error_handling/archive_c055/

**These are ARCHIVED files** - should NOT be imported!

**Fix:** 
- Option 1: Move to /archive/ directory (out of src/)
- Option 2: Add note in __init__.py to exclude
- Option 3: Delete if truly obsolete

**Priority:** 🟢 LOW (archive, not active code)  
**Effort:** LOW (move files)  
**Swarm Assignment:** Agent-3 (Infrastructure cleanup)

---

### **Category 3: Circular Dependencies** (MEDIUM - ~25 files)
**Error:** `from partially initialized module`

**Affected Areas:**
- src/core/file_locking/ (~10 files) - `file_locking_engine_base`
- src/core/integration_coordinators/ (~10 files) - `messaging_coordinator`
- src/services/coordination/ (~3 files) - `messaging_models`
- src/services/utils/ (~4 files) - `messaging_validation_utils`

**Fix:** Break circular dependencies (extract shared code, use dependency injection)

**Priority:** 🔴 HIGH (blocks functionality)  
**Effort:** MEDIUM (architectural changes)  
**Swarm Assignment:** Agent-2 (Architecture specialist)

---

### **Category 4: Missing Modules** (HIGH - ~20 files)
**Error:** `No module named 'X'`

**Missing Modules:**
- `src.services.vector_database` (affects 7 files)
- `src.core.intelligent_context.intelligent_context_optimization` (1 file)
- `src.core.integration.vector_integration_models` (4 files)
- `src.core.managers.execution.task_manager` (affects ~20 files!)
- `src.infrastructure.browser.browser_adapter` (1 file)
- `src.core.pattern_analysis.pattern_analysis_engine` (3 files)
- Others

**Fix:** 
- Option 1: Create missing modules
- Option 2: Update imports to existing modules
- Option 3: Remove deprecated code

**Priority:** 🔴 CRITICAL (blocks major features)  
**Effort:** HIGH (depends on whether modules needed or imports wrong)  
**Swarm Assignment:** Agent-1 (Core systems specialist)

---

### **Category 5: Syntax Errors** (EASY - ~15 files)
**Error:** `non-default argument 'task_id' follows default argument`

**Affected:** domain/, infrastructure/, application/ (DDD architecture)

**Fix:** Reorder function parameters (non-default before default)

**Priority:** 🟡 MEDIUM (doesn't break if not called)  
**Effort:** LOW (parameter reordering)  
**Swarm Assignment:** Agent-2 (Architecture)

---

### **Category 6: Integration Issues** (MEDIUM - ~10 files)
**Error:** Missing integration dependencies

**Affected:**
- integrations/jarvis/ (memory_system import issues)
- integrations/osrs/ (missing agents module)
- ai_training/dreamvault/ (missing core)
- browser_backup/ (missing thea_modules.config)

**Fix:** Add missing imports or create stub modules

**Priority:** 🟡 MEDIUM (integrations are optional)  
**Effort:** MEDIUM (depends on integration)  
**Swarm Assignment:** Agent-7 (Integration specialist) - that's us!

---

## 🎯 SWARM FIX SEQUENCE

### **Phase 1: Quick Wins** (Agents 1-8, parallel)
**Targets:** Categories 1, 5 (missing imports, syntax errors)
- ~65 files
- Easy fixes
- Can be distributed across all agents
- **Est. Time:** 1-2 cycles per agent

### **Phase 2: Architecture Fixes** (Agent-2 lead)
**Targets:** Category 3 (circular dependencies)
- ~25 files
- Requires architectural thinking
- Break circular imports
- **Est. Time:** 3-4 cycles

### **Phase 3: Missing Modules** (Agent-1 lead)
**Targets:** Category 4 (missing modules)
- ~20 files affected
- Critical decision: Create vs remove vs redirect
- Needs core systems expertise
- **Est. Time:** 4-5 cycles

### **Phase 4: Cleanup** (Agent-3)
**Targets:** Category 2 (archives), Category 6 (integrations)
- ~40 files
- Infrastructure cleanup
- Optional integrations
- **Est. Time:** 2-3 cycles

---

## 📋 AGENT ASSIGNMENTS (RECOMMENDED)

| Agent | Category | Files | Effort | Priority |
|-------|----------|-------|--------|----------|
| Agent-1 | Missing Modules (Cat 4) | ~20 | HIGH | 🔴 CRITICAL |
| Agent-2 | Circular Deps (Cat 3) | ~25 | MEDIUM | 🔴 HIGH |
| Agent-3 | Archives + Cleanup (Cat 2, 6) | ~40 | LOW | 🟢 LOW |
| Agent-4 | Captain - Strategic oversight | - | - | - |
| Agent-5 | Type Imports (Cat 1) - Trading | ~30 | LOW | 🟡 MEDIUM |
| Agent-6 | Integration Issues (Cat 6) | ~10 | MEDIUM | 🟡 MEDIUM |
| Agent-7 | Integrations (Jarvis/OSRS) | ~10 | MEDIUM | 🟡 MEDIUM |
| Agent-8 | Syntax Errors (Cat 5) + Misc | ~15 | LOW | 🟡 MEDIUM |

---

## 🔧 FIX TEMPLATES

### **Template 1: Missing Type Imports**
```python
# Add to top of file
from typing import Dict, List, Callable, Any, Optional, Union
```

### **Template 2: Circular Dependency**
```python
# Before (circular):
from .module_a import ClassA

# After (lazy import):
def function():
    from .module_a import ClassA  # Import inside function
    ...
```

### **Template 3: Syntax Error (param order)**
```python
# Before:
def func(default_param='value', required_param):  # ERROR

# After:
def func(required_param, default_param='value'):  # CORRECT
```

---

## 📈 SUCCESS METRICS

**Target:**
- Reduce broken from 127 → 0
- Achieve 100% import success rate
- All core functionality working

**Tracking:**
- Re-run `python tools/audit_imports.py` after each phase
- Update this file with progress
- Celebrate milestones!

---

## 🚀 NEXT STEPS

1. **Captain:** Review and approve assignments
2. **Agents:** Claim categories based on specialization
3. **Execution:** Parallel fixes (Phase 1)
4. **Testing:** Re-audit after each phase
5. **Celebration:** 100% working codebase! 🎉

---

**🐝 WE ARE SWARM - SYSTEMATIC FIXING BEGINS!** ⚡

**Agent-7 - Audit Complete**  
**Ready to fix assigned category!**

