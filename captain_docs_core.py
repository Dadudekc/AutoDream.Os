"""
Captain Documentation Core - V2 Compliant
=========================================

Core Captain documentation ingestion functionality.
Maintains single responsibility principle.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-6 SSOT_MANAGER
License: MIT
"""
import json
import sys
from pathlib import Path
from typing import Any

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from swarm_brain import Ingestor, Retriever, SwarmBrain


class CaptainDocumentationCore:
    """Core Captain documentation ingestion functionality."""
    
    def __init__(self):
        """Initialize the documentation core."""
        self.brain = SwarmBrain()
        self.ingestor = Ingestor(self.brain)
        self.retriever = Retriever(self.brain)
        print("🧠 Captain Documentation Core initialized")
    
    def ingest_captain_log(self, log_path: str) -> int:
        """Ingest Captain's log into vector database."""
        try:
            with open(log_path, encoding="utf-8") as f:
                log_content = f.read()
            
            # Parse log metadata
            log_lines = log_content.split("\n")
            date_line = [line for line in log_lines if line.startswith("**Date:**")]
            date = date_line[0].split("**Date:**")[1].strip() if date_line else "2025-01-17"
            
            # Extract key sections
            sections = self._parse_log_sections(log_content)
            
            # Ingest as protocol document
            doc_id = self.ingestor.protocol(
                title=f"Captain Log - {date}",
                content=log_content,
                metadata={
                    "type": "captain_log",
                    "date": date,
                    "sections": sections,
                    "source": log_path
                }
            )
            
            print(f"✅ Captain log ingested: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"❌ Error ingesting Captain log: {e}")
            return 0
    
    def _parse_log_sections(self, content: str) -> list[str]:
        """Parse log content into sections."""
        sections = []
        lines = content.split("\n")
        
        current_section = ""
        for line in lines:
            if line.startswith("##") or line.startswith("###"):
                if current_section:
                    sections.append(current_section.strip())
                current_section = line
            elif current_section:
                current_section += "\n" + line
        
        if current_section:
            sections.append(current_section.strip())
        
        return sections
    
    def ingest_captain_handbook(self, handbook_path: str) -> int:
        """Ingest Captain's handbook into vector database."""
        try:
            with open(handbook_path, encoding="utf-8") as f:
                handbook_content = f.read()
            
            # Ingest as protocol document
            doc_id = self.ingestor.protocol(
                title="Captain Handbook",
                content=handbook_content,
                metadata={
                    "type": "captain_handbook",
                    "source": handbook_path
                }
            )
            
            print(f"✅ Captain handbook ingested: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"❌ Error ingesting Captain handbook: {e}")
            return 0
    
    def ingest_captain_cheatsheet(self, cheatsheet_path: str) -> int:
        """Ingest Captain's cheatsheet into vector database."""
        try:
            with open(cheatsheet_path, encoding="utf-8") as f:
                cheatsheet_content = f.read()
            
            # Ingest as protocol document
            doc_id = self.ingestor.protocol(
                title="Captain Cheatsheet",
                content=cheatsheet_content,
                metadata={
                    "type": "captain_cheatsheet",
                    "source": cheatsheet_path
                }
            )
            
            print(f"✅ Captain cheatsheet ingested: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"❌ Error ingesting Captain cheatsheet: {e}")
            return 0
    
    def search_captain_docs(self, query: str, limit: int = 5) -> list[dict]:
        """Search Captain documentation."""
        try:
            results = self.retriever.search(query, k=limit)
            return results
        except Exception as e:
            print(f"❌ Error searching Captain docs: {e}")
            return []
    
    def get_captain_expertise(self, limit: int = 10) -> list[dict]:
        """Get Captain expertise from vector database."""
        try:
            results = self.retriever.get_agent_expertise("Captain Agent-4", k=limit)
            return results
        except Exception as e:
            print(f"❌ Error getting Captain expertise: {e}")
            return []
