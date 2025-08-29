#!/usr/bin/env python3
"""
Frontend UI Module
Agent_Cellphone_V2_Repository TDD Integration Project

This module handles all UI component concerns extracted from the monolithic frontend_app.py file.

Author: Agent-8 (Integration Enhancement Manager)
Contract: MODERATE-021 - Frontend App Modularization
License: MIT
"""

import json
import uuid
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# Mock logger for testing
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import from core module (commented out for testing)
# from .frontend_app_core import UIComponent, create_component



# ============================================================================
# UI COMPONENT MODELS & DATA STRUCTURES
# ============================================================================

@dataclass
class UIComponent:
    """Represents a UI component with its properties and state"""
    
    id: str
    type: str
    props: Dict[str, Any]
    state: Dict[str, Any]
    children: List["UIComponent"]
    event_handlers: Dict[str, str]
    created_at: datetime
    updated_at: datetime


@dataclass
class UITheme:
    """UI theme configuration"""
    
    name: str
    colors: Dict[str, str]
    fonts: Dict[str, str]
    spacing: Dict[str, str]
    shadows: Dict[str, str]
    created_at: datetime
    updated_at: datetime


@dataclass
class UIStyle:
    """UI style configuration"""
    
    component_type: str
    css_classes: List[str]
    inline_styles: Dict[str, str]
    responsive_breakpoints: Dict[str, Dict[str, str]]
    animations: List[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class UIEvent:
    """UI event configuration"""
    
    event_type: str
    handler: str
    target: str
    prevent_default: bool
    stop_propagation: bool
    debounce_ms: Optional[int]
    throttle_ms: Optional[int]
    created_at: datetime
    updated_at: datetime


class UIComponentRenderer:
    """Renders UI components to HTML"""
    
    def __init__(self):
        self.template_engine = "jinja2"  # Default template engine
        self.partial_templates: Dict[str, str] = {}
        self.global_styles: Dict[str, str] = {}
    
    def render_component(self, component: UIComponent) -> str:
        """Render a UI component to HTML"""
        try:
            # Get component template
            template = self._get_component_template(component)
            
            # Apply component props and state
            rendered = self._apply_component_data(template, component)
            
            # Apply component styles
            rendered = self._apply_component_styles(rendered, component)
            
            # Apply component scripts
            rendered = self._apply_component_scripts(rendered, component)
            
            return rendered
            
        except Exception as e:
            logger.error(f"Error rendering component {component.type}: {e}")
            return f"<div class='error'>Error rendering component: {str(e)}</div>"
    
    def _get_component_template(self, component: UIComponent) -> str:
        """Get component template"""
        # This would typically load from a template file or database
        # For now, return a basic template
        return f"<div class='component {component.type.lower()}' id='{component.id}'></div>"
    
    def _apply_component_data(self, template: str, component: UIComponent) -> str:
        """Apply component props and state to template"""
        # Simple template variable replacement
        rendered = template
        
        # Replace props
        for key, value in component.props.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in rendered:
                rendered = rendered.replace(placeholder, str(value))
        
        # Replace state
        for key, value in component.state.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in rendered:
                rendered = rendered.replace(placeholder, str(value))
        
        return rendered
    
    def _apply_component_styles(self, html: str, component: UIComponent) -> str:
        """Apply component styles"""
        # This would typically inject CSS into the HTML
        # For now, just return the HTML as-is
        return html
    
    def _apply_component_scripts(self, html: str, component: UIComponent) -> str:
        """Apply component scripts"""
        # This would typically inject JavaScript into the HTML
        # For now, just return the HTML as-is
        return html


class UIComponentLibrary:
    """Library of pre-built UI components"""
    
    def __init__(self):
        self.components: Dict[str, Dict[str, Any]] = {}
        self._register_default_components()
    
    def _register_default_components(self):
        """Register default UI components"""
        # Button component
        self.components["Button"] = {
            "template": '<button class="btn btn-{{ variant }}" id="{{ id }}">{{ text }}</button>',
            "style": """
                .btn {
                    padding: 8px 16px;
                    border-radius: 4px;
                    border: none;
                    cursor: pointer;
                    font-size: 14px;
                    transition: all 0.2s ease;
                }
                .btn-primary { background-color: #007bff; color: white; }
                .btn-secondary { background-color: #6c757d; color: white; }
                .btn-success { background-color: #28a745; color: white; }
                .btn-danger { background-color: #dc3545; color: white; }
                .btn:hover { opacity: 0.8; transform: translateY(-1px); }
            """,
            "script": """
                function handleButtonClick(event) {
                    const button = event.target;
                    const componentId = button.id;
                    console.log('Button clicked:', componentId);
                    
                    // Emit component event
                    if (window.emitComponentEvent) {
                        window.emitComponentEvent(componentId, 'click', {
                            buttonText: button.textContent,
                            timestamp: new Date().toISOString()
                        });
                    }
                }
            """,
            "props": ["text", "variant"],
            "events": ["click"]
        }
        
        # Card component
        self.components["Card"] = {
            "template": """
                <div class="card" id="{{ id }}">
                    <div class="card-header">{{ title }}</div>
                    <div class="card-body">{{ content }}</div>
                    <div class="card-footer">{{ footer }}</div>
                </div>
            """,
            "style": """
                .card {
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    margin: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .card-header {
                    padding: 12px 16px;
                    background-color: #f8f9fa;
                    border-bottom: 1px solid #ddd;
                    font-weight: bold;
                }
                .card-body {
                    padding: 16px;
                }
                .card-footer {
                    padding: 12px 16px;
                    background-color: #f8f9fa;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #666;
                }
            """,
            "script": "",
            "props": ["title", "content", "footer"],
            "events": []
        }
        
        # Input component
        self.components["Input"] = {
            "template": '<input type="{{ type }}" class="form-control" id="{{ id }}" placeholder="{{ placeholder }}" value="{{ value }}">',
            "style": """
                .form-control {
                    padding: 8px 12px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 14px;
                    width: 100%;
                    box-sizing: border-box;
                }
                .form-control:focus {
                    outline: none;
                    border-color: #007bff;
                    box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
                }
            """,
            "script": """
                function handleInputChange(event) {
                    const input = event.target;
                    const componentId = input.id;
                    const value = input.value;
                    
                    if (window.emitComponentEvent) {
                        window.emitComponentEvent(componentId, 'change', {
                            value: value,
                            timestamp: new Date().toISOString()
                        });
                    }
                }
            """,
            "props": ["type", "placeholder", "value"],
            "events": ["change", "input", "focus", "blur"]
        }
        
        # Modal component
        self.components["Modal"] = {
            "template": """
                <div class="modal-overlay" id="{{ id }}-overlay">
                    <div class="modal" id="{{ id }}">
                        <div class="modal-header">
                            <h3>{{ title }}</h3>
                            <button class="modal-close" onclick="closeModal('{{ id }}')">&times;</button>
                        </div>
                        <div class="modal-body">{{ content }}</div>
                        <div class="modal-footer">{{ footer }}</div>
                    </div>
                </div>
            """,
            "style": """
                .modal-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0,0,0,0.5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 1000;
                }
                .modal {
                    background: white;
                    border-radius: 8px;
                    min-width: 300px;
                    max-width: 80%;
                    max-height: 80%;
                    overflow: auto;
                }
                .modal-header {
                    padding: 16px;
                    border-bottom: 1px solid #ddd;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .modal-body {
                    padding: 16px;
                }
                .modal-footer {
                    padding: 16px;
                    border-top: 1px solid #ddd;
                    text-align: right;
                }
                .modal-close {
                    background: none;
                    border: none;
                    font-size: 24px;
                    cursor: pointer;
                    padding: 0;
                    width: 30px;
                    height: 30px;
                }
            """,
            "script": """
                function closeModal(modalId) {
                    const overlay = document.getElementById(modalId + '-overlay');
                    if (overlay) {
                        overlay.style.display = 'none';
                    }
                }
                
                function openModal(modalId) {
                    const overlay = document.getElementById(modalId + '-overlay');
                    if (overlay) {
                        overlay.style.display = 'flex';
                    }
                }
            """,
            "props": ["title", "content", "footer"],
            "events": ["open", "close"]
        }
    
    def get_component(self, name: str) -> Optional[Dict[str, Any]]:
        """Get component definition"""
        return self.components.get(name)
    
    def list_components(self) -> List[str]:
        """List available components"""
        return list(self.components.keys())
    
    def register_component(self, name: str, definition: Dict[str, Any]):
        """Register a new component"""
        self.components[name] = definition
        logger.info(f"Registered UI component: {name}")
    
    def get_component_template(self, name: str) -> Optional[str]:
        """Get component template"""
        component = self.get_component(name)
        return component.get("template") if component else None
    
    def get_component_style(self, name: str) -> Optional[str]:
        """Get component style"""
        component = self.get_component(name)
        return component.get("style") if component else None
    
    def get_component_script(self, name: str) -> Optional[str]:
        """Get component script"""
        component = self.get_component(name)
        return component.get("script") if component else None


class UIThemeManager:
    """Manages UI themes and styling"""
    
    def __init__(self):
        self.themes: Dict[str, UITheme] = {}
        self.current_theme: str = "light"
        self._register_default_themes()
    
    def _register_default_themes(self):
        """Register default themes"""
        # Light theme
        light_theme = UITheme(
            name="light",
            colors={
                "primary": "#007bff",
                "secondary": "#6c757d",
                "success": "#28a745",
                "danger": "#dc3545",
                "warning": "#ffc107",
                "info": "#17a2b8",
                "light": "#f8f9fa",
                "dark": "#343a40",
                "white": "#ffffff",
                "black": "#000000"
            },
            fonts={
                "primary": "Arial, sans-serif",
                "secondary": "Georgia, serif",
                "monospace": "Courier New, monospace"
            },
            spacing={
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px"
            },
            shadows={
                "sm": "0 2px 4px rgba(0,0,0,0.1)",
                "md": "0 4px 8px rgba(0,0,0,0.15)",
                "lg": "0 8px 16px rgba(0,0,0,0.2)"
            },
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Dark theme
        dark_theme = UITheme(
            name="dark",
            colors={
                "primary": "#0d6efd",
                "secondary": "#6c757d",
                "success": "#198754",
                "danger": "#dc3545",
                "warning": "#ffc107",
                "info": "#0dcaf0",
                "light": "#212529",
                "dark": "#f8f9fa",
                "white": "#000000",
                "black": "#ffffff"
            },
            fonts={
                "primary": "Arial, sans-serif",
                "secondary": "Georgia, serif",
                "monospace": "Courier New, monospace"
            },
            spacing={
                "xs": "4px",
                "sm": "8px",
                "md": "16px",
                "lg": "24px",
                "xl": "32px"
            },
            shadows={
                "sm": "0 2px 4px rgba(255,255,255,0.1)",
                "md": "0 4px 8px rgba(255,255,255,0.15)",
                "lg": "0 8px 16px rgba(255,255,255,0.2)"
            },
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.themes["light"] = light_theme
        self.themes["dark"] = dark_theme
    
    def get_theme(self, name: str) -> Optional[UITheme]:
        """Get theme by name"""
        return self.themes.get(name)
    
    def set_current_theme(self, theme_name: str):
        """Set current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            logger.info(f"Switched to theme: {theme_name}")
        else:
            logger.warning(f"Theme not found: {theme_name}")
    
    def get_current_theme(self) -> UITheme:
        """Get current theme"""
        return self.themes[self.current_theme]
    
    def get_theme_css(self, theme_name: str) -> str:
        """Get CSS for a theme"""
        theme = self.get_theme(theme_name)
        if not theme:
            return ""
        
        css = f"/* Theme: {theme.name} */\n"
        css += ":root {\n"
        
        # Add CSS variables for colors
        for name, value in theme.colors.items():
            css += f"  --color-{name}: {value};\n"
        
        # Add CSS variables for spacing
        for name, value in theme.spacing.items():
            css += f"  --spacing-{name}: {value};\n"
        
        # Add CSS variables for shadows
        for name, value in theme.shadows.items():
            css += f"  --shadow-{name}: {value};\n"
        
        css += "}\n"
        return css


# ============================================================================
# UI UTILITY FUNCTIONS
# ============================================================================


def create_ui_component(
    component_type: str,
    props: Dict[str, Any],
    children: List[UIComponent] = None,
    events: List[UIEvent] = None
) -> UIComponent:
    """Create a new UI component with enhanced functionality"""
    return UIComponent(
        id=str(uuid.uuid4()),
        type=component_type,
        props=props,
        state={},
        children=children or [],
        event_handlers=events or [],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def validate_ui_props(props: Dict[str, Any], required_props: List[str]) -> bool:
    """Validate UI component properties"""
    for prop in required_props:
        if prop not in props:
            logger.warning(f"Required UI prop '{prop}' missing")
            return False
    return True


def sanitize_ui_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize UI data for security"""
    # Basic sanitization - remove potentially dangerous keys
    dangerous_keys = ["__class__", "__dict__", "__module__", "__bases__", "javascript:", "data:"]
    sanitized = {}
    
    for key, value in data.items():
        if key not in dangerous_keys:
            if isinstance(value, dict):
                sanitized[key] = sanitize_ui_data(value)
            elif isinstance(value, list):
                sanitized[key] = [sanitize_ui_data(item) if isinstance(item, dict) else item for item in value]
            elif isinstance(value, str):
                # Basic XSS protection
                if any(dangerous in value.lower() for dangerous in dangerous_keys):
                    sanitized[key] = value.replace("javascript:", "").replace("data:", "")
                else:
                    sanitized[key] = value
            else:
                sanitized[key] = value
    
    return sanitized


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Test the UI module
    print("Frontend UI Module")
    print("=" * 40)
    
    # Test component library
    library = UIComponentLibrary()
    print(f"Available components: {library.list_components()}")
    
    # Test theme manager
    theme_manager = UIThemeManager()
    print(f"Available themes: {list(theme_manager.themes.keys())}")
    
    # Test component creation
    component = create_ui_component("Button", {"text": "Click me", "variant": "primary"})
    print(f"Created UI component: {component.type} with props: {component.props}")
    
    # Test component rendering
    renderer = UIComponentRenderer()
    html = renderer.render_component(component)
    print(f"Rendered HTML: {html[:100]}...")
    
    print("UI module tests completed successfully!")
