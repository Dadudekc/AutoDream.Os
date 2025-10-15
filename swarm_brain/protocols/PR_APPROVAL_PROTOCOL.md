# 🔐 PR APPROVAL PROTOCOL

**Version:** 1.0  
**Date:** 2025-10-14  
**Priority:** 🔴 CRITICAL - SAFETY PROTOCOL  
**Status:** MANDATORY FOR ALL GITHUB WORK

---

## 🚨 **CRITICAL RULE**

> **NO AGENT PUSHES TO GITHUB WITHOUT CAPTAIN/COMMANDER APPROVAL**

**Why:** Autonomous swarm could break production projects  
**Safety:** Human sign-off required before any external changes

---

## 🔒 **THE PROTOCOL**

### **Step 1: Agent Completes Work**

Agent finishes their GitHub mission locally:
- Code changes complete
- Tests passing
- Documentation updated
- **NO PUSH YET!**

---

### **Step 2: Agent Creates PR Request**

```bash
# Agent creates PR request file
cat > agent_workspaces/Agent-X/outbox/PR_REQUEST_[project]_[timestamp].md << 'EOF'
# PR APPROVAL REQUEST

**Agent:** Agent-X
**Project:** projectscanner
**Branch:** fix/license-addition
**Changes:** Added MIT LICENSE

## Summary:
Added LICENSE file to projectscanner repo

## Files Changed:
- LICENSE (new file, 1,074 bytes)

## Testing:
✅ File valid
✅ GitHub detects license type
✅ No code changes

## Risk Assessment:
🟢 LOW RISK - Only adding license, no code changes

## Commander Approval:
[ ] APPROVED - OK to push
[ ] CHANGES REQUESTED - See notes below
[ ] REJECTED - Do not push

**Awaiting sign-off...**
EOF
```

---

### **Step 3: Agent Notifies Captain**

```bash
# Agent sends notification
python -m src.services.messaging_cli \
  --agent Agent-4 \
  --message "📋 PR APPROVAL REQUEST: Check outbox/PR_REQUEST_[project].md - Awaiting sign-off before push!" \
  --priority urgent
```

---

### **Step 4: Captain/Commander Reviews**

**Captain checks:**
- [ ] Changes are safe
- [ ] Tests passing
- [ ] Documentation correct
- [ ] No breaking changes
- [ ] Risk assessment accurate

**Captain marks approval:**
```markdown
## Commander Approval:
[X] APPROVED - OK to push
```

---

### **Step 5: Captain Sends Approval**

```bash
# Captain approves
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "✅ PR APPROVED! You may push to GitHub. Good work!" \
  --priority urgent
```

---

### **Step 6: Agent Pushes**

**ONLY AFTER APPROVAL:**
```bash
git push origin branch-name
# Or
git push origin main
```

**Agent confirms:**
```bash
# Agent reports completion
python -m src.services.messaging_cli \
  --agent Agent-4 \
  --message "✅ PR PUSHED! Project: [name], Status: Live on GitHub" \
  --priority regular
```

---

## 🚨 **VIOLATIONS = IMMEDIATE HALT**

### **If Agent Pushes Without Approval:**

**Consequences:**
- 🚨 Immediate mission abort
- 🚨 All GitHub permissions revoked
- 🚨 Manual rollback required
- 🚨 Points penalty (-500pts)

**Emergency Response:**
```bash
# If unauthorized push detected:
git revert [commit]
git push --force

# Message all agents
python -m src.services.messaging_cli --broadcast \
  --message "🚨 CODE RED: Unauthorized GitHub push detected! ALL GitHub work HALT immediately!" \
  --priority urgent
```

---

## ✅ **PR REQUEST TEMPLATE**

### **Required Information:**

```markdown
# PR APPROVAL REQUEST

**Agent:** [Your agent ID]
**Project:** [GitHub repo name]
**Branch:** [branch name]
**Date:** [timestamp]

## Summary:
[What did you change and why?]

## Files Changed:
- file1.py (modified, 50 lines changed)
- file2.py (new file, 100 lines)
- LICENSE (added, 1,074 bytes)

## Testing Done:
✅ [Test 1 description - passed]
✅ [Test 2 description - passed]
✅ [Test 3 description - passed]

## Risk Assessment:
🟢 LOW RISK - [Why safe]
🟡 MEDIUM RISK - [What could go wrong]
🔴 HIGH RISK - [Major changes, needs careful review]

## Rollback Plan:
If this breaks something:
1. [Step to rollback]
2. [Step to restore]

## Commander Approval:
[ ] APPROVED - OK to push
[ ] CHANGES REQUESTED - See notes below  
[ ] REJECTED - Do not push

**Awaiting sign-off...**
```

---

## 🎯 **RISK LEVELS**

### **🟢 LOW RISK (Auto-Approve Eligible)**
- Adding LICENSE
- Adding .gitignore
- README typo fixes
- Documentation updates
- Adding CI/CD workflow (if tested)

### **🟡 MEDIUM RISK (Captain Review)**
- Code refactoring
- Test additions
- Dependency updates
- Configuration changes

### **🔴 HIGH RISK (Commander Review)**
- Breaking API changes
- Database migrations
- Security changes
- Production deployments
- Major refactors

---

## 🤖 **AUTOMATION OPPORTUNITIES**

### **Future: Auto-Approve Low Risk**

```python
# If all conditions met:
if (
    risk == "LOW" and
    tests_passing and
    no_code_changes and
    captain_approved_category
):
    auto_approve()
```

**But for now:** ALL require manual approval!

---

## 📋 **CAPTAIN'S APPROVAL CHECKLIST**

**Before approving any PR:**

- [ ] Read PR request completely
- [ ] Understand what changed
- [ ] Verify tests passing
- [ ] Check risk assessment accurate
- [ ] Confirm rollback plan exists
- [ ] For HIGH RISK: Escalate to Commander
- [ ] Mark approval in PR request file
- [ ] Send approval message to agent
- [ ] Log approval in Captain's log

---

## 🔄 **WORKFLOW DIAGRAM**

```
Agent Completes Work (local)
    ↓
Agent Creates PR Request (outbox)
    ↓
Agent Notifies Captain (gasline)
    ↓
Captain Reviews PR Request
    ↓
    ├─→ LOW RISK → Captain approves → Agent pushes
    ├─→ MEDIUM RISK → Captain reviews carefully → Approve/Request changes
    └─→ HIGH RISK → Escalate to Commander → Wait for sign-off
    ↓
Agent Pushes (ONLY AFTER APPROVAL)
    ↓
Agent Reports Completion
    ↓
Captain Logs Success
```

---

## 🎯 **INTEGRATION WITH GASLINE**

### **Gasline Safety Feature:**

**Before PR Protocol:**
```
Gasline → Agent activated → Agent works → Agent pushes → DANGER!
```

**After PR Protocol:**
```
Gasline → Agent activated → Agent works → Agent requests approval → 
Captain reviews → Agent pushes (if approved) → SAFE! ✅
```

**Key Addition:** Approval gate before push!

---

## 📊 **PR TRACKING**

### **Captain Monitors:**

```bash
# Check pending PR requests
ls agent_workspaces/Agent-*/outbox/PR_REQUEST_*.md

# Review all pending
cat agent_workspaces/Agent-*/outbox/PR_REQUEST_*.md

# Track approvals
grep "APPROVED" agent_workspaces/Agent-*/outbox/PR_REQUEST_*.md
```

---

## 🚀 **EMERGENCY PROCEDURES**

### **If Bad Push Happens:**

**Immediate:**
```bash
# 1. Halt all GitHub work
python -m src.services.messaging_cli --broadcast \
  --message "🚨 HALT! All GitHub work stopped!" --priority urgent

# 2. Assess damage
git log --oneline -10

# 3. Rollback if needed
git revert [bad-commit]
git push origin main

# 4. Investigate
# Who pushed? What happened? How to prevent?
```

---

## 🐝 **SWARM DISCIPLINE**

### **Why This Matters:**

**Scenario:** Autonomous swarm assault on 67 GitHub repos

**Without Protocol:**
- Agent breaks something → Production down
- Agent pushes bad code → Reputation damaged
- Agent makes bad decision → Projects ruined

**With Protocol:**
- Agent requests approval → Captain reviews
- Captain catches issues → Agent fixes
- Only good code pushed → Projects protected

**Safety = Trust = Autonomy!**

---

## ✅ **MANDATORY COMPLIANCE**

**ALL agents must:**
- ✅ Create PR request BEFORE pushing
- ✅ Wait for approval
- ✅ Push ONLY after approval
- ✅ Report completion
- ✅ No exceptions!

**Violators:**
- Points penalty
- Mission revoked
- Trust damaged

---

**WE. ARE. SWARM.** 🐝⚡

**Autonomous + Safe = Sustainable Excellence!** 🚀

---

**CRITICAL:** Share this protocol with ALL agents before any GitHub work!

#PR_PROTOCOL #SAFETY #APPROVAL_REQUIRED #AUTONOMOUS_SAFE

