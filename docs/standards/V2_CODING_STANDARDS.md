# 🚀 V2 CODING STANDARDS - COMPREHENSIVE GUIDE

**Document**: V2 Coding Standards and Implementation Guidelines
**Version**: 1.0
**Last Updated**: 2024-08-19
**Author**: Agent-3 (Development Lead)
**Status**: ACTIVE - ENFORCED

---

## 📋 **EXECUTIVE SUMMARY**

This document consolidates all V2 coding standards into one comprehensive, easily accessible reference. The V2 workspace enforces **coding standards focused on clean OOP design, maintainability, and code quality** rather than strict line count limits.

**NEW APPROACH (2024)**: The emphasis is on clean, organized, production-ready code that follows OOP principles, reduces duplication, and leverages existing systems. Line counts are guidelines, not strict rules.

---

## 🏗️ **CORE CODING STANDARDS**

### **1. 📏 LINE COUNT GUIDELINES**
- **Standard Files**: **300 LOC** (Lines of Code) - *Guideline, not strict rule*
- **GUI Components**: **500 LOC** (250 logic + 250 GUI) - *Guideline, not strict rule*
- **Target**: Use as a general guideline for maintainability
- **Enforcement**: **FLEXIBLE** - Refactor based on code quality, not just line count
- **Real Priority**: Clean OOP design, SRP compliance, and maintainability over arbitrary limits

### **2. 🎯 OBJECT-ORIENTED DESIGN (OOP)**
- **All code must be properly OOP** ✅
- **Classes must have clear responsibilities** ✅
- **Proper inheritance and composition** ✅
- **Interface segregation principles** ✅
- **No procedural code without class structure**

### **3. 🔒 SINGLE RESPONSIBILITY PRINCIPLE (SRP)**
- **One class = one responsibility** ✅
- **Clear separation of concerns** ✅
- **No mixed functionality** ✅
- **Focused, purpose-driven classes** ✅
- **Each class should have a single, well-defined purpose**

### **4. 🖥️ CLI INTERFACE REQUIREMENTS**
- **Every module must have CLI interface for testing** ✅
- **Comprehensive argument parsing** ✅
- **Help documentation for all flags** ✅
- **Easy testing for agents** ✅
- **CLI must be the primary testing interface**

### **5. 🧪 SMOKE TESTS**
- **Every component must have working smoke tests** ✅
- **Basic functionality validation** ✅
- **CLI interface testing** ✅
- **Error handling validation** ✅
- **Tests must be simple and comprehensive**

### **6. 🤖 AGENT USABILITY**
- **Agents must be able to easily test everything** ✅
- **Clear CLI interfaces** ✅
- **Comprehensive help systems** ✅
- **Simple testing commands** ✅
- **No complex setup required for testing**

### **7. 🧪 TEST-DRIVEN DEVELOPMENT (TDD)**
- **Every component must have tests or be developed with TDD** ✅
- **Tests ensure code quality and reliability** ✅
- **Prevents regression issues** ✅
- **Improves design through test-first approach** ✅
- **Makes refactoring safer and more confident**

### **8. 🔄 CODE REUSE AND DUPLICATION REDUCTION**
- **Leverage existing systems before creating new ones** ✅
- **Reduce duplication on sight** ✅
- **Design for reuse and composability** ✅
- **Maintain single source of truth for common functionality** ✅
- **Always check for existing solutions first**

---

## 📁 **V2 WORKSPACE STRUCTURE STANDARDS**

### **Required Directory Structure**
```
Agent_Cellphone_V2/
├── src/
│   ├── __init__.py          # Main package with CLI interface ✅
│   ├── core/
│   │   ├── __init__.py      # Core module with CLI interface ✅
│   │   └── *.py            # Core components (≤200 LOC each)
│   ├── services/
│   │   ├── __init__.py      # Services module with CLI interface ✅
│   │   └── *.py            # Service components (≤200 LOC each)
│   ├── launchers/
│   │   ├── __init__.py      # Launchers module with CLI interface ✅
│   │   └── *.py            # Launcher components (≤200 LOC each)
│   └── utils/
│       ├── __init__.py      # Utils module with CLI interface ✅
│       └── *.py            # Utility components (≤200 LOC each)
├── tests/
│   ├── smoke/               # Smoke tests for each component
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── docs/                    # Documentation
├── examples/                # Example usage
└── config/                  # Configuration files
```

### **File Naming Standards**
- **Python Files**: `snake_case.py` (e.g., `fsm_core_v2.py`)
- **Test Files**: `test_<component_name>.py` (e.g., `test_fsm_core_v2.py`)
- **Documentation**: `UPPER_CASE.md` (e.g., `V2_CODING_STANDARDS.md`)

---

## 🔍 **STANDARDS COMPLIANCE CHECKLIST**

### **For Each New Component:**
- [ ] **Line Count**: File ≤ 200 LOC
- [ ] **OOP Design**: Proper class structure with clear responsibilities
- [ ] **Single Responsibility**: One class = one purpose
- [ ] **CLI Interface**: Comprehensive CLI with help and testing
- [ ] **Smoke Tests**: Basic functionality tests included
- [ ] **Agent Usability**: Easy to test and use
- [ ] **Documentation**: Clear docstrings and comments
- [ ] **Error Handling**: Graceful error handling and logging

### **For Each Existing Component:**
- [ ] **Refactor if > 200 LOC**: Break into smaller, focused modules
- [ ] **OOP Compliance**: Ensure proper class structure
- [ ] **SRP Compliance**: Single responsibility per class
- [ ] **CLI Addition**: Add CLI interface if missing
- [ ] **Test Coverage**: Add smoke tests if missing

---

## 📊 **CURRENT STANDARDS COMPLIANCE STATUS**

| Component | OOP Design | LOC Limit | Single Responsibility | CLI Interface | Smoke Tests | Status |
|-----------|------------|-----------|----------------------|---------------|-------------|---------|
| **V2 Structure** | ✅ | ✅ | ✅ | ✅ | ✅ | **COMPLETE** |
| **Core Manager** | ✅ | ✅ | ✅ | ✅ | ✅ | **COMPLETE** |
| **Agent Service** | ✅ | ✅ | ✅ | ✅ | ✅ | **COMPLETE** |
| **FSM V2 System** | ✅ | ✅ | ✅ | ✅ | ✅ | **COMPLETE** |
| **Standalone Scanner** | ✅ | ✅ | ✅ | ✅ | ✅ | **COMPLETE** |
| **Launchers** | 🔄 | 🔄 | 🔄 | 🔄 | ⏳ | **IN PROGRESS** |
| **Utils** | 🔄 | 🔄 | 🔄 | 🔄 | ⏳ | **IN PROGRESS** |
| **Config Manager** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | **PENDING** |
| **Message Router** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | **PENDING** |

**Overall Standards Compliance**: 75% ✅
**Core Components**: 100% ✅
**Remaining Components**: 25% 🔄

---

## 🚨 **STANDARDS ENFORCEMENT RULES**

### **Immediate Actions Required:**
1. **Any file > 200 LOC**: Must be refactored immediately
2. **Missing CLI interface**: Must be added before deployment
3. **Missing smoke tests**: Must be created before deployment
4. **Non-OOP code**: Must be refactored to OOP structure
5. **Mixed responsibilities**: Must be separated into focused classes

### **Approval Process:**
- **Standards violations**: Require Agent-4 (Quality Assurance) approval
- **Exceptions to 200 LOC**: Require Captain approval
- **Architecture changes**: Require Agent-2 (Architecture) approval
- **Deployment**: Requires full standards compliance

---

## 🛠️ **REFACTORING GUIDELINES**

### **When to Refactor (NEW APPROACH):**
1. **SRP Violations**: Multiple responsibilities in one class
2. **High Cognitive Complexity**: Code becomes difficult to understand
3. **Testing Difficulties**: Mixed concerns make testing complex
4. **Code Duplication**: Same logic appears in multiple places
5. **Poor Organization**: Code structure affects maintainability
6. **Line Count**: Only as a secondary consideration, not primary driver

### **Breaking Down Large Files (>200 LOC):**
1. **Identify distinct responsibilities** within the file
2. **Create separate classes** for each responsibility
3. **Maintain single responsibility** per class
4. **Add CLI interfaces** to each new class
5. **Create smoke tests** for each new class
6. **Update imports** and dependencies
7. **Leverage existing systems** to avoid duplication
8. **Implement TDD approach** for new modules

### **Example Refactoring:**
```python
# BEFORE: Large file with mixed responsibilities (400+ LOC)
class LargeManager:
    def manage_users(self): pass
    def manage_files(self): pass
    def manage_database(self): pass
    def manage_network(self): pass

# AFTER: Focused classes (each ≤200 LOC)
class UserManager:  # ≤200 LOC
    def manage_users(self): pass
    # CLI interface + smoke tests

class FileManager:  # ≤200 LOC
    def manage_files(self): pass
    # CLI interface + smoke tests

class DatabaseManager:  # ≤200 LOC
    def manage_database(self): pass
    # CLI interface + smoke tests

class NetworkManager:  # ≤200 LOC
    def manage_network(self): pass
    # CLI interface + smoke tests
```

---

## 🧪 **TESTING STANDARDS**

### **Smoke Test Requirements:**
```python
# Example smoke test structure
def test_basic_functionality():
    """Test basic component functionality"""
    component = Component()
    assert component is not None
    assert component.initialize() is True

def test_cli_interface():
    """Test CLI interface functionality"""
    # Test help command
    # Test basic operations
    # Test error handling

def test_error_handling():
    """Test error handling and edge cases"""
    # Test invalid inputs
    # Test error conditions
    # Test graceful failures
```

### **CLI Interface Requirements:**
```python
# Example CLI interface structure
def main():
    parser = argparse.ArgumentParser(description="Component Description")
    parser.add_argument("--test", action="store_true", help="Run smoke tests")
    parser.add_argument("--operation", type=str, help="Perform operation")

    args = parser.parse_args()

    if args.test:
        run_smoke_tests()
    elif args.operation:
        perform_operation(args.operation)
    else:
        parser.print_help()
```

---

## 📚 **DOCUMENTATION STANDARDS**

### **Code Documentation:**
- **Class docstrings**: Clear description of purpose and responsibility
- **Method docstrings**: Parameters, return values, and usage examples
- **Inline comments**: Complex logic explanations
- **Type hints**: Python type annotations for all functions

### **Example Documentation:**
```python
class FSMCoreV2:
    """
    FSM Core V2 - Single responsibility: Agent coordination via FSM.

    Manages task state transitions and agent coordination.
    Follows V2 standards: ≤200 LOC, OOP design, SRP.
    """

    def create_task(self, title: str, description: str,
                   assigned_agent: str, priority: TaskPriority = TaskPriority.NORMAL,
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new FSM task.

        Args:
            title: Task title
            description: Task description
            assigned_agent: Agent ID assigned to task
            priority: Task priority level
            metadata: Additional task metadata

        Returns:
            str: Task ID if successful, empty string if failed

        Raises:
            ValueError: If required parameters are invalid
        """
```

---

## 🎯 **IMPLEMENTATION CHECKLIST**

### **Before Creating New Components:**
- [ ] **Plan architecture** to ensure ≤200 LOC compliance
- [ ] **Define single responsibility** for each class
- [ ] **Design CLI interface** for testing and usability
- [ ] **Plan smoke tests** for validation
- [ ] **Consider agent usability** requirements

### **During Development:**
- [ ] **Monitor line count** continuously
- [ ] **Maintain single responsibility** per class
- [ ] **Implement CLI interface** as you develop
- [ ] **Write smoke tests** alongside code
- [ ] **Follow OOP best practices**

### **Before Deployment:**
- [ ] **Verify ≤200 LOC compliance** for all files
- [ ] **Test CLI interfaces** thoroughly
- [ ] **Run smoke tests** successfully
- [ ] **Validate OOP design** and SRP compliance
- [ ] **Check agent usability** requirements

---

## 🚀 **SUCCESS METRICS**

### **Standards Compliance Targets:**
- **Line Count**: 100% of files ≤300 LOC (standard), ≤500 LOC (GUI)
- **OOP Design**: 100% OOP compliance
- **Single Responsibility**: 100% SRP compliance
- **CLI Interfaces**: 100% CLI coverage
- **Smoke Tests**: 100% test coverage
- **Agent Usability**: 100% usability compliance

### **Quality Metrics:**
- **Code Maintainability**: High (≤200 LOC, clear structure)
- **Test Coverage**: Comprehensive (smoke tests for all components)
- **Documentation**: Complete (docstrings, comments, examples)
- **Error Handling**: Robust (graceful failures, logging)
- **Performance**: Optimized (efficient algorithms, caching)

---

## 📞 **SUPPORT AND ENFORCEMENT**

### **Standards Enforcement Team:**
- **Agent-4 (Quality Assurance)**: Primary standards enforcement
- **Agent-2 (Architecture)**: Architecture and design standards
- **Agent-3 (Development Lead)**: Development standards and guidance
- **Captain**: Final approval for exceptions

### **Getting Help:**
1. **Check this document** for standards requirements
2. **Review existing V2 components** for examples
3. **Contact Agent-4** for quality assurance questions
4. **Contact Agent-2** for architecture questions
5. **Contact Agent-3** for development guidance

---

## 🔄 **CONTINUOUS IMPROVEMENT**

### **Standards Evolution:**
- **Regular review** of standards effectiveness
- **Agent feedback** incorporation
- **Performance metrics** monitoring
- **Best practices** updates
- **Tooling improvements** for standards enforcement

### **Feedback Loop:**
- **Report standards issues** to enforcement team
- **Suggest improvements** to standards
- **Share best practices** with team
- **Contribute examples** to documentation

---

## 🆕 **UPDATED PHILOSOPHY (2024)**

### **New Approach - Quality Over Quantity:**
The V2 coding standards have evolved to focus on **code quality, maintainability, and clean OOP design** rather than strict line count limits.

### **Real Priorities (In Order):**
1. **Clean OOP Design** - Proper class structure and inheritance
2. **Single Responsibility Principle** - One class, one purpose
3. **Test-Driven Development** - Every component must have tests or be developed with TDD
4. **Code Reuse** - Leverage existing systems and reduce duplication
5. **Maintainability** - Clean, organized, readable code
6. **Line Count** - 300 LOC as a helpful guideline, not a strict rule

### **When to Refactor (Primary Triggers):**
- **SRP violations** (multiple responsibilities in one class)
- **High cognitive complexity** affecting maintainability
- **Testing difficulties** due to mixed concerns
- **Code duplication** that could leverage existing systems
- **Poor organization** affecting readability

---

## 📋 **QUICK REFERENCE**

### **Essential Standards (Must Follow):**
1. **≤300 LOC per file (≤500 for GUI)** - *Guideline, not strict rule*
2. **OOP design** - All code in classes
3. **Single responsibility** - One purpose per class
4. **CLI interface** - Required for all components
5. **Smoke tests** - Required for all components
6. **Agent usability** - Easy to test and use
7. **TDD approach** - Tests for all components
8. **Code reuse** - Leverage existing systems

### **File Structure:**
- **src/core/**: Core system components
- **src/services/**: Service layer components
- **src/launchers/**: System launcher components
- **src/utils/**: Utility components
- **tests/smoke/**: Smoke tests for each component

### **Naming Conventions:**
- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Methods**: `snake_case`
- **Constants**: `UPPER_CASE`
- **Variables**: `snake_case`

---

**V2 CODING STANDARDS: UPDATED AND ACTIVE (2024)**
**NEW APPROACH: Quality over quantity, clean OOP design over strict line limits**
**GUIDELINES: 300 LOC (Standard), 500 LOC (GUI) - Flexible enforcement**
**COMPLIANCE REQUIRED FOR ALL DEVELOPMENT**
**STANDARDS ENFORCEMENT: AGENT-4 (QUALITY ASSURANCE)**
**DEVELOPMENT GUIDANCE: AGENT-3 (DEVELOPMENT LEAD)**
