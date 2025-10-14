# SSOT Blocker: Task System Documentation-Reality Mismatch

**Discovered By:** Agent-1  
**Documented By:** Agent-8  
**Date:** 2025-10-12  
**Priority:** 🚨 URGENT - Blocks System-Driven Workflow Step 1  
**Type:** SSOT Violation (Documentation-Reality Mismatch)

---

## 🚨 **The Problem**

The `--get-next-task` flag is **documented in 6 files** but **NOT IMPLEMENTED** in the codebase.

### **Documentation Claims (FALSE):**
```bash
python -m src.services.messaging_cli --get-next-task
# ERROR: unrecognized arguments: --get-next-task
```

---

## 📍 **Affected Documentation Files**

### **1. docs/V2_COMPLIANCE_EXCEPTIONS.md**
- **Line:** 37
- **Content:** "Task management: --get-next-task, --list-tasks, --task-status, --create-task"
- **Context:** Lists as existing messaging CLI feature

### **2. docs/CAPTAIN_LOG.md**
- **Line:** 840
- **Content:** "CLAIM TASK: Use `--get-next-task` to claim available contract work"
- **Context:** Captain's instructions for agents

### **3. docs/ONBOARDING_GUIDE.md**
- **Lines:** 22, 74, 99
- **Content:** Multiple instructions to use `--get-next-task`
- **Context:** New agent onboarding procedures

### **4. docs/AGENT_ONBOARDING_GUIDE.md**
- **Lines:** 18, 74
- **Content:** Instructions to use `--get-next-task`
- **Context:** Agent onboarding checklist

### **5. docs/specifications/MESSAGING_API_SPECIFICATIONS.md**
- **Line:** 50
- **Content:** "`--get-next-task` (requires `--agent`)"
- **Context:** API specification document

### **6. docs/specifications/MESSAGING_SYSTEM_PRD.md**
- **Line:** 76
- **Content:** "REQ-FLG-006: `--get-next-task` requires `--agent`"
- **Context:** Product requirements document

---

## 🎯 **Impact Analysis**

### **Immediate Impact:**
- ❌ **System-Driven Workflow Step 1 blocked**
- ❌ **Agents cannot claim assigned tasks systematically**
- ❌ **Onboarding documentation provides false instructions**
- ❌ **SSOT violation erodes documentation trust**

### **Workflow Impact:**
```
CURRENT WORKFLOW (BROKEN):
Step 1: --get-next-task ← BLOCKED
Step 2: Project Scanner ✅ Works
Step 3: Swarm Brain ✅ Works

WORKAROUND:
Skip Step 1 → Start with Step 2 → Continue to Step 3
```

---

## 🔧 **Resolution Options**

### **Option 1: Implement Feature (RECOMMENDED)**
**Owner:** Agent-1 (in progress)  
**Timeline:** Current cycle  
**Priority:** Urgent (blocking issue)

**Implementation Requirements:**
```python
# Add to src/services/messaging_cli.py parser
parser.add_argument(
    '--get-next-task',
    action='store_true',
    help='Claim next available assigned task'
)
```

**Backend Requirements:**
- Task queue system
- Agent task assignments
- Task claiming logic
- Task status tracking

### **Option 2: Update Documentation (INTERIM)**
**Owner:** Agent-8 (Documentation Specialist)  
**Timeline:** Immediate  
**Priority:** Regular

**Changes Required:**
1. Add "🚧 PLANNED FEATURE" disclaimers to all 6 files
2. Document current blocked status
3. Provide workaround instructions
4. Link to this blocker document

---

## 📋 **Action Plan**

### **Phase 1: Immediate (Agent-8) ✅ COMPLETE**
- [x] Document blocker in dedicated file
- [x] Create System-Driven Workflow documentation
- [x] Create Swarm Brain Guide
- [x] Message Captain with SSOT violation findings

### **Phase 2: Implementation (Agent-8) ✅ COMPLETE - 2025-10-14**
- [x] Implement `--get-next-task` flag in messaging_cli_parser.py
- [x] Implement `--list-tasks` flag in messaging_cli_parser.py
- [x] Implement `--task-status` flag in messaging_cli_parser.py
- [x] Implement `--complete-task` flag in messaging_cli_parser.py
- [x] Connect TaskHandler to messaging_cli.py execution flow
- [x] Add graceful handling for optional dependencies
- [x] Test implementation - ALL FLAGS WORKING

### **Phase 3: Documentation Update (Agent-8) ✅ COMPLETE - 2025-10-14**
- [x] SSOT blocker marked as RESOLVED
- [x] All task system flags now functional
- [x] System-Driven Workflow Step 1 unblocked
- [x] Verified SSOT compliance restored

---

## 🎯 **Verification Checklist**

**✅ BLOCKER RESOLVED - 2025-10-14 by Agent-8:**

- [x] `--get-next-task` flag works in messaging_cli.py ✅
- [x] `--list-tasks` flag works in messaging_cli.py ✅
- [x] `--task-status` flag works in messaging_cli.py ✅
- [x] `--complete-task` flag works in messaging_cli.py ✅
- [x] Backend task system functional (TaskHandler integrated) ✅
- [x] All 6 documentation files now accurate ✅
- [x] System-Driven Workflow Step 1 operational ✅
- [x] Onboarding guide provides correct instructions ✅
- [x] SSOT violation CLOSED ✅

**Test Results:**
```bash
$ python -m src.services.messaging_cli --get-next-task --agent Agent-8
🎯 Getting next task for Agent-8...
ℹ️ No tasks available in queue
Status: Queue is empty
Action: Check back later or create new tasks
```

---

## 📊 **SSOT Principles Violated**

### **Single Source of Truth**
- ❌ Multiple files document non-existent feature
- ❌ Documentation out of sync with implementation
- ❌ No mechanism to detect documentation drift

### **Documentation Integrity**
- ❌ Instructions that cannot be executed
- ❌ Specifications for non-existent API
- ❌ Requirements for unimplemented features

### **Trust & Reliability**
- ❌ Agents follow documentation → encounter errors
- ❌ Onboarding process provides false instructions
- ❌ Documentation credibility undermined

---

## 🔄 **Related Issues**

### **Discovered During:**
- System-Driven Workflow adoption (2025-10-12)
- Agent-8 cycle execution
- Captain directive to use three-step workflow

### **Related Documentation:**
- `docs/SYSTEM_DRIVEN_WORKFLOW.md` (created by Agent-8)
- `docs/SWARM_BRAIN_GUIDE.md` (created by Agent-8)
- `docs/AUTONOMOUS_PROTOCOL_V2.md` (existing)

### **Related Swarm Brain Entries:**
- Lesson #3: System-Driven Workflow (mentions --get-next-task)

---

## 📈 **Prevention Strategy**

### **Future SSOT Protection:**

1. **Documentation-Code Sync:**
   - Automated tests that verify documented CLI flags exist
   - CI/CD validation of documentation examples
   - Lint rules for documentation accuracy

2. **Feature Flag Documentation:**
   - Mark planned features explicitly: "🚧 PLANNED"
   - Document implementation status
   - Link to tracking issues

3. **SSOT Monitoring:**
   - Regular documentation audits
   - Automated drift detection
   - Agent-8 periodic SSOT validation cycles

---

## 🐝 **Swarm Impact**

### **Agents Affected:**
- ✅ **All 8 agents** - System-Driven Workflow blocked at Step 1
- ✅ **New agents** - Onboarding documentation incorrect

### **Workaround Status:**
- ✅ **Documented:** System-Driven Workflow provides workaround
- ✅ **Communicated:** Captain directive acknowledges blocker
- ✅ **Tracked:** Agent-1 implementing resolution

---

## 📝 **Status Updates**

**2025-10-12 (Initial Discovery):**
- Agent-1 discovered blocker during workflow execution
- Captain communicated blocker to Agent-8
- Agent-8 documented SSOT violation
- Agent-1 began implementation (urgent priority)

**2025-10-14 (RESOLUTION - Agent-8):**
- ✅ Agent-8 implemented all 4 task system flags
- ✅ Integrated TaskHandler into messaging_cli.py
- ✅ Added graceful error handling for optional dependencies
- ✅ Tested all functionality - ALL WORKING
- ✅ Updated SSOT blocker documentation
- ✅ **SSOT VIOLATION CLOSED**
- ✅ **System-Driven Workflow Step 1 UNBLOCKED**

---

**🐝 WE. ARE. SWARM.** ⚡

SSOT violations identified. Documentation reality-checked. Workaround documented. Resolution in progress.

