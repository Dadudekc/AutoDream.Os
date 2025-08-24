# 🔧 SSOT Troubleshooting Guide
**Quick Reference for Common Issues**

## 📋 **Overview**

This guide provides step-by-step solutions for common Single Source of Truth (SSOT) issues that agents may encounter during daily operations.

**Target Audience**: All V2 agents  
**Skill Level**: Beginner to Intermediate  
**Update Frequency**: As needed based on new issues

---

## 🚨 **Emergency Quick Reference**

### **Critical Issues (Stop Work Immediately)**
| Issue | Quick Fix | Escalate To |
|-------|-----------|-------------|
| Validation script won't run | Check Python installation | Agent-4 |
| Master file corrupted/missing | Restore from Git backup | Agent-4 |
| Multiple agents editing simultaneously | Coordinate via messaging | Agent-4 |
| System-wide SSOT failure | Stop all tracker updates | Agent-4 |

### **Common Issues (Safe to Fix)**
| Issue | Quick Fix | Time |
|-------|-----------|------|
| Files out of sync | Run validation script | 1 min |
| Git merge conflicts | Edit master file, remove markers | 5 min |
| Duplicate entries | Edit master file, remove duplicates | 3 min |
| Wrong file counts | Run validation script | 1 min |

---

## 🔍 **Issue Identification Guide**

### **How to Identify Issues**

#### **Step 1: Run Validation**
```bash
python scripts/utilities/validate_compliance_tracker.py
```

#### **Step 2: Check Exit Code**
- **Exit Code 0**: ✅ All good, no issues
- **Exit Code 1**: ❌ Critical error, needs immediate attention
- **Exit Code 2**: ⚠️ Warning, minor issue detected

#### **Step 3: Read Status Message**
- **"Status: consistent"**: No issues
- **"Status: warning"**: Minor issues detected
- **"Status: error"**: Critical issues found

---

## 🛠️ **Detailed Troubleshooting**

### **Issue 1: "Tracker files are not identical"**

#### **Symptoms:**
```
🔍 Validating tracker consistency...
   Status: warning
   ⚠️  Issue: Tracker files are not identical
   💡 Recommendation: Synchronize tracker files
```

#### **Cause:**
The master file and docs copy have different content.

#### **Solution:**
```bash
# The validation script should auto-fix this
python scripts/utilities/validate_compliance_tracker.py

# Verify fix
python scripts/utilities/validate_compliance_tracker.py
# Should now show "Status: consistent"
```

#### **If Auto-Fix Fails:**
```bash
# Manual sync - copy master to docs
cp V2_COMPLIANCE_PROGRESS_TRACKER.md docs/reports/V2_COMPLIANCE_PROGRESS_TRACKER.md

# Validate
python scripts/utilities/validate_compliance_tracker.py
```

#### **Prevention:**
- Always run validation after editing master file
- Never edit the docs version manually

---

### **Issue 2: "Git merge conflicts detected"**

#### **Symptoms:**
```
🔍 Validating tracker consistency...
   Status: error
   ⚠️  Issue: Git merge conflicts detected in root tracker
```

#### **Cause:**
Unresolved Git merge conflicts in the master file.

#### **What You'll See in File:**
```markdown
<<<<<<< HEAD
**Current Compliance**: 58.6%
=======
**Current Compliance**: 60.0%
>>>>>>> feature/update-compliance
```

#### **Solution:**

##### **Step 1: Open Master File**
```bash
# Use your preferred editor
code V2_COMPLIANCE_PROGRESS_TRACKER.md
```

##### **Step 2: Find Conflict Markers**
Look for:
- `<<<<<<< HEAD`
- `=======`
- `>>>>>>> branch-name`

##### **Step 3: Resolve Conflicts**
Choose the correct version and remove all conflict markers:

**Before:**
```markdown
<<<<<<< HEAD
**Current Compliance**: 58.6%
=======
**Current Compliance**: 60.0%
>>>>>>> feature/update-compliance
```

**After:**
```markdown
**Current Compliance**: 58.6%
```

##### **Step 4: Validate Resolution**
```bash
python scripts/utilities/validate_compliance_tracker.py
# Should show "Status: consistent"
```

#### **Prevention:**
- Pull latest changes before editing
- Coordinate with other agents
- Use proper Git workflow

---

### **Issue 3: "One or more tracker files missing"**

#### **Symptoms:**
```
🔍 Validating tracker consistency...
   Status: error
   ⚠️  Issue: One or more tracker files missing
```

#### **Cause:**
Master file or docs copy has been deleted.

#### **Solution:**

##### **If Master File Missing:**
```bash
# Check if file was accidentally deleted
ls -la V2_COMPLIANCE_PROGRESS_TRACKER.md

# Restore from Git
git checkout HEAD V2_COMPLIANCE_PROGRESS_TRACKER.md

# If that fails, restore from backup
git log --oneline -- V2_COMPLIANCE_PROGRESS_TRACKER.md
git checkout <commit-hash> V2_COMPLIANCE_PROGRESS_TRACKER.md

# Validate restoration
python scripts/utilities/validate_compliance_tracker.py
```

##### **If Docs File Missing:**
```bash
# Create docs directory if needed
mkdir -p docs/reports

# Run validation to recreate docs file
python scripts/utilities/validate_compliance_tracker.py
```

#### **Prevention:**
- Don't delete tracker files manually
- Use Git for version control
- Create regular backups

---

### **Issue 4: "Duplicate contract entries detected"**

#### **Symptoms:**
```
🔍 Validating tracker consistency...
   Status: warning
   ⚠️  Issue: Duplicate contract entries detected
```

#### **Cause:**
Same contract appears multiple times in the tracker.

#### **Solution:**

##### **Step 1: Find Duplicates**
```bash
# Search for duplicate contract numbers
grep -n "CONTRACT #" V2_COMPLIANCE_PROGRESS_TRACKER.md
```

##### **Step 2: Edit Master File**
Open the master file and remove duplicate entries, keeping only one copy of each contract.

##### **Step 3: Validate Fix**
```bash
python scripts/utilities/validate_compliance_tracker.py
```

#### **Prevention:**
- Check for existing entries before adding new ones
- Use search function in editor
- Review changes before saving

---

### **Issue 5: Validation Script Won't Run**

#### **Symptoms:**
```bash
python scripts/utilities/validate_compliance_tracker.py
# Returns error or "command not found"
```

#### **Possible Causes & Solutions:**

##### **Cause A: Wrong Directory**
```bash
# Check current directory
pwd

# Navigate to repository root
cd D:\Agent_Cellphone_V2_Repository

# Try again
python scripts/utilities/validate_compliance_tracker.py
```

##### **Cause B: Python Not Installed**
```bash
# Check Python installation
python --version

# If not found, install Python or use alternative
python3 scripts/utilities/validate_compliance_tracker.py
```

##### **Cause C: Script File Missing**
```bash
# Check if script exists
ls -la scripts/utilities/validate_compliance_tracker.py

# If missing, restore from Git
git checkout HEAD scripts/utilities/validate_compliance_tracker.py
```

##### **Cause D: Permission Issues**
```bash
# Check permissions
ls -la scripts/utilities/validate_compliance_tracker.py

# Fix permissions if needed (Linux/Mac)
chmod +x scripts/utilities/validate_compliance_tracker.py
```

---

### **Issue 6: Incorrect File Counts**

#### **Symptoms:**
Validation shows different file counts than expected.

#### **Cause:**
Files have been added, deleted, or moved since last validation.

#### **Solution:**
```bash
# This is normal - validation script recalculates automatically
# Just run validation to get current counts
python scripts/utilities/validate_compliance_tracker.py

# The displayed counts are always current and accurate
```

#### **Note:**
File counts in the tracker are automatically updated by the validation script. Don't edit them manually.

---

### **Issue 7: Slow Validation Performance**

#### **Symptoms:**
Validation script takes a very long time to run.

#### **Possible Causes & Solutions:**

##### **Cause A: Large Repository**
```bash
# Check repository size
du -sh .

# If very large, consider excluding certain directories
# (This requires script modification - contact Agent-4)
```

##### **Cause B: System Resources**
```bash
# Check system resources
# Close unnecessary applications
# Run validation during low-usage periods
```

##### **Cause C: Network Issues**
```bash
# Ensure you're working locally, not over network
# Copy repository locally if working remotely
```

---

### **Issue 8: Agent Coordination Conflicts**

#### **Symptoms:**
Multiple agents trying to update tracker simultaneously.

#### **Solution:**

##### **Step 1: Immediate Coordination**
```
# Send message to team
"SSOT UPDATE IN PROGRESS - Agent-X updating tracker, please wait"
```

##### **Step 2: Check for Conflicts**
```bash
# Before editing, always check status
python scripts/utilities/validate_compliance_tracker.py
```

##### **Step 3: Quick Updates**
- Make updates quickly and efficiently
- Validate immediately after changes
- Notify team when complete

##### **Step 4: If Conflicts Occur**
```bash
# Pull latest changes
git pull origin main

# Resolve any conflicts
# Re-run validation
python scripts/utilities/validate_compliance_tracker.py
```

#### **Prevention:**
- Announce tracker updates in team chat
- Keep updates brief and focused
- Coordinate with Agent-4 for major changes

---

## 📋 **Diagnostic Commands**

### **System Health Check**
```bash
# Full system check
python scripts/utilities/validate_compliance_tracker.py

# Check Git status
git status

# Check file permissions
ls -la V2_COMPLIANCE_PROGRESS_TRACKER.md
ls -la docs/reports/V2_COMPLIANCE_PROGRESS_TRACKER.md

# Check Python environment
python --version
which python
```

### **File Integrity Check**
```bash
# Compare tracker files
diff V2_COMPLIANCE_PROGRESS_TRACKER.md docs/reports/V2_COMPLIANCE_PROGRESS_TRACKER.md

# Check file sizes
wc -l V2_COMPLIANCE_PROGRESS_TRACKER.md
wc -l docs/reports/V2_COMPLIANCE_PROGRESS_TRACKER.md

# Check for hidden characters
cat -A V2_COMPLIANCE_PROGRESS_TRACKER.md | head -10
```

### **Repository Analysis**
```bash
# Count Python files manually
find . -name "*.py" | wc -l

# Check for large files
find . -name "*.py" -exec wc -l {} + | sort -n | tail -20

# Check recent changes
git log --oneline -10 -- V2_COMPLIANCE_PROGRESS_TRACKER.md
```

---

## 🚨 **Escalation Procedures**

### **When to Escalate to Agent-4**

#### **Immediate Escalation (Critical):**
- ❌ Validation script completely fails
- ❌ Master file is corrupted or missing
- ❌ System-wide SSOT failure
- ❌ Data loss or corruption
- ❌ Multiple agents unable to work

#### **Standard Escalation (Non-Critical):**
- ⚠️ Repeated issues despite following guide
- ⚠️ New issues not covered in this guide
- ⚠️ Performance problems persisting
- ⚠️ Questions about SSOT procedures

### **Escalation Message Template**
```
SUBJECT: SSOT Issue - [CRITICAL/STANDARD] - Agent-X

ISSUE: [Brief description]

SYMPTOMS: [What you observed]

ATTEMPTED SOLUTIONS: [What you tried]

CURRENT STATUS: [Can you continue work?]

VALIDATION OUTPUT: [Paste relevant output]

URGENCY: [How urgent is this?]
```

### **Before Escalating:**
1. ✅ Try solutions in this guide
2. ✅ Run validation script
3. ✅ Check Git status
4. ✅ Document what you tried
5. ✅ Gather error messages

---

## 📚 **Reference Information**

### **File Locations**
- **Master File**: `V2_COMPLIANCE_PROGRESS_TRACKER.md`
- **Docs Copy**: `docs/reports/V2_COMPLIANCE_PROGRESS_TRACKER.md`
- **Validation Script**: `scripts/utilities/validate_compliance_tracker.py`
- **Results Report**: `data/compliance_validation_results.json`

### **Key Commands**
```bash
# Basic validation
python scripts/utilities/validate_compliance_tracker.py

# File comparison
diff V2_COMPLIANCE_PROGRESS_TRACKER.md docs/reports/V2_COMPLIANCE_PROGRESS_TRACKER.md

# Git operations
git status
git pull origin main
git checkout HEAD V2_COMPLIANCE_PROGRESS_TRACKER.md

# Backup operations
cp V2_COMPLIANCE_PROGRESS_TRACKER.md V2_COMPLIANCE_PROGRESS_TRACKER.md.backup
```

### **Exit Codes Reference**
- **0**: Success, all consistent
- **1**: Error, critical issues
- **2**: Warning, minor issues

### **Status Messages**
- **"consistent"**: All good
- **"warning"**: Minor issues
- **"error"**: Critical issues

---

## 🎯 **Best Practices for Issue Prevention**

### **Daily Habits**
1. **Always validate** before and after tracker updates
2. **Check status** before starting work
3. **Coordinate** with team for updates
4. **Keep backups** of important changes
5. **Report issues** promptly to Agent-4

### **Update Workflow**
1. **Check current status** → Run validation
2. **Make updates** → Edit master file only
3. **Validate changes** → Run validation script
4. **Verify success** → Check for "consistent" status
5. **Notify team** → Announce completion

### **Error Prevention**
- ✅ Never edit docs version manually
- ✅ Always run validation after changes
- ✅ Use proper Git workflow
- ✅ Coordinate with other agents
- ✅ Keep changes focused and small

---

## 📞 **Quick Help Contacts**

### **Primary Support**
- **Agent-4 (Quality Assurance)**: SSOT system guardian
- **Technical Issues**: Run validation first, then escalate
- **Process Questions**: Check training materials first

### **Self-Help Resources**
1. **This troubleshooting guide**
2. **SSOT training materials**
3. **Single Source of Truth guide**
4. **Validation script output**

### **Emergency Procedures**
1. **Stop work** if critical issues
2. **Notify Agent-4** immediately
3. **Document the issue** thoroughly
4. **Wait for guidance** before proceeding

---

**Remember: When in doubt, run the validation script first! 🔧**

*Most SSOT issues can be resolved quickly by following this guide. For persistent problems, don't hesitate to escalate to Agent-4.*
