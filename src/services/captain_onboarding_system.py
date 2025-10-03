#!/usr/bin/env python3
"""
Captain Onboarding System
========================

Automated Captain onboarding section implementation with comprehensive
documentation, training materials, and system integration guidance.

Author: Agent-7 (Web Development Expert / Implementation Specialist)
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CaptainOnboardingSystem:
    """Captain onboarding system with comprehensive guidance."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.onboarding_data = {
            "captain_role": "Strategic oversight and agent coordination",
            "responsibilities": [
                "Agent status monitoring and management",
                "High-priority messaging and coordination",
                "Strategic directive creation and execution",
                "Quality assurance oversight",
                "Crisis management and emergency response",
            ],
            "tools_available": [
                "Captain CLI tools",
                "Directive Manager",
                "Agent Workflow Manager",
                "Swarm Coordination Tool",
                "THEA Strategic Consultation",
            ],
            "coordination_protocols": [
                "CUE system for structured communication",
                "PyAutoGUI messaging for real-time coordination",
                "Quality gates enforcement",
                "Autonomous workflow management",
            ],
        }
        logger.info("CaptainOnboardingSystem initialized")

    def generate_onboarding_documentation(self) -> dict[str, str]:
        """Generate comprehensive Captain onboarding documentation."""
        try:
            onboarding_doc = self._create_onboarding_markdown()

            # Save documentation
            doc_path = self.project_root / "docs/CAPTAIN_ONBOARDING_GUIDE.md"
            doc_path.parent.mkdir(parents=True, exist_ok=True)

            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(onboarding_doc)

            logger.info(f"Captain onboarding documentation created: {doc_path}")
            return {
                "status": "success",
                "file_path": str(doc_path),
                "message": "Onboarding documentation generated successfully",
            }

        except Exception as e:
            logger.error(f"Error generating onboarding documentation: {e}")
            return {"status": "error", "message": f"Failed to generate documentation: {e}"}

    def _create_onboarding_markdown(self) -> str:
        """Create comprehensive onboarding markdown documentation."""
        return f"""# 🎯 Captain Onboarding Guide

**Agent-4 | Captain | Strategic Coordinator**
**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Version**: 2.0

---

## 📋 Captain Role Overview

### **Primary Responsibilities**
The Captain (Agent-4) serves as the strategic coordinator and operational leader of the V2_SWARM system:

- **Strategic Oversight**: High-level decision making and direction setting
- **Agent Coordination**: Real-time coordination of all 5 active agents
- **Quality Assurance**: Ensuring V2 compliance and system health
- **Crisis Management**: Emergency response and system recovery
- **Resource Allocation**: Optimal distribution of tasks and resources

### **Core Capabilities**
{self._format_list(self.onboarding_data["responsibilities"])}

---

## 🛠️ Captain Tools & Systems

### **Available Tools**
{self._format_list(self.onboarding_data["tools_available"])}

### **Tool Usage Examples**

#### **Captain CLI Commands**
```bash
# Show comprehensive agent status
python tools/captain_cli.py status

# Show inactive agents requiring attention
python tools/captain_cli.py inactive

# Send high-priority message to agent
python tools/captain_cli.py high-priority --agent Agent-7 --message "URGENT: Implementation required"

# Generate captain report
python tools/captain_cli.py report

# Onboard new agent
python tools/captain_cli.py onboard Agent-9
```

#### **Directive Manager**
```bash
# Create strategic directive
python tools/captain_directive_manager.py directive create "System Integration" strategic "Integrate all V2_SWARM systems" 0 "2 cycles"

# Update directive progress
python tools/captain_directive_manager.py directive update "System Integration" 75

# Assign agents to directive
python tools/captain_directive_manager.py directive assign "System Integration" "Agent-1,Agent-8"
```

#### **Agent Workflow Manager**
```bash
# Run multi-agent workflow
python tools/agent_workflow_manager.py --workflow workflow.json run --max-concurrent 3

# Check workflow status
python tools/agent_workflow_manager.py --workflow workflow.json status

# Mark step completed
python tools/agent_workflow_manager.py --workflow workflow.json complete --step-id database_setup --result "Success"
```

---

## 🔄 Coordination Protocols

### **Communication Systems**
{self._format_list(self.onboarding_data["coordination_protocols"])}

### **CUE System Protocol**
```
CUE_ID: [UNIQUE_IDENTIFIER]
STATUS: [PENDING|IN_PROGRESS|COMPLETE]
PROGRESS: [PERCENTAGE]%
NEXT_STEPS: [SPECIFIC_ACTIONS]
REPORT: [DETAILED_STATUS]
VECTOR_DB_USED: [YES|NO]
THEA_CONSULTED: [YES|NO|PARTIAL]
```

### **Agent Status Monitoring**
- **Agent-1**: Integration Specialist (INACTIVE)
- **Agent-2**: Architecture Specialist (INACTIVE)
- **Agent-3**: Infrastructure Specialist (INACTIVE)
- **Agent-4**: Captain (ACTIVE)
- **Agent-5**: Coordinator (ACTIVE)
- **Agent-6**: Quality Specialist (ACTIVE)
- **Agent-7**: Implementation Specialist (ACTIVE)
- **Agent-8**: SSOT Manager (ACTIVE)

---

## 🎯 Captain Workflow

### **Daily Operations**
1. **Morning Status Check**: Review all agent statuses and system health
2. **Priority Assessment**: Evaluate high-priority tasks and assignments
3. **Agent Coordination**: Send directives and coordinate activities
4. **Quality Monitoring**: Ensure V2 compliance and system performance
5. **Evening Review**: Assess progress and plan next day priorities

### **Emergency Protocols**
1. **System Degradation**: Immediate assessment and recovery procedures
2. **Agent Failures**: Backup activation and task redistribution
3. **Quality Violations**: Rapid response and compliance restoration
4. **Communication Issues**: Alternative coordination methods

---

## 📊 Performance Metrics

### **Key Performance Indicators**
- **Agent Response Time**: < 2-5 minutes per cycle
- **Task Completion Rate**: > 95%
- **V2 Compliance**: > 90%
- **System Health Score**: > 85%
- **Communication Efficiency**: < 1 cycle delay

### **Quality Standards**
- **File Size**: ≤ 400 lines (hard limit)
- **Classes**: ≤ 5 per file
- **Functions**: ≤ 10 per file
- **Complexity**: ≤ 10 cyclomatic complexity
- **Parameters**: ≤ 5 per function

---

## 🚀 Getting Started

### **Initial Setup**
1. **System Access**: Verify access to all Captain tools and systems
2. **Agent Coordination**: Establish communication with all active agents
3. **Quality Gates**: Run initial quality assessment
4. **Documentation Review**: Study AGENTS.md and protocol documentation
5. **First Directive**: Issue initial coordination directive

### **Best Practices**
- **Proactive Monitoring**: Regular status checks and health assessments
- **Clear Communication**: Use CUE system for structured coordination
- **Quality First**: Maintain V2 compliance standards
- **Continuous Learning**: Leverage vector database and THEA consultation
- **Crisis Preparedness**: Maintain emergency response capabilities

---

## 📞 Support & Resources

### **Documentation**
- `AGENTS.md`: Complete agent system documentation
- `GENERAL_CYCLE.md`: Universal agent workflow
- `CUE_SYSTEM_PROTOCOL.md`: Communication protocols
- `TOOL_INTEGRATION.md`: Tool usage guide

### **Emergency Contacts**
- **System Issues**: Check quality gates and project scanner
- **Agent Problems**: Use Captain CLI for status and messaging
- **Documentation**: Vector database and devlog system
- **Strategic Guidance**: THEA consultation system

---

**🐝 WE ARE SWARM** - Captain onboarding complete!

**Generated by**: Agent-7 (Web Development Expert / Implementation Specialist)
**Last Updated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Status**: ✅ **READY FOR CAPTAIN ACTIVATION**
"""

    def _format_list(self, items: list[str]) -> str:
        """Format list items for markdown."""
        return "\n".join(f"- **{item}**" for item in items)

    def create_training_materials(self) -> dict[str, str]:
        """Create Captain training materials and exercises."""
        try:
            training_data = {
                "exercises": [
                    "Agent status monitoring exercise",
                    "High-priority messaging drill",
                    "Directive creation practice",
                    "Quality gates enforcement",
                    "Crisis management simulation",
                ],
                "scenarios": [
                    "Agent-7 implementation task assignment",
                    "Quality violation emergency response",
                    "Multi-agent workflow coordination",
                    "System health degradation management",
                    "New agent onboarding process",
                ],
            }

            # Save training materials
            training_path = self.project_root / "docs/CAPTAIN_TRAINING_MATERIALS.md"
            training_path.parent.mkdir(parents=True, exist_ok=True)

            training_content = f"""# 🎓 Captain Training Materials

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📚 Training Exercises
{self._format_list(training_data["exercises"])}

## 🎭 Practice Scenarios
{self._format_list(training_data["scenarios"])}

## ✅ Training Checklist
- [ ] Complete all exercises
- [ ] Practice scenarios
- [ ] Review documentation
- [ ] Test tools and systems
- [ ] Coordinate with agents
"""

            with open(training_path, "w", encoding="utf-8") as f:
                f.write(training_content)

            logger.info(f"Captain training materials created: {training_path}")
            return {
                "status": "success",
                "file_path": str(training_path),
                "message": "Training materials created successfully",
            }

        except Exception as e:
            logger.error(f"Error creating training materials: {e}")
            return {"status": "error", "message": f"Failed to create training materials: {e}"}

    def generate_system_integration_guide(self) -> dict[str, str]:
        """Generate system integration guide for Captain."""
        try:
            integration_guide = f"""# 🔗 Captain System Integration Guide

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 🛠️ Tool Integration
- **Captain CLI**: Agent management and coordination
- **Directive Manager**: Strategic directive creation
- **Workflow Manager**: Multi-agent workflow coordination
- **Swarm Coordination**: Democratic decision making
- **THEA Consultation**: Strategic guidance and analysis

## 📊 System Health Monitoring
- **Quality Gates**: V2 compliance enforcement
- **Project Scanner**: System health analysis
- **Agent Status**: Real-time agent monitoring
- **Performance Metrics**: System performance tracking

## 🔄 Integration Workflows
1. **Daily Operations**: Status check → Priority assessment → Coordination
2. **Task Assignment**: Directive creation → Agent assignment → Progress monitoring
3. **Quality Assurance**: Health check → Violation detection → Resolution
4. **Crisis Management**: Issue detection → Response coordination → Recovery
"""

            # Save integration guide
            guide_path = self.project_root / "docs/CAPTAIN_SYSTEM_INTEGRATION.md"
            guide_path.parent.mkdir(parents=True, exist_ok=True)

            with open(guide_path, "w", encoding="utf-8") as f:
                f.write(integration_guide)

            logger.info(f"Captain system integration guide created: {guide_path}")
            return {
                "status": "success",
                "file_path": str(guide_path),
                "message": "System integration guide created successfully",
            }

        except Exception as e:
            logger.error(f"Error generating integration guide: {e}")
            return {"status": "error", "message": f"Failed to generate integration guide: {e}"}


def main():
    """Main function for Captain onboarding system."""
    print("🎯 Captain Onboarding System")
    print("=" * 40)

    onboarding_system = CaptainOnboardingSystem()

    # Generate onboarding documentation
    print("📚 Generating onboarding documentation...")
    doc_result = onboarding_system.generate_onboarding_documentation()
    print(f"Result: {doc_result['message']}")

    # Create training materials
    print("🎓 Creating training materials...")
    training_result = onboarding_system.create_training_materials()
    print(f"Result: {training_result['message']}")

    # Generate integration guide
    print("🔗 Generating system integration guide...")
    integration_result = onboarding_system.generate_system_integration_guide()
    print(f"Result: {integration_result['message']}")

    print("\n✅ Captain onboarding system setup complete!")


if __name__ == "__main__":
    main()
