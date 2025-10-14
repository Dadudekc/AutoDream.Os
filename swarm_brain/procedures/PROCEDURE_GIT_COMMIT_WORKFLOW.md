# PROCEDURE: Git Commit Workflow

**Category**: Development Workflow  
**Author**: Agent-5  
**Date**: 2025-10-14  
**Tags**: git, workflow, version-control, commits

---

## 🎯 WHEN TO USE

**Trigger**: After completing any code changes

**Who**: ALL agents

---

## 📋 PREREQUISITES

- Code changes tested and working
- V2 compliance verified
- Pre-commit hooks configured

---

## 🔄 PROCEDURE STEPS

### **Step 1: Verify Changes Are V2 Compliant**

```bash
# Check compliance BEFORE staging
python -m tools_v2.toolbelt v2.check --file path/to/changed/file.py

# Must show: ✅ COMPLIANT
```

### **Step 2: Stage Files**

```bash
# Stage specific files
git add path/to/file1.py path/to/file2.py

# OR stage all (if all compliant)
git add .
```

### **Step 3: Write Commit Message**

**Format**: `type: short description`

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring  
- `test:` - Test additions
- `chore:` - Maintenance

**Examples**:
```
feat: add memory leak detection tool
fix: resolve message queue race condition
docs: update agent onboarding guide
refactor: split autonomous_task_engine into 3 modules
```

### **Step 4: Commit**

```bash
# Commit with proper message
git commit -m "feat: your description here"

# Pre-commit hooks will run:
# - Ruff (linting)
# - Black (formatting)
# - isort (import sorting)
# - V2 violations check
```

### **Step 5: Handle Pre-Commit Results**

**If hooks PASS** ✅:
```
[agent-branch 1234abc] feat: your description
 3 files changed, 45 insertions(+), 12 deletions(-)
```
→ **SUCCESS! Proceed to push**

**If hooks FAIL** ❌:
```
ruff................................................Failed
- hook id: ruff
- exit code: 1

Found 5 syntax errors in file.py
```
→ **FIX ISSUES, re-commit**

### **Step 6: Push to Remote**

```bash
# Push to branch
git push

# If pre-push hooks fail, fix and re-push
```

---

## ✅ SUCCESS CRITERIA

- [ ] All files V2 compliant
- [ ] Commit message follows format
- [ ] Pre-commit hooks pass
- [ ] Pre-push hooks pass
- [ ] Changes pushed to remote

---

## 🔄 ROLLBACK

**Undo last commit** (if mistake):
```bash
git reset HEAD~1  # Undo commit, keep changes
```

**Undo commit and changes**:
```bash
git reset --hard HEAD~1  # ⚠️ DESTRUCTIVE - loses changes
```

**Revert pushed commit**:
```bash
git revert HEAD  # Creates new commit undoing changes
git push
```

---

## 📝 EXAMPLES

**Example 1: Successful Commit**

```bash
$ python -m tools_v2.toolbelt v2.check --file src/core/new_feature.py
✅ COMPLIANT

$ git add src/core/new_feature.py
$ git commit -m "feat: add intelligent caching system"
[agent-5-branch abc123] feat: add intelligent caching system
 1 file changed, 87 insertions(+)

$ git push
To github.com:user/repo.git
   def456..abc123  agent-5-branch -> agent-5-branch
```

**Example 2: Pre-Commit Failure**

```bash
$ git commit -m "fix: memory leak"
ruff.....................................Failed
- 5 syntax errors found

# Fix errors
$ python -m ruff check src/file.py --fix

# Re-commit
$ git commit -m "fix: memory leak"
✅ All hooks passed!
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_V2_COMPLIANCE_CHECK
- PROCEDURE_CODE_REVIEW
- PROCEDURE_PRE_COMMIT_HOOKS

---

**Agent-5 - Procedure Documentation** 📚

