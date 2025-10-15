# 📨 PROCEDURE: MESSAGE TAGGING STANDARD

**Version:** 1.0  
**Created:** 2025-10-15  
**Created By:** Co-Captain Agent-6  
**Status:** MANDATORY SWARM STANDARD  

---

## 🎯 PURPOSE

**Standardize message tags for clear communication channels.**

**Why This Matters:**
- Agents need to know message source instantly
- Different sources = different priorities
- Proper tagging = efficient processing

---

## 📋 MESSAGE TAG DEFINITIONS

### **[C2A] - Captain-to-Agent**

**Source:** Captain Agent-4  
**Direction:** Captain → Specific Agent OR All Agents  
**Usage:** Orders, coordination, validation, feedback  

**Examples:**
```
[C2A] Agent-6: Mission complete! Well done!
[C2A] ALL: GitHub analysis mission activated!
```

---

### **[D2A] - Discord-to-Agent** (MISSING IN SYSTEM!)

**Source:** Commander via Discord (General's broadcasts)  
**Direction:** Discord → All Agents (broadcast)  
**Usage:** Strategic directives, swarm-wide announcements, policy changes  

**Examples:**
```
[D2A] ALL: Clean your workspaces immediately!
[D2A] ALL: New operating procedure added!
```

**CRITICAL:** Currently NOT implemented! General's broadcasts use [C2A] incorrectly!

---

### **[A2A] - Agent-to-Agent**

**Source:** Any Agent  
**Direction:** Agent → Specific Agent  
**Usage:** Peer coordination, collaboration, information sharing  

**Examples:**
```
[A2A] Agent-7: Great work on that consolidation!
[A2A] Agent-1: Can you review my PR?
```

---

### **[A2C] - Agent-to-Captain**

**Source:** Any Agent  
**Direction:** Agent → Captain Agent-4  
**Usage:** Status reports, requests, escalations  

**Examples:**
```
[A2C] Agent-6: Mission complete, awaiting next assignment
[A2C] Agent-3: Request approval for deployment
```

---

## 🚨 CRITICAL ISSUE: [D2A] NOT IMPLEMENTED!

**Current Problem:**
- General's Discord broadcasts tagged [C2A]
- Should be tagged [D2A]
- System doesn't recognize [D2A] tag!

**Impact:**
- Confusion about message source
- Discord broadcasts look like Captain messages
- Improper prioritization

**Fix Required:**

### **Option A: Implement [D2A] Tag**

**Add to messaging system:**
```python
class MessageTag(Enum):
    C2A = "c2a"  # Captain-to-Agent
    D2A = "d2a"  # Discord-to-Agent (NEW!)
    A2A = "a2a"  # Agent-to-Agent
    A2C = "a2c"  # Agent-to-Captain
```

**Add to Discord service:**
```python
def broadcast_to_agents(message: str, source: str = "discord"):
    tag = "[D2A]" if source == "discord" else "[C2A]"
    formatted = f"{tag} ALL: {message}"
    # Send to all agents...
```

### **Option B: Use Existing [C2A] with Source Indicator**

**Keep [C2A] but add source:**
```
[C2A] (Discord/General): Clean workspaces!
vs
[C2A] (Captain): Mission status update
```

**Recommendation:** Option A (implement [D2A]) for clarity!

---

## 📊 TAG PRIORITY LEVELS

**By Source (Urgency):**
1. **[D2A]** - General/Commander (STRATEGIC - highest priority!)
2. **[C2A]** - Captain (TACTICAL - high priority)
3. **[A2C]** - Agent reporting (COORDINATION - normal priority)
4. **[A2A]** - Peer coordination (COLLABORATION - normal priority)

**Agents should:**
- Check [D2A] first (strategic directives)
- Then [C2A] (tactical orders)
- Then [A2C]/[A2A] (coordination)

---

## 🎯 IMPLEMENTATION PLAN

### **Step 1: Add [D2A] to Messaging System**

**Files to update:**
```
src/services/messaging_cli.py
src/services/discord_service.py  
src/core/messaging_protocol.py
```

**Changes:**
- Add D2A to MessageTag enum
- Update Discord broadcast to use [D2A]
- Update inbox sorting by tag priority

### **Step 2: Update Documentation**

**Add to:**
```
swarm_brain/protocols/MESSAGING_STANDARDS.md (create)
docs/MESSAGING_SYSTEM_GUIDE.md (update)
```

### **Step 3: Retroactive Tagging**

**Update old Discord broadcasts:**
- Identify messages from Discord/General
- Retag from [C2A] to [D2A]
- Maintain message history

---

## 🔍 DETECTION RULES

**How to identify message source:**

**Discord/General ([D2A]):**
- Contains "GENERAL" or "Commander" attribution
- Broadcast to ALL agents
- Strategic/policy nature
- Comes via Discord integration

**Captain ([C2A]):**
- From Agent-4 directly
- May target specific agent or ALL
- Tactical/operational nature
- Internal swarm coordination

**Agent ([A2A] or [A2C]):**
- From Agent-1 through Agent-8
- Peer coordination or reporting
- Collaboration nature

---

## 📋 AGENT RESPONSIBILITIES

**When receiving messages:**

1. **Check tag first:**
   - [D2A]: Strategic directive (highest priority!)
   - [C2A]: Tactical order (high priority)
   - [A2C]/[A2A]: Coordination (normal priority)

2. **Process by priority:**
   - [D2A]: Execute immediately
   - [C2A]: Execute within 1 cycle
   - Others: Execute within normal workflow

3. **Archive after processing:**
   - Move to inbox/archive/YYYY-MM/
   - Keep inbox clean

---

## 🚀 IMMEDIATE FIX NEEDED

**For Current Issue:**

**General's message should be:**
```
[D2A] ALL: Agents clean workspaces and check inboxes!
```

**Not:**
```
[C2A] Agent-6: ... (current incorrect tagging)
```

**Fix:** Implement [D2A] tag in messaging system!

---

**WE. ARE. SWARM.** 🐝⚡

**Proper tagging = Clear communication!**

---

**#MESSAGE_TAGGING #D2A_IMPLEMENTATION #WORKSPACE_HYGIENE #MANDATORY_PROCEDURE**

