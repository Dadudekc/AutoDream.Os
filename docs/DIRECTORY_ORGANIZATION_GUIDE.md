# 📁 Directory Organization Guide - Agent Cellphone V2

## 🎯 **Purpose**
This guide establishes a clean, organized directory structure to prevent the creation of messy, unorganized directories in the project root.

## 🚫 **What NOT to Do**
- ❌ **NEVER create directories in the project root**
- ❌ **NEVER use hardcoded paths like `"message_data"` or `"test_dashboard"`**
- ❌ **NEVER create temporary directories without cleanup**
- ❌ **NEVER leave test artifacts in the root directory**

## ✅ **What TO Do**
- ✅ **ALWAYS use the organized `data/` structure**
- ✅ **ALWAYS use relative paths from project root**
- ✅ **ALWAYS implement proper cleanup in tests**
- ✅ **ALWAYS use UUID-based unique test directories**

## 🏗️ **Organized Directory Structure**

```
data/
├── test_outputs/          # All test artifacts and temporary files
│   ├── test_abc12345/     # Unique test directories with UUID
│   ├── test_def67890/     # Each test gets its own subdirectory
│   └── ...
├── financial/             # Financial data and analytics
│   ├── market_data/
│   ├── portfolio_data/
│   └── risk_data/
├── communication/         # Message data and inbox
│   ├── inbox/
│   ├── message_history/
│   └── attachments/
├── workspaces/            # Agent workspaces and FSM data
│   ├── agent_workspaces/
│   ├── fsm_data/
│   └── task_data/
└── logs/                  # System logs and monitoring
    ├── application/
    ├── error/
    └── performance/
```

## 🔧 **Implementation Standards**

### **1. Test Directory Creation**
```python
# ❌ WRONG - Creates messy root directories
self.temp_dir = tempfile.mkdtemp()
self.data_dir = Path(self.temp_dir) / "message_data"

# ✅ CORRECT - Uses organized structure
self.temp_dir = Path("data/test_outputs") / f"test_{uuid.uuid4().hex[:8]}"
self.data_dir = self.temp_dir / "communication"
```

### **2. Configuration Files**
```python
# ❌ WRONG - Hardcoded root paths
"inbox_path": "message_data",
"workspace_path": "agent_workspaces"

# ✅ CORRECT - Organized paths
"inbox_path": "data/communication",
"workspace_path": "data/workspaces"
```

### **3. Test Cleanup**
```python
# ❌ WRONG - No cleanup
def setUp(self):
    self.test_dir = tempfile.mkdtemp()

# ✅ CORRECT - Proper cleanup
def setUp(self):
    self.test_dir = Path("data/test_outputs") / f"test_{uuid.uuid4().hex[:8]}"
    self.test_dir.mkdir(parents=True, exist_ok=True)

def tearDown(self):
    if self.test_dir.exists():
        shutil.rmtree(self.test_dir)
```

## 📋 **Required Imports**
```python
import uuid
from pathlib import Path
import shutil
```

## 🧪 **Test File Template**
```python
class TestExample(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Create unique test directory in organized structure
        self.test_dir = Path("data/test_outputs") / f"test_{uuid.uuid4().hex[:8]}"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories as needed
        self.data_dir = self.test_dir / "test_data"
        self.data_dir.mkdir(exist_ok=True)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
```

## 🔍 **Code Review Checklist**
- [ ] No hardcoded root directory paths
- [ ] All test directories use `data/test_outputs/`
- [ ] Proper cleanup implemented in `tearDown()`
- [ ] UUID-based unique directory names
- [ ] Relative paths from project root
- [ ] Configuration files use organized structure

## 🚨 **Common Violations to Watch For**
1. **`tempfile.mkdtemp()`** without cleanup
2. **Hardcoded paths** like `"message_data"`, `"test_dashboard"`
3. **Root directory creation** in tests
4. **Missing cleanup** in test teardown
5. **Absolute paths** instead of relative paths

## 📚 **Examples of Good vs Bad Code**

### **Bad Example:**
```python
# Creates messy root directories
def test_something(self):
    test_dir = Path("test_dashboard")  # ❌ Creates in root
    test_dir.mkdir(exist_ok=True)
    # ... test code ...
    # No cleanup! ❌
```

### **Good Example:**
```python
# Uses organized structure with cleanup
def setUp(self):
    self.test_dir = Path("data/test_outputs") / f"test_{uuid.uuid4().hex[:8]}"
    self.test_dir.mkdir(parents=True, exist_ok=True)

def tearDown(self):
    if self.test_dir.exists():
        shutil.rmtree(self.test_dir)
```

## 🎉 **Benefits of This Approach**
1. **Clean Project Root** - No more messy directories
2. **Organized Data** - Everything has its proper place
3. **Easy Cleanup** - Simple to remove all test artifacts
4. **Team Consistency** - Everyone follows the same pattern
5. **Professional Appearance** - Project looks organized and professional

## 🔄 **Migration Steps**
1. **Update configuration files** to use `data/` paths
2. **Refactor test files** to use organized structure
3. **Add proper cleanup** to all test classes
4. **Remove old messy directories** from root
5. **Update documentation** and team guidelines

---

**Remember: A clean project structure reflects clean code practices! 🧹✨**
