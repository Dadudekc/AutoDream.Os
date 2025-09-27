# 🚀 Enhanced Project Scanner Guide

## Overview

The Enhanced Project Scanner is a comprehensive code analysis tool that integrates advanced language analysis, intelligent caching, agent categorization, and swarm intelligence features. It represents a significant upgrade from the basic project scanner with enhanced capabilities for multi-language support and agent system analysis.

## 🎯 Key Enhancements

### 1. **Advanced Language Analysis**
- **Tree-sitter Integration**: AST parsing for Python, Rust, JavaScript, TypeScript
- **Enhanced Route Detection**: Flask, FastAPI, Express.js route extraction
- **Sophisticated AST Analysis**: Deep code structure analysis with metadata
- **Multi-language Support**: Unified analysis across different programming languages

### 2. **Intelligent Caching System**
- **File Movement Detection**: Automatically detects moved/renamed files
- **Hash-based Tracking**: MD5 hash comparison for change detection
- **Cache Optimization**: Skips unchanged files for faster subsequent scans
- **Memory Efficient**: Thread-safe caching with automatic cleanup

### 3. **Agent Categorization & Maturity Assessment**
- **Agent Type Classification**: ActionAgent, DataAgent, SignalAgent, CommunicationAgent, etc.
- **Maturity Levels**: Kiddie Script, Prototype, Core Asset assessment
- **Swarm Intelligence Analysis**: Physical agent positioning and coordination analysis
- **V2 Compliance Monitoring**: Automatic compliance checking and reporting

### 4. **Enhanced Report Generation**
- **Data Merging**: Preserves existing analysis data during updates
- **Modular Reports**: Separate reports for different aspects (agents, architecture, tests)
- **ChatGPT Context**: Enhanced context export for AI assistance
- **Automatic Documentation**: Auto-generates `__init__.py` files for Python packages

## 🛠️ Usage

### Basic Usage

```python
from tools.projectscanner import EnhancedProjectScanner

# Initialize scanner
scanner = EnhancedProjectScanner(project_root=".")

# Run enhanced scan
scanner.scan_project()

# Generate additional outputs
scanner.generate_init_files()
scanner.export_chatgpt_context()
```

### Advanced Usage

```python
from tools.projectscanner import EnhancedProjectScanner

# Initialize with custom settings
scanner = EnhancedProjectScanner(project_root=".")

# Add ignore directories
scanner.add_ignore_directory("temp")
scanner.add_ignore_directory("build")

# Progress callback
def progress_callback(percent: int):
    print(f"Scan progress: {percent}%")

# Run scan with custom parameters
scanner.scan_project(
    progress_callback=progress_callback,
    num_workers=8,
    file_extensions={'.py', '.rs', '.js', '.ts', '.go'}
)

# Get analysis summary
summary = scanner.get_analysis_summary()
print(f"Total files: {summary['total_files']}")
print(f"V2 Compliance: {summary['v2_compliance']['compliance_rate']:.1f}%")
```

### Command Line Interface

```bash
# Basic enhanced scan
python tools/projectscanner/enhanced_scanner.py

# Advanced options
python tools/projectscanner/enhanced_scanner.py \
    --project-root . \
    --ignore temp build logs \
    --workers 8 \
    --extensions .py .rs .js .ts \
    --summary \
    --clear-cache

# Skip certain outputs
python tools/projectscanner/enhanced_scanner.py \
    --no-chatgpt-context \
    --no-init-files
```

## 📊 Output Files

### Core Analysis Files
- `project_analysis.json` - Main analysis results with enhanced metadata
- `test_analysis.json` - Separated test file analysis
- `chatgpt_project_context.json` - Enhanced context for AI assistance
- `dependency_cache.json` - Intelligent caching data

### Enhanced Reports
- `analysis/enhanced_agent_analysis.json` - Agent categorization and swarm analysis
- `analysis/enhanced_architecture_overview.json` - System architecture overview

## 🔍 Analysis Features

### Language-Specific Analysis

#### Python Analysis
```python
{
    "language": ".py",
    "functions": [
        {
            "name": "process_data",
            "line": 42,
            "args": 3,
            "decorators": ["@route", "@cache"]
        }
    ],
    "classes": {
        "DataProcessor": {
            "methods": ["process", "validate", "transform"],
            "docstring": "Processes incoming data...",
            "base_classes": ["BaseProcessor"],
            "maturity": "Core Asset",
            "agent_type": "DataAgent"
        }
    },
    "routes": [
        {
            "function": "process_data",
            "method": "POST",
            "path": "/api/data",
            "line": 42
        }
    ],
    "complexity": 15,
    "file_size": 234,
    "maturity": "Core Asset",
    "agent_type": "DataAgent"
}
```

#### Rust Analysis
```python
{
    "language": ".rs",
    "functions": [
        {
            "name": "calculate_hash",
            "line": 12
        }
    ],
    "structs": {
        "HashCalculator": {
            "line": 8,
            "fields": []
        }
    },
    "impls": {
        "HashCalculator": ["calculate", "verify"]
    },
    "complexity": 8,
    "maturity": "Core Asset",
    "agent_type": "SystemAgent"
}
```

#### JavaScript Analysis
```python
{
    "language": ".js",
    "functions": [
        {
            "name": "handleRequest",
            "line": 15
        }
    ],
    "classes": {
        "APIController": {
            "line": 5,
            "methods": []
        }
    },
    "routes": [
        {
            "object": "app",
            "method": "GET",
            "path": "/api/users",
            "line": 20
        }
    ],
    "complexity": 6,
    "maturity": "Prototype",
    "agent_type": "WebAgent"
}
```

### Agent Categorization

#### Agent Types
- **ActionAgent**: Classes with `run()` or `execute()` methods
- **DataAgent**: Classes focused on data transformation/processing
- **SignalAgent**: Classes with prediction/analysis capabilities
- **CommunicationAgent**: Classes handling messaging/communication
- **MonitoringAgent**: Classes for system monitoring/scanning
- **WebAgent**: Classes handling web requests/routes
- **SystemAgent**: Low-level system functionality
- **UtilityAgent**: General utility functions

#### Maturity Levels
- **Kiddie Script**: Basic scripts with minimal structure
- **Prototype**: Developing code with some structure
- **Core Asset**: Production-ready, well-structured code

### V2 Compliance Monitoring

The enhanced scanner automatically monitors V2 compliance:
- **File Size Limits**: Tracks files exceeding 400 lines
- **Compliance Rate**: Calculates percentage of compliant files
- **Violation Detection**: Identifies files needing refactoring
- **Recommendations**: Suggests improvements for non-compliant code

## 🐝 Swarm Intelligence Features

### Physical Agent Positioning
The scanner analyzes the swarm's physical architecture:
```python
"swarm_coordination": {
    "total_agents": 8,
    "active_agents": 8,
    "coordination_method": "PyAutoGUI automation",
    "physical_positions": {
        "Monitor 1": [(-1269, 481), (-308, 480), (-1269, 1001), (-308, 1000)],
        "Monitor 2": [(652, 421), (1612, 419), (920, 851), (1611, 941)]
    }
}
```

### Agent Distribution Analysis
- Tracks agent types across the codebase
- Monitors agent maturity levels
- Analyzes swarm coordination patterns
- Reports on agent specialization

## 🔧 Configuration

### Cache Management
```python
# Clear cache
scanner.clear_cache()

# Get cache statistics
stats = scanner.get_cache_stats()
print(f"Cache size: {stats['cache_size']}")

# Cache file location
print(f"Cache file: {stats['cache_file']}")
```

### Ignore Directories
```python
# Add ignore directories
scanner.add_ignore_directory("temp")
scanner.add_ignore_directory("build")

# Remove ignore directories
scanner.remove_ignore_directory("temp")

# Default ignored directories
default_ignores = {
    "__pycache__", "node_modules", ".git", ".venv", "venv", "env",
    "build", "dist", "target", "coverage", "htmlcov", ".pytest_cache",
    "migrations", "chrome_profile", "temp", "tmp", "logs"
}
```

## 📈 Performance Optimizations

### Intelligent Caching
- **Hash-based Change Detection**: Only processes changed files
- **File Movement Detection**: Automatically handles moved/renamed files
- **Incremental Updates**: Merges new analysis with existing data
- **Memory Efficient**: Thread-safe caching with automatic cleanup

### Multi-threaded Processing
- **Configurable Workers**: Adjustable number of worker threads
- **Parallel File Processing**: Concurrent analysis of multiple files
- **Progress Tracking**: Real-time progress updates
- **Error Handling**: Graceful handling of processing errors

### Optimized File Discovery
- **Smart Directory Filtering**: Efficient exclusion of irrelevant directories
- **Virtual Environment Detection**: Automatic detection of Python virtual environments
- **Extension-based Filtering**: Configurable file extension filtering
- **Path Optimization**: Efficient file path resolution

## 🚀 Integration with Existing Tools

### Pre-commit Integration
The enhanced scanner integrates seamlessly with the existing pre-commit workflow:

```bash
# Run enhanced scan (used by pre-commit)
python tools/run_project_scan.py
```

### Git Integration
Automatically stages generated artifacts:
- `project_analysis.json`
- `test_analysis.json`
- `chatgpt_project_context.json`
- `dependency_cache.json`
- `analysis/enhanced_agent_analysis.json`
- `analysis/enhanced_architecture_overview.json`

## 🔍 Troubleshooting

### Common Issues

1. **Tree-sitter Not Installed**
   ```
   ⚠️ tree-sitter not installed. Rust/JS/TS AST parsing will be partially disabled.
   ```
   **Solution**: Install tree-sitter for enhanced language support
   ```bash
   pip install tree-sitter
   ```

2. **Cache Corruption**
   ```
   Failed to load cache: JSON decode error
   ```
   **Solution**: Clear the cache
   ```python
   scanner.clear_cache()
   ```

3. **Permission Errors**
   ```
   PermissionError: [Errno 13] Permission denied
   ```
   **Solution**: Check file permissions and ensure write access to output directory

### Performance Issues

1. **Slow Scanning**
   - Increase worker threads: `num_workers=8`
   - Add more ignore directories
   - Use caching to skip unchanged files

2. **Memory Usage**
   - Reduce worker threads
   - Clear cache periodically
   - Process smaller file sets

## 🎯 Best Practices

### 1. Regular Scanning
- Run scans after significant code changes
- Use pre-commit hooks for automatic scanning
- Schedule periodic full scans

### 2. Cache Management
- Clear cache when switching branches
- Monitor cache size and clean up periodically
- Use cache for incremental updates

### 3. Configuration
- Customize ignore directories for your project
- Adjust worker threads based on system resources
- Configure file extensions based on project needs

### 4. Integration
- Use enhanced reports for project documentation
- Export ChatGPT context for AI assistance
- Monitor V2 compliance regularly

## 🚀 Future Enhancements

### Planned Features
- **Additional Language Support**: Go, C++, Java analysis
- **Dependency Graph Analysis**: Import/export relationship mapping
- **Code Quality Metrics**: Cyclomatic complexity, maintainability index
- **Security Analysis**: Vulnerability detection and security scanning
- **Performance Profiling**: Execution time and resource usage analysis

### Swarm Intelligence Evolution
- **Real-time Agent Monitoring**: Live agent status tracking
- **Predictive Analysis**: Agent behavior prediction
- **Optimization Suggestions**: Automatic swarm configuration optimization
- **Collaborative Analysis**: Multi-agent analysis coordination

## 📚 References

- [Tree-sitter Documentation](https://tree-sitter.github.io/tree-sitter/)
- [AST Module Documentation](https://docs.python.org/3/library/ast.html)
- [V2 Compliance Guidelines](../AGENTS.md#v2-compliance)
- [Swarm Architecture Documentation](../AGENTS.md#swarm-physical-architecture)

---

**🐝 WE. ARE. SWARM. Enhanced Project Scanner ready for deployment! ⚡️🔥**


