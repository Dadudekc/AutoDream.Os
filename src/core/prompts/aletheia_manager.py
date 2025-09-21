"""
AletheiaPromptManager - Advanced prompt management system.
Based on Dream.OS patterns with V2 compliance and KISS principles.

Features:
- Jinja2 template-based prompt generation
- Memory-aware prompt generation
- Template caching and optimization
- Context management
- Performance monitoring
"""

import os
import sys
import json
import re
import threading
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Union, Callable, Optional
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path

logger = logging.getLogger(__name__)

class AletheiaPromptManager:
    """
    Advanced prompt management system with template-based generation.
    V2 Compliant: ≤400 lines, simple data classes, direct method calls.
    """
    
    def __init__(self, template_dir: str = "templates/prompts", memory_dir: str = "memory"):
        """Initialize AletheiaPromptManager."""
        self.template_dir = Path(template_dir)
        self.memory_dir = Path(memory_dir)
        self.template_cache: Dict[str, Template] = {}
        self.memory_cache: Dict[str, Any] = {}
        self._lock = threading.Lock()
        
        # Ensure directories exist
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Load memory cache
        self._load_memory_cache()
        
        logger.info(f"AletheiaPromptManager initialized with template dir: {self.template_dir}")
    
    def _load_memory_cache(self) -> None:
        """Load memory cache from disk."""
        try:
            memory_file = self.memory_dir / "prompt_memory.json"
            if memory_file.exists():
                with open(memory_file, 'r') as f:
                    self.memory_cache = json.load(f)
                logger.info(f"Memory cache loaded: {len(self.memory_cache)} entries")
        except Exception as e:
            logger.warning(f"Failed to load memory cache: {e}")
            self.memory_cache = {}
    
    def _save_memory_cache(self) -> None:
        """Save memory cache to disk."""
        try:
            memory_file = self.memory_dir / "prompt_memory.json"
            with open(memory_file, 'w') as f:
                json.dump(self.memory_cache, f, indent=2)
            logger.info(f"Memory cache saved: {len(self.memory_cache)} entries")
        except Exception as e:
            logger.error(f"Failed to save memory cache: {e}")
    
    def _get_template(self, template_name: str) -> Template:
        """Get template from cache or load from disk."""
        with self._lock:
            if template_name not in self.template_cache:
                try:
                    template = self.jinja_env.get_template(template_name)
                    self.template_cache[template_name] = template
                    logger.info(f"Template loaded: {template_name}")
                except Exception as e:
                    logger.error(f"Failed to load template {template_name}: {e}")
                    raise
            
            return self.template_cache[template_name]
    
    def generate_prompt(self, 
                       template_name: str, 
                       context: Dict[str, Any], 
                       memory_key: Optional[str] = None) -> str:
        """Generate prompt from template with context and memory."""
        try:
            # Get template
            template = self._get_template(template_name)
            
            # Prepare context with memory
            prompt_context = context.copy()
            
            # Add memory if provided
            if memory_key and memory_key in self.memory_cache:
                prompt_context['memory'] = self.memory_cache[memory_key]
            
            # Add timestamp
            prompt_context['timestamp'] = datetime.now(timezone.utc).isoformat()
            
            # Generate prompt
            prompt = template.render(**prompt_context)
            
            # Update memory cache
            if memory_key:
                self.memory_cache[memory_key] = {
                    'last_used': datetime.now(timezone.utc).isoformat(),
                    'context': context,
                    'generated_prompt': prompt
                }
                self._save_memory_cache()
            
            logger.info(f"Prompt generated from template: {template_name}")
            return prompt
            
        except Exception as e:
            logger.error(f"Failed to generate prompt from {template_name}: {e}")
            raise
    
    def create_template(self, template_name: str, content: str) -> bool:
        """Create a new template file."""
        try:
            template_file = self.template_dir / template_name
            with open(template_file, 'w') as f:
                f.write(content)
            
            # Clear cache for this template
            with self._lock:
                if template_name in self.template_cache:
                    del self.template_cache[template_name]
            
            logger.info(f"Template created: {template_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create template {template_name}: {e}")
            return False
    
    def update_template(self, template_name: str, content: str) -> bool:
        """Update an existing template file."""
        try:
            template_file = self.template_dir / template_name
            if not template_file.exists():
                logger.warning(f"Template {template_name} does not exist")
                return False
            
            with open(template_file, 'w') as f:
                f.write(content)
            
            # Clear cache for this template
            with self._lock:
                if template_name in self.template_cache:
                    del self.template_cache[template_name]
            
            logger.info(f"Template updated: {template_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update template {template_name}: {e}")
            return False
    
    def delete_template(self, template_name: str) -> bool:
        """Delete a template file."""
        try:
            template_file = self.template_dir / template_name
            if not template_file.exists():
                logger.warning(f"Template {template_name} does not exist")
                return False
            
            template_file.unlink()
            
            # Clear cache for this template
            with self._lock:
                if template_name in self.template_cache:
                    del self.template_cache[template_name]
            
            logger.info(f"Template deleted: {template_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete template {template_name}: {e}")
            return False
    
    def list_templates(self) -> List[str]:
        """List all available templates."""
        try:
            templates = []
            for file_path in self.template_dir.glob("*.j2"):
                templates.append(file_path.name)
            return templates
        except Exception as e:
            logger.error(f"Failed to list templates: {e}")
            return []
    
    def get_template_content(self, template_name: str) -> Optional[str]:
        """Get template content."""
        try:
            template_file = self.template_dir / template_name
            if not template_file.exists():
                return None
            
            with open(template_file, 'r') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to get template content {template_name}: {e}")
            return None
    
    def update_memory(self, key: str, value: Any) -> None:
        """Update memory cache."""
        with self._lock:
            self.memory_cache[key] = {
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'value': value
            }
            self._save_memory_cache()
    
    def get_memory(self, key: str) -> Optional[Any]:
        """Get value from memory cache."""
        with self._lock:
            return self.memory_cache.get(key)
    
    def clear_memory(self, key: Optional[str] = None) -> None:
        """Clear memory cache."""
        with self._lock:
            if key:
                if key in self.memory_cache:
                    del self.memory_cache[key]
                    self._save_memory_cache()
            else:
                self.memory_cache.clear()
                self._save_memory_cache()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get prompt manager statistics."""
        with self._lock:
            return {
                'templates_cached': len(self.template_cache),
                'memory_entries': len(self.memory_cache),
                'template_dir': str(self.template_dir),
                'memory_dir': str(self.memory_dir)
            }

# Global prompt manager instance
prompt_manager = AletheiaPromptManager()

def generate_prompt(template_name: str, context: Dict[str, Any], memory_key: Optional[str] = None) -> str:
    """Generate prompt from template."""
    return prompt_manager.generate_prompt(template_name, context, memory_key)

def create_template(template_name: str, content: str) -> bool:
    """Create a new template."""
    return prompt_manager.create_template(template_name, content)

def update_template(template_name: str, content: str) -> bool:
    """Update an existing template."""
    return prompt_manager.update_template(template_name, content)

def delete_template(template_name: str) -> bool:
    """Delete a template."""
    return prompt_manager.delete_template(template_name)

def list_templates() -> List[str]:
    """List all templates."""
    return prompt_manager.list_templates()

def get_template_content(template_name: str) -> Optional[str]:
    """Get template content."""
    return prompt_manager.get_template_content(template_name)

def update_memory(key: str, value: Any) -> None:
    """Update memory cache."""
    prompt_manager.update_memory(key, value)

def get_memory(key: str) -> Optional[Any]:
    """Get value from memory cache."""
    return prompt_manager.get_memory(key)

def clear_memory(key: Optional[str] = None) -> None:
    """Clear memory cache."""
    prompt_manager.clear_memory(key)

def get_prompt_stats() -> Dict[str, Any]:
    """Get prompt manager statistics."""
    return prompt_manager.get_stats()

