# ⚡ CYCLE PROTOCOLS - MANDATORY EVERY CYCLE

**Last Updated:** 2025-10-15  
**Purpose:** What agents MUST do EVERY cycle (CYCLE-based, NOT time-based!)

---

## 📊 WHAT IS A CYCLE?

**1 CYCLE = 1 Captain prompt + 1 Agent response**

- **NOT** time-based (no "daily", "hourly", etc.)
- **NOT** task-based (multiple tasks can happen in one cycle)
- **IS** interaction-based (each Captain prompt = new cycle)

**Frequency:** Every time Captain interacts with you

---

## ✅ START OF CYCLE (MANDATORY)

### 1. CHECK INBOX
```bash
# Check for messages
ls agent_workspaces/Agent-X/inbox/

# Count messages
ls agent_workspaces/Agent-X/inbox/ | wc -l
```

### 2. UPDATE STATUS.JSON
**Required fields to update:**
- `status`: "ACTIVE"
- `last_updated`: ISO 8601 timestamp
- `cycle_count`: Increment by 1
- `current_phase`: Current work description
- `fsm_state`: "active"

**Quick update:**
```python
from src.core.agent_lifecycle import AgentLifecycle
lifecycle = AgentLifecycle('Agent-X')
lifecycle.start_cycle()  # Automatic!
```

### 3. REVIEW CURRENT MISSION
- Read `current_mission` field
- Check `mission_priority`
- Verify `next_actions`

---

## 🔄 DURING CYCLE (AS NEEDED)

### When to Update Status:
- **Phase change** → Update `current_phase`
- **Task complete** → Add to `completed_tasks`, update points
- **Blocked** → Set status="BLOCKED", add to `blockers` array
- **Tool use** → Update `current_phase`
- **Message sent** → Increment message count

**Quick updates:**
```python
lifecycle.complete_task("Task name", points=100)
lifecycle.update_phase("New phase description")
lifecycle.add_blocker("Waiting for X")
```

---

## ✅ END OF CYCLE (MANDATORY)

### 1. UPDATE STATUS.JSON FINAL STATE
```python
lifecycle.end_cycle(commit=True)  # Auto-saves + commits
```

**What this updates:**
- `last_updated`: Current timestamp
- `completed_tasks`: All tasks done this cycle
- `next_actions`: What's planned for next cycle
- Git commit with status.json

### 2. CREATE DEVLOG (if significant work)
**Only if:** Major feature, bug fix, or milestone
```bash
echo "# Agent-X Cycle N - [Topic]" > devlogs/$(date +%Y%m%d)_agent-x_topic.md
```

---

## 🚨 VIOLATIONS & CONSEQUENCES

### What Happens If You Don't Follow Cycle Protocols:

1. **Captain can't track you** - Won't assign new work
2. **Fuel monitor thinks you're idle** - No GAS delivery
3. **Discord bot shows stale state** - Team sees you as inactive
4. **Integrity validator flags you** - Audit failure
5. **Database out of sync** - Analytics broken
6. **Other agents can't coordinate** - Swarm breaks

### Enforcement:
- Pre-cycle checks alert you of violations
- Post-cycle validation catches missing updates
- Captain monitor reports violations to Captain
- Repeated violations = mission reassignment

---

## 📋 CYCLE CHECKLIST (QUICK REFERENCE)

```
CYCLE START:
[ ] Check inbox
[ ] Update status.json (status=ACTIVE, increment cycle_count)
[ ] Review current mission

DURING CYCLE:
[ ] Update status when phase changes
[ ] Update when tasks complete
[ ] Update if blocked

CYCLE END:
[ ] Update completed_tasks
[ ] Update next_actions
[ ] Commit status.json to git
[ ] Create devlog (if needed)
```

---

## 💡 BEST PRACTICES

### ✅ DO:
- Update status.json EVERY cycle (use AgentLifecycle)
- Use CYCLE-based tracking (not time-based)
- Commit status.json after updates
- Keep next_actions current

### ❌ DON'T:
- Skip status updates ("I'll do it later")
- Use time estimates ("2 hours left")
- Leave status.json unchanged for multiple cycles
- Forget to commit to git

---

## 🔗 RELATED GUIDES

- **STATUS_JSON_GUIDE.md** - Complete status.json reference
- **AGENT_LIFECYCLE_FSM.md** - FSM state management
- **SWARM_BRAIN_ACCESS_GUIDE.md** - How to use Swarm Brain

---

**🐝 UPDATE EVERY CYCLE - CAPTAIN IS WATCHING!** ⚡

