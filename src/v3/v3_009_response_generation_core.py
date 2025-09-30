"""
V3-009 Response Generation Core
Core classes and data structures for response generation
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class ResponseTone(Enum):
    """Response tone types"""

    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    URGENT = "urgent"
    TECHNICAL = "technical"
    CASUAL = "casual"


class ResponseFormat(Enum):
    """Response format types"""

    TEXT = "text"
    STRUCTURED = "structured"
    BULLET_POINTS = "bullet_points"
    TABLE = "table"
    JSON = "json"


@dataclass
class ResponseTemplate:
    """Response template structure"""

    template_id: str
    category: str
    tone: ResponseTone
    format: ResponseFormat
    template: str
    variables: list[str]
    conditions: list[str] | None = None

    def __post_init__(self):
        if self.conditions is None:
            self.conditions = []


@dataclass
class ResponseContext:
    """Context for response generation"""

    agent_id: str
    target_agent: str
    message_type: str
    priority: str
    timestamp: datetime
    metadata: dict[str, Any]


@dataclass
class ResponseRequest:
    """Request for response generation"""

    context: ResponseContext
    template_id: str | None = None
    custom_template: str | None = None
    variables: dict[str, Any] | None = None
    tone: ResponseTone | None = None
    format: ResponseFormat | None = None

    def __post_init__(self):
        if self.variables is None:
            self.variables = {}


@dataclass
class GeneratedResponse:
    """Generated response structure"""

    content: str
    template_id: str | None
    tone: ResponseTone
    format: ResponseFormat
    variables_used: dict[str, Any]
    generation_time: datetime
    metadata: dict[str, Any]

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ResponseGeneratorCore:
    """Core response generation logic"""

    def __init__(self):
        self.templates: dict[str, ResponseTemplate] = {}
        self._initialize_default_templates()

    def _initialize_default_templates(self):
        """Initialize default response templates"""
        default_templates = [
            ResponseTemplate(
                template_id="task_assignment",
                category="task",
                tone=ResponseTone.PROFESSIONAL,
                format=ResponseFormat.STRUCTURED,
                template="Task {task_name} assigned to {agent_id}",
                variables=["task_name", "agent_id"],
            ),
            ResponseTemplate(
                template_id="status_update",
                category="status",
                tone=ResponseTone.PROFESSIONAL,
                format=ResponseFormat.TEXT,
                template="Status: {status} - {details}",
                variables=["status", "details"],
            ),
            ResponseTemplate(
                template_id="coordination_request",
                category="coordination",
                tone=ResponseTone.URGENT,
                format=ResponseFormat.STRUCTURED,
                template="Coordination needed: {request_type}",
                variables=["request_type"],
            ),
        ]

        for template in default_templates:
            self.templates[template.template_id] = template

    def generate_response(self, request: ResponseRequest) -> GeneratedResponse:
        """Generate response based on request"""
        template = self._get_template(request)
        content = self._process_template(template, request)

        return GeneratedResponse(
            content=content,
            template_id=template.template_id if template else None,
            tone=request.tone or template.tone,
            format=request.format or template.format,
            variables_used=request.variables or {},
            generation_time=datetime.now(),
            metadata={"generated_by": "ResponseGeneratorCore"},
        )

    def _get_template(self, request: ResponseRequest) -> ResponseTemplate:
        """Get template for request"""
        if request.template_id and request.template_id in self.templates:
            return self.templates[request.template_id]

        # Return default template if none specified
        return self.templates["status_update"]

    def _process_template(self, template: ResponseTemplate, request: ResponseRequest) -> str:
        """Process template with variables"""
        content = template.template

        if request.variables:
            for key, value in request.variables.items():
                placeholder = f"{{{key}}}"
                content = content.replace(placeholder, str(value))

        return content

    def add_template(self, template: ResponseTemplate):
        """Add new template"""
        self.templates[template.template_id] = template

    def get_template(self, template_id: str) -> ResponseTemplate | None:
        """Get template by ID"""
        return self.templates.get(template_id)

    def list_templates(self) -> list[str]:
        """List all template IDs"""
        return list(self.templates.keys())
