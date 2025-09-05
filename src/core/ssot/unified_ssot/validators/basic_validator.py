"""
Basic SSOT Validator
====================

Handles basic field validation for SSOT components.
Extracted from validator.py for improved modularity.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from typing import List, Dict, Any
from datetime import datetime

from ..models import SSOTComponent, SSOTValidationLevel


class BasicValidator:
    """Handles basic SSOT component validation."""
    
    def __init__(self):
        """Initialize basic validator."""
        self.validation_rules = {
            'required_fields': ['component_id', 'component_type', 'component_name'],
            'field_length_limits': {
                'component_name': 100,
                'description': 500,
                'version': 20
            }
        }
    
    def validate_basic_fields(self, component: SSOTComponent) -> List[str]:
        """Validate basic component fields."""
        issues = []
        
        try:
            # Check required fields
            for field in self.validation_rules['required_fields']:
                if not hasattr(component, field) or getattr(component, field) is None:
                    issues.append(f"Missing required field: {field}")
                elif isinstance(getattr(component, field), str) and not getattr(component, field).strip():
                    issues.append(f"Empty required field: {field}")
            
            # Check field length limits
            for field, limit in self.validation_rules['field_length_limits'].items():
                if hasattr(component, field):
                    value = getattr(component, field)
                    if isinstance(value, str) and len(value) > limit:
                        issues.append(f"Field '{field}' exceeds length limit ({len(value)} > {limit})")
            
            # Check component_id format
            if hasattr(component, 'component_id') and component.component_id:
                if not isinstance(component.component_id, str):
                    issues.append("component_id must be a string")
                elif len(component.component_id) < 3:
                    issues.append("component_id must be at least 3 characters")
                elif not component.component_id.replace('_', '').replace('-', '').isalnum():
                    issues.append("component_id contains invalid characters")
            
            # Check timestamps if present
            timestamp_fields = ['created_at', 'updated_at', 'last_validated']
            for field in timestamp_fields:
                if hasattr(component, field):
                    value = getattr(component, field)
                    if value is not None and not isinstance(value, datetime):
                        issues.append(f"Field '{field}' must be a datetime object")
            
        except Exception as e:
            issues.append(f"Basic validation error: {str(e)}")
        
        return issues
    
    def validate_component_metadata(self, component: SSOTComponent) -> List[str]:
        """Validate component metadata fields."""
        issues = []
        
        try:
            # Check version format if present
            if hasattr(component, 'version') and component.version:
                version = component.version
                if not isinstance(version, str):
                    issues.append("version must be a string")
                elif not any(char.isdigit() for char in version):
                    issues.append("version must contain at least one digit")
            
            # Check tags if present
            if hasattr(component, 'tags') and component.tags:
                if not isinstance(component.tags, list):
                    issues.append("tags must be a list")
                else:
                    for i, tag in enumerate(component.tags):
                        if not isinstance(tag, str):
                            issues.append(f"Tag at index {i} must be a string")
                        elif not tag.strip():
                            issues.append(f"Tag at index {i} cannot be empty")
            
            # Check dependencies if present
            if hasattr(component, 'dependencies') and component.dependencies:
                if not isinstance(component.dependencies, list):
                    issues.append("dependencies must be a list")
                else:
                    for i, dep in enumerate(component.dependencies):
                        if not isinstance(dep, str):
                            issues.append(f"Dependency at index {i} must be a string")
                        elif not dep.strip():
                            issues.append(f"Dependency at index {i} cannot be empty")
            
        except Exception as e:
            issues.append(f"Metadata validation error: {str(e)}")
        
        return issues
    
    def get_validation_score(self, issues: List[str]) -> float:
        """Calculate validation score based on issues."""
        try:
            base_score = 100.0
            # Deduct 10 points per basic issue
            score = base_score - (len(issues) * 10)
            return max(0.0, score)  # Ensure score doesn't go below 0
        except Exception:
            return 0.0
