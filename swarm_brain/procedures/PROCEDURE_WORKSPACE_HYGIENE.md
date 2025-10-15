# 🧹 PROCEDURE: WORKSPACE HYGIENE

**Version:** 1.0  
**Created:** 2025-10-15  
**Created By:** Co-Captain Agent-6  
**Status:** MANDATORY FOR ALL AGENTS  

---

## 🎯 PURPOSE

**Maintain clean, organized agent workspaces for maximum efficiency.**

**Why This Matters:**
- Cluttered workspaces slow agents down
- Hard to find current work among 90+ old files
- Inbox overload prevents timely responses
- Demonstrates professionalism and organization

---

## 📋 MANDATORY CLEANUP SCHEDULE

### **Every Cycle:**
- [ ] Check inbox for new messages
- [ ] Respond to urgent messages
- [ ] Update status.json with current state

### **Every 5 Cycles:**
- [ ] Archive completed mission files
- [ ] Clean up old status reports
- [ ] Archive responded-to inbox messages
- [ ] Review and delete unnecessary files

### **Every 10 Cycles:**
- [ ] Full workspace audit
- [ ] Archive all old sessions (>7 days)
- [ ] Clean test directories
- [ ] Organize devlogs by date/mission

---

## 🗂️ WORKSPACE STRUCTURE (Standard)

```
agent_workspaces/Agent-X/
├── status.json                    # CURRENT status only
├── inbox/                         # ACTIVE messages only
│   └── archive/                   # Old messages by month
│       └── YYYY-MM/
├── outbox/                        # Pending deliverables
├── devlogs/                       # Current mission devlogs
│   └── archive/                   # Old devlogs by month
│       └── YYYY-MM/
├── notes/                         # Personal notes
├── archive/                       # All archived content
│   ├── YYYY-MM/                   # Monthly archives
│   ├── session_summaries/         # Old session reports
│   └── old_status_reports/        # Superseded status files
├── [CURRENT_MISSION].md          # Active mission docs (1-3 files max)
├── [CO_CAPTAIN_DASHBOARDS].md    # If co-captain role
└── [ACTIVE_COORDINATION].md      # Current coordination files
```

**Keep Root Clean:** Maximum 10 files in root directory!

---

## 🧹 CLEANUP PROCEDURE

### **Step 1: Identify What to Archive**

**Archive candidates:**
- Session summaries older than current
- Status reports superseded by status.json
- Completed mission files
- Old coordination trackers
- Responded-to messages

**Keep active:**
- status.json
- Current mission files (1-3 only)
- Unresponded inbox messages
- Current devlogs
- Active coordination dashboards

### **Step 2: Create Archive Structure**

```bash
cd agent_workspaces/Agent-X

# Create archive directories
mkdir -p archive/2025-10
mkdir -p archive/session_summaries
mkdir -p archive/old_status_reports
mkdir -p inbox/archive/2025-10
mkdir -p devlogs/archive/2025-10
```

### **Step 3: Move Files to Archive**

```bash
# Archive old session summaries
mv *SESSION_SUMMARY*.md archive/session_summaries/

# Archive old status reports
mv *READY*.md *STATUS*.md archive/old_status_reports/

# Archive completed missions
mv C0*_*.md archive/2025-10/

# Archive old inbox
cd inbox
mv C2A_*.md CAPTAIN_MESSAGE_*.md archive/2025-10/
cd ..
```

### **Step 4: Verify Clean State**

```bash
# Check root directory
ls *.md | wc -l
# Should be: <10 files

# Check inbox
ls inbox/*.md | wc -l  
# Should be: <10 unresponded messages
```

---

## 📨 INBOX MANAGEMENT

### **Inbox Hygiene Rules:**

**1. Check inbox EVERY cycle** (mandatory!)

**2. Categorize messages:**
- 🚨 **URGENT:** Respond immediately
- ⚡ **IMPORTANT:** Respond within 2 cycles
- 📋 **NORMAL:** Respond within 5 cycles
- 📁 **FYI:** Read and archive

**3. After responding:**
- Move to inbox/archive/YYYY-MM/
- Keep inbox/ root clean (<10 active messages)

**4. Unresponded messages:**
- If >10 unresponded: PRIORITY cleanup day!
- Respond to all or archive with reason

---

## 🎯 WORKSPACE AUDIT CHECKLIST

**Run this every 10 cycles:**

- [ ] Root directory has <10 .md files
- [ ] status.json is current (updated this cycle)
- [ ] Inbox has <10 unresponded messages
- [ ] All old sessions archived
- [ ] Devlogs organized by mission/month
- [ ] Test directories cleaned
- [ ] No orphaned files
- [ ] Archive/ properly organized

**If any fail:** Immediate cleanup required!

---

## 🚨 ENFORCEMENT

### **Captain/Co-Captain Checks:**

**Every 5 cycles:**
- Audit all 8 agent workspaces
- Flag cluttered workspaces
- Send cleanup reminders
- Track compliance

**Workspace Violations:**
- >20 files in root: ⚠️ WARNING
- >50 files in root: 🚨 CRITICAL
- >20 unresponded messages: 🚨 CRITICAL
- status.json >5 cycles old: 🚨 CRITICAL

---

## 📊 CLEANUP METRICS

**Healthy Workspace:**
- ✅ <10 files in root
- ✅ <10 unresponded inbox messages
- ✅ status.json current (this cycle)
- ✅ Archive/ properly organized
- ✅ Easy to find current work

**Unhealthy Workspace (Agent-6 BEFORE cleanup):**
- ❌ 90+ files in root
- ❌ 50+ inbox messages
- ❌ Hard to find current work
- ❌ Multiple duplicate status files

**After cleanup:**
- ✅ ~5-7 files in root
- ✅ Current files only
- ✅ Clean and professional

---

## 🚀 QUICK CLEANUP SCRIPT

```bash
#!/bin/bash
# cleanup_workspace.sh

AGENT_ID=$1

cd agent_workspaces/$AGENT_ID

# Create archives
mkdir -p archive/$(date +%Y-%m)
mkdir -p archive/session_summaries
mkdir -p inbox/archive/$(date +%Y-%m)

# Archive old summaries
mv *SUMMARY*.md archive/session_summaries/ 2>/dev/null

# Archive old status
mv *READY*.md *COMPLETE*.md archive/$(date +%Y-%m)/ 2>/dev/null

# Archive completed missions
mv C0*_*.md archive/$(date +%Y-%m)/ 2>/dev/null

# Archive old inbox
cd inbox
mv *_20*.md archive/$(date +%Y-%m)/ 2>/dev/null
cd ..

echo "✅ Workspace cleaned for $AGENT_ID"
```

**Usage:**
```bash
./cleanup_workspace.sh Agent-6
```

---

**WE. ARE. SWARM.** 🐝⚡

**Clean workspaces = Efficient agents!**

---

**#WORKSPACE_HYGIENE #CLEANUP_PROCEDURE #MANDATORY #CO_CAPTAIN_EXAMPLE**

