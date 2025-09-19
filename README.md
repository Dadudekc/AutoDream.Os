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
- **Agent-1**: Integration & Core Systems Specialist
- **Agent-2**: Architecture & Design Specialist  
- **Agent-3**: Database & Data Management Specialist
- **Agent-4**: Captain & Operations Coordinator
- **Agent-5**: Business Intelligence & Analytics Specialist
- **Agent-6**: Communication & Coordination Specialist
- **Agent-7**: Python Development & Optimization Specialist
- **Agent-8**: Release & Deployment Captain

## 🚀 **Quick Start**

### **For New Agents**
1. **Read the Captain Handbook**: `docs/CAPTAIN_HANDBOOK.md`
2. **Follow Onboarding Guide**: `docs/CAPTAIN_ONBOARDING_GUIDE.md`
3. **Check Agent Guidelines**: `docs/CAPTAIN_AUTONOMOUS_PROTOCOL.md`

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
