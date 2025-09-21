"""
V3-009 Intent Recognition System
Advanced intent classification and recognition for agent communication
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class IntentCategory(Enum):
    """Intent categories"""
    TASK_MANAGEMENT = "task_management"
    SYSTEM_OPERATIONS = "system_operations"
    COMMUNICATION = "communication"
    EMERGENCY = "emergency"
    INFORMATION = "information"
    COORDINATION = "coordination"

class IntentConfidence(Enum):
    """Intent confidence levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"

@dataclass
class IntentResult:
    """Intent recognition result"""
    category: IntentCategory
    subcategory: str
    confidence: float
    confidence_level: IntentConfidence
    keywords: List[str]
    entities: Dict[str, Any]
    context_clues: List[str]
    original_text: str

class IntentClassifier:
    """Core intent classification engine"""
    
    def __init__(self):
        self.intent_patterns = self._initialize_intent_patterns()
        self.keyword_weights = self._initialize_keyword_weights()
        self.context_indicators = self._initialize_context_indicators()
        self.entity_patterns = self._initialize_entity_patterns()
        
    def _initialize_intent_patterns(self) -> Dict[IntentCategory, Dict[str, List[str]]]:
        """Initialize intent patterns by category and subcategory"""
        return {
            IntentCategory.TASK_MANAGEMENT: {
                "assign_task": [
                    r'\b(assign|give|delegate|hand over|distribute)\b.*\b(task|mission|job|work|assignment)\b',
                    r'\b(claim|take|accept|pick up|grab)\b.*\b(task|contract|assignment|work)\b',
                    r'\b(V3-?\d{3}|V2-?\w+-\d{3})\b.*\b(assign|claim|take|give)\b'
                ],
                "complete_task": [
                    r'\b(complete|finish|done|accomplish|achieve)\b.*\b(task|mission|job|work)\b',
                    r'\b(task|mission|job|work)\b.*\b(complete|finished|done|accomplished)\b',
                    r'\b(V3-?\d{3}|V2-?\w+-\d{3})\b.*\b(complete|finish|done)\b'
                ],
                "update_task": [
                    r'\b(update|modify|change|revise|edit)\b.*\b(task|mission|job|work|progress)\b',
                    r'\b(task|mission|job|work)\b.*\b(update|modify|change|revise)\b',
                    r'\b(progress|status|update|report)\b.*\b(task|mission|job|work)\b'
                ]
            },
            IntentCategory.SYSTEM_OPERATIONS: {
                "start_system": [
                    r'\b(start|begin|launch|initiate|activate)\b.*\b(system|service|process|component)\b',
                    r'\b(system|service|process|component)\b.*\b(start|begin|launch|initiate)\b',
                    r'\b(turn on|power on|boot up|bring up)\b'
                ],
                "stop_system": [
                    r'\b(stop|end|terminate|shutdown|deactivate)\b.*\b(system|service|process|component)\b',
                    r'\b(system|service|process|component)\b.*\b(stop|end|terminate|shutdown)\b',
                    r'\b(turn off|power off|shut down|bring down)\b'
                ],
                "monitor_system": [
                    r'\b(monitor|watch|observe|track|supervise)\b.*\b(system|service|process|component)\b',
                    r'\b(system|service|process|component)\b.*\b(monitor|watch|observe|track)\b',
                    r'\b(check|verify|inspect|examine)\b.*\b(system|service|process)\b'
                ]
            },
            IntentCategory.COMMUNICATION: {
                "send_message": [
                    r'\b(send|deliver|transmit|forward|relay)\b.*\b(message|communication|notification|alert)\b',
                    r'\b(message|communication|notification|alert)\b.*\b(send|deliver|transmit|forward)\b',
                    r'\b(notify|inform|tell|alert|warn)\b.*\b(agent|team|captain)\b'
                ],
                "request_information": [
                    r'\b(ask|request|inquire|query|question)\b.*\b(information|data|details|status|report)\b',
                    r'\b(information|data|details|status|report)\b.*\b(ask|request|inquire|query)\b',
                    r'\b(what|how|when|where|why|who|which)\b.*\b(about|regarding|concerning)\b'
                ],
                "provide_feedback": [
                    r'\b(feedback|response|reply|answer|comment)\b',
                    r'\b(agree|disagree|approve|reject|accept|decline)\b',
                    r'\b(good|bad|excellent|poor|great|terrible)\b.*\b(job|work|performance|result)\b'
                ]
            },
            IntentCategory.EMERGENCY: {
                "critical_alert": [
                    r'\b(emergency|urgent|critical|immediate|asap)\b',
                    r'\b(alert|warning|danger|problem|issue|fault|failure)\b',
                    r'\b(crash|down|offline|broken|malfunction)\b'
                ],
                "escalate_issue": [
                    r'\b(escalate|notify|warn|alert|contact)\b.*\b(captain|agent-4|supervisor|manager)\b',
                    r'\b(captain|agent-4|supervisor|manager)\b.*\b(escalate|notify|warn|alert)\b',
                    r'\b(priority|urgent|critical|immediate)\b.*\b(escalate|notify|warn)\b'
                ],
                "system_recovery": [
                    r'\b(recover|restore|fix|repair|resolve|solve)\b.*\b(system|service|process|component)\b',
                    r'\b(system|service|process|component)\b.*\b(recover|restore|fix|repair|resolve)\b',
                    r'\b(restart|reboot|reload|refresh|reset)\b'
                ]
            },
            IntentCategory.INFORMATION: {
                "status_inquiry": [
                    r'\b(status|health|state|condition|progress|performance)\b',
                    r'\b(how is|what is the status of|check the status)\b',
                    r'\b(report|update|summary|overview|dashboard)\b'
                ],
                "data_request": [
                    r'\b(data|information|details|facts|statistics|metrics)\b',
                    r'\b(show|display|get|fetch|retrieve|obtain)\b.*\b(data|information|details)\b',
                    r'\b(export|download|save|backup)\b.*\b(data|information|files)\b'
                ],
                "help_request": [
                    r'\b(help|assist|support|guide|tutorial|documentation)\b',
                    r'\b(how to|how do I|what should I|can you help)\b',
                    r'\b(explain|describe|tell me about|show me how)\b'
                ]
            },
            IntentCategory.COORDINATION: {
                "team_sync": [
                    r'\b(sync|synchronize|align|harmonize|coordinate)\b.*\b(team|group|agents|members)\b',
                    r'\b(team|group|agents|members)\b.*\b(sync|synchronize|align|harmonize)\b',
                    r'\b(meeting|discussion|conference|briefing|standup)\b'
                ],
                "collaboration": [
                    r'\b(collaborate|work together|team up|join forces|cooperate)\b',
                    r'\b(partnership|alliance|cooperation|joint effort)\b',
                    r'\b(share|exchange|contribute|participate)\b.*\b(work|project|task)\b'
                ],
                "resource_sharing": [
                    r'\b(share|distribute|allocate|assign|provide)\b.*\b(resource|tool|component|service)\b',
                    r'\b(resource|tool|component|service)\b.*\b(share|distribute|allocate|assign)\b',
                    r'\b(access|permission|authorization|grant|allow)\b'
                ]
            }
        }
        
    def _initialize_keyword_weights(self) -> Dict[str, float]:
        """Initialize keyword weights for intent scoring"""
        return {
            # High weight keywords
            "emergency": 10.0,
            "critical": 9.0,
            "urgent": 8.0,
            "immediate": 7.0,
            "asap": 7.0,
            "assign": 6.0,
            "task": 6.0,
            "complete": 5.0,
            "status": 5.0,
            "monitor": 5.0,
            "coordinate": 4.0,
            "help": 4.0,
            "information": 3.0,
            "message": 3.0,
            "system": 3.0,
            "agent": 2.0,
            "captain": 2.0,
            "v3": 2.0,
            "v2": 2.0
        }
        
    def _initialize_context_indicators(self) -> Dict[str, List[str]]:
        """Initialize context indicators for intent recognition"""
        return {
            "urgency": ["urgent", "critical", "emergency", "immediate", "asap", "priority"],
            "task_related": ["task", "mission", "job", "work", "assignment", "contract"],
            "system_related": ["system", "service", "process", "component", "infrastructure"],
            "communication": ["message", "communication", "notification", "alert", "report"],
            "coordination": ["coordinate", "collaborate", "team", "sync", "meeting", "discussion"],
            "information": ["information", "data", "details", "status", "report", "help"]
        }
        
    def _initialize_entity_patterns(self) -> Dict[str, str]:
        """Initialize entity extraction patterns"""
        return {
            'agent_id': r'\b(Agent-?[1-8]|Captain|Agent-4)\b',
            'task_id': r'\b(V3-?\d{3}|V2-?\w+-\d{3})\b',
            'priority': r'\b(CRITICAL|HIGH|MEDIUM|LOW|urgent|normal|low)\b',
            'status': r'\b(ACTIVE|INACTIVE|COMPLETED|IN_PROGRESS|PENDING|FAILED)\b',
            'timeframe': r'\b(\d+)\s*(cycle|cycles|hour|hours|day|days|minute|minutes)\b',
            'file_path': r'[a-zA-Z0-9_/.-]+\.(py|json|md|txt|yaml|yml)',
            'number': r'\b\d+\b',
            'percentage': r'\b\d+(\.\d+)?%\b',
            'url': r'https?://[^\s]+',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
        
    def recognize_intent(self, text: str) -> IntentResult:
        """Recognize intent from text"""
        # Clean and normalize text
        cleaned_text = self._clean_text(text)
        
        # Extract keywords and entities
        keywords = self._extract_keywords(cleaned_text)
        entities = self._extract_entities(cleaned_text)
        context_clues = self._extract_context_clues(cleaned_text)
        
        # Classify intent
        category, subcategory, confidence = self._classify_intent(cleaned_text, keywords)
        
        # Determine confidence level
        confidence_level = self._determine_confidence_level(confidence)
        
        return IntentResult(
            category=category,
            subcategory=subcategory,
            confidence=confidence,
            confidence_level=confidence_level,
            keywords=keywords,
            entities=entities,
            context_clues=context_clues,
            original_text=text
        )
        
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\?\!\.\,]', '', text)
        
        return text
        
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        keywords = []
        for keyword in self.keyword_weights.keys():
            if keyword in text:
                keywords.append(keyword)
        return keywords
        
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text"""
        entities = {}
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                if len(matches) == 1:
                    entities[entity_type] = matches[0]
                else:
                    entities[entity_type] = matches
        return entities
        
    def _extract_context_clues(self, text: str) -> List[str]:
        """Extract context clues from text"""
        clues = []
        for context_type, indicators in self.context_indicators.items():
            for indicator in indicators:
                if indicator in text:
                    clues.append(f"{context_type}:{indicator}")
        return clues
        
    def _classify_intent(self, text: str, keywords: List[str]) -> Tuple[IntentCategory, str, float]:
        """Classify intent based on text and keywords"""
        best_category = IntentCategory.INFORMATION
        best_subcategory = "general_inquiry"
        best_confidence = 0.0
        
        for category, subcategories in self.intent_patterns.items():
            for subcategory, patterns in subcategories.items():
                confidence = self._calculate_intent_confidence(text, patterns, keywords)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_category = category
                    best_subcategory = subcategory
                    
        return best_category, best_subcategory, best_confidence
        
    def _calculate_intent_confidence(self, text: str, patterns: List[str], keywords: List[str]) -> float:
        """Calculate confidence score for intent classification"""
        # Pattern matching score
        pattern_score = 0.0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                pattern_score += 1.0
        pattern_score = pattern_score / len(patterns) if patterns else 0.0
        
        # Keyword weight score
        keyword_score = 0.0
        for keyword in keywords:
            weight = self.keyword_weights.get(keyword, 1.0)
            keyword_score += weight
        keyword_score = keyword_score / 10.0  # Normalize to 0-1 range
        
        # Combined confidence
        confidence = (pattern_score * 0.7) + (keyword_score * 0.3)
        return min(1.0, confidence)
        
    def _determine_confidence_level(self, confidence: float) -> IntentConfidence:
        """Determine confidence level from confidence score"""
        if confidence >= 0.8:
            return IntentConfidence.HIGH
        elif confidence >= 0.6:
            return IntentConfidence.MEDIUM
        elif confidence >= 0.4:
            return IntentConfidence.LOW
        else:
            return IntentConfidence.VERY_LOW

class IntentRecognitionSystem:
    """Main intent recognition system"""
    
    def __init__(self):
        self.classifier = IntentClassifier()
        self.recognition_history: List[IntentResult] = []
        
    def process_intent(self, text: str) -> IntentResult:
        """Process text for intent recognition"""
        result = self.classifier.recognize_intent(text)
        self.recognition_history.append(result)
        return result
        
    def get_intent_statistics(self) -> Dict[str, Any]:
        """Get intent recognition statistics"""
        if not self.recognition_history:
            return {"total_intents": 0}
            
        category_counts = {}
        confidence_levels = {}
        
        for result in self.recognition_history:
            category = result.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
            
            confidence_level = result.confidence_level.value
            confidence_levels[confidence_level] = confidence_levels.get(confidence_level, 0) + 1
            
        return {
            "total_intents": len(self.recognition_history),
            "category_distribution": category_counts,
            "confidence_distribution": confidence_levels,
            "average_confidence": sum(r.confidence for r in self.recognition_history) / len(self.recognition_history)
        }
        
    def get_system_status(self) -> Dict[str, Any]:
        """Get intent recognition system status"""
        return {
            "system": "V3-009 Intent Recognition",
            "status": "operational",
            "categories": len(self.classifier.intent_patterns),
            "total_patterns": sum(len(patterns) for patterns in self.classifier.intent_patterns.values()),
            "keyword_weights": len(self.classifier.keyword_weights),
            "entity_patterns": len(self.classifier.entity_patterns),
            "recognition_history_count": len(self.recognition_history),
            "timestamp": datetime.now().isoformat()
        }

# Global intent recognition system instance
intent_system = IntentRecognitionSystem()

def recognize_intent(text: str) -> IntentResult:
    """Recognize intent from text"""
    return intent_system.process_intent(text)

def get_intent_statistics() -> Dict[str, Any]:
    """Get intent recognition statistics"""
    return intent_system.get_intent_statistics()

def get_intent_system_status() -> Dict[str, Any]:
    """Get intent recognition system status"""
    return intent_system.get_system_status()

if __name__ == "__main__":
    # Test intent recognition system
    test_texts = [
        "Agent-3, please assign V3-006 to me with HIGH priority",
        "What is the current status of the performance monitoring system?",
        "Emergency: Critical error in database system - need immediate attention",
        "Can you help me coordinate with Agent-1 on the API integration?",
        "I need information about the V3 pipeline progress",
        "Please start the analytics dashboard service"
    ]
    
    for text in test_texts:
        print(f"\nText: {text}")
        result = recognize_intent(text)
        print(f"Category: {result.category.value}")
        print(f"Subcategory: {result.subcategory}")
        print(f"Confidence: {result.confidence:.2f} ({result.confidence_level.value})")
        print(f"Keywords: {result.keywords}")
        print(f"Entities: {result.entities}")
        print(f"Context Clues: {result.context_clues}")
        
    # Show statistics
    stats = get_intent_statistics()
    print(f"\nIntent Statistics: {stats}")
    
    # Show system status
    status = get_intent_system_status()
    print(f"\nIntent System Status: {status}")


