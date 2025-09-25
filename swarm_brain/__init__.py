"""
Swarm Brain - Vectorized Swarm Intelligence Core
===============================================

The central nervous system for agent coordination, providing:
- Living documentation through agent behavior patterns
- Collective intelligence layer for tools, workflows, and protocols
- Semantic search across all agent activities
- Self-improving swarm memory

Usage:
    from swarm_brain import SwarmBrain, Ingestor, Retriever
    from swarm_brain.decorators import vectorized_action
    
    # Initialize
    brain = SwarmBrain()
    ingestor = Ingestor(brain)
    retriever = Retriever(brain)
    
    # Record agent actions
    ingestor.action(
        title="Project Analysis",
        tool="project_scanner",
        outcome="success",
        context={"files_analyzed": 603, "compliance_rate": 0.864},
        project="Agent_Cellphone_V2",
        agent_id="Agent-2",
        tags=["analysis", "compliance", "scanner"]
    )
    
    # Query collective intelligence
    patterns = retriever.how_do_agents_do("V2 compliance refactoring")
    
    # Use decorators for automatic recording
    @vectorized_action(tool="discord_commander", project="Agent_Cellphone_V2", 
                      agent_id="Agent-6", tags=["discord", "coordination"])
    def send_coordination_message(message: str):
        # Agent action automatically recorded
        return {"success": True, "message": message}
"""

from .db import SwarmBrain
from .ingest import Ingestor
from .retriever import Retriever
from .decorators import vectorized_action, vectorized_protocol, vectorized_workflow

__version__ = "1.0.0"
__all__ = ["SwarmBrain", "Ingestor", "Retriever", "vectorized_action", "vectorized_protocol", "vectorized_workflow"]




