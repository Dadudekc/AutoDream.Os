# Thea Strategic Consultation System

🤖 **Strategic consultation and autonomous communication system for Thea**

## Overview

The Thea Strategic Consultation System provides comprehensive strategic guidance and autonomous communication capabilities for the Agent Cellphone V2 project. The system includes multiple consultation templates, CLI interfaces, and autonomous communication features.

## System Components

### 🎯 Core Modules

1. **Strategic Consultation Core** (`strategic_consultation_core.py`)
   - Core consultation logic and processing
   - Template-based consultation responses
   - Consultation history management
   - V2 compliant (≤400 lines)

2. **Consultation Templates** (`strategic_consultation_templates.py`)
   - 8 specialized consultation templates
   - Priority guidance, crisis response, strategic planning
   - Quality assessment, architecture review, team coordination
   - Performance optimization, risk assessment

3. **CLI Interface** (`strategic_consultation_cli.py`)
   - Command-line interface for consultations
   - Emergency consultation support
   - Status reporting and history
   - Comprehensive help system

4. **Autonomous Communication** (`thea_autonomous_cli.py`)
   - Autonomous message sending to Thea
   - Communication logging and tracking
   - Session management
   - Response handling

### 🚀 Quick Start

#### Strategic Consultation
```bash
# From project root
python thea_consultation.py help

# Priority guidance consultation
python thea_consultation.py consult --template priority_guidance --question "What should be our next priority?"

# Emergency consultation
python thea_consultation.py emergency --issue "System experiencing performance issues"

# Status report
python thea_consultation.py status-report
```

#### Autonomous Communication
```bash
# From project root
python thea_autonomous.py send "Message to send to Thea"

# Check communication status
python thea_autonomous.py status
```

### 📚 Available Consultation Templates

| Template | Purpose | Context | Output |
|----------|---------|---------|---------|
| `priority_guidance` | Task prioritization and resource allocation | project_analysis | recommendations |
| `crisis_response` | Emergency consultation for critical issues | system_health | action_plan |
| `strategic_planning` | Long-term strategic planning and roadmap | project_roadmap | strategic_plan |
| `quality_assessment` | Quality and compliance assessment | quality_metrics | assessment_report |
| `architecture_review` | System architecture analysis | system_architecture | architecture_analysis |
| `team_coordination` | Agent coordination and team management | swarm_coordination | coordination_plan |
| `performance_optimization` | Performance analysis and optimization | performance_metrics | optimization_plan |
| `risk_assessment` | Risk analysis and mitigation strategy | risk_management | risk_report |

### 🔧 Technical Details

- **V2 Compliance**: All modules ≤400 lines
- **Python 3.8+**: Compatible with project requirements
- **JSON Storage**: Consultation and communication data stored in JSON files
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Robust error handling and graceful degradation

### 📁 File Structure

```
src/services/thea/
├── strategic_consultation_core.py      # Core consultation logic
├── strategic_consultation_templates.py # Consultation templates
├── strategic_consultation_cli.py       # CLI interface
├── thea_autonomous_cli.py             # Autonomous communication
└── README.md                          # This documentation

Project Root:
├── thea_consultation.py               # Strategic consultation launcher
├── thea_autonomous.py                 # Autonomous communication launcher
└── consultations/                     # Consultation storage directory
```

### 🎯 Usage Examples

#### Priority Guidance
```bash
python thea_consultation.py consult \
  --template priority_guidance \
  --question "What should be our next priority for the project?"
```

#### Crisis Response
```bash
python thea_consultation.py emergency \
  --issue "Discord routing issues affecting agent communication"
```

#### Strategic Planning
```bash
python thea_consultation.py consult \
  --template strategic_planning \
  --question "How should we plan our next development phase?"
```

#### Autonomous Communication
```bash
python thea_autonomous.py send "Mission Report: Discord routing fix completed successfully"
```

### 📊 System Features

- **Template-Based Consultations**: 8 specialized consultation types
- **Emergency Response**: Dedicated crisis consultation system
- **Autonomous Communication**: Direct messaging to Thea
- **History Tracking**: Complete consultation and communication logs
- **Session Management**: Persistent session tracking
- **Status Reporting**: Comprehensive system status and history
- **V2 Compliance**: All modules follow V2 coding standards

### 🔍 Monitoring and Debugging

- **Consultation History**: Stored in `consultations/` directory
- **Communication Logs**: Stored in `thea_communications.json`
- **Session Tracking**: Persistent session IDs and timestamps
- **Error Logging**: Comprehensive error logging and reporting

### 🚀 Integration

The Thea consultation system integrates with:
- **Discord System**: For agent communication and status updates
- **Project CLI**: For task management and coordination
- **Messaging System**: For agent-to-agent communication
- **Quality Gates**: For V2 compliance and code quality

### 📝 Notes

- All consultations are logged and stored for future reference
- The system provides structured responses with confidence levels
- Emergency consultations use specialized crisis response templates
- Autonomous communication allows direct messaging to Thea
- The system is designed for both human and agent interaction

---

**Author**: Agent-7 (Implementation Specialist)  
**License**: MIT  
**V2 Compliant**: ✅ All modules ≤400 lines
