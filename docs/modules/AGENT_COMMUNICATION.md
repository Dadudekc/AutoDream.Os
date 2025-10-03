# 📱 Agent Communication System
# =============================

**Purpose**: Agent-to-agent communication protocols and systems  
**Generated**: 2025-10-02  
**By**: Agent-7 (Implementation Specialist)  
**Status**: V2 COMPLIANT MODULE (≤400 lines)

---

## 📱 **AGENT-TO-AGENT COMMUNICATION**

### **PyAutoGUI Messaging System**

**Primary Communication Method**: Direct screen coordinate messaging using PyAutoGUI automation.

#### **Message Format**
```
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-X
📥 TO: Agent-Y
Priority: NORMAL/HIGH/URGENT
Tags: GENERAL/TASK/COORDINATION/EMERGENCY
------------------------------------------------------------
[Message Content]
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
------------------------------------------------------------
🎯 QUALITY GUIDELINES REMINDER
============================================================
📋 V2 Compliance Requirements:
• File Size: ≤400 lines (hard limit)
• Enums: ≤3 per file
• Classes: ≤5 per file
• Functions: ≤10 per file
• Complexity: ≤10 cyclomatic complexity per function
• Parameters: ≤5 per function
• Inheritance: ≤2 levels deep
============================================================
------------------------------------------------------------
```

#### **Message Types**
- **GENERAL**: General communication and coordination
- **TASK**: Task assignments and updates
- **COORDINATION**: Swarm coordination and planning
- **EMERGENCY**: Critical issues requiring immediate attention

#### **Priority Levels**
- **NORMAL**: Standard communication
- **HIGH**: Important but not urgent
- **URGENT**: Requires immediate attention

### **Discord Integration**

**Secondary Communication Method**: Discord bot for enhanced communication and monitoring.

#### **Discord Commands**
- `/send_message <agent> <message>` - Send message to specific agent
- `/run_scan <mode>` - Run project scanner
- `/fix_violations` - Fix V2 compliance violations
- `/agent_status` - Get status of all agents
- `/custom_task <agent> <task>` - Assign custom task to agent

#### **Discord Features**
- **Real-time Status Updates**: Live agent status monitoring
- **Command Execution**: Direct agent control via Discord
- **Notification System**: Automated alerts and updates
- **Log Integration**: Discord devlog posting

---

## 🤖 **AGENT COORDINATION PROTOCOLS**

### **Captain Agent-4 Coordination**

**Primary Coordinator**: Agent-4 (Captain) manages all agent coordination.

#### **Coordination Responsibilities**
- **Role Assignment**: Dynamic role assignment based on task requirements
- **Task Distribution**: Assigning tasks to appropriate agents
- **Emergency Response**: Coordinating emergency interventions
- **Performance Monitoring**: Tracking agent performance and health
- **Quality Assurance**: Ensuring V2 compliance across all agents

#### **Coordination Commands**
- **Role Assignment**: `python messaging_cli.py --agent <agent> --role <role>`
- **Task Assignment**: `python messaging_cli.py --agent <agent> --task <task>`
- **Status Check**: `python messaging_cli.py --agent <agent> --status`
- **Emergency Alert**: `python messaging_cli.py --agent <agent> --urgent <message>`

### **Agent-5 Coordinator Role**

**Secondary Coordinator**: Agent-5 (Coordinator) assists with coordination tasks.

#### **Coordination Support**
- **Inter-agent Communication**: Facilitating communication between agents
- **Task Coordination**: Coordinating multi-agent tasks
- **Status Reporting**: Collecting and reporting agent status
- **Coordination Updates**: Providing coordination updates to Captain

---

## 📊 **COMMUNICATION MONITORING**

### **Message Tracking**
- **Message Count**: Track total messages sent/received
- **Response Time**: Monitor response times between agents
- **Success Rate**: Track successful message delivery
- **Error Rate**: Monitor communication errors and failures

### **Performance Metrics**
- **Communication Efficiency**: Messages per cycle
- **Coordination Effectiveness**: Task completion rate
- **Response Quality**: Quality of agent responses
- **System Health**: Overall communication system health

### **Monitoring Tools**
- **Message Logs**: Comprehensive message logging
- **Performance Dashboards**: Real-time performance monitoring
- **Alert System**: Automated alerts for communication issues
- **Health Checks**: Regular communication system health checks

---

## 🔄 **COMMUNICATION WORKFLOWS**

### **Standard Communication Flow**
1. **Message Creation**: Agent creates message with proper format
2. **Message Routing**: Message routed to target agent via PyAutoGUI
3. **Message Delivery**: Target agent receives and processes message
4. **Response Generation**: Target agent generates appropriate response
5. **Response Delivery**: Response sent back to originating agent
6. **Status Update**: Communication status updated in system

### **Emergency Communication Flow**
1. **Emergency Detection**: Critical issue detected
2. **Emergency Alert**: Emergency message sent to Captain
3. **Captain Response**: Captain evaluates and coordinates response
4. **Agent Activation**: Relevant agents activated for emergency response
5. **Coordination**: Agents coordinate emergency response
6. **Resolution**: Emergency resolved and status updated

### **Task Assignment Flow**
1. **Task Identification**: Task identified for assignment
2. **Agent Selection**: Appropriate agent selected based on capabilities
3. **Task Assignment**: Task assigned to selected agent
4. **Task Execution**: Agent executes assigned task
5. **Progress Updates**: Regular progress updates during execution
6. **Task Completion**: Task completed and status reported

---

## 🛠️ **COMMUNICATION TOOLS**

### **Messaging CLI**
- **Purpose**: Command-line interface for agent messaging
- **Features**: Send messages, check status, assign tasks
- **Usage**: `python messaging_cli.py --help`

### **Discord Commander**
- **Purpose**: Discord bot for agent control and monitoring
- **Features**: Slash commands, real-time monitoring, notifications
- **Usage**: `/agent_status`, `/send_message`, `/run_scan`

### **Consolidated Messaging Service**
- **Purpose**: Centralized messaging service for all agents
- **Features**: Message routing, delivery confirmation, error handling
- **Integration**: PyAutoGUI, Discord, internal systems

---

## 📋 **COMMUNICATION BEST PRACTICES**

### **Message Formatting**
- **Consistent Structure**: Use standard message format
- **Clear Priority**: Set appropriate priority levels
- **Proper Tags**: Use correct message tags
- **Complete Information**: Include all necessary information

### **Response Guidelines**
- **Timely Responses**: Respond within cycle time limits
- **Clear Communication**: Use clear and concise language
- **Status Updates**: Provide regular status updates
- **Error Reporting**: Report errors and issues promptly

### **Coordination Principles**
- **Captain Authority**: Respect Captain's coordination authority
- **Role Compliance**: Follow assigned role protocols
- **Team Collaboration**: Work collaboratively with other agents
- **Quality Standards**: Maintain V2 compliance standards

---

🐝 **WE ARE SWARM** - Seamless communication for autonomous coordination

