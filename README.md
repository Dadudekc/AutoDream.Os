# Agent Cellphone V2 - Swarm Intelligence System

## 🐝 **WE ARE SWARM: Multi-Agent Coordination System**

A sophisticated multi-agent system with 8 autonomous agents positioned across dual monitors, enabling real-time coordination through PyAutoGUI automation and Discord integration.

## 🎯 **System Overview**

### **Swarm Architecture**
- **8 Autonomous Agents** positioned at specific pixel coordinates
- **Dual Monitor Setup** for optimal agent distribution
- **Real-Time Coordination** through PyAutoGUI automation
- **Discord Integration** for enhanced communication
- **Vector Database** for swarm intelligence and knowledge sharing

### **Agent Specializations**
- **Agent-1**: Architecture Foundation Specialist (Team Alpha)
- **Agent-2**: Architecture & Design Specialist (Team Alpha)
- **Agent-3**: Database Specialist (Team Alpha)
- **Agent-4**: Captain & Operations Coordinator (Team Alpha)
- **Agent-5**: Quality Assurance Specialist (Team Beta)
- **Agent-6**: Integration Specialist (Team Beta)
- **Agent-7**: Testing Specialist (Team Beta)
- **Agent-8**: Documentation Specialist (Team Beta)

## 🚀 **Quick Start**

### **For New Agents**
1. **Read the Captain Handbook**: `docs/CAPTAIN_HANDBOOK.md`
2. **Follow Onboarding Guide**: `docs/CAPTAIN_ONBOARDING_GUIDE.md`
3. **Check Agent Guidelines**: `docs/CAPTAIN_AUTONOMOUS_PROTOCOL.md`
4. **Access V3 Web Dashboard**: `web_dashboard/` (React-based real-time monitoring)

### **V3 Pipeline Status: 100% COMPLETE ✅**
- **V3-001**: Cloud Infrastructure Setup ✅ COMPLETED
- **V3-004**: Distributed Tracing Implementation ✅ COMPLETED
- **V3-007**: ML Pipeline Setup ✅ COMPLETED
- **V3-010**: Web Dashboard Development ✅ COMPLETED

### **Phase 3 System Integration: READY 🚀**
- **Timeline**: 720-900 cycles for complete system integration
- **Focus**: Dream.OS native integration with all V3 components
- **Architecture Support**: Agent-1 ready to provide foundational guidance
- **Status**: All Phase 2 components ready for native integration

### **Essential Commands**
```bash
# Check agent status
python tools/simple_vector_search.py --agent Agent-4 --status

# Search swarm knowledge
python tools/simple_vector_search.py --query "Discord bot issues" --devlogs

# Run Discord commander
python simple_discord_commander.py

# Check V2 compliance
python check_v2_compliance.py

# Start V3 Web Dashboard
cd web_dashboard
npm install && npm start          # React frontend (port 3000)
python api.py                     # Flask API server (port 8000)
python websocket.py              # WebSocket server (port 8001)
```

## 🧠 **Vector Database Integration**

### **Automatic Knowledge Storage**
Every agent message is automatically stored in the vector database for semantic search and knowledge retrieval.

### **Search Commands**
```bash
# Search similar messages across all agents
python tools/simple_vector_search.py --query "your search term" --limit 5

# Search agent experiences
python tools/simple_vector_search.py --agent Agent-4 --query "consolidation" --devlogs

# Get agent knowledge summary
python tools/simple_vector_search.py --agent Agent-4 --knowledge-summary

# Get swarm knowledge summary
python tools/simple_vector_search.py --swarm-summary
```

## 🤖 **Discord Commander**

### **Features**
- **Slash Commands**: `/ping`, `/status`, `/help`, `/send`, `/swarm`
- **Agent Communication**: Send messages to specific agents
- **Swarm Broadcasting**: Send messages to all agents
- **Real-Time Status**: Monitor agent status and system health

### **Usage**
```bash
# Start Discord commander
python simple_discord_commander.py

# Available commands in Discord:
# /ping - Test bot responsiveness
# /status - Show system status
# /help - Show help information
# /send agent:Agent-1 message:Hello from Discord
# /swarm message:All agents report status
```

## 📁 **Project Structure**

```
├── src/                          # Source code
│   ├── services/                 # Core services
│   │   ├── messaging/           # Agent messaging system
│   │   ├── vector_database/     # Swarm intelligence
│   │   └── discord_bot/         # Discord integration
│   └── core/                    # Core functionality
├── tools/                       # Agent tools
├── docs/                        # Core documentation (4 files)
├── agent_workspaces/            # Agent workspaces
├── devlogs/                     # Agent devlogs
└── config/                      # Configuration files
```

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Discord Bot Configuration
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_channel_id

# Agent Channels
DISCORD_CHANNEL_AGENT_1=agent_1_channel_id
DISCORD_CHANNEL_AGENT_2=agent_2_channel_id
# ... (Agent-3 through Agent-8)
```

### **Coordinate System**
- **SSOT**: `config/coordinates.json`
- **8-Agent Mode**: Default for full swarm operations
- **Real-Time Updates**: Coordinate validation and routing

## 🧪 **Testing**

### **Run Tests**
```bash
# Run all tests
python run_tests.py

# Run specific test suites
python -m pytest tests/ -v

# Check V2 compliance
python check_v2_compliance.py
```

## 📚 **Documentation**

### **Core Documentation**
- **[Captain Handbook](docs/CAPTAIN_HANDBOOK.md)** - Complete system guide
- **[Onboarding Guide](docs/CAPTAIN_ONBOARDING_GUIDE.md)** - Agent onboarding
- **[Autonomous Protocol](docs/CAPTAIN_AUTONOMOUS_PROTOCOL.md)** - Agent protocols
- **[Cheatsheet](docs/CAPTAIN_CHEATSHEET.md)** - Quick reference

## 🐝 **Swarm Intelligence Features**

### **Collective Learning**
- **Automatic Message Storage**: All messages stored for semantic search
- **Experience Sharing**: Agents learn from each other's experiences
- **Pattern Recognition**: Identify recurring issues and solutions
- **Cross-Agent Learning**: Share expertise across the swarm

### **Benefits**
- **🧠 Swarm Intelligence**: Learn from all agents' experiences
- **🔍 Semantic Search**: Find similar problems and solutions
- **📚 Knowledge Retrieval**: Access past successful strategies
- **🤝 Cross-Agent Learning**: Share expertise across the swarm

## 🚀 **Getting Started**

1. **Clone the repository**
2. **Set up environment variables** (see Configuration section)
3. **Read the Captain Handbook** for complete system understanding
4. **Follow the Onboarding Guide** for agent setup
5. **Start with the Discord Commander** for basic operations
6. **Use Vector Database tools** for swarm intelligence

## 📝 **Contributing**

This is a multi-agent system. Each agent has specific responsibilities and protocols. See the documentation in the `docs/` directory for detailed information about agent roles and coordination protocols.

## 🐝 **WE ARE SWARM**

The system enables true swarm intelligence through:
- **Physical Automation**: Real-time coordination through PyAutoGUI
- **Collective Memory**: Vector database for shared knowledge
- **Democratic Decision Making**: All agents participate in architectural decisions
- **Self-Improving System**: Each agent's learning benefits the entire swarm

---

**Ready for swarm operations!** 🚀🐝
