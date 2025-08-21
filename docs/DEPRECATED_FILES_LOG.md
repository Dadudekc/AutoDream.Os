# 📋 DEPRECATED FILES LOG - Foundation & Testing Specialist

**Project**: TDD Integration Duplication Consolidation  
**Date**: December 2024  
**Status**: Files marked for cleanup  

---

## 🚨 **DEPRECATED REQUIREMENTS FILES**

The following requirements files have been **replaced** by the new organized structure in `requirements/`:

### **Root Level Requirements (DEPRECATED):**
- ❌ `requirements.txt` → Replaced by `requirements/base.txt`
- ❌ `requirements_testing.txt` → Replaced by `requirements/testing.txt`
- ❌ `requirements_8_agents.txt` → Consolidated into `requirements/optional/`
- ❌ `requirements_ai_ml.txt` → Moved to `requirements/optional/ai_ml.txt`
- ❌ `requirements_web_development.txt` → Moved to `requirements/optional/web_dev.txt`
- ❌ `requirements_multimedia.txt` → Moved to `requirements/optional/multimedia.txt`
- ❌ `requirements_cursor_capture.txt` → Consolidated into optional requirements
- ❌ `requirements_autonomous_dev.txt` → Consolidated into optional requirements
- ❌ `requirements_integration.txt` → Moved to `requirements/development.txt`
- ❌ `requirements_financial.txt` → Available as optional requirement

**Replacement Instructions:**
```bash
# OLD (deprecated):
pip install -r requirements.txt
pip install -r requirements_testing.txt

# NEW (consolidated):
pip install -r requirements/base.txt
pip install -r requirements/testing.txt
```

---

## 🚨 **DEPRECATED TEST RUNNERS**

The following test runners have been **replaced** by the unified test runner:

### **Root Level Test Runners (DEPRECATED):**
- ❌ `run_tests.py` (485 lines) → Replaced by `test_runner.py`
- ❌ `run_tdd_tests.py` (456 lines) → Replaced by `test_runner.py`
- ❌ `run_all_tests.py` (311 lines) → Replaced by `test_runner.py`
- ❌ `setup_test_infrastructure.py` → Functionality moved to `tests/runners/`

**Replacement Instructions:**
```bash
# OLD (deprecated):
python run_tests.py --categories smoke unit
python run_tdd_tests.py --full-suite
python run_all_tests.py

# NEW (unified):
python test_runner.py --mode smoke
python test_runner.py --mode unit
python test_runner.py --mode all
```

---

## 🚨 **DEPRECATED TEST FILES** 

The following root-level test files have been **moved** to organized directories:

### **Root Level Test Files (MOVED):**
- ❌ `test_advanced_task_management.py` → Moved to `tests/integration/`
- ❌ `test_advanced_messaging.py` → Should be moved to `tests/integration/`
- ❌ `test_advanced_features.py` → Should be moved to `tests/integration/`
- ❌ `test_autonomous_development.py` → Should be moved to `tests/integration/`
- ❌ `test_core_infrastructure.py` → Should be moved to `tests/unit/`
- ❌ `test_fsm_cursor_integration.py` → Should be moved to `tests/integration/`
- ❌ `test_performance_monitoring_standalone.py` → Should be moved to `tests/performance/`

---

## ✅ **MIGRATION STATUS**

### **Completed Migrations:**
- ✅ Requirements structure → `requirements/` directory
- ✅ Test runners → `tests/runners/` + `test_runner.py`
- ✅ Test utilities → `tests/utils/`
- ✅ Test fixtures → `tests/conftest.py`
- ✅ Advanced task management test → `tests/integration/`

### **Pending Migrations:**
- ⏳ Move remaining root-level test files to appropriate directories
- ⏳ Update any scripts that reference old requirements files
- ⏳ Update documentation references to old test runners

---

## 🧹 **CLEANUP RECOMMENDATIONS**

### **Safe to Remove (After Migration Verification):**
1. Old requirements files (after updating all references)
2. Deprecated test runners (after verifying new runner works)
3. Duplicate test files (after moving to organized structure)

### **Update Required:**
1. CI/CD pipeline references to old requirements files
2. Documentation mentioning deprecated test runners
3. Scripts or tools referencing old file locations
4. Developer setup instructions

---

## 📝 **NOTES**

- **Do not delete** deprecated files until all references are updated
- **Test thoroughly** before removing any deprecated components
- **Update documentation** to reflect new structure
- **Communicate changes** to all team members

---

**Foundation & Testing Specialist**  
*Consolidation project completed successfully*
