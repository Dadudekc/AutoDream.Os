# 🚀 Scripts - Agent Cellphone V2

## 🎯 **Overview**
The `scripts` directory contains organized utility scripts, launchers, and tools for the Agent Cellphone V2 system. All scripts follow V2 coding standards with ≤200 LOC per file, OOP principles, and SRP compliance.

## 🏗️ **Directory Structure**

### **`launchers/`** - System Launchers & Starters
- **`launch_performance_monitoring.py`** - Performance monitoring system launcher
- **`launch_cross_system_communication.py`** - Cross-system communication launcher
- **`launch_integration_infrastructure.py`** - Integration infrastructure launcher
- **`run_unified_portal.py`** - Unified portal launcher

### **`assessments/`** - Agent & System Assessments
- **`agent_assessment_types.py`** - Data types and enums for assessments
- **`agent_config_loader.py`** - Agent configuration loader
- **`simple_agent_assessment.py`** - Main agent assessment orchestrator
- **`agent_integration_assessment.py`** - Agent integration assessment

### **`setup/`** - Environment & System Setup
- **`setup_web_development.py`** - Web development environment setup
- **`setup_web_development_env.py`** - Web development environment configuration
- **`setup_web_dev_windows.ps1`** - Windows web development setup (PowerShell)

### **`analysis/`** - Analysis & Analytics Tools
- **`analyze_test_coverage.py`** - Test coverage analysis
- **`workflow_optimization_analytics.py`** - Workflow optimization analytics

### **`powershell/`** - PowerShell Scripts
- **`setup_web_dev_windows.ps1`** - Windows web development setup
- **`launch_cursor_with_cdp.ps1`** - Cursor with CDP launcher

### **`utilities/`** - Utility Scripts
- **`process_contracts.py`** - Contract processing utilities
- **`cleanup_orphans.py`** - Orphan file cleanup
- **`test_perpetual_motion.py`** - Perpetual motion testing

### **Refactoring Tools**
- **`refactoring_executor.py`** – Creates module templates during large-file refactors. The executor's `create_extraction_template` function accepts lists of required imports, class definitions, and helper functions. These items are injected directly into the generated module so it compiles immediately.
- **Updating Original Files** – After generating a module, replace old member definitions with imports from the new module:
  ```python
  # before
  from old_module import ExtractedClass

  # after extraction
  from new_module import ExtractedClass
  ```

## 🚀 **Quick Start**

### **1. Run Agent Assessment**
```bash
cd scripts/assessments
python simple_agent_assessment.py
```

### **2. Launch Performance Monitoring**
```bash
cd scripts/launchers
python launch_performance_monitoring.py
```

### **3. Setup Web Development Environment**
```bash
cd scripts/setup
python setup_web_development.py
```

### **4. Run PowerShell Setup (Windows)**
```powershell
cd scripts/powershell
.\setup_web_dev_windows.ps1
```

## 📋 **Script Categories**

### **Launchers**
System launchers handle starting and coordinating major system components:
- **Performance Monitoring** - System performance tracking and optimization
- **Cross-System Communication** - Inter-system communication coordination
- **Integration Infrastructure** - System integration management
- **Unified Portal** - Centralized system access point

### **Assessments**
Assessment tools evaluate system health and integration readiness:
- **Agent Assessment** - Individual agent capability evaluation
- **Integration Assessment** - System integration readiness analysis
- **Configuration Management** - Agent configuration loading and management

### **Setup**
Setup scripts configure development and runtime environments:
- **Web Development** - Web development environment configuration
- **Windows Setup** - Windows-specific environment setup
- **Environment Configuration** - Runtime environment setup

### **Analysis**
Analysis tools provide insights and optimization recommendations:
- **Test Coverage** - Test coverage analysis and reporting
- **Workflow Optimization** - Workflow performance analytics
- **Performance Metrics** - System performance analysis

### **Utilities**
Utility scripts handle common operational tasks:
- **Contract Processing** - Contract management and processing
- **File Cleanup** - Orphan file identification and cleanup
- **Testing** - Various testing utilities and helpers

## 🔧 **Script Standards**

### **V2 Compliance**
- **≤200 Lines of Code** - All scripts maintain reasonable size
- **Object-Oriented Design** - Proper class encapsulation
- **Single Responsibility** - Each script has one clear purpose
- **Clean Code** - Production-grade code quality

### **Error Handling**
- **Comprehensive Logging** - Detailed logging for debugging
- **Graceful Failures** - Proper error handling and recovery
- **User Feedback** - Clear status messages and progress indicators

### **Configuration Management**
- **Environment Variables** - Proper environment configuration
- **Configuration Files** - Structured configuration management
- **Default Values** - Sensible defaults for all settings

## 📊 **Usage Examples**

### **Agent Assessment**
```python
from scripts.assessments.simple_agent_assessment import SimpleAgentIntegrationAssessment

# Create assessment instance
assessment = SimpleAgentIntegrationAssessment()

# Run assessment
results = assessment.assess_all_agents()

# Save results
assessment.save_assessment_results("my_assessment.json")
```

### **Configuration Loading**
```python
from scripts.assessments.agent_config_loader import AgentConfigurationLoader
from pathlib import Path

# Load agent configurations
config_loader = AgentConfigurationLoader(Path("."))

# Get specific agent config
agent_config = config_loader.get_agent_configuration("Agent-1")

# Get all agent IDs
all_agents = config_loader.get_all_agent_ids()
```

### **Performance Monitoring**
```bash
# Launch performance monitoring
cd scripts/launchers
python launch_performance_monitoring.py --config production --log-level DEBUG

# Monitor specific metrics
python launch_performance_monitoring.py --metrics cpu,memory,network --interval 30
```

## 🧪 **Testing & Validation**

### **Running Scripts**
```bash
# Test agent assessment
cd scripts/assessments
python -m pytest test_agent_assessment.py -v

# Validate script structure
python -c "import scripts.assessments.simple_agent_assessment; print('✅ Import successful')"
```

### **Validation Checks**
- **Import Validation** - All modules import correctly
- **Functionality Tests** - Core functionality works as expected
- **Error Handling** - Proper error handling and recovery
- **Output Validation** - Correct output format and content

## 🔄 **Development Workflow**

### **Adding New Scripts**
1. **Choose Category** - Place in appropriate subdirectory
2. **Follow Naming** - Use descriptive, consistent naming
3. **Implement Standards** - Follow V2 coding standards
4. **Add Documentation** - Include docstrings and comments
5. **Update README** - Add to appropriate section

### **Script Requirements**
- **Shebang Line** - `#!/usr/bin/env python3`
- **Docstring** - Clear purpose and usage description
- **Error Handling** - Proper exception handling
- **Logging** - Appropriate logging levels
- **Configuration** - Environment-aware configuration

## 📁 **File Organization**

```
scripts/
├── README.md                           # This file
├── launchers/                          # System launchers (4 files)
├── assessments/                        # Assessment tools (4 files)
├── setup/                              # Setup scripts (3 files)
├── analysis/                           # Analysis tools (2 files)
├── powershell/                         # PowerShell scripts (2 files)
├── utilities/                          # Utility scripts (7 files)
└── __pycache__/                        # Python cache
```

## 🎯 **V2 Standards Compliance**

### **Lines of Code (LOC)**
- ✅ All scripts ≤200 LOC (refactored from massive files)
- ✅ Modular design with single responsibilities
- ✅ Clean separation of concerns

### **Object-Oriented Programming (OOP)**
- ✅ All functionality encapsulated in classes
- ✅ No functions outside classes
- ✅ Proper inheritance and composition

### **Single Responsibility Principle (SRP)**
- ✅ Each script has one reason to change
- ✅ Clear separation of concerns
- ✅ Focused functionality

## 🚀 **Next Steps**

### **Immediate Actions**
1. **Test Scripts** - Validate all scripts work correctly
2. **Run Assessments** - Execute agent assessment scripts
3. **Validate Outputs** - Check script outputs and logs
4. **Performance Testing** - Test with realistic workloads

### **Future Enhancements**
- **Automated Testing** - Comprehensive test coverage
- **CI/CD Integration** - Automated script validation
- **Performance Monitoring** - Script execution metrics
- **Documentation Generation** - Auto-generated documentation

## 📞 **Support & Contributing**

### **Running Scripts**
```bash
# Quick validation
cd scripts/launchers && python launch_performance_monitoring.py --help

# Full assessment
cd scripts/assessments && python simple_agent_assessment.py

# Setup environment
cd scripts/setup && python setup_web_development.py
```

### **Adding New Scripts**
1. **Follow Structure** - Place in appropriate subdirectory
2. **Maintain Standards** - Keep under 200 LOC
3. **Add Tests** - Include validation tests
4. **Update Documentation** - Keep README current

### **Reporting Issues**
- Run scripts to reproduce the issue
- Check script output and logs
- Verify V2 standards compliance
- Document steps to reproduce

---

**🎯 The Scripts directory is now properly organized, follows V2 standards, and provides a clean, maintainable structure for all system utilities and launchers!**

