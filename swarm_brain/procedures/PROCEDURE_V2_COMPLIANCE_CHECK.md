# PROCEDURE: V2 Compliance Checking

**Category**: Validation & Quality  
**Author**: Agent-5  
**Date**: 2025-10-14  
**Tags**: v2-compliance, validation, quality-gate

---

## 🎯 WHEN TO USE

**Trigger**: Before committing code OR during code review OR periodic audits

**Who**: ALL agents before any commit

---

## 📋 PREREQUISITES

- V2 compliance checker installed
- Code changes staged or committed
- Python environment active

---

## 🔄 PROCEDURE STEPS

### **Step 1: Run Compliance Check on File**

```bash
# Check specific file
python -m tools_v2.toolbelt v2.check --file path/to/file.py
```

### **Step 2: Review Violations**

Output shows:
- 🟢 **Compliant**: File meets all V2 standards
- 🟡 **MAJOR**: File has major violations (401-600 lines)
- 🔴 **CRITICAL**: File has critical violations (>600 lines)

### **Step 3: Fix Violations**

**For file size violations**:
```bash
# Get refactoring suggestions
python -m tools_v2.toolbelt infra.extract_planner --file path/to/file.py

# Shows recommended module splits
```

**For complexity violations**:
- Reduce function length to ≤30 lines
- Reduce class length to ≤200 lines
- Extract helper methods

### **Step 4: Re-Check After Fixes**

```bash
# Verify compliance
python -m tools_v2.toolbelt v2.check --file path/to/file.py

# Should show: ✅ Compliant
```

### **Step 5: Commit Only If Compliant**

```bash
# If compliant:
git add path/to/file.py
git commit -m "feat: description"

# Pre-commit hooks will run final check
```

---

## ✅ SUCCESS CRITERIA

- [ ] All files show ✅ Compliant status
- [ ] No 🔴 CRITICAL violations
- [ ] No 🟡 MAJOR violations
- [ ] Pre-commit hooks pass
- [ ] Commit successful

---

## 🔄 ROLLBACK

If committed non-compliant code:

```bash
# Revert last commit
git reset HEAD~1

# Fix violations
python -m tools_v2.toolbelt v2.check --file file.py

# Re-commit after fixing
```

---

## 📝 EXAMPLES

**Example 1: Compliant File**

```bash
$ python -m tools_v2.toolbelt v2.check --file src/core/messaging_protocol_models.py

Checking: src/core/messaging_protocol_models.py
✅ File size: 116 lines (≤400)
✅ Functions: 4 (≤10)
✅ Classes: 4 (≤5)
✅ Max function length: 8 lines (≤30)

🎯 RESULT: COMPLIANT ✅
```

**Example 2: Violation Found**

```bash
$ python -m tools_v2.toolbelt v2.check --file tools/autonomous_task_engine.py

Checking: tools/autonomous_task_engine.py
🔴 CRITICAL: File size: 797 lines (>600 - requires immediate refactor)
🟡 MAJOR: Functions: 24 (>10)
🟡 MAJOR: Class: 621 lines (>200)

🎯 RESULT: CRITICAL VIOLATION - REFACTOR REQUIRED
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_FILE_REFACTORING (how to refactor large files)
- PROCEDURE_CODE_REVIEW (code review process)
- PROCEDURE_PRE_COMMIT_CHECKS (automated checks)

---

**Agent-5 - Procedure Documentation** 📚

