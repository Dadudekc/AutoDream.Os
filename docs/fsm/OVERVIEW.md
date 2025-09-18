# Dream.OS FSM Overview

## 🎯 **Finite State Machine System**

The Dream.OS FSM (Finite State Machine) system provides canonical state management for agents and swarm coordination. This system ensures consistent state tracking across all components.

## 📊 **Agent FSM States**

```ascii
Agent FSM
──────────
 ONBOARDING ──┐
              ▼
           ACTIVE ──► CONTRACT_EXECUTION_ACTIVE ──► SURVEY_MISSION_COMPLETED
              ▲                                            │
              └─────────────◄───────────────◄──────────────┘
              │
              ├─► PAUSED
              ├─► ERROR ─► RESET ─► ACTIVE
              └─► SHUTDOWN (terminal)
```

### **Agent States:**

- **`ONBOARDING`** - Initial agent setup and configuration
- **`ACTIVE`** - Agent ready for task assignment
- **`CONTRACT_EXECUTION_ACTIVE`** - Agent executing assigned contract
- **`SURVEY_MISSION_COMPLETED`** - Agent completed survey/mission
- **`PAUSED`** - Agent temporarily paused (maintenance)
- **`ERROR`** - Agent in error state, requires intervention
- **`RESET`** - Agent recovering from error state
- **`SHUTDOWN`** - Agent shutting down (terminal state)

## 🐝 **Swarm FSM States**

```ascii
Swarm FSM
──────────
 IDLE ─► COORDINATING ─► BROADCAST
  │            │               │
  └────────────┴──► DEGRADED ◄─┘
                 │
                 └─► HALT (terminal)
```

### **Swarm States:**

- **`IDLE`** - Swarm idle, no active coordination
- **`COORDINATING`** - Swarm actively coordinating agents
- **`BROADCAST`** - Swarm broadcasting to all agents
- **`DEGRADED`** - Swarm operating in degraded mode
- **`HALT`** - Swarm halted (terminal state)

## 📁 **Status File Locations**

### **Agent Status Files:**
- **Primary:** `agent_workspaces/{Agent-ID}/status.json`
- **Secondary:** `data/semantic_seed/status/{Agent-ID}.json`

### **Swarm Status Files:**
- **Primary:** `swarm_coordination/swarm_state.json`

## 🔧 **FSM System Components**

### **1. FSM Specification**
- **File:** `runtime/fsm/fsm_spec.yaml`
- **Purpose:** Canonical state definitions and transitions
- **Owner:** V2_SWARM

### **2. FSM Registry**
- **File:** `src/fsm/fsm_registry.py`
- **Purpose:** State management and validation functions
- **Features:**
  - State validation
  - Status file reading/writing
  - State summary generation

### **3. FSM Scanner**
- **File:** `tools/fsm/fsm_scan.py`
- **Purpose:** Validate all status files for consistency
- **Usage:** `python tools/fsm/fsm_scan.py`

### **4. FSM Tests**
- **File:** `tests/test_fsm_consistency.py`
- **Purpose:** Unit tests for FSM validation
- **Usage:** `pytest tests/test_fsm_consistency.py`

### **5. FSM CI Script**
- **File:** `scripts/fsm_ci.sh`
- **Purpose:** CI validation of FSM system
- **Usage:** `bash scripts/fsm_ci.sh`

## 📋 **State Transition Rules**

### **Agent Transitions:**
- `ONBOARDING` → `ACTIVE` (when environment ready)
- `ACTIVE` → `CONTRACT_EXECUTION_ACTIVE` (when contract assigned)
- `CONTRACT_EXECUTION_ACTIVE` → `SURVEY_MISSION_COMPLETED` (when contract complete)
- `SURVEY_MISSION_COMPLETED` → `ACTIVE` (when new tasks available)
- `ACTIVE` → `PAUSED` (during maintenance)
- `*` → `ERROR` (on fatal exception)
- `ERROR` → `RESET` (when autoheal possible)
- `RESET` → `ACTIVE` (when health restored)
- `*` → `SHUTDOWN` (on shutdown signal)

### **Swarm Transitions:**
- `IDLE` → `COORDINATING` (when 2+ agents active)
- `COORDINATING` → `BROADCAST` (on global announcement)
- `COORDINATING` → `DEGRADED` (when unhealthy ratio > 25%)
- `DEGRADED` → `COORDINATING` (when recovery complete)
- `*` → `HALT` (on emergency stop)

## 🚨 **Validation Requirements**

### **State Validation:**
- All status files MUST use canonical state names
- No custom or ad-hoc state values allowed
- State transitions must follow defined rules

### **File Validation:**
- Status files must be valid JSON
- Required fields must be present
- State values must match enum definitions

### **CI Validation:**
- FSM scan must pass with 0 issues
- All consistency tests must pass
- State files must use canonical values

## 🛠️ **Usage Examples**

### **Reading Agent State:**
```python
from src.fsm.fsm_registry import read_agent_state

state = read_agent_state("Agent-1")
print(f"Agent-1 state: {state}")
```

### **Validating State:**
```python
from src.fsm.fsm_registry import validate_agent_state

is_valid = validate_agent_state("ACTIVE")
print(f"State valid: {is_valid}")
```

### **Getting State Summary:**
```python
from src.fsm.fsm_registry import get_state_summary

summary = get_state_summary()
print(f"Active agents: {summary['active_agents']}")
```

### **Running FSM Scan:**
```bash
python tools/fsm/fsm_scan.py
```

### **Running FSM Tests:**
```bash
pytest tests/test_fsm_consistency.py
```

### **Running FSM CI:**
```bash
bash scripts/fsm_ci.sh
```

## 📊 **State Monitoring**

### **Status Sources:**
- Agent workspace status files
- Semantic seed status files
- Swarm coordination files

### **Monitoring Fields:**
- `fsm_state` - Current state
- `last_transition` - Last state change
- `health` - Health status
- `run_id` - Execution run ID

## 🔄 **Integration Points**

### **Messaging System:**
- FSM states integrated with messaging system
- State changes trigger notifications
- Status monitoring via messaging service

### **Discord Commander:**
- FSM states accessible via Discord commands
- State monitoring and reporting
- Agent coordination based on states

### **Quality Gates:**
- FSM validation integrated with quality gates
- State consistency enforced in CI/CD
- Automated state validation

## 🎯 **Best Practices**

### **State Management:**
- Always use canonical state names
- Update states immediately on transitions
- Validate states before updates
- Maintain state consistency across files

### **Error Handling:**
- Handle invalid states gracefully
- Provide clear error messages
- Log state transition failures
- Implement fallback mechanisms

### **Testing:**
- Test all state transitions
- Validate state consistency
- Test error conditions
- Run FSM CI regularly

## 📝 **Migration Guide**

### **From Legacy States:**
- Replace `"active"` with `"ACTIVE"`
- Replace `"onboarding"` with `"ONBOARDING"`
- Replace `"ACTIVE_AGENT_MODE"` with `"ACTIVE"`
- Update all status files to use canonical states

### **Backfill Process:**
1. Run FSM scan to identify issues
2. Update status files with canonical states
3. Validate changes with FSM tests
4. Run FSM CI to confirm consistency

## 🚀 **Future Enhancements**

### **Planned Features:**
- State transition logging
- Automated state recovery
- State-based routing
- Enhanced monitoring

### **Integration Plans:**
- Real-time state updates
- State-based task assignment
- Automated state transitions
- State analytics dashboard

---

## 📋 **Quick Reference**

### **Valid Agent States:**
```
ONBOARDING, ACTIVE, CONTRACT_EXECUTION_ACTIVE, 
SURVEY_MISSION_COMPLETED, PAUSED, ERROR, RESET, SHUTDOWN
```

### **Valid Swarm States:**
```
IDLE, COORDINATING, BROADCAST, DEGRADED, HALT
```

### **Key Files:**
- `runtime/fsm/fsm_spec.yaml` - FSM specification
- `src/fsm/fsm_registry.py` - FSM registry
- `tools/fsm/fsm_scan.py` - FSM scanner
- `tests/test_fsm_consistency.py` - FSM tests
- `scripts/fsm_ci.sh` - FSM CI script

**📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory**
