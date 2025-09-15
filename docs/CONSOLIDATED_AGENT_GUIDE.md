# 🤖 **CONSOLIDATED AGENT COORDINATION GUIDE**

## 🎯 **Agent System Overview**

The AutoDream OS uses an 8-agent swarm system with coordinate-based positioning across multiple monitors for real-time coordination through PyAutoGUI automation.

### **Agent Roles & Coordinates**
```
Monitor 1 (Left Screen):     Monitor 2 (Right Screen):
┌─────────────────┐         ┌─────────────────┐
│ Agent-1         │         │ Agent-5         │
│ (-1269, 481)    │         │ (652, 421)      │
│ Integration     │         │ Business Intel  │
├─────────────────┤         ├─────────────────┤
│ Agent-2         │         │ Agent-6         │
│ (-308, 480)     │         │ (1612, 419)     │
│ Architecture    │         │ Communication   │
├─────────────────┤         ├─────────────────┤
│ Agent-3         │         │ Agent-7         │
│ (-1269, 1001)   │         │ (653, 940)      │
│ Infrastructure  │         │ Web Development │
├─────────────────┤         ├─────────────────┤
│ Agent-4         │         │ Agent-8         │
│ (-308, 1000)    │         │ (1611, 941)     │
│ Captain         │         │ SSOT Integration│
└─────────────────┘         └─────────────────┘
```

## 🚀 **Quick Start Commands**

### **Agent Communication**
```bash
# Send message to specific agent
python -m src.services.messaging --agent Agent-1 --message "Hello Agent-1!"

# Broadcast to all agents
python -m src.services.messaging --bulk --message "System broadcast"

# Get next task for agent
python -m src.services.messaging --get-next-task --agent Agent-7
```

### **Coordinate Management**
```bash
# View coordinate mapping
python -m src.services.messaging --coordinates

# Validate coordinates
python -m src.services.messaging --validate
```

## 📊 **Agent Status Monitoring**

Each agent maintains a status file at `agent_workspaces/{Agent-X}/status.json` with:
- Current mission and tasks
- Completed achievements
- Next actions
- Performance metrics

## 🔧 **System Requirements**

- **Python 3.8+**
- **PyAutoGUI** for coordinate automation
- **Multi-monitor setup** for full swarm operations
- **Cursor IDE** for agent positioning

## 📚 **Additional Resources**

- [API Reference](API_REFERENCE.md)
- [Development Guide](DEVELOPER_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Architecture Overview](ARCHITECTURE.md)

---
*For detailed agent capabilities and advanced coordination, see the individual agent documentation in the archive.*