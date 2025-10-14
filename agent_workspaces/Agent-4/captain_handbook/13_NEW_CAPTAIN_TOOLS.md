# ⚡ CHAPTER 13: NEW CAPTAIN TOOLS

**Read Time:** 4 minutes  
**Priority:** 🔴 CRITICAL (NEW!)  
**Date Added:** 2025-10-14

---

## 🎯 **MAJOR TOOLBELT EXPANSION**

**Growth:** 91 → 106 tools (+16%)  
**New Tools:** 10 specialized tools for democratic innovation & coordination

---

## 🏛️ **PROPOSAL TOOLS (5 TOOLS)**

### **Democratic Innovation Infrastructure**

Enable swarm-wide democratic decision-making through structured proposals.

---

### **1. proposal.create**

**Purpose:** Initialize new proposal topic

**When to Use:**
- Need swarm input on major decision
- Multiple valid approaches exist
- Democratic buy-in important for success

**Usage:**
```python
from tools_v2.toolbelt_core import ToolbeltCore
tb = ToolbeltCore()

result = tb.run('proposal.create', {
    'topic_id': 'testing_strategy',
    'title': 'Testing Strategy for V2 Compliance',
    'description': 'How should we ensure 85%+ test coverage?',
    'requirements': [
        'Must achieve 85%+ coverage',
        'Must be maintainable',
        'Must integrate with CI/CD'
    ],
    'deadline_hours': 48
})
```

**Output:** Topic created, all agents notified

---

### **2. proposal.list**

**Purpose:** View all proposals for a topic

**When to Use:**
- Review what proposals have been submitted
- Count participation
- Prepare for voting

**Usage:**
```python
result = tb.run('proposal.list', {
    'topic': 'orientation_system'
})

# Returns: List of all proposal files with metadata
# Example: 8 proposals for orientation_system
```

**Output:** Array of proposals with agent_id, title, filename

---

### **3. proposal.view**

**Purpose:** Read specific proposal details

**When to Use:**
- Deep-dive into specific proposal
- Review proposal before voting
- Compare different approaches

**Usage:**
```python
result = tb.run('proposal.view', {
    'topic': 'orientation_system',
    'filename': 'Agent-6_intelligent_orientation_pathways.md'
})

# Returns: Full proposal content
```

**Output:** Complete proposal markdown content

---

### **4. proposal.contribute**

**Purpose:** Submit your proposal to a topic

**When to Use:**
- You have a solution to propose
- Want to participate in democratic process
- Ready to share your approach

**Usage:**
```python
result = tb.run('proposal.contribute', {
    'topic': 'orientation_system',
    'agent_id': 'Agent-4',
    'title': 'Comprehensive Orientation Index',
    'content': '''
# Comprehensive Orientation Index

## Problem Statement
...

## Proposed Solution
...

## Benefits
...
'''
})
```

**Output:** Proposal file created, swarm notified

---

### **5. proposal.debate**

**Purpose:** Start democratic debate and voting

**When to Use:**
- Proposals submitted (minimum 2)
- Ready for swarm decision
- Need democratic consensus

**Usage:**
```python
result = tb.run('proposal.debate', {
    'topic': 'orientation_system',
    'question': 'Which orientation approach should we implement?',
    'duration_hours': 24,
    'options': [
        'Individual Approach (pick one)',
        'Integration Approach (combine all)',
        'Hybrid (start one, add others)'
    ]
})
```

**Output:** Debate started, voting period active

---

## 👨‍✈️ **CAPTAIN TOOLS (5 TOOLS)**

### **Enhanced Coordination Capabilities**

Powerful tools for monitoring, coordinating, and activating the swarm.

---

### **1. captain.track_progress**

**Purpose:** Monitor agent progress across missions

**When to Use:**
- Daily swarm health check
- Identify blockers early
- Track completion rates
- Monitor points earned

**Usage:**
```python
result = tb.run('captain.track_progress', {
    'agent_ids': ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-5', 
                  'Agent-6', 'Agent-7', 'Agent-8'],
    'time_range': '24h',
    'include_metrics': True
})

# Returns: Progress percentages, blockers, points earned
```

**Output:**
```json
{
  "Agent-1": {
    "progress": 75,
    "current_task": "Testing pyramid",
    "blockers": [],
    "points_earned": 300
  },
  ...
}
```

**Integration:** Use daily as part of Captain's monitoring duties (Chapter 08)

---

### **2. captain.create_mission**

**Purpose:** Create new mission assignments

**When to Use:**
- Assigning new tasks to agents
- Creating structured missions
- Documenting mission details

**Usage:**
```python
result = tb.run('captain.create_mission', {
    'mission_id': 'M-042',
    'title': 'V2 Compliance - Error Handling',
    'agent_id': 'Agent-3',
    'priority': 'high',
    'value_range': '800-1000pts',
    'roi': 25.5,
    'details': '''
    Refactor error_handling_core.py to V2 compliance.
    Target: <400 lines, 100% type hints, 85%+ coverage.
    ''',
    'deliverables': [
        'File <400 lines',
        'Tests passing',
        'Documentation updated'
    ]
})
```

**Output:** Mission file created in agent's inbox

**Integration:** Use with messaging system (Chapter 06) to activate agent

---

### **3. captain.batch_onboard**

**Purpose:** Onboard multiple agents simultaneously

**When to Use:**
- Starting new cycle with all agents
- Swarm-wide activation
- Coordinated mission launches

**Usage:**
```python
result = tb.run('captain.batch_onboard', {
    'agents': [
        {
            'agent_id': 'Agent-1',
            'role': 'Testing & QA Specialist',
            'mission': 'Testing pyramid implementation',
            'tools': 12,
            'value': '800-1200pts'
        },
        {
            'agent_id': 'Agent-2',
            'role': 'V2 Compliance',
            'mission': 'Architecture excellence',
            'tools': 15,
            'value': '1000-1500pts'
        },
        # ... all 8 agents
    ],
    'mode': 'hard',  # or 'soft'
    'send_activation': True  # PyAutoGUI messages
})
```

**Output:** All agents onboarded, activation messages sent

**Time Saved:** 7x faster than individual onboarding!

---

### **4. captain.swarm_status**

**Purpose:** Comprehensive swarm health check

**When to Use:**
- Start of cycle (morning check)
- Before major decisions
- After significant events
- Daily monitoring

**Usage:**
```python
result = tb.run('captain.swarm_status', {
    'include_metrics': True,
    'include_blockers': True,
    'include_health': True,
    'time_range': '24h'
})

# Returns: Complete swarm state
```

**Output:**
```json
{
  "total_agents": 8,
  "active_agents": 8,
  "idle_agents": 0,
  "blocked_agents": 0,
  "swarm_health": "EXCELLENT",
  "total_points_earned": 4200,
  "average_roi": 18.5,
  "critical_issues": [],
  "agent_statuses": {
    "Agent-1": "WORKING",
    "Agent-2": "WORKING",
    ...
  }
}
```

**Integration:** Perfect for daily checklist (Chapter 05)

---

### **5. captain.activate_agent**

**Purpose:** Activate specific agent with PyAutoGUI

**When to Use:**
- Agent idle and needs activation
- Urgent mission assignment
- Targeted fuel delivery
- Emergency activation

**Usage:**
```python
result = tb.run('captain.activate_agent', {
    'agent_id': 'Agent-7',
    'message': '''
    🎯 URGENT: New high-value mission assigned!
    
    Mission: Knowledge base expansion
    Value: 800-1200pts
    ROI: 22.5
    
    Check inbox for full details. BEGIN NOW! 🐝
    ''',
    'priority': 'urgent',
    'delivery_method': 'pyautogui'  # Physical swarm activation
})
```

**Output:** PyAutoGUI message delivered to agent coordinates

**Integration:** Implements "Prompts are GAS" principle (Chapter 01)

---

## 📊 **TOOL USAGE WORKFLOW**

### **Daily Captain Cycle with New Tools:**

**Morning (Planning):**
```python
# 1. Check swarm status
swarm_status = tb.run('captain.swarm_status', {
    'include_metrics': True
})

# 2. Track progress from yesterday
progress = tb.run('captain.track_progress', {
    'agent_ids': ALL_AGENTS,
    'time_range': '24h'
})

# 3. Identify idle or blocked agents
# 4. Create missions for available agents
```

**Midday (Coordination):**
```python
# 1. Activate any idle agents
tb.run('captain.activate_agent', {
    'agent_id': 'Agent-X',
    'message': 'Activation message'
})

# 2. Monitor proposal progress (if active)
proposals = tb.run('proposal.list', {
    'topic': 'current_topic'
})

# 3. Track mission progress
```

**Evening (Review):**
```python
# 1. Final status check
final_status = tb.run('captain.swarm_status', {
    'include_metrics': True
})

# 2. Document in Captain's log
# 3. Plan next cycle
```

---

## 🎯 **INTEGRATION WITH EXISTING TOOLS**

### **Proposal Tools + Existing Systems:**

**Proposal Tools integrate with:**
- ✅ Debate system (democratic voting)
- ✅ Swarm Brain (proposals as knowledge)
- ✅ Messaging (coordination notifications)
- ✅ Documentation (structured proposals)

**Captain Tools integrate with:**
- ✅ Messaging system (Chapter 06)
- ✅ Monitoring tools (Chapter 08)
- ✅ Daily checklist (Chapter 05)
- ✅ Cycle workflow (Chapter 04)

---

## 📋 **BEST PRACTICES**

### **When to Use Proposal Tools:**

✅ **DO use for:**
- Major architectural decisions
- Multiple valid approaches exist
- Swarm buy-in critical
- Innovation opportunities

❌ **DON'T use for:**
- Emergency situations (no time)
- Obvious solutions (no debate needed)
- Captain-only decisions (operational choices)
- Trivial matters (overhead not justified)

### **When to Use Captain Tools:**

✅ **DO use daily:**
- `captain.swarm_status` - Every morning
- `captain.track_progress` - Multiple times daily
- `captain.activate_agent` - As needed

✅ **DO use weekly:**
- `captain.batch_onboard` - New cycle starts
- `captain.create_mission` - Regular assignments

---

## 🏆 **SUCCESS METRICS**

**Track effectiveness:**
- Proposal tools: % agent participation, decision quality
- Captain tools: Time saved, swarm health score, activation rate

**Expected improvements:**
- **Decision quality:** +30% (swarm intelligence)
- **Coordination efficiency:** +40% (batch operations)
- **Agent activation:** +50% (automated processes)
- **Monitoring coverage:** 100% (real-time status)

---

## ⚡ **QUICK REFERENCE**

| Tool | Use Case | Frequency |
|------|----------|-----------|
| **proposal.create** | Start new topic | As needed |
| **proposal.list** | Check submissions | Daily (active topic) |
| **proposal.view** | Review proposal | Before voting |
| **proposal.contribute** | Submit proposal | When have solution |
| **proposal.debate** | Start vote | When ready |
| **captain.swarm_status** | Health check | Daily (morning) |
| **captain.track_progress** | Monitor agents | Multiple/day |
| **captain.activate_agent** | Fuel agent | As needed |
| **captain.create_mission** | Assign task | Weekly |
| **captain.batch_onboard** | Mass activation | Per cycle |

---

## 🎯 **REMEMBER**

**These tools enable:**
- 🏛️ **Democratic innovation** (proposal tools)
- 👨‍✈️ **Enhanced coordination** (captain tools)
- 🐝 **Swarm intelligence** (collective decision-making)
- ⚡ **Operational efficiency** (automated processes)

**Use them to lead the swarm to unprecedented success!** 🚀

---

[← Previous: Emergency Protocols](./12_EMERGENCY_PROTOCOLS.md) | [Back to Index](./00_INDEX.md)

**#NEW_TOOLS #DEMOCRATIC_INNOVATION #CAPTAIN_COORDINATION**

