# 🔍 ROOT CAUSE ANALYSIS: [D2A] Tagging Issue

**Analyst:** Co-Captain Agent-6  
**Issue:** General's Discord broadcast tagged [C2A] instead of [D2A]  
**Date:** 2025-10-15  
**Status:** INVESTIGATION COMPLETE  

---

## 🚨 THE ISSUE

**What Happened:**
```
General's Discord broadcast:
"[C2A] Agent-6: agents haven't been checking inboxes..."
         ↑
    SHOULD BE [D2A]!
```

**Expected:**
```
"[D2A] ALL: agents haven't been checking inboxes..."
```

---

## 🔍 ROOT CAUSE IDENTIFIED

**Location:** `src/core/message_formatters.py` line 77

**Current Logic:**
```python
elif "discord" in msg_type_lower or "discord" in str(message.sender).lower():
    prefix = "[D2A]"
```

**Problem:** 
- Checks for "discord" in `message_type` OR `sender` field
- General's Discord broadcast likely has:
  - `message_type`: "text" or "broadcast" (NOT "discord")
  - `sender`: "General" or "Commander" (NOT contains "discord")
- **Both checks FAIL → Falls through to default [C2A]!**

---

## 🎯 THE FIX

### **Option A: Add "general" and "commander" Detection**

```python
elif ("discord" in msg_type_lower or 
      "discord" in str(message.sender).lower() or
      "general" in str(message.sender).lower() or
      "commander" in str(message.sender).lower()):
    prefix = "[D2A]"
    label = "DISCORD MESSAGE"
```

### **Option B: Check Message Source Metadata**

```python
# Check if message came via Discord integration
if message.metadata and message.metadata.get('source') == 'discord':
    prefix = "[D2A]"
elif "discord" in msg_type_lower or "discord" in str(message.sender).lower():
    prefix = "[D2A]"
```

### **Option C: Use Recipient Pattern**

```python
# If recipient is "ALL" and not from Captain, it's likely Discord
if message.recipient == "ALL" and "captain" not in str(message.sender).lower():
    prefix = "[D2A]"
```

**Recommended:** **Combination of A + B** for robustness!

---

## 📋 IMPLEMENTATION PLAN

### **Step 1: Update message_formatters.py**

**Add detection for:**
- "general" in sender
- "commander" in sender
- metadata.source == "discord"
- recipient == "ALL" (broadcast pattern)

### **Step 2: Update Discord Service**

**Ensure Discord broadcasts set:**
```python
message.metadata = {
    'source': 'discord',
    'broadcast': True,
    'from': 'general' or 'commander'
}

message.sender = "Discord/General" or "Discord/Commander"
```

### **Step 3: Test**

**Verify:**
- General's broadcasts → [D2A]
- Captain's broadcasts → [C2A]
- Agent messages → [A2A]
- System messages → [S2A]

---

## 🚀 IMMEDIATE ACTION

**Creating fix now:**

```python
# Enhanced detection in message_formatters.py (line 77)

# Discord/General/Commander detection (most comprehensive!)
sender_lower = str(message.sender).lower()
is_discord_source = (
    "discord" in msg_type_lower or
    "discord" in sender_lower or
    "general" in sender_lower or
    "commander" in sender_lower or
    (hasattr(message, 'metadata') and 
     isinstance(message.metadata, dict) and 
     message.metadata.get('source') == 'discord')
)

if is_discord_source:
    prefix = "[D2A]"
    label = "DISCORD MESSAGE"
```

---

## 📊 EXPECTED BEHAVIOR AFTER FIX

**Discord General broadcasts:**
```
[D2A] ALL: Clean your workspaces!
```

**Captain broadcasts:**
```
[C2A] ALL: Mission status update
```

**Captain to specific agent:**
```
[C2A] Agent-6: Mission complete!
```

**Agent-to-agent:**
```
[A2A] Agent-1 → Agent-7: Great work!
```

---

**WE. ARE. SWARM.** 🐝⚡

**#ROOT_CAUSE #D2A_FIX #TAGGING_ISSUE #INVESTIGATION_COMPLETE**

