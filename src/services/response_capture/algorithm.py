"""Algorithmic helpers for response capture."""

from __future__ import annotations

from typing import Callable, Iterable

from .models import CapturedResponse

AI_INDICATORS = [
    "I'll help you",
    "Here's what I found",
    "Based on",
    "Let me",
    "I can",
    "I will",
    "Here's how",
    "The answer is",
]


def is_likely_ai_response(content: str) -> bool:
    """Return True if the content appears to be AI generated."""
    content_lower = content.lower()
    return any(indicator.lower() in content_lower for indicator in AI_INDICATORS)


def dispatch_response(
    response: CapturedResponse,
    handlers: Iterable[Callable[[CapturedResponse], None]],
) -> None:
    """Send the response to all registered handlers."""
    for handler in handlers:
        handler(response)


__all__ = ["is_likely_ai_response", "dispatch_response"]
