# Service Level Objectives (SLOs)

**Reliability targets for Agent Swarm systems**

---

## 📊 **Message-Task Integration**

### **Ingest Success Rate**

- **Target:** ≥ 99%
- **Measurement:** `(msg_task.ingest.ok / (msg_task.ingest.ok + msg_task.ingest.fail)) × 100`
- **Window:** 24 hours
- **Action:** If < 99%, investigate parser failures

### **Deduplication Collision Rate**

- **Target:** ≤ 0.1%
- **Measurement:** `(msg_task.dedupe.duplicate / msg_task.ingest.ok) × 100`
- **Window:** 7 days
- **Action:** If > 0.1%, review fingerprint algorithm

### **Parser Success Rate**

- **Target:** 100%
- **Measurement:** All messages must parse (3-tier cascade)
- **Window:** Always
- **Action:** If any fail all 3 parsers, enhance fallback

---

## 🌍 **OSS Contribution System**

### **Clone Success Rate**

- **Target:** ≥ 95%
- **Measurement:** `(oss.clone.ok / (oss.clone.ok + oss.clone.fail)) × 100`
- **Window:** 7 days
- **Action:** If < 95%, check network/git availability

### **PR Submit Success Rate**

- **Target:** ≥ 97%
- **Measurement:** `(oss.pr.submitted / oss.pr.attempts) × 100`
- **Window:** 30 days
- **Action:** If < 97%, review GitHub CLI/API issues

### **Issue Import Success**

- **Target:** ≥ 98%
- **Measurement:** Successful issue → task conversion rate
- **Window:** 7 days
- **Action:** If < 98%, review GitHub API integration

---

## 📨 **Messaging System**

### **Message Delivery Rate**

- **Target:** 100%
- **Measurement:** All messages must be delivered
- **Window:** Always
- **Action:** If any fail, check lock system

### **Race Condition Rate**

- **Target:** 0%
- **Measurement:** `messaging.race_prevented` should be 0
- **Window:** Always
- **Action:** If > 0, verify lock is working

### **Lock Acquisition Success**

- **Target:** ≥ 99%
- **Measurement:** Lock acquired within timeout
- **Window:** 24 hours
- **Action:** If < 99%, increase timeout or reduce concurrency

---

## 🔴 **Error Handling**

### **Classification Accuracy**

- **Target:** ≥ 95%
- **Measurement:** Correct severity/recoverability classification
- **Window:** Manual review
- **Action:** If < 95%, enhance classifier rules

### **Retry Success Rate**

- **Target:** ≥ 80%
- **Measurement:** Recoverable errors succeed after retry
- **Window:** 7 days
- **Action:** If < 80%, review retry configuration

---

## 🚨 **Alerts**

### **Critical (Immediate Action)**

| Alert | Condition | Response |
|-------|-----------|----------|
| Ingest spike failures | `msg_task.ingest.fail` > 5× baseline in 10min | Disable FF_MSG_TASK, investigate |
| OSS clone failures | `oss.clone.fail` > 5 in 1 hour | Check network, git, permissions |
| Messaging failures | `messaging.failed` > 10 in 5min | Disable FF_CONCURRENT_MSG_LOCK |

### **Warning (Investigation Needed)**

| Alert | Condition | Response |
|-------|-----------|----------|
| High dedupe rate | `msg_task.dedupe.duplicate` > 20% | Review message sources |
| Parser imbalance | Fallback > 80% usage | Improve structured message format |
| Low merge rate | OSS merge rate < 50% | Review contribution quality |

---

## 📈 **Error Budget**

### **Monthly Error Budget**

- **Total Operations:** 10,000 (estimated)
- **Allowed Failures:** 100 (99% SLO)
- **Current Usage:** Track via metrics

**Calculation:**
```
error_budget_remaining = 100 - current_failures
burn_rate = current_failures / days_elapsed
projected_overrun = burn_rate × days_remaining > error_budget_remaining
```

---

## ✅ **Compliance Check**

```bash
# Check all SLOs
python -c "
from src.obs.metrics import get
ingest_ok = get('msg_task.ingest.ok', 0)
ingest_fail = get('msg_task.ingest.fail', 0)
if ingest_ok + ingest_fail > 0:
    rate = (ingest_ok / (ingest_ok + ingest_fail)) * 100
    print(f'Ingest Success: {rate:.2f}% (Target: ≥99%)')
    print('✅ PASS' if rate >= 99 else '❌ FAIL')
"

# View all metrics
make metrics
```

---

**Monitor these SLOs to ensure system reliability!**


