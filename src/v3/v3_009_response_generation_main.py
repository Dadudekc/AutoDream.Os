"""
V3-009 Response Generation Main
Main response generation system with advanced features
"""

from datetime import datetime
from typing import Any

from .v3_009_response_generation_core import (
    GeneratedResponse,
    ResponseFormat,
    ResponseGeneratorCore,
    ResponseRequest,
    ResponseTemplate,
    ResponseTone,
)
from .v3_009_response_generation_utils import (
    ResponseAnalyzer,
    ResponseCache,
    ResponseFormatter,
    ResponseValidator,
    create_response_request,
    format_response_content,
)


class AdvancedResponseGenerator:
    """Advanced response generation with caching and analysis"""

    def __init__(self, cache_size: int = 100):
        self.core = ResponseGeneratorCore()
        self.cache = ResponseCache(cache_size)
        self.validator = ResponseValidator()
        self.analyzer = ResponseAnalyzer()
        self.formatter = ResponseFormatter()

    def generate_response(self, request: ResponseRequest) -> GeneratedResponse:
        """Generate response with caching and validation"""
        # Validate request
        errors = self.validator.validate_request(request)
        if errors:
            raise ValueError(f"Invalid request: {', '.join(errors)}")

        # Check cache first
        cache_key = self._generate_cache_key(request)
        cached_response = self.cache.get(cache_key)

        if cached_response:
            return self._create_cached_response(cached_response, request)

        # Generate new response
        response = self.core.generate_response(request)

        # Format content
        response.content = format_response_content(response.content, response.format)

        # Analyze response
        analysis = self.analyzer.analyze_complexity(response.content)
        response.metadata.update(analysis)

        # Cache response
        self.cache.set(cache_key, response.content)

        return response

    def generate_task_assignment_response(
        self, agent_id: str, target_agent: str, task_name: str, priority: str = "normal"
    ) -> GeneratedResponse:
        """Generate task assignment response"""
        request = create_response_request(
            agent_id=agent_id,
            target_agent=target_agent,
            message_type="task_assignment",
            priority=priority,
            template_id="task_assignment",
            variables={"task_name": task_name, "agent_id": target_agent},
        )

        return self.generate_response(request)

    def generate_status_update_response(
        self, agent_id: str, target_agent: str, status: str, details: str, priority: str = "normal"
    ) -> GeneratedResponse:
        """Generate status update response"""
        request = create_response_request(
            agent_id=agent_id,
            target_agent=target_agent,
            message_type="status_update",
            priority=priority,
            template_id="status_update",
            variables={"status": status, "details": details},
        )

        return self.generate_response(request)

    def generate_coordination_response(
        self, agent_id: str, target_agent: str, request_type: str, priority: str = "urgent"
    ) -> GeneratedResponse:
        """Generate coordination request response"""
        request = create_response_request(
            agent_id=agent_id,
            target_agent=target_agent,
            message_type="coordination_request",
            priority=priority,
            template_id="coordination_request",
            variables={"request_type": request_type},
        )

        return self.generate_response(request)

    def add_custom_template(
        self,
        template_id: str,
        category: str,
        template: str,
        variables: list[str],
        tone: ResponseTone = ResponseTone.PROFESSIONAL,
        format_type: ResponseFormat = ResponseFormat.TEXT,
    ):
        """Add custom template"""
        custom_template = ResponseTemplate(
            template_id=template_id,
            category=category,
            tone=tone,
            format=format_type,
            template=template,
            variables=variables,
        )

        errors = self.validator.validate_template(custom_template)
        if errors:
            raise ValueError(f"Invalid template: {', '.join(errors)}")

        self.core.add_template(custom_template)

    def get_response_statistics(self) -> dict[str, Any]:
        """Get response generation statistics"""
        return {
            "cache_size": len(self.cache.cache),
            "template_count": len(self.core.list_templates()),
            "cache_hit_rate": self._calculate_cache_hit_rate(),
            "generation_time": datetime.now().isoformat(),
        }

    def _generate_cache_key(self, request: ResponseRequest) -> str:
        """Generate cache key for request"""
        key_parts = [
            request.context.agent_id,
            request.context.target_agent,
            request.context.message_type,
            request.template_id or "custom",
            str(sorted(request.variables.items())) if request.variables else "",
        ]
        return "|".join(key_parts)

    def _create_cached_response(self, content: str, request: ResponseRequest) -> GeneratedResponse:
        """Create response from cached content"""
        return GeneratedResponse(
            content=content,
            template_id=request.template_id,
            tone=request.tone or ResponseTone.PROFESSIONAL,
            format=request.format or ResponseFormat.TEXT,
            variables_used=request.variables or {},
            generation_time=datetime.now(),
            metadata={"cached": True},
        )

    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate (simplified)"""
        # This is a simplified implementation
        return 0.75  # Placeholder value


class ResponseGenerationService:
    """Service class for response generation"""

    def __init__(self):
        self.generator = AdvancedResponseGenerator()

    def process_message_request(
        self,
        agent_id: str,
        target_agent: str,
        message_type: str,
        content: str | None = None,
        variables: dict[str, Any] | None = None,
        priority: str = "normal",
    ) -> GeneratedResponse:
        """Process message request and generate response"""
        if content:
            # Custom content request
            request = create_response_request(
                agent_id=agent_id,
                target_agent=target_agent,
                message_type=message_type,
                priority=priority,
                variables=variables or {},
            )
            request.custom_template = content
            return self.generator.generate_response(request)
        else:
            # Template-based request
            template_id = self._get_template_for_message_type(message_type)
            request = create_response_request(
                agent_id=agent_id,
                target_agent=target_agent,
                message_type=message_type,
                priority=priority,
                template_id=template_id,
                variables=variables or {},
            )
            return self.generator.generate_response(request)

    def _get_template_for_message_type(self, message_type: str) -> str:
        """Get template ID for message type"""
        template_mapping = {
            "task_assignment": "task_assignment",
            "status_update": "status_update",
            "coordination_request": "coordination_request",
        }
        return template_mapping.get(message_type, "status_update")


# Main entry point
def create_response_generation_service() -> ResponseGenerationService:
    """Create response generation service instance"""
    return ResponseGenerationService()


def generate_agent_response(
    agent_id: str, target_agent: str, message_type: str, **kwargs
) -> GeneratedResponse:
    """Generate agent response (convenience function)"""
    service = create_response_generation_service()
    return service.process_message_request(
        agent_id=agent_id, target_agent=target_agent, message_type=message_type, **kwargs
    )
