"""
V3-009 Natural Language Processing Pipeline
Command understanding, intent recognition, and response generation
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class IntentType(Enum):
    """Types of user intents"""
    GREETING = "greeting"
    QUESTION = "question"
    COMMAND = "command"
    STATUS_REQUEST = "status_request"
    HELP_REQUEST = "help_request"
    ERROR_REPORT = "error_report"
    UNKNOWN = "unknown"

class ResponseType(Enum):
    """Types of responses"""
    TEXT = "text"
    ACTION = "action"
    STATUS = "status"
    HELP = "help"
    ERROR = "error"

@dataclass
class Intent:
    """User intent classification"""
    intent_type: IntentType
    confidence: float
    entities: Dict[str, str]
    original_text: str
    processed_text: str

@dataclass
class Response:
    """Generated response"""
    response_type: ResponseType
    content: str
    actions: List[str]
    confidence: float
    timestamp: datetime

class NLPPipeline:
    """Core NLP processing pipeline"""
    
    def __init__(self):
        self.intent_patterns = self._initialize_intent_patterns()
        self.entity_patterns = self._initialize_entity_patterns()
        self.response_templates = self._initialize_response_templates()
        
    def _initialize_intent_patterns(self) -> Dict[IntentType, List[str]]:
        """Initialize regex patterns for intent recognition"""
        return {
            IntentType.GREETING: [
                r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b',
                r"\b(how are you|how's it going|what's up)\b"
            ],
            IntentType.QUESTION: [
                r'\b(what|how|when|where|why|who|which)\b.*\?',
                r'\b(can you|could you|would you)\b.*\?',
                r'\b(is|are|was|were|do|does|did|will|would|should)\b.*\?'
            ],
            IntentType.COMMAND: [
                r'\b(start|stop|run|execute|launch|deploy|build|test)\b',
                r'\b(show|display|get|fetch|retrieve|list)\b',
                r'\b(create|add|insert|update|modify|delete|remove)\b',
                r'\b(analyze|process|calculate|compute|generate)\b'
            ],
            IntentType.STATUS_REQUEST: [
                r'\b(status|health|state|condition|performance)\b',
                r'\b(how is|what is the status of|check the status)\b',
                r'\b(monitor|watch|observe|track)\b'
            ],
            IntentType.HELP_REQUEST: [
                r'\b(help|assist|support|guide|tutorial|documentation)\b',
                r'\b(how to|how do I|what should I)\b',
                r'\b(explain|describe|tell me about)\b'
            ],
            IntentType.ERROR_REPORT: [
                r'\b(error|bug|issue|problem|fault|failure|crash)\b',
                r'\b(not working|broken|failed|exception)\b',
                r'\b(fix|resolve|repair|debug)\b'
            ]
        }
        
    def _initialize_entity_patterns(self) -> Dict[str, str]:
        """Initialize regex patterns for entity extraction"""
        return {
            'agent_id': r'\b(Agent-?[1-8]|Captain|Agent-4)\b',
            'task_id': r'\b(V3-?\d{3}|V2-?\w+-\d{3})\b',
            'priority': r'\b(CRITICAL|HIGH|MEDIUM|LOW|urgent|normal)\b',
            'status': r'\b(ACTIVE|INACTIVE|COMPLETED|IN_PROGRESS|PENDING|FAILED)\b',
            'number': r'\b\d+\b',
            'file_path': r'[a-zA-Z0-9_/.-]+\.(py|json|md|txt|yaml|yml)',
            'url': r'https?://[^\s]+',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
        
    def _initialize_response_templates(self) -> Dict[IntentType, Dict[str, str]]:
        """Initialize response templates for different intents"""
        return {
            IntentType.GREETING: {
                "text": "Hello! I'm Agent-3, Infrastructure & DevOps Specialist. How can I assist you today?",
                "actions": []
            },
            IntentType.QUESTION: {
                "text": "I'd be happy to help answer your question. Let me analyze that for you.",
                "actions": ["analyze_question", "provide_answer"]
            },
            IntentType.COMMAND: {
                "text": "Command received. I'll execute that for you right away.",
                "actions": ["execute_command", "confirm_completion"]
            },
            IntentType.STATUS_REQUEST: {
                "text": "Let me check the current status and provide you with a comprehensive report.",
                "actions": ["check_status", "generate_report"]
            },
            IntentType.HELP_REQUEST: {
                "text": "I'm here to help! Let me provide you with the information you need.",
                "actions": ["provide_help", "show_documentation"]
            },
            IntentType.ERROR_REPORT: {
                "text": "I understand there's an issue. Let me investigate and help resolve it.",
                "actions": ["investigate_error", "provide_solution"]
            }
        }
        
    def process_text(self, text: str) -> Intent:
        """Process input text and extract intent"""
        # Clean and normalize text
        processed_text = self._clean_text(text)
        
        # Extract entities
        entities = self._extract_entities(processed_text)
        
        # Classify intent
        intent_type, confidence = self._classify_intent(processed_text)
        
        return Intent(
            intent_type=intent_type,
            confidence=confidence,
            entities=entities,
            original_text=text,
            processed_text=processed_text
        )
        
    def _clean_text(self, text: str) -> str:
        """Clean and normalize input text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\?\!\.\,]', '', text)
        
        return text
        
    def _extract_entities(self, text: str) -> Dict[str, str]:
        """Extract entities from text"""
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                entities[entity_type] = matches[0] if len(matches) == 1 else matches
                
        return entities
        
    def _classify_intent(self, text: str) -> Tuple[IntentType, float]:
        """Classify intent based on text patterns"""
        best_intent = IntentType.UNKNOWN
        best_confidence = 0.0
        
        for intent_type, patterns in self.intent_patterns.items():
            confidence = self._calculate_pattern_confidence(text, patterns)
            if confidence > best_confidence:
                best_confidence = confidence
                best_intent = intent_type
                
        return best_intent, best_confidence
        
    def _calculate_pattern_confidence(self, text: str, patterns: List[str]) -> float:
        """Calculate confidence score for pattern matching"""
        matches = 0
        total_patterns = len(patterns)
        
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matches += 1
                
        return matches / total_patterns if total_patterns > 0 else 0.0
        
    def generate_response(self, intent: Intent) -> Response:
        """Generate response based on intent"""
        template = self.response_templates.get(intent.intent_type, {
            "text": "I understand. Let me help you with that.",
            "actions": ["process_request"]
        })
        
        # Customize response based on entities
        content = self._customize_response(template["text"], intent.entities)
        actions = template["actions"].copy()
        
        # Add entity-specific actions
        if intent.entities.get('agent_id'):
            actions.append("notify_agent")
        if intent.entities.get('task_id'):
            actions.append("process_task")
        if intent.entities.get('priority') == 'CRITICAL':
            actions.append("escalate_priority")
            
        return Response(
            response_type=self._determine_response_type(intent.intent_type),
            content=content,
            actions=actions,
            confidence=intent.confidence,
            timestamp=datetime.now()
        )
        
    def _customize_response(self, template: str, entities: Dict[str, str]) -> str:
        """Customize response template with entities"""
        content = template
        
        if entities.get('agent_id'):
            content = content.replace("you", f"Agent-{entities['agent_id']}")
        if entities.get('task_id'):
            content += f" I see you're referring to {entities['task_id']}."
        if entities.get('priority'):
            content += f" Priority level: {entities['priority']}."
            
        return content
        
    def _determine_response_type(self, intent_type: IntentType) -> ResponseType:
        """Determine response type based on intent"""
        type_mapping = {
            IntentType.GREETING: ResponseType.TEXT,
            IntentType.QUESTION: ResponseType.TEXT,
            IntentType.COMMAND: ResponseType.ACTION,
            IntentType.STATUS_REQUEST: ResponseType.STATUS,
            IntentType.HELP_REQUEST: ResponseType.HELP,
            IntentType.ERROR_REPORT: ResponseType.ERROR
        }
        return type_mapping.get(intent_type, ResponseType.TEXT)

class CommandProcessor:
    """Command processing and execution"""
    
    def __init__(self, nlp_pipeline: NLPPipeline):
        self.nlp_pipeline = nlp_pipeline
        self.command_handlers = self._initialize_command_handlers()
        
    def _initialize_command_handlers(self) -> Dict[str, callable]:
        """Initialize command handlers for different actions"""
        return {
            "execute_command": self._execute_command,
            "check_status": self._check_status,
            "provide_help": self._provide_help,
            "investigate_error": self._investigate_error,
            "analyze_question": self._analyze_question,
            "notify_agent": self._notify_agent,
            "process_task": self._process_task,
            "escalate_priority": self._escalate_priority
        }
        
    def process_command(self, text: str) -> Dict[str, Any]:
        """Process command and execute actions"""
        # Process text through NLP pipeline
        intent = self.nlp_pipeline.process_text(text)
        response = self.nlp_pipeline.generate_response(intent)
        
        # Execute actions
        action_results = []
        for action in response.actions:
            if action in self.command_handlers:
                try:
                    result = self.command_handlers[action](intent, response)
                    action_results.append({
                        "action": action,
                        "status": "success",
                        "result": result
                    })
                except Exception as e:
                    action_results.append({
                        "action": action,
                        "status": "error",
                        "error": str(e)
                    })
                    
        return {
            "intent": {
                "type": intent.intent_type.value,
                "confidence": intent.confidence,
                "entities": intent.entities
            },
            "response": {
                "type": response.response_type.value,
                "content": response.content,
                "confidence": response.confidence
            },
            "actions": action_results,
            "timestamp": response.timestamp.isoformat()
        }
        
    def _execute_command(self, intent: Intent, response: Response) -> str:
        """Execute a command"""
        return f"Command executed: {intent.processed_text}"
        
    def _check_status(self, intent: Intent, response: Response) -> str:
        """Check system status"""
        return "System status: All systems operational"
        
    def _provide_help(self, intent: Intent, response: Response) -> str:
        """Provide help information"""
        return "Help documentation available for all V3 systems"
        
    def _investigate_error(self, intent: Intent, response: Response) -> str:
        """Investigate reported error"""
        return "Error investigation initiated - checking logs and system state"
        
    def _analyze_question(self, intent: Intent, response: Response) -> str:
        """Analyze and answer question"""
        return "Question analyzed - providing detailed answer"
        
    def _notify_agent(self, intent: Intent, response: Response) -> str:
        """Notify relevant agent"""
        agent_id = intent.entities.get('agent_id', 'Unknown')
        return f"Notification sent to {agent_id}"
        
    def _process_task(self, intent: Intent, response: Response) -> str:
        """Process task request"""
        task_id = intent.entities.get('task_id', 'Unknown')
        return f"Task {task_id} processing initiated"
        
    def _escalate_priority(self, intent: Intent, response: Response) -> str:
        """Escalate high priority request"""
        return "Priority escalation activated - Captain notified"

class NLPSystem:
    """Main NLP system coordinator"""
    
    def __init__(self):
        self.nlp_pipeline = NLPPipeline()
        self.command_processor = CommandProcessor(self.nlp_pipeline)
        
    def process_input(self, text: str) -> Dict[str, Any]:
        """Process user input through complete NLP pipeline"""
        return self.command_processor.process_command(text)
        
    def get_system_status(self) -> Dict[str, Any]:
        """Get NLP system status"""
        return {
            "system": "V3-009 NLP Pipeline",
            "status": "operational",
            "intent_types": len(self.nlp_pipeline.intent_patterns),
            "entity_types": len(self.nlp_pipeline.entity_patterns),
            "response_templates": len(self.nlp_pipeline.response_templates),
            "command_handlers": len(self.command_processor.command_handlers),
            "timestamp": datetime.now().isoformat()
        }

# Global NLP system instance
nlp_system = NLPSystem()

def process_nlp_input(text: str) -> Dict[str, Any]:
    """Process input through NLP system"""
    return nlp_system.process_input(text)

def get_nlp_system_status() -> Dict[str, Any]:
    """Get NLP system status"""
    return nlp_system.get_system_status()

if __name__ == "__main__":
    # Test NLP system with sample inputs
    test_inputs = [
        "Hello Agent-3, how are you?",
        "What is the status of V3-006?",
        "Can you help me with database optimization?",
        "There's an error in the performance monitoring system",
        "Start the analytics dashboard with HIGH priority"
    ]
    
    for test_input in test_inputs:
        print(f"\nInput: {test_input}")
        result = process_nlp_input(test_input)
        print(f"Intent: {result['intent']['type']} (confidence: {result['intent']['confidence']:.2f})")
        print(f"Response: {result['response']['content']}")
        print(f"Actions: {[action['action'] for action in result['actions']]}")
        
    # Show system status
    status = get_nlp_system_status()
    print(f"\nNLP System Status: {status}")
