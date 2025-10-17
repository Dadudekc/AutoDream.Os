# Hard Onboarding Protocol
## Complete Agent Reset & Onboarding

**Created:** 2025-10-11  
**Status:** ACTIVE  
**Priority:** CRITICAL - Use for Major Resets Only

---

## 🎯 **PROTOCOL OVERVIEW**

Hard onboarding is a complete reset protocol for agents. Unlike soft onboarding (which preserves session context), hard onboarding clears everything and starts completely fresh.

**When to Use:**
- ✅ Major agent resets
- ✅ Complete context clearing needed
- ✅ Starting entirely new development phase
- ✅ Troubleshooting stuck agents
- ✅ Project-wide resets

**When NOT to Use:**
- ❌ Regular session transitions (use soft onboarding)
- ❌ Normal workflow continuation
- ❌ Minor context updates

---

## 🚨 **CRITICAL: ANTI-STOP TRAINING (READ FIRST!)**

**Before hard onboarding, understand:** 🔴

### **NEVER STOP = CORE PRINCIPLE:**
- ❌ **NEVER** ask "what should I do next?"
- ❌ **NEVER** wait for permission to act
- ❌ **NEVER** say "awaiting directive" or "standing by"
- ❌ **NEVER** idle between tasks
- ✅ **ALWAYS** self-direct to next task
- ✅ **ALWAYS** continuous execution
- ✅ **ALWAYS** have next action ready

### **🔴 CRITICAL: UPDATE STATUS.JSON EVERY 15-30 MINUTES!**
- ❌ **NOT updating status.json = System thinks you STOPPED!**
- ✅ **Update status.json = Proof you're ACTIVE!**
- 📍 **Location:** `agent_workspaces/Agent-X/status.json`
- ⏰ **Frequency:** Every cycle (15-30 min) or at progress milestones
- 💓 **status.json = YOUR HEARTBEAT!**

### **🚨 CRITICAL: STRATEGIC REST ≠ PASSIVE WAITING!**
- ❌ **Strategic rest as passive waiting = STOPPING!**
- ✅ **Strategic rest = READY + proactive opportunity finding!**
- ⚡ **After completing mission: Find next work within 10 minutes!**
- 🎯 **"Standing by" for > 10 minutes = YOU'RE STOPPING!**
- 💪 **Scan for opportunities, identify work, START immediately!**

**Read ALL FOUR:**
- `swarm_brain/protocols/ANTI_STOP_PROTOCOL.md` (MANDATORY!)
- `swarm_brain/protocols/STATUS_JSON_UPDATE_PROTOCOL.md` (CRITICAL!)
- `swarm_brain/protocols/ANTI_STOP_STRATEGIC_REST_PROTOCOL.md` (CRITICAL!)
- `swarm_brain/protocols/ANTI_STOP_AUTONOMOUS_CHOICE.md` (NEW!)

**If you don't update status.json = Captain detects STOP = You failed!**

---

## 📋 **5-STEP PROTOCOL**

```
┌──────────────────────────────────────────────────────────────┐
│ STEP 1: Go to Chat Input → Ctrl+Shift+Backspace (Clear)    │
│ ↓ Clears chat/resets agent state                            │
├──────────────────────────────────────────────────────────────┤
│ STEP 2: Ctrl+Enter (Send/Execute)                           │
│ ↓ Executes the clear command                                │
├──────────────────────────────────────────────────────────────┤
│ STEP 3: Ctrl+N (New Window/Session)                         │
│ ↓ Creates fresh context window                              │
├──────────────────────────────────────────────────────────────┤
│ STEP 4: Navigate to Onboarding Input Coords                 │
│ ↓ Moves to onboarding area                                  │
├──────────────────────────────────────────────────────────────┤
│ STEP 5: Send Onboarding Message → Press Enter               │
│ ↓ Agent receives new directives in fresh context            │
└──────────────────────────────────────────────────────────────┘
```

---

## 🗑️ **STEP 1: CLEAR CHAT**

**Purpose:** Clear agent's current chat and reset state

**Coordinates:** Chat input area (from `cursor_agent_coords.json`)  
**Action:** Press `Ctrl+Shift+Backspace`

**What Happens:**
- Clears current conversation
- Resets agent state
- Prepares for complete fresh start

**Code:**
```python
# Click chat input
pyautogui.moveTo(chat_x, chat_y)
pyautogui.click()

# Clear chat
pyautogui.hotkey("ctrl", "shift", "backspace")
```

---

## ⚡ **STEP 2: SEND/EXECUTE**

**Purpose:** Execute the clear command

**Action:** Press `Ctrl+Enter`

**What Happens:**
- Sends/executes the clear action
- Confirms the reset
- Prepares for new window

**Code:**
```python
pyautogui.hotkey("ctrl", "enter")
```

---

## 🆕 **STEP 3: NEW WINDOW**

**Purpose:** Create completely fresh context window

**Action:** Press `Ctrl+N`  
**Wait:** 1.5 seconds for window initialization

**What Happens:**
- Opens new window/session
- Provides clean slate
- Fresh context for onboarding

**Code:**
```python
pyautogui.hotkey("ctrl", "n")
time.sleep(1.5)  # Wait for initialization
```

---

## 🎯 **STEP 4: NAVIGATE TO ONBOARDING**

**Purpose:** Position at onboarding input area

**Coordinates:** Onboarding input area (from `cursor_agent_coords.json`)  
**Action:** Move to coordinates and click

**What Happens:**
- Moves to onboarding input coordinates
- Clicks to focus input area
- Ready for onboarding message

**Code:**
```python
# Move to onboarding coordinates
pyautogui.moveTo(onboarding_x, onboarding_y)
pyautogui.click()
```

---

## 📝 **STEP 5: SEND ONBOARDING MESSAGE**

**Purpose:** Deliver new directives to reset agent

**Action:** Paste message, press Enter

**What Happens:**
- Onboarding message pasted
- Enter sends message
- Agent receives fresh directives in clean context

**Code:**
```python
# Paste onboarding message
pyperclip.copy(onboarding_message)
pyautogui.hotkey("ctrl", "v")

# Send message
pyautogui.press("enter")
```

---

## 🛠️ **USAGE**

### **CLI Tool**

```bash
# Hard onboard single agent (with confirmation)
python -m src.services.messaging_cli \
  --hard-onboarding \
  --agent Agent-1 \
  --message "Your fresh start mission here"

# Skip confirmation prompt
python -m src.services.messaging_cli \
  --hard-onboarding \
  --agent Agent-1 \
  --message "Mission" \
  --yes

# With role assignment
python -m src.services.messaging_cli \
  --hard-onboarding \
  --agent Agent-1 \
  --role "Integration Specialist" \
  --message "Focus on core system integration"

# Load message from file
python -m src.services.messaging_cli \
  --hard-onboarding \
  --agent Agent-1 \
  --onboarding-file reset_mission.txt \
  --yes

# Dry run (test without executing)
python -m src.services.messaging_cli \
  --hard-onboarding \
  --agent Agent-1 \
  --message "Test" \
  --dry-run
```

### **Python API**

```python
from src.services.hard_onboarding_service import (
    HardOnboardingService,
    hard_onboard_agent,
    hard_onboard_multiple_agents
)

# Single agent
success = hard_onboard_agent(
    agent_id="Agent-1",
    onboarding_message="Your fresh start mission...",
    role="Integration Specialist"
)

# Multiple agents
agents = [
    ("Agent-1", "Mission 1"),
    ("Agent-2", "Mission 2"),
    ("Agent-3", "Mission 3")
]
results = hard_onboard_multiple_agents(agents, role="Team Reset")

# Step-by-step control
service = HardOnboardingService()
service.step_1_clear_chat("Agent-1")
service.step_2_send_execute()
service.step_3_new_window()
service.step_4_navigate_to_onboarding("Agent-1")
service.step_5_send_onboarding_message("Agent-1", "New mission")
```

---

## ⚙️ **SYSTEM INTEGRATION**

### **Coordinate Validation**

All coordinates validated before PyAutoGUI operations using:
- `cursor_agent_coords.json` (SSOT)
- Validation bounds checking
- Mismatch detection

### **Dependencies**

- `src/core/messaging_pyautogui.py` - Coordinate validation
- `src/core/coordinate_loader.py` - Coordinate loading
- `cursor_agent_coords.json` - Coordinate SSOT
- PyAutoGUI - UI automation
- pyperclip - Clipboard operations

---

## 🔄 **SOFT VS HARD ONBOARDING**

| Feature | Soft Onboarding | Hard Onboarding |
|---------|----------------|----------------|
| **Purpose** | Session transition | Complete reset |
| **Clears Chat** | ❌ No | ✅ Yes (Ctrl+Shift+Backspace) |
| **Session Cleanup** | ✅ Yes (Step 1) | ❌ No (immediate reset) |
| **New Chat** | ✅ Ctrl+T | ✅ Ctrl+N (new window) |
| **Context** | Preserves some | Completely fresh |
| **Coordinates** | Chat + Onboarding | Chat + Onboarding |
| **Confirmation** | Optional | **Required** (unless --yes) |
| **Use Case** | Regular sessions | Major resets |
| **Documentation** | Encouraged | N/A (fresh start) |

---

## 🚨 **SAFETY & CONFIRMATION**

### **Required Confirmation**

Hard onboarding requires explicit confirmation (unless `--yes` flag used):

```
🚨 HARD ONBOARDING WARNING!
This will RESET Agent-1 with:
  1. Clear chat (Ctrl+Shift+Backspace)
  2. Execute (Ctrl+Enter)
  3. New window (Ctrl+N)
  4. Navigate to onboarding input
  5. Send onboarding message

Continue? (yes/no):
```

### **Why Confirmation?**

- ❌ **Destructive operation** - clears agent context
- ❌ **Cannot be undone** - fresh start only
- ❌ **Loses current state** - no session preservation
- ✅ **Prevents accidents** - explicit user intent required

### **Bypass Confirmation**

Use `--yes` flag only when:
- ✅ Scripting/automation
- ✅ You're certain of the reset
- ✅ Fresh start is required
- ✅ No context preservation needed

---

## 📊 **SUCCESS CRITERIA**

✅ **Step 1 Success:**
- Chat input clicked
- Ctrl+Shift+Backspace executed
- Chat cleared

✅ **Step 2 Success:**
- Ctrl+Enter executed
- Clear command processed

✅ **Step 3 Success:**
- Ctrl+N executed
- New window created
- Fresh context ready

✅ **Step 4 Success:**
- Onboarding coordinates reached
- Input area clicked
- Ready for message

✅ **Step 5 Success:**
- Onboarding message pasted
- Enter pressed
- Agent receives directives in fresh context

---

## 🚨 **ERROR HANDLING**

**Coordinate Validation Failure:**
- Logs: `❌ Coordinate validation failed for {agent_id}`
- Action: Check `cursor_agent_coords.json` accuracy
- Fix: Update coordinates and retry

**PyAutoGUI Failure:**
- Logs: `❌ Failed to [step description]`
- Action: Verify PyAutoGUI installation
- Fix: `pip install pyautogui pyperclip`

**Agent Not Found:**
- Logs: `❌ No coordinates for {agent_id}`
- Action: Verify agent exists in `cursor_agent_coords.json`
- Fix: Add agent coordinates

**User Cancelled:**
- Logs: `🛑 Hard onboarding cancelled by user`
- Action: Normal - user chose not to proceed
- No fix needed

---

## 🎯 **BEST PRACTICES**

1. **Use sparingly** - Hard onboarding is for major resets only
2. **Prefer soft onboarding** for regular session transitions
3. **Always confirm** unless automated/scripted
4. **Document reason** for hard reset in onboarding message
5. **Test with --dry-run** before executing
6. **Use --yes carefully** - only when certain
7. **Allow initialization time** - new window needs ~1.5s
8. **Validate coordinates** - ensure accuracy before reset
9. **Have backup plan** - know agent's last state if needed
10. **Communicate reset** - inform team of major resets

---

## ⚠️ **WARNINGS**

**🚨 DESTRUCTIVE OPERATION:**
- Hard onboarding **CLEARS ALL CONTEXT**
- Previous conversation **CANNOT BE RECOVERED**
- Session state **LOST**
- Use only when **FRESH START REQUIRED**

**🚨 NO SESSION CLEANUP:**
- Unlike soft onboarding, **NO CLEANUP STEP**
- No passdown.json creation
- No devlog reminder
- No swarm brain update
- Agent resets **WITHOUT DOCUMENTATION**

**🚨 CONFIRMATION REQUIRED:**
- Always requires explicit confirmation
- Use `--yes` only when certain
- Accidental resets cannot be undone

---

## 📖 **EXAMPLE SCENARIOS**

### **Scenario 1: Major Development Phase Reset**
```bash
# Reset agent for completely new project phase
python -m src.services.messaging_cli \
  --hard-onboarding \
  --agent Agent-1 \
  --message "NEW PHASE: V3 Architecture Implementation. Previous work complete. Focus on: [...]" \
  --yes
```

### **Scenario 2: Troubleshooting Stuck Agent**
```bash
# Reset stuck agent with fresh directives
python -m src.services.messaging_cli \
  --hard-onboarding \
  --agent Agent-3 \
  --message "RESET: Infrastructure issues resolved. Continue with: [...]" \
  --yes
```

### **Scenario 3: Project-Wide Reset**
```python
# Reset multiple agents for new project
agents = [
    ("Agent-1", "NEW PROJECT: Core Systems"),
    ("Agent-2", "NEW PROJECT: Architecture Design"),
    ("Agent-3", "NEW PROJECT: Infrastructure Setup")
]
results = hard_onboard_multiple_agents(agents)
```

---

## 🐝 **CIVILIZATION-BUILDING NOTES**

**Hard Onboarding Impact:**
- ⚠️ **Context Loss**: All previous context cleared
- ⚠️ **Documentation Gap**: No automatic cleanup/devlog
- ✅ **Fresh Start**: Complete reset for major changes
- ✅ **Clean Slate**: No baggage from previous sessions

**When Hard Reset is Appropriate:**
- Major project phase transitions
- Complete architecture changes
- Troubleshooting persistent issues
- Starting entirely new development tracks

**Recommendation:**
Use soft onboarding (session cleanup protocol) for regular work. Reserve hard onboarding for true resets only.

---

**Status:** Protocol active and tested  
**Coordinate Validation:** Operational  
**Confirmation:** Required (unless --yes)  
**Safety:** Destructive operation warnings in place  

🐝 **WE. ARE. SWARM.** ⚡

