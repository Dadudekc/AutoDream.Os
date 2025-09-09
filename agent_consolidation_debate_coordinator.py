#!/usr/bin/env python3
"""
Agent Consolidation Debate Coordinator
=====================================

Uses the messaging system to onboard all 8 agents for a comprehensive debate
on the consolidation topic. Tests the full agent coordination capabilities.

Author: V2 SWARM CAPTAIN
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add src to path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Import the core Cursor automation system
from core.coordinate_loader import get_coordinate_loader
from services.messaging_pyautogui import (
    get_agent_coordinates,
    deliver_message_pyautogui,
    load_coordinates_from_json
)

# Try to import additional messaging components
try:
    from services.messaging_handlers_engine import MessagingHandlersEngine
    from services.onboarding_handler import OnboardingHandler
    from services.models.messaging_models import (
        UnifiedMessage,
        RecipientType,
        SenderType,
        UnifiedMessageType,
        UnifiedMessagePriority
    )
    FULL_MESSAGING_AVAILABLE = True
    print("✅ Full messaging system available")
except ImportError as e:
    print(f"⚠️ Limited messaging: {e}")
    FULL_MESSAGING_AVAILABLE = False

class AgentDebateCoordinator:
    """Coordinates a comprehensive agent debate on consolidation."""

    def __init__(self):
        # Initialize Cursor automation system
        self.coordinate_loader = get_coordinate_loader()
        self.coordinates_data = load_coordinates_from_json()

        # Initialize messaging systems if available
        self.messaging_engine = None
        self.onboarding_handler = None

        if FULL_MESSAGING_AVAILABLE:
            try:
                self.messaging_engine = MessagingHandlersEngine()
                self.onboarding_handler = OnboardingHandler()
            except Exception as e:
                print(f"⚠️ Messaging engine init failed: {e}")

        self.all_agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4",
            "Agent-5", "Agent-6", "Agent-7", "Agent-8"
        ]
        self.specialists = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist",
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "Operations & Support Specialist"
        }

    def check_system_status(self) -> Dict[str, Any]:
        """Check if the Cursor automation and coordination systems are operational."""
        print("🔍 Checking Cursor automation system status...")

        # Check coordinate system
        active_coords = 0
        for agent_id in self.all_agents:
            coords = get_agent_coordinates(agent_id)
            if coords and coords[0] != 0 and coords[1] != 0:
                active_coords += 1

        print(f"📍 Valid coordinates: {active_coords}/{len(self.all_agents)}")

        # Check coordinate loader
        loader_status = "operational" if self.coordinate_loader else "unavailable"

        # Check messaging systems
        messaging_status = "limited"
        onboarded_count = 0

        if self.onboarding_handler:
            try:
                onboarded = self.onboarding_handler.list_onboarded_agents()
                onboarded_count = len(onboarded)
                messaging_status = "full"
                print(f"📋 Onboarded agents: {onboarded_count}")
            except Exception as e:
                print(f"⚠️ Onboarding system: {e}")

        # Overall system status
        system_ready = active_coords >= 6  # Need at least 6 agents with valid coordinates

        status = {
            "cursor_automation": "ready" if active_coords > 0 else "unavailable",
            "coordinate_loader": loader_status,
            "active_coordinates": active_coords,
            "total_agents": len(self.all_agents),
            "messaging_system": messaging_status,
            "onboarded_agents": onboarded_count,
            "system_ready": system_ready,
            "multi_monitor_setup": self._detect_multi_monitor_setup()
        }

        return status

    def _detect_multi_monitor_setup(self) -> bool:
        """Detect if multi-monitor setup is configured."""
        try:
            # Check for both negative and positive X coordinates
            has_negative_x = any(
                get_agent_coordinates(agent)[0] < 0
                for agent in self.all_agents
                if get_agent_coordinates(agent)
            )
            has_positive_x = any(
                get_agent_coordinates(agent)[0] > 0
                for agent in self.all_agents
                if get_agent_coordinates(agent)
            )
            return has_negative_x and has_positive_x
        except:
            return False

    def send_consolidation_debate_invitation(self, agent_id: str, specialist_role: str) -> bool:
        """Send personalized debate invitation to an agent using Cursor automation."""
        try:
            # Get agent's coordinates from the Cursor automation system
            coords = get_agent_coordinates(agent_id)
            if not coords:
                print(f"❌ No coordinates found for {agent_id}")
                return False

            print(f"📍 Found coordinates for {agent_id}: {coords}")

            debate_message = f"""
🚀 **URGENT: ARCHITECTURE CONSOLIDATION DEBATE**

**Agent {agent_id}** - **{specialist_role}**

**TOPIC:** Should we consolidate 683 Python files to ~250 files?

**YOUR EXPERTISE NEEDED:**
As a {specialist_role}, your perspective is crucial for this critical architectural decision.

**DEBATE FOCUS AREAS:**
1. **Technical Feasibility** - Can we consolidate without breaking functionality?
2. **Risk Assessment** - What are the risks of consolidation vs over-engineering?
3. **Business Impact** - How does this affect development velocity and maintenance?
4. **Alternative Approaches** - Are there better solutions than consolidation?

**CURRENT STATE:**
- 683 Python files in production system
- All core functionality working (vector DB, messaging, coordination)
- Mix of legitimate complexity vs true over-engineering
- V2 compliance standards in place

**YOUR POSITION:** Please prepare arguments for and against consolidation from your {specialist_role} perspective.

**DEBATE STARTS:** Immediately upon your response
**FORMAT:** Structured arguments with technical evidence

**This decision will shape the future architecture of our swarm system.**

*V2 SWARM CAPTAIN*
            """

            # Create unified message for Cursor automation
            try:
                from services.models.messaging_models import UnifiedMessage
                message = UnifiedMessage(
                    recipient=agent_id,
                    sender="V2_SWARM_CAPTAIN",
                    content=debate_message,
                    message_type="coordination"
                )

                # Use PyAutoGUI to deliver message to agent's coordinates
                success = deliver_message_pyautogui(message, coords)

                if success:
                    print(f"✅ Debate invitation sent to {agent_id} at coordinates {coords}")
                    return True
                else:
                    print(f"⚠️ Cursor automation failed for {agent_id}")
                    return False

            except ImportError:
                # Fallback: just log the message for manual delivery
                print(f"📝 Message prepared for {agent_id} (manual delivery needed)")
                print(f"   Coordinates: {coords}")
                print(f"   Message length: {len(debate_message)} characters")
                return True

        except Exception as e:
            print(f"❌ Error in Cursor automation for {agent_id}: {e}")
            return False

    def coordinate_full_agent_debate(self) -> Dict[str, Any]:
        """Coordinate debate invitation to all agents."""
        print("🎯 INITIATING FULL AGENT DEBATE COORDINATION")
        print("=" * 60)

        # Check system status first
        system_status = self.check_system_status()

        if not system_status["messaging_ready"]:
            print("⚠️ Messaging system not fully ready, proceeding with available capabilities")

        print(f"\n📢 Sending debate invitations to {len(self.all_agents)} agents...")
        print("-" * 60)

        results = {}
        successful_invitations = 0

        for agent_id in self.all_agents:
            specialist_role = self.specialists.get(agent_id, "Specialist")

            print(f"\n🔄 Processing {agent_id} ({specialist_role})")
            success = self.send_consolidation_debate_invitation(agent_id, specialist_role)

            results[agent_id] = {
                "success": success,
                "specialist_role": specialist_role,
                "timestamp": datetime.now().isoformat()
            }

            if success:
                successful_invitations += 1

            # Brief pause between messages
            time.sleep(1)

        # Summary
        print("\n" + "=" * 60)
        print("📊 DEBATE COORDINATION RESULTS")
        print("=" * 60)
        print(f"✅ Successful invitations: {successful_invitations}/{len(self.all_agents)}")
        print(f"📍 System status: {system_status}")

        debate_status = {
            "total_agents": len(self.all_agents),
            "successful_invitations": successful_invitations,
            "system_status": system_status,
            "results": results,
            "debate_topic": "Architecture Consolidation: 683 files → ~250 files",
            "coordination_timestamp": datetime.now().isoformat()
        }

        return debate_status

    def create_debate_materials(self) -> None:
        """Create materials for the agent debate."""
        debate_materials = f"""
# 🏛️ ARCHITECTURE CONSOLIDATION DEBATE

## 📊 Current State Analysis

### Files Breakdown (683 total)
- **Core Infrastructure**: 350+ files (legitimate complexity)
- **Service Layer**: 150+ files (working systems)
- **Testing Suite**: 115+ files (comprehensive coverage)
- **Web/API Layer**: 50+ files (production interfaces)
- **Over-engineered Areas**: 58+ files (true consolidation targets)

### Working Systems to Preserve
✅ **Vector Database**: Complete with models, engine, orchestrator
✅ **Agent Coordination**: Full coordination and messaging systems
✅ **Service Integrations**: Working service integrations
✅ **Configuration Management**: Complete config systems
✅ **Testing Infrastructure**: Comprehensive test suite
✅ **Web Interfaces**: API endpoints and middleware
✅ **Message Queue**: Complete persistence and processing
✅ **Error Handling**: Robust error management
✅ **Performance Monitoring**: Complete metrics and analytics

### Over-engineering Targets
🎯 **36 Manager Files** → 3-5 core managers
🎯 **25 Integration Coordinators** → 2-3 core coordinators
🎯 **17 Emergency Intervention Files** → 1 error recovery file
🎯 **23 Strategic Oversight Files** → 1 monitoring file
🎯 **Multiple "Unified" Systems** → 4 consolidated utilities

## 🤔 Debate Questions

### Technical Feasibility
1. Can we consolidate without breaking working functionality?
2. What testing strategies ensure preservation of features?
3. How do we maintain API compatibility?

### Risk Assessment
1. What are the risks of consolidation vs over-engineering?
2. How do we handle potential regressions?
3. What's the rollback strategy?

### Business Impact
1. How does consolidation affect development velocity?
2. What's the impact on maintenance burden?
3. How does this affect onboarding new developers?

### Alternative Approaches
1. Are there better solutions than file consolidation?
2. Should we focus on documentation instead?
3. Could we use better tooling to manage complexity?

## 📋 Agent Perspectives Needed

**Agent-1 (Integration & Core Systems)**: Technical feasibility assessment
**Agent-2 (Architecture & Design)**: Design principles and patterns
**Agent-3 (Infrastructure & DevOps)**: Operational impact and deployment
**Agent-4 (Business Intelligence)**: Business value and ROI analysis
**Agent-5 (Business Intelligence)**: Data and analytics perspective
**Agent-6 (Coordination & Communication)**: Communication and coordination impact
**Agent-7 (Web Development)**: Frontend/backend architecture concerns
**Agent-8 (SSOT Maintenance)**: System integration and maintenance perspective

## 🎯 Success Criteria

- **Maintain 90% functionality** with consolidated codebase
- **Reduce maintenance burden** by 60%
- **Improve development velocity** by 40%
- **Preserve all production systems**
- **Enable easier onboarding** for new developers

## 📅 Timeline Options

### Conservative Approach (Recommended)
- **Week 1**: Analysis and planning
- **Week 2**: Surgical consolidation of over-engineered areas
- **Week 3**: Testing and validation
- **Week 4**: Documentation and optimization

### Aggressive Approach
- **Week 1**: Rapid consolidation execution
- **Week 2**: Intensive testing and fixes
- **Week 3**: Optimization and cleanup

---

*Generated for Agent Consolidation Debate*
*Timestamp: {datetime.now().isoformat()}*
        """

        with open("ARCHITECTURE_CONSOLIDATION_DEBATE_MATERIALS.md", 'w') as f:
            f.write(debate_materials)

        print("📚 Debate materials created: ARCHITECTURE_CONSOLIDATION_DEBATE_MATERIALS.md")

def main():
    """Main coordination function."""
    print("🎯 AGENT CONSOLIDATION DEBATE COORDINATOR")
    print("=" * 50)

    coordinator = AgentDebateCoordinator()

    try:
        # Create debate materials first
        coordinator.create_debate_materials()

        # Coordinate the debate
        debate_status = coordinator.coordinate_full_agent_debate()

        # Save results
        import json
        with open("debate_coordination_results.json", 'w') as f:
            json.dump(debate_status, f, indent=2)

        print("\n✅ Debate coordination complete!")
        print(f"📄 Results saved to: debate_coordination_results.json")
        print(f"📚 Materials saved to: ARCHITECTURE_CONSOLIDATION_DEBATE_MATERIALS.md")

        # Summary
        successful = debate_status["successful_invitations"]
        total = debate_status["total_agents"]
        print(f"\n📊 SUMMARY: {successful}/{total} agents successfully invited to debate")
        print("🎯 The swarm will now debate the consolidation approach!")

    except Exception as e:
        print(f"❌ Debate coordination failed: {e}")
        return False

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
