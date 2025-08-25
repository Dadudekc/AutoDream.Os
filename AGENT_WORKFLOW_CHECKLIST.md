# AGENT WORKFLOW CHECKLIST - AUTOMATED DEVELOPMENT
## Agent Cellphone V2 Repository

---

## 🎯 **OVERVIEW**

This checklist ensures all agents (including AI assistants) follow proper workflows, maintain code quality, and prevent technical debt. **CLEANUP IS MANDATORY** - agents must clean up after themselves and use existing architecture.

---

## 🧹 **MANDATORY CLEANUP REQUIREMENTS**

### **After Every Task/Operation:**
- ✅ **Delete temporary files** created during development
- ✅ **Remove duplicate documents** (check for existing files first)
- ✅ **Clean up test artifacts** and temporary outputs
- ✅ **Update documentation** to reflect changes
- ✅ **Remove old/outdated files** that are no longer needed
- ✅ **Consolidate similar documents** into single sources of truth

### **Document Cleanup Rules:**
- **NEVER create duplicate documents** - check existing files first
- **ALWAYS search before creating** - use `file_search` and `grep_search`
- **Consolidate related information** into single documents
- **Delete old versions** when creating new unified documents
- **Maintain single source of truth** for each topic

---

## 🏗️ **ARCHITECTURE USAGE REQUIREMENTS**

### **MANDATORY - Use Existing Architecture:**
- ✅ **FSM System**: Use `src/core/fsm_core_v2.py` for state tracking
- ✅ **Contract System**: Use `contracts/` directory for task management
- ✅ **Standards Checker**: Use `tests/v2_standards_checker_simple.py`
- ✅ **Pre-commit Hooks**: Use `.pre-commit-config.yaml`
- ✅ **Existing Utilities**: Use `src/utils/` and `tools/` directories

### **NEVER Reinvent:**
- ❌ Don't create new state management systems
- ❌ Don't create new compliance checkers
- ❌ Don't create new task management systems
- ❌ Don't duplicate existing functionality

---

## 📏 **MONOLITHIC FILE HANDLING**

### **When Encountering Large Files (>400 LOC):**
1. **Check if file should be exempted** (test files, demos, etc.)
2. **Use existing contract system** in `contracts/` directory
3. **Follow modularization patterns** established in the project
4. **Extract logical components** into separate modules
5. **Maintain single responsibility principle**

### **Modularization Rules:**
- **Core Business Logic**: Extract into `src/core/` modules
- **Utilities**: Extract into `src/utils/` modules
- **Services**: Extract into `src/services/` modules
- **Tests**: Keep comprehensive tests together (exemptions apply)
- **Demos**: Keep complete workflows together (exemptions apply)

---

## 🔄 **DUPLICATION PREVENTION**

### **Before Creating New Code:**
1. **Search existing codebase** for similar functionality
2. **Check `src/` directory** for existing implementations
3. **Look in `tools/` directory** for utility functions
4. **Check `examples/` directory** for similar patterns
5. **Use existing base classes** and interfaces

### **Code Reuse Requirements:**
- **Inherit from existing classes** when possible
- **Use existing utility functions** instead of rewriting
- **Extend existing interfaces** rather than creating new ones
- **Follow established patterns** in the codebase
- **Reference existing examples** for guidance

---

## 🤖 **FSM INTEGRATION REQUIREMENTS**

### **State Tracking for All Operations:**
- ✅ **Create FSM tasks** for all major operations
- ✅ **Update task states** as work progresses
- ✅ **Track compliance progress** in FSM system
- ✅ **Monitor contract execution** via FSM
- ✅ **Log all state transitions** for audit trail

### **FSM Usage Pattern:**
```python
# Create task
task_id = fsm_core.create_task(
    title="Modularize Core System File",
    description="Extract modules from large file",
    assigned_agent="agent_id",
    priority=TaskPriority.HIGH
)

# Update progress
fsm_core.update_task_state(
    task_id=task_id,
    new_state=TaskState.IN_PROGRESS,
    agent_id="agent_id",
    summary="Started module extraction"
)

# Complete task
fsm_core.update_task_state(
    task_id=task_id,
    new_state=TaskState.COMPLETED,
    agent_id="agent_id",
    summary="Successfully modularized file"
)
```

---

## 📋 **WORKFLOW CHECKLIST FOR EVERY TASK**

### **Pre-Task Checklist:**
- [ ] **Search existing codebase** for similar functionality
- [ ] **Check existing architecture** for relevant components
- [ ] **Review coding standards** (400/600/400 LOC limits)
- [ ] **Check compliance status** for affected areas
- [ ] **Create FSM task** for tracking progress
- [ ] **Plan cleanup strategy** for after completion

### **During Task Checklist:**
- [ ] **Use existing utilities** and base classes
- [ ] **Follow established patterns** in the codebase
- [ ] **Update FSM task state** as progress is made
- [ ] **Document decisions** and architectural choices
- [ ] **Test incremental changes** to ensure stability

### **Post-Task Checklist:**
- [ ] **Delete temporary files** and artifacts
- [ ] **Remove duplicate documents** created during task
- [ ] **Update existing documentation** to reflect changes
- [ ] **Consolidate related information** into single sources
- [ ] **Update FSM task** to completed status
- [ ] **Verify compliance** with coding standards
- [ ] **Clean up test artifacts** and temporary outputs

---

## 🚨 **COMPLIANCE ENFORCEMENT**

### **Standards Compliance:**
- **Line Count Limits**: 400 LOC for standard/core files, 600 LOC for GUI
- **Quality Standards**: OOP, SRP, CLI interfaces, smoke tests
- **Architecture Compliance**: Use existing FSM, contract, and utility systems
- **Documentation Standards**: Single source of truth, no duplicates

### **Compliance Checking:**
```bash
# Run standards checker
python tests/v2_standards_checker_simple.py --all

# Check pre-commit hooks
pre-commit run --all-files

# Verify FSM state
python -c "from src.core.fsm_core_v2 import FSMCoreV2; print('FSM Status:', FSMCoreV2.status)"
```

---

## 🔍 **SEARCH AND DISCOVERY TOOLS**

### **Before Creating New Code:**
```bash
# Search for existing functionality
codebase_search "similar functionality description"

# Find existing files
file_search "filename_pattern"

# Search for specific text
grep_search "function_name_or_pattern"

# List directory contents
list_dir "directory_path"
```

### **Architecture Discovery:**
- **Check `src/core/`** for core functionality
- **Check `src/utils/`** for utility functions
- **Check `tools/`** for specialized tools
- **Check `examples/`** for usage patterns
- **Check `contracts/`** for task definitions

---

## 📊 **PROGRESS TRACKING**

### **FSM State Updates:**
- **NEW**: Task created, not yet started
- **IN_PROGRESS**: Work has begun
- **REVIEW**: Code review or testing phase
- **COMPLETED**: Task finished successfully
- **FAILED**: Task encountered errors
- **CANCELLED**: Task was cancelled

### **Compliance Tracking:**
- **Current Status**: 93.0% compliance
- **Target**: 97.2% compliance
- **Files Over 400 LOC**: 73 remaining
- **Phase 3 Ready**: 44 files to modularize

---

## 🎯 **AUTOMATED DEVELOPMENT GOALS**

### **Short-term (Next 7 weeks):**
- **Week 1-2**: Core system modularization (25 files)
- **Week 3-4**: Services modularization (23 files)
- **Week 5-6**: Web & testing modularization (20 files)
- **Week 7**: Final cleanup and verification

### **Long-term Goals:**
- **100% Architecture Compliance**: Use existing systems only
- **Zero Duplication**: No duplicate code or documents
- **Automated Compliance**: Self-maintaining codebase
- **FSM-Driven Development**: All work tracked via state machine

---

## 📝 **AGENT RESPONSIBILITIES**

### **Every Agent Must:**
1. **Clean up after themselves** - mandatory requirement
2. **Use existing architecture** - never reinvent
3. **Prevent duplication** - search before creating
4. **Track progress via FSM** - maintain state visibility
5. **Follow coding standards** - maintain compliance
6. **Consolidate information** - single source of truth

### **Quality Assurance:**
- **Self-review** all code before submission
- **Verify compliance** with standards
- **Test functionality** before marking complete
- **Document decisions** for future reference
- **Update FSM state** for transparency

---

## 🔄 **CONTINUOUS IMPROVEMENT**

### **Feedback Loop:**
- **Monitor FSM states** for bottlenecks
- **Track compliance metrics** for trends
- **Identify architectural gaps** for improvement
- **Update workflow checklist** based on learnings
- **Share best practices** across all agents

### **Success Metrics:**
- **Compliance percentage** increasing over time
- **FSM task completion** rate improving
- **Duplicate code** eliminated
- **Architecture usage** consistent
- **Cleanup compliance** 100%

---

## 📋 **QUICK REFERENCE**

### **Essential Commands:**
```bash
# Standards compliance
python tests/v2_standards_checker_simple.py --all

# FSM status
python -c "from src.core.fsm_core_v2 import FSMCoreV2; print('Status:', FSMCoreV2.status)"

# Search codebase
codebase_search "search_term"

# File discovery
file_search "pattern"
```

### **Key Directories:**
- **`src/core/`** - Core functionality and FSM
- **`contracts/`** - Task definitions and progress
- **`tools/`** - Utility functions and tools
- **`examples/`** - Usage patterns and demos

### **Critical Files:**
- **`UNIFIED_CODING_STANDARDS_AND_COMPLIANCE_2024.md`** - Single source of truth
- **`src/core/fsm_core_v2.py`** - State management
- **`.pre-commit-config.yaml`** - Compliance hooks

---

**Remember: CLEANUP IS MANDATORY. Every agent must clean up after themselves and use existing architecture. This ensures the codebase remains maintainable and compliant as we move to automated development.**
