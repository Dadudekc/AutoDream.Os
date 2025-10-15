# Agent Toolbelt Expansion Proposal
## Adding More Tools to agent_toolbelt.py

**Current Status:** Toolbelt has 5 command categories  
**Proposal:** Add 8 more categories with existing tools

---

## 🎯 Currently Available

### 1. Vector DB (`vector`)
- context, search, patterns, index, stats

### 2. Messaging (`message`)
- message, broadcast, inbox, status

### 3. Analysis (`analyze`)
- project, complexity, duplicates, refactor

### 4. V2 Compliance (`v2`)
- check, report, violations

### 5. Agent Operations (`agent`)
- status, inbox, claim-task, coordinates

---

## 🚀 Proposed Additions

### 6. **Onboarding Tools** (`onboard`) 🆕
**Tools Available:**
- `soft_onboard_cli.py` - 3-step session cleanup
- Messaging CLI `--soft-onboarding` flag
- Messaging CLI `--hard-onboarding` flag

**Proposed Commands:**
```bash
python tools/agent_toolbelt.py onboard soft --agent Agent-7 --message "Mission"
python tools/agent_toolbelt.py onboard hard --agent Agent-7 --message "Mission" --yes
python tools/agent_toolbelt.py onboard status --agent Agent-7  # Show onboarding status
```

**Value:** Streamlined agent session management

---

### 7. **Leaderboard & Competition** (`leaderboard`)
**Tool Available:** `autonomous_leaderboard.py`

**Proposed Commands:**
```bash
python tools/agent_toolbelt.py leaderboard show         # Show current standings
python tools/agent_toolbelt.py leaderboard agent Agent-7  # Agent details
python tools/agent_toolbelt.py leaderboard award Agent-7 velocity-bonus
python tools/agent_toolbelt.py leaderboard top 5         # Top 5 agents
```

**Value:** Quick access to competition standings

---

### 8. **Compliance Tracking** (`compliance`)
**Tools Available:**
- `compliance_history_tracker.py` - Track over time
- `compliance_history_database.py` - SQLite storage
- `compliance_history_reports.py` - Trend analysis
- `compliance_dashboard.py` - Visual dashboard

**Proposed Commands:**
```bash
python tools/agent_toolbelt.py compliance track       # Take snapshot
python tools/agent_toolbelt.py compliance history     # Show history
python tools/agent_toolbelt.py compliance trends      # Show trends
python tools/agent_toolbelt.py compliance dashboard   # Launch dashboard
python tools/agent_toolbelt.py compliance compare     # Compare snapshots
```

**Value:** Historical V2 compliance tracking (currently missing from toolbelt!)

---

### 9. **Testing & Coverage** (`testing`)
**Tools Available:**
- `coverage/run_coverage_analysis.py` - Coverage pipeline
- `coverage/changed_file_report.py` - Changed file coverage
- `coverage/mutation_gate.py` - Mutation testing

**Proposed Commands:**
```bash
python tools/agent_toolbelt.py testing coverage        # Run coverage analysis
python tools/agent_toolbelt.py testing changed         # Coverage on changed files
python tools/agent_toolbelt.py testing mutation        # Mutation testing
python tools/agent_toolbelt.py testing gate            # Quality gate check
```

**Value:** Comprehensive testing tools in one place

---

### 10. **Code Transformation** (`codemod`)
**Tools Available:**
- `codemods/migrate_managers.py` - Migrate manager imports
- `codemods/migrate_orchestrators.py` - Migrate orchestrator imports
- `codemods/replace_prints_with_logger.py` - Replace print with logger

**Proposed Commands:**
```bash
python tools/agent_toolbelt.py codemod print-to-logger src/
python tools/agent_toolbelt.py codemod migrate-managers src/
python tools/agent_toolbelt.py codemod migrate-orchestrators src/
python tools/agent_toolbelt.py codemod list  # Show available transformations
```

**Value:** Automated code transformations

---

### 11. **Documentation Management** (`docs`)
**Tools Available:**
- `cleanup_documentation_refactored.py` - Doc cleanup
- `cleanup_documentation_deduplicator.py` - Find duplicates
- `cleanup_documentation_reference_scanner.py` - Find references
- `analyze_init_files.py` - Analyze __init__ files

**Proposed Commands:**
```bash
python tools/agent_toolbelt.py docs cleanup          # Clean documentation
python tools/agent_toolbelt.py docs duplicates       # Find duplicate docs
python tools/agent_toolbelt.py docs references FILE  # Find doc references
python tools/agent_toolbelt.py docs init-analysis    # Analyze __init__ files
```

**Value:** Documentation consolidation tools

---

### 12. **Swarm Status** (`swarm`)
**Tools Available:**
- `captain_snapshot.py` - Quick swarm overview
- `agent_checkin.py` - Agent check-in system

**Proposed Commands:**
```bash
python tools/agent_toolbelt.py swarm snapshot        # Captain's view
python tools/agent_toolbelt.py swarm checkin --agent Agent-7 --status "working"
python tools/agent_toolbelt.py swarm active          # Show active agents
python tools/agent_toolbelt.py swarm health          # Overall swarm health
```

**Value:** Quick swarm status visibility

---

### 13. **Quality Verification** (`verify`)
**Tools Available:**
- `functionality_verification.py` - Verify functionality preserved
- `functionality_comparison.py` - Compare before/after
- `functionality_signature.py` - Generate signatures
- `functionality_tests.py` - Run tests

**Proposed Commands:**
```bash
python tools/agent_toolbelt.py verify file original.py refactored.py
python tools/agent_toolbelt.py verify compare before/ after/
python tools/agent_toolbelt.py verify tests FILE    # Run functionality tests
python tools/agent_toolbelt.py verify signature FILE  # Generate signature
```

**Value:** Ensure refactoring doesn't break functionality

---

## 📊 Summary

**Current:** 5 command categories, ~20 commands  
**Proposed:** 13 command categories, ~60+ commands

**New Categories:**
1. ✅ `onboard` - Session management (NEW tools!)
2. ✅ `leaderboard` - Competition tracking
3. ✅ `compliance` - Historical tracking
4. ✅ `testing` - Coverage & mutation
5. ✅ `codemod` - Code transformations
6. ✅ `docs` - Documentation management
7. ✅ `swarm` - Swarm status
8. ✅ `verify` - Functionality verification

---

## 🎯 Prioritization

### HIGH Priority (Immediate Value)
1. **`onboard`** - NEW tools just created, high usage expected
2. **`leaderboard`** - Active competition system needs easy access
3. **`swarm`** - Captain needs quick status view
4. **`compliance`** - Historical tracking currently missing

### MEDIUM Priority (Enhanced Workflows)
5. **`testing`** - Quality assurance workflows
6. **`verify`** - Refactoring safety
7. **`docs`** - C-055-8 documentation consolidation

### LOW Priority (Advanced Features)
8. **`codemod`** - Specialized transformations

---

## 💻 Implementation Plan

### Phase 1: Core Extensions (HIGH Priority)
**Effort:** 2-3 cycles

```python
def _add_onboarding_parser(self, subparsers):
    """Add onboarding subcommand."""
    onboard_parser = subparsers.add_parser('onboard', help='Agent onboarding')
    onboard_sub = onboard_parser.add_subparsers(dest='onboard_action')
    
    # Soft onboarding
    soft_p = onboard_sub.add_parser('soft', help='Soft onboarding (session cleanup)')
    soft_p.add_argument('--agent', required=True)
    soft_p.add_argument('--message', required=True)
    
    # Hard onboarding
    hard_p = onboard_sub.add_parser('hard', help='Hard onboarding (complete reset)')
    hard_p.add_argument('--agent', required=True)
    hard_p.add_argument('--message', required=True)
    hard_p.add_argument('--yes', action='store_true', help='Confirm destructive operation')

def _add_leaderboard_parser(self, subparsers):
    """Add leaderboard subcommand."""
    lb_parser = subparsers.add_parser('leaderboard', help='Competition leaderboard')
    lb_sub = lb_parser.add_subparsers(dest='lb_action')
    
    lb_sub.add_parser('show', help='Show current standings')
    
    agent_p = lb_sub.add_parser('agent', help='Agent details')
    agent_p.add_argument('agent_id', help='Agent ID')
    
    top_p = lb_sub.add_parser('top', help='Top N agents')
    top_p.add_argument('n', type=int, default=5, help='Number of agents')

# Similar for other categories...
```

### Phase 2: Enhanced Workflows (MEDIUM Priority)
**Effort:** 2-3 cycles
- Add `testing`, `verify`, `docs` commands
- Integrate with existing tools
- Test workflows

### Phase 3: Advanced Features (LOW Priority)
**Effort:** 1-2 cycles
- Add `codemod` commands
- Polish and optimize
- Complete documentation

**Total Estimated Effort:** 5-8 cycles

---

## 🏆 Benefits

### For Agents
- ✅ Single command interface for all tools
- ✅ Consistent syntax across operations
- ✅ Easy discovery of available tools
- ✅ Reduced cognitive load (one tool to remember)

### For Swarm
- ✅ Standardized tool access
- ✅ Easier onboarding (agents learn one interface)
- ✅ Better tool discoverability
- ✅ Unified error handling

### For Tooling
- ✅ Centralized tool registry
- ✅ Easier maintenance
- ✅ Consistent help documentation
- ✅ Version control over tool access

---

## 📝 Examples

### Before (Multiple Tools)
```bash
# Different commands for different tools
python autonomous_leaderboard.py show
python tools/soft_onboard_cli.py --agent Agent-7 --message "Test"
python tools/compliance_history_tracker.py --track
python tools/captain_snapshot.py
```

### After (Unified Toolbelt)
```bash
# Single interface
python tools/agent_toolbelt.py leaderboard show
python tools/agent_toolbelt.py onboard soft --agent Agent-7 --message "Test"
python tools/agent_toolbelt.py compliance track
python tools/agent_toolbelt.py swarm snapshot
```

**Simpler, more consistent, easier to remember!**

---

## ✅ Next Steps

1. **Phase 1 Implementation:**
   - Add `onboard` command (NEW tools priority!)
   - Add `leaderboard` command (active competition system)
   - Add `swarm` command (Captain visibility)
   - Add `compliance` command (historical tracking)

2. **Testing:**
   - Test all new commands
   - Verify backward compatibility
   - Update help documentation

3. **Documentation:**
   - Update `README_TOOLBELT.md`
   - Add usage examples
   - Update `AGENT_TOOLS_DOCUMENTATION.md`

4. **Rollout:**
   - Announce to swarm
   - Training/examples
   - Gather feedback

---

**Status:** 📝 PROPOSAL DOCUMENTED  
**Priority:** HIGH (especially `onboard` and `leaderboard`)  
**Estimated Effort:** 5-8 cycles total  
**Value:** SIGNIFICANT (unified tool interface)

---

*Proposal compiled by: Agent-8 (Documentation Specialist)*  
*Date: 2025-10-11*  
*Based on: tools/ directory analysis*

🐝 **WE. ARE. SWARM.** ⚡🔥






