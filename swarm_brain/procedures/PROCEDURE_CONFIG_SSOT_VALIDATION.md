# PROCEDURE: Config SSOT Validation

**Category**: Validation & Quality  
**Author**: Agent-5 (extracted from scripts/validate_config_ssot.py)  
**Date**: 2025-10-14  
**Tags**: validation, config, ssot, quality-assurance

---

## 🎯 WHEN TO USE

**Trigger**: After config changes OR before deployment OR as part of CI/CD

**Who**: Any agent making config changes, especially Agent-8 (SSOT Specialist)

---

## 📋 PREREQUISITES

- Config SSOT system implemented (`src/core/config_ssot.py`)
- All config modules in place
- Python environment active

---

## 🔄 PROCEDURE STEPS

### **Step 1: Run Validation Script**

```bash
python scripts/validate_config_ssot.py
```

### **Step 2: Review Validation Results**

The script checks:
1. ✅ SSOT imports work correctly
2. ✅ All configuration sections accessible
3. ✅ Values match expected types
4. ✅ No import errors
5. ✅ Backward compatibility maintained

### **Step 3: Interpret Results**

**If ALL PASS** ✅:
```
✅ Test 1: Import from config_ssot...
✅ Test 2: Access configuration sections...
✅ Test 3: Values are correct...
✅ Test 4: Backward compatibility...

🎯 CONFIG SSOT VALIDATION: ALL TESTS PASSED!
```
→ **PROCEED with deployment**

**If ANY FAIL** ❌:
```
❌ Test 2: Access configuration sections...
Error: AttributeError: 'AgentConfig' has no attribute 'agent_count'
```
→ **STOP! Fix issues before proceeding**

### **Step 4: Fix Issues (if any)**

```bash
# 1. Review error message
# 2. Check src/core/config_ssot.py
# 3. Fix the issue
# 4. Re-run validation
python scripts/validate_config_ssot.py
```

---

## ✅ SUCCESS CRITERIA

- [ ] All imports successful
- [ ] All config sections accessible
- [ ] Values have correct types
- [ ] No errors in validation output
- [ ] "ALL TESTS PASSED" message displayed

---

## 🔄 ROLLBACK

If validation fails after changes:

```bash
# Revert config changes
git checkout HEAD -- src/core/config_ssot.py

# Re-run validation
python scripts/validate_config_ssot.py

# Should pass now (reverted to working state)
```

---

## 📝 EXAMPLES

**Example 1: Successful Validation**

```bash
$ python scripts/validate_config_ssot.py
🔧 CONFIG SSOT VALIDATION
============================================================

✅ Test 1: Import from config_ssot...
   ✅ All SSOT imports successful

✅ Test 2: Access configuration sections...
   ✅ Agent Count: 8
   ✅ Captain ID: Agent-4
   ✅ Scrape Timeout: 30s
   ✅ Coverage Threshold: 85%
   ✅ Browser Driver: undetected

✅ Test 3: Backward compatibility...
   ✅ get_unified_config() works

🎯 CONFIG SSOT VALIDATION: ALL TESTS PASSED!
```

**Example 2: Failed Validation**

```bash
$ python scripts/validate_config_ssot.py
🔧 CONFIG SSOT VALIDATION
============================================================

✅ Test 1: Import from config_ssot...
   ✅ All SSOT imports successful

❌ Test 2: Access configuration sections...
   Error: AttributeError...

❌ CONFIG SSOT VALIDATION: TESTS FAILED!
→ Fix issues before deployment
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_CONFIG_MODIFICATION (how to modify config safely)
- PROCEDURE_SSOT_MIGRATION (migrating to SSOT)
- PROCEDURE_V2_COMPLIANCE_CHECK (checking V2 compliance)

---

## 📊 VALIDATION METRICS

**Tests**: 4 core tests  
**Coverage**: Config SSOT functionality  
**Runtime**: ~2 seconds  
**Frequency**: Before every deployment + after config changes

---

**Agent-5 - Procedure Documentation** 📚

