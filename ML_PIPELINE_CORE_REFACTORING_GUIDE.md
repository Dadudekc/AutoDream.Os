# ML Pipeline Core Refactoring Guide for Agent-4

## Overview
**Target File**: `src/ml/ml_pipeline_core.py` (580 lines)
**Agent**: Agent-4
**Priority**: HIGH (V2 Violation)
**Goal**: Split into 3 V2-compliant modules (≤400 lines each)

## Current File Analysis
- **Total Lines**: 580 (V2 Violation: >400)
- **Classes**: 2 (MLPipelineCore, MLPipelineManager)
- **Functions**: 19
- **Methods**: 18
- **Complexity**: High (ML pipeline logic)

## Refactoring Plan

### 1. ml_pipeline_core.py (≤300 lines)
**Primary Class**: MLPipelineCore
**Responsibilities**:
- Core ML pipeline logic
- Model training and evaluation
- Data processing
- Pipeline execution

**Key Methods**:
- `__init__()`
- `train_model()`
- `evaluate_model()`
- `process_data()`
- `execute_pipeline()`
- `validate_input()`

### 2. ml_pipeline_manager.py (≤200 lines)
**Primary Class**: MLPipelineManager
**Responsibilities**:
- Pipeline management
- Configuration handling
- Resource management
- Error handling

**Key Methods**:
- `__init__()`
- `configure_pipeline()`
- `manage_resources()`
- `handle_errors()`
- `log_pipeline()`
- `cleanup()`

### 3. ml_pipeline_utils.py (≤150 lines)
**Responsibilities**:
- Utility functions
- Helper methods
- Data validation
- Common operations

**Key Methods**:
- `validate_data()`
- `format_results()`
- `parse_config()`
- `calculate_metrics()`
- `save_model()`
- `load_model()`

## Implementation Steps

### Step 1: Extract Core Module
1. Create `src/ml/ml_pipeline_core.py`
2. Move `MLPipelineCore` class
3. Include core ML pipeline logic
4. Add model training and evaluation
5. Ensure ≤300 lines

### Step 2: Extract Manager Module
1. Create `src/ml/ml_pipeline_manager.py`
2. Move `MLPipelineManager` class
3. Include pipeline management
4. Add configuration handling
5. Ensure ≤200 lines

### Step 3: Extract Utils Module
1. Create `src/ml/ml_pipeline_utils.py`
2. Move utility functions
3. Include helper methods
4. Add data validation
5. Ensure ≤150 lines

### Step 4: Update Imports
1. Update all files importing from `ml_pipeline_core.py`
2. Add proper import statements
3. Test compatibility

### Step 5: Validation
1. Run quality gates: `python quality_gates.py`
2. Verify V2 compliance
3. Test functionality
4. Update documentation

## V2 Compliance Requirements
- **File Size**: ≤400 lines (hard limit)
- **Classes**: ≤5 per file
- **Functions**: ≤10 per file
- **Complexity**: ≤10 cyclomatic complexity per function
- **Parameters**: ≤5 per function
- **Inheritance**: ≤2 levels deep

## Quality Gates
- Run `python quality_gates.py` before submission
- Ensure all tests pass
- Verify import compatibility
- Check for circular dependencies

## Success Criteria
- [ ] All 3 modules ≤400 lines
- [ ] V2 compliance verified
- [ ] Functionality preserved
- [ ] Imports updated
- [ ] Tests passing
- [ ] Documentation updated

## Notes
- Maintain backward compatibility
- Preserve all existing functionality
- Follow KISS principle
- Use simple data structures
- Avoid complex inheritance

**Agent-4**: Begin with `ml_pipeline_core.py` extraction. Report progress via messaging system.
