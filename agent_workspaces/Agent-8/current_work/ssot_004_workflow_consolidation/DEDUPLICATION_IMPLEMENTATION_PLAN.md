# 🚀 DEDUPLICATION IMPLEMENTATION PLAN
## SSOT-004: Workflow & Reporting System Consolidation - Phase 2

**Contract ID:** SSOT-004  
**Title:** Workflow & Reporting System Consolidation  
**Agent:** Agent-8 (Integration Enhancement Optimization Manager)  
**Status:** IMPLEMENTATION PLAN READY  
**Priority:** CRITICAL - IMMEDIATE EXECUTION REQUIRED  

---

## 📋 **IMPLEMENTATION OVERVIEW**

This plan provides **step-by-step execution details** for eliminating 200+ duplicate implementations across the codebase. Each phase includes specific file operations, code consolidation strategies, and validation steps.

**Total Expected Impact:** 15,000+ lines of code eliminated, 100+ duplicate files removed

---

## 🎯 **PHASE 1: CRITICAL CONSOLIDATION (Week 1)**

### **DAY 1-2: VALIDATOR CONSOLIDATION**

#### **Step 1.1: Create Unified BaseValidator**
**Target:** `src/core/validation/base_validator.py`
**Consolidate:** 4 duplicate implementations (800+ lines eliminated)

**Actions:**
1. **Analyze all duplicate implementations:**
   ```bash
   # Files to analyze:
   - src/core/validation/base_validator.py (253 lines)
   - src/core/base/base_validator.py (350 lines)
   - src/core/validation/validators/base_validator.py
   - tools/modularizer/validation_manager.py
   ```

2. **Create unified implementation:**
   ```python
   # src/core/validation/base_validator.py
   class BaseValidator(ABC):
       """Unified base class for all validators"""
       
       def __init__(self, validator_name: str):
           self.validator_name = validator_name
           self.validation_rules = {}
           self.validation_history = []
           self._load_rules_from_file()
       
       @abstractmethod
       def validate(self, data: Any, **kwargs) -> List[ValidationResult]:
           """Main validation method - must be implemented by subclasses"""
           pass
       
       # ... consolidated methods from all implementations
   ```

3. **Update all imports:**
   ```bash
   # Find all files importing BaseValidator
   grep -r "from.*BaseValidator" src/ --include="*.py"
   grep -r "import.*BaseValidator" src/ --include="*.py"
   
   # Update imports to use unified version
   sed -i 's|from.*base_validator import BaseValidator|from src.core.validation.base_validator import BaseValidator|g' src/**/*.py
   ```

#### **Step 1.2: Create Unified ConfigLoader**
**Target:** `src/core/config/loader.py`
**Consolidate:** 4 duplicate implementations (400+ lines eliminated)

**Actions:**
1. **Analyze all duplicate implementations:**
   ```bash
   # Files to analyze:
   - config/config_loader.py (64 lines)
   - src/utils/config_loader.py (213 lines)
   - src/core/config_loader.py
   - src/core/config_manager_loader.py
   ```

2. **Create unified implementation:**
   ```python
   # src/core/config/loader.py
   class ConfigLoader:
       """Unified configuration loader for all config types"""
       
       def __init__(self, config_dir: str = "config"):
           self.config_dir = Path(config_dir)
           self.config_cache = {}
       
       def load_yaml(self, filename: str) -> Dict[str, Any]:
           """Load YAML configuration file"""
           # ... consolidated implementation
       
       def load_json(self, filename: str) -> Dict[str, Any]:
           """Load JSON configuration file"""
           # ... consolidated implementation
       
       def get_config(self, key_path: str, default: Any = None) -> Any:
           """Get configuration value using dot notation"""
           # ... consolidated implementation
   ```

3. **Update all imports:**
   ```bash
   # Find all files importing ConfigLoader
   grep -r "from.*ConfigLoader" src/ --include="*.py"
   grep -r "import.*ConfigLoader" src/ --include="*.py"
   
   # Update imports to use unified version
   sed -i 's|from.*config_loader import ConfigLoader|from src.core.config.loader import ConfigLoader|g' src/**/*.py
   ```

### **DAY 3-4: TASK MANAGEMENT CONSOLIDATION**

#### **Step 1.3: Create Unified TaskManager**
**Target:** `src/core/task_management/task_manager.py`
**Consolidate:** 4 duplicate implementations (1000+ lines eliminated)

**Actions:**
1. **Analyze all duplicate implementations:**
   ```bash
   # Files to analyze:
   - src/core/workflow/managers/task_manager.py (320 lines)
   - src/core/task_manager.py (556 lines)
   - src/core/workflow/managers/workflow_manager.py
   - src/fsm/core/workflows/workflow_manager.py
   ```

2. **Create unified implementation:**
   ```python
   # src/core/task_management/task_manager.py
   class TaskManager(BaseManager):
       """Unified task management system"""
       
       def __init__(self, workspace_manager):
           super().__init__(
               manager_id="task_manager",
               name="Unified Task Manager",
               description="Orchestrates all task management functionality"
           )
           
           # Initialize specialized components
           self.scheduler = TaskScheduler(workspace_manager)
           self.executor = TaskExecutor()
           self.monitor = TaskMonitor(workspace_manager)
           self.recovery = TaskRecovery(workspace_manager)
           
           # Consolidated task storage
           self.tasks = {}
           self.workflow_tasks = {}
           self.contract_tasks = {}
       
       # ... consolidated methods from all implementations
   ```

3. **Update all imports:**
   ```bash
   # Find all files importing TaskManager
   grep -r "from.*TaskManager" src/ --include="*.py"
   grep -r "import.*TaskManager" src/ --include="*.py"
   
   # Update imports to use unified version
   sed -i 's|from.*task_manager import TaskManager|from src.core.task_management.task_manager import TaskManager|g' src/**/*.py
   ```

### **DAY 5-7: MANAGER HIERARCHY CONSOLIDATION**

#### **Step 1.4: Create Unified Manager Base Classes**
**Target:** `src/core/managers/base/`
**Consolidate:** 15+ duplicate implementations (2000+ lines eliminated)

**Actions:**
1. **Create unified manager hierarchy:**
   ```python
   # src/core/managers/base/base_manager.py
   class BaseManager(ABC):
       """Unified base class for all managers"""
       
       def __init__(self, manager_id: str, name: str, description: str):
           self.manager_id = manager_id
           self.name = name
           self.description = description
           self.status = ManagerStatus.INITIALIZING
           self.start_time = None
           self.performance_metrics = {}
       
       @abstractmethod
       def start(self) -> bool:
           """Start the manager - must be implemented by subclasses"""
           pass
       
       @abstractmethod
       def stop(self) -> bool:
           """Stop the manager - must be implemented by subclasses"""
           pass
       
       # ... consolidated lifecycle management methods
   ```

2. **Create specialized manager base classes:**
   ```python
   # src/core/managers/base/workflow_manager.py
   class BaseWorkflowManager(BaseManager):
       """Base class for workflow-related managers"""
       
       def __init__(self, manager_id: str, name: str, description: str):
           super().__init__(manager_id, name, description)
           self.workflows = {}
           self.workflow_history = []
       
       # ... consolidated workflow management methods
   
   # src/core/managers/base/reporting_manager.py
   class BaseReportingManager(BaseManager):
       """Base class for reporting-related managers"""
       
       def __init__(self, manager_id: str, name: str, description: str):
           super().__init__(manager_id, name, description)
           self.reports = {}
           self.report_templates = {}
       
       # ... consolidated reporting management methods
   ```

3. **Update all manager imports:**
   ```bash
   # Find all files importing manager classes
   grep -r "class.*Manager" src/ --include="*.py" | grep -v "BaseManager"
   
   # Update imports to use unified versions
   sed -i 's|from.*manager import|from src.core.managers.base.base_manager import|g' src/**/*.py
   ```

---

## 🎯 **PHASE 2: HIGH PRIORITY CONSOLIDATION (Week 2)**

### **DAY 1-3: REPORTING SYSTEM CONSOLIDATION**

#### **Step 2.1: Create Unified Reporting Framework**
**Target:** `src/core/reporting/`
**Consolidate:** 25+ duplicate implementations (3000+ lines eliminated)

**Actions:**
1. **Create unified reporting structure:**
   ```python
   # src/core/reporting/base_reporter.py
   class BaseReporter(BaseManager):
       """Unified base class for all reporters"""
       
       def __init__(self, reporter_id: str, name: str, description: str):
           super().__init__(reporter_id, name, description)
           self.reports = {}
           self.templates = {}
           self.formatters = {}
       
       @abstractmethod
       def generate_report(self, data: Any, **kwargs) -> Dict[str, Any]:
           """Generate report - must be implemented by subclasses"""
           pass
       
       # ... consolidated reporting methods
   ```

2. **Create specialized reporters:**
   ```python
   # src/core/reporting/testing_reporter.py
   class TestingReporter(BaseReporter):
       """Unified testing reporter"""
       
       def __init__(self):
           super().__init__(
               reporter_id="testing_reporter",
               name="Unified Testing Reporter",
               description="Consolidated testing reporting functionality"
           )
       
       # ... consolidated testing reporting methods
   
   # src/core/reporting/performance_reporter.py
   class PerformanceReporter(BaseReporter):
       """Unified performance reporter"""
       
       def __init__(self):
           super().__init__(
               reporter_id="performance_reporter",
               name="Unified Performance Reporter",
               description="Consolidated performance reporting functionality"
           )
       
       # ... consolidated performance reporting methods
   ```

3. **Update all reporting imports:**
   ```bash
   # Find all files importing reporter classes
   grep -r "from.*reporter" src/ --include="*.py"
   grep -r "import.*reporter" src/ --include="*.py"
   
   # Update imports to use unified versions
   sed -i 's|from.*reporter import|from src.core.reporting|g' src/**/*.py
   ```

### **DAY 4-7: UTILITY CONSOLIDATION**

#### **Step 2.2: Create Unified Utility Framework**
**Target:** `src/core/utils/`
**Consolidate:** 20+ duplicate implementations (2000+ lines eliminated)

**Actions:**
1. **Create unified utility structure:**
   ```python
   # src/core/utils/base_utils.py
   class BaseUtils:
       """Unified base class for utility functions"""
       
       @staticmethod
       def safe_import(module_name: str, class_name: str = None):
           """Safely import module or class"""
           # ... consolidated implementation
       
       @staticmethod
       def validate_path(path: str) -> bool:
           """Validate file or directory path"""
           # ... consolidated implementation
       
       # ... other consolidated utility methods
   ```

2. **Create specialized utility modules:**
   ```python
   # src/core/utils/validation_utils.py
   class ValidationUtils(BaseUtils):
       """Unified validation utilities"""
       
       @staticmethod
       def validate_email(email: str) -> bool:
           """Validate email format"""
           # ... consolidated implementation
       
       @staticmethod
       def validate_url(url: str) -> bool:
           """Validate URL format"""
           # ... consolidated implementation
       
       # ... other consolidated validation methods
   ```

3. **Update all utility imports:**
   ```bash
   # Find all files importing utility classes
   grep -r "from.*utils" src/ --include="*.py"
   grep -r "import.*utils" src/ --include="*.py"
   
   # Update imports to use unified versions
   sed -i 's|from.*utils import|from src.core.utils|g' src/**/*.py
   ```

---

## 🎯 **PHASE 3: MEDIUM PRIORITY CONSOLIDATION (Week 3)**

### **DAY 1-4: MODEL AND TYPE CONSOLIDATION**

#### **Step 3.1: Create Unified Data Models**
**Target:** `src/core/models/`
**Consolidate:** 32 duplicate implementations (2500+ lines eliminated)

**Actions:**
1. **Create unified model structure:**
   ```python
   # src/core/models/base_models.py
   from dataclasses import dataclass, field
   from datetime import datetime
   from typing import Any, Dict, List, Optional
   
   @dataclass
   class BaseModel:
       """Unified base model for all data structures"""
       
       id: str
       created_at: datetime = field(default_factory=datetime.now)
       updated_at: Optional[datetime] = None
       metadata: Dict[str, Any] = field(default_factory=dict)
       
       def update(self, **kwargs):
           """Update model fields"""
           for key, value in kwargs.items():
               if hasattr(self, key):
                   setattr(self, key, value)
           self.updated_at = datetime.now()
   ```

2. **Create specialized model categories:**
   ```python
   # src/core/models/workflow_models.py
   @dataclass
   class WorkflowModel(BaseModel):
       """Unified workflow data model"""
       
       name: str
       description: str
       status: str
       steps: List[Dict[str, Any]] = field(default_factory=list)
       dependencies: List[str] = field(default_factory=list)
       
       # ... consolidated workflow model fields
   
   # src/core/models/reporting_models.py
   @dataclass
   class ReportModel(BaseModel):
       """Unified report data model"""
       
       title: str
       content: str
       report_type: str
       format: str
       generated_at: datetime = field(default_factory=datetime.now)
       
       # ... consolidated report model fields
   ```

3. **Update all model imports:**
   ```bash
   # Find all files importing model classes
   grep -r "from.*models" src/ --include="*.py"
   grep -r "import.*models" src/ --include="*.py"
   
   # Update imports to use unified versions
   sed -i 's|from.*models import|from src.core.models|g' src/**/*.py
   ```

#### **Step 3.2: Create Unified Type System**
**Target:** `src/core/types/`
**Consolidate:** 15+ duplicate implementations (1000+ lines eliminated)

**Actions:**
1. **Create unified type structure:**
   ```python
   # src/core/types/base_types.py
   from enum import Enum
   from typing import Any, Dict, List, Optional, Union
   
   class BaseStatus(Enum):
       """Unified status enumeration"""
       PENDING = "pending"
       IN_PROGRESS = "in_progress"
       COMPLETED = "completed"
       FAILED = "failed"
       CANCELLED = "cancelled"
   
   class BasePriority(Enum):
       """Unified priority enumeration"""
       LOW = "low"
       MEDIUM = "medium"
       HIGH = "high"
       CRITICAL = "critical"
       EMERGENCY = "emergency"
   ```

2. **Create specialized type categories:**
   ```python
   # src/core/types/workflow_types.py
   class WorkflowStatus(BaseStatus):
       """Workflow-specific status values"""
       BLOCKED = "blocked"
       SUSPENDED = "suspended"
       ARCHIVED = "archived"
   
   class WorkflowType(Enum):
       """Workflow type enumeration"""
       SEQUENTIAL = "sequential"
       PARALLEL = "parallel"
       CONDITIONAL = "conditional"
       LOOP = "loop"
   
   # src/core/types/reporting_types.py
   class ReportFormat(Enum):
       """Report format enumeration"""
       JSON = "json"
       YAML = "yaml"
       XML = "xml"
       HTML = "html"
       PDF = "pdf"
       CSV = "csv"
   ```

3. **Update all type imports:**
   ```bash
   # Find all files importing type classes
   grep -r "from.*types" src/ --include="*.py"
   grep -r "import.*types" src/ --include="*.py"
   
   # Update imports to use unified versions
   sed -i 's|from.*types import|from src.core.types|g' src/**/*.py
   ```

---

## 🔧 **MIGRATION AND VALIDATION TOOLS**

### **Automated Migration Scripts**

#### **Script 1: Import Update Script**
```python
#!/usr/bin/env python3
"""Automated import update script for deduplication"""

import os
import re
from pathlib import Path

def update_imports(directory: str, old_import: str, new_import: str):
    """Update import statements across codebase"""
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                update_file_imports(file_path, old_import, new_import)

def update_file_imports(file_path: Path, old_import: str, new_import: str):
    """Update imports in a single file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update from imports
    content = re.sub(
        rf'from\s+{re.escape(old_import)}\s+import',
        f'from {new_import} import',
        content
    )
    
    # Update direct imports
    content = re.sub(
        rf'import\s+{re.escape(old_import)}',
        f'import {new_import}',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    # Example usage
    update_imports("src/", "src.core.validation.base_validator", "src.core.validation.base_validator")
```

#### **Script 2: Duplicate Detection Script**
```python
#!/usr/bin/env python3
"""Automated duplicate detection script"""

import os
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple

def detect_duplicates(directory: str) -> Dict[str, List[str]]:
    """Detect duplicate files by content hash"""
    
    file_hashes = {}
    duplicates = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                content_hash = hash_file_content(file_path)
                
                if content_hash in file_hashes:
                    if content_hash not in duplicates:
                        duplicates[content_hash] = [file_hashes[content_hash]]
                    duplicates[content_hash].append(str(file_path))
                else:
                    file_hashes[content_hash] = str(file_path)
    
    return duplicates

def hash_file_content(file_path: Path) -> str:
    """Generate hash of file content"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Normalize content (remove comments, whitespace)
    normalized = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return hashlib.md5(normalized.encode()).hexdigest()

if __name__ == "__main__":
    duplicates = detect_duplicates("src/")
    
    print("Duplicate files detected:")
    for hash_val, files in duplicates.items():
        if len(files) > 1:
            print(f"\nHash: {hash_val}")
            for file in files:
                print(f"  - {file}")
```

### **Validation and Testing**

#### **Test Suite: Consolidation Validation**
```python
#!/usr/bin/env python3
"""Test suite for deduplication validation"""

import unittest
from pathlib import Path
import importlib

class TestDeduplicationValidation(unittest.TestCase):
    """Test that deduplication was successful"""
    
    def test_no_duplicate_base_validators(self):
        """Test that only one BaseValidator exists"""
        
        base_validator_files = list(Path("src/").rglob("*base_validator.py"))
        self.assertEqual(len(base_validator_files), 1, 
                        f"Multiple BaseValidator files found: {base_validator_files}")
    
    def test_no_duplicate_config_loaders(self):
        """Test that only one ConfigLoader exists"""
        
        config_loader_files = list(Path("src/").rglob("*config_loader.py"))
        self.assertEqual(len(config_loader_files), 1,
                        f"Multiple ConfigLoader files found: {config_loader_files}")
    
    def test_unified_imports_work(self):
        """Test that unified imports can be loaded"""
        
        # Test BaseValidator import
        try:
            from src.core.validation.base_validator import BaseValidator
            self.assertTrue(True, "BaseValidator import successful")
        except ImportError as e:
            self.fail(f"BaseValidator import failed: {e}")
        
        # Test ConfigLoader import
        try:
            from src.core.config.loader import ConfigLoader
            self.assertTrue(True, "ConfigLoader import successful")
        except ImportError as e:
            self.fail(f"ConfigLoader import failed: {e}")

if __name__ == "__main__":
    unittest.main()
```

---

## 📊 **PROGRESS TRACKING**

### **Daily Progress Checklist**

#### **Week 1 Checklist:**
- [ ] Day 1-2: Validator consolidation complete
- [ ] Day 3-4: Task management consolidation complete  
- [ ] Day 5-7: Manager hierarchy consolidation complete
- [ ] All imports updated and tested
- [ ] Phase 1 validation tests passing

#### **Week 2 Checklist:**
- [ ] Day 1-3: Reporting system consolidation complete
- [ ] Day 4-7: Utility consolidation complete
- [ ] All imports updated and tested
- [ ] Phase 2 validation tests passing

#### **Week 3 Checklist:**
- [ ] Day 1-4: Model and type consolidation complete
- [ ] All imports updated and tested
- [ ] Phase 3 validation tests passing
- [ ] Complete deduplication validation

### **Success Metrics**
- **Code Reduction:** 15,000+ lines eliminated
- **File Reduction:** 100+ duplicate files removed
- **Import Updates:** 100% of imports updated to unified versions
- **Test Coverage:** 100% of validation tests passing
- **SSOT Compliance:** 100% for all consolidated systems

---

## 🚨 **ROLLBACK PLAN**

### **Emergency Rollback Procedures**

#### **If Critical Issues Arise:**
1. **Immediate Stop:** Halt all deduplication activities
2. **Restore from Backup:** Restore original files from git history
3. **Revert Imports:** Restore original import statements
4. **Investigate Issues:** Analyze what caused the problems
5. **Plan Recovery:** Develop revised approach with lessons learned

#### **Rollback Commands:**
```bash
# Restore specific files from git
git checkout HEAD -- src/core/validation/base_validator.py
git checkout HEAD -- src/core/config/loader.py
git checkout HEAD -- src/core/task_management/task_manager.py

# Restore all changes
git reset --hard HEAD
git clean -fd

# Restore specific commits
git revert <commit-hash>
```

---

**Plan Generated By:** Agent-8 (Integration Enhancement Optimization Manager)  
**Plan Date:** Current Sprint  
**Next Review:** Captain Approval Required  
**Status:** READY FOR EXECUTION
