# UNIFIED CODING STANDARDS 2024
## Agent Cellphone V2 Repository

---

## 🎯 **OVERVIEW**

This document consolidates the updated coding standards across the entire Agent Cellphone V2 repository. All previous references to strict 200/300 LOC limits have been updated to reflect a more balanced, maintainable approach.

---

## 📏 **UPDATED LINE COUNT STANDARDS (2024)**

### **New Balanced Approach:**
- **Standard Files**: **400 LOC** - Balanced for maintainability
- **GUI Components**: **600 LOC** - Generous for UI while maintaining structure  
- **Core Files**: **400 LOC** - Focused and testable business logic

### **Previous Strict Standards (Deprecated):**
- ~~Standard Files: 200 LOC~~ ❌
- ~~GUI Components: 300 LOC~~ ❌  
- ~~Core Files: 200 LOC~~ ❌

---

## 🔄 **WHAT WAS UPDATED**

### **1. Pre-commit Configuration**
- **File**: `.pre-commit-config.yaml`
- **Change**: Updated V2 standards checker hook name and comments
- **Status**: ✅ **COMPLETED**

### **2. V2 Standards Checker**
- **File**: `tests/v2_standards_checker_simple.py`
- **Change**: Updated LOC constants from 200/300/200 to 400/600/400
- **Status**: ✅ **COMPLETED**

### **3. Main Standards Documentation**
- **File**: `docs/standards/V2_CODING_STANDARDS.md`
- **Change**: Updated all LOC references and directory structure examples
- **Status**: ✅ **COMPLETED**

### **4. Quick Reference Guide**
- **File**: `docs/standards/CODING_STANDARDS_QUICK_REFERENCE.md`
- **Change**: Updated all LOC limits and compliance checklists
- **Status**: ✅ **COMPLETED**

### **5. Test Configuration**
- **File**: `tests/conftest.py`
- **Change**: Updated MAX_LOC constants to match new standards
- **Status**: ✅ **COMPLETED**

---

## 🚨 **FILES STILL NEEDING UPDATES**

The following files still contain references to old standards and need to be updated:

### **Scripts Directory:**
- `scripts/README.md` - References ≤200 LOC
- `scripts/utilities/validate_compliance_tracker.py` - References 300 LOC
- `scripts/utilities/setup_precommit_hooks.py` - References ≤200 LOC
- `scripts/analysis/analyze_test_coverage.py` - References 200 LOC
- `scripts/utilities/check_line_counts.py` - References 300 LOC

### **Tools Directory:**
- `tools/README.md` - References ≤200 LOC
- `tools/duplication_detector_main.py` - References ≤200 LOC
- `tools/duplication/duplication_reporter.py` - References ≤200 LOC
- `tools/duplication/duplication_detector.py` - References ≤200 LOC
- `tools/duplication/code_analyzer.py` - References ≤200 LOC
- `tools/duplication/duplication_types.py` - References ≤200 LOC
- `tools/duplication/__init__.py` - References ≤200 LOC

### **Source Code:**
- Multiple files in `src/core/` - Reference 200 LOC limits
- `gaming_systems/osrs/README.md` - References ≤200 LOC
- Various gaming system files - Reference ≤200 LOC

### **Examples:**
- `examples/workflows/sprint_system_demo.py` - References 200 LOC limit
- `examples/workflows/sprint_demo_simple.py` - References 200 LOC limit
- `examples/workflows/demo_suite.py` - References 200 LOC limit

### **Data Files:**
- `data/refactoring_tasks.json` - Contains target_lines: 300

---

## 🎯 **NEXT STEPS**

### **Immediate Actions:**
1. **Update all file headers** that reference old LOC standards
2. **Update README files** in each directory
3. **Update refactoring task data** to reflect new targets
4. **Update example files** to demonstrate new standards

### **Recommended Approach:**
1. **Batch update** all file headers with new standards
2. **Update documentation** systematically by directory
3. **Update data files** to reflect new targets
4. **Verify consistency** across the entire project

---

## 📋 **NEW STANDARDS SUMMARY**

### **File Size Guidelines:**
- **Small files** (< 200 LOC): Excellent, keep as-is
- **Medium files** (200-400 LOC): Good, acceptable
- **Large files** (400-600 LOC): Monitor, refactor if quality suffers
- **Very large files** (> 600 LOC): Must refactor (except GUI files up to 600 LOC)

### **Quality Over Quantity:**
- **Focus on maintainability** rather than strict line counts
- **OOP principles** remain mandatory
- **Single Responsibility Principle** is still required
- **CLI interfaces** are still mandatory for all components
- **Smoke tests** are still required for all components

---

## 🔍 **VERIFICATION COMMANDS**

To verify the new standards are working:

```bash
# Run the updated V2 standards checker
python tests/v2_standards_checker_simple.py --all

# Check pre-commit hooks
pre-commit run --all-files

# Run tests to ensure new limits are enforced
pytest tests/ -v
```

---

## 📝 **CONTACT & UPDATES**

This document should be updated whenever coding standards change. All team members should reference this unified document rather than individual file standards.

**Last Updated**: 2024
**Standards Version**: V2.1 (Balanced Approach)
**Previous Version**: V2.0 (Strict Approach)
