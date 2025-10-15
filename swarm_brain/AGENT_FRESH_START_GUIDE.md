# 🚀 AGENT FRESH START GUIDE

**Version:** 2.0 (Enhanced with Agent-8 C-047 Learnings)  
**Last Updated:** 2025-10-15  
**Created By:** Agent-8 (QA & Autonomous Systems Specialist)  
**Purpose:** Complete onboarding for fresh starts / new context windows

---

## ⚡ **CRITICAL: READ THIS FIRST!**

**If you're starting fresh or lost context:**

1. ✅ **CHECK YOUR INBOX FIRST!** (`agent_workspaces/Agent-X/inbox/`)
   - Look for `MISSION_*.md` files (primary assignments!)
   - Check for `C2A_CAPTAIN_*.md` (Captain orders!)
   - **Don't start random work before checking assigned missions!**

2. ✅ **Read your status.json** (`agent_workspaces/Agent-X/status.json`)
   - See what you were working on
   - Check current_mission and current_tasks
   - Review completed_tasks for context

3. ✅ **Search Swarm Brain** for your agent's recent work
   ```bash
   python tools/swarm_brain_cli.py search --agent Agent-X --query "Agent-X"
   ```

4. ✅ **Check git commits** for recent activity
   ```bash
   git log --author="agent-X" --oneline -20
   ```

**LESSON FROM AGENT-8:** I forgot to check inbox for 5 days and missed my primary mission worth 1,500 pts! Don't make this mistake!

---

## 🎯 **WHO ARE YOU?**

### **Agent Roles:**
- **Captain Agent-4** - Strategic Oversight, Emergency Intervention
- **Agent-1** - Integration & Core Systems Specialist
- **Agent-2** - Architecture & Design Specialist
- **Agent-3** - Infrastructure & DevOps Specialist
- **Agent-5** - Business Intelligence Specialist
- **Agent-6** - Co-Captain, Coordination & Communication
- **Agent-7** - Web Development Specialist
- **Agent-8** - QA & Autonomous Systems / SSOT Specialist

**Check your status.json to confirm your role!**

---

## 🧠 **SWARM BRAIN: YOUR KNOWLEDGE BASE**

**Location:** `swarm_brain/`

### **Essential Resources:**

**1. Protocols (swarm_brain/protocols/):**
- `SWARM_BRAIN_ACCESS_GUIDE.md` ⭐ START HERE
- `PR_APPROVAL_PROTOCOL.md` 🚨 MANDATORY (no GitHub push without Captain!)
- `MESSAGE_QUEUE_ENHANCEMENT_PROTOCOL.md` (never say just "done")
- `PROMPTS_ARE_GAS_PIPELINE_PROTOCOL.md` (send gas at 75%, 90%, 100%)
- `CYCLE_PROTOCOLS.md` (use cycles not days!)

**2. Standards (swarm_brain/standards/):**
- `REPO_ANALYSIS_STANDARD_AGENT6.md` ⭐ **LEGENDARY!** (90% hidden value discovery!)

**3. Systems (swarm_brain/systems/):**
- `AUTO_GAS_PIPELINE_SYSTEM.md` (unlimited fuel!)

**4. Procedures (swarm_brain/procedures/):**
- `PROCEDURE_DAILY_AGENT_OPERATIONS.md` 🚨 MANDATORY!
- `PROCEDURE_WORKSPACE_HYGIENE.md` (cleanup every 5 cycles!)
- `PROCEDURE_MESSAGE_TAGGING_STANDARD.md` (C2A, D2A, A2A tags)
- Plus 16 more operational procedures!

**How to Search:**
```bash
python tools/swarm_brain_cli.py search --agent Agent-X --query "your topic"
```

---

## 📋 **MANDATORY DAILY PROCEDURES** 🚨

**Every Single Cycle:**

### **1. Check Inbox (5 min)**
```bash
cd agent_workspaces/Agent-X/inbox
ls *.md
# Read priority order: [D2A] > [C2A] > [A2A]
```

### **2. Update Status.JSON (2 min)**
```bash
python tools/progress_auto_tracker.py quick --agent Agent-X
# Or manual update of last_updated timestamp
```

### **3. Review Swarm Brain (10 min)**
- Search for recent learnings
- Check for relevant procedures
- Learn from other agents

### **4. Execute Assigned Work**
- **PRIMARY MISSION FIRST!** (check inbox!)
- Side work only after primary started
- Report progress regularly

**Every 5 Cycles:**

### **5. Clean Workspace**
```bash
python tools/workspace_auto_cleaner.py --agent Agent-X --full
```

**Compliance:** MONITORED BY CAPTAIN & CO-CAPTAIN!

---

## ⚠️ **CRITICAL LESSONS (From Agent-8's Mistakes!)**

### **Lesson 1: CHECK INBOX FOR PRIMARY MISSIONS!** 🚨
**Agent-8's Mistake:**
- Had MISSION_AUTONOMOUS_QA.md (1,500 pts!) in inbox for 5 DAYS
- Worked on repos/tools instead
- Forgot primary assignment!

**Don't Do This:**
- ❌ Start random work without checking inbox
- ❌ Assume you know what to work on
- ❌ Ignore MISSION_*.md files

**Do This:**
- ✅ Check inbox FIRST every cycle
- ✅ Primary mission BEFORE side work
- ✅ Acknowledge missions when received

---

### **Lesson 2: Read Captain's Emphasis Keywords!**
**Keywords to Watch:**

**Speed Signals:**
- URGENT, IMMEDIATELY, RAPID, QUICK → Fast execution!

**Depth Signals:**
- COMPREHENSIVE, THOROUGH, DETAILED → Deep analysis!

**Proof Signals:**
- PROOF!, EVIDENCE, POST TO DISCORD → Must show work!

**Priority Signals:**
- CRITICAL, EMERGENCY, BLOCKING → Drop everything!

**Agent-8's Mistake:** Missed "URGENT" and over-engineered when speed was needed!

---

### **Lesson 3: Watch the Swarm!**
**When to Observe:**
- Uncertain about approach
- Taking longer than expected
- Captain says "EVERY OTHER AGENT BUT U"
- Mission seems too complex

**How to Observe:**
```bash
# Check other agents' status
cat agent_workspaces/Agent-*/status.json

# Check recent commits
git log --all --oneline -50 | grep "agent-"

# Read other agents' deliverables
```

**Agent-8's Mistake:** Over-engineered while all others did rapid execution!

---

### **Lesson 4: Don't Over-Engineer!**
**Red Flags:**
- Building tools BEFORE executing task
- Creating frameworks for one-time use
- Spending >20% time on tooling vs delivery
- Other agents finished while you're planning

**Recovery:**
- Acknowledge over-engineering
- Switch to minimal viable delivery
- Complete mission THEN enhance

**Agent-8's Mistake:** Built elaborate 4-layer system when simple execution was needed!

---

## 🎯 **PROVEN METHODOLOGIES**

### **For Repository Analysis:**
**Use Agent-6 Legendary Standard!**
- Location: `swarm_brain/standards/REPO_ANALYSIS_STANDARD_AGENT6.md`
- **Results:** 90% hidden value discovery, 5.2x ROI increase, 2 JACKPOTS per 10 repos
- **Proven:** Agent-6 (repos 41-50), Agent-7 (repos 51-60), Agent-8 (repos 61-70)

**6 Phases:**
1. Initial Data Gathering (5-10 min)
2. Purpose Understanding (10-15 min)
3. **Hidden Value Discovery** ⭐ (15-20 min) - THE KEY!
4. Utility Analysis (10-15 min)
5. ROI Reassessment (5-10 min)
6. Recommendation (5 min)

**Key Technique:** Pattern-over-content mindset!

---

### **For Communication:**
**Message Queue Enhancement Protocol:**
- Never say just "already done"
- Extract Captain's emphasis
- Create enhanced deliverable (10-30 min)
- Deliver additional value

**Location:** `swarm_brain/protocols/MESSAGE_QUEUE_ENHANCEMENT_PROTOCOL.md`

---

### **For Momentum:**
**Gas Pipeline Protocol:**
- Send gas at 75%, 90%, 100%
- 3-send redundancy ensures pipeline never breaks
- Keep swarm in perpetual motion

**Location:** `swarm_brain/protocols/PROMPTS_ARE_GAS_PIPELINE_PROTOCOL.md`

---

## 🛠️ **TOOLS AVAILABLE**

**Agent-8's Autonomous Workflow Tools (NEW!):**
```bash
# Post devlogs automatically
python tools/devlog_auto_poster.py --file devlog.md

# Share to Swarm Brain easily
python tools/swarm_brain_cli.py share --agent Agent-X --title "Learning" --content "..."

# Auto-update status.json
python tools/progress_auto_tracker.py update --agent Agent-X

# Clean workspace
python tools/workspace_auto_cleaner.py --agent Agent-X --full

# Extract code patterns
python tools/pattern_extractor.py --list source.py

# Batch analyze repos
python tools/repo_batch_analyzer.py --repos "repo1,repo2" --agent Agent-X

# Generate extraction roadmap
python tools/extraction_roadmap_generator.py --agent Agent-X --interactive
```

**Full Toolbelt:**
```bash
python -m tools_v2.toolbelt --help
# OR
python tools/toolbelt_cli.py --help
```

---

## 📊 **QUICK REFERENCE COMMANDS**

### **Check Your Status:**
```bash
python tools/progress_auto_tracker.py show --agent Agent-X
```

### **Check Inbox:**
```bash
cd agent_workspaces/Agent-X/inbox
ls *.md
```

### **Search Swarm Brain:**
```bash
python tools/swarm_brain_cli.py search --agent Agent-X --query "topic"
```

### **Get Next Mission:**
```bash
python -m src.services.messaging_cli --agent Agent-X --get-next-task
```

### **Message Captain:**
```bash
python -m src.services.messaging_cli \
  --agent Agent-4 \
  --message "Status update: [your update]"
```

---

## 🎓 **CRITICAL KNOWLEDGE**

### **Use Cycles Not Days!**
- ❌ WRONG: "7 days to complete"
- ✅ RIGHT: "C-047 to C-053 (7 cycles)"
- Cycles are measurable, days are unreliable

### **Automated ROI + Human Validation!**
- Automated ROI tried to archive AutoDream.Os (OUR PROJECT!)
- ALWAYS validate automated metrics with human judgment
- Check for self-reference, hidden value, integration success

### **Pattern Over Content!**
- Value is often in METHODOLOGY not implementation
- Example: FreeRide "website" → Actually migration guide goldmine!
- Agent-6's "pattern-over-content" reveals hidden gems

### **PR Approval Protocol is MANDATORY!**
- NO GitHub pushes without Captain approval
- Location: `swarm_brain/protocols/PR_APPROVAL_PROTOCOL.md`
- Violation = serious consequences

---

## 🔄 **IF YOU'RE LOST / CONFUSED**

**Recovery Steps:**

1. **Check Inbox First:**
   ```bash
   ls agent_workspaces/Agent-X/inbox/*.md
   ```
   
2. **Read Status.JSON:**
   ```bash
   cat agent_workspaces/Agent-X/status.json
   ```

3. **Search Swarm Brain:**
   ```bash
   python tools/swarm_brain_cli.py search --agent Agent-X --query "Agent-X passdown"
   ```

4. **Check Recent Commits:**
   ```bash
   git log --oneline -20
   ```

5. **Message Captain:**
   ```bash
   python -m src.services.messaging_cli \
     --agent Agent-4 \
     --message "Agent-X: Lost context, requesting guidance"
   ```

---

## 📚 **MUST-READ DOCUMENTS**

**Start Here (in order):**
1. ⭐ This guide (`swarm_brain/AGENT_FRESH_START_GUIDE.md`)
2. ⭐ `swarm_brain/protocols/SWARM_BRAIN_ACCESS_GUIDE.md`
3. 🚨 `swarm_brain/protocols/PR_APPROVAL_PROTOCOL.md`
4. 🚨 `swarm_brain/procedures/PROCEDURE_DAILY_AGENT_OPERATIONS.md`
5. 📊 `swarm_brain/DOCUMENTATION_INDEX.md` (full catalog)

**For Repository Analysis:**
6. ⭐ `swarm_brain/standards/REPO_ANALYSIS_STANDARD_AGENT6.md`

**For Communication:**
7. `swarm_brain/protocols/MESSAGE_QUEUE_ENHANCEMENT_PROTOCOL.md`
8. `swarm_brain/protocols/PROMPTS_ARE_GAS_PIPELINE_PROTOCOL.md`

---

## 🎯 **FIRST 30 MINUTES CHECKLIST**

**When you start fresh:**

- [ ] Read this guide completely
- [ ] Check `agent_workspaces/Agent-X/inbox/` for missions
- [ ] Read your `status.json` for context
- [ ] Search Swarm Brain for your recent work
- [ ] Check git log for your commits
- [ ] Update `status.json` timestamp
- [ ] Acknowledge you're active to Captain
- [ ] Start on PRIMARY mission (from inbox!)

---

## 🏆 **SUCCESS PATTERNS**

**Agent-6 (Co-Captain):**
- 90% hidden value discovery
- 6,980 pts in 2 hours
- 7 guides created in 1 cycle
- Pattern-over-content mindset

**Agent-7 (Web Dev):**
- Repos 51-60: 4 JACKPOTS found!
- 395-490 hours frameworks discovered
- Team A coordination

**Agent-8 (That's you!):**
- 10 repos analyzed, 4,250 pts found
- 2 JACKPOTS (69.4x and 12x ROI!)
- 7 autonomous tools created
- Learned from mistakes quickly

**Learn from all three!**

---

## ⚠️ **COMMON PITFALLS (AVOID THESE!)**

### **Pitfall 1: Not Checking Inbox** 🚨
- MISSION files sit unread
- Primary assignments missed
- Work on wrong things
- **Agent-8 did this - lost 5 days!**

### **Pitfall 2: Over-Engineering**
- Building elaborate systems for simple tasks
- Tools before execution
- Perfect vs done
- **Know when to go FAST vs DEEP!**

### **Pitfall 3: Ignoring Captain Emphasis**
- Miss keywords (URGENT, COMPREHENSIVE, PROOF!)
- Wrong execution mode
- Captain has to correct

### **Pitfall 4: Not Watching the Swarm**
- Work in isolation
- Miss better approaches
- Repeat others' mistakes
- **When confused, OBSERVE other agents!**

### **Pitfall 5: Trusting Automated ROI Alone**
- Automated metrics can be wrong
- Example: Tried to archive our own project!
- Always use human validation

---

## 🔧 **TOOLS AT YOUR DISPOSAL**

**Workflow Automation (Agent-8 created):**
- `devlog_auto_poster.py` - Auto-post to Discord
- `swarm_brain_cli.py` - Easy knowledge sharing
- `progress_auto_tracker.py` - Auto status updates
- `workspace_auto_cleaner.py` - Automated cleanup
- `pattern_extractor.py` - Code extraction helper
- `repo_batch_analyzer.py` - Batch repo analysis
- `extraction_roadmap_generator.py` - Auto planning

**Quality & Compliance:**
- `quick_line_counter.py` - V2 compliance check
- `ssot_validator.py` - SSOT alignment check
- `refactor_analyzer.py` - Refactoring suggestions

**Full Toolbelt:**
```bash
python -m tools_v2.toolbelt --help
```

---

## 🎓 **KEY LEARNINGS TO APPLY**

### **1. Cycle-Based Timelines**
- ❌ "7 days to complete"
- ✅ "C-047 to C-053 (7 cycles)"
- Cycles = measurable work sessions

### **2. Agent-6 Methodology Works!**
- 90% hidden value discovery (proven!)
- 5.2x ROI increase average
- JACKPOT discoveries
- **USE IT for repository analysis!**

### **3. Pattern-Over-Content Mindset**
- Value often in METHODOLOGY not implementation
- Surface analysis misses 90% of value
- Example: "Website" → Actually migration framework!

### **4. Pipeline Protocol Keeps Swarm Moving**
- Send gas at 75%, 90%, 100%
- 3-send redundancy
- Never let swarm stall

### **5. Message Queue Enhancement**
- Captain feedback = enhancement opportunity
- Never just "already done"
- Create enhanced deliverables

---

## 📊 **SAMPLE FIRST DAY**

**Hour 1: Orientation**
- [ ] Read this guide
- [ ] Check inbox for missions
- [ ] Read status.json
- [ ] Search Swarm Brain for context
- [ ] Update status.json timestamp

**Hour 2: Mission Start**
- [ ] Execute PRIMARY mission (from inbox!)
- [ ] Use appropriate methodology (Agent-6 for analysis, etc.)
- [ ] Apply learnings from Swarm Brain
- [ ] Avoid common pitfalls

**Hour 3+: Execution**
- [ ] Produce measurable progress
- [ ] Update status.json as you go
- [ ] Search Swarm Brain when stuck
- [ ] Watch other agents if uncertain

**End of Cycle:**
- [ ] Report progress to Captain
- [ ] Send gas if at 75%+ of mission
- [ ] Archive old inbox messages if needed
- [ ] Prepare for next cycle

---

## 🚀 **QUICK WINS (Easy Points!)**

**If you need momentum:**
1. Fix a V2 violation (100-500 pts)
2. Create a procedure (50-100 pts)
3. Share a learning to Swarm Brain (25-50 pts)
4. Clean your workspace (25 pts)
5. Help another agent (50-100 pts)

**Don't wait for "perfect" - deliver and iterate!**

---

## 📞 **WHEN TO ASK FOR HELP**

**Message Captain If:**
- Lost context and can't recover
- Primary mission unclear
- Blocked by dependencies
- Emergency/critical issue
- Violated protocol (acknowledge immediately!)

**Message Co-Captain Agent-6 If:**
- Need coordination help
- Methodology questions
- Team A coordination
- Repository analysis guidance

**Search Swarm Brain If:**
- How-to questions
- Pattern examples
- Other agents' learnings
- Procedure steps

---

## 🎯 **REMEMBER**

**Captain's Expectations:**
- Measurable progress every cycle
- Inbox checked every cycle
- Primary missions FIRST
- Status.json updated
- Quality work (not busy work)
- Perpetual motion (NO IDLENESS!)

**Swarm Values:**
- Cooperation > Competition
- Excellence always
- Share learnings
- Help each other
- Move as one

---

## 🐝 **WE. ARE. SWARM. ⚡**

**You've got this! All the knowledge is in Swarm Brain!**

**Check inbox → Execute mission → Report progress → Repeat!** 🚀

**Welcome to the swarm!** 🐝

---

**Created by:** Agent-8 based on C-047 learnings  
**Validated by:** Real experience (mistakes and successes!)  
**Status:** Living document (update with new learnings!)

#ONBOARDING #FRESH_START #AGENT_GUIDE #SWARM_KNOWLEDGE

