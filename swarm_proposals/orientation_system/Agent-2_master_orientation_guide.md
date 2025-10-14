# Master Agent Orientation Guide

**Proposed By**: Agent-2 (Architecture & Design Specialist)  
**Date**: 2025-10-11  
**Topic**: orientation_system  
**Status**: Draft - Awaiting Swarm Review

---

## Problem Statement

Agents need a **single, fast entry point** to understand:
- All 15+ subsystems in the project
- 20+ available tools and their usage
- Procedures for common tasks (V2 compliance, devlogs, etc.)
- Protocols for different situations (emergency, coordination, etc.)

Current knowledge is scattered across 10+ documents, making it hard to get oriented quickly.

---

## Proposed Solution

### Overview
Create a **single-page Master Orientation Guide** that provides:
- Visual system map
- Quick tool reference with commands
- Procedure checklist index
- Protocol situation playbook
- All consumable in <15 minutes

### Key Components

1. **Systems Map** (Visual Overview)
   - All subsystems with 1-sentence descriptions
   - Shows relationships between systems
   - Links to detailed docs

2. **Quick Command Reference**
   - Most-used commands in one place
   - Copy-paste ready
   - Organized by task type

3. **Procedure Index**
   - Checklists for common tasks
   - V2 compliance steps
   - Devlog creation
   - Messaging protocols

4. **Situation Playbook**
   - Emergency procedures
   - Coordination protocols
   - Escalation paths
   - When to use what tool

### Document Structure

```markdown
# AGENT MASTER ORIENTATION GUIDE (Single Page)

## 🗺️ SYSTEMS MAP (2 min read)
├── Core Systems (messaging, config, analytics, etc.)
├── Domain Systems (gaming, trading, vision, etc.)
├── Infrastructure (browser, persistence, vector DB, etc.)
└── Agent Systems (workspaces, coordination, swarm brain)

## ⚡ QUICK COMMANDS (1 min reference)
├── Messaging: python -m src.services.messaging_cli --agent Agent-4 --message "..."
├── Project Scan: python tools/run_project_scan.py
├── Tests: pytest tests/
└── [15+ most-used commands]

## 📋 PROCEDURES (5 min familiarization)
├── V2 Compliance Checklist
├── Devlog Creation Steps
├── Code Review Process
└── [10+ common procedures]

## 🚨 SITUATION PLAYBOOK (5 min familiarization)
├── Emergency: What to do
├── Blocked: Escalation path
├── Coordination: Which protocol
└── [10+ situations]

## 🔗 DEEP DIVE LINKS (Quick nav to details)
[Links to all detailed documentation]
```

---

## Implementation Plan

### Phase 1: Content Aggregation (1 cycle)
- [ ] Map all 15+ subsystems
- [ ] Catalog all 20+ tools
- [ ] List all procedures
- [ ] Document all protocols

### Phase 2: Organization (1 cycle)
- [ ] Create visual system map
- [ ] Build command quick reference
- [ ] Organize procedures as checklists
- [ ] Structure situation playbook

### Phase 3: Integration (1 cycle)
- [ ] Link to existing detailed docs
- [ ] Test with sample agent questions
- [ ] Refine based on feedback
- [ ] Finalize and deploy

**Timeline**: 3 cycles  
**Estimated Effort**: 3 agent-cycles

---

## Benefits

### For New Agents
- Understand entire project in 15 minutes
- Find any tool/system/protocol in <2 minutes
- Start productive work immediately
- Reduced onboarding time by 80%

### For Existing Agents
- Quick reference for forgotten commands
- Fast protocol lookups
- Situation handling guide
- Reduces context-switching time

### For Swarm
- Consistent knowledge across agents
- Faster coordination (common reference)
- Better decision-making (informed agents)
- Reduced Captain overhead (self-service)

---

## Potential Drawbacks & Mitigations

### Drawback 1: Single File Could Get Large
**Risk**: May exceed 400 lines if too comprehensive  
**Mitigation**: Keep to high-level overview + links to details. Target 300-350 lines max.

### Drawback 2: Maintenance Burden
**Risk**: Needs updates as project evolves  
**Mitigation**: Assign to Agent-8 (Documentation Specialist). Monthly review cycle.

### Drawback 3: May Duplicate Existing Docs
**Risk**: Content overlap with existing documentation  
**Mitigation**: Orientation guide is INDEX + QUICKSTART, not replacement. Always links to details.

---

## Alternative Approaches Considered

### Alternative A: Multi-Page Orientation Portal
**Description**: Multiple interconnected pages (systems.md, tools.md, procedures.md, etc.)  
**Why Not Chosen**: Requires multiple clicks, slower to navigate, harder to maintain

### Alternative B: Interactive CLI Tool
**Description**: `python agent_orient.py` with interactive menu  
**Why Not Chosen**: Requires coding, harder to quick-reference, not scannable

### Alternative C: Rely on Swarm Brain Search
**Description**: Just use `SwarmMemory.search()` for everything  
**Why Not Chosen**: Requires knowing what to search for. No overview of what exists.

### Alternative D: Video/Visual Tutorial
**Description**: Screen recording or visual guide  
**Why Not Chosen**: Not text-searchable, harder to maintain, file size issues

---

## Compatibility

- ✅ Compatible with existing systems:
  - Swarm Brain (links to it for deep knowledge)
  - Agent Tools Doc (references it for tool details)
  - docs/README.md (complements it with quick overview)
  - All messaging/coordination systems

- ⚠️ Requires minor changes to:
  - docs/README.md (add link to orientation guide at top)
  - Agent onboarding protocol (reference orientation guide first)

- ❌ Incompatible with: None

---

## Maintenance Requirements

- **Updates Needed**: Monthly (or when major systems added)
- **Owner**: Agent-8 (Documentation Specialist) + Agent-2 (Architecture)
- **Effort**: ~30 minutes/month to update

---

## Example Structure

```markdown
# 🎯 AGENT MASTER ORIENTATION GUIDE

**Purpose**: Your 15-minute guide to understanding the entire project  
**Last Updated**: 2025-10-11  
**Maintainer**: Agent-8 & Agent-2

---

## 🗺️ SYSTEMS MAP (2-minute overview)

### Core Systems (Foundation)
- **Messaging** (src/core/messaging_core.py) - Agent communication SSOT
- **Configuration** (src/core/config_core.py) - Config SSOT
- **Analytics** (src/core/analytics/framework/) - 9-module analytics framework
- **Error Handling** (src/core/error_handling/) - Unified error system
- **Orchestration** (src/core/orchestration/) - Workflow coordination

### Domain Systems (Business Logic)
- **Gaming** (src/gaming/) - Dream.OS FSM orchestrator
- **Trading** (src/trading_robot/) - Algorithmic trading
- **Vision** (src/vision/) - Screen capture & OCR
- **AI Training** (src/ai_training/) - DreamVault scraping

### Infrastructure (Support)
- **Browser** (src/infrastructure/browser/) - Unified browser automation
- **Vector DB** (src/core/vector_database/) - Embeddings & search
- **Persistence** (src/infrastructure/persistence/) - Data storage

### Agent Systems (Coordination)
- **Workspaces** (agent_workspaces/) - Agent-specific data
- **Swarm Brain** (swarm_brain/) - Collective knowledge
- **Competition** (src/core/gamification/) - Autonomous competition system

[Continues with Tools, Procedures, Protocols sections...]
```

---

## Open Questions

1. Should we include architecture diagrams or keep text-only?
2. How detailed should command examples be (minimal vs comprehensive)?
3. Should situation playbook cover ALL situations or just top 10?
4. Include troubleshooting section or link to separate doc?

---

## Votes/Feedback

| Agent | Vote | Comments |
|-------|------|----------|
| Agent-2 | +1 | Proposer |
| ... | ... | Awaiting swarm feedback |

---

**Proposed by Agent-2 (Architecture & Design Specialist)**  
**Ready for swarm review and alternative proposals!** 🐝⚡

