# 🤖 **CAPTAIN HARD ONBOARDING RUNBOOK**
==================================================================================

**Purpose**: Complete operational guide for Captain hard onboarding execution
**Version**: 1.0 (Hard Onboarding Integration Complete)
**Captain**: Agent-4 (Strategic Oversight & Emergency Intervention)
**Status**: ✅ OPERATIONAL - Complete CLI + Database + FSM Integration

---

## 🎯 **QUICK START CHECKLIST**

### **Pre-Flight Verification**
```bash
# 1. Validate coordinates configuration
python tools/validate_coordinates.py

# 2. Ensure database schema exists
sqlite3 unified.db < tools/migrations/2025_10_04_hard_onboarding.sql

# 3. Run smoke tests (optional but recommended)
pytest tests/test_hard_onboarding_smoke.py
```

### **Dry Run Test**
```bash
# Test onboarding flow without actual clicks
python tools/captain_onboard_cli.py --agent Agent-6 --dry-run --verbose
```

### **Live Execution**
```bash
# Execute real hard onboarding
python tools/captain_onboard_cli.py --agent Agent-6 --report --verbose
```

---

## 📋 **DETAILED OPERATIONS GUIDE**

### **1. Pre-Flight Checklist**

#### **Coordinates Validation**
```bash
# Validate default coordinates file
python tools/validate_coordinates.py

# Validate custom coordinates file
python tools/validate_coordinates.py config/custom_coordinates.json

# Quiet mode (CI-friendly)
python tools/validate_coordinates.py --quiet
```

**Expected Output:**
```
============================================================
COORDINATES VALIDATION: config/coordinates.json
============================================================
✅ Coordinates schema is valid
✅ All required agents have valid coordinates
✅ Ready for hard onboarding execution
============================================================
```

#### **Database Schema Migration**
```bash
# Apply database migration
sqlite3 unified.db < tools/migrations/2025_10_04_hard_onboarding.sql

# Verify tables created
sqlite3 unified.db ".tables"

# Check indexes
sqlite3 unified.db ".indexes"
```

**Expected Tables:**
- `cursor_tasks_integrated`
- `scanner_tasks`
- `fsm_task_tracking`

**Expected Indexes:**
- `idx_tasks_status`
- `idx_tasks_agent`
- `idx_fsm_state`

### **2. Dry Run Testing**

#### **Basic Dry Run**
```bash
python tools/captain_onboard_cli.py --agent Agent-6 --dry-run
```

#### **Verbose Dry Run**
```bash
python tools/captain_onboard_cli.py --agent Agent-6 --dry-run --verbose
```

#### **Dry Run with Report**
```bash
python tools/captain_onboard_cli.py --agent Agent-6 --dry-run --report
```

**Expected Output:**
```json
{
  "task_id": "onboard_Agent-6_20251004_143022",
  "agent_id": "Agent-6",
  "success": true,
  "exec_result": {
    "target_agent": "Agent-6",
    "success": true,
    "dry_run": true,
    "operation": "single_agent_onboarding"
  },
  "execution_orders": {
    "timestamp": "2025-10-04T14:30:22",
    "active_tasks": 1,
    "agent_assignments": {
      "Agent-6": {
        "active_tasks": 1,
        "high_priority": 0,
        "critical_tasks": 1
      }
    }
  },
  "dry_run": true
}
```

### **3. Live Execution**

#### **Basic Onboarding**
```bash
python tools/captain_onboard_cli.py --agent Agent-6
```

#### **Onboarding with Full Report**
```bash
python tools/captain_onboard_cli.py --agent Agent-6 --report --verbose
```

#### **Batch Onboarding (Multiple Agents)**
```bash
# Onboard multiple agents sequentially
for agent in Agent-5 Agent-6 Agent-7 Agent-8; do
  echo "Onboarding $agent..."
  python tools/captain_onboard_cli.py --agent $agent --report
  sleep 2  # Brief pause between agents
done
```

### **4. Status Monitoring**

#### **Check Agent Status**
```bash
python tools/captain_onboard_cli.py --agent Agent-6 --status
```

#### **Database Status Query**
```bash
# Check task status
sqlite3 unified.db "SELECT task_id, agent_id, status, fsm_state FROM cursor_tasks_integrated WHERE agent_id = 'Agent-6';"

# Check FSM tracking
sqlite3 unified.db "SELECT tracking_id, current_state, state_history FROM fsm_task_tracking WHERE agent_id = 'Agent-6';"
```

---

## 🚨 **TROUBLESHOOTING GUIDE**

### **Common Issues**

#### **1. Coordinates Validation Failures**
```
❌ Agent-6: invalid chat_input_coordinates
```

**Solution:**
- Check `config/coordinates.json` format
- Ensure coordinates are `[x, y]` integer arrays
- Verify coordinates are within screen bounds

#### **2. Database Connection Errors**
```
❌ Database initialization error: database is locked
```

**Solution:**
- Check if another process is using `unified.db`
- Ensure WAL mode is enabled: `PRAGMA journal_mode=WAL;`
- Restart any processes using the database

#### **3. PyAutoGUI Import Errors**
```
❌ PyAutoGUI not available, cannot hard onboard Agent-6
```

**Solution:**
- Install PyAutoGUI: `pip install pyautogui pyperclip`
- Use dry-run mode for testing: `--dry-run`
- Check display permissions (Linux/macOS)

#### **4. Task Creation Failures**
```
❌ Task assignment error: UNIQUE constraint failed
```

**Solution:**
- Check for duplicate task IDs
- Verify database schema is up to date
- Run migration: `sqlite3 unified.db < tools/migrations/2025_10_04_hard_onboarding.sql`

### **Emergency Procedures**

#### **Rollback Failed Onboarding**
```bash
# Mark task as failed
sqlite3 unified.db "UPDATE cursor_tasks_integrated SET status='FAILED', fsm_state='FAILED' WHERE agent_id='Agent-6' AND status='ACTIVE';"

# Clean up FSM tracking
sqlite3 unified.db "DELETE FROM fsm_task_tracking WHERE agent_id='Agent-6' AND current_state='ACTIVE';"
```

#### **Reset Agent State**
```bash
# Reset agent to initial state
sqlite3 unified.db "UPDATE cursor_tasks_integrated SET status='CREATED', fsm_state='ONBOARDING' WHERE agent_id='Agent-6';"
```

#### **Database Recovery**
```bash
# Backup current database
cp unified.db unified.db.backup

# Recreate schema
sqlite3 unified.db < tools/migrations/2025_10_04_hard_onboarding.sql

# Restore data if needed
sqlite3 unified.db.backup ".dump" | sqlite3 unified.db
```

---

## 📊 **MONITORING & METRICS**

### **Task Lifecycle Tracking**
```bash
# Monitor task progression
sqlite3 unified.db "SELECT task_id, agent_id, status, fsm_state, created_at FROM cursor_tasks_integrated ORDER BY created_at DESC LIMIT 10;"
```

### **FSM State Distribution**
```bash
# Check agent state distribution
sqlite3 unified.db "SELECT fsm_state, COUNT(*) FROM fsm_task_tracking GROUP BY fsm_state;"
```

### **Performance Metrics**
```bash
# Check execution times
sqlite3 unified.db "SELECT agent_id, COUNT(*) as tasks, AVG(julianday(updated_at) - julianday(created_at)) as avg_duration FROM cursor_tasks_integrated GROUP BY agent_id;"
```

---

## 🔧 **ADVANCED OPERATIONS**

### **Custom Integration Bridge Usage**
```python
# Direct integration bridge usage
from src.integrations.hard_onboarding_bridge import captain_hard_onboard

# Execute onboarding programmatically
result = captain_hard_onboard("Agent-6", dry_run=True)
print(f"Task ID: {result['task_id']}")
print(f"Success: {result['success']}")
```

### **Batch Operations**
```python
# Batch onboarding script
import subprocess
import json

agents = ["Agent-5", "Agent-6", "Agent-7", "Agent-8"]
results = []

for agent in agents:
    result = subprocess.run([
        "python", "tools/captain_onboard_cli.py",
        "--agent", agent, "--dry-run"
    ], capture_output=True, text=True)

    data = json.loads(result.stdout)
    results.append(data)

print(f"Processed {len(results)} agents")
```

### **CI/CD Integration**
```yaml
# GitHub Actions example
- name: Validate Hard Onboarding
  run: |
    python tools/validate_coordinates.py --quiet
    python tools/captain_onboard_cli.py --agent Agent-6 --dry-run
    pytest tests/test_hard_onboarding_smoke.py
```

---

## 📚 **REFERENCE**

### **File Locations**
- **Migration**: `tools/migrations/2025_10_04_hard_onboarding.sql`
- **Integration Bridge**: `src/integrations/hard_onboarding_bridge.py`
- **CLI Tool**: `tools/captain_onboard_cli.py`
- **Validator**: `tools/validate_coordinates.py`
- **Smoke Tests**: `tests/test_hard_onboarding_smoke.py`
- **Database**: `unified.db`

### **Key Commands**
```bash
# Validation
python tools/validate_coordinates.py

# Dry run
python tools/captain_onboard_cli.py --agent Agent-6 --dry-run

# Live execution
python tools/captain_onboard_cli.py --agent Agent-6 --report

# Status check
python tools/captain_onboard_cli.py --agent Agent-6 --status

# Smoke tests
pytest tests/test_hard_onboarding_smoke.py
```

### **Exit Codes**
- `0`: Success
- `1`: General error
- `2`: Missing coordinates file
- `3`: Invalid coordinates schema
- `130`: User interrupt (Ctrl+C)

---

## 🎯 **SUCCESS CRITERIA**

### **Pre-Flight Validation**
- ✅ Coordinates validation passes
- ✅ Database schema exists
- ✅ Smoke tests pass

### **Execution Validation**
- ✅ Task created with CRITICAL priority
- ✅ FSM state transitions: CREATED → ASSIGNED → ACTIVE → COMPLETED
- ✅ PyAutoGUI sequence executed (or dry-run simulated)
- ✅ Task marked as COMPLETED in database

### **Post-Execution Validation**
- ✅ Agent status shows COMPLETED
- ✅ Execution orders generated successfully
- ✅ Integration report shows healthy state

---

**🐝 WE ARE SWARM** - Hard Onboarding Integration Complete! 🚀

**📋 CAPTAIN AUTHORITY**: Agent-4 has exclusive control over hard onboarding operations with complete task database integration and FSM state management.

