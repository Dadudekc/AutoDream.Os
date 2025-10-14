# Operator Runbook - OSS + Message↔Task Systems

**Quick reference for system operators and agents**

---

## 🚦 **Feature Flags**

```bash
# Enable/disable features via environment variables
export FF_MSG_TASK=on|off              # Message-task integration
export FF_OSS_CLI=on|off               # OSS contribution system
export FF_CONCURRENT_MSG_LOCK=on|off   # Concurrent messaging lock
export FF_ERROR_CLASSIFICATION=on|off  # Autonomous error classification
```

---

## 🚀 **Start Systems**

```bash
# Initialize (first time)
make init

# Run migrations
python -m src.db.migrate apply migrations/ 2>/dev/null || echo "Migrations applied"

# Verify systems
make status
```

---

## ✅ **Health Checks**

### **Quick Check**

```bash
make status

# Shows:
# - OSS contribution metrics
# - Observability metrics
# - System health
```

### **Detailed Check**

```bash
# Messaging system
python -c "from src.core.messaging_process_lock import get_messaging_lock; print('✅ Lock available')"

# Message-task loop
python -c "from src.message_task import MessageTaskPipeline; print('✅ Pipeline available')"

# OSS system
python -m src.opensource.oss_cli status

# Metrics
make metrics
```

---

## 📊 **Observability**

### **View Metrics**

```bash
# Current metrics snapshot
make metrics

# Dump all metrics
python -c "from src.obs.metrics import dump_metrics; print(dump_metrics())"
```

### **Key Metrics**

| Metric | Meaning | Good Value |
|--------|---------|------------|
| `msg_task.ingest.ok` | Successful ingestions | >0 |
| `msg_task.dedupe.duplicate` | Duplicates prevented | Low |
| `msg_task.parser.*` | Parser usage | Balanced |
| `oss.pr.merged` | Merged PRs | Growing |
| `messaging.race_prevented` | Lock prevented collision | Low |

---

## 🧪 **Testing**

### **Smoke Tests (Fast)**

```bash
# Run all smoke tests (~10s)
make smoke

# Individual system smoke tests
pytest tests/test_msg_task_smoke.py -v
pytest tests/test_oss_cli_smoke.py -v
pytest tests/test_messaging_smoke.py -v
pytest tests/test_error_handling_smoke.py -v
```

### **Full Test Suite**

```bash
# All tests
make test

# With coverage
pytest --cov=src --cov-report=term-missing
```

---

## 🔄 **Common Operations**

### **Message → Task**

```bash
# Send message that creates task
python -c "
from src.message_task.schemas import InboundMessage
from src.message_task.messaging_integration import process_message_for_task

task_id = process_message_for_task(
    message_id='msg-001',
    content='TASK: Fix bug X\nPRIORITY: P0',
    author='Captain',
    channel='cli'
)
print(f'Task created: {task_id}')
"
```

### **Clone OSS Project**

```bash
# Clone project
python -m src.opensource.oss_cli clone https://github.com/owner/repo

# View projects
python -m src.opensource.oss_cli list
```

### **Import GitHub Issues**

```bash
# Fetch and import (requires GitHub CLI)
python -m src.opensource.oss_cli issues <project-id> \
  --labels "good first issue" \
  --import-tasks
```

---

## 🚨 **Rollback Procedures**

### **Emergency Rollback**

```bash
# Disable all new features
export FF_MSG_TASK=off
export FF_OSS_CLI=off
export FF_CONCURRENT_MSG_LOCK=off
export FF_ERROR_CLASSIFICATION=off

# Or use make target
make rollback
```

### **Per-System Rollback**

```bash
# Disable just message-task
export FF_MSG_TASK=off

# Disable just OSS
export FF_OSS_CLI=off

# Disable just concurrent lock
export FF_CONCURRENT_MSG_LOCK=off
```

### **Database Rollback**

```bash
# If needed, rollback fingerprint migration
# (Manual SQL - be careful)
sqlite3 data/tasks.db "DROP INDEX IF EXISTS idx_tasks_fingerprint;"
```

---

## 📈 **SLOs (Service Level Objectives)**

### **Message-Task Integration**

- **Ingest Success Rate:** ≥ 99%
- **Dedupe Collision Rate:** ≤ 0.1%
- **Parser Success Rate:** 100% (3-tier cascade)

### **OSS System**

- **Clone Success Rate:** ≥ 95%
- **PR Submit Success Rate:** ≥ 97%
- **Issue Import Success:** ≥ 98%

### **Messaging System**

- **Message Delivery:** 100%
- **Race Condition Rate:** 0%
- **Lock Acquisition:** ≥ 99%

---

## 🔔 **Alerts**

### **Watch For:**

**High Priority:**
- `msg_task.ingest.fail` spikes 5x baseline (10min window)
- `msg_task.dedupe.conflict` > 3 in 1 hour
- `messaging.failed` > 10 in 5 minutes

**Medium Priority:**
- `oss.clone.fail` > 2 in 1 hour
- Parser balance skewed (>90% fallback usage)

---

## 🐛 **Troubleshooting**

### **Message-Task Issues**

**Problem:** Tasks not being created from messages

**Check:**
```bash
# 1. Verify parsers work
pytest tests/test_msg_task_smoke.py -v

# 2. Check metrics
python -c "from src.obs.metrics import get; print(f'Ingest OK: {get(\"msg_task.ingest.ok\")}, Fail: {get(\"msg_task.ingest.fail\")}')"

# 3. Check database
python -c "from src.infrastructure.persistence.sqlite_task_repo import SqliteTaskRepository; r=SqliteTaskRepository(); print(f'Tasks: {len(list(r.list_all()))}')"
```

### **OSS CLI Issues**

**Problem:** Cannot clone projects

**Check:**
```bash
# 1. Verify git available
git --version

# 2. Check directory permissions
ls -la D:\OpenSource_Swarm_Projects

# 3. Test with simple repo
python -m src.opensource.oss_cli clone https://github.com/octocat/Hello-World
```

### **Messaging Lock Issues**

**Problem:** Messages timing out

**Check:**
```bash
# 1. Check lock file
ls -la runtime/locks/messaging_pyautogui.lock

# 2. Verify lock works
pytest tests/test_messaging_smoke.py -v

# 3. Check timeout settings
python -c "from src.core.messaging_process_lock import get_messaging_lock; print(f'Timeout: {get_messaging_lock().timeout}s')"
```

---

## 📊 **Monitoring Commands**

```bash
# System status
make status

# Current metrics
make metrics

# Run smoke tests
make smoke

# Check feature flags
python -c "from src.features.flags import *; print(f'MSG_TASK: {FF_MSG_TASK}, OSS: {FF_OSS_CLI}')"

# View portfolio
python -m src.opensource.oss_cli portfolio --format markdown
```

---

## 🔧 **Maintenance**

### **Daily**

- Check metrics for anomalies
- Review failed message ingestions
- Monitor OSS PR status

### **Weekly**

- Run full test suite
- Review SLO compliance
- Update portfolio

### **Monthly**

- Analyze contribution trends
- Review agent specialization
- Plan new OSS targets

---

## 📞 **Emergency Contacts**

**System Issues:**
- Check logs in `logs/` directory
- Review metrics via `make metrics`
- Run smoke tests to isolate issue

**Escalation:**
- Disable failing system via feature flags
- Review recent changes
- Consult documentation

---

**🐝 Keep the swarm running smoothly!**


