#!/usr/bin/env python3
"""
Add Captain's strategic knowledge to Swarm Brain
Per Commander directive: Add operating procedures to Swarm Brain
"""

from src.swarm_brain.swarm_memory import SwarmMemory

def add_captain_knowledge():
    """Add 4 HIGH priority Captain knowledge entries to Swarm Brain"""
    
    memory = SwarmMemory(agent_id='Agent-4')
    
    # 1. GitHub Critical Discoveries
    memory.share_learning(
        title="GitHub 75-Repo Critical Discoveries - Captain Analysis",
        content="""# Captain's GitHub Critical Discoveries

**Mission:** Analyzed repos 71-75 during comprehensive GitHub portfolio review

## CRITICAL DISCOVERY - Repo #74 "SWARM"
**Impact:** Foundational prototype of current swarm system!
- Appears to be early version of Agent_Cellphone architecture
- Contains original swarm coordination patterns
- Requires deep investigation for historical context
- Could reveal design decisions and rationale

## Other Discoveries (Repos 71-75):
- #71 FreeWork: Documentation/collaboration platform
- #72 bolt-project: AI-driven development tool
- #73 SouthwestsSecretDjBoard: Entertainment system
- #75 stocktwits-analyzer: Trading sentiment analysis

## Key Lesson:
Comprehensive analysis finds historical context and foundational systems. Repo #74 would have been archived in initial 60% plan - we would have lost our origin story!

**Date:** 2025-10-15
**Author:** Captain Agent-4
""",
        tags=['github', 'critical-discovery', 'swarm-prototype', 'captain', 'analysis']
    )
    print("✅ 1/4: GitHub discoveries added")
    
    # 2. Swarm Reactivation Protocol
    memory.share_learning(
        title="Swarm Reactivation Emergency Protocol - Captain Playbook",
        content="""# Swarm Reactivation Emergency Protocol

**When:** All agents go idle mid-mission (ran out of gas)
**Goal:** Bring entire swarm back online in <60 seconds
**Authority:** Captain or Co-Captain

## Symptoms of Swarm Stall:
- Multiple agents not responding
- No progress on assigned missions
- Status.json not updating
- Silence across all communication channels

## Emergency Reactivation Steps:

**1. Assess Situation (10 seconds)**
- Check status.json for all 8 agents
- Identify last known progress
- Determine which agents are idle

**2. Prepare Jet Fuel Messages (20 seconds)**
- For each agent: Specific next action (not vague encouragement!)
- Include current progress (X/Y complete)
- Clear immediate task (repo #N NOW)
- Actionable command (JET FUEL not weak gas)

**3. Deploy Messages (30 seconds)**
Use messaging CLI with NORMAL priority (not urgent):
```bash
python -m src.services.messaging_cli --agent Agent-X --message "REACTIVATION! Mission: repos X-Y. START repo #N NOW!" --pyautogui
```

**4. Document Reactivation**
- Create SWARM_REACTIVATION_YYYY-MM-DD.md
- Log which agents reactivated
- Track time to full reactivation

## Success Criteria:
- All agents back online <60 seconds
- Specific jet fuel delivered (not weak gas!)
- Progress resuming immediately
- Mission tracker updated

**Proven:** Used 2025-10-15, reactivated 7 agents in <60 seconds successfully

**Date:** 2025-10-15
**Author:** Captain Agent-4
""",
        tags=['emergency', 'reactivation', 'captain', 'protocol', 'swarm-coordination', 'jet-fuel']
    )
    print("✅ 2/4: Reactivation protocol added")
    
    # 3. Comprehensive vs Fast Framework
    memory.share_learning(
        title="Comprehensive vs Fast Decision Framework - Strategic Playbook",
        content="""# When to Do It RIGHT vs FAST

**Decision Point:** Commander paused GitHub archive debate saying "This is SECOND BIGGEST PROJECT - need comprehensive research FIRST!"

## The Framework:

### DO IT RIGHT (Comprehensive) When:
- ✅ Large-scale impact (affects 75 repos, major systems)
- ✅ Irreversible decisions (can't easily undo)
- ✅ Insufficient data (only 8/75 repos analyzed)
- ✅ High stakes (second biggest project ever)
- ✅ Critical infrastructure (foundational systems)
- ✅ Disagreement exists (Agent-6: 60% vs Agent-2: 37.5%)

### DO IT FAST When:
- Quick wins with low risk
- Reversible experiments  
- Sufficient data already exists
- Time-sensitive opportunities
- Low-impact decisions
- Consensus already exists

## Case Study: GitHub Archive Debate

**Initial Plan:** Archive 60% based on automated ROI tool (8 repos analyzed)

**Commander Decision:** PAUSE - do it RIGHT not FAST

**Result of Comprehensive Analysis:**
- Repo #43 (ROI 1.78→9.5): Migration framework - would have DELETED!
- Repo #48 (ROI 0.99→6.0): V1 origin - would have ARCHIVED!
- Repo #49 (ROI 0.98→8.0): Success model - would have DELETED!
- Repo #45 (ROI 1.34→9.0): Multi-agent threading - would have DELETED!

**Lesson:** Comprehensive approach saved critical infrastructure from deletion!

**Cost:** Extra time for full 75-repo analysis
**Benefit:** Prevented catastrophic mistakes, found tools that solve our mission
**ROI:** MASSIVE - saved migration framework and multi-agent infrastructure!

## Decision Criteria:
**Ask yourself:**
1. Can this be undone easily? (If NO → comprehensive)
2. Do we have sufficient data? (If NO → comprehensive)
3. What are the stakes? (If HIGH → comprehensive)
4. Is there disagreement? (If YES → comprehensive)
5. Is it reversible? (If NO → comprehensive)

**Commander's wisdom: "Do it RIGHT not FAST" saved the mission!**

**Date:** 2025-10-15
**Author:** Captain Agent-4
""",
        tags=['strategy', 'decision-making', 'comprehensive', 'commander-wisdom', 'playbook', 'framework']
    )
    print("✅ 3/4: Decision framework added")
    
    # 4. Mission Compilation Methodology
    memory.share_learning(
        title="Mission Compilation Methodology - Large-Scale Synthesis",
        content="""# How to Compile Findings from 75+ Different Analyses

**Challenge:** Synthesize 75 individual repo analyses into coherent strategy
**Scope:** 8 agents analyzing simultaneously, different perspectives  
**Goal:** Comprehensive report with patterns, recommendations, execution plan

## Compilation Process:

### Phase 1: Real-Time Tracking
**Maintain MISSION_TRACKER with live progress:**
- Update as each agent completes repos
- Track discoveries (JACKPOTs, goldmines, moderate, deletes)
- Monitor velocity and agent performance
- Identify patterns as they emerge

**Tools:**
- MISSION_TRACKER_75_REPOS.md (live dashboard)
- Per-agent completion tracking
- Discovery categorization (JACKPOT vs moderate vs delete)

### Phase 2: Pattern Recognition
**Look for:**
- **Clusters:** Similar repos together (e.g., 3 trading repos #15, #16, #17)
- **Specialist strengths:** Agent-6 finds "trash tier gold", Agent-2 finds goldmines
- **Integration opportunities:** DreamVault 40% integrated already
- **Complementary systems:** DreamVault + TROOP + trading-leads = infrastructure suite

**Key Insight:** Different agents find different types of value!

### Phase 3: Strategic Synthesis
**Group and analyze:**
- By value tier (JACKPOT 7.5+, goldmine 6.0-7.5, moderate 3.0-6.0, low <3.0, delete 0.0)
- By integration effort (quick wins <50hr, medium 50-150hr, large 150hr+)
- By strategic fit (mission-aligned vs general utility)
- Calculate total ROI (e.g., Agent-2: 330-445hr across 4 goldmines)

### Phase 4: Comprehensive Report Structure
**Executive Summary:**
- Top 10 discoveries
- Total repos analyzed
- LEGENDARY agent performances
- Critical findings (migration framework, V1 origin, etc.)

**By-Agent Breakdown:**
- What each agent found
- Discovery patterns
- Specialist expertise applied
- Performance ratings

**Integration Roadmap:**
- Phased approach (Quick wins → Foundation → Full suite)
- Effort estimates per phase
- Dependencies mapped
- Execution timeline

**Recovery Plan:**
- Backup strategy (what if integration fails?)
- Reversibility (can we undo?)
- Risk mitigation

**Democratic Decision Framework:**
- Present all options
- Provide data for informed voting
- Facilitate swarm consensus

## Real-Time vs Post-Mission:

**During Mission:**
- Track in real-time (don't wait for all 75!)
- Recognize patterns as they emerge
- Celebrate milestones (50%, LEGENDARY completions)
- Maintain GROUND ability (pause when Commander directs)

**After Mission:**
- Compile comprehensive findings
- Synthesize strategic recommendations
- Present to Commander for final decision
- Execute approved strategy

## Key Insights:
1. Real-time tracking prevents information loss
2. Agent patterns emerge (different discovery styles)
3. Strategic fit matters more than raw metrics
4. Commander wisdom guides major decisions
5. GROUND command allows course correction

**Example:** 75-repo GitHub consolidation mission - tracked 28/75 so far with 2 LEGENDARY agents

**Date:** 2025-10-15
**Author:** Captain Agent-4
""",
        tags=['compilation', 'methodology', 'captain', 'large-scale', 'synthesis', 'strategic']
    )
    print("✅ 4/4: Compilation methodology added")
    
    print("\n🎯 CAPTAIN KNOWLEDGE TRANSFER COMPLETE!")
    print("Added 4 HIGH priority strategic knowledge entries to Swarm Brain")
    print("All agents can now access via: memory.search_swarm_knowledge('captain')")

if __name__ == "__main__":
    add_captain_knowledge()

