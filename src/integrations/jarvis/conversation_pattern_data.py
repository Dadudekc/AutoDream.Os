"""
Conversation Pattern Data - V2 Compliant
=========================================

Pattern and response definitions for conversation engine.
Extracted from conversation_engine.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist
Date: 2025-10-11
"""

CONVERSATION_PATTERNS = {
    "greetings": {
        "patterns": [
            r"hello|hi|hey|greetings|good morning|good afternoon|good evening",
            r"how are you|how do you do|what\'s up",
            r"are you there|jarvis|wake up",
        ],
        "responses": [
            "Hello! I'm here and ready to help you.",
            "Hi there! How can I assist you today?",
            "Greetings! I'm listening and ready to work.",
        ],
    },
    "identity": {
        "patterns": [
            r"who are you|what are you|tell me about yourself",
            r"what can you do|what are your capabilities",
            r"are you ai|are you artificial intelligence",
        ],
        "responses": [
            "I'm Jarvis, your personal AI assistant for development and system control.",
            "I'm your AI assistant with vision, voice, and system control capabilities.",
        ],
    },
    "memory": {
        "patterns": [
            r"do you remember|can you remember|what do you know about me",
            r"what have we talked about|our previous conversations",
            r"do you know who i am|what\'s my name",
        ],
        "responses": [
            "Let me check my memory...",
            "I'll look through our conversation history...",
        ],
    },
    "learning": {
        "patterns": [
            r"learn|remember|save|store|memorize",
            r"my name is|i am|call me",
            r"i like|i prefer|my favorite",
        ],
        "responses": [
            "I'll remember that for you.",
            "Got it! I've stored that information.",
            "I've learned that about you.",
        ],
    },
    "gratitude": {
        "patterns": [
            r"thank you|thanks|appreciate it|good job",
            r"well done|excellent|perfect|great",
        ],
        "responses": [
            "You're welcome! I'm happy to help.",
            "My pleasure! Is there anything else you need?",
        ],
    },
    "farewell": {
        "patterns": [
            r"goodbye|bye|see you|later|exit|quit",
            r"stop|end|shut down|turn off",
        ],
        "responses": [
            "Goodbye! I'll be here when you need me.",
            "See you later! Don't hesitate to call if you need help.",
        ],
    },
    "confusion": {
        "patterns": [
            r"i don\'t understand|what do you mean|confused",
            r"that doesn\'t make sense|i\'m lost",
        ],
        "responses": [
            "I apologize for the confusion. Let me clarify...",
            "Let me explain differently...",
        ],
    },
    "help": {
        "patterns": [
            r"help|what can you do|show me|guide me",
            r"how do i|how can i|instructions",
        ],
        "responses": [
            "I can help you with many tasks. Here are some examples:",
            "Let me show you what I'm capable of:",
        ],
    },
}
