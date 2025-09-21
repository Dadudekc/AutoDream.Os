#!/usr/bin/env python3
"""
Template-Based Messaging System for Phase 2.3 Enhanced Discord Integration

V2 Compliance: ≤400 lines, 3 classes, 10 functions
Purpose: Jinja2 template engine for Discord message generation
"""

import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template, TemplateError
from pathlib import Path


class TemplateEngine:
    """Jinja2 template engine for Discord message generation"""
    
    def __init__(self, template_dir: str = "templates/discord"):
        """Initialize template engine with template directory"""
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=False,  # Discord supports markdown
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Register custom filters
        self._register_filters()
        
        # Load default templates
        self._load_default_templates()
    
    def _register_filters(self) -> None:
        """Register custom Jinja2 filters for Discord formatting"""
        def format_timestamp(timestamp: datetime) -> str:
            """Format timestamp for Discord display"""
            return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
        
        def format_priority(priority: str) -> str:
            """Format priority with emoji"""
            priority_emojis = {
                "LOW": "🟢",
                "NORMAL": "🟡", 
                "HIGH": "🟠",
                "URGENT": "🔴"
            }
            return f"{priority_emojis.get(priority, '⚪')} {priority}"
        
        def truncate_text(text: str, max_length: int = 100) -> str:
            """Truncate text for Discord message limits"""
            if len(text) <= max_length:
                return text
            return text[:max_length-3] + "..."
        
        self.env.filters['timestamp'] = format_timestamp
        self.env.filters['priority'] = format_priority
        self.env.filters['truncate'] = truncate_text
    
    def _load_default_templates(self) -> None:
        """Load default Discord message templates"""
        default_templates = {
            "agent_status.j2": """
🎯 **AGENT STATUS UPDATE**
**Agent:** {{ agent_id }}
**Status:** {{ status }}
**Task:** {{ current_task or 'No active task' }}
**Progress:** {{ progress }}%
**Next Action:** {{ next_action or 'Awaiting assignment' }}
**Timestamp:** {{ timestamp | timestamp }}
{% if notes %}**Notes:** {{ notes | truncate(200) }}{% endif %}
""",
            
            "system_alert.j2": """
🚨 **SYSTEM ALERT**
**Type:** {{ alert_type }}
**Severity:** {{ severity | priority }}
**Message:** {{ message }}
**Timestamp:** {{ timestamp | timestamp }}
{% if affected_agents %}**Affected Agents:** {{ affected_agents | join(', ') }}{% endif %}
{% if resolution_steps %}**Resolution Steps:** {{ resolution_steps | truncate(300) }}{% endif %}
""",
            
            "coordination_request.j2": """
📋 **COORDINATION REQUEST**
**From:** {{ from_agent }}
**To:** {{ to_agent }}
**Priority:** {{ priority | priority }}
**Request:** {{ request }}
**Deadline:** {{ deadline | timestamp }}
{% if context %}**Context:** {{ context | truncate(200) }}{% endif %}
{% if expected_response %}**Expected Response:** {{ expected_response }}{% endif %}
""",
            
            "task_completion.j2": """
✅ **TASK COMPLETION**
**Agent:** {{ agent_id }}
**Task:** {{ task_title }}
**Status:** {{ status }}
**Duration:** {{ duration }}
**Deliverables:** {{ deliverables | length }} items
**Timestamp:** {{ timestamp | timestamp }}
{% if notes %}**Notes:** {{ notes | truncate(200) }}{% endif %}
""",
            
            "swarm_coordination.j2": """
🐝 **SWARM COORDINATION**
**Event:** {{ event_type }}
**Source:** {{ source_agent }}
**Targets:** {{ target_agents | join(', ') }}
**Priority:** {{ priority | priority }}
**Message:** {{ message }}
**Timestamp:** {{ timestamp | timestamp }}
{% if coordination_data %}**Data:** {{ coordination_data | truncate(300) }}{% endif %}
"""
        }
        
        # Write default templates to files
        for filename, content in default_templates.items():
            template_path = self.template_dir / filename
            if not template_path.exists():
                template_path.write_text(content.strip())
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render template with provided context"""
        try:
            template = self.env.get_template(template_name)
            return template.render(context)
        except TemplateError as e:
            return f"❌ **Template Error:** {str(e)}"
        except Exception as e:
            return f"❌ **Rendering Error:** {str(e)}"
    
    def get_available_templates(self) -> List[str]:
        """Get list of available templates"""
        return [f.name for f in self.template_dir.glob("*.j2")]


class MessageRenderer:
    """Message rendering with context injection and validation"""
    
    def __init__(self, template_engine: TemplateEngine):
        """Initialize message renderer with template engine"""
        self.template_engine = template_engine
        self.max_message_length = 2000  # Discord message limit
    
    def render_agent_status(self, agent_data: Dict[str, Any]) -> str:
        """Render agent status message"""
        context = {
            "agent_id": agent_data.get("agent_id", "Unknown"),
            "status": agent_data.get("status", "Unknown"),
            "current_task": agent_data.get("current_task"),
            "progress": agent_data.get("progress", 0),
            "next_action": agent_data.get("next_action"),
            "notes": agent_data.get("notes"),
            "timestamp": datetime.utcnow()
        }
        return self.template_engine.render_template("agent_status.j2", context)
    
    def render_system_alert(self, alert_data: Dict[str, Any]) -> str:
        """Render system alert message"""
        context = {
            "alert_type": alert_data.get("alert_type", "Unknown"),
            "severity": alert_data.get("severity", "NORMAL"),
            "message": alert_data.get("message", "No message"),
            "affected_agents": alert_data.get("affected_agents", []),
            "resolution_steps": alert_data.get("resolution_steps"),
            "timestamp": datetime.utcnow()
        }
        return self.template_engine.render_template("system_alert.j2", context)
    
    def render_coordination_request(self, request_data: Dict[str, Any]) -> str:
        """Render coordination request message"""
        context = {
            "from_agent": request_data.get("from_agent", "Unknown"),
            "to_agent": request_data.get("to_agent", "Unknown"),
            "priority": request_data.get("priority", "NORMAL"),
            "request": request_data.get("request", "No request"),
            "deadline": request_data.get("deadline", datetime.utcnow()),
            "context": request_data.get("context"),
            "expected_response": request_data.get("expected_response")
        }
        return self.template_engine.render_template("coordination_request.j2", context)
    
    def render_task_completion(self, task_data: Dict[str, Any]) -> str:
        """Render task completion message"""
        context = {
            "agent_id": task_data.get("agent_id", "Unknown"),
            "task_title": task_data.get("task_title", "Unknown Task"),
            "status": task_data.get("status", "Completed"),
            "duration": task_data.get("duration", "Unknown"),
            "deliverables": task_data.get("deliverables", []),
            "notes": task_data.get("notes"),
            "timestamp": datetime.utcnow()
        }
        return self.template_engine.render_template("task_completion.j2", context)
    
    def render_swarm_coordination(self, coordination_data: Dict[str, Any]) -> str:
        """Render swarm coordination message"""
        context = {
            "event_type": coordination_data.get("event_type", "Unknown"),
            "source_agent": coordination_data.get("source_agent", "Unknown"),
            "target_agents": coordination_data.get("target_agents", []),
            "priority": coordination_data.get("priority", "NORMAL"),
            "message": coordination_data.get("message", "No message"),
            "coordination_data": coordination_data.get("coordination_data"),
            "timestamp": datetime.utcnow()
        }
        return self.template_engine.render_template("swarm_coordination.j2", context)
    
    def validate_message_length(self, message: str) -> str:
        """Validate and truncate message if necessary"""
        if len(message) <= self.max_message_length:
            return message
        
        # Truncate and add truncation indicator
        truncated = message[:self.max_message_length - 50]
        return truncated + "\n\n... (message truncated)"


class TemplateRegistry:
    """Template registration and management system"""
    
    def __init__(self, template_engine: TemplateEngine):
        """Initialize template registry"""
        self.template_engine = template_engine
        self.custom_templates = {}
        self.template_metadata = {}
    
    def register_template(self, name: str, template_content: str, 
                         metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Register custom template"""
        try:
            # Validate template syntax
            template = self.template_engine.env.from_string(template_content)
            template.render()  # Test render with empty context
            
            # Store template
            self.custom_templates[name] = template_content
            self.template_metadata[name] = metadata or {}
            
            # Write to file
            template_path = self.template_engine.template_dir / f"{name}.j2"
            template_path.write_text(template_content)
            
            return True
        except Exception as e:
            print(f"Template registration failed: {e}")
            return False
    
    def get_template_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get template information and metadata"""
        if name in self.custom_templates:
            return {
                "name": name,
                "type": "custom",
                "metadata": self.template_metadata.get(name, {}),
                "content": self.custom_templates[name]
            }
        
        # Check if it's a default template
        template_path = self.template_engine.template_dir / f"{name}.j2"
        if template_path.exists():
            return {
                "name": name,
                "type": "default",
                "metadata": {},
                "content": template_path.read_text()
            }
        
        return None
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates with metadata"""
        templates = []
        
        # Add default templates
        for template_file in self.template_engine.template_dir.glob("*.j2"):
            if template_file.name not in self.custom_templates:
                templates.append({
                    "name": template_file.stem,
                    "type": "default",
                    "metadata": {},
                    "file_path": str(template_file)
                })
        
        # Add custom templates
        for name, content in self.custom_templates.items():
            templates.append({
                "name": name,
                "type": "custom",
                "metadata": self.template_metadata.get(name, {}),
                "content": content
            })
        
        return templates


# Example usage and testing
if __name__ == "__main__":
    # Initialize template system
    template_engine = TemplateEngine()
    message_renderer = MessageRenderer(template_engine)
    template_registry = TemplateRegistry(template_engine)
    
    # Test agent status rendering
    agent_data = {
        "agent_id": "Agent-2",
        "status": "Active",
        "current_task": "Phase 2.3 Discord Architecture Design",
        "progress": 75,
        "next_action": "Complete template system implementation",
        "notes": "V2 compliance maintained throughout design"
    }
    
    status_message = message_renderer.render_agent_status(agent_data)
    print("Agent Status Message:")
    print(status_message)
    print("\n" + "="*50 + "\n")
    
    # Test system alert rendering
    alert_data = {
        "alert_type": "V2 Compliance Violation",
        "severity": "HIGH",
        "message": "File exceeds 400 line limit",
        "affected_agents": ["Agent-3", "Agent-6"],
        "resolution_steps": "Refactor file into smaller modules"
    }
    
    alert_message = message_renderer.render_system_alert(alert_data)
    print("System Alert Message:")
    print(alert_message)
    print("\n" + "="*50 + "\n")
    
    # List available templates
    templates = template_registry.list_templates()
    print("Available Templates:")
    for template in templates:
        print(f"- {template['name']} ({template['type']})")


