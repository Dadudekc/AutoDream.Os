"""
GPT Automation Engine - V2 Compliant
====================================

OpenAI API wrapper for GPT-driven automation workflows.
Provides retry logic, timeout handling, and V2 configuration integration.

V2 Compliance: ≤200 lines, comprehensive error handling, type hints.

Original: gpt-automation repository
Ported & Adapted: Agent-7 - Repository Cloning Specialist
License: MIT
"""

import logging
import time

# Optional OpenAI dependency
try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OpenAI = None
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI package not available - automation engine disabled")

# V2 Integration
try:
    from ..core.unified_config import get_unified_config
except ImportError:

    def get_unified_config():
        """Fallback config when V2 core unavailable."""
        import os

        return type(
            "MockConfig", (), {"get_env": lambda self, key, default=None: os.getenv(key, default)}
        )()


logger = logging.getLogger(__name__)


class AutomationEngine:
    """
    OpenAI Chat Completions API wrapper with retry and timeout.

    Capabilities:
    - GPT-3.5/GPT-4 prompt execution
    - Automatic retry with exponential backoff
    - Configurable timeout
    - V2 configuration integration
    """

    def __init__(
        self,
        client: object | None = None,
        model: str = "gpt-3.5-turbo",
        max_retries: int = 2,
        timeout_seconds: float = 15.0,
        backoff_seconds: float = 0.5,
    ) -> None:
        """
        Initialize automation engine.

        Args:
            client: Optional pre-configured OpenAI client
            model: Model name (gpt-3.5-turbo, gpt-4, etc.)
            max_retries: Maximum retry attempts
            timeout_seconds: API call timeout
            backoff_seconds: Base backoff time for retries
        """
        self.model = model
        self.max_retries = max(0, int(max_retries))
        self.timeout_seconds = float(timeout_seconds)
        self.backoff_seconds = float(backoff_seconds)

        # Use provided client or create new one
        if client is not None:
            self.client = client
            logger.info("AutomationEngine initialized with provided client")
            return

        # Check OpenAI availability
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "openai package is required when no client is provided. "
                "Install with: pip install openai"
            )

        # Get API key from V2 config
        config = get_unified_config()
        api_key = config.get_env("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. " "Set it in your environment or .env file."
            )

        # Create OpenAI client with timeout and retry support
        try:
            self.client = OpenAI(
                api_key=api_key, timeout=self.timeout_seconds, max_retries=self.max_retries
            )
        except TypeError:
            # Older OpenAI versions may not accept these kwargs
            self.client = OpenAI(api_key=api_key)
            logger.warning("Using older OpenAI client (timeout/retry not configurable)")

        logger.info(f"AutomationEngine initialized with model: {self.model}")

    def run_prompt(self, prompt: str) -> str:
        """
        Send a prompt to GPT and return the response with retry/timeout.

        Args:
            prompt: The prompt text to send to GPT

        Returns:
            The GPT response text (stripped)

        Raises:
            Exception: If all retry attempts fail
        """
        last_error: Exception | None = None
        attempts = self.max_retries + 1

        for attempt_index in range(attempts):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=self.timeout_seconds,
                )

                result = response.choices[0].message.content.strip()
                logger.info(f"Prompt executed successfully (attempt {attempt_index + 1})")
                return result

            except Exception as exc:
                last_error = exc
                logger.warning(f"Attempt {attempt_index + 1} failed: {exc}")

                # Break if this was the last attempt
                if attempt_index >= attempts - 1:
                    break

                # Exponential backoff before retry
                backoff_time = self.backoff_seconds * (2**attempt_index)
                logger.info(f"Retrying in {backoff_time}s...")
                time.sleep(backoff_time)

        # All retries exhausted
        logger.error(f"All {attempts} attempts failed")
        assert last_error is not None
        raise last_error

    def get_engine_info(self) -> dict:
        """
        Get information about engine configuration.

        Returns:
            Dictionary with engine settings
        """
        return {
            "model": self.model,
            "max_retries": self.max_retries,
            "timeout_seconds": self.timeout_seconds,
            "backoff_seconds": self.backoff_seconds,
            "openai_available": OPENAI_AVAILABLE,
            "has_client": self.client is not None,
        }
