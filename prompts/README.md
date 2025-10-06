# V2_SWARM Cycle Prompts

## Overview

This directory contains all 70 cycle prompts for the V2_SWARM production readiness initiative. Each prompt is designed to guide agents through specific tasks with clear objectives, commands, and success criteria.

## Directory Structure

```
prompts/
├── README.md                    # This file
├── phase1_discovery/           # Cycles 1-8 (Discovery & Analysis)
│   ├── c001.md                # Agent-3: Project Scanner Execution
│   ├── c002.md                # Agent-6: Duplicate Analysis
│   ├── c003.md                # Agent-2: Workspace Analysis
│   ├── c004.md                # Agent-5: Documentation Baseline
│   ├── c005.md                # Agent-1: Infrastructure Analysis
│   ├── c006.md                # Agent-8: Integration Analysis
│   ├── c007.md                # Agent-4: Captain Assessment
│   └── c008.md                # Agent-7: Web Interface Analysis
├── phase2_cleanup/            # Cycles 9-20 (File Cleanup & Consolidation)
│   ├── c009.md                # Agent-2: Workspace Cleanup Execution
│   ├── c010.md                # Agent-6: Consolidate core.py
│   ├── c011.md                # Agent-6: Consolidate models.py
│   ├── c012.md                # Agent-6: Clean README duplicates
│   └── c013-c020.md           # Additional cleanup tasks
├── phase3_enhancement/        # Cycles 21-40 (Feature Enhancement)
│   ├── c021.md                # Agent-7: Discord Commander Audit
│   ├── c022.md                # Agent-7: Fix Discord Issues
│   ├── c023.md                # Agent-1: Production Infrastructure
│   └── c024-c040.md           # Additional enhancement tasks
├── phase4_documentation/      # Cycles 41-55 (Professional Documentation)
│   ├── c041.md                # Agent-5: Professional README
│   ├── c042.md                # Agent-5: Installation Guide
│   ├── c043.md                # Agent-5: Usage Guide
│   └── c044-c055.md           # Additional documentation
└── phase5_testing/            # Cycles 56-70 (Testing & Validation)
    ├── c056.md                # Agent-3: Create Test Suite
    ├── c057.md                # Agent-3: Run Integration Tests
    └── c058-c070.md           # Additional testing tasks
```

## Phase Overview

### Phase 1: Discovery (Cycles 1-8) - ~6 hours
**Objective:** Understand current system state and identify all issues

- **C1:** Agent-3 runs comprehensive project scanner
- **C2:** Agent-6 analyzes all duplicate files
- **C3:** Agent-2 analyzes agent workspaces (801 files)
- **C4:** Agent-5 creates documentation baseline
- **C5-C8:** Additional discovery by all agents

**Target:** Complete system inventory and issue identification

### Phase 2: Cleanup (Cycles 9-20) - ~8 hours
**Objective:** Clean up files and resolve duplicates

- **C9:** Agent-2 executes workspace cleanup (801 → 200 files)
- **C10-C12:** Agent-6 consolidates duplicate files
- **C13-C20:** Additional cleanup tasks

**Target:** Reduce total files from 2362 to ~1500

### Phase 3: Enhancement (Cycles 21-40) - ~20 hours
**Objective:** Implement features and fix issues

- **C21:** Agent-7 audits Discord Commander
- **C22-C25:** Agent-7 fixes Discord issues
- **C23:** Agent-1 sets up production infrastructure
- **C24-C40:** Additional enhancements

**Target:** All systems production-ready

### Phase 4: Documentation (Cycles 41-55) - ~19 hours
**Objective:** Create professional documentation

- **C41:** Agent-5 creates professional README
- **C42:** Agent-5 creates installation guide
- **C43:** Agent-5 creates usage guide
- **C44-C55:** Additional documentation

**Target:** Complete documentation suite

### Phase 5: Testing & Validation (Cycles 56-70) - ~13 hours
**Objective:** Comprehensive testing and validation

- **C56:** Agent-3 creates test suite
- **C57:** Agent-3 runs integration tests
- **C58-C70:** Additional testing and validation

**Target:** 80%+ test coverage and production validation

## Usage Instructions

### For Agents
1. **Receive cycle assignment** from Captain (Agent-4)
2. **Read the prompt** for your assigned cycle
3. **Execute commands** as specified
4. **Create deliverables** as required
5. **Report completion** using CYCLE_DONE format

### For Captain (Agent-4)
1. **Assign cycles** based on dependencies and agent availability
2. **Monitor progress** using progress tracker
3. **Resolve blockers** as they arise
4. **Generate reports** daily

### CYCLE_DONE Format
```
CYCLE_DONE <Agent-ID> <Cycle-ID> ["Metric1", "Metric2", "Metric3", "Metric4"] "Summary of completion"
```

Example:
```
CYCLE_DONE Agent-3 c-scan-001 ["Scanned 2362 files", "Found 26 duplicates", "Identified 15 V2 violations", "Generated 3 reports"] "Project scan complete, ready for duplicate analysis"
```

## Progress Tracking

### Real-time Dashboard
```bash
python tools/cycle_progress_tracker.py --format dashboard
```

### Daily Reports
```bash
python tools/generate_progress_report.py --format markdown > reports/progress_$(date +%Y%m%d).md
```

### JSON Data
```bash
python tools/cycle_progress_tracker.py --format json > reports/progress_data.json
```

## Success Metrics

- **Total Cycles:** 70
- **Target Completion:** 8-10 working days (with 8 agents)
- **File Reduction:** 2362 → 1500 files (36% reduction)
- **Test Coverage:** 80%+
- **Documentation:** Complete professional suite
- **Production Ready:** YES

## Agent Roles

- **Agent-1:** Infrastructure Specialist - Deployment & DevOps
- **Agent-2:** Data Processing Expert - Data management & analytics
- **Agent-3:** Quality Assurance Lead - Testing & compliance
- **Agent-4:** Captain - Strategic oversight & coordination
- **Agent-5:** SSOT Manager - Documentation & standards
- **Agent-6:** Code Quality Specialist - Refactoring & optimization
- **Agent-7:** Web Development Expert - UI/UX & interfaces
- **Agent-8:** Integration Specialist - System integration & testing

## Emergency Procedures

### If Agent Becomes Unresponsive
1. Captain assigns cycle to backup agent
2. Document issue in Captain's Log
3. Escalate if critical blocker

### If Cycle Fails
1. Agent reports blocker immediately
2. Captain analyzes issue
3. Captain provides resolution or assigns to different agent
4. Update cycle dependencies

### If System Issues Occur
1. Captain halts all cycles
2. Assess system stability
3. Resume with safe cycles only
4. Document lessons learned

---

**Created:** 2025-01-27  
**Version:** 1.0  
**Status:** Ready for Production Readiness Initiative

