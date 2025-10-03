#!/usr/bin/env python3
"""
Anti-Slop Protocol Implementation
================================

V2 Compliant: ≤400 lines, implements anti-slop protocol
to prevent meaningless file generation and content bloat.

This module implements content deduplication, quality gates,
and generation limits to prevent autonomous agents from
generating slop content.

🐝 WE ARE SWARM - Anti-Slop Protocol
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AntiSlopProtocol:
    """Implements anti-slop protocol to prevent content bloat."""
    
    def __init__(self, content_dir: str = "content_registry"):
        """Initialize anti-slop protocol."""
        self.content_dir = Path(content_dir)
        self.content_dir.mkdir(exist_ok=True)
        
        # Content generation limits
        self.max_files_per_cycle = 5
        self.max_content_per_file = 10240  # 10KB
        self.min_content_length = 100
        self.max_repetition_ratio = 0.2  # 20% repetition allowed
        self.unique_content_threshold = 0.8  # 80% unique content required
        
        # Content registry file
        self.registry_file = self.content_dir / "content_registry.json"
        self.content_registry = self._load_registry()
        
    def _load_registry(self) -> Dict[str, Any]:
        """Load content registry from file."""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading registry: {e}")
        
        return {
            "content_hashes": {},
            "agent_stats": {},
            "generation_history": [],
            "last_cleanup": None
        }
    
    def _save_registry(self):
        """Save content registry to file."""
        try:
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(self.content_registry, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving registry: {e}")
    
    def check_content_quality(self, content: str, agent_id: str) -> Dict[str, Any]:
        """Check if content meets quality standards."""
        result = {
            "approved": False,
            "reasons": [],
            "content_hash": hashlib.md5(content.encode()).hexdigest(),
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        # Check content length
        if len(content) < self.min_content_length:
            result["reasons"].append(f"Content too short: {len(content)} chars (min: {self.min_content_length})")
        
        # Check content size
        if len(content) > self.max_content_per_file:
            result["reasons"].append(f"Content too large: {len(content)} chars (max: {self.max_content_per_file})")
        
        # Check for duplicate content
        content_hash = result["content_hash"]
        if content_hash in self.content_registry["content_hashes"]:
            result["reasons"].append("Duplicate content detected")
        
        # Check repetition ratio
        repetition_ratio = self._calculate_repetition_ratio(content)
        if repetition_ratio > self.max_repetition_ratio:
            result["reasons"].append(f"Too much repetition: {repetition_ratio:.2%} (max: {self.max_repetition_ratio:.2%})")
        
        # Check unique content ratio
        unique_ratio = self._calculate_unique_ratio(content)
        if unique_ratio < self.unique_content_threshold:
            result["reasons"].append(f"Insufficient unique content: {unique_ratio:.2%} (min: {self.unique_content_threshold:.2%})")
        
        # Check agent generation limits
        if not self._check_agent_limits(agent_id):
            result["reasons"].append("Agent generation limit exceeded")
        
        # Approve if no issues
        if not result["reasons"]:
            result["approved"] = True
            self._register_content(content, agent_id, result["content_hash"])
        
        return result
    
    def _calculate_repetition_ratio(self, content: str) -> float:
        """Calculate repetition ratio in content."""
        words = content.split()
        if len(words) < 10:
            return 0.0
        
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        repeated_words = sum(count - 1 for count in word_counts.values() if count > 1)
        total_words = len(words)
        
        return repeated_words / total_words if total_words > 0 else 0.0
    
    def _calculate_unique_ratio(self, content: str) -> float:
        """Calculate unique content ratio."""
        words = content.split()
        if len(words) < 10:
            return 1.0
        
        unique_words = len(set(words))
        total_words = len(words)
        
        return unique_words / total_words if total_words > 0 else 0.0
    
    def _check_agent_limits(self, agent_id: str) -> bool:
        """Check if agent has exceeded generation limits."""
        agent_stats = self.content_registry["agent_stats"].get(agent_id, {})
        current_cycle = datetime.now().strftime("%Y-%m-%d-%H")
        
        if agent_stats.get("current_cycle") != current_cycle:
            # Reset for new cycle
            agent_stats["current_cycle"] = current_cycle
            agent_stats["files_generated"] = 0
        
        return agent_stats.get("files_generated", 0) < self.max_files_per_cycle
    
    def _register_content(self, content: str, agent_id: str, content_hash: str):
        """Register approved content in registry."""
        # Register content hash
        self.content_registry["content_hashes"][content_hash] = {
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "content_length": len(content)
        }
        
        # Update agent stats
        if agent_id not in self.content_registry["agent_stats"]:
            self.content_registry["agent_stats"][agent_id] = {}
        
        agent_stats = self.content_registry["agent_stats"][agent_id]
        agent_stats["files_generated"] = agent_stats.get("files_generated", 0) + 1
        agent_stats["total_files"] = agent_stats.get("total_files", 0) + 1
        
        # Add to generation history
        self.content_registry["generation_history"].append({
            "agent_id": agent_id,
            "content_hash": content_hash,
            "timestamp": datetime.now().isoformat(),
            "content_length": len(content)
        })
        
        # Keep only last 1000 entries
        if len(self.content_registry["generation_history"]) > 1000:
            self.content_registry["generation_history"] = self.content_registry["generation_history"][-1000:]
        
        self._save_registry()
    
    def cleanup_old_content(self, days_old: int = 7):
        """Clean up old content from registry."""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        cutoff_str = cutoff_date.isoformat()
        
        # Clean up content hashes
        old_hashes = []
        for content_hash, data in self.content_registry["content_hashes"].items():
            if data["timestamp"] < cutoff_str:
                old_hashes.append(content_hash)
        
        for content_hash in old_hashes:
            del self.content_registry["content_hashes"][content_hash]
        
        # Clean up generation history
        self.content_registry["generation_history"] = [
            entry for entry in self.content_registry["generation_history"]
            if entry["timestamp"] >= cutoff_str
        ]
        
        self.content_registry["last_cleanup"] = datetime.now().isoformat()
        self._save_registry()
        
        logger.info(f"Cleaned up {len(old_hashes)} old content entries")

def main():
    """Main execution function."""
    protocol = AntiSlopProtocol()
    
    # Test content quality check
    test_content = "This is a test content for quality checking. It should be unique and meaningful."
    result = protocol.check_content_quality(test_content, "Agent-8")
    
    print(f"Content approved: {result['approved']}")
    if result["reasons"]:
        print(f"Reasons: {result['reasons']}")
    
    # Cleanup old content
    protocol.cleanup_old_content()

if __name__ == "__main__":
    main()
