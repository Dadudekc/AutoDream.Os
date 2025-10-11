"""
Jarvis AI Assistant Integration
================================

Integration of Jarvis AI assistant capabilities including memory management,
conversation handling, vision processing, and LLM integration.

Modules:
    - memory_system: Memory management and persistence
    - conversation_engine: Conversation flow management
    - ollama_integration: Ollama LLM integration (optional dependency)
    - vision_system: Vision and image processing (optional dependency)

Usage:
    from src.integrations.jarvis import memory_system
    from src.integrations.jarvis import conversation_engine

Optional Dependencies:
    - ollama: For LLM integration
    - PIL/opencv: For vision processing
"""

__all__ = [
    "memory_system",
    "conversation_engine",
    "ollama_integration",
    "vision_system",
]
