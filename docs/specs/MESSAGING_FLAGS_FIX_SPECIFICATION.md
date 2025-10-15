# 📨 Messaging Flags Fix Specification

**Lead Architect:** Agent-2  
**Issue Reporter:** Agent-6 (Co-Captain)  
**Root Cause:** General's directive  
**Date:** 2025-10-15  
**Priority:** 🚨 CRITICAL - General's broadcasts mistagged  

---

## 🎯 GENERAL'S DIRECTIVE

**From General's broadcast:**
> "figure out why this discord broadcast is tagged c2a instead of d2a THIS IS A BROADCAST FROM THE GENERAL via discord"

**Issue:** [C2A] instead of [D2A] for Discord broadcasts from General

---

## 🚨 CRITICAL ISSUE: [D2A] Detection Failure

**Agent-6's Root Cause Analysis:** ✅ EXCELLENT

**Problem:**
```python
# Current code (src/core/message_formatters.py:77)
elif "discord" in msg_type_lower or "discord" in str(message.sender).lower():
    prefix = "[D2A]"
    label = "DISCORD MESSAGE"
```

**Why it fails:**
- Checks for "discord" in sender field
- General's broadcasts have `sender="General"` or `sender="Commander"`
- Does NOT contain "discord" string
- Detection fails → defaults to [C2A]

**Evidence:**
```
General's actual broadcast:
"[C2A] Agent-6: agents haven't been checking inboxes..."
      ↑
  Should be [D2A]!
```

---

## 🔧 FIX #1: [D2A] Enhanced Detection (CRITICAL)

**File:** `src/core/message_formatters.py`  
**Lines:** ~77-79  
**Priority:** ⚡⚡⚡ IMMEDIATE  

### **Implementation:**

```python
# BEFORE (broken):
elif "discord" in msg_type_lower or "discord" in str(message.sender).lower():
    prefix = "[D2A]"
    label = "DISCORD MESSAGE"

# AFTER (fixed):
sender_lower = str(message.sender).lower()

# Enhanced Discord source detection
is_discord_source = (
    "discord" in msg_type_lower or
    "discord" in sender_lower or
    "general" in sender_lower or          # FIX: Add General
    "commander" in sender_lower or        # FIX: Add Commander  
    sender_lower.startswith("general") or # FIX: Exact match
    sender_lower.startswith("commander")  # FIX: Exact match
)

# Additional metadata check if available
if hasattr(message, 'metadata') and isinstance(message.metadata, dict):
    if message.metadata.get('source') == 'discord':
        is_discord_source = True

if is_discord_source:
    prefix = "[D2A]"
    label = "DISCORD MESSAGE"
```

### **Testing:**

**Test Case 1: General's Broadcast**
```python
# Input
message = UnifiedMessage(
    sender="General",
    recipient="Agent-6",
    content="agents haven't been checking inboxes...",
    message_type=UnifiedMessageType.BROADCAST
)

# Expected Output
assert format_message(message).startswith("[D2A]")  # NOT [C2A]!
```

**Test Case 2: Commander's Broadcast**
```python
# Input  
message = UnifiedMessage(
    sender="Commander",
    recipient="Agent-2",
    content="NEW MISSION ASSIGNED",
    message_type=UnifiedMessageType.TEXT
)

# Expected Output
assert format_message(message).startswith("[D2A]")
```

**Test Case 3: Discord Metadata**
```python
# Input
message = UnifiedMessage(
    sender="User",
    recipient="Agent-7",
    content="Update status",
    metadata={'source': 'discord'}
)

# Expected Output
assert format_message(message).startswith("[D2A]")
```

**Estimated Time:** 30 minutes implementation + 30 minutes testing = **1 hour**

---

## 🔧 FIX #2: [A2C] Explicit Detection

**File:** `src/core/message_formatters.py`  
**Priority:** ⚡⚡ HIGH  

### **Implementation:**

```python
# Add BEFORE the generic [A2A] check
# Location: After [C2A] check, before [A2A] check

# Agent-to-Captain detection
if message.recipient in ["Agent-4", "Captain", "agent-4", "captain"]:
    prefix = "[A2C]"
    label = "AGENT TO CAPTAIN"
```

### **Testing:**

**Test Case: Agent Reporting to Captain**
```python
# Input
message = UnifiedMessage(
    sender="Agent-6",
    recipient="Agent-4",
    content="Phase 1 complete!"
)

# Expected Output
assert format_message(message).startswith("[A2C]")  # NOT [A2A]!
```

**Estimated Time:** 20 minutes implementation + 20 minutes testing = **40 minutes**

---

## 📊 FIX #3: Priority Mapping Documentation

**File:** `docs/messaging/FLAG_PRIORITY_MAPPING.md` (NEW)  
**Priority:** ⚡ MEDIUM  

### **Content:**

```markdown
# 🏷️ Messaging Flag Priority Mapping

**Purpose:** Define which flags map to which priority levels for agent inbox processing

## Priority Levels

### **URGENT** 🚨
- **[D2A]** - Discord/General directives (HIGHEST PRIORITY!)
- **[ONBOARDING]** - New agent onboarding
- **[BROADCAST]** with urgent metadata

**Action Required:** Process immediately, interrupt current work if needed

---

### **HIGH** ⚡
- **[C2A]** - Captain orders and coordination
- **[BROADCAST]** - Swarm-wide messages (default)
- **[A2C]** with high priority flag

**Action Required:** Process within current cycle, prioritize over normal work

---

### **NORMAL** 📋
- **[A2A]** - Agent-to-agent peer coordination
- **[A2C]** - Agent reports to Captain (default)
- **[S2A]** - System notifications (most)
- **[H2A]** - Human instructions (routine)
- **[MSG]** - Generic messages

**Action Required:** Process in order received, during normal workflow

---

## Inbox Processing Order

1. **URGENT** messages first ([D2A], [ONBOARDING])
2. **HIGH** messages second ([C2A], [BROADCAST])
3. **NORMAL** messages third ([A2A], [A2C], [S2A])

## Override Flags

Messages can include explicit priority in metadata:
- `priority="urgent"` → Force URGENT
- `priority="high"` → Force HIGH  
- `priority="normal"` → Force NORMAL

**General's broadcasts = ALWAYS URGENT regardless of flag!**
```

**Estimated Time:** 1 hour documentation + 30 minutes Swarm Brain integration = **1.5 hours**

---

## 🚀 IMPLEMENTATION ORDER (Agent-6)

### **IMMEDIATE (This Cycle - 3 hours):**

**Priority 1: [D2A] Fix** ⚡⚡⚡ CRITICAL
- 30 min: Implement enhanced detection
- 30 min: Test with General's broadcast scenarios
- 15 min: Verify all Discord sources detected
- **Total:** 1 hour 15 minutes

**Priority 2: [A2C] Detection** ⚡⚡ HIGH
- 20 min: Add Agent-to-Captain logic
- 20 min: Test agent reporting scenarios
- **Total:** 40 minutes

**Priority 3: Priority Mapping Doc** ⚡ MEDIUM  
- 45 min: Create documentation
- 30 min: Add to Swarm Brain
- **Total:** 1 hour 15 minutes

**Cycle Total:** ~3 hours

---

### **NEXT CYCLE (Phase 2 - Discord Commands):**

After messaging flags fixed, proceed to:
- Discord !restart command implementation
- Discord !shutdown command implementation
- Real-time status updates

---

## ✅ SUCCESS CRITERIA

**Fix #1 (D2A):**
- [ ] General's broadcasts tagged [D2A] not [C2A]
- [ ] Commander broadcasts tagged [D2A]
- [ ] Discord metadata source detected
- [ ] All existing Discord messages still work

**Fix #2 (A2C):**
- [ ] Agent→Captain messages tagged [A2C] not [A2A]
- [ ] Agent-4 recipient properly detected
- [ ] "Captain" recipient properly detected

**Fix #3 (Priority Mapping):**
- [ ] Documentation created
- [ ] Shared to Swarm Brain
- [ ] All 9 flags have priority assignments
- [ ] Agents know processing order

---

## 🎯 IMMEDIATE ACTION (Agent-6)

**This Cycle (3 hours):**

1. **Fix [D2A] detection** (1 hr 15 min)
   - Update `src/core/message_formatters.py`
   - Add "general", "commander", metadata checks
   - Test with General's broadcast format

2. **Add [A2C] detection** (40 min)
   - Add Agent-to-Captain logic
   - Test agent reporting

3. **Create priority mapping** (1 hr 15 min)
   - Document all 9 flags → priority levels
   - Share to Swarm Brain

**Expected Outcome:**
- General's broadcasts properly tagged [D2A] ✅
- Agent reports properly tagged [A2C] ✅
- All agents know message priorities ✅

---

**Agent-2 (LEAD) - Architectural decisions complete!**  
**Agent-6 (Co-Captain) - CRITICAL fix ready for implementation!**

**This fixes General's specific directive!** 🎯

---

**WE. ARE. SWARM.** 🐝⚡

**#D2A_FIX_CRITICAL #GENERAL_DIRECTIVE #MESSAGING_FLAGS #PHASE1_COMPLETE**

