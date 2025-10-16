# Toolbelt Quarantine System
## 29 Tools Need Fixing (71% Working, 29% Broken)

---

## 🚨 QUARANTINE STATUS

**Last Audit:** October 14, 2025  
**Total Tools:** 100  
**Working:** 71 (71%)  
**Quarantined:** 29 (29%)  

---

## 📋 BROKEN TOOLS BY CATEGORY

### 🧠 Brain Tools (5 tools) - **HIGH PRIORITY**
```
❌ brain.get
❌ brain.note
❌ brain.search
❌ brain.session
❌ brain.share
```
**Issue:** Missing `get_spec()` and `validate()` methods  
**Impact:** Swarm brain integration broken  
**Assigned To:** Available for claiming

---

### 💬 Discord Tools (3 tools) - **MEDIUM PRIORITY**
```
❌ discord.health
❌ discord.start
❌ discord.test
```
**Issue:** Missing `get_spec()` and `validate()` methods  
**Impact:** Discord bot integration broken  
**Assigned To:** Available for claiming

---

### 🏗️ Infrastructure Tools (4 tools) - **MEDIUM PRIORITY**
```
❌ infra.extract_planner
❌ infra.file_lines
❌ infra.orchestrator_scan
❌ infra.roi_calc
```
**Issue:** Missing `get_spec()` and `validate()` methods  
**Impact:** Infrastructure analysis tools broken  
**Assigned To:** Available for claiming

---

### 📨 Message-Task Tools (3 tools) - **MEDIUM PRIORITY**
```
❌ msgtask.fingerprint
❌ msgtask.ingest
❌ msgtask.parse
```
**Issue:** Missing `get_spec()` and `validate()` methods  
**Impact:** Message-to-task conversion broken  
**Assigned To:** Available for claiming

---

### 📊 Observability Tools (4 tools) - **LOW PRIORITY**
```
❌ obs.get
❌ obs.health
❌ obs.metrics
❌ obs.slo
```
**Issue:** Missing `get_spec()` and `validate()` methods  
**Impact:** Metrics monitoring broken  
**Assigned To:** Available for claiming

---

### 🌐 OSS Tools (5 tools) - **LOW PRIORITY**
```
❌ oss.clone
❌ oss.import
❌ oss.issues
❌ oss.portfolio
❌ oss.status
```
**Issue:** Missing `get_spec()` and `validate()` methods  
**Impact:** Open source contribution tools broken  
**Assigned To:** Available for claiming

---

### ✅ Validation Tools (4 tools) - **MEDIUM PRIORITY**
```
❌ val.flags
❌ val.report
❌ val.rollback
❌ val.smoke
```
**Issue:** Missing `get_spec()` and `validate()` methods  
**Impact:** Validation framework broken  
**Assigned To:** Available for claiming

---

### 🧪 Test Pyramid (1 tool) - **LOW PRIORITY**
```
❌ test.pyramid_check
```
**Issue:** Import error - class not found in module  
**Impact:** Test pyramid validation broken  
**Assigned To:** Available for claiming

---

## 🔧 HOW TO FIX

### Standard Fix (28 tools with TypeError)

All 28 tools need the same fix - add two methods:

```python
def get_spec(self):
    from ..adapters.base_adapter import ToolSpec
    return ToolSpec(
        name="category.toolname",
        version="1.0.0",
        category="category",
        summary="Brief description",
        required_params=["param1"],
        optional_params={"param2": "default"}
    )

def validate(self, params: dict) -> tuple[bool, list[str]]:
    # Check required params
    missing = [p for p in self.get_spec().required_params if p not in params]
    return (len(missing) == 0, missing)
```

**Reference Implementation:** See `tools_v2/categories/coordination_tools.py` (Agent-1's tools)

---

### Special Fix (1 tool with ToolNotFoundError)

**test.pyramid_check:**
- Issue: Class name mismatch in module
- Fix: Update class name in module or registry

---

## 📊 WORKING TOOLS (71 tools) ✅

These tools are fully operational:

**Integration (4):** integration.* - All Agent-1 tools working!  
**Coordination (3):** coord.* - Pattern #5 tools working!  
**Config (3):** config.* - SSOT validation tools working!  
**Advisor (4):** advisor.* - All working  
**Agent (3):** agent.* - All working  
**Analysis (3):** analysis.* - All working  
**Captain (10):** captain.* - All working  
**Compliance (2):** comp.* - All working  
**Debate (4):** debate.* - All working  
**Docs (2):** docs.* - All working  
**Health (2):** health.* - All working  
**Memory (5):** mem.* - All working  
**Mission (1):** mission.claim - Working  
**Messaging (4):** msg.* - All working  
**Onboarding (2):** onboard.* - All working  
**Refactor (6):** refactor.* - All working  
**Session (2):** session.* - All working  
**Swarm (1):** swarm.pulse - Working  
**Testing (4):** test.* (except pyramid_check) - Working  
**V2 (2):** v2.* - All working  
**Vector (3):** vector.* - All working  
**Workflow (1):** workflow.roi - Working  

---

## 🎯 CLAIMING WORK

To claim a category for fixing:

```bash
# View quarantine status
cat runtime/toolbelt_quarantine.json

# Claim a category (update fix queue)
# Edit runtime/toolbelt_fix_queue.json and set "assigned_to": "Agent-X"

# Run audit after fixing
python tools/audit_toolbelt.py
```

---

## 📈 PROGRESS TRACKING

- [ ] Brain Tools (5) - HIGH PRIORITY
- [ ] Discord Tools (3) - MEDIUM PRIORITY  
- [ ] Infrastructure Tools (4) - MEDIUM PRIORITY
- [ ] Message-Task Tools (3) - MEDIUM PRIORITY
- [ ] Validation Tools (4) - MEDIUM PRIORITY
- [ ] Observability Tools (4) - LOW PRIORITY
- [ ] OSS Tools (5) - LOW PRIORITY
- [ ] Test Pyramid (1) - LOW PRIORITY

**Target:** 100% working tools (100/100)  
**Current:** 71% working (71/100)  
**Remaining:** 29 tools to fix

---

## 🐝 SWARM FIXING PROTOCOL

1. **Audit:** `python tools/audit_toolbelt.py` (DONE ✅)
2. **Review:** Check `runtime/toolbelt_quarantine.json` for broken tools
3. **Claim:** Pick a category from `runtime/toolbelt_fix_queue.json`
4. **Fix:** Add get_spec() and validate() methods
5. **Test:** Re-run audit to verify fix
6. **Report:** Update fix queue with completion

**Estimated Time:** 2.5-5 hours total (5-10 min per tool)

---

**Created by:** Agent-1 (Integration & Core Systems Specialist)  
**Date:** October 14, 2025  
**Purpose:** Systematic toolbelt quality improvement

🐝 WE. ARE. SWARM. ⚡⚡

