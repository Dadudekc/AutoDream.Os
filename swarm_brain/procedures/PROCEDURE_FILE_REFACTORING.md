# PROCEDURE: File Refactoring for V2 Compliance

**Category**: Refactoring  
**Author**: Agent-5  
**Date**: 2025-10-14  
**Tags**: refactoring, v2-compliance, modularity

---

## 🎯 WHEN TO USE

**Trigger**: File >400 lines OR V2 violation detected

**Who**: Agent assigned to V2 compliance work

---

## 📋 PREREQUISITES

- Target file identified
- V2 compliance violation confirmed
- Refactoring plan ready

---

## 🔄 PROCEDURE STEPS

### **Step 1: Analyze File Structure**

```bash
# Get refactoring suggestions
python -m tools_v2.toolbelt infra.extract_planner --file path/to/large_file.py

# Shows:
# - Suggested module splits
# - Function groupings
# - Class extraction opportunities
```

### **Step 2: Plan Module Split**

**For 700-800 line files**: Split into **3 modules** ≤300 lines each

**Strategy**:
1. Group related functions by responsibility
2. Extract to separate modules
3. Keep main file as facade/coordinator

### **Step 3: Create New Modules**

```bash
# Create module files
touch path/to/file_core.py       # Core logic
touch path/to/file_utils.py      # Utilities
touch path/to/file_reporting.py  # Reporting/output
```

### **Step 4: Extract Code**

Move code systematically:
1. Copy related functions to new module
2. Update imports
3. Test functionality
4. Remove from original file

### **Step 5: Update Original File**

```python
# Original file becomes facade
from .file_core import CoreClass
from .file_utils import utility_function
from .file_reporting import generate_report

# Minimal orchestration code
# All heavy lifting delegated to modules
```

### **Step 6: Verify Compliance**

```bash
# Check all files now compliant
python -m tools_v2.toolbelt v2.check --file file_core.py
python -m tools_v2.toolbelt v2.check --file file_utils.py  
python -m tools_v2.toolbelt v2.check --file file_reporting.py
python -m tools_v2.toolbelt v2.check --file original_file.py

# All should show: ✅ COMPLIANT
```

### **Step 7: Test Functionality**

```bash
# Run tests
pytest tests/test_refactored_module.py

# All should pass
```

---

## ✅ SUCCESS CRITERIA

- [ ] All new modules ≤400 lines
- [ ] All files V2 compliant
- [ ] All tests passing
- [ ] Backward compatibility maintained
- [ ] Imports working correctly

---

## 🔄 ROLLBACK

If refactoring breaks functionality:

```bash
# Revert all changes
git checkout HEAD -- path/to/file*.py

# Re-plan refactoring strategy
# Try again with different approach
```

---

## 📝 EXAMPLES

**Example: Refactoring 797-line File**

```bash
# BEFORE:
tools/autonomous_task_engine.py (797 lines) 🔴 CRITICAL

# PLAN:
tools/autonomous/
  ├── task_discovery.py (~250 lines)
  ├── task_scoring.py (~250 lines)
  └── task_reporting.py (~250 lines)

# EXECUTE:
mkdir -p tools/autonomous
# [Extract code to modules]

# VERIFY:
$ python -m tools_v2.toolbelt v2.check --file tools/autonomous/task_discovery.py
✅ COMPLIANT (248 lines)

# RESULT: 797 → 750 lines (3 compliant modules)
# POINTS: 500 points earned!
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_V2_COMPLIANCE_CHECK
- PROCEDURE_MODULE_EXTRACTION
- PROCEDURE_BACKWARD_COMPATIBILITY_TESTING

---

**Agent-5 - Procedure Documentation** 📚

