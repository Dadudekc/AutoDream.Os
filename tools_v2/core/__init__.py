"""
Tools V2 Core - Tool System Facade
===================================

Provides unified access to tool system components through facade pattern.
Re-exports from parent modules for backward compatibility.

Author: Agent-7 - Repository Cloning Specialist
Mission: Quarantine Fix Phase 4 (Utilities & Structure)
Date: 2025-10-16
Points: 150 pts
V2 Compliant: Facade pattern

Architecture:
- Facade for tools_v2 parent modules
- Maintains backward compatibility
- No duplicate logic
- Simple re-export + tool specs

Usage:
    from tools_v2.core import ToolFacade, ToolSpec
    
    facade = ToolFacade()
    spec = ToolSpec(name="tool", description="desc")
"""

# Re-export from parent modules
try:
    from ..toolbelt_core import *
except ImportError:
    pass

try:
    from ..tool_registry import *
except ImportError:
    pass


# Tool specification class for standardization
class ToolSpec:
    """
    Tool specification for standardized tool definition.
    
    Attributes:
        name: Tool name
        description: Tool description
        category: Tool category
        parameters: Tool parameters
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        category: str = "general",
        parameters: dict = None
    ):
        """
        Initialize tool specification.
        
        Args:
            name: Tool name
            description: Tool description
            category: Tool category
            parameters: Tool parameters dictionary
        """
        self.name = name
        self.description = description
        self.category = category
        self.parameters = parameters or {}
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "parameters": self.parameters
        }
    
    def __repr__(self) -> str:
        return f"ToolSpec(name='{self.name}', category='{self.category}')"


# Tool facade for unified access
class ToolFacade:
    """
    Tool facade for unified access to tool system.
    
    Provides simplified interface to complex tool system.
    """
    
    def __init__(self):
        """Initialize tool facade."""
        self.tools = {}
    
    def register_tool(self, spec: ToolSpec) -> None:
        """
        Register tool with facade.
        
        Args:
            spec: Tool specification
        """
        self.tools[spec.name] = spec
    
    def get_tool(self, name: str) -> ToolSpec:
        """
        Get tool by name.
        
        Args:
            name: Tool name
            
        Returns:
            Tool specification or None
        """
        return self.tools.get(name)
    
    def list_tools(self) -> list:
        """
        List all registered tools.
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys())
    
    def get_tools_by_category(self, category: str) -> list:
        """
        Get tools by category.
        
        Args:
            category: Tool category
            
        Returns:
            List of tool specifications
        """
        return [
            tool for tool in self.tools.values()
            if tool.category == category
        ]


__all__ = [
    'ToolSpec',
    'ToolFacade',
]

