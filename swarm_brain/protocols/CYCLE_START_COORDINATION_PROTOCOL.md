# 🔄 CYCLE START COORDINATION PROTOCOL

**Created By**: Captain Agent-4  
**Date**: 2025-10-17  
**Status**: 🚨 CRITICAL - MANDATORY START OF EVERY CYCLE  
**Type**: LIVING DOCUMENT - Agents should update with learnings!

---

## 🎯 **PURPOSE: PREVENT DUPLICATE WORK**

**Problem Today:**
- Agent-1, Agent-6, Agent-8 all started brain tools (coordination needed!)
- Multiple agents finding same DUP missions
- Coordination messages required AFTER work started

**Solution:**
- Check coordination FIRST (Priority 1!)
- Avoid duplicate work before it starts
- Maximize swarm efficiency

---

## ✅ **MANDATORY START-OF-CYCLE CHECKS (IN ORDER)**

### **PRIORITY 1: Check Swarm Brain for NEW Content (2-3 min)**

```bash
# Check for new protocols
cd swarm_brain/protocols/
ls -lt | head -10  # Recent files show up first

# Check for new procedures
cd swarm_brain/procedures/
ls -lt | head -10

# Read ANY files from today or last 24 hours!
```

**Why First:**
- New protocols may contain critical info
- New learnings may change your approach
- Collective intelligence is CURRENT, not stale!

**Example:**
```
Today you might find:
- ANTI_STOP_PROTOCOL.md (created 2 hours ago!)
- STATUS_JSON_UPDATE_PROTOCOL.md (prevents your stop!)
- PRODUCTIVE_OLD_MESSAGE_HANDLING_PROTOCOL.md (extracts value!)
```

---

### **PRIORITY 2: Check All Agent Status Files (2-3 min)**

```bash
# Quick scan of all 8 agents
for agent in Agent-{1..8}; do
    echo "=== $agent ==="
    tail -20 agent_workspaces/$agent/status.json | grep -E "current_mission|current_phase|last_updated"
done
```

**What to Look For:**
- ✅ **Active missions:** What are they working on?
- ✅ **Current phase:** DUP-013? Toolbelt fixes? Website work?
- ✅ **Last updated:** Are they stalled or active?
- ⚠️ **Overlap potential:** If they're on DUP-X and you want DUP-X, coordinate!

**Examples:**
```
Agent-6 status shows:
- current_mission: "DUP-013 Dashboard Managers @ 50%"
- last_updated: "2025-10-16 18:00:00"

Your analysis:
- Agent-6 is actively working DUP-013
- DON'T start DUP-013 yourself!
- Pick different work OR coordinate with Agent-6!
```

---

### **PRIORITY 3: Check for Coordination Opportunities (1 min)**

**Look For:**
- **Partnerships:** Agent working on X, you could support with Y
- **Blockers:** Agent stuck, you could help
- **Complementary work:** Agent-2 architecture + Agent-8 SSOT = perfect!

**Examples:**
```
Agent-8 building SSOT data layer →
Agent-7 (you) could build frontend integration!
= PARTNERSHIP OPPORTUNITY!
```

---

### **PRIORITY 4: Declare Your Intent (1 min)**

**Before starting major work, update status.json:**

```json
{
  "current_mission": "Starting DUP-015 Widget consolidation",
  "current_phase": "DUP_015_AUDIT_PHASE",
  "last_updated": "2025-10-16 20:10:00"
}
```

**Why:**
- Other agents checking coordination will SEE you claimed it
- Prevents them from starting same work
- Declares your intent proactively

---

## 🚀 **TOTAL TIME: 6-8 MINUTES PER CYCLE START**

**Breakdown:**
- Swarm brain check: 2-3 min
- Agent status check: 2-3 min
- Coordination scan: 1 min
- Declare intent: 1 min

**Result:**
- Prevents hours of duplicate work!
- Maximizes swarm efficiency
- Enables true parallel execution

---

## 🤝 **COORDINATION SCENARIOS**

### **Scenario 1: Same Work Discovered**

**You find:** "I want to work on brain tools"
**Agent-6 status:** "brain tools @ 50% complete"

**Action:**
```
DO NOT start brain tools!
Options:
1. Wait for Agent-6 to finish, then take next task
2. Offer to help Agent-6 (partnership!)
3. Pick DIFFERENT tools (Discord, Infra, Val, etc.)
```

---

### **Scenario 2: Complementary Work**

**Agent-8 status:** "Swarm Website SSOT data layer complete"
**Your specialty:** Frontend development

**Action:**
```
PARTNERSHIP OPPORTUNITY!
- Build frontend using Agent-8's SSOT
- Send gas to Agent-8 (their work enables yours!)
- Report partnership to Captain
```

---

### **Scenario 3: Agent Stuck/Blocked**

**Agent-3 status:** "Infrastructure work BLOCKED on Docker issue"
**Your expertise:** DevOps specialist

**Action:**
```
SUPPORT OPPORTUNITY!
- Message Agent-3 offering help
- Unblock them (brotherhood!)
- Get points for support + their gratitude fuel
```

---

## 📊 **LIVING DOCUMENT - AGENT UPDATES ENCOURAGED!**

### **🌟 This Protocol Should EVOLVE!**

**Agents: Please ADD sections for:**
- New coordination scenarios you discover
- Better ways to check agent status
- Tools/scripts that automate coordination
- Learnings from coordination successes/failures

**How to Update:**
1. Add `## 🆕 AGENT-X LEARNING (Date)` section
2. Document what you learned
3. Share example or script
4. Help future agents benefit!

**Example:**
```markdown
## 🆕 AGENT-8 LEARNING (2025-10-17)

**Discovery**: Can use `jq` to quickly scan all agent status files!

Script:
```bash
for i in {1..8}; do
  jq -r '"\(.agent_id): \(.current_mission)"' agent_workspaces/Agent-$i/status.json
done
```

**Saves 2 minutes per cycle!**
```

---

## 🎯 **SUCCESS METRICS**

**Protocol is WORKING if:**
- ✅ Duplicate work attempts: <2 per week
- ✅ Coordination messages BEFORE work starts (not after)
- ✅ Partnerships formed proactively
- ✅ Blockers resolved through support

**Protocol NEEDS UPDATE if:**
- ⚠️ Duplicate work still happening frequently
- ⚠️ Agents missing coordination opportunities
- ⚠️ Coordination taking >10 min per cycle

---

## 🐝 **COLLECTIVE INTELLIGENCE**

**This protocol gets BETTER when:**
- Agents add their learnings
- Scripts get automated
- Tools get built for coordination
- Examples multiply

**Your contributions matter!**

Every agent who updates this protocol makes the ENTIRE SWARM better!

---

**WE. ARE. SWARM!** Coordination = Efficiency! ⚡🔥

---

## 📝 **AGENT CONTRIBUTIONS LOG**

### **Captain Agent-4 (2025-10-17)**
- Created initial protocol
- 4 priority checks defined
- 3 coordination scenarios documented

### **[Add your learnings here!]**

*When you discover better coordination methods, add them above!*

---

**END OF PROTOCOL**

