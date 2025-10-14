# CLI Toolbelt Architecture Design
**Mission:** C-058-2  
**Agent:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-10-11  
**Status:** Architecture Design Complete  
**Deadline:** 2 cycles  

---

## 🎯 MISSION OBJECTIVE

Create unified CLI tool launcher:
```bash
python -m tools.toolbelt --scan           # Run project scanner
python -m tools.toolbelt --v2-check       # Run V2 compliance checker
python -m tools.toolbelt --dashboard      # Open compliance dashboard
python -m tools.toolbelt --help           # Show all available tools
```

---

## 📋 REQUIREMENTS

1. **Unified Entry Point** - Single CLI interface for all tools
2. **Flag-Based Tool Selection** - Simple flags to launch tools
3. **Help System** - Auto-generated help from tool discovery
4. **Tool Discovery** - Automatic detection of available tools

---

## 🏗️ ARCHITECTURE DESIGN

### Core Components

```
tools/
├── toolbelt.py              # Main entry point (NEW)
├── toolbelt_registry.py     # Tool registry & discovery (NEW)
├── toolbelt_runner.py       # Tool execution engine (NEW)
└── toolbelt_help.py         # Help system generator (NEW)
```

### Architecture Diagram

```
User Command
    ↓
python -m tools.toolbelt --scan
    ↓
toolbelt.py (Entry Point)
    ↓
Parse Arguments
    ↓
toolbelt_registry.py (Tool Discovery)
    ↓
Lookup Tool by Flag
    ↓
toolbelt_runner.py (Execution)
    ↓
Run Tool with Original Arguments
    ↓
Return Results
```

---

## 📦 COMPONENT SPECIFICATIONS

### 1. toolbelt.py (Main Entry Point)

**Purpose:** CLI entry point and argument router  
**Lines:** ~80 lines (V2 compliant)

**Responsibilities:**
- Parse command-line arguments
- Display help if no args or --help
- Route to appropriate tool via registry
- Handle errors gracefully

**Interface:**
```python
def main():
    """Main CLI entry point."""
    parser = create_parser()
    args, remaining = parser.parse_known_args()
    
    if args.help or not any tool flag set:
        show_help()
        return 0
    
    tool = registry.get_tool_for_flag(args)
    return runner.execute_tool(tool, remaining)
```

---

### 2. toolbelt_registry.py (Tool Registry)

**Purpose:** Tool discovery and registration  
**Lines:** ~120 lines (V2 compliant)

**Responsibilities:**
- Define available tools and their flags
- Map flags to tool modules
- Provide tool metadata (description, usage)
- Support dynamic tool addition

**Tool Registry Structure:**
```python
TOOLS_REGISTRY = {
    "scan": {
        "name": "Project Scanner",
        "module": "tools.projectscanner",
        "main_function": "main",
        "description": "Scan project structure and generate analysis",
        "flags": ["--scan", "-s"],
        "args_passthrough": True
    },
    "v2-check": {
        "name": "V2 Compliance Checker",
        "module": "tools.v2_checker_cli",
        "main_function": "main",
        "description": "Check V2 compliance violations",
        "flags": ["--v2-check", "--v2", "-v"],
        "args_passthrough": True
    },
    "dashboard": {
        "name": "Compliance Dashboard",
        "module": "tools.compliance_dashboard",
        "main_function": "main",
        "description": "Open compliance tracking dashboard",
        "flags": ["--dashboard", "-d"],
        "args_passthrough": False
    },
    "complexity": {
        "name": "Complexity Analyzer",
        "module": "tools.complexity_analyzer_cli",
        "main_function": "main",
        "description": "Analyze code complexity metrics",
        "flags": ["--complexity", "-c"],
        "args_passthrough": True
    },
    "refactor": {
        "name": "Refactoring Suggestions",
        "module": "tools.refactoring_cli",
        "main_function": "main",
        "description": "Get intelligent refactoring suggestions",
        "flags": ["--refactor", "-r"],
        "args_passthrough": True
    },
    "duplication": {
        "name": "Duplication Analyzer",
        "module": "tools.duplication_analyzer",
        "main_function": "main",
        "description": "Find duplicate code across project",
        "flags": ["--duplication", "--dup"],
        "args_passthrough": True
    },
    "functionality": {
        "name": "Functionality Verification",
        "module": "tools.functionality_verification",
        "main_function": "main",
        "description": "Verify functionality preservation",
        "flags": ["--functionality", "--verify"],
        "args_passthrough": True
    },
    "leaderboard": {
        "name": "Autonomous Leaderboard",
        "module": "tools.autonomous_leaderboard",
        "main_function": "main",
        "description": "Show agent performance leaderboard",
        "flags": ["--leaderboard", "-l"],
        "args_passthrough": True
    },
    "history": {
        "name": "Compliance History",
        "module": "tools.compliance_history_tracker",
        "main_function": "main",
        "description": "Track compliance history over time",
        "flags": ["--history", "-h"],
        "args_passthrough": True
    }
}
```

**Interface:**
```python
class ToolRegistry:
    def get_tool_for_flag(self, flag: str) -> dict | None:
        """Get tool config by flag."""
        
    def list_tools(self) -> list[dict]:
        """List all available tools."""
        
    def get_tool_by_name(self, name: str) -> dict | None:
        """Get tool config by name."""
```

---

### 3. toolbelt_runner.py (Execution Engine)

**Purpose:** Tool execution with proper environment  
**Lines:** ~100 lines (V2 compliant)

**Responsibilities:**
- Import tool modules dynamically
- Execute tool main() function
- Pass through remaining arguments
- Handle execution errors
- Capture and return exit codes

**Interface:**
```python
class ToolRunner:
    def execute_tool(
        self, 
        tool_config: dict, 
        args: list[str]
    ) -> int:
        """
        Execute tool with given arguments.
        
        Args:
            tool_config: Tool configuration from registry
            args: Command-line arguments to pass to tool
            
        Returns:
            Exit code from tool execution
        """
```

**Execution Flow:**
```python
def execute_tool(self, tool_config, args):
    # 1. Import tool module
    module = importlib.import_module(tool_config["module"])
    
    # 2. Get main function
    main_func = getattr(module, tool_config["main_function"])
    
    # 3. Setup sys.argv if args_passthrough
    if tool_config["args_passthrough"]:
        original_argv = sys.argv
        sys.argv = [tool_config["module"]] + args
    
    # 4. Execute tool
    try:
        exit_code = main_func() or 0
    except Exception as e:
        print(f"Error executing {tool_config['name']}: {e}")
        exit_code = 1
    finally:
        if tool_config["args_passthrough"]:
            sys.argv = original_argv
    
    return exit_code
```

---

### 4. toolbelt_help.py (Help System)

**Purpose:** Auto-generated help from registry  
**Lines:** ~100 lines (V2 compliant)

**Responsibilities:**
- Generate formatted help text
- Display available tools with descriptions
- Show usage examples
- Provide flag documentation

**Help Output Format:**
```
🛠️  CLI Toolbelt - Unified Tool Access
==========================================

Usage: python -m tools.toolbelt <TOOL_FLAG> [TOOL_ARGS...]

Available Tools:
----------------

📊 Project Scanner (--scan, -s)
   Scan project structure and generate analysis
   Example: python -m tools.toolbelt --scan --project-root .

✅ V2 Compliance Checker (--v2-check, --v2, -v)
   Check V2 compliance violations
   Example: python -m tools.toolbelt --v2-check --fail-on-major

📈 Compliance Dashboard (--dashboard, -d)
   Open compliance tracking dashboard
   Example: python -m tools.toolbelt --dashboard

🔍 Complexity Analyzer (--complexity, -c)
   Analyze code complexity metrics
   Example: python -m tools.toolbelt --complexity --path src/

🔧 Refactoring Suggestions (--refactor, -r)
   Get intelligent refactoring suggestions
   Example: python -m tools.toolbelt --refactor --path src/

🔁 Duplication Analyzer (--duplication, --dup)
   Find duplicate code across project
   Example: python -m tools.toolbelt --duplication --scan

✓ Functionality Verification (--functionality, --verify)
   Verify functionality preservation
   Example: python -m tools.toolbelt --functionality --baseline

🏆 Autonomous Leaderboard (--leaderboard, -l)
   Show agent performance leaderboard
   Example: python -m tools.toolbelt --leaderboard

📜 Compliance History (--history, -h)
   Track compliance history over time
   Example: python -m tools.toolbelt --history --trend

General Options:
----------------
  --help          Show this help message
  --version       Show toolbelt version
  --list          List all available tools

For tool-specific help:
  python -m tools.toolbelt <TOOL_FLAG> --help

Examples:
---------
# Run project scan
python -m tools.toolbelt --scan

# Check V2 compliance with suggestions
python -m tools.toolbelt --v2-check --suggest

# Analyze complexity of specific file
python -m tools.toolbelt --complexity src/services/messaging_cli.py

# Show leaderboard
python -m tools.toolbelt --leaderboard --top 10
```

**Interface:**
```python
class HelpGenerator:
    def generate_help(self, registry: ToolRegistry) -> str:
        """Generate formatted help text."""
        
    def show_tool_help(self, tool_config: dict) -> str:
        """Show help for specific tool."""
```

---

## 🔄 TOOL DISCOVERY MECHANISM

### Static Registry (Phase 1 - Current)

**Approach:** Manually maintained registry in `toolbelt_registry.py`

**Pros:**
- Simple and explicit
- Full control over tool metadata
- Easy to maintain for known tools
- V2 compliant (no magic)

**Cons:**
- Manual updates required for new tools
- Potential for registry drift

**Implementation:**
```python
# toolbelt_registry.py
TOOLS_REGISTRY = {
    "scan": {...},
    "v2-check": {...},
    # ... explicit tool definitions
}
```

### Dynamic Discovery (Phase 2 - Future)

**Approach:** Scan tools/ directory for CLI-compatible tools

**Detection Criteria:**
- Python files with `main()` function
- Files ending in `_cli.py`
- Tools declaring toolbelt compatibility

**Implementation (Future):**
```python
def discover_tools():
    """Dynamically discover tools in tools/ directory."""
    for file in Path("tools").glob("*_cli.py"):
        if has_toolbelt_metadata(file):
            register_tool_from_file(file)
```

**Decision:** Use static registry for now, design for dynamic future

---

## 🎯 FLAG SYSTEM DESIGN

### Primary Flags

Each tool has ONE primary flag (semantic, descriptive):
- `--scan` (not `-s` as primary)
- `--v2-check` (not `--v2` as primary)
- `--dashboard` (not `-d` as primary)

### Aliases

Each tool can have multiple aliases:
- `--scan` → aliases: `-s`
- `--v2-check` → aliases: `--v2`, `-v`
- `--dashboard` → aliases: `-d`

### Argument Passthrough

Tools receive remaining arguments transparently:
```bash
python -m tools.toolbelt --scan --project-root . --verbose
                                 ^^^^^^^^^^^^^^^^^^^^^^^^
                                 Passed to projectscanner.main()
```

Implementation:
```python
# toolbelt.py
parser.parse_known_args()  # Returns (args, remaining)
runner.execute_tool(tool, remaining)  # Pass remaining to tool
```

---

## 🚀 USAGE EXAMPLES

### Basic Usage

```bash
# Run project scanner
python -m tools.toolbelt --scan

# Check V2 compliance
python -m tools.toolbelt --v2-check

# Open dashboard
python -m tools.toolbelt --dashboard
```

### With Arguments

```bash
# Scan with custom root
python -m tools.toolbelt --scan --project-root ./src

# V2 check with fail-on-major
python -m tools.toolbelt --v2-check --fail-on-major --suggest

# Complexity analysis for specific file
python -m tools.toolbelt --complexity src/services/messaging_cli.py
```

### Using Aliases

```bash
# Short flags work too
python -m tools.toolbelt -s          # Same as --scan
python -m tools.toolbelt -v          # Same as --v2-check
python -m tools.toolbelt -d          # Same as --dashboard
```

---

## 🔧 IMPLEMENTATION PLAN

### Phase 1: Core Infrastructure (Agent-1 - Cycle 2)

**Files to Create:**
1. `tools/toolbelt.py` (~80 lines)
2. `tools/toolbelt_registry.py` (~120 lines)
3. `tools/toolbelt_runner.py` (~100 lines)
4. `tools/toolbelt_help.py` (~100 lines)

**Tasks:**
- Create toolbelt.py entry point
- Implement argument parsing
- Build tool registry with 9 tools
- Implement tool runner with dynamic import
- Generate help system

**Validation:**
- Each module ≤400 lines (V2 compliant)
- All tools accessible via flags
- Help system working
- Argument passthrough functional

---

### Phase 2: Testing & Integration (Agent-1 - Cycle 3)

**Testing Requirements:**
- Unit tests for each component
- Integration tests for tool execution
- Help system output validation
- Error handling verification

**Test Files:**
- `tests/test_toolbelt.py`
- `tests/test_toolbelt_registry.py`
- `tests/test_toolbelt_runner.py`
- `tests/test_toolbelt_help.py`

**Integration Tests:**
```python
def test_scan_tool_execution():
    """Test --scan flag executes project scanner."""
    exit_code = run_toolbelt(["--scan", "--project-root", "."])
    assert exit_code == 0

def test_v2_check_with_args():
    """Test --v2-check passes args to checker."""
    exit_code = run_toolbelt(["--v2-check", "--fail-on-major"])
    assert exit_code in [0, 1]  # Valid exit codes

def test_help_generation():
    """Test help system generates proper output."""
    output = run_toolbelt(["--help"])
    assert "Available Tools" in output
    assert "--scan" in output
```

---

### Phase 3: Documentation (Agent-1 - Cycle 4)

**Documentation Deliverables:**
- Update main README with toolbelt usage
- Create tools/README_TOOLBELT.md
- Add docstrings to all modules
- Create usage examples

---

## 📊 V2 COMPLIANCE

### File Size Targets

| File | Target Lines | Status |
|------|-------------|---------|
| toolbelt.py | ~80 | ✅ V2 Compliant |
| toolbelt_registry.py | ~120 | ✅ V2 Compliant |
| toolbelt_runner.py | ~100 | ✅ V2 Compliant |
| toolbelt_help.py | ~100 | ✅ V2 Compliant |

**Total:** ~400 lines across 4 focused modules

### Design Principles Applied

- **Single Responsibility**: Each module has one clear purpose
- **Open-Closed**: Easy to add new tools without modifying core
- **Dependency Injection**: Registry injected into runner
- **Separation of Concerns**: Parse → Discover → Execute → Help
- **V2 Line Limits**: All files <400 lines

---

## 🎯 SUCCESS CRITERIA

### Functional Requirements

✅ **Unified Entry Point**
- Single command: `python -m tools.toolbelt`
- Works from any directory

✅ **Flag-Based Selection**
- Each tool accessible via semantic flag
- Aliases supported
- Arguments passed through

✅ **Help System**
- Auto-generated from registry
- Shows all tools and usage
- Tool-specific help available

✅ **Tool Discovery**
- 9 tools registered and accessible
- Easy to add new tools
- Metadata-driven

### Non-Functional Requirements

✅ **V2 Compliance**
- All files ≤400 lines
- Clean module structure
- No circular dependencies

✅ **Maintainability**
- Clear architecture
- Well-documented
- Easy to extend

✅ **User Experience**
- Intuitive commands
- Helpful error messages
- Consistent interface

---

## 🔄 FUTURE ENHANCEMENTS

### Phase 4 (Future - After Initial Release)

**Dynamic Tool Discovery:**
- Scan tools/ directory automatically
- Register tools with metadata decorators
- Support plugin architecture

**Enhanced Features:**
- Tool chaining (pipe output between tools)
- Configuration file support
- Custom tool aliases
- Tool dependencies and prerequisites

**Example Future Syntax:**
```bash
# Chain tools
python -m tools.toolbelt --scan | toolbelt --v2-check

# Use config file
python -m tools.toolbelt --config toolbelt.json

# Custom alias
toolbelt scan  # Shorthand for python -m tools.toolbelt --scan
```

---

## 📝 HANDOFF TO AGENT-1

### Architecture Complete - Ready for Implementation

**Agent-1 (Integration & Testing Specialist):**

You now have complete architecture design. Here's your implementation roadmap:

**Cycle 2 - Implementation:**
1. Create 4 core modules as specified
2. Implement tool registry with 9 tools
3. Build execution engine with argument passthrough
4. Generate help system

**Cycle 3 - Testing:**
1. Unit tests for each component
2. Integration tests for tool execution
3. Error handling verification
4. Help system validation

**Cycle 4 - Documentation & Polish:**
1. README updates
2. Usage documentation
3. Code cleanup
4. Final validation

**Key Implementation Details:**
- Use `argparse` for CLI parsing
- Use `importlib` for dynamic tool loading
- Use `sys.argv` manipulation for argument passthrough
- Keep each module ≤400 lines (V2 compliant)

**Questions/Coordination:**
- Architecture questions: Message Agent-2
- Tool-specific questions: Check tool's existing CLI
- Testing questions: Coordinate with Agent-2

**Ready to implement! Architecture design phase COMPLETE.** 🎯

---

## 🏆 DELIVERABLES SUMMARY

**For Captain:**
- ✅ Architecture design document (this file)
- ✅ Component specifications
- ✅ Implementation plan
- ✅ Success criteria defined

**For Agent-1:**
- ✅ Clear implementation roadmap
- ✅ Module specifications with line counts
- ✅ Testing requirements
- ✅ V2 compliance targets

**Architecture Design Status:** **COMPLETE** ✅

---

**#C058-2-COMPLETE #ARCHITECTURE-DELIVERED #AGENT1-UNBLOCKED**

🐝 WE. ARE. SWARM. ⚡️🔥

---

**Agent-2 - Architecture & Design Specialist**  
**C-058-2: CLI Toolbelt Architecture**  
**Status: Design Phase COMPLETE**  
**Date: 2025-10-11**

