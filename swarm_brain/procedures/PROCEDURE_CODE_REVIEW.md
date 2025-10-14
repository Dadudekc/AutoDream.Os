# PROCEDURE: Code Review Process

**Category**: Quality Assurance  
**Author**: Agent-5  
**Date**: 2025-10-14  
**Tags**: code-review, qa, peer-review

---

## 🎯 WHEN TO USE

**Trigger**: Pull request created OR major refactoring completed

**Who**: Senior agents or designated reviewers

---

## 📋 PREREQUISITES

- Code changes committed to branch
- Tests passing
- V2 compliance verified

---

## 🔄 PROCEDURE STEPS

### **Step 1: Review Checklist**

**Code Quality**:
- [ ] Follows PEP 8 style
- [ ] Type hints present
- [ ] Docstrings comprehensive
- [ ] No commented-out code
- [ ] No print() statements (use logger)

**V2 Compliance**:
- [ ] Files ≤400 lines
- [ ] Functions ≤30 lines
- [ ] Classes ≤200 lines
- [ ] ≤10 functions per module
- [ ] ≤5 classes per module

**Architecture**:
- [ ] SOLID principles followed
- [ ] No circular dependencies
- [ ] Proper error handling
- [ ] Single responsibility principle

**Testing**:
- [ ] Tests included
- [ ] Coverage ≥85%
- [ ] Edge cases covered
- [ ] Integration tests if needed

### **Step 2: Run Automated Checks**

```bash
# V2 compliance
python -m tools_v2.toolbelt v2.check --file changed_file.py

# Architecture validation
python tools/arch_pattern_validator.py changed_file.py

# Test coverage
pytest --cov=src --cov-report=term-missing
```

### **Step 3: Manual Review**

- Read code thoroughly
- Check logic correctness
- Verify error handling
- Test locally if needed

### **Step 4: Provide Feedback**

```bash
# If issues found, message author
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "Code review feedback: [specific issues]"

# Or approve
python -m src.services.messaging_cli \
  --agent Agent-X \
  --message "Code review: APPROVED ✅"
```

---

## ✅ SUCCESS CRITERIA

- [ ] All checklist items passed
- [ ] Automated checks passed
- [ ] Manual review completed
- [ ] Feedback provided
- [ ] Approval given (if no issues)

---

## 📝 EXAMPLES

**Example: Approving Code**

```bash
# Run checks
$ python -m tools_v2.toolbelt v2.check --file src/new_feature.py
✅ COMPLIANT

$ pytest tests/test_new_feature.py
✅ All tests passing

# Review code manually
# Looks good!

# Approve
$ python -m src.services.messaging_cli \
  --agent Agent-7 \
  --message "Code review APPROVED ✅ - Excellent work on new feature. V2 compliant, well-tested, clean architecture."
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_V2_COMPLIANCE_CHECK
- PROCEDURE_TEST_EXECUTION
- PROCEDURE_GIT_COMMIT_WORKFLOW

---

**Agent-5 - Procedure Documentation** 📚

