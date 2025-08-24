"""
Message Formatter - Extracted from v2_comprehensive_messaging_system.py

This module handles message formatting including:
- Message serialization and deserialization
- Format conversion (JSON, XML, etc.)
- Message template formatting
- Output formatting for different channels

Original file: src/core/v2_comprehensive_messaging_system.py
Extraction date: 2024-12-19
"""

import json
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from dataclasses import asdict

# Configure logging
logger = logging.getLogger(__name__)

# Import enums and data structures from main file
from ..v2_comprehensive_messaging_system import (
    V2MessageType, V2MessagePriority, V2MessageStatus,
    V2Message, V2AgentInfo
)


class V2MessageFormatter:
    """Message formatting implementation - SRP: Format messages for different outputs"""
    
    def __init__(self):
        self.format_templates: Dict[V2MessageType, str] = {}
        self.output_formats: List[str] = ['json', 'xml', 'text', 'html']
        self._setup_default_templates()
        
    def _setup_default_templates(self):
        """Setup default formatting templates for different message types"""
        self.format_templates = {
            V2MessageType.TASK_ASSIGNMENT: "Task Assignment: {subject}\n\n{content}\n\nTask ID: {task_id}",
            V2MessageType.STATUS_UPDATE: "Status Update: {subject}\n\n{content}",
            V2MessageType.COORDINATION: "Coordination: {subject}\n\n{content}",
            V2MessageType.BROADCAST: "Broadcast: {subject}\n\n{content}",
            V2MessageType.SYSTEM: "System: {subject}\n\n{content}",
            V2MessageType.ALERT: "ALERT [{priority}]: {subject}\n\n{content}",
            V2MessageType.WORKFLOW_UPDATE: "Workflow Update: {subject}\n\n{content}\n\nWorkflow ID: {workflow_id}"
        }
    
    def format_message(self, message: V2Message, output_format: str = 'json') -> str:
        """Format message according to specified output format"""
        try:
            if output_format == 'json':
                return self._format_as_json(message)
            elif output_format == 'xml':
                return self._format_as_xml(message)
            elif output_format == 'text':
                return self._format_as_text(message)
            elif output_format == 'html':
                return self._format_as_html(message)
            else:
                logger.warning(f"Unsupported output format: {output_format}, defaulting to JSON")
                return self._format_as_json(message)
        except Exception as e:
            logger.error(f"Error formatting message: {e}")
            return f"Error formatting message: {str(e)}"
    
    def _format_as_json(self, message: V2Message) -> str:
        """Format message as JSON"""
        try:
            # Convert message to dictionary
            message_dict = asdict(message)
            
            # Handle datetime serialization
            for key, value in message_dict.items():
                if isinstance(value, datetime):
                    message_dict[key] = value.isoformat()
                elif hasattr(value, 'value'):  # Handle enums
                    message_dict[key] = value.value
            
            return json.dumps(message_dict, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error formatting as JSON: {e}")
            return json.dumps({"error": f"Failed to format message: {str(e)}"})
    
    def _format_as_xml(self, message: V2Message) -> str:
        """Format message as XML"""
        try:
            xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
            xml_parts.append('<message>')
            
            # Add basic message attributes
            xml_parts.append(f'  <message_id>{message.message_id}</message_id>')
            xml_parts.append(f'  <message_type>{message.message_type.value}</message_type>')
            xml_parts.append(f'  <priority>{message.priority.value}</priority>')
            xml_parts.append(f'  <status>{message.status.value}</status>')
            xml_parts.append(f'  <sender_id>{message.sender_id}</sender_id>')
            xml_parts.append(f'  <recipient_id>{message.recipient_id}</recipient_id>')
            xml_parts.append(f'  <subject>{self._escape_xml(message.subject)}</subject>')
            xml_parts.append(f'  <content>{self._escape_xml(message.content)}</content>')
            xml_parts.append(f'  <timestamp>{message.timestamp.isoformat()}</timestamp>')
            
            # Add optional fields if present
            if message.task_id:
                xml_parts.append(f'  <task_id>{message.task_id}</task_id>')
            if message.workflow_id:
                xml_parts.append(f'  <workflow_id>{message.workflow_id}</workflow_id>')
            if message.phase_number is not None:
                xml_parts.append(f'  <phase_number>{message.phase_number}</phase_number>')
            
            # Add payload if present
            if message.payload:
                xml_parts.append('  <payload>')
                for key, value in message.payload.items():
                    xml_parts.append(f'    <{key}>{self._escape_xml(str(value))}</{key}>')
                xml_parts.append('  </payload>')
            
            xml_parts.append('</message>')
            return '\n'.join(xml_parts)
            
        except Exception as e:
            logger.error(f"Error formatting as XML: {e}")
            return f"<error>Failed to format message: {str(e)}</error>"
    
    def _format_as_text(self, message: V2Message) -> str:
        """Format message as human-readable text"""
        try:
            # Get template for message type
            template = self.format_templates.get(message.message_type, "{subject}\n\n{content}")
            
            # Format using template
            formatted = template.format(
                subject=message.subject,
                content=message.content,
                task_id=message.task_id or "N/A",
                workflow_id=message.workflow_id or "N/A",
                priority=message.priority.value if message.priority else "N/A"
            )
            
            # Add metadata
            metadata = f"\n\n---\nFrom: {message.sender_id}"
            if message.recipient_id and message.recipient_id != "broadcast":
                metadata += f" | To: {message.recipient_id}"
            metadata += f" | Time: {message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            
            return formatted + metadata
            
        except Exception as e:
            logger.error(f"Error formatting as text: {e}")
            return f"Error formatting message: {str(e)}"
    
    def _format_as_html(self, message: V2Message) -> str:
        """Format message as HTML"""
        try:
            html_parts = ['<div class="message">']
            
            # Message header
            html_parts.append(f'<div class="message-header">')
            html_parts.append(f'  <span class="message-type">{message.message_type.value}</span>')
            html_parts.append(f'  <span class="priority priority-{message.priority.value.lower()}">{message.priority.value}</span>')
            html_parts.append('</div>')
            
            # Message subject
            html_parts.append(f'<h3 class="message-subject">{message.subject}</h3>')
            
            # Message content
            html_parts.append(f'<div class="message-content">{message.content}</div>')
            
            # Message metadata
            html_parts.append('<div class="message-metadata">')
            html_parts.append(f'  <span class="sender">From: {message.sender_id}</span>')
            if message.recipient_id and message.recipient_id != "broadcast":
                html_parts.append(f'  <span class="recipient">To: {message.recipient_id}</span>')
            html_parts.append(f'  <span class="timestamp">{message.timestamp.strftime("%Y-%m-%d %H:%M:%S")}</span>')
            html_parts.append('</div>')
            
            # Additional fields
            if message.task_id:
                html_parts.append(f'<div class="task-info">Task ID: {message.task_id}</div>')
            if message.workflow_id:
                html_parts.append(f'<div class="workflow-info">Workflow ID: {message.workflow_id}</div>')
            
            html_parts.append('</div>')
            return '\n'.join(html_parts)
            
        except Exception as e:
            logger.error(f"Error formatting as HTML: {e}")
            return f'<div class="error">Failed to format message: {str(e)}</div>'
    
    def _escape_xml(self, text: str) -> str:
        """Escape special characters for XML"""
        if not text:
            return ""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&apos;'))
    
    def add_format_template(self, message_type: V2MessageType, template: str) -> None:
        """Add custom formatting template for message type"""
        self.format_templates[message_type] = template
    
    def get_format_templates(self) -> Dict[V2MessageType, str]:
        """Get all format templates"""
        return self.format_templates.copy()
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported output formats"""
        return self.output_formats.copy()
    
    def get_formatting_stats(self) -> Dict[str, Any]:
        """Get formatting statistics for monitoring"""
        return {
            "format_templates_count": len(self.format_templates),
            "supported_formats": self.output_formats,
            "message_types_with_templates": list(self.format_templates.keys())
        }
