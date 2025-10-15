# 🔧 V2 Refactor Plan: messaging_infrastructure.py

**File:** `src/services/messaging_infrastructure.py`  
**Current Size:** 489 lines  
**Status:** MAJOR V2 VIOLATION (401-600 lines)  
**Target:** Split into <400 line modules  
**Agent:** Agent-7 (Web Development Specialist)

---

## 📊 **File Structure Analysis**

### **Current Sections:**
1. **Message Templates** (Lines 32-125) - ~93 lines
2. **CLI Parser** (Lines 131-235) - ~104 lines
3. **PyAutoGUI Helpers** (Lines 242-321) - ~79 lines
4. **Message Handlers** (Lines 323-475) - ~152 lines
5. **Main Service Class** (Lines 482-582) - ~100 lines
6. **Discord Integration** (Lines 584-595) - ~11 lines

---

## 🎯 **Refactoring Strategy**

### **Extract into 3 modules:**

1. **`messaging_templates.py`** (~100 lines)
   - All message templates
   - Template formatters
   - CLI help text

2. **`messaging_handlers.py`** (~200 lines)
   - All handle_* functions
   - PyAutoGUI helpers
   - MessageCoordinator class

3. **`messaging_infrastructure.py`** (~200 lines)
   - create_messaging_parser
   - ConsolidatedMessagingService
   - Main entry point
   - Imports from other modules

---

## ✅ **Benefits**

- ✅ V2 Compliance: 489 → 3 files @ ~150-200 lines each
- ✅ Clear separation of concerns
- ✅ Easier testing and maintenance
- ✅ Reusable components

---

## 🚀 **Execution Plan**

1. Create `messaging_templates.py` with all templates
2. Create `messaging_handlers.py` with all handlers
3. Refactor `messaging_infrastructure.py` to import from modules
4. Run linter to verify no errors
5. Update imports in dependent files

---

**Status:** READY TO EXECUTE

