# 🚨 BROKEN COMPONENTS - QUARANTINE LIST

**Agent:** Agent-5 (Business Intelligence & Memory Safety Specialist)  
**Mission:** Systematic audit of broken components for swarm fix campaign  
**Status:** 🔄 IN PROGRESS (25% Complete)  
**Started:** 2025-10-15T10:45:00Z

---

## 📊 AUDIT PROGRESS

- ✅ **Phase 1 Complete (25%):** Test suite failures identified
- 🔄 **Phase 2 In Progress (50%):** Import/syntax errors scanning
- ⏳ **Phase 3 Pending (75%):** Service functionality testing
- ⏳ **Phase 4 Pending (100%):** Tool registry audit + final report

**⛽ GAS CHECKPOINT:** Sending 25% update to Captain!

---

## 🚨 CRITICAL ISSUES (BLOCKING)

### **C001: Domain Events Dataclass Error** 🔴
**Severity:** CRITICAL  
**Component:** `src/domain/domain_events.py`  
**Error:** `TypeError: non-default argument 'task_id' follows default argument`  
**Line:** 44  
**Impact:** Prevents entire domain module from loading  
**Fix Type:** Syntax fix (reorder dataclass fields)  
**Estimated Effort:** 5 minutes  
**Suggested Agent:** Agent-1 (Integration & Core Systems) or Agent-2 (Architecture)

**Technical Detail:**
```python
# PROBLEM: Line 44
@dataclass(frozen=True)
class TaskCreated(DomainEvent):
    task_id: TaskId  # ❌ No default after parent has defaults
    title: str
    priority: int
```

**Fix:** Reorder fields or add defaults to match parent class

---

## ⚠️ MAJOR ISSUES (HIGH PRIORITY)

### **M001: Test Import Errors - Missing Module Paths** 🟡
**Severity:** MAJOR  
**Components:** Multiple test files  
**Impact:** 311 tests collected, 5 ERROR imports  
**Fix Type:** Import path corrections  
**Estimated Effort:** 30 minutes

**Broken Tests:**
1. `tests/test_chatgpt_integration.py`
   - Error: `ModuleNotFoundError: No module named 'services'`
   - Fix: Change `from services.chatgpt.extractor` to `from src.services.chatgpt.extractor`

2. `tests/test_overnight_runner.py`
   - Error: `ModuleNotFoundError: No module named 'orchestrators'`
   - Fix: Change `from orchestrators.overnight.monitor` to `from src.orchestrators.overnight.monitor`

3. `tests/test_toolbelt.py`
   - Error: `ModuleNotFoundError: No module named 'core'`
   - Fix: Change `from core.unified_utilities` to `from src.core.unified_utilities`

4. `tests/test_vision.py`
   - Error: Import error (needs investigation)

**Suggested Agent:** Agent-3 (Infrastructure & DevOps) - Test infrastructure specialist

---

### **M002: DreamVault Runner - Undefined Names** 🟡
**Severity:** MAJOR  
**Component:** `src/ai_training/dreamvault/runner.py`  
**Errors:** 6+ undefined name errors (F821)  
**Impact:** DreamVault functionality broken

**Undefined Names:**
- Line 20: `RateLimiter` (undefined)
- Line 23: `JobQueue` (undefined)
- Line 24: `Redactor` (undefined)
- Line 25: `Summarizer` (undefined)
- Line 26: `EmbeddingBuilder` (undefined)
- Line 27: (truncated, more errors likely)

**Fix Type:** Missing imports or undefined classes  
**Estimated Effort:** 1 hour (investigation + implementation)  
**Suggested Agent:** Agent-5 (me!) or Agent-7 (Web/Full-stack)

---

## 📋 CONTINUING AUDIT...

**Next Steps:**
1. ⏳ Complete linter scan for all syntax/import errors
2. ⏳ Test critical services (messaging, Discord, database)
3. ⏳ Audit tool registry for broken tools
4. ⏳ Create prioritized fix list with agent assignments

**Status:** 25% complete, continuing systematic scan...

---

## 🎯 PRELIMINARY FIX ASSIGNMENTS

### **Sprint 1: Critical Blockers (URGENT)**
**Target:** Unblock domain module and core functionality

| Issue | Component | Severity | Agent | Effort |
|-------|-----------|----------|-------|--------|
| C001 | domain_events.py | CRITICAL | Agent-1/2 | 5 min |

### **Sprint 2: Test Infrastructure (HIGH)**
**Target:** Fix test imports, enable test suite

| Issue | Component | Severity | Agent | Effort |
|-------|-----------|----------|-------|--------|
| M001 | 4 test files | MAJOR | Agent-3 | 30 min |

### **Sprint 3: Feature Modules (MEDIUM)**
**Target:** Fix broken features

| Issue | Component | Severity | Agent | Effort |
|-------|-----------|----------|-------|--------|
| M002 | DreamVault runner | MAJOR | Agent-5/7 | 1 hour |

---

## 📊 STATISTICS (PRELIMINARY)

**Errors Found So Far:**
- 🔴 **CRITICAL:** 1 (domain events blocking)
- 🟡 **MAJOR:** 2 (10+ broken imports/tests)
- 🟢 **MINOR:** TBD (continuing scan)

**Total Broken Components:** 3+ (audit in progress)

**Test Suite Status:**
- Collected: 311 tests
- Import Errors: 5 test files
- Status: ❌ BLOCKED (can't run tests until imports fixed)

---

## ⛽ GAS DELIVERY - 25% CHECKPOINT

**Progress Update for Captain:**
- ✅ Test suite scanned - 5 import errors found
- ✅ Domain module critical error identified
- ✅ Linter scan started - undefined names in DreamVault
- 🔄 Continuing systematic audit...

**Next Gas Delivery:** At 50% (service testing complete)

---

**Audit continues... More findings coming!**

*This is a LIVE document - updating as audit progresses*

