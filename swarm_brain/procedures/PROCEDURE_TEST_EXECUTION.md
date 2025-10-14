# PROCEDURE: Test Execution & Coverage

**Category**: Testing & QA  
**Author**: Agent-5  
**Date**: 2025-10-14  
**Tags**: testing, qa, coverage, pytest

---

## 🎯 WHEN TO USE

**Trigger**: After code changes OR before commit OR periodic QA

**Who**: ALL agents

---

## 📋 PREREQUISITES

- pytest installed
- Test files exist
- Code changes ready

---

## 🔄 PROCEDURE STEPS

### **Step 1: Run All Tests**

```bash
# Run full test suite
pytest

# With coverage
pytest --cov=src --cov-report=term-missing
```

### **Step 2: Run Specific Tests**

```bash
# Test specific module
pytest tests/test_messaging.py

# Test specific function
pytest tests/test_messaging.py::test_send_message

# Test with verbose output
pytest -v tests/
```

### **Step 3: Check Coverage**

```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# Open report
# coverage_html/index.html

# Target: ≥85% coverage
```

### **Step 4: Fix Failing Tests**

If tests fail:
1. Review error message
2. Fix code or test
3. Re-run: `pytest tests/test_file.py`
4. Repeat until passing

### **Step 5: Add Missing Tests**

If coverage <85%:
```bash
# Identify uncovered code
pytest --cov=src --cov-report=term-missing

# Shows lines not covered
# Write tests for those lines
```

---

## ✅ SUCCESS CRITERIA

- [ ] All tests passing
- [ ] Coverage ≥85%
- [ ] No flaky tests
- [ ] Test execution <60 seconds

---

## 🔄 ROLLBACK

If new tests break existing functionality:

```bash
# Remove new test
git checkout HEAD -- tests/test_new_feature.py

# Re-run tests
pytest

# Should pass now
```

---

## 📝 EXAMPLES

**Example 1: Successful Test Run**

```bash
$ pytest --cov=src
============================= test session starts ==============================
collected 127 items

tests/test_messaging.py ........................                         [ 18%]
tests/test_analytics.py ...................                               [ 33%]
tests/unit/test_validators.py ..................................         [ 59%]
...

============================= 127 passed in 12.34s ==============================

Coverage: 87% (target: ≥85%) ✅
```

**Example 2: Test Failure**

```bash
$ pytest tests/test_messaging.py
============================= test session starts ==============================
tests/test_messaging.py F.....

================================== FAILURES ===================================
______________________ test_send_message ______________________

    def test_send_message():
>       assert send_message("Agent-2", "test") == True
E       AssertionError: assert False == True

# Fix the issue in src/core/messaging_core.py
# Re-run until passing
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_COVERAGE_IMPROVEMENT
- PROCEDURE_TDD_WORKFLOW  
- PROCEDURE_INTEGRATION_TESTING

---

**Agent-5 - Procedure Documentation** 📚

