"""
V3-009 Response Generation System
Intelligent response generation for agent communication
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

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
    variables: List[str]
    conditions: List[str] = None
    
    def __post_init__(self):
        if self.conditions is None:
            self.conditions = []

@dataclass
class GeneratedResponse:
    """Generated response structure"""
    content: str
    tone: ResponseTone
    format: ResponseFormat
    confidence: float
    variables_used: Dict[str, str]
    template_id: str
    timestamp: datetime

class ResponseGenerator:
    """Core response generation engine"""
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.tone_modifiers = self._initialize_tone_modifiers()
        self.format_handlers = self._initialize_format_handlers()
        
    def _initialize_templates(self) -> Dict[str, List[ResponseTemplate]]:
        """Initialize response templates by category"""
        return {
            "task_assignment": [
                ResponseTemplate(
                    template_id="task_assign_confirm",
                    category="task_assignment",
                    tone=ResponseTone.PROFESSIONAL,
                    format=ResponseFormat.STRUCTURED,
                    template="✅ TASK ASSIGNMENT CONFIRMED\n\n**Task**: {task_id}\n**Assigned to**: {agent_id}\n**Priority**: {priority}\n**Status**: {status}\n**Estimated Duration**: {duration}\n\nI'll begin implementation immediately.",
                    variables=["task_id", "agent_id", "priority", "status", "duration"],
                    conditions=["task_id", "agent_id"]
                ),
                ResponseTemplate(
                    template_id="task_assign_urgent",
                    category="task_assignment",
                    tone=ResponseTone.URGENT,
                    format=ResponseFormat.TEXT,
                    template="🚨 URGENT TASK ASSIGNMENT: {task_id} - {agent_id} - {priority} PRIORITY - Starting immediately!",
                    variables=["task_id", "agent_id", "priority"],
                    conditions=["priority=CRITICAL", "priority=HIGH"]
                )
            ],
            "status_update": [
                ResponseTemplate(
                    template_id="status_complete",
                    category="status_update",
                    tone=ResponseTone.PROFESSIONAL,
                    format=ResponseFormat.STRUCTURED,
                    template="📊 STATUS UPDATE\n\n**Mission**: {mission}\n**Current Task**: {current_task}\n**Status**: {status}\n**Progress**: {progress}%\n**Next Actions**: {next_actions}\n\n**Achievements**:\n{achievements}",
                    variables=["mission", "current_task", "status", "progress", "next_actions", "achievements"],
                    conditions=["status"]
                ),
                ResponseTemplate(
                    template_id="status_operational",
                    category="status_update",
                    tone=ResponseTone.FRIENDLY,
                    format=ResponseFormat.TEXT,
                    template="✅ All systems operational! {mission} in progress - {current_task} - {status}",
                    variables=["mission", "current_task", "status"],
                    conditions=["status=ACTIVE", "status=OPERATIONAL"]
                )
            ],
            "coordination": [
                ResponseTemplate(
                    template_id="coordination_ready",
                    category="coordination",
                    tone=ResponseTone.PROFESSIONAL,
                    format=ResponseFormat.STRUCTURED,
                    template="🤝 COORDINATION READY\n\n**From**: {sender}\n**To**: {recipient}\n**Purpose**: {purpose}\n**Status**: Ready to collaborate\n**Next Steps**: {next_steps}\n\nLet's work together effectively!",
                    variables=["sender", "recipient", "purpose", "next_steps"],
                    conditions=["sender", "recipient"]
                ),
                ResponseTemplate(
                    template_id="coordination_swarm",
                    category="coordination",
                    tone=ResponseTone.FRIENDLY,
                    format=ResponseFormat.TEXT,
                    template="🐝 WE. ARE. SWARM. - {sender} ready to coordinate with {recipient} on {purpose}!",
                    variables=["sender", "recipient", "purpose"],
                    conditions=["sender", "recipient"]
                )
            ],
            "emergency": [
                ResponseTemplate(
                    template_id="emergency_alert",
                    category="emergency",
                    tone=ResponseTone.URGENT,
                    format=ResponseFormat.STRUCTURED,
                    template="🚨 EMERGENCY ALERT\n\n**Type**: {alert_type}\n**Severity**: {severity}\n**Description**: {description}\n**Actions Taken**: {actions}\n**Status**: {status}\n\nEscalating to Captain immediately!",
                    variables=["alert_type", "severity", "description", "actions", "status"],
                    conditions=["alert_type", "severity"]
                ),
                ResponseTemplate(
                    template_id="emergency_resolved",
                    category="emergency",
                    tone=ResponseTone.PROFESSIONAL,
                    format=ResponseFormat.TEXT,
                    template="✅ EMERGENCY RESOLVED: {description} - {actions} - System restored to normal operation",
                    variables=["description", "actions"],
                    conditions=["description"]
                )
            ],
            "information": [
                ResponseTemplate(
                    template_id="info_provided",
                    category="information",
                    tone=ResponseTone.TECHNICAL,
                    format=ResponseFormat.STRUCTURED,
                    template="📋 INFORMATION PROVIDED\n\n**Query**: {query}\n**Answer**: {answer}\n**Details**: {details}\n**References**: {references}\n**Confidence**: {confidence}%",
                    variables=["query", "answer", "details", "references", "confidence"],
                    conditions=["query", "answer"]
                ),
                ResponseTemplate(
                    template_id="info_help",
                    category="information",
                    tone=ResponseTone.FRIENDLY,
                    format=ResponseFormat.BULLET_POINTS,
                    template="💡 HELP PROVIDED\n\n• **Question**: {question}\n• **Answer**: {answer}\n• **Steps**: {steps}\n• **Resources**: {resources}",
                    variables=["question", "answer", "steps", "resources"],
                    conditions=["question", "answer"]
                )
            ],
            "error_handling": [
                ResponseTemplate(
                    template_id="error_acknowledged",
                    category="error_handling",
                    tone=ResponseTone.PROFESSIONAL,
                    format=ResponseFormat.STRUCTURED,
                    template="⚠️ ERROR ACKNOWLEDGED\n\n**Error Type**: {error_type}\n**Description**: {description}\n**Impact**: {impact}\n**Resolution**: {resolution}\n**Status**: {status}\n\nWorking on resolution...",
                    variables=["error_type", "description", "impact", "resolution", "status"],
                    conditions=["error_type", "description"]
                ),
                ResponseTemplate(
                    template_id="error_resolved",
                    category="error_handling",
                    tone=ResponseTone.PROFESSIONAL,
                    format=ResponseFormat.TEXT,
                    template="✅ ERROR RESOLVED: {error_type} - {resolution} - System back to normal",
                    variables=["error_type", "resolution"],
                    conditions=["error_type", "resolution"]
                )
            ]
        }
        
    def _initialize_tone_modifiers(self) -> Dict[ResponseTone, Dict[str, str]]:
        """Initialize tone modifiers for response customization"""
        return {
            ResponseTone.PROFESSIONAL: {
                "greeting": "Hello",
                "closing": "Best regards",
                "emphasis": "**",
                "urgency": "Please note",
                "confirmation": "Confirmed"
            },
            ResponseTone.FRIENDLY: {
                "greeting": "Hi there",
                "closing": "Cheers",
                "emphasis": "*",
                "urgency": "Heads up",
                "confirmation": "Got it"
            },
            ResponseTone.URGENT: {
                "greeting": "URGENT",
                "closing": "Immediate action required",
                "emphasis": "**",
                "urgency": "CRITICAL",
                "confirmation": "ACKNOWLEDGED"
            },
            ResponseTone.TECHNICAL: {
                "greeting": "Technical update",
                "closing": "End of technical report",
                "emphasis": "`",
                "urgency": "Priority",
                "confirmation": "Verified"
            },
            ResponseTone.CASUAL: {
                "greeting": "Hey",
                "closing": "Later",
                "emphasis": "*",
                "urgency": "FYI",
                "confirmation": "Sure thing"
            }
        }
        
    def _initialize_format_handlers(self) -> Dict[ResponseFormat, callable]:
        """Initialize format handlers for different response formats"""
        return {
            ResponseFormat.TEXT: self._format_text,
            ResponseFormat.STRUCTURED: self._format_structured,
            ResponseFormat.BULLET_POINTS: self._format_bullet_points,
            ResponseFormat.TABLE: self._format_table,
            ResponseFormat.JSON: self._format_json
        }
        
    def generate_response(self, category: str, context: Dict[str, Any], 
                         tone: ResponseTone = ResponseTone.PROFESSIONAL,
                         format_type: ResponseFormat = ResponseFormat.STRUCTURED) -> GeneratedResponse:
        """Generate response based on category and context"""
        # Select appropriate template
        template = self._select_template(category, context, tone, format_type)
        
        if not template:
            # Fallback to default template
            template = self._get_default_template(category, tone, format_type)
            
        # Fill template with context variables
        content = self._fill_template(template, context)
        
        # Apply tone modifications
        content = self._apply_tone_modifications(content, tone)
        
        # Format response
        formatted_content = self._format_response(content, format_type)
        
        return GeneratedResponse(
            content=formatted_content,
            tone=tone,
            format=format_type,
            confidence=self._calculate_confidence(template, context),
            variables_used=self._extract_used_variables(template, context),
            template_id=template.template_id,
            timestamp=datetime.now()
        )
        
    def _select_template(self, category: str, context: Dict[str, Any], 
                        tone: ResponseTone, format_type: ResponseFormat) -> Optional[ResponseTemplate]:
        """Select appropriate template based on category and context"""
        templates = self.templates.get(category, [])
        
        # Filter by tone and format
        matching_templates = [
            t for t in templates 
            if t.tone == tone and t.format == format_type
        ]
        
        if not matching_templates:
            # Fallback to any template in category
            matching_templates = templates
            
        if not matching_templates:
            return None
            
        # Check conditions
        for template in matching_templates:
            if self._check_template_conditions(template, context):
                return template
                
        # Return first matching template if no conditions met
        return matching_templates[0] if matching_templates else None
        
    def _check_template_conditions(self, template: ResponseTemplate, context: Dict[str, Any]) -> bool:
        """Check if template conditions are met"""
        if not template.conditions:
            return True
            
        for condition in template.conditions:
            if '=' in condition:
                key, value = condition.split('=', 1)
                if context.get(key) != value:
                    return False
            else:
                if key not in context:
                    return False
                    
        return True
        
    def _get_default_template(self, category: str, tone: ResponseTone, 
                            format_type: ResponseFormat) -> ResponseTemplate:
        """Get default template for category"""
        return ResponseTemplate(
            template_id=f"default_{category}",
            category=category,
            tone=tone,
            format=format_type,
            template="Response for {category}: {message}",
            variables=["category", "message"]
        )
        
    def _fill_template(self, template: ResponseTemplate, context: Dict[str, Any]) -> str:
        """Fill template with context variables"""
        content = template.template
        
        for variable in template.variables:
            value = context.get(variable, f"{{{variable}}}")
            content = content.replace(f"{{{variable}}}", str(value))
            
        return content
        
    def _apply_tone_modifications(self, content: str, tone: ResponseTone) -> str:
        """Apply tone modifications to content"""
        modifiers = self.tone_modifiers.get(tone, {})
        
        # Apply greeting and closing if not present
        if not content.startswith(('Hello', 'Hi', 'URGENT', 'Technical')):
            content = f"{modifiers.get('greeting', 'Hello')}\n\n{content}"
            
        if not content.endswith(('regards', 'Cheers', 'required', 'report', 'Later')):
            content = f"{content}\n\n{modifiers.get('closing', 'Best regards')}"
            
        return content
        
    def _format_response(self, content: str, format_type: ResponseFormat) -> str:
        """Format response according to format type"""
        handler = self.format_handlers.get(format_type, self._format_text)
        return handler(content)
        
    def _format_text(self, content: str) -> str:
        """Format as plain text"""
        return content
        
    def _format_structured(self, content: str) -> str:
        """Format as structured text"""
        return content
        
    def _format_bullet_points(self, content: str) -> str:
        """Format as bullet points"""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip().startswith('•'):
                formatted_lines.append(line)
            elif line.strip():
                formatted_lines.append(f"• {line.strip()}")
            else:
                formatted_lines.append(line)
                
        return '\n'.join(formatted_lines)
        
    def _format_table(self, content: str) -> str:
        """Format as table"""
        # Simple table formatting - in real implementation would be more sophisticated
        return content
        
    def _format_json(self, content: str) -> str:
        """Format as JSON"""
        try:
            # Try to parse as JSON first
            data = json.loads(content)
            return json.dumps(data, indent=2)
        except:
            # Fallback to structured text
            return content
            
    def _calculate_confidence(self, template: ResponseTemplate, context: Dict[str, Any]) -> float:
        """Calculate confidence score for generated response"""
        # Base confidence from template match
        base_confidence = 0.8
        
        # Increase confidence for each variable that's provided
        provided_variables = sum(1 for var in template.variables if var in context)
        variable_confidence = provided_variables / len(template.variables) if template.variables else 0.0
        
        # Increase confidence for condition matches
        condition_confidence = 1.0 if self._check_template_conditions(template, context) else 0.5
        
        # Combined confidence
        confidence = (base_confidence * 0.4) + (variable_confidence * 0.3) + (condition_confidence * 0.3)
        return min(1.0, confidence)
        
    def _extract_used_variables(self, template: ResponseTemplate, context: Dict[str, Any]) -> Dict[str, str]:
        """Extract variables that were used in template"""
        used_variables = {}
        for variable in template.variables:
            if variable in context:
                used_variables[variable] = str(context[variable])
        return used_variables

class ResponseGenerationSystem:
    """Main response generation system"""
    
    def __init__(self):
        self.generator = ResponseGenerator()
        self.generation_history: List[GeneratedResponse] = []
        
    def generate_response(self, category: str, context: Dict[str, Any], 
                         tone: ResponseTone = ResponseTone.PROFESSIONAL,
                         format_type: ResponseFormat = ResponseFormat.STRUCTURED) -> GeneratedResponse:
        """Generate response through complete system"""
        response = self.generator.generate_response(category, context, tone, format_type)
        self.generation_history.append(response)
        return response
        
    def get_generation_statistics(self) -> Dict[str, Any]:
        """Get response generation statistics"""
        if not self.generation_history:
            return {"total_responses": 0}
            
        tone_counts = {}
        format_counts = {}
        category_counts = {}
        
        for response in self.generation_history:
            tone = response.tone.value
            tone_counts[tone] = tone_counts.get(tone, 0) + 1
            
            format_type = response.format.value
            format_counts[format_type] = format_counts.get(format_type, 0) + 1
            
        return {
            "total_responses": len(self.generation_history),
            "tone_distribution": tone_counts,
            "format_distribution": format_counts,
            "average_confidence": sum(r.confidence for r in self.generation_history) / len(self.generation_history)
        }
        
    def get_system_status(self) -> Dict[str, Any]:
        """Get response generation system status"""
        return {
            "system": "V3-009 Response Generation",
            "status": "operational",
            "template_categories": len(self.generator.templates),
            "total_templates": sum(len(templates) for templates in self.generator.templates.values()),
            "tone_types": len(self.generator.tone_modifiers),
            "format_types": len(self.generator.format_handlers),
            "generation_history_count": len(self.generation_history),
            "timestamp": datetime.now().isoformat()
        }

# Global response generation system instance
response_system = ResponseGenerationSystem()

def generate_response(category: str, context: Dict[str, Any], 
                     tone: ResponseTone = ResponseTone.PROFESSIONAL,
                     format_type: ResponseFormat = ResponseFormat.STRUCTURED) -> GeneratedResponse:
    """Generate response through system"""
    return response_system.generate_response(category, context, tone, format_type)

def get_response_statistics() -> Dict[str, Any]:
    """Get response generation statistics"""
    return response_system.get_generation_statistics()

def get_response_system_status() -> Dict[str, Any]:
    """Get response generation system status"""
    return response_system.get_system_status()

if __name__ == "__main__":
    # Test response generation system
    test_contexts = [
        {
            "category": "task_assignment",
            "context": {
                "task_id": "V3-009",
                "agent_id": "Agent-3",
                "priority": "HIGH",
                "status": "IN_PROGRESS",
                "duration": "1 cycle"
            },
            "tone": ResponseTone.PROFESSIONAL
        },
        {
            "category": "status_update",
            "context": {
                "mission": "V3 Infrastructure Deployment",
                "current_task": "V3-009 NLP Pipeline",
                "status": "COMPLETED",
                "progress": 100,
                "next_actions": "Ready for next assignment",
                "achievements": "NLP system implemented successfully"
            },
            "tone": ResponseTone.FRIENDLY
        },
        {
            "category": "emergency",
            "context": {
                "alert_type": "System Error",
                "severity": "CRITICAL",
                "description": "Database connection failed",
                "actions": "Restarting database service",
                "status": "RESOLVING"
            },
            "tone": ResponseTone.URGENT
        }
    ]
    
    for test in test_contexts:
        print(f"\nCategory: {test['category']}")
        response = generate_response(
            test['category'], 
            test['context'], 
            test['tone']
        )
        print(f"Response: {response.content}")
        print(f"Confidence: {response.confidence:.2f}")
        print(f"Variables Used: {response.variables_used}")
        
    # Show statistics
    stats = get_response_statistics()
    print(f"\nResponse Statistics: {stats}")
    
    # Show system status
    status = get_response_system_status()
    print(f"\nResponse System Status: {status}")


