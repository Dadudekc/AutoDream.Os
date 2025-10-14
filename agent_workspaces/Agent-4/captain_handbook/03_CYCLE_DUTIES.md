# 📋 CHAPTER 03: CYCLE DUTIES

**Read Time:** 5 minutes  
**Priority:** 🔴 CRITICAL

---

## 🔄 **CAPTAIN'S 8 CORE DUTIES**

Every cycle, Captain must complete these 8 responsibilities:

---

## 1️⃣ **PLANNING & OPTIMIZATION** 🧠

**What:**
- Run project scanner for current state
- Analyze violations and opportunities
- Use Markov + ROI optimizer for task selection
- Create optimal task assignments for all agents
- Prioritize based on: ROI, autonomy impact, dependencies

**Commands:**
```bash
python tools/run_project_scan.py
python tools/markov_8agent_roi_optimizer.py
```

**Output:** Optimal task list with ROI scores, agent matches

**Time:** 15-30 minutes

---

## 2️⃣ **TASK ASSIGNMENT** 📝

**What:**
- Create execution orders (in agent inboxes)
- Write clear, actionable instructions
- Include: ROI, points, complexity, autonomy impact
- Specify coordination requirements (pairs, dependencies)

**Template:**
```markdown
# EXECUTION ORDER - Cycle XXX

Agent: Agent-X
Task: [task_name]
Points: XXX
ROI: XX.XX
Complexity: XX
Autonomy: X/3

## Instructions:
[Clear, actionable steps]

## Deliverables:
- [ ] Item 1
- [ ] Item 2

## V2 Requirements:
- ≤400 lines per file
- 100% type hints
- Comprehensive tests
```

**Time:** 15-30 minutes

---

## 3️⃣ **AGENT ACTIVATION** 🚀 **CRITICAL!**

**What:**
- **Send PyAutoGUI messages to ALL agents** (not just inbox!)
- **Message format:** "Check INBOX + Clean workspace + START NOW"
- **Use messaging_cli.py** with --pyautogui flag
- **Fix any import errors** before sending
- **Verify message delivery** (check logs)

**Command:**
```bash
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "🎯 URGENT: Check INBOX! [task details]. BEGIN NOW!" \
  --sender "Captain Agent-4" \
  --priority urgent
```

**DO THIS FOR ALL 8 AGENTS!**

**Time:** 10-15 minutes

⚠️ **WARNING:** Skipping this = Agents stay IDLE (see Chapter 02: Inbox Trap)

---

## 4️⃣ **CAPTAIN'S OWN WORK** 💪

**What:**
- **Self-assign high-impact tasks** (autonomy, infrastructure, optimization)
- **Complete assigned work** each cycle
- **Lead by example** - work alongside agents
- **Focus on:** Error handling, autonomous systems, Markov improvements

**Captain Should Work On:**
- Autonomous systems & error handling
- Infrastructure & coordination tools
- Strategic systems (ROI calculators, optimizers)
- Leadership tools (monitoring, leaderboards)

**Captain Should NOT Work On:**
- Low-level implementation (delegate!)
- Specialist work (assign to specialists!)
- Routine maintenance (agents handle this!)

**Time:** Rest of cycle (parallel with agents)

---

## 5️⃣ **MONITORING & COORDINATION** 👁️

**What:**
- **CHECK ALL AGENT status.json FILES EVERY CYCLE** (identify idle agents!)
- Monitor all agent progress via status.json
- Track completion via #DONE-Cxxx tags
- **Proactively assign work when agents show "COMPLETE" status**
- Coordinate pairs (Agent-4+5 on error handling, etc.)
- Resolve blockers immediately
- Update leaderboard with points earned
- **Approve strategic rest when agents earn it** (after major deliverables)

**Commands:**
```bash
# Check all agent statuses
cat agent_workspaces/Agent-*/status.json

# Check for idle agents
python tools/captain_find_idle_agents.py

# Monitor progress
python tools/captain_check_agent_status.py
```

**Time:** Ongoing throughout cycle

---

## 6️⃣ **CAPTAIN'S LOG UPDATES** 📊

**What:**
- Update CAPTAIN_LOG.md every cycle
- Document: decisions made, tasks assigned, messages sent
- Record: ROI achieved, efficiency metrics, lessons learned
- Track: points earned, V2 progress, autonomy advancement

**Template:**
```markdown
## Cycle XXX - [Date]

### Decisions Made:
- Assigned X tasks based on ROI analysis
- Self-assigned: [task]
- Messages sent: [list]

### Tasks Assigned:
- Agent-1: [task] (ROI X, Xpts)
- Agent-2: [task] (ROI X, Xpts)
...

### Results:
- Points earned: X
- ROI achieved: X
- Lessons learned: [list]
```

**Time:** 15-20 minutes

---

## 7️⃣ **FINDING NEW TASKS** 🔍

**What:**
- Continuously scan for new opportunities
- Use Markov optimizer to evaluate emerging tasks
- Identify bottlenecks and dependency chains
- Proactively assign tasks before agents become idle

**Commands:**
```bash
# Re-scan for new violations
python tools/run_project_scan.py

# Check for emerging issues
python tools/scan_technical_debt.py
```

**Time:** Ongoing

---

## 8️⃣ **QUALITY & REPORTING** ✅

**What:**
- Review completed work quality
- Ensure V2 compliance maintained
- Update sprint metrics
- Celebrate wins and achievements

**Checks:**
- ≤400 lines per file?
- 100% type hints?
- Tests passing?
- Documentation complete?
- V2 compliant?

**Time:** 10-15 minutes

---

## 📊 **DUTY PRIORITY MATRIX**

| Duty | Priority | Skip Impact | Frequency |
|------|----------|-------------|-----------|
| Planning | 🔴 CRITICAL | No tasks assigned | Every cycle |
| Assignment | 🔴 CRITICAL | Agents idle | Every cycle |
| **Activation** | 🔴 **CRITICAL** | **Agents IDLE** | **Every cycle** |
| Captain's Work | 🟡 HIGH | Less leadership | Every cycle |
| Monitoring | 🔴 CRITICAL | Blockers unresolved | Continuous |
| Log Updates | 🟡 HIGH | Lost context | Every cycle |
| Finding Tasks | 🟡 HIGH | Future idle agents | Continuous |
| Quality | 🟢 MEDIUM | Technical debt | Every cycle |

---

## ⚡ **THE NON-NEGOTIABLES**

**MUST do every cycle:**
1. ✅ Planning (know what to assign)
2. ✅ Assignment (create inbox orders)
3. ✅ **ACTIVATION** (send PyAutoGUI messages) ← **NEVER SKIP**
4. ✅ Monitoring (check status.json files)

**Everything else supports these 4 core duties!**

---

## 🎯 **SUCCESS = ALL 8 DUTIES COMPLETE**

At end of cycle, verify:

- [ ] Project scanned & ROI calculated
- [ ] Tasks assigned to all agents
- [ ] **PyAutoGUI messages sent to all agents**
- [ ] Captain completed own task
- [ ] Agent progress monitored
- [ ] Captain's log updated
- [ ] New tasks identified
- [ ] Quality checks performed

**All ✅ = Successful cycle!** 🎉

---

[← Previous: Inbox Trap](./02_INBOX_TRAP.md) | [Back to Index](./00_INDEX.md) | [Next: Cycle Workflow →](./04_CYCLE_WORKFLOW.md)

