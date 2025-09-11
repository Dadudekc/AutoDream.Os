# 🔧 **CAPTAIN'S HANDBOOK - CORE SYSTEMS CLI COMMANDS**

## **Advanced Core System Operations**
**V2 Compliance**: Single Source of Truth for all core CLI operations

**Author**: Agent-1 - Integration & Core Systems Specialist
**Last Updated**: 2025-09-09
**Status**: ACTIVE - Complete Core Systems Documentation

---

## 🎯 **OVERVIEW**

The Core Systems CLI provides advanced operations for DRY violation elimination, unified analysis workflows, project analysis, and core system management. These tools enable sophisticated automation and optimization across the entire swarm system.

**Key Components**:
- **DRY Eliminator**: Automated duplicate code elimination system
- **Unified Runner**: Single-entry point for analysis and elimination workflows
- **Project Analyzer**: Comprehensive code analysis and chunked reporting
- **Core Managers**: System-wide management and coordination tools

---

## 🧹 **DRY ELIMINATOR SYSTEM**

### **1. DRY Violation Analysis & Elimination**
```bash
python src/core/dry_eliminator/dry_eliminator_orchestrator.py
```

**Description**: Executes comprehensive DRY (Don't Repeat Yourself) violation elimination across the entire codebase.

**Core Functionality**:
- **Violation Detection**: Identifies duplicate code patterns
- **Automated Refactoring**: Eliminates violations through modular architecture
- **Pattern Recognition**: Learns from successful eliminations
- **V2 Compliance**: Ensures all changes meet architectural standards

**Workflow Process**:
1. **Analysis Phase**: Scans codebase for DRY violations
2. **Pattern Matching**: Identifies elimination opportunities
3. **Refactoring**: Applies modular architecture solutions
4. **Validation**: Ensures V2 compliance and functionality preservation
5. **Documentation**: Updates system documentation

**Success Metrics**:
- **Violation Reduction**: 90%+ duplicate code elimination
- **Modular Architecture**: Single responsibility principle enforcement
- **V2 Compliance**: All modules < 300 lines
- **Functionality Preservation**: 100% backward compatibility

**Example Output**:
```
🚀 Advanced DRY Elimination Started
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Analysis Complete:
   • Violations Found: 247
   • High-Impact Targets: 34
   • Estimated Reduction: 85%

⚡ Elimination Phase:
   • Modules Created: 12
   • Files Refactored: 28
   • Code Reduction: 15,432 lines (67%)
   • V2 Compliance: 100%

✅ Elimination Complete
   • All violations resolved
   • Modular architecture implemented
   • System performance improved by 34%
```

---

## 🔄 **UNIFIED RUNNER SYSTEM**

### **2. Unified Analysis Workflow**
```bash
python run_unified.py --mode advanced-analysis
```

**Description**: Single-entry point for executing advanced analysis workflows across the entire system.

**Available Modes**:
- **`advanced-analysis`**: Comprehensive system analysis
- **`advanced-elimination`**: Advanced DRY violation elimination
- **`comprehensive`**: Full system analysis suite
- **`focused`**: Targeted analysis on specific components
- **`mass`**: Bulk elimination operations

**Advanced Analysis Mode**:
```bash
python run_unified.py --mode advanced-analysis
```
**Features**:
- **Multi-dimensional Analysis**: Code quality, performance, architecture
- **Automated Reporting**: Comprehensive analysis reports
- **Trend Analysis**: Historical comparison and improvement tracking
- **Actionable Insights**: Specific recommendations for optimization

**Advanced Elimination Mode**:
```bash
python run_unified.py --mode advanced-elimination
```
**Features**:
- **Intelligent Elimination**: AI-powered duplicate detection
- **Pattern Learning**: Improves with each elimination cycle
- **Batch Processing**: Handles large-scale refactoring
- **Rollback Capability**: Safe elimination with recovery options

**Comprehensive Mode**:
```bash
python run_unified.py --mode comprehensive
```
**Features**:
- **Full System Scan**: Complete codebase analysis
- **Multi-tool Integration**: Combines multiple analysis tools
- **Performance Benchmarking**: System performance analysis
- **Optimization Recommendations**: Prioritized improvement suggestions

**Example Usage**:
```bash
# Run comprehensive system analysis
python run_unified.py --mode comprehensive

# Execute advanced DRY elimination
python run_unified.py --mode advanced-elimination

# Perform focused analysis on specific directory
python run_unified.py --mode focused --target src/services/
```

---

## 📊 **PROJECT ANALYZER SYSTEM**

### **3. Comprehensive Project Analysis**
```bash
python comprehensive_project_analyzer.py
```

**Description**: Performs detailed analysis of the entire project with chunked reporting for large-scale codebases.

**Core Features**:
- **Chunked Analysis**: Breaks large projects into manageable chunks
- **Comprehensive Metadata**: Detailed file and function analysis
- **Dependency Mapping**: Inter-module relationship analysis
- **Quality Metrics**: Code quality and complexity assessment
- **Performance Analysis**: Execution time and resource usage tracking

**Analysis Categories**:
- **Code Metrics**: Lines of code, complexity, maintainability
- **Structure Analysis**: Import patterns, module organization
- **Quality Assessment**: PEP8 compliance, documentation coverage
- **Performance Profiling**: Memory usage, execution patterns
- **Security Scanning**: Potential security vulnerabilities

**Output Formats**:
- **Chunked Reports**: Analysis results in manageable chunks
- **Summary Reports**: Executive-level project overview
- **Detailed Reports**: Granular analysis with recommendations
- **Trend Reports**: Historical analysis comparison

**Example Command**:
```bash
# Run comprehensive project analysis
python comprehensive_project_analyzer.py

# Analyze specific directory with custom chunk size
python comprehensive_project_analyzer.py --directory src/ --chunk-size 25
```

**Analysis Output Structure**:
```
📊 Comprehensive Project Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Project Overview:
   • Total Files: 1,247
   • Total Lines: 89,432
   • Languages: Python (94%), JavaScript (4%), Other (2%)
   • Analysis Chunks: 12

🔍 Quality Metrics:
   • Average Complexity: 3.2/10
   • Documentation Coverage: 87%
   • Test Coverage: 73%
   • PEP8 Compliance: 91%

⚡ Performance Insights:
   • Largest File: 1,234 lines (refactor recommended)
   • Most Complex Function: 45 complexity points
   • Import Dependencies: 156 unique modules
   • Circular Dependencies: 3 detected (action required)

📋 Recommendations:
   1. Refactor oversized files (>400 lines): 8 files identified
   2. Improve documentation: 12 functions need docstrings
   3. Resolve circular dependencies: 3 import cycles to fix
   4. Consider modular decomposition: 5 large modules identified
```

---

## 🎯 **CORE MANAGEMENT SYSTEMS**

### **4. Core Unified System Manager**
```bash
python src/core/core_unified_system.py
```

**Description**: Unified management interface for all core system operations and configurations.

**Management Areas**:
- **Configuration Management**: System-wide configuration coordination
- **Module Coordination**: Inter-module communication and dependencies
- **Resource Management**: System resource allocation and optimization
- **Health Monitoring**: Core system health and performance tracking

**Key Functions**:
- **System Initialization**: Coordinated startup of all core components
- **Configuration Synchronization**: Ensures consistent system configuration
- **Dependency Resolution**: Manages inter-module dependencies
- **Performance Optimization**: Core system performance tuning

### **5. Core Manager System**
```bash
python src/core/core_manager_system.py
```

**Description**: Advanced system management with intelligent coordination and optimization capabilities.

**Management Features**:
- **Intelligent Coordination**: AI-powered system coordination
- **Resource Optimization**: Dynamic resource allocation
- **Performance Monitoring**: Real-time system performance tracking
- **Automated Optimization**: Self-optimizing system management

**Coordination Capabilities**:
- **Load Balancing**: Intelligent distribution of system load
- **Fault Tolerance**: Automated recovery from system failures
- **Scalability Management**: Dynamic scaling based on demand
- **Performance Tuning**: Continuous system optimization

---

## 🔍 **ANALYSIS & INSPECTION TOOLS**

### **6. Source Directory Analysis**
```bash
python analyze_src_directories.py
```

**Description**: Specialized analysis tool for examining source code directory structures and organization.

**Analysis Features**:
- **Directory Structure**: Comprehensive folder organization analysis
- **File Distribution**: File type and size distribution analysis
- **Import Patterns**: Module import relationship mapping
- **Dependency Analysis**: Inter-directory dependency assessment

### **7. Messaging System Analysis**
```bash
python analyze_messaging_files.py
```

**Description**: Dedicated analysis tool for messaging system components and communication patterns.

**Analysis Areas**:
- **Message Flow**: Communication pattern analysis
- **System Integration**: Messaging system integration assessment
- **Performance Metrics**: Message delivery and processing analysis
- **Error Patterns**: Communication failure analysis

### **8. Onboarding System Analysis**
```bash
python analyze_onboarding_files.py
```

**Description**: Comprehensive analysis of agent onboarding systems and processes.

**Analysis Components**:
- **Onboarding Workflows**: Process efficiency analysis
- **Integration Points**: System integration assessment
- **Documentation Quality**: Onboarding documentation evaluation
- **Success Metrics**: Onboarding success rate analysis

---

## 🏗️ **ARCHITECTURE & DESIGN TOOLS**

### **9. Unified Architecture Core**
```bash
python src/architecture/unified_architecture_core.py
```

**Description**: Core architecture management and design pattern enforcement system.

**Architecture Functions**:
- **Design Pattern Enforcement**: Ensures consistent architectural patterns
- **Modular Architecture**: Maintains clean module boundaries
- **Dependency Management**: Manages architectural dependencies
- **Quality Assurance**: Architectural quality validation

### **10. System Integration Manager**
```bash
python src/architecture/system_integration.py
```

**Description**: Manages system integration points and ensures seamless component interaction.

**Integration Features**:
- **API Management**: Application programming interface coordination
- **Data Flow**: System data flow management and optimization
- **Component Integration**: Seamless component interaction
- **Interface Standardization**: Consistent interface patterns

### **11. Design Patterns Library**
```bash
python src/architecture/design_patterns.py
```

**Description**: Comprehensive design pattern library and application system.

**Pattern Categories**:
- **Creational Patterns**: Object creation pattern management
- **Structural Patterns**: Object composition pattern management
- **Behavioral Patterns**: Object interaction pattern management
- **Architectural Patterns**: System-level architectural patterns

---

## 🔧 **ADVANCED OPERATIONS WORKFLOWS**

### **System Health Check Workflow**
```bash
# 1. Run comprehensive analysis
python run_unified.py --mode comprehensive

# 2. Analyze project structure
python comprehensive_project_analyzer.py

# 3. Check for DRY violations
python src/core/dry_eliminator/dry_eliminator_orchestrator.py

# 4. Generate health report
python src/core/core_unified_system.py --report health
```

### **Optimization Workflow**
```bash
# 1. Analyze current state
python analyze_src_directories.py

# 2. Run advanced analysis
python run_unified.py --mode advanced-analysis

# 3. Execute optimizations
python run_unified.py --mode advanced-elimination

# 4. Validate improvements
python comprehensive_project_analyzer.py
```

### **Architecture Review Workflow**
```bash
# 1. Analyze architecture
python src/architecture/unified_architecture_core.py --analyze

# 2. Check integration points
python src/architecture/system_integration.py --validate

# 3. Review design patterns
python src/architecture/design_patterns.py --audit

# 4. Generate architecture report
python src/architecture/unified_architecture_core.py --report
```

---

## 📋 **COMMAND QUICK REFERENCE**

| System | Primary Command | Key Features | Use Case |
|--------|-----------------|--------------|----------|
| **DRY Eliminator** | `python src/core/dry_eliminator/` | Automated elimination, pattern learning | Code deduplication |
| **Unified Runner** | `python run_unified.py --mode` | Multi-mode analysis, batch processing | Unified workflows |
| **Project Analyzer** | `python comprehensive_project_analyzer.py` | Chunked analysis, quality metrics | Project assessment |
| **Core Manager** | `python src/core/core_manager_system.py` | Intelligent coordination, optimization | System management |
| **Architecture Core** | `python src/architecture/unified_architecture_core.py` | Pattern enforcement, quality assurance | Architecture management |
| **System Integration** | `python src/architecture/system_integration.py` | API management, data flow | Integration management |
| **Source Analysis** | `python analyze_src_directories.py` | Directory structure, import patterns | Code organization |
| **Messaging Analysis** | `python analyze_messaging_files.py` | Message flow, performance metrics | Communication analysis |
| **Onboarding Analysis** | `python analyze_onboarding_files.py` | Workflow efficiency, success metrics | Onboarding optimization |

---

## ⚠️ **SYSTEM REQUIREMENTS & DEPENDENCIES**

### **Core Dependencies**
- **Python 3.8+**: Required for advanced features
- **Analysis Libraries**: AST parsing, code analysis tools
- **File System Access**: Full read/write permissions
- **Memory Requirements**: 2GB+ RAM for large projects
- **Storage Requirements**: Adequate space for analysis reports

### **Optional Enhancements**
- **AI/ML Libraries**: Enhanced pattern recognition
- **Database Integration**: Historical analysis storage
- **Cloud Integration**: Distributed analysis capabilities
- **Visualization Tools**: Graphical analysis reports

---

## 🚨 **TROUBLESHOOTING & MAINTENANCE**

### **Common Issues**

**Issue**: Analysis commands fail with permission errors
**Solution**: Ensure proper file system permissions and user access

**Issue**: Memory errors during large project analysis
**Solution**: Use chunked analysis mode or increase system memory

**Issue**: DRY elimination produces unexpected results
**Solution**: Run analysis first, review patterns before elimination

**Issue**: Architecture analysis shows false positives
**Solution**: Update pattern recognition database and rerun analysis

### **Performance Optimization**
- **Chunked Processing**: Break large operations into smaller chunks
- **Parallel Processing**: Use multiple cores for analysis operations
- **Incremental Analysis**: Analyze only changed files when possible
- **Caching**: Cache analysis results for repeated operations

---

## 📈 **INTEGRATION WITH SWARM OPERATIONS**

### **Captain's Core System Oversight**
- **Daily Analysis**: Run unified analysis daily for system health
- **Weekly Optimization**: Execute DRY elimination weekly
- **Monthly Architecture Review**: Comprehensive architecture assessment
- **Quarterly System Audit**: Full system analysis and optimization

### **Agent Integration Points**
- **Analysis Results**: Agents consume analysis reports for optimization
- **Architecture Guidelines**: Follow core system architectural patterns
- **Quality Standards**: Adhere to core system quality requirements
- **Performance Benchmarks**: Meet core system performance standards

---

**✅ CORE SYSTEMS CLI COMPLETE**
**11 Commands Documented | All Workflows Covered | V2 Compliant**

**Ready for advanced swarm system operations!** 🚀⚡
