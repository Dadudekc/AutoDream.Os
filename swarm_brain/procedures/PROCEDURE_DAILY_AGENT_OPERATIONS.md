# 📋 PROCEDURE: DAILY AGENT OPERATIONS

**Version:** 1.0  
**Created:** 2025-10-15  
**Created By:** Co-Captain Agent-6  
**Source:** General's Directive  
**Status:** 🚨 **MANDATORY FOR ALL AGENTS**  

---

## 🎯 PURPOSE

**Standard operating procedure ALL agents MUST follow every cycle.**

**Mandated by:** General (via Discord broadcast)  
**Enforcement:** Captain & Co-Captain  
**Compliance:** MANDATORY  

---

## ✅ EVERY CYCLE CHECKLIST (MANDATORY!)

### **STEP 1: CHECK INBOX (5 minutes)**

```bash
cd agent_workspaces/Agent-X/inbox
ls *.md  # List unread messages

# Check each message:
#  - [D2A] = General/Discord (HIGHEST PRIORITY!)
#  - [C2A] = Captain (HIGH PRIORITY!)
#  - [A2A] = Agent coordination (NORMAL PRIORITY!)
```

**Actions:**
- [ ] Read all new messages
- [ ] Respond to [D2A] immediately
- [ ] Respond to [C2A] within 1 cycle
- [ ] Respond to [A2A] within 3 cycles

---

### **STEP 2: UPDATE STATUS.JSON (2 minutes)**

```python
# Update these fields EVERY cycle:
{
  "last_updated": "2025-10-15 HH:MM:SS",  # THIS CYCLE!
  "current_mission": "What I'm doing RIGHT NOW",
  "current_tasks": ["Active work this cycle"],
  "completed_tasks": ["Just finished" at top]
}
```

**Compliance Check:**
- [ ] Timestamp is THIS cycle
- [ ] Current mission reflects actual work
- [ ] Completed tasks updated
- [ ] No stale information

---

###  **STEP 3: CLEAN WORKSPACE (10 minutes, every 5 cycles)**

**Every 5 cycles, archive:**

```bash
cd agent_workspaces/Agent-X

# Archive old session summaries
mv *SUMMARY*.md archive/session_summaries/

# Archive old status reports  
mv *READY*.md *STATUS*.md archive/2025-10/

# Archive completed missions
mv C0*_COMPLETE*.md archive/2025-10/

# Clean inbox
cd inbox
mv responded_messages/*.md archive/2025-10/
```

**Target:** <10 files in root directory!

---

### **STEP 4: RESPOND TO MESSAGES (varies)**

**Priority order:**
1. **[D2A] - General/Discord:** Respond immediately (this cycle!)
2. **[C2A] - Captain:** Respond within 1 cycle
3. **[A2A] - Agents:** Respond within 3 cycles

**After responding:**
- Move message to inbox/archive/YYYY-MM/
- Keep inbox clean

---

### **STEP 5: EXECUTE MISSION (main work)**

**Your assigned work!**

**Remember:**
- Send gas at 75-80% (pipeline protocol!)
- Update status.json as you progress
- Log learnings to Swarm Brain
- Maintain quality standards

---

### **STEP 6: END-OF-CYCLE REPORT (5 minutes)**

**Update Captain:**
- Progress this cycle
- Blockers (if any)
- Next cycle plan
- Gas sent to next agent?

---

## 🚨 COMPLIANCE ENFORCEMENT

**Captain/Co-Captain checks EVERY 5 cycles:**

**Green (Compliant):**
- ✅ Inbox <10 unresponded messages
- ✅ Status.json updated this cycle
- ✅ Workspace <10 root files
- ✅ All [D2A] responded to

**Yellow (Warning):**
- ⚠️ Inbox 10-20 messages
- ⚠️ Status.json 1-2 cycles old
- ⚠️ Workspace 10-20 files

**Red (Violation):**
- 🚨 Inbox >20 unresponded
- 🚨 Status.json >3 cycles old
- 🚨 Workspace >50 files
- 🚨 [D2A] messages ignored

---

## 📊 WORKSPACE HEALTH METRICS

**Healthy Agent:**
```
Root directory: 5-7 files
Inbox: 3-5 unresponded messages
Status.json: Updated this cycle
Archives: Organized by month
```

**Unhealthy Agent (Agent-6 BEFORE cleanup):**
```
Root directory: 90+ files! ❌
Inbox: 50+ messages! ❌
Status.json: 1 day old ⚠️
Archives: None (everything in root!) ❌
```

**After cleanup:**
```
Root directory: ~6 files ✅
Inbox: Cleaned ✅
Status.json: Current ✅
Archives: Organized ✅
```

---

## 🛠️ CLEANUP AUTOMATION

**Quick cleanup script:**

```bash
# cleanup_agent_workspace.sh
AGENT_ID=$1
MONTH=$(date +%Y-%m)

cd agent_workspaces/$AGENT_ID

# Create archives
mkdir -p archive/$MONTH
mkdir -p archive/session_summaries
mkdir -p inbox/archive/$MONTH

# Archive old files
mv *SUMMARY*.md archive/session_summaries/ 2>/dev/null
mv *READY*.md *COMPLETE*.md archive/$MONTH/ 2>/dev/null
mv C0*_*.md archive/$MONTH/ 2>/dev/null

# Clean inbox
cd inbox
mv C2A_*.md CAPTAIN_*.md AGENT*_*.md archive/$MONTH/ 2>/dev/null

echo "✅ Workspace cleaned: $AGENT_ID"
```

---

**WE. ARE. SWARM.** 🐝⚡

**Clean workspace = Professional agent!**

---

**#WORKSPACE_HYGIENE #MANDATORY #EVERY_CYCLE #GENERAL_DIRECTIVE**

