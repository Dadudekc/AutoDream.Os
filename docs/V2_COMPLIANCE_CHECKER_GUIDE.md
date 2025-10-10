# V2 Compliance Checker - Automated Quality Gate
## Complete User Guide

**Author**: Agent-6 (VSCode Forking & Quality Gates Specialist)  
**Version**: 1.0  
**Date**: 2025-10-09

---

## 📋 **Overview**

The V2 Compliance Checker is an automated quality gate system that enforces V2 compliance rules across the codebase. It scans Python files and reports violations of coding standards, helping maintain code quality and consistency.

---

## 🎯 **V2 Compliance Rules**

### **File-Level Rules**:
1. **File Size**: ≤400 lines (MAJOR if 401-600, CRITICAL if >600)
2. **Function Count**: ≤10 functions per file
3. **Class Count**: ≤5 classes per file
4. **Enum Count**: ≤3 enums per file

### **Function-Level Rules**:
5. **Function Size**: ≤30 lines per function
6. **Function Parameters**: ≤5 parameters per function

### **Class-Level Rules**:
7. **Class Size**: ≤200 lines per class

---

## 🚀 **Installation**

The V2 Compliance Checker is already included in the repository. No installation required!

### **Prerequisites**:
- Python 3.8+
- Standard library only (no external dependencies)

---

## 💻 **Usage**

### **Command Line Usage**:

#### **Scan Current Directory**:
```bash
python tools/v2_compliance_checker.py
```

#### **Scan Specific Directory**:
```bash
python tools/v2_compliance_checker.py src
```

#### **Scan with Custom Pattern**:
```bash
python tools/v2_compliance_checker.py src --pattern "**/*.py"
```

#### **Fail on Major Violations** (for CI/CD):
```bash
python tools/v2_compliance_checker.py --fail-on-major
```

#### **Fail on Critical Violations** (for strict enforcement):
```bash
python tools/v2_compliance_checker.py --fail-on-critical
```

#### **Verbose Output**:
```bash
python tools/v2_compliance_checker.py --verbose
```

---

## 🔧 **Pre-Commit Hook Integration**

The V2 Compliance Checker is automatically integrated with pre-commit hooks to block commits with major violations.

### **Setup Pre-Commit**:

1. **Install pre-commit** (if not installed):
```bash
pip install pre-commit
```

2. **Install hooks**:
```bash
pre-commit install
```

3. **Run hooks manually**:
```bash
pre-commit run --all-files
```

### **Hook Configuration**:

The hook is configured in `.pre-commit-config.yaml`:

```yaml
- id: v2-compliance-checker
  name: V2 Compliance Checker (Quality Gate)
  entry: python tools/v2_compliance_checker.py --fail-on-major
  language: system
  types: [python]
  pass_filenames: false
  stages: [commit]
```

This configuration:
- Runs on all Python files before commit
- Blocks commits with MAJOR or CRITICAL violations
- Provides detailed violation reports

---

## 📊 **Understanding the Report**

### **Report Structure**:

```
================================================================================
V2 COMPLIANCE REPORT
================================================================================
Total files scanned: 150
Compliant files: 120
Files with violations: 30
Compliance rate: 80.0%

VIOLATIONS FOUND: 45
  - Critical: 3 (>600 lines)
  - Major: 35 (>400 lines or rule violations)
  - Minor: 7

src/example/file.py:
  🔴 [CRITICAL] file: File has 658 lines (CRITICAL: >600 lines, requires immediate refactor)
  🟡 [MAJOR] line 82: Function 'calculate' has 45 lines (max 30)
  🟢 [MINOR] line 120: Function 'process' has 6 parameters (max 5)
```

### **Severity Levels**:

| Severity | Symbol | Meaning | Action Required |
|----------|--------|---------|-----------------|
| **CRITICAL** | 🔴 | File >600 lines | Immediate refactor |
| **MAJOR** | 🟡 | File >400 lines or rule violation | Refactor required |
| **MINOR** | 🟢 | Guideline violation | Improvement recommended |

---

## 🔍 **Violation Types Explained**

### **FILE_SIZE**:
- File exceeds maximum line count
- **Fix**: Extract code into separate modules

### **FUNCTION_COUNT**:
- Too many functions in one file
- **Fix**: Split into multiple focused modules

### **CLASS_COUNT**:
- Too many classes in one file
- **Fix**: Separate classes into their own files

### **ENUM_COUNT**:
- Too many enums in one file
- **Fix**: Extract enums to separate enum module

### **FUNCTION_SIZE**:
- Function too long
- **Fix**: Break into smaller helper functions

### **FUNCTION_PARAMS**:
- Too many parameters
- **Fix**: Use dataclasses or parameter objects

### **CLASS_SIZE**:
- Class too large
- **Fix**: Apply Single Responsibility Principle, extract methods

### **SYNTAX_ERROR**:
- Python syntax error detected
- **Fix**: Fix syntax errors before committing

---

## 🎓 **Examples**

### **Example 1: Clean Scan**:

```bash
$ python tools/v2_compliance_checker.py src/core/managers/
================================================================================
V2 COMPLIANCE REPORT
================================================================================
Total files scanned: 12
Compliant files: 12
Files with violations: 0
Compliance rate: 100.0%

✅ All files are V2 compliant!
================================================================================
```

### **Example 2: Violations Found**:

```bash
$ python tools/v2_compliance_checker.py src/services/
================================================================================
V2 COMPLIANCE REPORT
================================================================================
Total files scanned: 25
Compliant files: 18
Files with violations: 7
Compliance rate: 72.0%

VIOLATIONS FOUND: 15
  - Critical: 1 (>600 lines)
  - Major: 12 (>400 lines or rule violations)
  - Minor: 2

src/services/messaging_cli.py:
  🟡 [MAJOR] file: File has 403 lines (MAJOR VIOLATION: ≤400 required)
  🟡 [MAJOR] line 203: Function '_create_parser' has 69 lines (max 30)

src/services/simple_onboarding.py:
  🟡 [MAJOR] file: File has 445 lines (MAJOR VIOLATION: ≤400 required)
  🟡 [MAJOR] line 216: Function '_onboard_agent' has 51 lines (max 30)
  🟡 [MAJOR] line 34: Class 'SimpleOnboarding' has 411 lines (max 200)
================================================================================
```

---

## 🚦 **CI/CD Integration**

### **GitHub Actions Example**:

```yaml
name: V2 Compliance Check

on: [push, pull_request]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Run V2 Compliance Checker
        run: python tools/v2_compliance_checker.py --fail-on-major
```

### **GitLab CI Example**:

```yaml
v2_compliance:
  stage: test
  script:
    - python tools/v2_compliance_checker.py --fail-on-major
  only:
    - merge_requests
    - main
```

---

## 🛠️ **Fixing Violations**

### **Strategy 1: Extract to Helper Modules**

**Before** (523 lines):
```python
# core_resource_manager.py
class CoreResourceManager:
    def handle_file_operation(self, payload):
        # 100+ lines of file operations
        
    def handle_lock_operation(self, payload):
        # 100+ lines of lock operations
        
    def handle_context_operation(self, payload):
        # 100+ lines of context operations
```

**After** (266 lines + 3 helper modules):
```python
# core_resource_manager.py
from .resource_file_operations import FileOperations
from .resource_lock_operations import LockOperations
from .resource_context_operations import ContextOperations

class CoreResourceManager:
    def __init__(self):
        self.file_ops = FileOperations()
        self.lock_ops = LockOperations()
        self.context_ops = ContextOperations()
```

### **Strategy 2: Extract Configuration**

**Before** (457 lines):
```python
# unified_config.py
@dataclass
class TestConfig:
    test_categories: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "smoke": { ... },  # 70+ lines of categories
        "unit": { ... },
        # etc.
    })
```

**After** (324 lines + helper module):
```python
# unified_config.py
from .test_categories_config import get_test_categories

@dataclass
class TestConfig:
    test_categories: Dict[str, Dict[str, Any]] = field(default_factory=get_test_categories)
```

### **Strategy 3: Break Long Functions**

**Before** (60 lines):
```python
def complex_operation(param1, param2, param3, param4, param5, param6):
    # 60 lines of complex logic
    result1 = calculate_step1()
    result2 = calculate_step2()
    result3 = calculate_step3()
    return combine_results()
```

**After** (10 lines each):
```python
def complex_operation(config: OperationConfig):
    result1 = _calculate_step1(config)
    result2 = _calculate_step2(config, result1)
    result3 = _calculate_step3(config, result2)
    return _combine_results(result1, result2, result3)

def _calculate_step1(config): ...
def _calculate_step2(config, result1): ...
def _calculate_step3(config, result2): ...
def _combine_results(r1, r2, r3): ...
```

---

## 📈 **Best Practices**

### **1. Run Regularly**:
- Run before committing changes
- Include in CI/CD pipeline
- Regular codebase scans

### **2. Address Critical First**:
- Fix CRITICAL violations immediately (>600 lines)
- Then address MAJOR violations (>400 lines)
- Finally improve MINOR violations

### **3. Preventive Development**:
- Check file size as you develop
- Keep functions focused and small
- Apply Single Responsibility Principle

### **4. Team Coordination**:
- Share compliance reports with team
- Track compliance rate over time
- Celebrate 100% compliance milestones

### **5. Incremental Refactoring**:
- Don't refactor all at once
- Fix violations file by file
- Test after each refactor

---

## 🎯 **Success Metrics**

### **Target Compliance Rates**:
- **Green**: 90-100% compliant
- **Yellow**: 70-89% compliant
- **Red**: <70% compliant

### **Tracking Progress**:
```bash
# Weekly compliance check
python tools/v2_compliance_checker.py src > compliance_report.txt
git add compliance_report.txt
git commit -m "docs: Weekly compliance report"
```

---

## 🐛 **Troubleshooting**

### **Issue**: "File not found" error
**Solution**: Check file path and ensure file exists

### **Issue**: Syntax errors reported
**Solution**: Fix Python syntax errors first

### **Issue**: Too many violations
**Solution**: Focus on critical/major violations first, use `--fail-on-critical` initially

### **Issue**: Pre-commit hook not running
**Solution**: Run `pre-commit install` to ensure hooks are installed

---

## 📚 **Additional Resources**

- **V2 Compliance Standards**: `docs/V2_COMPLIANCE_EXCEPTIONS.md`
- **Architecture Guidelines**: `AGENTS.md`
- **Refactoring Examples**: See `agent_workspaces/Agent-6/` for real-world refactoring examples

---

## 🚀 **Quick Reference**

```bash
# Basic scan
python tools/v2_compliance_checker.py

# Scan specific directory
python tools/v2_compliance_checker.py src/core

# CI/CD mode (fail on major)
python tools/v2_compliance_checker.py --fail-on-major

# Strict mode (fail on critical)
python tools/v2_compliance_checker.py --fail-on-critical

# Install pre-commit hooks
pre-commit install

# Run pre-commit manually
pre-commit run --all-files
```

---

**🐝 WE ARE SWARM** - Automated quality gates for consistent code excellence!

---

**Agent-6 Signature**: Quality Gates & V2 Compliance Specialist  
**Tool Version**: 1.0  
**Last Updated**: 2025-10-09




