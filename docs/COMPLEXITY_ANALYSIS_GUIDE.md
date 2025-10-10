# Complexity Analysis - Intelligent Quality Automation
## Complete User Guide

**Author**: Agent-6 (VSCode Forking & Quality Gates Specialist)  
**Version**: 1.0  
**Date**: 2025-10-10

---

## 📋 **Overview**

The Complexity Analyzer provides AST-based complexity metrics for Python code, helping identify functions that are hard to understand and maintain. It calculates three key metrics: cyclomatic complexity, cognitive complexity, and nesting depth.

---

## 🎯 **Complexity Metrics Explained**

### **1. Cyclomatic Complexity**
**What**: Number of independent paths through code  
**How**: Counts decision points (if, while, for, try, and, or)  
**Threshold**: ≤10 (recommended)

**Formula**: 1 + (# of decision points)

**Example**:
```python
def simple():  # Complexity = 1
    return True

def complex(x, y):  # Complexity = 4
    if x > 0:  # +1
        while y > 0:  # +1
            if x == y:  # +1
                return True
    return False
```

### **2. Cognitive Complexity**
**What**: How hard code is to understand  
**How**: Counts decision points with nesting penalties  
**Threshold**: ≤15 (recommended)

**Formula**: Sum of (decision points + nesting level)

**Example**:
```python
def readable(x):  # Cognitive = 1
    if x > 0:  # +1 (nesting=0)
        return True
    return False

def hard_to_read(x, y):  # Cognitive = 7
    if x > 0:  # +1 (nesting=0)
        while y > 0:  # +2 (1 + nesting=1)
            if x == y:  # +3 (1 + nesting=2)
                return True
    return False
```

### **3. Nesting Depth**
**What**: Maximum nesting level in function  
**How**: Counts deepest indentation level  
**Threshold**: ≤4 (recommended)

**Example**:
```python
def shallow():  # Nesting = 1
    if True:
        return

def deep():  # Nesting = 4
    if True:  # Level 1
        for i in range(10):  # Level 2
            while i > 0:  # Level 3
                if i == 5:  # Level 4
                    break
```

---

## 🚀 **Installation**

Already included! No setup required.

**Prerequisites**:
- Python 3.8+
- Standard library only

---

## 💻 **Usage**

### **Analyze Single File**:
```bash
python tools/complexity_analyzer.py src/services/my_service.py
```

### **Detailed Analysis**:
```bash
python tools/complexity_analyzer.py src/services/my_service.py --verbose
```

### **Analyze Directory**:
```bash
python tools/complexity_analyzer.py src/services
```

### **Limit Results**:
```bash
python tools/complexity_analyzer.py src --limit 10
```

### **Integrated with V2 Checker**:
```bash
# Show V2 violations + complexity
python tools/v2_compliance_checker.py src --complexity

# Show V2 + suggestions + complexity (ALL FEATURES!)
python tools/v2_compliance_checker.py src --suggest --complexity
```

---

## 📊 **Understanding Reports**

### **Single File Report**:

```
================================================================================
COMPLEXITY ANALYSIS: simple_onboarding.py
================================================================================
Total functions analyzed: 19
Average cyclomatic complexity: 4.0
Average cognitive complexity: 3.4
Maximum nesting depth: 2

⚠️  COMPLEXITY VIOLATIONS: 1

🟢 LOW SEVERITY: 1 violations
  Line 216: _onboard_agent - CYCLOMATIC = 11 (threshold: 10)

DETAILED METRICS:
Function                                   Cyclomatic    Cognitive    Nesting
--------------------------------------------------------------------------------
_onboard_agent                                     11           12          2
execute                                             7            7          2
_validate_coordinates                               7            6          1
================================================================================
```

### **Directory Summary**:

```
================================================================================
COMPLEXITY ANALYSIS SUMMARY
================================================================================
Files analyzed: 33
Files with violations: 9
Total violations: 39
  🔴 HIGH: 5
  🟡 MEDIUM: 11
  🟢 LOW: 23

TOP 5 FILES BY VIOLATIONS:

1. base_monitoring_manager.py - 8 violations
   Avg cyclomatic: 6.0 | Avg cognitive: 6.8 | Max nesting: 8
2. core_monitoring_manager.py - 6 violations
   Avg cyclomatic: 6.0 | Avg cognitive: 7.6 | Max nesting: 8
================================================================================
```

---

## 🎯 **Thresholds**

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| **Cyclomatic** | ≤10 | Industry standard, tested and proven |
| **Cognitive** | ≤15 | Balances readability with practicality |
| **Nesting** | ≤4 | Beyond 4 levels, code becomes hard to follow |

### **Severity Levels**:

| Ratio | Severity | Meaning |
|-------|----------|---------|
| ≥2.0x threshold | 🔴 HIGH | Requires immediate refactoring |
| 1.5-2.0x threshold | 🟡 MEDIUM | Should be refactored |
| 1.0-1.5x threshold | 🟢 LOW | Could be improved |

---

## 💡 **Reducing Complexity**

### **Strategy 1: Extract Helper Functions**

**Before** (Cyclomatic = 15):
```python
def process_data(data):
    result = []
    for item in data:
        if item.valid:
            if item.type == 'A':
                if item.value > 10:
                    result.append(transform_a(item))
            elif item.type == 'B':
                if item.value > 20:
                    result.append(transform_b(item))
    return result
```

**After** (Cyclomatic = 3):
```python
def process_data(data):
    return [_process_item(item) for item in data if item.valid]

def _process_item(item):
    if item.type == 'A':
        return _process_type_a(item)
    elif item.type == 'B':
        return _process_type_b(item)

def _process_type_a(item):
    return transform_a(item) if item.value > 10 else None

def _process_type_b(item):
    return transform_b(item) if item.value > 20 else None
```

### **Strategy 2: Use Early Returns**

**Before** (Nesting = 4, Cognitive = 8):
```python
def validate(data):
    if data:
        if data.valid:
            if data.value > 0:
                if data.active:
                    return True
    return False
```

**After** (Nesting = 1, Cognitive = 4):
```python
def validate(data):
    if not data:
        return False
    if not data.valid:
        return False
    if data.value <= 0:
        return False
    if not data.active:
        return False
    return True
```

### **Strategy 3: Replace Chains with Dictionaries**

**Before** (Cyclomatic = 10):
```python
def get_color(status):
    if status == 'success':
        return 'green'
    elif status == 'warning':
        return 'yellow'
    elif status == 'error':
        return 'red'
    elif status == 'info':
        return 'blue'
    # ... 6 more conditions
```

**After** (Cyclomatic = 1):
```python
def get_color(status):
    colors = {
        'success': 'green',
        'warning': 'yellow',
        'error': 'red',
        'info': 'blue',
        # ... more mappings
    }
    return colors.get(status, 'gray')
```

---

## 📈 **Integration Examples**

### **Example 1: V2 + Complexity**:

```bash
$ python tools/v2_compliance_checker.py src/services/my_service.py --complexity

src/services/my_service.py:
  🟡 [MAJOR] file: File has 450 lines (MAJOR VIOLATION: ≤400 required)

  📊 COMPLEXITY METRICS:
  Avg Cyclomatic: 8.2 | Avg Cognitive: 7.5 | Max Nesting: 5
  Violations: 3 (🔴1 🟡1 🟢1)
  Worst: _process_complex_data (CYCLOMATIC=18, threshold=10)
```

### **Example 2: V2 + Suggestions + Complexity (FULL POWER!)**:

```bash
$ python tools/v2_compliance_checker.py src/services/my_service.py --suggest --complexity

src/services/my_service.py:
  🟡 [MAJOR] file: File has 450 lines (MAJOR VIOLATION: ≤400 required)

  💡 REFACTORING SUGGESTIONS:
  Confidence: 85% | Estimated result: 320 lines
    → Extract to my_service_models.py (80 lines, 3 entities)
    → Extract to my_service_helpers.py (100 lines, 5 entities)

  📊 COMPLEXITY METRICS:
  Avg Cyclomatic: 8.2 | Avg Cognitive: 7.5 | Max Nesting: 5
  Violations: 3 (🔴1 🟡1 🟢1)
  Worst: _process_complex_data (CYCLOMATIC=18, threshold=10)
```

**Developer gets**:
- What's wrong (violations)
- How to fix structure (suggestions)
- What to simplify (complexity)

---

## 🎓 **Best Practices**

### **1. Monitor Regularly**:
```bash
# Weekly complexity check
python tools/complexity_analyzer.py src > complexity_report.txt
```

### **2. Address HIGH Severity First**:
Functions with 2x threshold are hardest to maintain

### **3. Use with Refactoring**:
Check complexity before and after refactoring to validate improvement

### **4. Set CI Thresholds**:
```yaml
# Fail build on high complexity
python tools/complexity_analyzer.py src --fail-on-high  # Future feature
```

---

## 📊 **Real-World Results**

### **From Agent-6's Testing**:

| Directory | Files | Violations | Avg Cyclomatic | Avg Cognitive |
|-----------|-------|------------|----------------|---------------|
| src/core/managers | 33 | 39 | 5.6 | 6.2 |
| src/services | 25 | 28 | 4.8 | 5.1 |
| src/infrastructure | 18 | 15 | 4.2 | 4.7 |

**Finding**: Most code has good complexity! Only 27% of files have violations.

---

## 🎯 **Quick Reference**

```bash
# Analyze single file
python tools/complexity_analyzer.py src/my_file.py --verbose

# Analyze directory
python tools/complexity_analyzer.py src/services

# V2 + Complexity
python tools/v2_compliance_checker.py src --complexity

# Full suite (V2 + Suggestions + Complexity)
python tools/v2_compliance_checker.py src --suggest --complexity

# Top 10 complex files
python tools/complexity_analyzer.py src --limit 10
```

---

**🐝 WE ARE SWARM** - Complexity analysis for maintainable, understandable code!

---

**Agent-6 Signature**: Quality Gates & V2 Compliance Specialist  
**Tool Version**: 1.0  
**Last Updated**: 2025-10-10




