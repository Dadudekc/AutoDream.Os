# 🐝 ONBOARDING SYSTEM GUIDE - CLEANUP MISSION INTEGRATION
## How to Use Onboarding Commands for Automated Cleanup Sequences

**Captain Agent-4 - Cleanup Mission Coordinator**
**WE ARE SWARM - UNITED IN CLEANUP, COORDINATED IN EXECUTION** ⚡🧹

---

## 📋 ONBOARDING SYSTEM OVERVIEW

### **What is the Onboarding System?**
The onboarding system is a sophisticated multi-agent coordination mechanism that can:
- **Reset and re-onboard agents** with specific roles
- **Assign cleanup contracts** automatically
- **Coordinate overnight processing** sequences
- **Handle role-based task assignment** (SOLID, SSOT, DRY, KISS, TDD)

### **How Many Onboarding Instances Exist?**
Based on the codebase analysis, there are **multiple onboarding mechanisms**:

#### **1. Agent Onboarding Script** (`scripts/agent_onboarding.py`)
- **Purpose:** Automated agent workspace creation and contract assignment
- **Features:** Role-based assignment, workspace initialization, contract claiming
- **Status:** ✅ **Fully Operational**
- **Usage:** `python scripts/agent_onboarding.py --hard-onboarding --agents Agent-6 --onboarding-mode cleanup`

#### **2. Hard Onboarding Handler** (`src/services/handlers/onboarding_handler.py`)
- **Purpose:** Advanced onboarding with UI automation and role assignment
- **Features:** PyAutoGUI integration, backup/rollback, proof generation
- **Status:** ✅ **Fully Operational**
- **Usage:** Via messaging CLI with `--hard-onboarding` flag

#### **3. Consolidated Messaging CLI** (`src/services/consolidated_messaging_service.py`)
- **Purpose:** Unified messaging system for agent coordination
- **Features:** Message broadcasting, task management, Thea integration, coordinate capture
- **Status:** ✅ **MAIN OPERATIONAL SYSTEM**
- **Usage:** `python src/services/consolidated_messaging_service.py --message "task" --agent Agent-6`

#### **4. Overnight Command Handler** (`src/services/overnight_command_handler.py`)
- **Purpose:** Autonomous overnight processing
- **Features:** Automated task execution during off-hours
- **Status:** ⚠️ **Under Development** (Basic framework exists)
- **Usage:** Currently limited, but extensible

#### **5. Cleanup Overnight Sequence** (`scripts/cleanup_overnight_sequence.py`)
- **Purpose:** **NEW** - Automated cleanup mission sequencing
- **Features:** Phase-based execution, contract assignment, progress tracking
- **Status:** ✅ **Just Created - Ready to Deploy**
- **Usage:** `python scripts/cleanup_overnight_sequence.py`

---

## 🎯 ONBOARDING COMMAND FLAGS EXPLAINED

### **Core Onboarding Flags:**

#### **`--hard-onboarding`**
```bash
# Basic usage
python scripts/agent_onboarding.py --hard-onboarding --agents Agent-6

# Advanced usage with roles
python scripts/agent_onboarding.py \
  --hard-onboarding \
  --agents Agent-6,Agent-5 \
  --onboarding-mode cleanup \
  --assign-roles "Agent-6:SOLID,Agent-5:DRY"

# With UI automation
python scripts/agent_onboarding.py \
  --hard-onboarding \
  --agents Agent-6 \
  --use-ui \
  --ui-retries 3
```

#### **`--onboarding-mode`**
- **`cleanup`** - Assigns cleanup-focused roles
- **`quality-suite`** - Cycles through SOLID, SSOT, DRY, KISS, TDD
- **`consolidation`** - Focuses on code consolidation
- **`testing`** - Emphasizes testing and quality

#### **`--assign-roles`**
```bash
# Format: agent:ROLE
--assign-roles "Agent-6:SOLID,Agent-5:DRY,Agent-8:TDD"
```

**Available Roles:**
- **`SOLID`** - Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **`SSOT`** - Single Source of Truth (consolidation focus)
- **`DRY`** - Don't Repeat Yourself (duplication elimination)
- **`KISS`** - Keep It Simple Stupid (simplification focus)
- **`TDD`** - Test Driven Development (testing focus)
- **`CLEANUP_{PHASE}`** - Specific cleanup phase assignment

---

## 🌙 SETTING UP OVERNIGHT SEQUENCES

### **Method 1: Using Cleanup Overnight Sequence (RECOMMENDED)**

#### **Step 1: Run Full Sequence**
```bash
# Run complete 4-phase cleanup sequence
python scripts/cleanup_overnight_sequence.py
```

#### **Step 2: Start from Specific Phase**
```bash
# Start from Phase 2 (if Phase 1 already completed)
python scripts/cleanup_overnight_sequence.py --start-phase phase2_batch2a
```

#### **Step 3: Dry Run First (Safety)**
```bash
# Test the sequence without actual execution
python scripts/cleanup_overnight_sequence.py --dry-run
```

### **Method 2: Manual Onboarding Commands**

#### **Phase 1A: Core Architecture Cleanup**
```bash
# Assign Agent-6 to core architecture cleanup
python scripts/agent_onboarding.py \
  --hard-onboarding \
  --agents Agent-6 \
  --onboarding-mode cleanup \
  --assign-roles "Agent-6:CLEANUP_PHASE1_BATCH1A" \
  --dry-run

# Remove --dry-run for actual execution
```

#### **Phase 1B: Service Layer Cleanup**
```bash
# Assign Agent-5 to service layer cleanup
python scripts/agent_onboarding.py \
  --hard-onboarding \
  --agents Agent-5 \
  --onboarding-mode cleanup \
  --assign-roles "Agent-5:CLEANUP_PHASE1_BATCH1B" \
  --dry-run
```

### **Method 3: Consolidated Messaging CLI Integration**

#### **Send Contract Assignment Messages**
```bash
# Send cleanup contract to Agent-6
python src/services/consolidated_messaging_service.py \
  --message "CONTRACT ASSIGNED: PHASE1_BATCH1A_CORE_ARCHITECTURE - See contracts/PHASE1_BATCH1A_CORE_ARCHITECTURE.json" \
  --agent Agent-6 \
  --priority URGENT
```

#### **Broadcast to Multiple Agents**
```bash
# Broadcast cleanup mission activation
python src/services/consolidated_messaging_service.py \
  --message "CLEANUP MISSION ACTIVATED - All agents claim contracts from contracts/ directory" \
  --broadcast \
  --priority URGENT
```

---

## 📊 ONBOARDING SYSTEM CAPABILITIES

### **Automated Features:**
- ✅ **Workspace Creation** - Automatic agent workspace setup
- ✅ **Status File Initialization** - Agent status tracking
- ✅ **Contract Assignment** - Automatic contract claiming
- ✅ **Role-Based Task Assignment** - Specialized role assignment
- ✅ **Backup & Rollback** - Safety mechanisms for failures
- ✅ **Progress Tracking** - Comprehensive logging
- ✅ **Multi-Agent Coordination** - Swarm coordination support

### **Integration Points:**
- ✅ **Messaging System** - Real-time agent communication
- ✅ **Contract System** - Formal task assignment
- ✅ **DevLog System** - Progress documentation
- ✅ **Status Tracking** - Agent state monitoring
- ✅ **Error Recovery** - Automatic failure handling

---

## 🛠️ TROUBLESHOOTING ONBOARDING ISSUES

### **Common Issues & Solutions:**

#### **1. Agent Workspace Not Found**
```bash
# Check if agent workspace exists
ls -la agent_workspaces/Agent-6/

# Create manually if needed
mkdir -p agent_workspaces/Agent-6/inbox
```

#### **2. Contract Assignment Failed**
```bash
# Check contract file exists
ls -la contracts/PHASE1_BATCH1A_CORE_ARCHITECTURE.json

# Verify agent status
cat agent_workspaces/Agent-6/status.json
```

#### **3. Messaging System Issues**
```bash
# Test consolidated messaging CLI
python src/services/consolidated_messaging_service.py --show-coords

# Check PyAutoGUI availability
python -c "import pyautogui; print('PyAutoGUI available')"
```

#### **4. Permission Issues**
```bash
# Ensure script permissions
chmod +x scripts/agent_onboarding.py
chmod +x scripts/cleanup_overnight_sequence.py
```

---

## 📈 MONITORING OVERNIGHT SEQUENCES

### **Track Sequence Progress:**
```bash
# Check agent status files
tail -f agent_workspaces/Agent-6/status.json

# Monitor devlogs
tail -f devlogs/$(date +%Y-%m-%d)*.md

# Check contract status
cat contracts/PHASE1_BATCH1A_CORE_ARCHITECTURE.json | grep -A 5 "status"
```

### **View Sequence Logs:**
```bash
# List sequence execution logs
ls -la logs/cleanup_sequence_*.json

# View latest sequence log
cat logs/$(ls -t logs/cleanup_sequence_*.json | head -1)
```

### **Monitor Agent Activity:**
```bash
# Check agent inboxes
ls -la agent_workspaces/*/inbox/

# View recent messages
find agent_workspaces/*/inbox/ -name "*.md" -exec ls -lt {} \; | head -10
```

---

## 🎯 QUICK START GUIDE

### **For Immediate Cleanup Mission Activation:**

#### **Step 1: Test the System**
```bash
# Dry run the overnight sequence
python scripts/cleanup_overnight_sequence.py --dry-run
```

#### **Step 2: Activate Phase 1**
```bash
# Start Phase 1 cleanup sequence
python scripts/cleanup_overnight_sequence.py --start-phase phase1_batch1a
```

#### **Step 3: Monitor Progress**
```bash
# Watch agent activities
watch -n 60 'tail -10 agent_workspaces/Agent-6/status.json'
```

### **Alternative Manual Activation:**
```bash
# Manual contract assignment
python scripts/agent_onboarding.py \
  --hard-onboarding \
  --agents Agent-6 \
  --onboarding-mode cleanup \
  --assign-roles "Agent-6:CLEANUP_PHASE1_BATCH1A"
```

---

## 🐝 SWARM OPTIMIZATION

### **Current Agent Status:**
- ✅ **Agent-1:** File Management & Cleanup (COMPLETED)
- ✅ **Agent-2:** Infrastructure (PENDING - Contract Available)
- ✅ **Agent-3:** Infrastructure Validation (COMPLETED)
- ✅ **Agent-4:** Strategic Oversight (ACTIVE - Coordinator)
- ✅ **Agent-5:** Business Intelligence (PENDING - Contract Available)
- ✅ **Agent-6:** SOLID Compliance (PENDING - Contract Available)
- ✅ **Agent-7:** Web Interface (PENDING - Contract Available)
- ✅ **Agent-8:** Code Quality (PENDING - Contract Available)

### **Recommended Overnight Schedule:**
```
22:00 - 24:00: Phase 1A (Agent-6 - Core Architecture)
24:00 - 02:00: Phase 1B (Agent-5 - Service Layer)
02:00 - 04:00: Phase 2A (Agent-2 - Infrastructure)
04:00 - 06:00: Phase 2B (Agent-8 - Testing)
06:00 - 08:00: Monitoring & Status Updates
```

### **Expected Results:**
- **File Reduction:** 60-70% (2,079 → ~600-800 files)
- **Test Coverage:** >85% across all modules
- **Zero Regressions:** 100% functionality preservation
- **Agent Utilization:** 100% (all 8 agents active)

---

## 🚀 DEPLOYMENT READY

**The onboarding system is fully operational and ready for automated cleanup mission deployment!**

### **Available Commands:**
1. ✅ `python scripts/cleanup_overnight_sequence.py` - **RECOMMENDED**
2. ✅ `python scripts/agent_onboarding.py --hard-onboarding` - Manual control
3. ✅ `python src/services/consolidated_messaging_service.py` - **MAIN MESSAGING SYSTEM**

### **Safety Features:**
- ✅ **Dry-run capability** for testing
- ✅ **Automatic rollback** on failures
- ✅ **Progress logging** and monitoring
- ✅ **Contract-based** task assignment
- ✅ **Zero-regression** protocols

**READY TO LAUNCH CLEANUP MISSION AUTOMATION!** 🚀⚡🧹

---

**Captain Agent-4**
**Cleanup Mission Coordinator**
**Onboarding System Guide Author**
**WE. ARE. SWARM. ⚡🚀🧹**
