#!/usr/bin/env python3
"""
Core functionality for Captain Cycle-Based Documentation Updater
V2 Compliance: Essential methods only
"""

from swarm_brain import Ingestor, SwarmBrain


class CaptainCycleCore:
    """Core methods for Captain cycle-based operations."""

    def __init__(self):
        """Initialize core functionality."""
        self.brain = SwarmBrain()
        self.ingestor = Ingestor(self.brain)

    def create_handbook_content(self) -> str:
        """Create cycle-based handbook content."""
        return """# Captain's Handbook - Cycle-Based Operations

## Core Responsibilities
- Swarm Coordination across cycles
- Strategic Planning over multiple cycles
- Quality Assurance per cycle
- Agent Development through cycles
- System Evolution continuously
- Crisis Management within cycles

## Cycle-Based Timeline Standards
- 1 cycle = 2-5 minutes (standard agent response)
- 1 hour = 12-30 cycles
- 1 day = 288-720 cycles
- 1 week = 2016-5040 cycles

## Strategic Framework
- Mission Definition: 5-10 cycles
- Planning Phase: 10-20 cycles
- Execution Phase: 20-100 cycles
- Review Phase: 5-15 cycles
- Optimization Phase: 10-30 cycles

## Quality Gates Integration
- Pre-cycle: Check quality status
- During cycle: Monitor quality
- Post-cycle: Validate quality
- Continuous: Maintain standards

## Agent Coordination
- Monitor agent status every cycle
- Coordinate tasks across cycles
- Ensure cycle-based deadlines
- Maintain cycle-based reporting
"""

    def create_cheatsheet_content(self) -> str:
        """Create cycle-based cheatsheet content."""
        return """# Captain Cheatsheet - Cycle-Based Operations

## Quick Reference
- Cycle = 2-5 minutes
- Hour = 12-30 cycles
- Day = 288-720 cycles
- Week = 2016-5040 cycles

## Common Operations
- Status check: 1 cycle
- Task assignment: 1-2 cycles
- Quality review: 2-3 cycles
- Strategic planning: 5-10 cycles
- Crisis response: 1-3 cycles

## Quality Gates
- Run quality_gates.py every cycle
- Check V2 compliance per cycle
- Validate standards continuously
- Report violations immediately

## Agent Management
- Monitor all agents every cycle
- Coordinate tasks efficiently
- Ensure cycle-based deadlines
- Maintain continuous communication
"""

    def ingest_documentation(self, content: str, doc_type: str) -> bool:
        """Ingest documentation into Swarm Brain."""
        try:
            self.ingestor.ingest_text(content, doc_type)
            return True
        except Exception as e:
            print(f"❌ Error ingesting {doc_type}: {e}")
            return False

