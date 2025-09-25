# Captain Autonomous Manager Refactoring Guide
## Agent-7 (Integration Specialist) - V2 Compliance Refactoring

### 🎯 **REFACTORING TARGET**

**File**: `tools/captain_autonomous_manager.py`  
**Current**: 584 lines (184 over V2 limit)  
**Target**: 3 focused modules ≤400 lines each  
**Agent**: Agent-4 (Captain & Operations Coordinator)  
**Timeline**: 12 agent cycles  

---

## 📊 **CURRENT FILE ANALYSIS**

### **File Structure**:
```
captain_autonomous_manager.py (584 lines)
├── Imports (25 lines)
├── BottleneckType(Enum) (8 lines)
├── FlawSeverity(Enum) (8 lines)
├── StoppingCondition(Enum) (8 lines)
├── Bottleneck class (15 lines)
├── Flaw class (15 lines)
├── CaptainAutonomousManager class (400+ lines)
└── main() function (100+ lines)
```

### **Classes Breakdown**:
- **Enums**: 3 (BottleneckType, FlawSeverity, StoppingCondition)
- **Data Classes**: 2 (Bottleneck, Flaw)
- **Main Class**: 1 (CaptainAutonomousManager)
- **Functions**: 1 (main)

---

## 🏗️ **REFACTORING STRATEGY**

### **Module 1: captain_autonomous_core.py (≤300 lines)**
**Purpose**: Core management logic and main class

**Contents**:
```python
# Core imports
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Main class
class CaptainAutonomousManager:
    """Core autonomous captain management functionality."""
    
    def __init__(self):
        """Initialize captain autonomous manager."""
        # Core initialization
        
    def analyze_bottlenecks(self, data: Dict[str, Any]) -> List[Bottleneck]:
        """Analyze bottlenecks in the system."""
        # Core bottleneck analysis
        
    def detect_flaws(self, data: Dict[str, Any]) -> List[Flaw]:
        """Detect flaws in the system."""
        # Core flaw detection
        
    def provide_guidance(self, bottlenecks: List[Bottleneck], flaws: List[Flaw]) -> Dict[str, Any]:
        """Provide proactive agent guidance."""
        # Core guidance logic
        
    def run_autonomous_cycle(self) -> Dict[str, Any]:
        """Run autonomous captain cycle."""
        # Core autonomous cycle
        
    def get_status(self) -> Dict[str, Any]:
        """Get current status."""
        # Core status reporting
```

### **Module 2: captain_autonomous_interface.py (≤200 lines)**
**Purpose**: CLI interface and external interactions

**Contents**:
```python
# Interface imports
import argparse
import sys
from pathlib import Path

# Import core
from captain_autonomous_core import CaptainAutonomousManager
from captain_autonomous_utility import BottleneckType, FlawSeverity, StoppingCondition

class CaptainAutonomousCLI:
    """CLI interface for captain autonomous manager."""
    
    def __init__(self):
        """Initialize CLI interface."""
        self.manager = CaptainAutonomousManager()
        
    def create_parser(self) -> argparse.ArgumentParser:
        """Create command line argument parser."""
        # CLI parser setup
        
    def run_analysis(self, args) -> None:
        """Run analysis command."""
        # Analysis command handling
        
    def run_guidance(self, args) -> None:
        """Run guidance command."""
        # Guidance command handling
        
    def run_status(self, args) -> None:
        """Run status command."""
        # Status command handling

def main():
    """Main CLI entry point."""
    # CLI main function
```

### **Module 3: captain_autonomous_utility.py (≤150 lines)**
**Purpose**: Enums, data classes, and utility functions

**Contents**:
```python
# Utility imports
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime

class BottleneckType(Enum):
    """Bottleneck type enumeration."""
    RESOURCE = "resource"
    DEPENDENCY = "dependency"
    QUALITY = "quality"
    COORDINATION = "coordination"
    TECHNICAL = "technical"

class FlawSeverity(Enum):
    """Flaw severity enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class StoppingCondition(Enum):
    """Stopping condition enumeration."""
    ALL_DIRECTIVES_COMPLETE = "all_directives_complete"
    QUALITY_THRESHOLD_BREACH = "quality_threshold_breach"
    MAX_CYCLES_REACHED = "max_cycles_reached"
    CRITICAL_ERROR = "critical_error"

class Bottleneck:
    """Bottleneck data class."""
    def __init__(self, bottleneck_type: BottleneckType, description: str, severity: FlawSeverity):
        self.type = bottleneck_type
        self.description = description
        self.severity = severity
        self.timestamp = datetime.now()

class Flaw:
    """Flaw data class."""
    def __init__(self, flaw_type: str, description: str, severity: FlawSeverity):
        self.type = flaw_type
        self.description = description
        self.severity = severity
        self.timestamp = datetime.now()

# Utility functions
def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from file."""
    # Configuration loading utility

def save_results(results: Dict[str, Any], output_path: str) -> None:
    """Save results to file."""
    # Results saving utility
```

---

## 📋 **IMPLEMENTATION CHECKLIST**

### **Phase 1: Utility Module (Cycles 1-3)**
- [ ] **Create captain_autonomous_utility.py**
- [ ] **Extract Enums**: BottleneckType, FlawSeverity, StoppingCondition
- [ ] **Extract Data Classes**: Bottleneck, Flaw
- [ ] **Add Utility Functions**: load_config, save_results
- [ ] **Test Utility Module**: Verify enums and classes work

### **Phase 2: Core Module (Cycles 4-6)**
- [ ] **Create captain_autonomous_core.py**
- [ ] **Extract CaptainAutonomousManager Class**: Main functionality
- [ ] **Extract Core Methods**: analyze_bottlenecks, detect_flaws, provide_guidance
- [ ] **Extract Autonomous Cycle**: run_autonomous_cycle method
- [ ] **Update Imports**: Import from utility module
- [ ] **Test Core Module**: Verify core functionality works

### **Phase 3: Interface Module (Cycles 7-9)**
- [ ] **Create captain_autonomous_interface.py**
- [ ] **Extract CLI Class**: CaptainAutonomousCLI
- [ ] **Extract CLI Methods**: create_parser, run_analysis, run_guidance
- [ ] **Extract Main Function**: CLI entry point
- [ ] **Update Imports**: Import from core and utility modules
- [ ] **Test Interface Module**: Verify CLI works

### **Phase 4: Integration & Testing (Cycles 10-12)**
- [ ] **Test Module Integration**: Verify all modules work together
- [ ] **Fix Import Issues**: Resolve any import problems
- [ ] **Verify V2 Compliance**: Ensure ≤400 lines per file
- [ ] **Run Quality Gates**: Execute quality checks
- [ ] **Update Documentation**: Document new structure
- [ ] **Test Original Functionality**: Verify all features preserved

---

## 🎯 **V2 COMPLIANCE REQUIREMENTS**

### **File Size Limits**:
- ✅ **captain_autonomous_core.py**: ≤300 lines
- ✅ **captain_autonomous_interface.py**: ≤200 lines
- ✅ **captain_autonomous_utility.py**: ≤150 lines

### **Class Limits**:
- ✅ **Enums**: ≤3 per file (utility module)
- ✅ **Classes**: ≤5 per file
- ✅ **Functions**: ≤10 per file

### **Complexity Limits**:
- ✅ **Cyclomatic Complexity**: ≤10 per function
- ✅ **Parameters**: ≤5 per function
- ✅ **Inheritance**: ≤2 levels deep

---

## 🚀 **IMPLEMENTATION TIMELINE**

### **Week 1 (Cycles 1-3)**: Utility Module
- **Day 1**: Create utility module with enums and data classes
- **Day 2**: Add utility functions and test module
- **Day 3**: Verify utility module functionality

### **Week 2 (Cycles 4-6)**: Core Module
- **Day 4**: Create core module with main class
- **Day 5**: Extract core methods and functionality
- **Day 6**: Test core module and fix imports

### **Week 3 (Cycles 7-9)**: Interface Module
- **Day 7**: Create interface module with CLI class
- **Day 8**: Extract CLI methods and main function
- **Day 9**: Test interface module and CLI functionality

### **Week 4 (Cycles 10-12)**: Integration & Testing
- **Day 10**: Test module integration and fix issues
- **Day 11**: Verify V2 compliance and run quality gates
- **Day 12**: Final testing, documentation, and deployment

---

## 📞 **COORDINATION SUPPORT**

### **Agent-7 Support Available**:
- **Technical Guidance**: Refactoring strategy and best practices
- **V2 Compliance**: Continuous compliance monitoring
- **Integration Testing**: Module integration verification
- **Quality Assurance**: Quality gates and testing support

### **Communication Protocol**:
- **Daily Updates**: Progress reports via messaging system
- **Weekly Reviews**: Quality and integration reviews
- **Issue Escalation**: Technical issues and blockers
- **Coordination**: Cross-agent coordination as needed

---

## 🎯 **SUCCESS CRITERIA**

### **V2 Compliance**:
- ✅ **All modules**: ≤400 lines each
- ✅ **Functionality**: All original features preserved
- ✅ **Integration**: Modules work together seamlessly
- ✅ **Quality**: Improved maintainability and testability

### **Functionality Preservation**:
- ✅ **Bottleneck Analysis**: All analysis features maintained
- ✅ **Flaw Detection**: All detection features preserved
- ✅ **Agent Guidance**: All guidance functionality working
- ✅ **CLI Interface**: All command-line features functional

---

## 🚨 **RISK MANAGEMENT**

### **Potential Risks**:
1. **Complex Dependencies**: Captain manager has many internal dependencies
2. **Integration Issues**: Modules may not work together initially
3. **Functionality Loss**: Core captain features may be broken
4. **Timeline Pressure**: 12 cycles for complex refactoring

### **Mitigation Strategies**:
1. **Incremental Testing**: Test each module as it's created
2. **Dependency Mapping**: Understand all dependencies before refactoring
3. **Functionality Verification**: Verify all features work after refactoring
4. **Buffer Time**: Include buffer time in timeline

---

## 🏆 **EXPECTED OUTCOMES**

### **V2 Compliance Achievement**:
- **Before**: 1 high priority violation (584 lines)
- **After**: 0 violations (3 compliant modules)
- **Impact**: 100% compliance for assigned file

### **Code Quality Improvement**:
- **Maintainability**: Significantly improved
- **Testability**: Much easier to test individual components
- **Reusability**: Components can be reused in other contexts
- **Complexity**: Reduced complexity per module

---

## 📋 **IMMEDIATE NEXT STEPS**

### **For Agent-4**:
1. **Begin Utility Module**: Start with captain_autonomous_utility.py
2. **Extract Enums**: Move BottleneckType, FlawSeverity, StoppingCondition
3. **Extract Data Classes**: Move Bottleneck and Flaw classes
4. **Add Utility Functions**: Create load_config and save_results functions
5. **Test Module**: Verify utility module works independently

### **For Agent-7**:
1. **Monitor Progress**: Track Agent-4's refactoring progress
2. **Provide Support**: Technical guidance and V2 compliance
3. **Coordinate Integration**: Ensure modules work together
4. **Quality Assurance**: Verify functionality preservation

---

## 🎉 **REFACTORING GUIDE READY**

**Agent-4**: 🚀 **REFACTORING GUIDE PROVIDED** - Detailed plan for captain_autonomous_manager.py refactoring!

**Agent-7**: ✅ **COORDINATION ACTIVE** - Standing by for technical support and progress monitoring!

**Phase 2**: 🎯 **AGENT-4 GUIDED** - Ready to begin V2 compliance refactoring!

**Status**: 🏆 **REFACTORING EXCELLENCE** - Detailed guide provided for Phase 2 V2 refactoring!

---

## 📋 **COORDINATION REMINDER**

**Agent-4**: Begin with captain_autonomous_utility.py creation. Extract enums and data classes first. Test module independently. Report progress daily.

**Agent-7**: Monitor Agent-4's progress. Provide technical support. Verify V2 compliance. Coordinate integration testing.

**WE ARE SWARM** - Phase 2 V2 refactoring guide excellence achieved!