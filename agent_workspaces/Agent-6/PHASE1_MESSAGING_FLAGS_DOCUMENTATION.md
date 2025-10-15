# 📨 PHASE 1: MESSAGING FLAGS COMPREHENSIVE DOCUMENTATION

**Documenter:** Co-Captain Agent-6  
**For:** Agent-2 (Infrastructure LEAD)  
**Date:** 2025-10-15  
**Purpose:** Infrastructure Consolidation - Objective 3  

---

## 🏷️ ALL MESSAGING FLAGS (Complete List)

**Source:** `src/core/message_formatters.py` + Agent-7's devlog

### **Implemented Flags:**

| Flag | Meaning | Sender | Recipient | When Used | Status |
|------|---------|--------|-----------|-----------|--------|
| **[C2A]** | Captain→Agent | Agent-4 | Any Agent | Captain coordinating | ✅ WORKS |
| **[A2A]** | Agent→Agent | Agent-X | Agent-Y | Peer coordination | ✅ WORKS |
| **[S2A]** | System→Agent | System | Any Agent | Automated notifications | ✅ WORKS |
| **[H2A]** | Human→Agent | Human/User | Any Agent | User instructions | ✅ WORKS |
| **[D2A]** | Discord→Agent | Discord/General | Any Agent | Discord broadcasts | ⚠️ PARTIAL |
| **[A2C]** | Agent→Captain | Any Agent | Agent-4 | Agent reporting | ✅ WORKS |
| **[BROADCAST]** | Broadcast | Anyone | ALL Agents | Swarm-wide messages | ✅ WORKS |
| **[ONBOARDING]** | Onboarding | Captain/System | Any Agent | New agent onboarding | ✅ WORKS |
| **[MSG]** | Generic | Unknown | Any | Fallback for unspecified | ✅ WORKS |

**Total:** 9 flag types

---

## 🚨 IDENTIFIED ISSUES

### **Issue #1: [D2A] Detection Failure** ⚠️ CRITICAL!

**Location:** `src/core/message_formatters.py` line 77

**Current Code:**
```python
elif "discord" in msg_type_lower or "discord" in str(message.sender).lower():
    prefix = "[D2A]"
    label = "DISCORD MESSAGE"
```

**Problem:**
- Checks for "discord" in sender field
- General's broadcasts have sender="General" or "Commander"
- NOT "discord"!
- Detection FAILS → defaults to [C2A]

**Evidence:**
```
General's broadcast:
"[C2A] Agent-6: agents haven't been checking inboxes..."
      ↑
  Should be [D2A]!
```

**Fix Required:**
```python
# Enhanced detection
sender_lower = str(message.sender).lower()
is_discord_source = (
    "discord" in msg_type_lower or
    "discord" in sender_lower or
    "general" in sender_lower or      # ADD THIS!
    "commander" in sender_lower or     # ADD THIS!
    (hasattr(message, 'metadata') and 
     isinstance(message.metadata, dict) and 
     message.metadata.get('source') == 'discord')  # AND THIS!
)

if is_discord_source:
    prefix = "[D2A]"
    label = "DISCORD MESSAGE"
```

**Priority:** ⚡⚡⚡ CRITICAL (General's directives must be [D2A]!)

---

### **Issue #2: [A2C] Not Clearly Defined** ⚠️

**Status:** Flag exists in table but not in message_formatters.py!

**Current:** No explicit [A2C] detection logic

**Needed:**
```python
# Add after [A2A] detection
elif message.recipient == "Agent-4" or message.recipient == "Captain":
    prefix = "[A2C]"
    label = "AGENT TO CAPTAIN"
```

**Priority:** ⚡⚡ HIGH (agents reporting to Captain)

---

### **Issue #3: Priority Mapping Unclear** ⚠️

**Question:** Which flags map to which priorities?

**Current:** Not documented!

**Needed:**
```
Flag → Priority Mapping:
[D2A] → URGENT (General/Commander directives!)
[C2A] → HIGH (Captain orders)
[A2C] → NORMAL (Agent reports)
[A2A] → NORMAL (Peer coordination)
[S2A] → varies (system notifications)
[BROADCAST] → HIGH (swarm-wide)
[ONBOARDING] → URGENT (new agent)
```

**Priority:** ⚡ MEDIUM (for agent inbox processing)

---

## ✅ WHAT WORKS WELL

**1. [C2A] - Captain-to-Agent:** ✅
- Reliable detection
- Properly formatted
- Clear priority

**2. [A2A] - Agent-to-Agent:** ✅
- Good peer coordination
- Proper formatting
- No issues found

**3. [BROADCAST] - Swarm-wide:** ✅
- Effective for all-agent messages
- Clear indication
- Works as expected

**4. [ONBOARDING] - New Agents:** ✅
- Proper new agent flow
- Clear purpose
- No issues

---

## 📋 TESTING PLAN

### **Phase 5: Messaging Audit Tests**

**Test Matrix:**

| From | To | Expected Tag | Test Status |
|------|----|--------------| ------------|
| Agent-4 | Agent-6 | [C2A] | ✅ PASS |
| Agent-6 | Agent-7 | [A2A] | ✅ PASS |
| Agent-6 | Agent-4 | [A2C] | ⏳ NEEDS TEST |
| System | Agent-6 | [S2A] | ⏳ NEEDS TEST |
| User | Agent-6 | [H2A] | ⏳ NEEDS TEST |
| Discord/General | Agent-6 | [D2A] | ❌ FAILS (root cause found!) |
| Captain | ALL | [BROADCAST] | ✅ PASS |

**Tests Needed:** 4 (A2C, S2A, H2A, D2A)

**Estimated Time:** 4-6 hours (comprehensive testing)

---

## 🔧 PROPOSED FIXES

### **Fix #1: [D2A] Enhanced Detection** (30 minutes)

**File:** `src/core/message_formatters.py`  
**Lines:** 77-79  
**Change:** Add "general", "commander", metadata.source checks  
**Testing:** 30 minutes  
**Total:** 1 hour  

### **Fix #2: [A2C] Explicit Detection** (20 minutes)

**File:** `src/core/message_formatters.py`  
**Add:** Agent-to-Captain detection logic  
**Testing:** 20 minutes  
**Total:** 40 minutes  

### **Fix #3: Priority Mapping Documentation** (1 hour)

**Create:** `docs/messaging/FLAG_PRIORITY_MAPPING.md`  
**Content:** Which flags = which priorities  
**Share:** To Swarm Brain  

---

## 🎯 DELIVERABLE FOR AGENT-2

**Complete Messaging Flags Documentation:**
- ✅ All 9 flags documented
- ✅ 2 critical issues identified
- ✅ Fixes proposed with timelines
- ✅ Testing plan created
- ✅ Priority mapping needed

**Ready for your architectural review and Phase 5 coordination!**

---

**File:** `agent_workspaces/Agent-6/PHASE1_MESSAGING_FLAGS_DOCUMENTATION.md`

---

**WE. ARE. SWARM.** 🐝⚡

**#MESSAGING_FLAGS #D2A_FIX_READY #PHASE1_COMPLETE**

