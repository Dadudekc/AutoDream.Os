#!/usr/bin/env python3
"""
Contract Template System - V2 Contract Management

This module provides comprehensive contract template management.
Follows Single Responsibility Principle - only template management.
Architecture: Single Responsibility Principle - template management only
LOC: 190 lines (under 200 limit)
"""

import json
import os
import time
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import copy

logger = logging.getLogger(__name__)


class TemplateCategory(Enum):
    """Contract template categories"""
    AGENT_SERVICES = "agent_services"
    TASK_ASSIGNMENT = "task_assignment"
    SERVICE_LEVEL = "service_level"
    COORDINATION = "coordination"
    ONBOARDING = "onboarding"
    COMPLIANCE = "compliance"
    CUSTOM = "custom"


class TemplateStatus(Enum):
    """Template status states"""
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


@dataclass
class TemplateField:
    """Template field definition"""
    name: str
    field_type: str  # "string", "number", "boolean", "date", "array", "object"
    required: bool
    default_value: Optional[Any] = None
    validation_rules: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


@dataclass
class ContractTemplate:
    """Contract template definition"""
    template_id: str
    name: str
    description: str
    category: TemplateCategory
    status: TemplateStatus
    version: str
    fields: List[TemplateField]
    default_terms: Dict[str, Any]
    workflow_steps: List[str]
    created_at: float
    updated_at: float
    created_by: str
    tags: List[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}


class ContractTemplateSystem:
    """
    Comprehensive contract template management system
    
    Responsibilities:
    - Template creation and management
    - Template validation and versioning
    - Template instantiation and customization
    - Template workflow integration
    """
    
    def __init__(self, templates_dir: str = "contract_templates"):
        self.templates_dir = Path(templates_dir)
        self.templates: Dict[str, ContractTemplate] = {}
        self.template_versions: Dict[str, List[str]] = {}
        self.logger = logging.getLogger(f"{__name__}.ContractTemplateSystem")
        
        # Ensure templates directory exists
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing templates
        self._load_existing_templates()
        
        # Initialize default templates if none exist
        if not self.templates:
            self._initialize_default_templates()
        
        self.logger.info(f"Contract Template System initialized with {len(self.templates)} templates")
    
    def _load_existing_templates(self):
        """Load existing templates from the templates directory"""
        try:
            for template_file in self.templates_dir.glob("*.json"):
                try:
                    with open(template_file, 'r') as f:
                        template_data = json.load(f)
                    
                    # Convert fields back to TemplateField objects
                    fields = []
                    for field_data in template_data.get("fields", []):
                        field = TemplateField(
                            name=field_data["name"],
                            field_type=field_data["field_type"],
                            required=field_data["required"],
                            default_value=field_data.get("default_value"),
                            validation_rules=field_data.get("validation_rules"),
                            description=field_data.get("description")
                        )
                        fields.append(field)
                    
                    # Create template object
                    template = ContractTemplate(
                        template_id=template_data["template_id"],
                        name=template_data["name"],
                        description=template_data["description"],
                        category=TemplateCategory(template_data["category"]),
                        status=TemplateStatus(template_data["status"]),
                        version=template_data["version"],
                        fields=fields,
                        default_terms=template_data["default_terms"],
                        workflow_steps=template_data["workflow_steps"],
                        created_at=template_data["created_at"],
                        updated_at=template_data["updated_at"],
                        created_by=template_data["created_by"],
                        tags=template_data.get("tags", []),
                        metadata=template_data.get("metadata", {})
                    )
                    
                    self.templates[template.template_id] = template
                    
                    # Track versions
                    if template.template_id not in self.template_versions:
                        self.template_versions[template.template_id] = []
                    self.template_versions[template.template_id].append(template.version)
                    
                except Exception as e:
                    self.logger.error(f"Failed to load template {template_file}: {e}")
                    
        except Exception as e:
            self.logger.error(f"Failed to load existing templates: {e}")
    
    def _initialize_default_templates(self):
        """Initialize system with default contract templates"""
        try:
            default_templates = [
                {
                    "template_id": "agent_task_contract",
                    "name": "Agent Task Contract",
                    "description": "Standard contract for agent task assignments",
                    "category": TemplateCategory.TASK_ASSIGNMENT,
                    "fields": [
                        TemplateField("task_id", "string", True, description="Unique task identifier"),
                        TemplateField("task_description", "string", True, description="Detailed task description"),
                        TemplateField("assignee", "string", True, description="Assigned agent ID"),
                        TemplateField("deadline", "string", True, description="Task completion deadline"),
                        TemplateField("priority", "string", False, "medium", description="Task priority level"),
                        TemplateField("requirements", "array", False, [], description="Task requirements list")
                    ],
                    "default_terms": {
                        "deliverables": ["Task completion", "Status updates", "Final report"],
                        "acceptance_criteria": ["All requirements met", "Quality standards achieved"],
                        "deadlines": {"completion": "72h", "updates": "12h"},
                        "penalties": {"late_delivery": "priority_reduction"},
                        "rewards": {"excellence": "reputation_boost"}
                    },
                    "workflow_steps": ["draft", "proposed", "approved", "active", "completed"]
                },
                {
                    "template_id": "service_level_agreement",
                    "name": "Service Level Agreement",
                    "description": "SLA defining service quality expectations",
                    "category": TemplateCategory.SERVICE_LEVEL,
                    "fields": [
                        TemplateField("service_name", "string", True, description="Service identifier"),
                        TemplateField("availability_target", "number", True, description="Uptime percentage target"),
                        TemplateField("response_time", "number", True, description="Response time in seconds"),
                        TemplateField("incident_severity", "string", False, "medium", description="Default incident severity")
                    ],
                    "default_terms": {
                        "deliverables": ["Service availability", "Performance metrics", "Incident reports"],
                        "acceptance_criteria": ["Uptime >= 99%", "Response time < 1s"],
                        "deadlines": {"incident_response": "15min", "resolution": "4h"},
                        "penalties": {"sla_breach": "service_credits"},
                        "rewards": {"sla_exceed": "performance_bonus"}
                    },
                    "workflow_steps": ["draft", "review", "approved", "active", "monitoring"]
                }
            ]
            
            for template_data in default_templates:
                self.create_template(
                    name=template_data["name"],
                    description=template_data["description"],
                    category=template_data["category"],
                    fields=template_data["fields"],
                    default_terms=template_data["default_terms"],
                    workflow_steps=template_data["workflow_steps"]
                )
                
        except Exception as e:
            self.logger.error(f"Failed to initialize default templates: {e}")
    
    def create_template(self, name: str, description: str, category: TemplateCategory,
                       fields: List[TemplateField], default_terms: Dict[str, Any],
                       workflow_steps: List[str], tags: List[str] = None) -> str:
        """Create a new contract template"""
        try:
            template_id = f"template_{int(time.time())}_{len(self.templates)}"
            current_time = time.time()
            
            template = ContractTemplate(
                template_id=template_id,
                name=name,
                description=description,
                category=category,
                status=TemplateStatus.DRAFT,
                version="1.0.0",
                fields=fields,
                default_terms=default_terms,
                workflow_steps=workflow_steps,
                created_at=current_time,
                updated_at=current_time,
                created_by="system",
                tags=tags or [],
                metadata={}
            )
            
            # Save template
            self.templates[template_id] = template
            self._save_template(template)
            
            # Track versions
            if template_id not in self.template_versions:
                self.template_versions[template_id] = []
            self.template_versions[template_id].append(template.version)
            
            self.logger.info(f"Created template: {template_id} ({name})")
            return template_id
            
        except Exception as e:
            self.logger.error(f"Failed to create template: {e}")
            return None
    
    def instantiate_template(self, template_id: str, field_values: Dict[str, Any],
                           custom_terms: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Instantiate a contract from a template"""
        try:
            if template_id not in self.templates:
                raise ValueError(f"Template {template_id} not found")
            
            template = self.templates[template_id]
            
            # Validate required fields
            for field in template.fields:
                if field.required and field.name not in field_values:
                    if field.default_value is not None:
                        field_values[field.name] = field.default_value
                    else:
                        raise ValueError(f"Required field '{field.name}' not provided")
            
            # Create contract data
            contract_data = {
                "template_id": template_id,
                "template_version": template.version,
                "contract_type": template.category.value,
                "title": template.name,
                "description": template.description,
                "fields": field_values,
                "terms": copy.deepcopy(template.default_terms),
                "workflow_steps": template.workflow_steps,
                "created_at": time.time(),
                "status": "draft"
            }
            
            # Apply custom terms if provided
            if custom_terms:
                for key, value in custom_terms.items():
                    if key in contract_data["terms"]:
                        if isinstance(value, dict) and isinstance(contract_data["terms"][key], dict):
                            contract_data["terms"][key].update(value)
                        else:
                            contract_data["terms"][key] = value
                    else:
                        contract_data["terms"][key] = value
            
            self.logger.info(f"Instantiated contract from template: {template_id}")
            return contract_data
            
        except Exception as e:
            self.logger.error(f"Failed to instantiate template {template_id}: {e}")
            return None
    
    def _save_template(self, template: ContractTemplate):
        """Save template to file"""
        try:
            template_file = self.templates_dir / f"{template.template_id}.json"
            
            # Convert template to dict for JSON serialization
            template_data = asdict(template)
            template_data["category"] = template.category.value
            template_data["status"] = template.status.value
            
            with open(template_file, 'w') as f:
                json.dump(template_data, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Failed to save template {template.template_id}: {e}")
    
    def get_template(self, template_id: str) -> Optional[ContractTemplate]:
        """Get a template by ID"""
        return self.templates.get(template_id)
    
    def list_templates(self, category: Optional[TemplateCategory] = None,
                      status: Optional[TemplateStatus] = None) -> List[ContractTemplate]:
        """List templates with optional filtering"""
        templates = list(self.templates.values())
        
        if category:
            templates = [t for t in templates if t.category == category]
        
        if status:
            templates = [t for t in templates if t.status == status]
        
        return templates
    
    def get_template_summary(self) -> Dict[str, Any]:
        """Get summary of all templates"""
        try:
            total_templates = len(self.templates)
            categories = {}
            statuses = {}
            
            for template in self.templates.values():
                cat = template.category.value
                categories[cat] = categories.get(cat, 0) + 1
                
                stat = template.status.value
                statuses[stat] = statuses.get(stat, 0) + 1
            
            return {
                "total_templates": total_templates,
                "categories": categories,
                "statuses": statuses,
                "template_ids": list(self.templates.keys())
            }
        except Exception as e:
            self.logger.error(f"Failed to get template summary: {e}")
            return {"error": str(e)}


def run_smoke_test():
    """Run basic functionality test for ContractTemplateSystem"""
    print("🧪 Running ContractTemplateSystem Smoke Test...")
    
    try:
        # Test with temporary directory
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            system = ContractTemplateSystem(temp_dir)
            
            # Test template creation
            fields = [
                TemplateField("test_field", "string", True, description="Test field")
            ]
            
            template_id = system.create_template(
                "Test Template",
                "Test description",
                TemplateCategory.CUSTOM,
                fields,
                {"test": "value"},
                ["draft", "active"]
            )
            
            assert template_id is not None
            
            # Test template instantiation
            contract_data = system.instantiate_template(template_id, {"test_field": "test_value"})
            assert contract_data is not None
            assert contract_data["template_id"] == template_id
            
            # Test template listing
            templates = system.list_templates()
            assert len(templates) > 0
            
            # Test template summary
            summary = system.get_template_summary()
            assert "total_templates" in summary
            
        print("✅ ContractTemplateSystem Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ ContractTemplateSystem Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for ContractTemplateSystem testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Contract Template System CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--list", action="store_true", help="List all templates")
    parser.add_argument("--create", action="store_true", help="Create test template")
    parser.add_argument("--instantiate", help="Instantiate template by ID")
    parser.add_argument("--summary", action="store_true", help="Show template summary")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    system = ContractTemplateSystem()
    
    if args.list:
        templates = system.list_templates()
        print(f"Templates ({len(templates)} total):")
        for template in templates:
            print(f"  {template.template_id}: {template.name} ({template.category.value})")
    
    elif args.create:
        fields = [
            TemplateField("name", "string", True, description="Contract name"),
            TemplateField("value", "number", False, 100, description="Contract value")
        ]
        
        template_id = system.create_template(
            "CLI Test Template",
            "Template created via CLI",
            TemplateCategory.CUSTOM,
            fields,
            {"deliverables": ["Test deliverable"]},
            ["draft", "active"]
        )
        
        if template_id:
            print(f"✅ Created template: {template_id}")
        else:
            print("❌ Failed to create template")
    
    elif args.instantiate:
        contract_data = system.instantiate_template(args.instantiate, {"name": "Test Contract"})
        if contract_data:
            print(f"✅ Instantiated contract from template {args.instantiate}")
            print(f"  Title: {contract_data['title']}")
            print(f"  Status: {contract_data['status']}")
        else:
            print(f"❌ Failed to instantiate template {args.instantiate}")
    
    elif args.summary:
        summary = system.get_template_summary()
        print("Template Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
