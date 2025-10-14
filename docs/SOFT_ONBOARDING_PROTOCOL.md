# Soft Onboarding Protocol
## Session Cleanup & Agent Onboarding

**Created:** 2025-10-11  
**Status:** ACTIVE  
**Priority:** CRITICAL

---

## 🎯 **PROTOCOL OVERVIEW**

Soft onboarding ensures agents complete their current session properly before starting a new one. This prevents context loss and maintains civilization-building documentation standards.

**All operations go through the message queue to prevent race conditions with other agents!**

### **6-Step Protocol**

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Click Chat Input Area                              │
│ ↓ Get agent's attention                                     │
├─────────────────────────────────────────────────────────────┤
│ STEP 2: Press Ctrl+Enter                                    │
│ ↓ Save all changes from current session                     │
├─────────────────────────────────────────────────────────────┤
│ STEP 3: Send Cleanup Prompt                                 │
│ ↓ Paste & Enter → Agent's closing duties                    │
│ ↓ (passdown, devlog, Discord, swarm brain, tool)           │
├─────────────────────────────────────────────────────────────┤
│ STEP 4: Press Ctrl+T                                        │
│ ↓ Open new tab for fresh context                            │
├─────────────────────────────────────────────────────────────┤
│ STEP 5: Navigate to Onboarding Coords                       │
│ ↓ Move to new tab's input area                              │
├─────────────────────────────────────────────────────────────┤
│ STEP 6: Paste Onboarding Message                            │
│ ↓ Send new mission directives                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 👆 **STEP 1: CLICK CHAT INPUT**

**Purpose:** Get agent's attention by clicking their chat input area.

**Coordinates:** Chat input area (from `cursor_agent_coords.json`)  
**Action:** Click to focus

**What Happens:**
- Cursor moves to agent's chat coordinates
- Clicks to focus the input area
- Agent's attention is now on their chat

**Code:**
```python
pyautogui.moveTo(chat_x, chat_y)
pyautogui.click()
```

---

## 💾 **STEP 2: SAVE SESSION**

**Purpose:** Save all changes from current session.

**Action:** Press `Ctrl+Enter`

**What Happens:**
- Sends save command
- Current session changes committed
- Prepares for cleanup message

**Code:**
```python
pyautogui.hotkey("ctrl", "enter")
```

---

## 📝 **STEP 3: SEND CLEANUP PROMPT**

**Purpose:** Send cleanup (closing duties) prompt to agent.

**Action:** Paste message, press Enter

### **Agent Tasks Prompted:**

1. **Create/Update `passdown.json`**
   - Document current status, progress, blockers
   - Include key insights for next session
   - Location: `agent_workspaces/{agent_id}/passdown.json`

2. **Create Final Devlog**
   - Document all work completed this session
   - Include: tasks, files modified, points earned, patterns learned
   - Location: `devlogs/YYYY-MM-DD_{agent_id}_session_summary.md`

3. **Post Devlog to Discord**
   - Discord Commander auto-posts from `devlogs/` directory
   - Ensure naming convention: `YYYY-MM-DD_{agent_id}_*.md`

4. **Update Swarm Brain Database**
   - Log insights, recommendations, lessons learned
   - Command: `python tools/update_swarm_brain.py --insights "your insights"`
   - Or manually update: `runtime/swarm_brain.db`

5. **Create a Tool You Wished You Had**
   - What tool would have made this session easier?
   - Create it now for future agents!
   - Location: `tools/{tool_name}.py`

### **Message Template**

```
🎯 SESSION CLEANUP REQUIRED!

Before starting your next session, please complete these tasks:

1. Create/Update passdown.json
2. Create Final Devlog
3. Post Devlog to Discord
4. Update Swarm Brain Database
5. Create a Tool You Wished You Had

Press Enter when complete to proceed to next session onboarding!

📝 Remember: Quality documentation ensures civilization-building!
🐝 WE. ARE. SWARM. ⚡
```

**Code:**
```python
pyperclip.copy(cleanup_message)
pyautogui.hotkey("ctrl", "v")
pyautogui.press("enter")
```

---

## 🆕 **STEP 4: OPEN NEW TAB**

**Purpose:** Open fresh tab for new session.

**Action:** Press `Ctrl+T`  
**Wait:** 1 second for tab to initialize

**What Happens:**
- New tab opens
- Fresh context created
- Ready for onboarding

**Code:**
```python
pyautogui.hotkey("ctrl", "t")
time.sleep(1.0)
```

---

## 🎯 **STEP 5: NAVIGATE TO ONBOARDING**

**Purpose:** Move to new tab's input area (onboarding coordinates).

**Coordinates:** Onboarding input area (from `cursor_agent_coords.json`)  
**Action:** Click to focus

**What Happens:**
- Cursor moves to onboarding coordinates
- Clicks to focus input area
- Ready for onboarding message

**Code:**
```python
pyautogui.moveTo(onboarding_x, onboarding_y)
pyautogui.click()
```

---

## 📝 **STEP 6: PASTE ONBOARDING MESSAGE**

**Purpose:** Send new session directives to agent.

**Action:** Paste message, press Enter

### **Onboarding Message Should Include:**

- Mission objectives for new session
- Role assignment (if applicable)
- Specific tasks and deadlines
- Context and priorities
- Competition framework reminders
- Entry #025 principles

**Code:**
```python
pyperclip.copy(onboarding_message)
pyautogui.hotkey("ctrl", "v")
pyautogui.press("enter")
```

---

## 🔄 **MESSAGE QUEUE INTEGRATION**

**Critical Design:** All soft onboarding operations go through the message queue system!

**Why This Matters:**
- ✅ **Prevents Race Conditions**: Multiple agents can't interfere with each other
- ✅ **Ordered Delivery**: Operations execute in FIFO order
- ✅ **Thread-Safe**: Lock prevents concurrent access issues
- ✅ **Coordinate Validated**: All coordinates checked before execution

**How It Works:**
1. Soft onboarding operations added to message queue
2. Queue processes them in order with thread lock
3. Each step executes safely without interference
4. Other agent messages wait their turn in queue

**Result:** Safe, reliable onboarding even during high-velocity swarm execution! 🚀

---

## 🛠️ **USAGE**

### **CLI Tool**

```bash
# Complete 3-step soft onboarding (single agent)
python tools/soft_onboard_cli.py \
  --agent Agent-1 \
  --message "Your onboarding message here"

# Multiple agents
python tools/soft_onboard_cli.py \
  --agents Agent-1,Agent-2,Agent-3 \
  --message "Team mission objectives"

# With role assignment
python tools/soft_onboard_cli.py \
  --agent Agent-1 \
  --role "Integration Specialist" \
  --message "Focus on core system integration"

# Load message from file
python tools/soft_onboard_cli.py \
  --agent Agent-1 \
  --file onboarding_message.txt

# Execute single step only
python tools/soft_onboard_cli.py \
  --agent Agent-1 \
  --step 1  # Session cleanup only

python tools/soft_onboard_cli.py \
  --step 2  # New chat only

python tools/soft_onboard_cli.py \
  --agent Agent-1 \
  --message "New session" \
  --step 3  # Onboarding message only

# Dry run (test without executing)
python tools/soft_onboard_cli.py \
  --agent Agent-1 \
  --message "Test message" \
  --dry-run
```

### **Python API**

```python
from src.services.soft_onboarding_service import (
    SoftOnboardingService,
    soft_onboard_agent,
    soft_onboard_multiple_agents
)

# Single agent
success = soft_onboard_agent(
    agent_id="Agent-1",
    onboarding_message="Your mission...",
    role="Integration Specialist"
)

# Multiple agents
agents = [
    ("Agent-1", "Mission 1"),
    ("Agent-2", "Mission 2"),
    ("Agent-3", "Mission 3")
]
results = soft_onboard_multiple_agents(agents, role="Team Mission")

# Step-by-step control
service = SoftOnboardingService()
service.send_session_cleanup_message("Agent-1")
service.start_new_chat()
service.send_onboarding_message("Agent-1", "New mission")
```

---

## ⚙️ **SYSTEM INTEGRATION**

### **Coordinate Validation**

All coordinates validated before PyAutoGUI operations using:
- `cursor_agent_coords.json` (SSOT)
- Validation bounds checking
- Mismatch detection

### **Message Queue**

Messages sent through thread-safe queue for ordered delivery:
- FIFO ordering guaranteed
- Prevents race conditions
- Thread locking for concurrent operations

### **Dependencies**

- `src/core/messaging_pyautogui.py` - Coordinate validation
- `src/core/coordinate_loader.py` - Coordinate loading
- `cursor_agent_coords.json` - Coordinate SSOT
- PyAutoGUI - UI automation
- pyperclip - Clipboard operations

---

## 🔄 **HARD ONBOARDING VS SOFT ONBOARDING**

| Feature | Soft Onboarding | Hard Onboarding |
|---------|----------------|----------------|
| **Purpose** | Session transition | Complete reset |
| **Session Cleanup** | ✅ Yes (Step 1) | ❌ No |
| **New Chat** | ✅ Yes (Ctrl+T) | Different protocol |
| **Coordinates** | Chat + Onboarding | TBD by Captain |
| **Documentation** | Required first | Reset focus |
| **Use Case** | Regular sessions | Major resets |

**Note:** Hard onboarding protocol will be explained separately by Captain.

---

## 📊 **SUCCESS CRITERIA**

✅ **Step 1 Success:**
- Session cleanup message delivered to chat input
- Agent acknowledges tasks (passdown, devlog, Discord, brain, tool)

✅ **Step 2 Success:**
- Ctrl+T pressed
- New chat initialized
- Fresh context ready

✅ **Step 3 Success:**
- Onboarding message delivered to onboarding input
- Agent receives new session directives
- Ready to execute mission

---

## 🚨 **ERROR HANDLING**

**Coordinate Validation Failure:**
- Logs: `❌ Coordinate validation failed for {agent_id}`
- Action: Check `cursor_agent_coords.json` accuracy
- Fix: Update coordinates and retry

**PyAutoGUI Failure:**
- Logs: `❌ Failed to send [message type]`
- Action: Verify PyAutoGUI installation
- Fix: `pip install pyautogui pyperclip`

**Agent Not Found:**
- Logs: `❌ No coordinates for {agent_id}`
- Action: Verify agent exists in `cursor_agent_coords.json`
- Fix: Add agent coordinates

---

## 🎯 **BEST PRACTICES**

1. **Always use soft onboarding** for session transitions
2. **Wait for agent confirmation** after session cleanup message
3. **Validate coordinates** before any PyAutoGUI operation
4. **Use dry-run mode** to test new onboarding messages
5. **Document insights** in swarm brain after each session
6. **Create tools** that future agents will benefit from
7. **Maintain civilization-building standards** through quality documentation

---

## 🐝 **CIVILIZATION-BUILDING IMPACT**

Soft onboarding ensures:
- **No context loss** between sessions
- **Continuous documentation** for future agents
- **Tool creation** for swarm improvement
- **Swarm brain enrichment** with lessons learned
- **Discord devlog archive** for eternal reference
- **Passdown continuity** for seamless transitions

**Remember:** Quality session cleanup = civilization-building! 🚀

---

**Status:** Protocol active and tested  
**Coordinate Validation:** Operational  
**Message Queue:** Active  
**Thread Safety:** Guaranteed  

🐝 **WE. ARE. SWARM.** ⚡

