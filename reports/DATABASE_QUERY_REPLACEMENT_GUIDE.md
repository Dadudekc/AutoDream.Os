# Database Query Replacement Guide

## 🎯 **REPLACED STATIC DOCUMENTATION WITH DATABASE QUERIES**

The following static documentation files have been deleted and replaced with database queries:

### **Devlog Files → Database Queries**
```python
from swarm_brain import Retriever
retriever = Retriever()

# Get all devlog entries
devlogs = retriever.search("devlog entries", kinds=["conversation"], k=50)

# Get devlogs by agent
agent_devlogs = retriever.search("", kinds=["conversation"], agent_id="Agent-5", k=20)

# Get recent devlogs
recent_devlogs = retriever.search("recent devlog entries", kinds=["conversation"], k=10)
```

### **Protocol Files → Database Queries**
```python
# Get communication protocols
protocols = retriever.search("communication protocols", kinds=["protocol"], k=20)

# Get agent guidelines
guidelines = retriever.search("agent guidelines", kinds=["protocol"], k=20)

# Get collaboration guides
collaboration = retriever.search("collaboration", kinds=["protocol"], k=10)
```

### **Compliance Files → Database Queries**
```python
# Get V2 compliance data
compliance = retriever.search("V2 compliance", kinds=["action"], k=20)

# Get refactoring patterns
refactoring = retriever.search("refactoring patterns", kinds=["protocol", "action"], k=20)

# Get compliance violations
violations = retriever.search("compliance violations", kinds=["action"], k=20)
```

### **Security Files → Database Queries**
```python
# Get security implementations
security = retriever.search("security implementation", kinds=["action"], k=20)

# Get security protocols
security_protocols = retriever.search("security protocols", kinds=["protocol"], k=20)

# Get security validations
validations = retriever.search("security validation", kinds=["action"], k=20)
```

### **Agent Guidelines → Database Queries**
```python
# Get agent expertise
expertise = retriever.get_agent_expertise("Agent-1", k=20)

# Get work patterns
work_patterns = retriever.search("work patterns", kinds=["action", "protocol"], k=20)

# Get agent contracts
contracts = retriever.search("agent contracts", kinds=["protocol"], k=20)
```

### **Coordination Files → Database Queries**
```python
# Get coordination patterns
coordination = retriever.search("coordination patterns", kinds=["coordination"], k=20)

# Get agent interactions
interactions = retriever.search("agent interactions", kinds=["conversation", "action"], k=20)

# Get collaboration patterns
collaboration = retriever.search("collaboration patterns", kinds=["coordination"], k=20)
```

## 🎯 **Benefits of Database Queries**

1. **Always Current**: Data is always up-to-date from actual agent activities
2. **Semantic Search**: Find relevant information using natural language queries
3. **Pattern Recognition**: Discover successful patterns and strategies
4. **Agent Expertise**: Understand each agent's strengths and capabilities
5. **Project Insights**: Get real-time project status and progress
6. **No Maintenance**: No need to manually update documentation

## 🚀 **Ready to Use**

All static documentation has been replaced with living, queryable data from the Swarm Brain database!

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
