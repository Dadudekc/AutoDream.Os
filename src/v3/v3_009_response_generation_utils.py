"""
V3-009 Response Generation Utils
Utility functions for response generation
"""

import json
from datetime import datetime
from typing import Any

from .v3_009_response_generation_core import ResponseFormat, ResponseRequest, ResponseTemplate


class ResponseFormatter:
    """Utility class for formatting responses"""

    @staticmethod
    def format_as_text(content: str) -> str:
        """Format content as plain text"""
        return content.strip()

    @staticmethod
    def format_as_structured(content: str) -> str:
        """Format content as structured text"""
        lines = content.split("\n")
        formatted_lines = []

        for line in lines:
            if line.strip():
                formatted_lines.append(f"• {line.strip()}")

        return "\n".join(formatted_lines)

    @staticmethod
    def format_as_bullet_points(content: str) -> str:
        """Format content as bullet points"""
        lines = content.split("\n")
        bullet_points = []

        for line in lines:
            if line.strip():
                bullet_points.append(f"  - {line.strip()}")

        return "\n".join(bullet_points)

    @staticmethod
    def format_as_table(content: str) -> str:
        """Format content as table"""
        lines = content.split("\n")
        if len(lines) < 2:
            return content

        # Simple table formatting
        table_lines = []
        for i, line in enumerate(lines):
            if i == 0:
                table_lines.append(f"| {line.strip()} |")
                table_lines.append("|" + "-" * (len(line.strip()) + 2) + "|")
            else:
                table_lines.append(f"| {line.strip()} |")

        return "\n".join(table_lines)

    @staticmethod
    def format_as_json(content: str, metadata: dict[str, Any]) -> str:
        """Format content as JSON"""
        data = {"content": content, "timestamp": datetime.now().isoformat(), "metadata": metadata}
        return json.dumps(data, indent=2)


class ResponseValidator:
    """Utility class for validating responses"""

    @staticmethod
    def validate_template(template: ResponseTemplate) -> list[str]:
        """Validate template structure"""
        errors = []

        if not template.template_id:
            errors.append("Template ID is required")

        if not template.template:
            errors.append("Template content is required")

        if not template.variables:
            errors.append("Template variables are required")

        return errors

    @staticmethod
    def validate_request(request: ResponseRequest) -> list[str]:
        """Validate request structure"""
        errors = []

        if not request.context:
            errors.append("Context is required")

        if not request.context.agent_id:
            errors.append("Agent ID is required")

        if not request.context.target_agent:
            errors.append("Target agent is required")

        return errors


class ResponseAnalyzer:
    """Utility class for analyzing responses"""

    @staticmethod
    def analyze_complexity(content: str) -> dict[str, Any]:
        """Analyze response complexity"""
        words = content.split()
        sentences = content.split(".")

        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_words_per_sentence": len(words) / len(sentences) if sentences else 0,
            "complexity_score": min(len(words) / 10, 10),  # Simple complexity score
        }

    @staticmethod
    def extract_keywords(content: str) -> list[str]:
        """Extract keywords from content"""
        # Simple keyword extraction
        words = content.lower().split()
        common_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
        }

        keywords = []
        for word in words:
            clean_word = word.strip(".,!?;:")
            if clean_word and clean_word not in common_words and len(clean_word) > 3:
                keywords.append(clean_word)

        return list(set(keywords))


class ResponseCache:
    """Utility class for caching responses"""

    def __init__(self, max_size: int = 100):
        self.cache: dict[str, str] = {}
        self.max_size = max_size
        self.access_times: dict[str, datetime] = {}

    def get(self, key: str) -> str | None:
        """Get cached response"""
        if key in self.cache:
            self.access_times[key] = datetime.now()
            return self.cache[key]
        return None

    def set(self, key: str, value: str):
        """Set cached response"""
        if len(self.cache) >= self.max_size:
            self._evict_oldest()

        self.cache[key] = value
        self.access_times[key] = datetime.now()

    def _evict_oldest(self):
        """Evict oldest cached item"""
        if not self.access_times:
            return

        oldest_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
        del self.cache[oldest_key]
        del self.access_times[oldest_key]

    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.access_times.clear()


def create_response_request(
    agent_id: str,
    target_agent: str,
    message_type: str,
    priority: str = "normal",
    template_id: str | None = None,
    variables: dict[str, Any] | None = None,
) -> ResponseRequest:
    """Create a response request with default context"""
    from .v3_009_response_generation_core import ResponseContext

    context = ResponseContext(
        agent_id=agent_id,
        target_agent=target_agent,
        message_type=message_type,
        priority=priority,
        timestamp=datetime.now(),
        metadata={},
    )

    return ResponseRequest(context=context, template_id=template_id, variables=variables or {})


def format_response_content(content: str, format_type: ResponseFormat) -> str:
    """Format content according to format type"""
    formatter = ResponseFormatter()

    if format_type == ResponseFormat.TEXT:
        return formatter.format_as_text(content)
    elif format_type == ResponseFormat.STRUCTURED:
        return formatter.format_as_structured(content)
    elif format_type == ResponseFormat.BULLET_POINTS:
        return formatter.format_as_bullet_points(content)
    elif format_type == ResponseFormat.TABLE:
        return formatter.format_as_table(content)
    elif format_type == ResponseFormat.JSON:
        return formatter.format_as_json(content, {})
    else:
        return content
