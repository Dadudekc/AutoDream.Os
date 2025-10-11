"""Browser Configuration - Extracted from unified_config.py | Agent-5 C-056"""

from dataclasses import dataclass, field

from .config_core import get_config


@dataclass
class BrowserConfig:
    """Centralized browser interaction configuration."""

    # URLs
    gpt_url: str = get_config(
        "GPT_URL", "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
    )
    conversation_url: str = get_config(
        "CONVERSATION_URL", "https://chatgpt.com/c/68bf1b1b-37b8-8324-be55-e3ccf20af737"
    )

    # Primary selectors
    input_selector: str = get_config("INPUT_SELECTOR", "textarea[data-testid='prompt-textarea']")
    send_button_selector: str = get_config(
        "SEND_BUTTON_SELECTOR", "button[data-testid='send-button']"
    )
    response_selector: str = get_config(
        "RESPONSE_SELECTOR", "[data-testid='conversation-turn']:last-child .markdown"
    )
    thinking_indicator: str = get_config("THINKING_INDICATOR", "[data-testid='thinking-indicator']")

    # Fallback selectors
    input_fallback_selectors: list[str] = field(
        default_factory=lambda: [
            "textarea#prompt-textarea",
            "textarea[placeholder*='Message']",
            "div[contenteditable='true']",
        ]
    )
    send_fallback_selectors: list[str] = field(
        default_factory=lambda: [
            "button[aria-label='Send']",
            "button:has(svg[data-testid='send-button-icon'])",
            "button.absolute.bottom-0",
        ]
    )
    response_fallback_selectors: list[str] = field(
        default_factory=lambda: [
            ".markdown.prose",
            "[data-message-author-role='assistant']",
            ".agent-turn",
        ]
    )
    max_scrape_retries: int = get_config("MAX_SCRAPE_RETRIES", 3)
