# ✅ CHAPTER 05: DAILY CHECKLIST

**Read Time:** 2 minutes  
**Priority:** 🔴 CRITICAL

---

## 📋 **CAPTAIN'S DAILY CHECKLIST**

Print this out. Check off every cycle. Never skip items.

---

## 🔵 **PHASE 1: PLANNING** (15-30 min)

```
[ ] Run project scanner
    Command: python tools/run_project_scan.py

[ ] Review project_analysis.json output

[ ] Review test_analysis.json output

[ ] Identify V2 violations and opportunities

[ ] Run Markov ROI optimizer
    Command: python tools/markov_8agent_roi_optimizer.py

[ ] Review ROI scores and agent matches

[ ] Confirm autonomy-advancing tasks prioritized

[ ] Create optimal task list for cycle
```

---

## 🔵 **PHASE 2: ASSIGNMENT** (15-30 min)

```
[ ] Write execution order for Agent-1
    Location: agent_workspaces/Agent-1/inbox/EXECUTION_ORDER_CXXX.md

[ ] Write execution order for Agent-2
    Location: agent_workspaces/Agent-2/inbox/EXECUTION_ORDER_CXXX.md

[ ] Write execution order for Agent-3
    Location: agent_workspaces/Agent-3/inbox/EXECUTION_ORDER_CXXX.md

[ ] Write execution order for Agent-5
    Location: agent_workspaces/Agent-5/inbox/EXECUTION_ORDER_CXXX.md

[ ] Write execution order for Agent-6
    Location: agent_workspaces/Agent-6/inbox/EXECUTION_ORDER_CXXX.md

[ ] Write execution order for Agent-7
    Location: agent_workspaces/Agent-7/inbox/EXECUTION_ORDER_CXXX.md

[ ] Write execution order for Agent-8
    Location: agent_workspaces/Agent-8/inbox/EXECUTION_ORDER_CXXX.md

[ ] Self-assign Captain's task (high autonomy impact)

[ ] All orders include: Task, ROI, Points, Complexity, Autonomy, V2 requirements
```

---

## 🔴 **PHASE 3: ACTIVATION** (10-15 min) **CRITICAL!**

```
[ ] Verify messaging_cli.py works
    Command: python -m src.services.messaging_cli --list-agents

[ ] Fix imports if needed (see Chapter 06)

[ ] Send PyAutoGUI message to Agent-1
    Command: python -m src.services.messaging_cli --agent Agent-1 --message "..." --sender "Captain Agent-4" --priority urgent

[ ] Send PyAutoGUI message to Agent-2

[ ] Send PyAutoGUI message to Agent-3

[ ] Send PyAutoGUI message to Agent-5

[ ] Send PyAutoGUI message to Agent-6

[ ] Send PyAutoGUI message to Agent-7

[ ] Send PyAutoGUI message to Agent-8

[ ] Verify all messages delivered (check logs)
    Look for: "Message sent to Agent-X at (x, y)"

[ ] Confirm "WE. ARE. SWARM." appears in logs
```

⚠️ **WARNING:** Skipping Phase 3 = All agents stay IDLE!

---

## 🔵 **PHASE 4: EXECUTION** (Rest of Cycle)

```
[ ] Start Captain's assigned task

[ ] Make measurable progress (50%+ completion target)

[ ] Document work in Captain's task tracker
```

---

## 🔵 **PHASE 5: MONITORING** (Continuous)

```
[ ] Check Agent-1 status.json
    Command: cat agent_workspaces/Agent-1/status.json

[ ] Check Agent-2 status.json

[ ] Check Agent-3 status.json

[ ] Check Agent-5 status.json

[ ] Check Agent-6 status.json

[ ] Check Agent-7 status.json

[ ] Check Agent-8 status.json

[ ] Look for #DONE-Cxxx tags in completed work

[ ] Resolve any blockers immediately

[ ] Coordinate pair programming if needed

[ ] Respond to agent questions/messages
```

---

## 🔵 **PHASE 6: DOCUMENTATION** (15-20 min)

```
[ ] Update Captain's log with cycle summary
    Location: prompts/captain/captain_log_YYYY-MM-DD.md

[ ] Document decisions made

[ ] Document tasks assigned (all 8 agents)

[ ] Document messages sent

[ ] Record points earned

[ ] Record ROI achieved

[ ] Record lessons learned

[ ] Update leaderboard
    Command: python tools/captain_leaderboard_update.py

[ ] Track V2 compliance progress

[ ] Track autonomy advancement metrics
```

---

## 🔵 **PHASE 7: DISCOVERY** (Ongoing)

```
[ ] Scan for new tasks/opportunities

[ ] Identify emerging violations

[ ] Look for dependency chain unlocks

[ ] Evaluate new tasks with Markov optimizer

[ ] Plan next cycle assignments

[ ] Optimize workflow based on lessons learned
```

---

## 🎯 **END-OF-CYCLE VERIFICATION**

Before closing cycle, verify:

```
CRITICAL ITEMS:
[ ] All 7 agents received inbox orders
[ ] All 7 agents received PyAutoGUI activation messages
[ ] Captain completed own task
[ ] Captain's log updated
[ ] All agent statuses checked

SUCCESS INDICATORS:
[ ] 8/8 agents activated (100%)
[ ] Points earned tracked
[ ] ROI achieved calculated
[ ] V2 compliance maintained
[ ] No critical blockers unresolved
[ ] Next cycle tasks identified
```

---

## 🚨 **RED FLAGS** (If Any Checked, Fix NOW!)

```
[ ] Any agent didn't receive activation message
[ ] Messaging system broken/not working
[ ] Captain didn't complete own task
[ ] Captain's log not updated
[ ] Agent statuses not checked
[ ] Critical blocker unresolved
[ ] Next cycle tasks unknown
```

**If ANY red flags checked → Fix before ending cycle!**

---

## ⏱️ **TIME BUDGET**

**Total Cycle Time:** ~6-8 hours

| Phase | Time | % of Cycle |
|-------|------|------------|
| Planning | 15-30 min | 5-10% |
| Assignment | 15-30 min | 5-10% |
| **Activation** | **10-15 min** | **5%** |
| Execution | 4-5 hours | 60-70% |
| Monitoring | Continuous | Throughout |
| Documentation | 15-20 min | 5% |
| Discovery | Ongoing | Throughout |

**Most time = Execution (actual work alongside agents)**

---

## 🏆 **PERFECT CYCLE = ALL BOXES CHECKED**

Print this checklist. Keep it visible. Check every box, every cycle.

**100% completion = Successful cycle!** ✅

---

[← Previous: Cycle Workflow](./04_CYCLE_WORKFLOW.md) | [Back to Index](./00_INDEX.md) | [Next: Messaging System →](./06_MESSAGING_SYSTEM.md)

