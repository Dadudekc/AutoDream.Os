# ❌ BROKEN TOOLS REGISTRY - SYSTEMATIC DOCUMENTATION

**Agent:** Agent-1 - Integration & Core Systems Specialist  
**Mission:** Toolbelt validation - Document all broken tools  
**Date:** 2025-10-15  
**Strategy:** Option D - Document & continue testing

---

## 🔴 **BROKEN TOOLS - REQUIRES FIX**

### **1. tools/agent_checkin.py** ❌ **SEVERELY CORRUPTED**
**Status:** BROKEN - NEEDS COMPLETE REWRITE OR GIT RESTORE  
**Priority:** HIGH (critical agent check-in system)

**Issues Found:**
1. ❌ Wrong import: `from core.unified_utilities` → should be `from src.utils.unified_utilities`
2. ❌ Importing non-existent `get_unified_validator()`
3. ❌ Importing non-existent `write_json()` function (it's `FileUtils.write_json()`)
4. ❌ Corrupted code: `parser.get_unified_utility().parse_args()` (nonsense!)
5. ❌ Corrupted code: `get_unified_utility().Path(src)` (Path already imported!)
6. ❌ Corrupted code: `get_unified_utility().remove(tmp_path)` (should be os.remove!)
7. ❌ Wrong function call: `get_unified_validator().raise_validation_error()` (doesn't exist)

**Root Cause:** Bad automated refactor replaced standard Python calls with `get_unified_utility().X()` nonsense

**Recommended Fix:** Restore from git history (find last working version)

**Error Output:**
```
AttributeError: 'ArgumentParser' object has no attribute 'get_unified_utility'
```

---

### **2. tools/captain_snapshot.py** ❌ **BROKEN**
**Status:** BROKEN - IMPORT PATH ISSUE  
**Priority:** MEDIUM (Captain monitoring tool)

**Issues Found:**
1. ❌ Wrong import: `from core.unified_utilities` → should be `from src.utils.unified_utilities`

**Recommended Fix:** Simple import path correction + sys.path fix

**Error Output:**
```
ModuleNotFoundError: No module named 'src.utils.unified_utilities'
```

---

### **3. tools/toolbelt.py** ❌ **BROKEN (Chain Import Failure)**
**Status:** BROKEN - INDIRECT FAILURE  
**Priority:** HIGH (main toolbelt interface)

**Issues Found:**
1. ❌ Chain import failure: imports from `tools.__init__.py` → `agent_checkin.py` (which is broken)

**Recommended Fix:** Fix agent_checkin.py first, then this should work

**Error Output:**
```
ModuleNotFoundError: No module named 'core' (via tools/__init__.py)
```

---

## ✅ **WORKING TOOLS - CONFIRMED FUNCTIONAL**

### **1. tools/captain_check_agent_status.py** ✅
**Status:** WORKING PERFECTLY  
**Tested:** Successfully scans all 8 agents  
**Notes:** Clean implementation, no problematic imports

---

### **2. tools/v2_compliance_checker.py** ✅
**Status:** WORKING PERFECTLY  
**Tested:** Help system functional, all flags operational  
**Notes:** Clean implementation

---

### **3. tools_v2/categories/swarm_state_reader.py** ✅
**Status:** WORKING (as module)  
**Tested:** Runs without errors as module import  
**Notes:** V2 tools appear cleaner than legacy tools/

---

## 📊 **TESTING STATISTICS**

**Total Tools Estimated:** 200+  
**Tools Tested:** 6  
**Working:** 3 (50%)  
**Broken:** 3 (50%)  

**Critical Corruption:** 1 tool (agent_checkin.py - SEVERE)  
**Simple Import Issues:** 2 tools (captain_snapshot.py, toolbelt.py)

---

## 🎯 **TESTING STRATEGY - CONTINUING**

### **Next Tools to Test (Phase 1 - Critical Captain Tools):**
1. ⏭️ captain_hard_onboard_agent.py
2. ⏭️ captain_find_idle_agents.py
3. ⏭️ captain_gas_check.py
4. ⏭️ captain_message_all_agents.py

### **Next Tools to Test (Phase 2 - Agent Core Tools):**
5. ⏭️ agent_fuel_monitor.py
6. ⏭️ agent_lifecycle_automator.py
7. ⏭️ agent_status_quick_check.py
8. ⏭️ toolbelt_runner.py

---

## 🔍 **PATTERNS EMERGING**

### **Pattern 1: Legacy tools/ vs tools_v2/**
- **tools_v2/** appears cleaner (swarm_state_reader.py works)
- **tools/** has more corruption (agent_checkin.py severely broken)

**Hypothesis:** Bad refactor only affected tools/, not tools_v2/

### **Pattern 2: Corruption Type**
- Simple import path issues: Fixable quickly
- Systematic corruption: Requires git restore or complete rewrite

### **Pattern 3: Working Tools**
- Tools without `get_unified_utility()` calls work fine
- Tools with standard Python imports work fine

---

## 📋 **SCOPE ASSESSMENT**

### **Best Case:** 10-20 tools broken (mostly import issues)
### **Worst Case:** 50-100 tools broken (widespread corruption)
### **Most Likely:** 20-30 tools broken (mix of issues)

**Will know more after testing 20+ tools...**

---

## 🚀 **CONTINUING SYSTEMATIC TESTING**

**Current Phase:** Testing critical Captain tools  
**Next:** Test 10 more tools to understand scope  
**Then:** Compile comprehensive report with fix strategy

---

**#BROKEN-TOOLS #DOCUMENTATION #SYSTEMATIC-TESTING #OPTION-D**

