from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

            from datetime import datetime, timedelta
            import json
from .knowledge_cli import KnowledgeCLI
from .knowledge_models import KnowledgeEntry, KnowledgeEntryBuilder
from .knowledge_search import KnowledgeSearch
from .knowledge_storage import KnowledgeStorage

#!/usr/bin/env python3
"""
Knowledge Database - Agent Cellphone V2 (MODULAR VERSION)
========================================================

Main orchestrator for the modularized knowledge database system.
This file replaces the monolithic knowledge_database.py with a clean,
modular architecture that follows V2 coding standards.

Follows V2 coding standards: ≤300 LOC, OOP design, SRP
"""




class KnowledgeDatabase:
    """Main orchestrator for the modularized knowledge database system"""
    
    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db_path = Path(db_path)
        self.logger = logging.getLogger(f"{__name__}.KnowledgeDatabase")
        
        # Initialize modules
        self.storage = KnowledgeStorage(db_path)
        self.search = KnowledgeSearch(db_path)
        self.cli = KnowledgeCLI(db_path)
        
        self.logger.info(f"Modular knowledge database initialized: {db_path}")
    
    def store_knowledge(self, entry: KnowledgeEntry) -> bool:
        """Store a knowledge entry using the storage module"""
        return self.storage.store_knowledge(entry)
    
    def get_knowledge_by_id(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Retrieve a knowledge entry by ID using the storage module"""
        return self.storage.get_knowledge_by_id(entry_id)
    
    def get_knowledge_by_category(self, category: str, limit: int = 50) -> List[KnowledgeEntry]:
        """Retrieve knowledge entries by category using the storage module"""
        return self.storage.get_knowledge_by_category(category, limit)
    
    def get_knowledge_by_agent(self, agent_id: str, limit: int = 50) -> List[KnowledgeEntry]:
        """Retrieve knowledge entries by agent using the storage module"""
        return self.storage.get_knowledge_by_agent(agent_id, limit)
    
    def search_knowledge(self, query: str, limit: int = 20) -> List[tuple]:
        """Search knowledge base using the search module"""
        return self.search.search_knowledge(query, limit)
    
    def search_by_tags(self, tags: List[str], limit: int = 50) -> List[KnowledgeEntry]:
        """Search by tags using the search module"""
        return self.search.search_by_tags(tags, limit)
    
    def search_by_date_range(self, start_date, end_date, limit: int = 50) -> List[KnowledgeEntry]:
        """Search by date range using the search module"""
        return self.search.search_by_date_range(start_date, end_date, limit)
    
    def get_search_suggestions(self, partial_query: str, limit: int = 10) -> List[str]:
        """Get search suggestions using the search module"""
        return self.search.get_search_suggestions(partial_query, limit)
    
    def get_popular_searches(self, limit: int = 10) -> List[tuple]:
        """Get popular searches using the search module"""
        return self.search.get_popular_searches(limit)
    
    def delete_knowledge(self, entry_id: str) -> bool:
        """Delete a knowledge entry using the storage module"""
        return self.storage.delete_knowledge(entry_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics using the storage module"""
        return self.storage.get_statistics()
    
    def create_entry(self, title: str, content: str, category: str, 
                    tags: List[str], source: str, agent_id: str, 
                    confidence: float = 1.0, related_entries: Optional[List[str]] = None,
                    metadata: Optional[Dict[str, Any]] = None) -> Optional[KnowledgeEntry]:
        """Create a new knowledge entry using the builder pattern"""
        try:
            entry = KnowledgeEntry.create(
                title=title,
                content=content,
                category=category,
                tags=tags or [],
                source=source,
                agent_id=agent_id,
                confidence=confidence,
                related_entries=related_entries or [],
                metadata=metadata or {}
            )
            
            # Store the entry
            if self.store_knowledge(entry):
                self.logger.info(f"Knowledge entry created successfully: {entry.id}")
                return entry
            else:
                self.logger.error("Failed to store knowledge entry")
                return None
                
        except Exception as e:
            self.logger.error(f"Error creating knowledge entry: {e}")
            return None
    
    def update_entry(self, entry_id: str, **kwargs) -> bool:
        """Update an existing knowledge entry"""
        try:
            entry = self.get_knowledge_by_id(entry_id)
            if not entry:
                self.logger.error(f"Entry not found: {entry_id}")
                return False
            
            # Update the entry
            entry.update(**kwargs)
            
            # Store the updated entry
            if self.store_knowledge(entry):
                self.logger.info(f"Knowledge entry updated successfully: {entry_id}")
                return True
            else:
                self.logger.error("Failed to store updated entry")
                return False
                
        except Exception as e:
            self.logger.error(f"Error updating knowledge entry: {e}")
            return False
    
    def add_tag_to_entry(self, entry_id: str, tag: str) -> bool:
        """Add a tag to an existing entry"""
        try:
            entry = self.get_knowledge_by_id(entry_id)
            if not entry:
                return False
            
            entry.add_tag(tag)
            return self.store_knowledge(entry)
            
        except Exception as e:
            self.logger.error(f"Error adding tag: {e}")
            return False
    
    def remove_tag_from_entry(self, entry_id: str, tag: str) -> bool:
        """Remove a tag from an existing entry"""
        try:
            entry = self.get_knowledge_by_id(entry_id)
            if not entry:
                return False
            
            entry.remove_tag(tag)
            return self.store_knowledge(entry)
            
        except Exception as e:
            self.logger.error(f"Error removing tag: {e}")
            return False
    
    def add_related_entry(self, entry_id: str, related_id: str) -> bool:
        """Add a related entry to an existing entry"""
        try:
            entry = self.get_knowledge_by_id(entry_id)
            if not entry:
                return False
            
            entry.add_related_entry(related_id)
            return self.store_knowledge(entry)
            
        except Exception as e:
            self.logger.error(f"Error adding related entry: {e}")
            return False
    
    def remove_related_entry(self, entry_id: str, related_id: str) -> bool:
        """Remove a related entry from an existing entry"""
        try:
            entry = self.get_knowledge_by_id(entry_id)
            if not entry:
                return False
            
            entry.remove_related_entry(related_id)
            return self.store_knowledge(entry)
            
        except Exception as e:
            self.logger.error(f"Error removing related entry: {e}")
            return False
    
    def get_recent_entries(self, days: int = 7, limit: int = 50) -> List[KnowledgeEntry]:
        """Get recent entries within specified days"""
        try:
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            return self.search_by_date_range(start_date, end_date, limit)
            
        except Exception as e:
            self.logger.error(f"Error getting recent entries: {e}")
            return []
    
    def get_high_confidence_entries(self, min_confidence: float = 0.8, limit: int = 50) -> List[KnowledgeEntry]:
        """Get entries with high confidence scores"""
        try:
            # This would require a new method in storage module
            # For now, get all entries and filter
            all_entries = self.storage.get_knowledge_by_category("", 1000)  # Get many entries
            high_confidence = [entry for entry in all_entries if entry.confidence >= min_confidence]
            return sorted(high_confidence, key=lambda x: x.confidence, reverse=True)[:limit]
            
        except Exception as e:
            self.logger.error(f"Error getting high confidence entries: {e}")
            return []
    
    def export_entries_to_json(self, filepath: str, entries: Optional[List[KnowledgeEntry]] = None) -> bool:
        """Export entries to JSON file"""
        try:
            
            if entries is None:
                # Export all entries
                entries = self.storage.get_knowledge_by_category("", 10000)
            
            # Convert entries to dictionaries
            export_data = []
            for entry in entries:
                export_data.append(entry.to_dict())
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Exported {len(export_data)} entries to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting entries: {e}")
            return False
    
    def import_entries_from_json(self, filepath: str) -> int:
        """Import entries from JSON file"""
        try:
            
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            imported_count = 0
            for entry_data in import_data:
                try:
                    entry = KnowledgeEntry.from_dict(entry_data)
                    if self.store_knowledge(entry):
                        imported_count += 1
                except Exception as e:
                    self.logger.warning(f"Failed to import entry: {e}")
                    continue
            
            self.logger.info(f"Imported {imported_count} entries from {filepath}")
            return imported_count
            
        except Exception as e:
            self.logger.error(f"Error importing entries: {e}")
            return 0
    
    def close(self):
        """Close all database connections"""
        self.storage.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Convenience function for backward compatibility
def create_knowledge_database(db_path: str = "knowledge_base.db") -> KnowledgeDatabase:
    """Create and return a new knowledge database instance"""
    return KnowledgeDatabase(db_path)


# Export main class and convenience function
__all__ = [
    'KnowledgeDatabase',
    'create_knowledge_database'
]
