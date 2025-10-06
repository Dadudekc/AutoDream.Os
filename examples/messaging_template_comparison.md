# 📱 Messaging Template Comparison Guide

**Overview**: Three messaging template styles for different communication scenarios in the agent system.

---

## 📊 **Template Comparison Table**

| Feature | Minimal | Compact | Full |
|---------|---------|---------|------|
| **Lines** | 16 | 26 | 48 |
| **Characters** | 775 | 1406 | 2560 |
| **Quality Gates** | Basic | Complete | Complete + Details |
| **Database Integration** | Core Commands | All Databases | Full Integration |
| **Tool Discovery** | None | Key Tools | Complete System |
| **Cycle Execution** | Essential | Complete | Detailed Phases |
| **Use Case** | Quick Messages | Standard Communication | Complex Missions |

---

## 🎯 **When to Use Each Template**

### **Minimal Template (16 lines)**
```
✅ Quick acknowledgments
✅ Space-limited scenarios  
✅ High-frequency messages
✅ Emergency communications
❌ Complex task assignments
❌ Role onboarding
❌ System integration projects
```

### **Compact Template (26 lines)**
```
✅ Standard communications
✅ Task assignments
✅ Status updates
✅ Coordination messages
✅ Most common use cases
❌ Complex missions
❌ Training scenarios
```

### **Full Template (48 lines)**
```
✅ Complex task assignments
✅ Role onboarding
✅ System integration projects
✅ Training scenarios
✅ Strategic planning
❌ Quick acknowledgments
❌ Space-limited scenarios
```

---

## 🔧 **Usage Examples**

### **Minimal Template**
```python
# Quick acknowledgment
formatter.format_a2a_message(
    'Agent-4', 'Agent-3', 
    'Task completed successfully', 
    'NORMAL', 
    minimal=True
)
```

### **Compact Template**
```python
# Standard communication
formatter.format_a2a_message(
    'Agent-4', 'Agent-3',
    'Analyze project and provide recommendations',
    'HIGH',
    compact=True
)
```

### **Full Template**
```python
# Complex mission
formatter.format_a2a_message(
    'Agent-4', 'Agent-3',
    'Comprehensive integration analysis with full system utilization',
    'CRITICAL'
    # compact=False is default
)
```

---

## 📋 **Feature Comparison**

### **Quality Gates**
- **Minimal**: `V2 compliance • Run quality_gates.py`
- **Compact**: Complete V2 guidelines with KISS principles
- **Full**: Complete guidelines with detailed restrictions and best practices

### **Database Integration**
- **Minimal**: Core commands only (`r.search`, `sqlite3`, `VectorDatabaseIntegration`)
- **Compact**: All databases with access methods
- **Full**: Complete integration with examples and usage patterns

### **Tool Discovery**
- **Minimal**: None
- **Compact**: Key tools (`scan_tools.py`, `find_tool.py`, `run_project_scan.py`)
- **Full**: Complete system (Captain tools, analysis tools, messaging systems)

### **Cycle Execution**
- **Minimal**: Essential cycle order with kickoff
- **Compact**: Complete cycle with kickoff instruction
- **Full**: Detailed phases with database integration per phase

---

## 🚀 **Performance Considerations**

### **Message Processing Time**
- **Minimal**: Fastest (minimal content to parse)
- **Compact**: Moderate (balanced content)
- **Full**: Slower (comprehensive content)

### **Agent Processing**
- **Minimal**: Quick acknowledgment and action
- **Compact**: Standard processing with tool integration
- **Full**: Comprehensive analysis and system utilization

### **Network/Storage Impact**
- **Minimal**: Minimal bandwidth and storage usage
- **Compact**: Moderate impact
- **Full**: Higher bandwidth and storage requirements

---

## 💡 **Recommendations**

### **Default Choice: Compact Template**
- Best balance of information and efficiency
- Suitable for 80% of agent communications
- Provides complete autonomous operation support

### **Use Minimal When:**
- Message length is constrained
- Quick acknowledgments are needed
- High-frequency communications
- Emergency scenarios

### **Use Full When:**
- Complex missions requiring comprehensive guidance
- Role onboarding and training
- System integration projects
- Strategic planning scenarios

---

## 🔄 **Migration Path**

1. **Start with Compact**: Use compact template for standard communications
2. **Add Minimal**: Implement minimal for quick acknowledgments
3. **Include Full**: Add full template for complex missions
4. **Monitor Usage**: Track which template works best for different scenarios
5. **Optimize**: Adjust template selection based on agent performance

---

**Summary**: Choose the template that provides the right level of guidance for your communication scenario while maintaining efficiency and agent autonomy.
