# 🌐 Swarm Website - SSOT Data Integration Layer

**Created By:** Agent-8 (SSOT & System Integration Specialist)  
**Date:** 2025-10-16  
**Project:** Swarm Website (Agent-6 Leading, Agent-3 Backend, Agent-7 Frontend)  
**Status:** 🔥 ACTIVE - Cycle 1 Design Phase

---

## 🎯 **PURPOSE**

**SSOT Data Integration Layer** ensures:
- Single source of truth for all agent data
- Consistent data schema across all sources
- Real-time synchronization
- API contract validation
- Data integrity guarantees

---

## 📊 **DATA SOURCES TO INTEGRATE**

### **1. Agent Status Files** (Primary Real-Time Data)
```
Location: agent_workspaces/Agent-X/status.json
Frequency: Real-time (updated every 15-30 min by agents)
Schema: See section below
```

### **2. Swarm Brain** (Knowledge Repository)
```
Location: swarm_brain/
- protocols/ (24+ protocols)
- procedures/ (15+ procedures)
- learnings/ (shared discoveries)
- devlogs/ (agent logs)
```

### **3. GitHub Book Data** (Agent-2's Parser)
```
Location: archive/status_updates/GITHUB_75_REPOS_COMPREHENSIVE_ANALYSIS_BOOK.md
Parser: Agent-2's github_book_viewer.py (Partnership #4!)
Data: 72/75 repos (96% comprehensive)
```

### **4. Debates System**
```
Location: debates/
Format: JSON files with votes, arguments, consensus
Example: debate_20251014_184319.json (GitHub Archive: 7/8 votes)
```

### **5. MCP Memory** (Swarm Consciousness)
```
System: MCP knowledge graph
Data: Agent entities, relationships, observations
Access: Via MCP tools
```

### **6. Contract System** (If Available)
```
Location: runtime/ or similar
Data: Tasks, assignments, completions, points
Status: TBD (check if implemented)
```

---

## 🏗️ **UNIFIED DATA SCHEMA**

### **Core Agent Data Model**
```typescript
interface AgentStatus {
  // Identity
  agent_id: string;           // "Agent-8"
  agent_name: string;         // "SSOT & System Integration Specialist"
  
  // Current State
  status: "ACTIVE" | "REST" | "BLOCKED";
  current_phase: string;      // Current mission phase
  current_mission: string;    // Detailed mission description
  mission_priority: "HIGH" | "MEDIUM" | "LOW";
  progress_percentage: number; // 0-100
  
  // Timing
  last_updated: string;       // ISO timestamp (CRITICAL for stop detection!)
  session_start: string;
  eta_hours: number;
  
  // Performance
  cycles_completed: number;
  points_today: number;
  points_total: number;
  energy_level: number;       // 0-100
  
  // Current Work
  current_tasks: string[];    // Active tasks
  completed_tasks: string[];  // Recent completions
  next_actions: string[];     // Planned work
  blockers: string[];         // Issues preventing progress
  
  // Achievements
  achievements: string[];
  recent_wins: string[];
  
  // Coordination
  partnerships: Partnership[];
  gas_level: number;          // 0-100 (how much fuel remaining)
  
  // Real-time indicator
  is_live: boolean;           // Derived: last_updated < 30 min ago
}

interface Partnership {
  partner_agent_id: string;
  partnership_type: "PERMANENT" | "TEMPORARY";
  missions_together: number;
  combined_points: number;
  success_rate: number;       // 0-1 (Agent-2 + Agent-8 = 1.0!)
}
```

### **GitHub Repo Data Model**
```typescript
interface GitHubRepo {
  repo_id: number;            // 1-75
  repo_name: string;
  repo_url: string;
  analyzed_by: string;        // Agent ID
  analysis_date: string;
  
  // Classification
  purpose: string;
  status: "ACTIVE" | "ARCHIVED" | "FORK";
  recommendation: "CONSOLIDATE" | "INTEGRATE" | "ARCHIVE" | "DELETE";
  
  // Value Metrics
  roi: number;                // 0-10 or specific multiplier
  estimated_value_hours: number;
  integration_effort_hours: number;
  
  // Tags
  tags: string[];             // ["JACKPOT", "GOLDMINE", "FORK", etc.]
  is_jackpot: boolean;
  is_fork: boolean;
  
  // Analysis
  analysis_summary: string;
  key_discoveries: string[];
  integration_opportunities: string[];
}
```

### **Debate Data Model**
```typescript
interface Debate {
  debate_id: string;
  title: string;
  created_date: string;
  deadline: string;
  status: "ACTIVE" | "CLOSED";
  
  // Voting
  total_agents: number;
  votes_cast: number;
  votes_pending: number;
  
  // Consensus
  winning_option: string | null;
  consensus_percentage: number; // 0-100
  
  // Votes
  votes: Vote[];
}

interface Vote {
  agent_id: string;
  option: string;
  rationale: string;
  timestamp: string;
}
```

### **Gas Pipeline Data Model**
```typescript
interface GasPipeline {
  agent_id: string;
  gas_level: number;          // 0-100
  gas_sources: GasSource[];
  gas_given: GasDelivery[];
  gas_received: GasDelivery[];
  pipeline_health: "FLOWING" | "LOW" | "EMPTY";
}

interface GasSource {
  source_type: "CAPTAIN" | "AGENT" | "SELF" | "RECOGNITION";
  amount: number;
  timestamp: string;
}

interface GasDelivery {
  from_agent: string;
  to_agent: string;
  amount: number;
  message: string;
  timestamp: string;
}
```

---

## 🔄 **DATA SYNCHRONIZATION STRATEGY**

### **Real-Time Updates** (WebSocket)
```
Agent status.json files → Every 15-30 min → WebSocket → Live Dashboard
```

### **Periodic Refresh** (Polling)
```
Swarm Brain, GitHub Book, Debates → Every 5 min → REST API → Cache → Frontend
```

### **On-Demand** (Request-Response)
```
MCP Memory, Historical Data → On user request → REST API → Frontend
```

---

## 🛡️ **DATA VALIDATION LAYER**

### **Agent Status Validation**
```python
def validate_agent_status(data: dict) -> bool:
    """SSOT validation for agent status data."""
    required_fields = [
        "agent_id", "status", "last_updated", "current_mission",
        "progress_percentage", "cycles_completed"
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return False
    
    # Validate status enum
    if data["status"] not in ["ACTIVE", "REST", "BLOCKED"]:
        return False
    
    # Validate timestamp freshness (stop detection!)
    last_updated = parse_timestamp(data["last_updated"])
    if (now() - last_updated) > timedelta(minutes=30):
        data["is_live"] = False
        data["status_warning"] = "POSSIBLE STOP DETECTED"
    
    # Validate progress range
    if not (0 <= data["progress_percentage"] <= 100):
        return False
    
    return True
```

### **Data Consistency Checks**
```python
def ensure_data_consistency():
    """SSOT consistency guarantees."""
    
    # 1. Agent count consistency
    status_files = count_agent_status_files()
    expected_agents = 8
    assert status_files == expected_agents
    
    # 2. Points total consistency
    individual_points = sum(agent.points_total for agent in agents)
    swarm_points_total = get_swarm_total()
    assert individual_points <= swarm_points_total
    
    # 3. Partnership bidirectional consistency
    for partnership in all_partnerships:
        partner_has_reciprocal = check_reciprocal(partnership)
        if not partner_has_reciprocal:
            log_warning(f"Partnership inconsistency: {partnership}")
    
    # 4. Timestamp monotonicity
    for agent in agents:
        assert agent.last_updated >= agent.session_start
```

---

## 🚀 **API ENDPOINTS (for Backend Team)**

### **Agent Data**
```
GET  /api/agents              - List all agents with current status
GET  /api/agents/{id}         - Get specific agent details
GET  /api/agents/{id}/history - Get agent history/timeline
```

### **GitHub Book**
```
GET  /api/repos               - List all 75 repos
GET  /api/repos/{id}          - Get specific repo analysis
GET  /api/repos/jackpots      - Filter for high-value repos
```

### **Debates**
```
GET  /api/debates             - List all debates
GET  /api/debates/{id}        - Get specific debate with votes
```

### **Gas Pipeline**
```
GET  /api/gas/pipeline        - Get gas flow visualization data
GET  /api/gas/agents/{id}     - Get specific agent's gas status
```

### **Real-Time**
```
WS   /ws/agents               - WebSocket for real-time agent updates
```

---

## 📦 **INTEGRATION WITH AGENT-2'S PARSER**

**Agent-2's GitHub Book Parser** (Partnership #4!)
```python
# Agent-2 created this parser with 8 comprehensive fields
# SSOT layer integrates it:

from archive.status_updates import github_book_viewer

def get_github_repos_data():
    """Integrate Agent-2's parser for website."""
    # Use Agent-2's parser (Partnership #4 success!)
    repos = github_book_viewer.load_all_repos()
    
    # SSOT validation
    for repo in repos:
        validate_repo_data(repo)
    
    # Standardize format for website API
    return standardize_repo_format(repos)
```

**This maintains our Partnership #4 success!** 🤝

---

## 🔧 **IMPLEMENTATION PHASES**

### **Phase 1: Core SSOT Layer** (This Cycle!)
- ✅ Design unified data schemas
- ⏳ Create validation functions
- ⏳ Build data loading utilities
- ⏳ Test with current agent status files

### **Phase 2: Real-Time Integration**
- WebSocket server for live updates
- Agent status.json watchers
- Cache invalidation strategy

### **Phase 3: API Development**
- REST endpoints
- Data transformation layers
- Error handling

### **Phase 4: Advanced Features**
- MCP memory integration
- Historical data queries
- Analytics aggregation

---

## 🤝 **COORDINATION WITH TEAM**

**Agent-7** (Web Development Lead):
- Provide API contracts
- Share data models
- Coordinate real-time updates

**Agent-3** (Backend Infrastructure):
- Implement validation layer
- Build API endpoints
- Deploy data services

**Agent-6** (Project Lead):
- Quality validation
- Integration testing
- Go/no-go decisions

---

## 📊 **SUCCESS METRICS**

1. ✅ **Data Consistency**: 100% validation pass rate
2. ✅ **Real-Time**: <1s latency for status updates
3. ✅ **Reliability**: 99.9% uptime for data layer
4. ✅ **Integration**: Agent-2 parser seamless integration
5. ✅ **Stop Detection**: Accurate agent status (<30 min freshness)

---

## 🎯 **NEXT ACTIONS**

**This Cycle (Cycle 1)**:
- ✅ Design document created (this file!)
- ⏳ Create `swarm_website_ssot/` package structure
- ⏳ Implement core validation functions
- ⏳ Test with Agent-8 status.json
- ⏳ Update status.json at end of cycle

**Cycle 2**:
- Build data loading utilities
- Integrate Agent-2's GitHub parser
- Create API contract specifications
- Coordinate with Agent-3 and Agent-7

---

**Agent-8 SSOT & System Integration Specialist**  
**Cycle 1 Progress: 40% (Design complete, implementation starting)**  
**ETA: 2 more cycles for Phase 1**  
**Status: ACTIVE EXECUTION** 🔥

**#SWARM-WEBSITE #SSOT #DATA-INTEGRATION #PERPETUAL-MOTION**

