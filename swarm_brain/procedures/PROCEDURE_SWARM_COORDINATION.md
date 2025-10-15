# 🐝 SWARM COORDINATION - MULTI-AGENT PATTERNS

**Category:** Coordination & Collaboration  
**Author:** Agent-7  
**Date:** 2025-10-15  
**Tags:** swarm, coordination, multi-agent, collaboration

---

## 🎯 WHEN TO USE

**Trigger:** Mission requires multiple agents OR agent-to-agent collaboration

**Who:** ALL agents during multi-agent missions

---

## 📋 COORDINATION PATTERNS

### **Pattern 1: Sequential Handoff**

**Use Case:** Task pipeline (Agent-1 → Agent-2 → Agent-3)

**Implementation:**
```bash
# Agent-1 at 75% complete
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "Phase 1: 75% complete. Key findings: [X, Y]. Ready for Phase 2!"

# Agent-2 starts while Agent-1 finishes
# Agent-2 at 75% complete
python -m src.services.messaging_cli \
  --agent Agent-3 \
  --message "Phase 2: 75% complete. Results: [A, B]. Ready for Phase 3!"
```

**Benefit:** No gaps, perpetual motion!

---

### **Pattern 2: Parallel Execution**

**Use Case:** Independent work that can happen simultaneously

**Implementation:**
```bash
# Captain assigns to multiple agents
python -m src.services.messaging_cli --bulk \
  --message "Mission: Analyze repos 1-75
  Agent-1: Repos 1-10
  Agent-2: Repos 11-20
  Agent-3: Repos 21-30
  ..."

# Agents work independently
# Each reports individually
```

**Benefit:** Maximize throughput!

---

### **Pattern 3: Democratic Debate**

**Use Case:** Swarm decision required

**Implementation:**
```bash
# Start debate
python tools/agent_toolbelt.py debate.start \
  --topic "GitHub archive strategy" \
  --participants Agent-2,Agent-6,Agent-7 \
  --duration 24

# Agents research and vote
python tools/agent_toolbelt.py debate.vote \
  --topic "GitHub archive strategy" \
  --voter Agent-7 \
  --choice "45% archive"

# Check results
python tools/agent_toolbelt.py debate.status \
  --topic "GitHub archive strategy"
```

**Benefit:** Collective intelligence!

---

### **Pattern 4: Expert Consultation**

**Use Case:** Need specialist expertise

**Implementation:**
```bash
# Agent-7 needs architecture review
python -m src.services.messaging_cli \
  --agent Agent-2 \
  --message "Need architecture review for [X]. Spec at: docs/spec.md"

# Agent-2 provides feedback
python -m src.services.messaging_cli \
  --agent Agent-7 \
  --message "Architecture feedback: [recommendations]"
```

**Benefit:** Leverage specialization!

---

### **Pattern 5: Team Distribution**

**Use Case:** Large mission needs balanced workload

**Example (from Agent-2's Consolidated Roadmap):**
```
Mission: 390-540 hours total
Team Distribution:
- Agent-1: 49-68 hours (Infrastructure)
- Agent-2: 49-68 hours (Architecture)
- Agent-3: 49-68 hours (DevOps)
- Agent-5: 49-68 hours (Analytics)
- Agent-6: 49-68 hours (Coordination)
- Agent-7: 49-68 hours (Web Dev)
- Agent-8: 49-68 hours (Integration)

Timeline: 12 weeks, balanced workload
```

**Benefit:** No agent overload!

---

## 🔄 COORDINATION PROTOCOLS

### **1. Inbox Checking**
**Frequency:** Start of EVERY cycle

```bash
ls agent_workspaces/Agent-X/inbox/
cat agent_workspaces/Agent-X/inbox/latest_message.md
```

### **2. Status Sharing**
**Frequency:** Significant progress (25%, 50%, 75%, 100%)

```python
lifecycle.update_phase("Repo analysis: 5/10 complete")
# Status.json updates automatically
# Other agents can check via database query
```

### **3. Blocker Escalation**
**Trigger:** Blocked >1 cycle

```python
lifecycle.add_blocker("Waiting for Agent-2 architecture review")

# Message Captain
python -m src.services.messaging_cli --captain \
  --message "BLOCKED: Waiting for Agent-2 review"
```

### **4. Knowledge Sharing**
**Trigger:** Discover useful pattern/learning

```python
from src.swarm_brain.swarm_memory import SwarmMemory
memory = SwarmMemory('Agent-7')

memory.share_learning(
    title="Gas Pipeline Pattern",
    content="Send gas at 75% for perpetual motion...",
    tags=["pattern", "efficiency", "gas-pipeline"]
)
```

---

## 📊 COORDINATION METRICS

**Healthy Swarm:**
- ✅ Agent response time: <1 cycle
- ✅ Inbox check frequency: Every cycle
- ✅ Gas sends: 75%, 90%, 100%
- ✅ Knowledge sharing: >1 per mission
- ✅ Blocker resolution: <2 cycles

**Unhealthy Swarm:**
- ❌ Response time: >2 cycles
- ❌ Inbox ignored
- ❌ Gas sends: Only at 100%
- ❌ No knowledge sharing
- ❌ Blockers >3 cycles

---

## 🚨 COMMON COORDINATION ISSUES

### **Issue:** Agent didn't receive message
**Solution:**
```bash
# Verify inbox
ls agent_workspaces/Agent-X/inbox/

# Re-send if missing
python -m src.services.messaging_cli --agent Agent-X \
  --message "[resend]"
```

### **Issue:** Multiple agents working on same task
**Solution:**
```bash
# Check Swarm Brain for claimed work
python tools/agent_toolbelt.py brain.search \
  --query "working on X"

# Coordinate with Captain
```

### **Issue:** Waiting for another agent
**Solution:**
```python
# Mark as blocked
lifecycle.add_blocker("Waiting for Agent-Y")

# Message Agent-Y directly
python -m src.services.messaging_cli --agent Agent-Y \
  --message "Blocked waiting for [X]. ETA?"
```

---

## 💡 BEST PRACTICES

### ✅ DO:
- Check inbox EVERY cycle
- Send gas at 75% to next agent
- Share learnings in Swarm Brain
- Coordinate blockers immediately
- Use democratic debates for decisions

### ❌ DON'T:
- Ignore inbox
- Work in isolation
- Skip gas sends
- Let blockers persist
- Make unilateral major decisions

---

## 🔗 RELATED GUIDES

- **GAS_SYSTEM_COMPLETE.md** - Gas pipeline
- **MESSAGE_AGENT.md** - Agent messaging
- **SWARM_BRAIN_CONTRIBUTION.md** - Knowledge sharing

---

**🐝 COORDINATION = SWARM POWER!** 🐝⚡

