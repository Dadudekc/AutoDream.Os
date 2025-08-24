# 🛠️ Tools - Agent Cellphone V2

## 🎯 **Overview**
The `tools/` directory contains essential development and analysis tools for the Agent Cellphone V2 system. All tools follow V2 coding standards with ≤200 LOC per file, OOP principles, and SRP compliance.

## 🏗️ **Directory Structure**

### **`duplication/`** - Duplication Detection System
- **`__init__.py`** - Package initialization and exports
- **`duplication_types.py`** - Data types and enums for duplication detection
- **`code_analyzer.py`** - Code analysis and block extraction
- **`duplication_detector.py`** - Main duplication detection orchestrator
- **`duplication_reporter.py`** - Reporting and output generation

### **Essential Tools**
- **`cdp_send_message.py`** - CDP messaging tool for headless communication
- **`launch_cursor_cdp.ps1`** - PowerShell script to launch Cursor with CDP debugging
- **`duplication_detector_main.py`** - Main entry point for duplication detection

## 🚀 **Quick Start**

### **1. Run Duplication Detection**
```bash
cd tools
python duplication_detector_main.py --help
python duplication_detector_main.py . --output report.json
```

### **2. Use CDP Messaging**
```bash
# Test CDP connection
python cdp_send_message.py "Test message"

# Launch Cursor with CDP debugging
.\launch_cursor_cdp.ps1
```

### **3. Import Duplication System**
```python
from tools.duplication import DuplicationDetector, DuplicationReporter

# Create detector
detector = DuplicationDetector()
issues = detector.analyze_codebase(".")

# Generate report
reporter = DuplicationReporter()
report = reporter.generate_report(issues)
```

## 📋 **Tool Categories**

### **Duplication Detection**
Advanced code duplication detection system that identifies:
- **Exact duplicates** - Identical code blocks
- **Similar structures** - Similar function/class patterns
- **Duplicate imports** - Repeated import statements
- **Backup files** - Temporary and backup files
- **Repeated patterns** - Common code patterns

**Features:**
- Configurable similarity thresholds
- Multiple detection algorithms
- Comprehensive reporting
- Actionable recommendations
- JSON output support

### **CDP Communication**
Chrome DevTools Protocol tools for headless communication:
- **CDP Messenger** - Send messages without mouse movement
- **Cursor Launcher** - Launch Cursor with debugging enabled
- **Connection Testing** - Verify CDP connectivity

**Use Cases:**
- Headless agent communication
- Automated testing
- Debugging and monitoring
- Integration testing

## 🔧 **Tool Standards**

### **V2 Compliance**
- **≤200 Lines of Code** - All tools maintain reasonable size
- **Object-Oriented Design** - Proper class encapsulation
- **Single Responsibility** - Each tool has one clear purpose
- **Clean Code** - Production-grade code quality

### **Error Handling**
- **Comprehensive Logging** - Detailed logging for debugging
- **Graceful Failures** - Proper error handling and recovery
- **User Feedback** - Clear status messages and progress indicators

### **Configuration Management**
- **Command Line Arguments** - Flexible configuration options
- **Environment Variables** - Environment-aware configuration
- **Default Values** - Sensible defaults for all settings

## 📊 **Usage Examples**

### **Duplication Detection**
```python
from tools.duplication import DuplicationDetector, DuplicationReporter

# Configure detector
detector = DuplicationDetector(min_similarity=0.8, min_block_size=5)

# Analyze codebase
issues = detector.analyze_codebase("src/")

# Generate report
reporter = DuplicationReporter()
report = reporter.generate_report(issues, total_files=100)

# Display results
reporter.print_report(report)

# Save to file
reporter.save_json_report(report, "duplication_report.json")
```

### **CDP Messaging**
```python
import subprocess

# Test CDP connection
result = subprocess.run([
    "python", "tools/cdp_send_message.py", 
    "Hello from agent!"
], capture_output=True, text=True)

print(result.stdout)
```

### **PowerShell Integration**
```powershell
# Launch Cursor with CDP debugging
cd tools
.\launch_cursor_cdp.ps1

# Check if Cursor is running
Get-Process -Name "Cursor" -ErrorAction SilentlyContinue
```

## 🧪 **Testing & Validation**

### **Running Tools**
```bash
# Test duplication detection
cd tools
python duplication_detector_main.py . --verbose

# Test CDP messaging
python cdp_send_message.py "Test message"

# Test PowerShell launcher
.\launch_cursor_cdp.ps1
```

### **Validation Checks**
- **Import Validation** - All modules import correctly
- **Functionality Tests** - Core functionality works as expected
- **Error Handling** - Proper error handling and recovery
- **Output Validation** - Correct output format and content

## 🔄 **Development Workflow**

### **Adding New Tools**
1. **Choose Category** - Place in appropriate subdirectory
2. **Follow Naming** - Use descriptive, consistent naming
3. **Implement Standards** - Follow V2 coding standards
4. **Add Documentation** - Include docstrings and comments
5. **Update README** - Add to appropriate section

### **Tool Requirements**
- **Shebang Line** - `#!/usr/bin/env python3`
- **Docstring** - Clear purpose and usage description
- **Error Handling** - Proper exception handling
- **Logging** - Appropriate logging levels
- **Configuration** - Environment-aware configuration

## 📁 **File Organization**

```
tools/
├── README.md                           # This file
├── duplication/                        # Duplication detection system
│   ├── __init__.py                     # Package initialization
│   ├── duplication_types.py            # Data types and enums
│   ├── code_analyzer.py                # Code analysis
│   ├── duplication_detector.py         # Main detector
│   └── duplication_reporter.py         # Reporting system
├── duplication_detector_main.py        # Main entry point
├── cdp_send_message.py                 # CDP messaging tool
└── launch_cursor_cdp.ps1               # Cursor launcher
```

## 🎯 **V2 Standards Compliance**

### **Lines of Code (LOC)**
- ✅ All tools ≤200 LOC (refactored from massive files)
- ✅ Modular design with single responsibilities
- ✅ Clean separation of concerns

### **Object-Oriented Programming (OOP)**
- ✅ All functionality encapsulated in classes
- ✅ No functions outside classes
- ✅ Proper inheritance and composition

### **Single Responsibility Principle (SRP)**
- ✅ Each tool has one reason to change
- ✅ Clear separation of concerns
- ✅ Focused functionality

## 🚀 **Next Steps**

### **Immediate Actions**
1. **Test Tools** - Validate all tools work correctly
2. **Run Duplication Detection** - Execute duplication analysis
3. **Validate Outputs** - Check tool outputs and logs
4. **Performance Testing** - Test with realistic workloads

### **Future Enhancements**
- **Automated Testing** - Comprehensive test coverage
- **CI/CD Integration** - Automated tool validation
- **Performance Monitoring** - Tool execution metrics
- **Documentation Generation** - Auto-generated documentation

## 📞 **Support & Contributing**

### **Running Tools**
```bash
# Quick validation
cd tools && python duplication_detector_main.py --help

# Full duplication analysis
python duplication_detector_main.py . --output report.json

# CDP messaging test
python cdp_send_message.py "Test message"
```

### **Adding New Tools**
1. **Follow Structure** - Place in appropriate subdirectory
2. **Maintain Standards** - Keep under 200 LOC
3. **Add Tests** - Include validation tests
4. **Update Documentation** - Keep README current

### **Reporting Issues**
- Run tools to reproduce the issue
- Check tool output and logs
- Verify V2 standards compliance
- Document steps to reproduce

---

**🎯 The Tools directory is now properly organized, follows V2 standards, and provides essential development and analysis capabilities!**
