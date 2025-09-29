# Captain's Cheatsheet - Quick Reference (Cycle-Based Operations)
## Agent-4 (Captain & Operations Coordinator)

### 🔄 **Cycle-Based Quick Commands**

**Swarm Status**:
```bash
# Check all agents (per cycle)
python tools/captain_cli.py status --all --cycle

# Check specific agent (within cycle)
python tools/captain_cli.py status --agent Agent-1 --cycle

# Run quality gates (per cycle)
python quality_gates.py --cycle
```

**Vector Database**:
```python
# Query swarm intelligence (cycle-based)
from swarm_brain import Retriever
retriever = Retriever()
patterns = retriever.how_do_agents_do("V2 compliance refactoring across cycles")
```

### 📊 **Priority Levels (Cycle-Based)**
- **P0 (Critical)**: Within current cycle - System failure, security breach, blocking issues
- **P1 (High)**: 1-2 cycles - Important features, performance issues, quality problems
- **P2 (Medium)**: 2-4 cycles - Enhancements, optimizations, documentation
- **P3 (Low)**: 4+ cycles - Nice-to-have features, minor improvements

### 🤖 **Agent Quick Reference (Cycle-Based)**

| Agent | Specialization | Cycle Focus | Contact Method |
|-------|---------------|-------------|----------------|
| Agent-1 | V3 Development | 2-3 cycles per feature | Discord/CLI |
| Agent-2 | System Coord | 1-2 cycles per component | Discord/CLI |
| Agent-3 | Database/ML | 3-4 cycles per pipeline | Discord/CLI |
| Agent-4 | Captain | Continuous cycle oversight | Self |
| Agent-5 | ML Training | 2-3 cycles per training | Discord/CLI |
| Agent-6 | Quality | 1 cycle per validation | Discord/CLI |
| Agent-7 | Web Dev | 2-3 cycles per phase | Discord/CLI |
| Agent-8 | Integration | 1-2 cycles per integration | Discord/CLI |

### 🎯 **Strategic Directives Status (Multi-Cycle)**

**V3 Pipeline Completion**: 75% → Web Dashboard (Agent-1) - 3-4 cycles remaining
**System Architecture Evolution**: 60% → FSM Implementation (Agent-2) - 4-5 cycles remaining
**Quality Standards Enforcement**: 95% → Ongoing (All Agents) - Per cycle
**Swarm Intelligence Enhancement**: 80% → Vector DB (Agent-3) - 2-3 cycles remaining

### 📈 **Quality Metrics (Per-Cycle)**

**V2 Compliance**: ≤400 lines, ≤5 classes, ≤10 functions (validated per cycle)
**Performance Targets**: 95% completion, <3min response, 95/100 quality (per cycle)
**Current Status**: 98% compliance, 95% completion, 2.3min avg response (last cycle)

### 🔧 **Tools Quick Access (Cycle-Based)**

**Captain Tools**:
- `tools/captain_autonomous_manager.py` - Core coordination (per cycle)
- `tools/captain_cli.py` - Command line interface (cycle-based)
- `tools/captain_progress_tracker.py` - Progress monitoring (per cycle)
- `tools/captain_onboarding_wizard.py` - Agent onboarding (1-2 cycles)

**System Tools**:
- `quality_gates.py` - V2 compliance checking (per cycle)
- `run_tests.py` - Test execution (per cycle)
- `check_v2_compliance.py` - Compliance validation (per cycle)

### 🚨 **Emergency Contacts (Cycle-Based)**

**Critical Issues**:
- Escalate immediately to General (Human Commander) within cycle
- Use P0 priority level
- Document in Captain's Log (per cycle)

**Agent Issues**:
- Check agent status first (within cycle)
- Redistribute tasks if needed (within cycle)
- Document in coordination log (per cycle)

### 📝 **Cycle Checklist**

**Cycle Initialization**:
- [ ] Swarm health check
- [ ] Priority review (previous cycle outcomes)
- [ ] Agent status verification
- [ ] Strategic alignment check (multi-cycle goals)

**Cycle Execution** (Mid-Cycle):
- [ ] Progress review (cycle milestones)
- [ ] Bottleneck detection (within cycle)
- [ ] Quality validation (per cycle)
- [ ] Resource reallocation (cycle-based)

**Cycle Completion**:
- [ ] Performance analysis (cycle metrics)
- [ ] Captain's log entry (per cycle)
- [ ] Next cycle planning (multi-cycle planning)
- [ ] Agent feedback (cycle-based)

### 🎓 **Learning Resources (Cycle-Based)**

**Vector Database Queries**:
- "How do agents handle V2 refactoring across cycles?"
- "What makes coordination successful over multiple cycles?"
- "What are common failure patterns within cycles?"
- "How do agents learn from each other across cycles?"

**Documentation**:
- `docs/CAPTAIN_HANDBOOK.md` - Complete operations manual (cycle-based)
- `swarm_coordination/captain_log_*.md` - Historical cycle logs
- `devlogs/` - Agent development logs (cycle-based)
- `vector_database/` - Swarm intelligence data (updated per cycle)

### 🔄 **Cycle Management**

**Cycle Duration**: 2-4 hours of focused work
**Cycle Objectives**: 3-5 key objectives per cycle
**Cycle Milestones**: Clear checkpoints within cycle
**Multi-Cycle Phases**: 5-8 cycles per major phase

---

**Quick Access**: Keep this cheatsheet handy for rapid reference during cycle operations.
**Last Updated**: 2025-01-19
**Version**: 2.0 (Cycle-Based Operations)
