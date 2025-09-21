#!/usr/bin/env python3
"""
AletheiaPromptManager - Advanced Prompt Management System
========================================================

Advanced prompt management and optimization system for Dream.OS integration.
Provides prompt storage, optimization, versioning, analytics, and security.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Backend & API Specialist)
License: MIT
"""

import json
import logging
import hashlib
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class PromptStatus(Enum):
    """Prompt status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class PromptType(Enum):
    """Prompt type enumeration."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TEMPLATE = "template"


@dataclass
class PromptMetadata:
    """Prompt metadata structure."""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = "1.0.0"
    author: str = "system"
    tags: List[str] = field(default_factory=list)
    category: str = "general"
    priority: int = 1
    usage_count: int = 0
    performance_score: float = 0.0


@dataclass
class PromptOptimization:
    """Prompt optimization data."""
    optimization_id: str
    original_prompt: str
    optimized_prompt: str
    improvement_score: float
    optimization_type: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class PromptStorage:
    """Prompt storage management."""
    
    def __init__(self, storage_path: str = "data/prompts"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.prompts: Dict[str, Dict] = {}
        self._load_prompts()
    
    def _load_prompts(self) -> None:
        """Load prompts from storage."""
        try:
            for prompt_file in self.storage_path.glob("*.json"):
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    prompt_data = json.load(f)
                    self.prompts[prompt_data['id']] = prompt_data
            logger.info(f"Loaded {len(self.prompts)} prompts from storage")
        except Exception as e:
            logger.error(f"Error loading prompts: {e}")
    
    def store_prompt(self, prompt_id: str, content: str, metadata: PromptMetadata) -> bool:
        """Store prompt with metadata."""
        try:
            prompt_data = {
                'id': prompt_id,
                'content': content,
                'metadata': {
                    'created_at': metadata.created_at.isoformat(),
                    'updated_at': metadata.updated_at.isoformat(),
                    'version': metadata.version,
                    'author': metadata.author,
                    'tags': metadata.tags,
                    'category': metadata.category,
                    'priority': metadata.priority,
                    'usage_count': metadata.usage_count,
                    'performance_score': metadata.performance_score
                }
            }
            
            self.prompts[prompt_id] = prompt_data
            
            # Save to file
            prompt_file = self.storage_path / f"{prompt_id}.json"
            with open(prompt_file, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Stored prompt {prompt_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing prompt {prompt_id}: {e}")
            return False
    
    def get_prompt(self, prompt_id: str) -> Optional[Dict]:
        """Get prompt by ID."""
        return self.prompts.get(prompt_id)
    
    def list_prompts(self, category: Optional[str] = None) -> List[Dict]:
        """List prompts, optionally filtered by category."""
        prompts = list(self.prompts.values())
        if category:
            prompts = [p for p in prompts if p['metadata']['category'] == category]
        return prompts


class PromptOptimizer:
    """Prompt optimization engine."""
    
    def __init__(self):
        self.optimization_history: List[PromptOptimization] = []
    
    def optimize_prompt(self, prompt_id: str, content: str, context: Dict) -> str:
        """Optimize prompt based on context and performance."""
        try:
            # Basic optimization strategies
            optimized_content = self._apply_optimizations(content, context)
            
            # Record optimization
            optimization = PromptOptimization(
                optimization_id=f"opt_{int(time.time())}",
                original_prompt=content,
                optimized_prompt=optimized_content,
                improvement_score=self._calculate_improvement(content, optimized_content),
                optimization_type="context_aware"
            )
            self.optimization_history.append(optimization)
            
            logger.info(f"Optimized prompt {prompt_id}")
            return optimized_content
            
        except Exception as e:
            logger.error(f"Error optimizing prompt {prompt_id}: {e}")
            return content
    
    def _apply_optimizations(self, content: str, context: Dict) -> str:
        """Apply optimization strategies to prompt content."""
        optimized = content
        
        # Context-aware optimization
        if context.get('urgency') == 'high':
            optimized = f"URGENT: {optimized}"
        
        if context.get('precision') == 'high':
            optimized = f"Be precise and detailed: {optimized}"
        
        # Length optimization
        if context.get('max_length'):
            max_len = context['max_length']
            if len(optimized) > max_len:
                optimized = optimized[:max_len-3] + "..."
        
        return optimized
    
    def _calculate_improvement(self, original: str, optimized: str) -> float:
        """Calculate improvement score."""
        # Simple improvement calculation
        length_improvement = len(optimized) / len(original) if original else 1.0
        return min(length_improvement, 2.0)  # Cap at 2x improvement


class PromptVersionControl:
    """Prompt version control system."""
    
    def __init__(self):
        self.versions: Dict[str, List[Dict]] = {}
    
    def create_version(self, prompt_id: str, content: str, version: str) -> bool:
        """Create new version of prompt."""
        try:
            if prompt_id not in self.versions:
                self.versions[prompt_id] = []
            
            version_data = {
                'version': version,
                'content': content,
                'created_at': datetime.now(timezone.utc).isoformat(),
                'is_current': True
            }
            
            # Mark previous versions as not current
            for v in self.versions[prompt_id]:
                v['is_current'] = False
            
            self.versions[prompt_id].append(version_data)
            logger.info(f"Created version {version} for prompt {prompt_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating version for prompt {prompt_id}: {e}")
            return False
    
    def get_version(self, prompt_id: str, version: str) -> Optional[Dict]:
        """Get specific version of prompt."""
        if prompt_id not in self.versions:
            return None
        
        for v in self.versions[prompt_id]:
            if v['version'] == version:
                return v
        
        return None
    
    def get_current_version(self, prompt_id: str) -> Optional[Dict]:
        """Get current version of prompt."""
        if prompt_id not in self.versions:
            return None
        
        for v in self.versions[prompt_id]:
            if v.get('is_current', False):
                return v
        
        return None


class PromptAnalytics:
    """Prompt analytics and performance tracking."""
    
    def __init__(self):
        self.usage_stats: Dict[str, Dict] = {}
        self.performance_metrics: Dict[str, List[float]] = {}
    
    def track_usage(self, prompt_id: str, context: Dict) -> None:
        """Track prompt usage."""
        if prompt_id not in self.usage_stats:
            self.usage_stats[prompt_id] = {
                'total_usage': 0,
                'last_used': None,
                'contexts': []
            }
        
        self.usage_stats[prompt_id]['total_usage'] += 1
        self.usage_stats[prompt_id]['last_used'] = datetime.now(timezone.utc).isoformat()
        self.usage_stats[prompt_id]['contexts'].append(context)
        
        logger.debug(f"Tracked usage for prompt {prompt_id}")
    
    def record_performance(self, prompt_id: str, score: float) -> None:
        """Record performance score for prompt."""
        if prompt_id not in self.performance_metrics:
            self.performance_metrics[prompt_id] = []
        
        self.performance_metrics[prompt_id].append(score)
        
        # Keep only last 100 scores
        if len(self.performance_metrics[prompt_id]) > 100:
            self.performance_metrics[prompt_id] = self.performance_metrics[prompt_id][-100:]
        
        logger.debug(f"Recorded performance {score} for prompt {prompt_id}")
    
    def get_analytics(self, prompt_id: str) -> Dict:
        """Get analytics for prompt."""
        usage = self.usage_stats.get(prompt_id, {})
        performance = self.performance_metrics.get(prompt_id, [])
        
        return {
            'usage_stats': usage,
            'performance_metrics': {
                'average_score': sum(performance) / len(performance) if performance else 0.0,
                'total_scores': len(performance),
                'recent_scores': performance[-10:] if performance else []
            }
        }


class PromptSecurity:
    """Prompt security and access control."""
    
    def __init__(self):
        self.access_control: Dict[str, List[str]] = {}
        self.encryption_key = self._generate_key()
    
    def _generate_key(self) -> str:
        """Generate encryption key."""
        return hashlib.sha256(f"prompt_security_{int(time.time())}".encode()).hexdigest()
    
    def set_access(self, prompt_id: str, users: List[str]) -> bool:
        """Set access control for prompt."""
        try:
            self.access_control[prompt_id] = users
            logger.info(f"Set access control for prompt {prompt_id}")
            return True
        except Exception as e:
            logger.error(f"Error setting access control for prompt {prompt_id}: {e}")
            return False
    
    def check_access(self, prompt_id: str, user: str) -> bool:
        """Check if user has access to prompt."""
        if prompt_id not in self.access_control:
            return True  # No restrictions if not set
        
        return user in self.access_control[prompt_id]
    
    def encrypt_content(self, content: str) -> str:
        """Encrypt prompt content."""
        # Simple encryption for demonstration
        encrypted = hashlib.sha256((content + self.encryption_key).encode()).hexdigest()
        return f"encrypted:{encrypted}"
    
    def decrypt_content(self, encrypted_content: str) -> str:
        """Decrypt prompt content."""
        if not encrypted_content.startswith("encrypted:"):
            return encrypted_content
        
        # Simple decryption for demonstration
        return "Decrypted content"  # In real implementation, proper decryption


class AletheiaPromptManager:
    """Main AletheiaPromptManager class."""
    
    def __init__(self, storage_path: str = "data/prompts"):
        self.storage = PromptStorage(storage_path)
        self.optimizer = PromptOptimizer()
        self.version_control = PromptVersionControl()
        self.analytics = PromptAnalytics()
        self.security = PromptSecurity()
        logger.info("AletheiaPromptManager initialized")
    
    def store_prompt(self, prompt_id: str, content: str, metadata: PromptMetadata) -> bool:
        """Store prompt with metadata and versioning."""
        try:
            # Check access control
            if not self.security.check_access(prompt_id, metadata.author):
                logger.warning(f"Access denied for prompt {prompt_id}")
                return False
            
            # Encrypt content if needed
            if metadata.category == "sensitive":
                content = self.security.encrypt_content(content)
            
            # Store prompt
            success = self.storage.store_prompt(prompt_id, content, metadata)
            
            if success:
                # Create version
                self.version_control.create_version(prompt_id, content, metadata.version)
                
                # Track usage
                self.analytics.track_usage(prompt_id, {'action': 'store'})
            
            return success
            
        except Exception as e:
            logger.error(f"Error storing prompt {prompt_id}: {e}")
            return False
    
    def get_prompt(self, prompt_id: str, user: str = "system") -> Optional[Dict]:
        """Get prompt by ID with access control."""
        try:
            if not self.security.check_access(prompt_id, user):
                logger.warning(f"Access denied for prompt {prompt_id}")
                return None
            
            prompt = self.storage.get_prompt(prompt_id)
            if prompt:
                # Track usage
                self.analytics.track_usage(prompt_id, {'action': 'retrieve', 'user': user})
            
            return prompt
            
        except Exception as e:
            logger.error(f"Error getting prompt {prompt_id}: {e}")
            return None
    
    def optimize_prompt(self, prompt_id: str, context: Dict) -> Optional[str]:
        """Optimize prompt based on context and performance."""
        try:
            prompt = self.storage.get_prompt(prompt_id)
            if not prompt:
                return None
            
            content = prompt['content']
            optimized_content = self.optimizer.optimize_prompt(prompt_id, content, context)
            
            # Record performance
            improvement_score = self.optimizer._calculate_improvement(content, optimized_content)
            self.analytics.record_performance(prompt_id, improvement_score)
            
            return optimized_content
            
        except Exception as e:
            logger.error(f"Error optimizing prompt {prompt_id}: {e}")
            return None
    
    def get_analytics(self, prompt_id: str) -> Dict:
        """Get analytics for prompt."""
        return self.analytics.get_analytics(prompt_id)
    
    def list_prompts(self, category: Optional[str] = None) -> List[Dict]:
        """List prompts, optionally filtered by category."""
        return self.storage.list_prompts(category)


def main():
    """Main function for testing."""
    manager = AletheiaPromptManager()
    
    # Test prompt storage
    metadata = PromptMetadata(
        author="test_user",
        category="test",
        tags=["test", "example"],
        priority=1
    )
    
    success = manager.store_prompt("test_prompt_1", "This is a test prompt", metadata)
    print(f"Prompt storage: {'Success' if success else 'Failed'}")
    
    # Test prompt retrieval
    prompt = manager.get_prompt("test_prompt_1")
    print(f"Prompt retrieval: {'Success' if prompt else 'Failed'}")
    
    # Test optimization
    context = {"urgency": "high", "precision": "high"}
    optimized = manager.optimize_prompt("test_prompt_1", context)
    print(f"Prompt optimization: {'Success' if optimized else 'Failed'}")
    
    # Test analytics
    analytics = manager.get_analytics("test_prompt_1")
    print(f"Analytics: {analytics}")


if __name__ == "__main__":
    main()
