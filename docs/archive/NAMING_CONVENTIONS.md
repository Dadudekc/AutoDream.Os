# SSOT System Naming Conventions

This document establishes the official naming conventions for the SSOT (Single Source of Truth) system to ensure consistency, maintainability, and clarity across all components.

## 📋 **File Naming Conventions**

### **Core System Files**
- **Canonical implementations**: `{system_name}.py` (e.g., `ssot_execution_coordinator.py`)
- **Supporting modules**: `{system_name}_{component}.py` (e.g., `ssot_validation_models.py`)
- **Legacy/deprecated files**: `{system_name}_{status}.py` (e.g., `ssot_execution_coordinator_legacy.py`)

### **File Status Suffixes**
- `_v2.py` - V2 compliant implementations
- `_refactored.py` - Refactored versions
- `_legacy.py` - Legacy/deprecated implementations
- `_deprecated.py` - Marked for removal
- `_backup.py` - Backup copies

### **Component-Specific Naming**
- **Models**: `{system}_models.py`
- **Handlers**: `{system}_handlers.py`
- **Utils**: `{system}_utils.py`
- **Tests**: `{system}_tests.py`
- **Factory**: `{system}_factory.py`

## 🏗️ **Class Naming Conventions**

### **Main System Classes**
- **Primary classes**: `{SystemName}` (e.g., `SSOTExecutionCoordinator`)
- **Supporting classes**: `{SystemName}{Component}` (e.g., `SSOTValidationSystem`)
- **Handler classes**: `{Component}Handler` (e.g., `TaskExecutionHandler`)
- **Model classes**: `{Component}Model` or descriptive names (e.g., `ExecutionTask`)

### **Interface Classes**
- **Abstract base classes**: `Abstract{ClassName}` (e.g., `AbstractSSOTComponent`)
- **Interface classes**: `{ClassName}Interface` (e.g., `ValidationInterface`)

## 🔧 **Function and Method Naming**

### **Public Methods**
- **Action methods**: `verb_noun` (e.g., `execute_task`, `validate_integration`)
- **Getter methods**: `get_{noun}` (e.g., `get_execution_status`)
- **Setter methods**: `set_{noun}` (e.g., `set_validation_level`)
- **Boolean methods**: `is_{condition}` or `has_{condition}` (e.g., `is_initialized`)

### **Private Methods**
- **Internal methods**: `_{verb_noun}` (e.g., `_execute_task_function`)
- **Helper methods**: `_{action}` (e.g., `_get_unified_logger`)

### **Factory Functions**
- **Create functions**: `create_{class_name}` (e.g., `create_ssot_execution_coordinator`)
- **Get singleton functions**: `get_{class_name}` (e.g., `get_ssot_execution_coordinator`)

## 📊 **Variable Naming Conventions**

### **Instance Variables**
- **System components**: `{component_name}` (e.g., `task_manager`, `coordination_manager`)
- **Status variables**: `{status}_status` (e.g., `execution_status`, `validation_status`)
- **Configuration**: `config` or `{system}_config`

### **Local Variables**
- **Temporary variables**: `{descriptive_name}` (e.g., `execution_result`, `validation_report`)
- **Loop variables**: `{item}` (e.g., `task`, `result`, `report`)

## 🎯 **Constants and Enums**

### **Enum Classes**
- **Status enums**: `{System}Status` (e.g., `ExecutionStatus`, `ValidationStatus`)
- **Type enums**: `{System}Type` (e.g., `ComponentType`, `ValidationLevel`)
- **Phase enums**: `{System}Phase` (e.g., `ExecutionPhase`)

### **Enum Values**
- **UPPER_CASE** with descriptive names (e.g., `PENDING`, `RUNNING`, `COMPLETED`)
- **Use underscores** for multi-word values (e.g., `SYSTEM_VALIDATION`)

## 📁 **Directory Structure**

### **Core System Structure**
```
src/core/ssot/
├── ssot_execution_coordinator.py      # Canonical coordinator
├── ssot_validation_system_core.py     # Canonical validation
├── ssot_coordination_manager.py       # Coordination management
├── ssot_integration_coordinator.py    # Integration management
├── execution_coordination_models.py   # Execution models
├── execution_coordination_handlers.py # Execution handlers
├── validation_models.py               # Validation models
├── validation_handlers.py             # Validation handlers
├── ssot_types.py                      # Common types and enums
├── ssot_factory.py                    # Factory functions
└── tests/                             # Test files
    ├── test_execution_coordinator.py
    ├── test_validation_system.py
    └── test_integration.py
```

## 🚫 **Deprecated Naming Patterns**

### **Avoid These Patterns**
- ❌ `{system}_{system}_{component}.py` (redundant)
- ❌ `{system}__{component}.py` (double underscores)
- ❌ `{system}_{number}.py` (version numbers in filenames)
- ❌ `{system}_{date}.py` (dates in filenames)

### **Legacy File Handling**
- **Mark deprecated files** with `_deprecated.py` suffix
- **Add deprecation warnings** in docstrings
- **Create migration guides** for deprecated functionality
- **Remove deprecated files** after migration period

## 📝 **Documentation Conventions**

### **File Headers**
```python
#!/usr/bin/env python3
"""
{System Name} - {Brief Description}

{Detailed description of purpose and functionality}

Features:
- Feature 1
- Feature 2
- Feature 3

Author: {Agent Name} ({Role})
Version: {Version} - {Status}
License: MIT
"""
```

### **Class Docstrings**
```python
class ClassName:
    """
    {Brief description of the class}.

    {Detailed description of functionality and purpose}.

    Features:
    - Feature 1
    - Feature 2

    Example:
        >>> instance = ClassName()
        >>> result = instance.method()
    """
```

### **Method Docstrings**
```python
def method_name(self, param1: Type, param2: Type) -> ReturnType:
    """
    {Brief description of what the method does}.

    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2

    Returns:
        Description of return value

    Raises:
        ExceptionType: Description of when this exception is raised
    """
```

## 🔄 **Migration Guidelines**

### **When Renaming Files**
1. **Create new file** with correct naming
2. **Add deprecation warning** to old file
3. **Update all imports** to use new file
4. **Test thoroughly** before removing old file
5. **Remove old file** after migration period

### **When Renaming Classes**
1. **Create alias** in old file pointing to new class
2. **Add deprecation warning** to old class
3. **Update all references** to use new class name
4. **Remove old class** after migration period

## ✅ **Compliance Checklist**

Before creating or modifying SSOT system files, ensure:

- [ ] File name follows naming conventions
- [ ] Class names are descriptive and consistent
- [ ] Method names follow verb_noun pattern
- [ ] Private methods are prefixed with underscore
- [ ] Constants and enums use UPPER_CASE
- [ ] Documentation follows established patterns
- [ ] Deprecated files are properly marked
- [ ] Migration path is documented

## 📚 **Examples**

### **Good Examples**
```python
# File: ssot_execution_coordinator.py
class SSOTExecutionCoordinator:
    def execute_task(self, task_id: str) -> ExecutionResult:
        """Execute a specific task."""
        pass

    def _get_unified_logger(self):
        """Get unified logger instance."""
        pass

# File: validation_models.py
class ValidationResult(Enum):
    PASSED = "passed"
    FAILED = "failed"
    PENDING = "pending"
```

### **Bad Examples**
```python
# File: ssot_execution_coordinator_v2_refactored.py (too verbose)
class SSOTExecutionCoordinatorV2Refactored:  # too verbose
    def ExecuteTask(self, taskId: str):  # wrong case, no return type
        pass

    def getUnifiedLogger(self):  # wrong case for private method
        pass
```

---

**Last Updated**: 2025-01-27
**Version**: 1.0.0
**Maintained by**: Agent-3 (Infrastructure & DevOps Specialist)
