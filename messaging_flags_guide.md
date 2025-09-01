# 🚀 **MESSAGING SYSTEM FLAGS GUIDE - COMPREHENSIVE REFERENCE**

## 📋 **OVERVIEW**

The Agent Cellphone V2 Messaging System provides **23 command-line flags** organized into logical categories. This guide explains each flag's purpose, usage, and how they differ from similar options.

### **🚀 QUICK START - DEFAULT BEHAVIOR**
```bash
# Send regular priority message (DEFAULT - just use Enter!)
python -m src.services.messaging_cli --agent Agent-X --message "Hello"

# Send to all agents (bulk)
python -m src.services.messaging_cli --bulk --message "System update"

# Get next task
python -m src.services.messaging_cli --agent Agent-X --get-next-task
```

### **⚠️ IMPORTANT: REGULAR PRIORITY IS THE DEFAULT**
- **No priority flag needed** = Regular priority (workflow-friendly)
- **Only use `--priority urgent`** or **`--high-priority`** for true emergencies
- **Regular priority** allows agents to finish current tasks before responding

---

## 🚨 **PRIORITY USAGE GUIDELINES - CRITICAL FOR WORKFLOW**

### **⚠️ PRIORITY SYSTEM OVERVIEW**
The messaging system uses a **two-tier priority system** designed to maintain workflow efficiency:

- **🟢 REGULAR PRIORITY** (Default): Allows agents to complete current tasks before responding
- **🔴 URGENT PRIORITY** (Emergency Only): Interrupts agents immediately for critical situations

### **✅ BEST PRACTICES**
```bash
# ✅ CORRECT: Use default regular priority for all normal communication
python -m src.services.messaging_cli --agent Agent-X --message "Status update"

# ❌ WRONG: Don't use high-priority for regular messages
python -m src.services.messaging_cli --agent Agent-X --message "Hello" --high-priority

# 🚨 EMERGENCY ONLY: Use urgent priority only for system failures
python -m src.services.messaging_cli --agent Agent-X --message "CRITICAL: System down!" --priority urgent
```

### **📊 WORKFLOW IMPACT**
- **Regular Priority**: Maintains 8x efficiency workflow, allows task completion
- **Urgent Priority**: Interrupts current work, requires immediate context switching
- **High Priority Flag**: Forces urgent regardless of other settings (use sparingly!)

### **🎯 WHEN TO USE URGENT PRIORITY**
- System crashes or critical failures
- Security breaches requiring immediate attention
- Time-sensitive emergencies that cannot wait
- **NOT for**: Regular updates, questions, coordination, or standard communication

---

## 🎯 **FLAG CATEGORIES & RELATIONSHIPS**

### **Mutual Exclusions:**
- `--agent` ↔ `--bulk` (cannot use both)
- `--onboarding` ↔ `--agent` (onboarding is always bulk)
- `--wrapup` ↔ `--agent` (wrapup is always bulk)

### **Dependencies:**
- `--get-next-task` **REQUIRES** `--agent`
- `--onboard` **REQUIRES** `--agent`
- `--message` required for standard message sending
- `--no-paste` only affects `--mode pyautogui`
- `--new-tab-method` only affects `--mode pyautogui`

---

## 📝 **MESSAGE CONTENT FLAGS**

### **`--message, -m`** (Required for standard messages)
```bash
--message "Your message content here"
```
- **Purpose**: Specifies the actual message content to send
- **Required**: Yes, for standard message sending
- **Default**: None (must be provided)
- **Usage**: Core content for any message operation
- **Differs from**: N/A (unique flag for message content)

### **`--sender, -s`** (Optional)
```bash
--sender "Captain Agent-4"
```
- **Purpose**: Sets the message sender identity
- **Required**: No
- **Default**: "Captain Agent-4" (from config)
- **Usage**: Override default sender identity
- **Differs from**: `--agent` (sender vs recipient), `--message` (who vs what)

---

## 👥 **RECIPIENT SELECTION FLAGS**

### **`--agent, -a`** (Single recipient)
```bash
--agent Agent-7
```
- **Purpose**: Send message to specific agent only
- **Required**: No (but required for `--get-next-task` and `--onboard`)
- **Default**: None (must specify recipient)
- **Usage**: Direct communication with individual agent
- **Conflicts with**: `--bulk`, `--onboarding`, `--wrapup`
- **Differs from**:
  - `--bulk`: Single agent vs all agents
  - `--onboarding`: Targeted agent vs all agents (onboarding)
  - `--wrapup`: Targeted agent vs all agents (wrapup)

### **`--bulk`** (All recipients)
```bash
--bulk
```
- **Purpose**: Send message to all agents simultaneously
- **Required**: No
- **Default**: False
- **Usage**: System-wide announcements, updates, broadcasts
- **Conflicts with**: `--agent`, `--onboarding`, `--wrapup`
- **Differs from**:
  - `--agent`: All agents vs single agent
  - `--onboarding`: General bulk vs specialized onboarding
  - `--wrapup`: General bulk vs specialized wrapup

---

## ⚙️ **MESSAGE PROPERTIES FLAGS**

### **`--type, -t`** (Message category)
```bash
--type text        # Standard message
--type broadcast   # System announcement
--type onboarding  # Agent initialization
```
- **Purpose**: Categorize message type for processing
- **Required**: No
- **Default**: "text"
- **Options**: `text`, `broadcast`, `onboarding`
- **Usage**:
  - `text`: Standard communication
  - `broadcast`: System-wide announcements
  - `onboarding`: Agent initialization/setup
- **Differs from**:
  - `--priority`: Message category vs delivery urgency
  - `--bulk`: Message type vs recipient scope

### **`--priority, -p`** (Delivery urgency)
```bash
# DEFAULT BEHAVIOR - No flag needed!
python -m src.services.messaging_cli --agent Agent-X --message "Hello"

# Only specify if you need urgent
--priority urgent   # EMERGENCY ONLY - disrupts workflow
```
- **Purpose**: Set delivery priority for queuing
- **Required**: No
- **Default**: `"regular"` (DEFAULT - use this!)
- **Options**: `regular`, `urgent`
- **Usage**:
  - `regular`: Standard priority (DEFAULT - allows workflow continuity)
  - `urgent`: High priority (EMERGENCY ONLY - disrupts agent workflow)
- **⚠️ CRITICAL**: Use `regular` by default. Only use `urgent` for true emergencies.
- **Differs from**:
  - `--type`: Delivery speed vs message category
  - `--high-priority`: Manual setting vs automatic override

### **`--high-priority`** (Priority override)
```bash
# ⚠️ WARNING: Disrupts agent workflow!
--high-priority  # EMERGENCY USE ONLY
```
- **Purpose**: Force urgent priority (overrides `--priority`)
- **Required**: No
- **Default**: False
- **Usage**: **EMERGENCY ONLY** - true system failures requiring immediate attention
- **⚠️ WARNING**: This flag disrupts agent workflow and should be avoided unless absolutely necessary
- **❌ AVOID**: Do not use this flag for regular communication - it interrupts agents mid-task
- **Conflicts with**: None (overrides other priority settings)
- **Differs from**:
  - `--priority urgent`: Automatic override vs manual setting
  - `--type`: Delivery speed vs message category

---

## 📨 **DELIVERY MODE FLAGS**

### **`--mode`** (Delivery mechanism)
```bash
--mode pyautogui   # GUI automation (default)
--mode inbox       # File-based delivery
```
- **Purpose**: Choose delivery method
- **Required**: No
- **Default**: "pyautogui" (from config)
- **Options**: `pyautogui`, `inbox`
- **Usage**:
  - `pyautogui`: Real-time GUI interaction
  - `inbox`: Reliable file-based storage
- **Differs from**:
  - `--bulk`: Delivery method vs recipient scope
  - `--priority`: Delivery method vs urgency

### **`--no-paste`** (PyAutoGUI typing method)
```bash
--no-paste
```
- **Purpose**: Disable clipboard paste (use keystroke typing)
- **Required**: No
- **Default**: False (paste enabled)
- **Usage**: When clipboard operations are unreliable
- **Only affects**: `--mode pyautogui`
- **Differs from**:
  - `--new-tab-method`: Paste method vs tab creation
  - `--mode inbox`: Typing method vs file delivery

### **`--new-tab-method`** (PyAutoGUI tab creation)
```bash
--new-tab-method ctrl_t  # New tab (default)
--new-tab-method ctrl_n  # New window
```
- **Purpose**: Choose tab/window creation method
- **Required**: No
- **Default**: "ctrl_t"
- **Options**: `ctrl_t` (new tab), `ctrl_n` (new window)
- **Only affects**: `--mode pyautogui`
- **Usage**:
  - `ctrl_t`: Standard new tab creation
  - `ctrl_n`: Isolated new window (agent separation)
- **Differs from**:
  - `--no-paste`: Tab creation vs content insertion
  - `--mode inbox`: Tab method vs file delivery

---

## 🔍 **UTILITY & INFORMATION FLAGS**

### **`--list-agents`** (Agent enumeration)
```bash
--list-agents
```
- **Purpose**: Display all available agents with details
- **Required**: No
- **Default**: N/A
- **Usage**: Get agent roster and capabilities
- **Output**: Agent names, roles, capabilities
- **Differs from**:
  - `--check-status`: Agent list vs status details
  - `--coordinates`: Agent names vs position data

### **`--coordinates`** (Position data)
```bash
--coordinates
```
- **Purpose**: Show PyAutoGUI coordinates for all agents
- **Required**: No
- **Default**: N/A
- **Usage**: Technical setup and debugging
- **Output**: X,Y coordinates for each agent
- **Differs from**:
  - `--list-agents`: Position data vs agent details
  - `--check-status`: Coordinates vs operational status

### **`--history`** (Message history)
```bash
--history
```
- **Purpose**: Show message delivery history
- **Required**: No
- **Default**: N/A
- **Usage**: Audit trail and troubleshooting
- **Output**: Previous message deliveries and status
- **Differs from**:
  - `--queue-stats`: Historical data vs current queue status
  - `--check-status`: Message history vs agent status

### **`--check-status`** (Agent status)
```bash
--check-status
```
- **Purpose**: Check status of all agents and contracts
- **Required**: No
- **Default**: N/A
- **Usage**: System health monitoring
- **Output**: Agent operational status and contract availability
- **Differs from**:
  - `--list-agents`: Status details vs basic agent list
  - `--queue-stats`: Agent status vs queue health

---

## 📊 **QUEUE MANAGEMENT FLAGS**

### **`--queue-stats`** (Queue health)
```bash
--queue-stats
```
- **Purpose**: Display message queue statistics
- **Required**: No
- **Default**: N/A
- **Usage**: Monitor queue health and performance
- **Output**: Pending, processing, delivered, failed counts
- **Differs from**:
  - `--check-status`: Queue metrics vs agent status
  - `--history`: Current queue vs historical data

### **`--process-queue`** (Manual processing)
```bash
--process-queue
```
- **Purpose**: Process one batch of queued messages
- **Required**: No
- **Default**: N/A
- **Usage**: Manual queue processing (one-time batch)
- **Output**: Processing results and updated statistics
- **Differs from**:
  - `--start-queue-processor`: Manual batch vs continuous processing
  - `--queue-stats`: Processing action vs status display

### **`--start-queue-processor`** (Background processing)
```bash
--start-queue-processor
```
- **Purpose**: Start continuous background queue processor
- **Required**: No
- **Default**: N/A
- **Usage**: Enable automatic queue processing
- **Output**: Processor startup confirmation
- **Differs from**:
  - `--process-queue`: Continuous background vs manual batch
  - `--stop-queue-processor`: Start vs stop operation

### **`--stop-queue-processor`** (Stop background processing)
```bash
--stop-queue-processor
```
- **Purpose**: Stop continuous background queue processor
- **Required**: No
- **Default**: N/A
- **Usage**: Disable automatic queue processing
- **Output**: Processor shutdown confirmation
- **Differs from**:
  - `--start-queue-processor`: Stop vs start operation
  - `--process-queue`: Stop background vs manual processing

---

## 🎓 **ONBOARDING FLAGS**

### **`--onboarding`** (Bulk onboarding)
```bash
--onboarding
```
- **Purpose**: Send onboarding message to all agents
- **Required**: No
- **Default**: N/A
- **Usage**: System-wide agent initialization
- **Conflicts with**: `--agent`, `--wrapup`
- **Differs from**:
  - `--onboard`: All agents vs specific agent
  - `--bulk`: Specialized onboarding vs general bulk

### **`--onboard`** (Single agent onboarding)
```bash
--onboard --agent Agent-7
```
- **Purpose**: Send onboarding message to specific agent
- **Required**: `--agent` must be specified
- **Default**: N/A
- **Usage**: Individual agent initialization
- **Differs from**:
  - `--onboarding`: Specific agent vs all agents
  - `--agent`: Onboarding context vs general messaging

### **`--onboarding-style`** (Message tone)
```bash
--onboarding-style friendly     # Casual approach
--onboarding-style professional # Formal approach
```
- **Purpose**: Set tone/style of onboarding messages
- **Required**: No
- **Default**: "friendly"
- **Options**: `friendly`, `professional`
- **Only affects**: `--onboarding` and `--onboard`
- **Usage**:
  - `friendly`: Casual, approachable language
  - `professional`: Formal, structured language
- **Differs from**:
  - `--type onboarding`: Message style vs message category
  - `--priority`: Tone vs delivery urgency

---

## 📋 **CONTRACT & TASK FLAGS**

### **`--get-next-task`** (Task assignment)
```bash
--get-next-task --agent Agent-7
```
- **Purpose**: Claim next contract task for specific agent
- **Required**: `--agent` must be specified
- **Default**: N/A
- **Usage**: Task assignment and contract management
- **Output**: Contract details, points, requirements
- **Differs from**:
  - `--check-status`: Task assignment vs status check
  - `--agent`: Task context vs general messaging

### **`--wrapup`** (System closure)
```bash
--wrapup
```
- **Purpose**: Send wrapup message to all agents
- **Required**: No
- **Default**: N/A
- **Usage**: System shutdown or cycle completion
- **Conflicts with**: `--agent`, `--onboarding`
- **Differs from**:
  - `--bulk`: Specialized wrapup vs general bulk
  - `--onboarding`: System closure vs system startup

---

## 🔀 **FLAG COMBINATION MATRIX**

### **Valid Combinations:**
```bash
# Basic messaging
--agent Agent-7 --message "Hello"

# Bulk communication
--bulk --message "System update"

# High priority urgent message
--agent Agent-7 --message "Emergency" --high-priority

# Onboarding with style
--onboarding --onboarding-style professional

# Queue management
--queue-stats
--process-queue

# Task management
--agent Agent-7 --get-next-task
```

### **Invalid Combinations:**
```bash
# ❌ Cannot combine single agent with bulk
--agent Agent-7 --bulk --message "Test"

# ❌ Onboarding cannot target specific agent
--agent Agent-7 --onboarding

# ❌ Wrapup cannot target specific agent
--agent Agent-7 --wrapup

# ❌ Task assignment requires specific agent
--get-next-task  # Missing --agent
```

---

## 📊 **FLAG USAGE STATISTICS**

| Category | Flag Count | Primary Use Case |
|----------|------------|------------------|
| **Message Content** | 2 | Content specification |
| **Recipient Selection** | 2 | Target specification |
| **Message Properties** | 3 | Message characteristics |
| **Delivery Mode** | 3 | Delivery mechanism |
| **Utility/Information** | 4 | System information |
| **Queue Management** | 4 | Queue operations |
| **Onboarding** | 3 | Agent initialization |
| **Contract/Task** | 2 | Task management |

**Total: 23 flags** across 8 functional categories

---

## 🎯 **BEST PRACTICES & RECOMMENDATIONS**

### **1. Message Sending:**
- Use `--bulk` for system-wide announcements
- Use `--urgent` for time-critical communications
- Use `--high-priority` for emergencies only

### **2. Queue Management:**
- Use `--queue-stats` regularly for monitoring
- Use `--start-queue-processor` for continuous processing
- Use `--process-queue` for manual batch processing

### **3. System Administration:**
- Use `--check-status` for system health
- Use `--coordinates` for technical setup
- Use `--history` for troubleshooting

### **4. Agent Management:**
- Use `--onboarding` for new agent initialization
- Use `--get-next-task` for contract assignment
- Use `--wrapup` for system shutdown

---

## 🚨 **COMMON PITFALLS TO AVOID**

1. **Don't mix recipient flags**: `--agent` and `--bulk` cannot be used together
2. **Don't forget dependencies**: `--get-next-task` requires `--agent`
3. **Don't overuse urgent priority**: Reserve `--urgent` for actual emergencies
4. **Don't use PyAutoGUI flags with inbox mode**: `--no-paste` and `--new-tab-method` only work with `--mode pyautogui`
5. **Don't run multiple queue processors**: Use either `--start-queue-processor` or manual `--process-queue`, not both simultaneously

---

## 📋 **FLAG QUICK REFERENCE**

| Flag | Short | Purpose | Requires | Conflicts |
|------|-------|---------|----------|-----------|
| `--message` | `-m` | Message content | - | - |
| `--sender` | `-s` | Message sender | - | - |
| `--agent` | `-a` | Single recipient | - | `--bulk`, `--onboarding`, `--wrapup` |
| `--bulk` | - | All recipients | - | `--agent`, `--onboarding`, `--wrapup` |
| `--type` | `-t` | Message category | - | - |
| `--priority` | `-p` | Delivery urgency | - | - |
| `--high-priority` | - | Priority override | - | - |
| `--mode` | - | Delivery method | - | - |
| `--no-paste` | - | Typing method | `--mode pyautogui` | - |
| `--new-tab-method` | - | Tab creation | `--mode pyautogui` | - |
| `--list-agents` | - | Agent roster | - | - |
| `--coordinates` | - | Position data | - | - |
| `--history` | - | Message history | - | - |
| `--check-status` | - | System status | - | - |
| `--queue-stats` | - | Queue health | - | - |
| `--process-queue` | - | Manual processing | - | - |
| `--start-queue-processor` | - | Auto processing | - | - |
| `--stop-queue-processor` | - | Stop auto processing | - | - |
| `--onboarding` | - | Bulk onboarding | - | `--agent`, `--wrapup` |
| `--onboard` | - | Single onboarding | `--agent` | - |
| `--onboarding-style` | - | Message tone | - | - |
| `--get-next-task` | - | Task assignment | `--agent` | - |
| `--wrapup` | - | System closure | - | `--agent`, `--onboarding` |

---

**Prepared by: Captain Agent-4**  
**Strategic Oversight & Emergency Intervention Manager**  
**Date: 2025-09-01**  
**Version: 2.0**  

**WE. ARE. SWARM. ⚡️🔥**
