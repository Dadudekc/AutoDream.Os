#!/usr/bin/env python3
"""
Aletheia Prompt Manager - Unified Interface
===========================================

Unified interface for Aletheia prompt management system.
Provides backward compatibility and easy access to all prompt management components.

V2 Compliance: ≤400 lines, unified interface module
Author: Agent-6 (Quality Assurance Specialist)
"""

import logging
from typing import Any

from .aletheia_prompt_models import PromptMetadata, PromptOptimization, PromptStatus, PromptType
from .aletheia_prompt_operations import (
    PromptAnalytics,
    PromptOptimizer,
    PromptSecurity,
    PromptVersionControl,
)
from .aletheia_prompt_storage import PromptStorage

logger = logging.getLogger(__name__)


class AletheiaPromptManager:
    """
    Unified Aletheia prompt management system.

    Integrates storage, optimization, version control, analytics, and security.
    """

    def __init__(self, storage_dir: str = "prompts"):
        """Initialize prompt manager."""
        self.storage = PromptStorage(storage_dir)
        self.optimizer = PromptOptimizer()
        self.version_control = PromptVersionControl()
        self.analytics = PromptAnalytics()
        self.security = PromptSecurity()
        self.logger = logging.getLogger(f"{__name__}.AletheiaPromptManager")

    def store_prompt(
        self,
        prompt_id: str,
        content: str,
        prompt_type: PromptType,
        metadata: PromptMetadata,
        status: PromptStatus = PromptStatus.DRAFT,
    ) -> bool:
        """Store a prompt with metadata."""
        try:
            # Store in storage system
            success = self.storage.store_prompt(prompt_id, content, prompt_type, metadata, status)

            if success:
                # Create initial version
                self.version_control.create_version(prompt_id, content, metadata, "Initial version")

                # Set default access
                self.security.set_access(prompt_id, "read")

                self.logger.info(f"Successfully stored prompt {prompt_id}")

            return success

        except Exception as e:
            self.logger.error(f"Error storing prompt {prompt_id}: {e}")
            return False

    def get_prompt(self, prompt_id: str, access_key: str = None) -> dict[str, Any] | None:
        """Get a prompt by ID with optional access control."""
        try:
            # Check access if key provided
            if access_key and not self.security.check_access(prompt_id, access_key):
                self.logger.warning(f"Access denied for prompt {prompt_id}")
                return None

            # Get prompt from storage
            prompt = self.storage.get_prompt(prompt_id)

            if prompt:
                # Track usage
                self.analytics.track_usage(prompt_id)

            return prompt

        except Exception as e:
            self.logger.error(f"Error getting prompt {prompt_id}: {e}")
            return None

    def optimize_prompt(self, prompt_id: str) -> PromptOptimization | None:
        """Optimize a prompt for better performance."""
        try:
            # Get current prompt
            prompt = self.storage.get_prompt(prompt_id)
            if not prompt:
                return None

            # Optimize the prompt
            optimization = self.optimizer.optimize_prompt(prompt_id, prompt["content"])

            # Record performance
            self.analytics.record_performance(prompt_id, optimization.performance_metrics)

            self.logger.info(f"Optimized prompt {prompt_id}")
            return optimization

        except Exception as e:
            self.logger.error(f"Error optimizing prompt {prompt_id}: {e}")
            return None

    def get_analytics(self, prompt_id: str) -> dict[str, Any]:
        """Get analytics for a prompt."""
        return self.analytics.get_analytics(prompt_id)

    def list_prompts(
        self, status: PromptStatus = None, prompt_type: PromptType = None
    ) -> list[dict[str, Any]]:
        """List prompts with optional filtering."""
        return self.storage.list_prompts(status, prompt_type)


def main():
    """Main function for testing."""
    # Example usage
    manager = AletheiaPromptManager()

    # Create sample metadata
    metadata = PromptMetadata(
        author="Agent-6",
        description="Test prompt for V2 compliance",
        tags=["test", "v2", "compliance"],
    )

    # Store a prompt
    success = manager.store_prompt(
        "test_prompt_001",
        "This is a test prompt for V2 compliance validation.",
        PromptType.SYSTEM,
        metadata,
        PromptStatus.ACTIVE,
    )

    if success:
        print("✅ Prompt stored successfully")

        # Get the prompt
        prompt = manager.get_prompt("test_prompt_001")
        if prompt:
            print(f"📝 Retrieved prompt: {prompt['content'][:50]}...")

        # Get analytics
        analytics = manager.get_analytics("test_prompt_001")
        print(f"📊 Analytics: {analytics}")
    else:
        print("❌ Failed to store prompt")


if __name__ == "__main__":
    main()


# Re-export all components for backward compatibility
__all__ = [
    "AletheiaPromptManager",
    "PromptStorage",
    "PromptOptimizer",
    "PromptVersionControl",
    "PromptAnalytics",
    "PromptSecurity",
    "PromptStatus",
    "PromptType",
    "PromptMetadata",
    "PromptOptimization",
]
