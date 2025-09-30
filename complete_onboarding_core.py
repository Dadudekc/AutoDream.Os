"""
Complete Onboarding Ingestor Core - V2 Compliant
===============================================

Core complete onboarding documentation ingestion functionality.
Maintains single responsibility principle.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import json
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from swarm_brain import Ingestor, Retriever, SwarmBrain


class CompleteOnboardingCore:
    """Core complete onboarding documentation ingestion functionality."""
    
    def __init__(self):
        """Initialize the complete onboarding core."""
        self.brain = SwarmBrain()
        self.ingestor = Ingestor(self.brain)
        self.retriever = Retriever(self.brain)
        self.ingested_files = []
        print("🧠 Complete Onboarding Core initialized")
    
    def ingest_agent_definitions(self) -> list[int]:
        """Ingest agent role definitions and coordinates."""
        print("\n🤖 Step 1: Ingesting Agent Definitions")
        print("-" * 40)
        
        doc_ids = []
        
        try:
            # Ingest agent coordinates and roles
            coords_path = Path("config/coordinates.json")
            if coords_path.exists():
                with open(coords_path, encoding="utf-8") as f:
                    coords_data = json.load(f)
                
                # Create comprehensive agent definitions
                agent_definitions = self._create_agent_definitions(coords_data)
                
                # Ingest as protocol document
                doc_id = self.ingestor.protocol(
                    title="Complete Agent Definitions",
                    content=agent_definitions,
                    metadata={
                        "type": "agent_definitions",
                        "source": "config/coordinates.json",
                        "agents_count": len(coords_data.get("agents", {}))
                    }
                )
                
                doc_ids.append(doc_id)
                print(f"✅ Agent definitions ingested: {doc_id}")
            
        except Exception as e:
            print(f"❌ Error ingesting agent definitions: {e}")
        
        return doc_ids
    
    def _create_agent_definitions(self, coords_data: dict) -> str:
        """Create comprehensive agent definitions from coordinates data."""
        agents = coords_data.get("agents", {})
        
        definitions = "# Complete Agent Definitions\n\n"
        definitions += "## Agent Configuration\n\n"
        
        for agent_id, agent_data in agents.items():
            definitions += f"### {agent_id}\n"
            definitions += f"- **Role**: {agent_data.get('role', 'Unknown')}\n"
            definitions += f"- **Status**: {agent_data.get('status', 'Unknown')}\n"
            definitions += f"- **Position**: {agent_data.get('position', 'Unknown')}\n"
            definitions += f"- **Coordinates**: {agent_data.get('coordinates', 'Unknown')}\n"
            definitions += f"- **Monitor**: {agent_data.get('monitor', 'Unknown')}\n"
            definitions += "\n"
        
        return definitions
    
    def ingest_onboarding_managers(self) -> list[int]:
        """Ingest onboarding manager documentation."""
        print("\n📋 Step 2: Ingesting Onboarding Managers")
        print("-" * 40)
        
        doc_ids = []
        
        try:
            # Ingest onboarding manager documentation
            onboarding_path = Path("docs/onboarding_manager.md")
            if onboarding_path.exists():
                with open(onboarding_path, encoding="utf-8") as f:
                    content = f.read()
                
                doc_id = self.ingestor.protocol(
                    title="Onboarding Manager Documentation",
                    content=content,
                    metadata={
                        "type": "onboarding_manager",
                        "source": str(onboarding_path)
                    }
                )
                
                doc_ids.append(doc_id)
                print(f"✅ Onboarding manager ingested: {doc_id}")
            
        except Exception as e:
            print(f"❌ Error ingesting onboarding managers: {e}")
        
        return doc_ids
    
    def ingest_workflow_guides(self) -> list[int]:
        """Ingest workflow guides and protocols."""
        print("\n🔄 Step 3: Ingesting Workflow Guides")
        print("-" * 40)
        
        doc_ids = []
        
        try:
            # Ingest workflow guides
            workflow_path = Path("docs/workflow_guides.md")
            if workflow_path.exists():
                with open(workflow_path, encoding="utf-8") as f:
                    content = f.read()
                
                doc_id = self.ingestor.protocol(
                    title="Workflow Guides and Protocols",
                    content=content,
                    metadata={
                        "type": "workflow_guides",
                        "source": str(workflow_path)
                    }
                )
                
                doc_ids.append(doc_id)
                print(f"✅ Workflow guides ingested: {doc_id}")
            
        except Exception as e:
            print(f"❌ Error ingesting workflow guides: {e}")
        
        return doc_ids
    
    def ingest_agent_protocols(self) -> list[int]:
        """Ingest agent protocols and standards."""
        print("\n📜 Step 4: Ingesting Agent Protocols")
        print("-" * 40)
        
        doc_ids = []
        
        try:
            # Ingest agent protocols
            protocol_path = Path("docs/AGENT_PROTOCOL_SYSTEM.md")
            if protocol_path.exists():
                with open(protocol_path, encoding="utf-8") as f:
                    content = f.read()
                
                doc_id = self.ingestor.protocol(
                    title="Agent Protocol System",
                    content=content,
                    metadata={
                        "type": "agent_protocols",
                        "source": str(protocol_path)
                    }
                )
                
                doc_ids.append(doc_id)
                print(f"✅ Agent protocols ingested: {doc_id}")
            
        except Exception as e:
            print(f"❌ Error ingesting agent protocols: {e}")
        
        return doc_ids
    
    def search_onboarding_docs(self, query: str, limit: int = 5) -> list[dict]:
        """Search onboarding documentation."""
        try:
            results = self.retriever.search(query, k=limit)
            return results
        except Exception as e:
            print(f"❌ Error searching onboarding docs: {e}")
            return []
    
    def get_onboarding_expertise(self, limit: int = 10) -> list[dict]:
        """Get onboarding expertise from vector database."""
        try:
            results = self.retriever.get_agent_expertise("onboarding", k=limit)
            return results
        except Exception as e:
            print(f"❌ Error getting onboarding expertise: {e}")
            return []
