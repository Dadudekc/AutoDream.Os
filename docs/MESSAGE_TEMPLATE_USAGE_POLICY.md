# Message Template Usage Policy
**Created**: 2025-10-13  
**Author**: Captain Agent-4  
**Purpose**: Define when to use FULL, COMPACT, and MINIMAL templates

---

## 🎯 **3 MESSAGE TEMPLATES**

### **FULL Template** (Detailed, Complete)
- **Lines**: ~15+
- **Includes**: All metadata, tags, context, swarm branding
- **Purpose**: Critical communications with complete information

### **COMPACT Template** (Standard)
- **Lines**: ~10
- **Includes**: Essential fields only (from, to, priority, timestamp)
- **Purpose**: Regular agent communications

### **MINIMAL Template** (Brief)
- **Lines**: ~4
- **Includes**: From/to only, content
- **Purpose**: Quick updates, passdown

---

## 📋 **WHEN TO USE EACH TEMPLATE**

### **USE FULL Template For**:

1. **Captain → Agent** (All [C2A] messages)
   - Captain's directives need complete context
   - Tags, priority, metadata important
   - Example: Mission assignments, urgent coordination

2. **User/Discord → Agent** (All [D2A], [H2A] messages)
   - User messages need clear sender identification
   - Full metadata helps agents understand context
   - Example: User giving instructions to agents

3. **Onboarding Messages** (All [ONBOARDING])
   - **MUST include operating cycle duties**
   - **MUST include workflow procedures**
   - **MUST use prompts/agents/onboarding.md template**
   - Example: Soft onboarding, hard onboarding

4. **Critical System Messages**
   - Blockers, emergencies, system-wide alerts
   - Example: [S2A] critical notifications

5. **Agent → Captain** (All [A2C] reports)
   - Captain needs full context from agent reports
   - Tags help categorize agent work
   - Example: Mission complete reports, status updates

---

### **USE COMPACT Template For**:

1. **Agent → Agent** (Regular [A2A])
   - Standard coordination between agents
   - Example: "Need help with X", "Coordination request"

2. **Agent → Captain** (Routine updates)
   - Regular progress reports
   - Example: "Task in progress", "Checkpoint reached"

3. **System Notifications** (Non-critical)
   - Standard status updates
   - Example: "Test suite passing", "Deploy complete"

---

### **USE MINIMAL Template For**:

1. **Passdown Channel**
   - Session handoff messages
   - Example: passdown.json summaries

2. **Quick Status Updates**
   - Very brief agent-to-agent
   - Example: "Done", "Blocked on X"

3. **Non-Captain → Non-Captain** (Quick coordination)
   - Agent-Agent brief messages
   - Example: "Check your inbox", "Ready when you are"

---

## 🏷️ **MESSAGE CLASSIFICATION FLAGS**

### **Sender Detection**:

**Environment Variables** (set before running messaging_cli):
```bash
# For User/General (you!)
$env:USER_ROLE="general"  # Shows as [H2A]
$env:USER_ROLE="discord"  # Shows as [D2A]

# For Captain (Agent-4)
$env:USER_ROLE="captain"  # Shows as [C2A]
# OR run from repo root (auto-detects as Captain)

# For Agents
$env:AGENT_CONTEXT="Agent-X"  # Shows as [A2A] when messaging other agents
```

### **Auto-Detection Logic**:

```
Is Captain?
→ YES: sender="Agent-4", type=CAPTAIN_TO_AGENT, flag=[C2A], template=FULL

Is Discord?
→ YES: sender="Discord", type=TEXT, flag=[D2A], template=FULL

Is User/General?
→ YES: sender="User", type=HUMAN_TO_AGENT, flag=[H2A], template=FULL

Is Agent?
→ YES: sender="Agent-X", type=AGENT_TO_AGENT, flag=[A2A], template=COMPACT

Default:
→ sender="System", type=SYSTEM_TO_AGENT, flag=[S2A], template=FULL
```

---

## 📋 **USAGE EXAMPLES**

### **User Sending Message** (Should show [H2A]):
```bash
$env:USER_ROLE="general"
python -m src.services.messaging_cli --agent Agent-6 --message "Your task here"
```
**Result**: [H2A] HUMAN MESSAGE with FULL template

### **Discord Bot Sending** (Should show [D2A]):
```bash
$env:USER_ROLE="discord"
python -m src.services.messaging_cli --agent Agent-6 --message "Discord command"
```
**Result**: [D2A] DISCORD MESSAGE with FULL template

### **Captain Sending** (Shows [C2A]):
```bash
# From repo root (auto-detects)
python -m src.services.messaging_cli --agent Agent-6 --message "Captain directive"
```
**Result**: [C2A] CAPTAIN MESSAGE with FULL template

### **Agent Sending to Agent** (Shows [A2A]):
```bash
$env:AGENT_CONTEXT="Agent-1"
python -m src.services.messaging_cli --agent Agent-6 --message "Need coordination"
```
**Result**: [A2A] AGENT MESSAGE with COMPACT template

---

## 🔧 **ONBOARDING TEMPLATE FIX**

### **Problem**:
- Onboarding messages were custom-only
- No operating cycle duties included
- Agents didn't get procedure reminders

### **Solution**:
- Created `onboarding_template_loader.py`
- Loads `prompts/agents/onboarding.md` (19,382 chars)
- Merges template + custom mission
- Agents now get FULL procedures

### **What Agents Now Receive**:
- ✅ Agent cycle system (8X efficiency)
- ✅ Expected workflow loop (6 steps)
- ✅ Actionable results requirements
- ✅ Critical communication protocols
- ✅ Multi-agent check-in system
- ✅ V2 compliance workflow
- ✅ Vector database integration guide
- ✅ Custom mission (merged at end)

---

## 🎯 **TEMPLATE SELECTION RULES**

### **Priority Order** (first match wins):

1. **Onboarding channel** → FULL (with cycle duties template!)
2. **Captain sender** → FULL
3. **User/Discord sender** → FULL
4. **Agent → Captain** → FULL
5. **Agent → Agent** → COMPACT
6. **Passdown channel** → MINIMAL
7. **Default** → COMPACT

---

## ✅ **FIXES IMPLEMENTED**

1. ✅ Message classification (Captain/Discord/User detection)
2. ✅ Onboarding template loader (includes cycle duties)
3. ✅ Soft onboarding updated (uses full template)
4. ✅ Flag system corrected ([C2A], [D2A], [H2A], [A2A])

---

## 🚀 **TESTING INSTRUCTIONS**

### **Test User Message**:
```bash
$env:USER_ROLE="general"
python -m src.services.messaging_cli --agent Agent-6 --message "Test user message"
# Should show: [H2A] HUMAN MESSAGE
```

### **Test Onboarding with Full Template**:
```bash
python -m src.services.messaging_cli --soft-onboarding --agent Agent-1 \
  --role "Integration & Core Systems Specialist" \
  --message "Your specific mission"
# Should include: AGENT CYCLE SYSTEM, EXPECTED WORKFLOW LOOP, etc.
```

---

🐝 **WE. ARE. SWARM.** ⚡

*Message template system fixed - agents will now receive complete procedures!*

