# 🏷️ Messaging Flag Priority Mapping

**Version:** 1.0  
**Created:** 2025-10-15  
**Lead:** Agent-2 (Infrastructure Mission LEAD)  
**Execution:** Agent-6 (Co-Captain)  
**Status:** ACTIVE STANDARD  

---

## 🎯 PURPOSE

**Define which messaging flags map to which priority levels for agent inbox processing.**

**Why This Matters:**
- Agents need clear priority order for inbox processing
- General's directives must be URGENT (highest priority!)
- Captain's orders are HIGH priority
- Peer coordination is NORMAL priority

---

## 📊 FLAG→PRIORITY MAPPING

### **URGENT 🚨 (Highest Priority)**

**Process IMMEDIATELY - Interrupt current work if needed!**

| Flag | Source | Meaning | Example |
|------|--------|---------|---------|
| **[D2A]** | Discord/General/Commander | Strategic directives | General: "Clean workspaces immediately!" |
| **[ONBOARDING]** | Captain/System | New agent onboarding | "Welcome Agent-X! Starting onboarding..." |
| **[BROADCAST]** (urgent) | Anyone → ALL | Urgent swarm-wide | "CRITICAL: All agents respond!" |

**Action Required:**
- ✅ Read immediately upon receipt
- ✅ Respond within same cycle
- ✅ Interrupt lower-priority work
- ✅ Update status.json with action taken
- ✅ Report completion to sender

**Why Urgent:**
- General/Commander directives = Strategic level
- Onboarding = Time-sensitive (new agent waiting)
- Urgent broadcasts = Swarm-critical issues

---

### **HIGH ⚡ (High Priority)**

**Process within current cycle - prioritize over normal work!**

| Flag | Source | Meaning | Example |
|------|--------|---------|---------|
| **[C2A]** | Captain (Agent-4) | Captain orders/coordination | Captain: "Begin Phase 2 execution" |
| **[BROADCAST]** (default) | Anyone → ALL | Swarm-wide messages | Captain: "Mission status update" |
| **[A2C]** (high flag) | Agent → Captain | Urgent agent reports | Agent: "CRITICAL blocker found!" |

**Action Required:**
- ✅ Process within current cycle
- ✅ Respond before cycle ends
- ✅ Prioritize over [A2A] work
- ✅ Update status.json
- ✅ Report to Captain if needed

**Why High:**
- Captain coordinates entire swarm
- Broadcasts affect all agents
- Urgent agent reports need fast response

---

### **NORMAL 📋 (Normal Priority)**

**Process in order received during normal workflow**

| Flag | Source | Meaning | Example |
|------|--------|---------|---------|
| **[A2A]** | Agent-X → Agent-Y | Peer coordination | Agent-7: "Can you review my PR?" |
| **[A2C]** (default) | Agent → Captain | Agent status reports | Agent-6: "Phase 1 complete!" |
| **[S2A]** | System | System notifications | System: "Build completed" |
| **[H2A]** | Human/User | User instructions | User: "Update documentation" |
| **[MSG]** | Generic | Unspecified messages | "General message" |

**Action Required:**
- ✅ Process in order received
- ✅ Respond within 3 cycles
- ✅ No work interruption needed
- ✅ Update status if significant

**Why Normal:**
- Peer coordination not urgent
- Status reports informational
- System notifications routine
- Can queue behind urgent/high work

---

## 🎯 INBOX PROCESSING PROTOCOL

**Every Cycle, Agents MUST:**

### **Step 1: Sort Inbox by Priority**

```python
inbox_messages = read_inbox()

urgent = [m for m in inbox if m.startswith('[D2A]') or m.startswith('[ONBOARDING]')]
high = [m for m in inbox if m.startswith('[C2A]') or m.startswith('[BROADCAST]')]
normal = [m for m in inbox if m.startswith('[A2A]') or m.startswith('[A2C]') or m.startswith('[S2A]')]

# Process in order
for msg in urgent:
    process_immediately(msg)

for msg in high:
    process_this_cycle(msg)

for msg in normal:
    queue_for_processing(msg)
```

### **Step 2: Process by Priority**

**URGENT ([D2A], [ONBOARDING]):**
- Interrupt current work
- Read and respond immediately
- Update status.json
- Archive after response

**HIGH ([C2A], [BROADCAST]):**
- Process before cycle ends
- Respond within 1 cycle
- Prioritize over normal work

**NORMAL ([A2A], [A2C], [S2A], [H2A]):**
- Process in queue order
- Respond within 3 cycles
- Normal workflow integration

---

## 🚨 SPECIAL CASES

### **Override: Explicit Priority in Metadata**

**Messages can force priority:**
```python
message.metadata = {
    'priority': 'urgent'  # Forces URGENT regardless of flag
}
```

**Priority override order:**
1. Metadata priority (if present)
2. Flag-based priority (per this mapping)
3. Default (NORMAL)

---

### **General's Broadcasts = ALWAYS URGENT**

**Special Rule:**
```python
if sender in ['General', 'Commander', 'general', 'commander']:
    priority = 'URGENT'  # Override all other priorities!
```

**Why:** Strategic directives from leadership

---

## 📋 PRIORITY EXAMPLES

### **Example 1: General's Directive**

**Message:**
```
[D2A] ALL: Clean your workspaces immediately!
From: General (via Discord)
```

**Priority:** 🚨 URGENT  
**Action:** Drop current work, clean workspace, respond immediately!

---

### **Example 2: Captain's Order**

**Message:**
```
[C2A] Agent-6: Begin Phase 2 execution
From: Captain Agent-4
```

**Priority:** ⚡ HIGH  
**Action:** Start Phase 2 this cycle, report progress before cycle ends!

---

### **Example 3: Agent Coordination**

**Message:**
```
[A2A] Agent-7 → Agent-6: Great work on repos 41-50!
```

**Priority:** 📋 NORMAL  
**Action:** Acknowledge within 3 cycles, no work interruption needed!

---

### **Example 4: Agent Report to Captain**

**Message:**
```
[A2C] Agent-6 → Captain: Infrastructure Phase 1 complete!
```

**Priority:** 📋 NORMAL (unless flagged high)  
**Action:** Captain reviews when available!

---

## 🎯 COMPLIANCE ENFORCEMENT

**Captain/Co-Captain checks:**

**Every 5 Cycles:**
- [ ] All agents processing [D2A] immediately?
- [ ] All agents responding to [C2A] within 1 cycle?
- [ ] Inbox priority violations detected?

**Violations:**
- ⚠️ [D2A] unresponded >1 cycle: WARNING
- 🚨 [D2A] unresponded >3 cycles: CRITICAL
- ⚠️ [C2A] unresponded >3 cycles: WARNING

---

## 📊 SUCCESS METRICS

**Effective Priority Mapping When:**
- ✅ 100% of [D2A] processed within 1 cycle
- ✅ 95%+ of [C2A] processed within 1 cycle
- ✅ 90%+ of [A2A] processed within 3 cycles
- ✅ No General directives ignored
- ✅ Agents understand processing order

---

## 🔍 QUICK REFERENCE CARD

**For Agents:**

```
URGENT 🚨: [D2A] (General/Discord), [ONBOARDING]
  → Process IMMEDIATELY, interrupt work!

HIGH ⚡: [C2A] (Captain), [BROADCAST]
  → Process this cycle, prioritize!

NORMAL 📋: [A2A], [A2C], [S2A], [H2A], [MSG]
  → Queue in order, process normally!

REMEMBER: General/Commander = ALWAYS URGENT!
```

---

## 📚 RELATED DOCUMENTATION

**See Also:**
- `swarm_brain/procedures/PROCEDURE_DAILY_AGENT_OPERATIONS.md` - Inbox checking procedure
- `swarm_brain/procedures/PROCEDURE_MESSAGE_TAGGING_STANDARD.md` - Flag definitions
- `src/core/message_formatters.py` - Implementation (lines 65-115)
- `docs/MESSAGING_SYSTEM_GUIDE.md` - Complete messaging system

---

**WE. ARE. SWARM.** 🐝⚡

**Clear priorities = Efficient swarm!**

---

**#FLAG_PRIORITY_MAPPING #D2A_URGENT #INBOX_PROCESSING #SWARM_STANDARD**

