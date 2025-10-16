"""
Tool Specification
===================

Tool specification and metadata.
"""

from typing import List, Optional


class ToolSpec:
    """Tool specification."""
    
    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        category: str = "general",
        summary: str = "",
        required_params: Optional[List[str]] = None,
        optional_params: Optional[dict] = None,
    ):
        """Initialize tool spec."""
        self.name = name
        self.version = version
        self.category = category
        self.summary = summary
        self.required_params = required_params or []
        self.optional_params = optional_params or {}
    
    def validate_params(self, params: dict) -> tuple[bool, List[str]]:
        """
        Validate parameters.
        
        Returns:
            (is_valid, missing_params)
        """
        missing = [p for p in self.required_params if p not in params]
        return (len(missing) == 0, missing)

