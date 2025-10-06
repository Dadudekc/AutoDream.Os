# API Documentation - Agent Cellphone V2 Repository

**Version**: 2.0.0  
**Last Updated**: 2025-10-05  
**Agent**: Agent-7 (Elevated Web Development Expert)  

## 🌟 **Overview**

This comprehensive API documentation covers all service interfaces, endpoints, and integration points in the Agent Cellphone V2 Repository. The system provides multiple API layers including Discord Commander REST APIs, agent communication interfaces, Thea consultation APIs, and web-based control interfaces.

## 📡 **API Architecture**

### **API Layers**

1. **Discord Commander REST API** - Web-based control interface
2. **Agent Communication API** - Inter-agent messaging and coordination
3. **Thea Consultation API** - Strategic consultation and autonomous communication
4. **Project Scanner API** - Code analysis and quality assessment
5. **Quality Assurance API** - V2 compliance and testing interfaces
6. **Messaging Service API** - Consolidated messaging and coordination

## 🤖 **Discord Commander REST API**

### **Base URL**: `http://localhost:8080`

### **Agent Management Endpoints**

#### **GET /api/agents**
Get status of all agents in the system.

**Response**:
```json
{
  "agents": {
    "Agent-1": {"status": "active", "last_seen": "2025-10-05T10:30:00Z"},
    "Agent-2": {"status": "active", "last_seen": "2025-10-05T10:29:45Z"},
    "Agent-3": {"status": "active", "last_seen": "2025-10-05T10:29:30Z"},
    "Agent-4": {"status": "active", "last_seen": "2025-10-05T10:29:15Z"},
    "Agent-5": {"status": "active", "last_seen": "2025-10-05T10:29:00Z"},
    "Agent-6": {"status": "active", "last_seen": "2025-10-05T10:28:45Z"},
    "Agent-7": {"status": "active", "last_seen": "2025-10-05T10:28:30Z"},
    "Agent-8": {"status": "active", "last_seen": "2025-10-05T10:28:15Z"}
  },
  "timestamp": "2025-10-05T10:30:00Z"
}
```

#### **POST /api/send_message**
Send a message to a specific agent.

**Request Body**:
```json
{
  "agent": "Agent-7",
  "message": "Task completed successfully",
  "priority": "NORMAL"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Message sent successfully",
  "timestamp": "2025-10-05T10:30:00Z"
}
```

#### **POST /api/broadcast_message**
Broadcast a message to all agents.

**Request Body**:
```json
{
  "message": "System maintenance scheduled",
  "priority": "HIGH"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Message broadcast to all agents",
  "timestamp": "2025-10-05T10:30:00Z"
}
```

#### **GET /api/system_status**
Get overall system status.

**Response**:
```json
{
  "status": {
    "discord_bot": "connected",
    "agents_active": 8,
    "system_health": "excellent",
    "last_activity": "2025-10-05T10:30:00Z"
  },
  "timestamp": "2025-10-05T10:30:00Z"
}
```

#### **GET /api/channels**
Get Discord channels information.

**Response**:
```json
{
  "channels": [
    {"id": "123456789", "name": "general", "type": "text"},
    {"id": "987654321", "name": "agent-coordination", "type": "text"}
  ],
  "timestamp": "2025-10-05T10:30:00Z"
}
```

### **WebSocket Events**

#### **Connection**
```javascript
const socket = io('http://localhost:8080');
```

#### **Agent Status Updates**
```javascript
socket.on('agent_status_update', (data) => {
  console.log('Agent status updated:', data);
});
```

#### **Message Events**
```javascript
socket.on('message_received', (data) => {
  console.log('Message received:', data);
});
```

## 📨 **Agent Communication API**

### **Messaging System**

#### **Send Message**
```python
python messaging_system.py <from_agent> <to_agent> "<message>" <priority>
```

**Parameters**:
- `from_agent`: Source agent identifier (Agent-1 to Agent-8)
- `to_agent`: Target agent identifier (Agent-1 to Agent-8)
- `message`: Message content (string)
- `priority`: Message priority (NORMAL, HIGH, CRITICAL)

**Example**:
```bash
python messaging_system.py Agent-7 Agent-4 "Task completed successfully" NORMAL
```

#### **Devlog System**
```python
python src/services/agent_devlog_posting.py --agent <agent_id> --action "<description>"
```

**Parameters**:
- `agent_id`: Agent identifier
- `action`: Description of the action performed

**Example**:
```bash
python src/services/agent_devlog_posting.py --agent Agent-7 --action "Documentation implementation complete"
```

### **Consolidated Messaging Service**

#### **Core Components**

```python
from src.services.messaging_service import (
    ConsolidatedMessagingService,
    MessageFormatter,
    MessageValidator,
    MessageSender,
    AgentOnboarder
)
```

#### **Message Validation**
```python
validator = MessageValidator()
is_valid = validator.validate_message(
    from_agent="Agent-7",
    to_agent="Agent-4",
    message="Test message",
    priority="NORMAL"
)
```

#### **Message Formatting**
```python
formatter = MessageFormatter()
formatted_message = formatter.format_message(
    from_agent="Agent-7",
    to_agent="Agent-4",
    message="Test message",
    priority="NORMAL"
)
```

#### **Message Sending**
```python
sender = MessageSender()
success = await sender.send_message(
    from_agent="Agent-7",
    to_agent="Agent-4",
    message="Test message",
    priority="NORMAL"
)
```

## 🌐 **Thea Consultation API**

### **Strategic Consultation**

#### **CLI Interface**
```bash
python thea_consultation.py help
python thea_consultation.py consult --template priority_guidance --question "What should be our next priority?"
python thea_consultation.py emergency --issue "System experiencing performance issues"
python thea_consultation.py status-report
```

#### **Available Templates**
- `priority_guidance` - Priority and task guidance
- `crisis_response` - Emergency response procedures
- `strategic_planning` - Strategic planning assistance
- `quality_assessment` - Quality assessment guidance
- `architecture_review` - Architecture review assistance
- `team_coordination` - Team coordination guidance
- `performance_optimization` - Performance optimization
- `risk_assessment` - Risk assessment procedures

### **Autonomous Communication**

#### **Send Message to Thea**
```bash
python thea_autonomous.py send "Message to send to Thea"
```

#### **Check Communication Status**
```bash
python thea_autonomous.py status
```

#### **Interactive Mode**
```bash
python thea_autonomous.py interactive
```

### **Thea Services API**

#### **Browser Manager**
```python
from src.services.thea.thea_browser_manager import TheaBrowserManager

browser_manager = TheaBrowserManager()
success = await browser_manager.initialize()
```

#### **Communication Core**
```python
from src.services.thea.thea_communication_core import TheaCommunicationCore

comm_core = TheaCommunicationCore()
response = await comm_core.send_message("Test message")
```

#### **Cookie Manager**
```python
from src.services.thea.thea_cookie_manager import TheaCookieManager

cookie_manager = TheaCookieManager()
cookies_loaded = await cookie_manager.load_cookies()
```

## 🔍 **Project Scanner API**

### **Enhanced Project Scanner**

#### **Run Comprehensive Scan**
```bash
python tools/projectscanner/run_project_scan.py
```

#### **Core Scanner**
```bash
python tools/run_project_scan.py
```

#### **Enhanced Scanner with Caching**
```bash
python tools/projectscanner/enhanced_scanner/core.py
```

### **Scanner Components**

#### **Language Analyzer**
```python
from tools.projectscanner.enhanced_analyzer.language_analyzer import EnhancedLanguageAnalyzer

analyzer = EnhancedLanguageAnalyzer()
analysis = analyzer.analyze_file(file_path)
```

#### **Caching System**
```python
from tools.projectscanner.enhanced_analyzer.caching_system import EnhancedCachingSystem

cache = EnhancedCachingSystem()
cached_result = cache.get_cached_analysis(file_path)
```

#### **Report Generator**
```python
from tools.projectscanner.enhanced_analyzer.report_generator import EnhancedReportGenerator

generator = EnhancedReportGenerator(project_root, analysis_data)
generator.generate_enhanced_reports()
```

## 🛡️ **Quality Assurance API**

### **V2 Compliance Validation**

#### **Quality Gates**
```bash
python quality_gates.py
```

#### **Compliance Checker**
```bash
python tools/v2_compliance_checker.py
```

### **Testing Framework**

#### **Run All Tests**
```bash
python -m pytest
```

#### **Run Specific Test Categories**
```bash
python -m pytest tests/unit/
python -m pytest tests/integration/
```

#### **Generate Test Coverage**
```bash
python -m pytest --cov=src tests/
```

## 📊 **Monitoring and Health Check APIs**

### **Agent Performance Monitor**
```bash
python src/services/monitoring/agent_performance_monitor.py
```

### **System Health Checker**
```bash
python src/services/alerting/agent_health_checker.py
```

### **Status Dashboard**
```bash
python src/services/dashboard/agent_status_dashboard.py
```

## 🔧 **Configuration APIs**

### **Environment Inference**
```bash
python tools/env_inference_tool.py
```

### **Configuration Validation**
```bash
python tools/discord_config_validator.py
```

### **Environment Setup**
```bash
python generate_env_example.py
```

## 🚀 **Deployment APIs**

### **Discord Commander Launcher**
```bash
python src/services/discord_commander/launcher.py
```

### **Web Controller**
```bash
python src/services/discord_commander/web_controller.py
```

### **Server Manager**
```bash
python src/services/discord_commander/server_manager.py
```

## 🔐 **Authentication and Security APIs**

### **Discord Authentication**
```python
# Environment variables required
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_guild_id_here
DISCORD_CHANNEL_ID=your_channel_id_here
```

### **Cookie Management**
```bash
# Save authentication cookies
python save_thea_cookies.py

# Extract cookies from browser
python extract_browser_cookies.py

# Manual cookie setup
python manual_cookie_setup.py
```

## 📈 **Performance and Metrics APIs**

### **Metrics Collection**
```bash
python tools/metrics_collector.py
```

### **Performance Reporter**
```bash
python tools/performance_reporter.py
```

### **Resource Monitor**
```bash
python tools/resource_monitor.py
```

## 🔍 **Diagnostic and Troubleshooting APIs**

### **System Diagnostics**
```bash
python tools/system_diagnostics.py
```

### **Sync Drift Diagnostic**
```bash
python sync_drift_diagnostic.py
```

### **Cookie Analysis**
```bash
python analyze_cookies.py
```

### **ChromeDriver Fix**
```bash
python fix_chromedriver.py
python force_chromedriver_fix.py
```

## 📚 **Error Handling and Response Codes**

### **HTTP Status Codes**
- `200 OK` - Request successful
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable

### **API Error Response Format**
```json
{
  "error": "Error description",
  "code": "ERROR_CODE",
  "timestamp": "2025-10-05T10:30:00Z",
  "details": "Additional error details"
}
```

### **Common Error Codes**
- `BOT_NOT_INITIALIZED` - Discord bot not initialized
- `AGENT_NOT_FOUND` - Agent identifier not found
- `INVALID_PRIORITY` - Invalid message priority
- `MESSAGE_TOO_LONG` - Message exceeds length limit
- `AUTHENTICATION_FAILED` - Authentication failed
- `SERVICE_UNAVAILABLE` - Service temporarily unavailable

## 🎯 **Integration Examples**

### **Python Integration**
```python
import requests
import json

# Send message via REST API
def send_message(agent, message, priority="NORMAL"):
    url = "http://localhost:8080/api/send_message"
    data = {
        "agent": agent,
        "message": message,
        "priority": priority
    }
    response = requests.post(url, json=data)
    return response.json()

# Get agent status
def get_agent_status():
    url = "http://localhost:8080/api/agents"
    response = requests.get(url)
    return response.json()
```

### **JavaScript Integration**
```javascript
// WebSocket connection
const socket = io('http://localhost:8080');

// Send message
function sendMessage(agent, message, priority = 'NORMAL') {
    socket.emit('send_message', {
        agent: agent,
        message: message,
        priority: priority
    });
}

// Listen for agent status updates
socket.on('agent_status_update', (data) => {
    updateAgentStatus(data);
});
```

### **cURL Examples**
```bash
# Get agent status
curl -X GET http://localhost:8080/api/agents

# Send message
curl -X POST http://localhost:8080/api/send_message \
  -H "Content-Type: application/json" \
  -d '{"agent": "Agent-7", "message": "Test message", "priority": "NORMAL"}'

# Get system status
curl -X GET http://localhost:8080/api/system_status
```

## 📋 **API Rate Limits and Best Practices**

### **Rate Limits**
- **REST API**: 100 requests per minute per IP
- **WebSocket**: 1000 messages per minute per connection
- **Agent Messaging**: 500 messages per minute per agent
- **Thea Communication**: 10 requests per minute

### **Best Practices**
- Use appropriate priority levels for messages
- Implement proper error handling and retry logic
- Cache frequently accessed data
- Monitor API usage and performance
- Use WebSocket connections for real-time updates
- Validate all input parameters
- Implement proper authentication and authorization

## 🔄 **API Versioning and Updates**

### **Version Information**
- **Current Version**: 2.0.0
- **API Version**: v1
- **Last Updated**: 2025-10-05

### **Backward Compatibility**
- API v1 is fully backward compatible
- New features are additive only
- Deprecated endpoints are marked with warnings
- Migration guides provided for major changes

---

**Status**: API Documentation Complete  
**Agent**: Agent-7 (Elevated Web Development Expert)  
**Version**: 2.0.0  
**Last Updated**: 2025-10-05  
**Next**: CONTRIBUTING.md Implementation
