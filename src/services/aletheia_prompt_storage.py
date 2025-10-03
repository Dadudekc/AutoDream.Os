#!/usr/bin/env python3
"""
Aletheia Prompt Storage - Storage Operations
=============================================

Storage operations for Aletheia prompt management system.
Handles prompt storage, retrieval, and management.

V2 Compliance: ≤400 lines, focused storage operations module
Author: Agent-6 (Quality Assurance Specialist)
"""

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

from .aletheia_prompt_models import PromptMetadata, PromptStatus, PromptType

logger = logging.getLogger(__name__)


class PromptStorage:
    """
    Storage operations for prompt management.

    Handles prompt storage, retrieval, and management.
    """

    def __init__(self, storage_dir: str = "prompts"):
        """Initialize prompt storage."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.prompts: dict[str, dict[str, Any]] = {}
        self._load_prompts()

    def _load_prompts(self) -> None:
        """Load prompts from storage."""
        try:
            prompts_file = self.storage_dir / "prompts.json"
            if prompts_file.exists():
                with open(prompts_file) as f:
                    self.prompts = json.load(f)
            logger.info(f"Loaded {len(self.prompts)} prompts from storage")
        except Exception as e:
            logger.error(f"Error loading prompts: {e}")
            self.prompts = {}

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
            # Generate content hash for deduplication
            content_hash = hashlib.sha256(content.encode()).hexdigest()

            prompt_data = {
                "id": prompt_id,
                "content": content,
                "type": prompt_type.value,
                "status": status.value,
                "metadata": {
                    "created_at": metadata.created_at.isoformat(),
                    "updated_at": metadata.updated_at.isoformat(),
                    "version": metadata.version,
                    "author": metadata.author,
                    "tags": metadata.tags,
                    "description": metadata.description,
                    "usage_count": metadata.usage_count,
                    "performance_score": metadata.performance_score,
                },
                "content_hash": content_hash,
                "stored_at": datetime.now(UTC).isoformat(),
            }

            self.prompts[prompt_id] = prompt_data

            # Save to file
            self._save_prompts()

            logger.info(f"Stored prompt {prompt_id} with hash {content_hash[:8]}")
            return True

        except Exception as e:
            logger.error(f"Error storing prompt {prompt_id}: {e}")
            return False

    def get_prompt(self, prompt_id: str) -> dict[str, Any] | None:
        """Get a prompt by ID."""
        return self.prompts.get(prompt_id)

    def list_prompts(
        self, status: PromptStatus = None, prompt_type: PromptType = None
    ) -> list[dict[str, Any]]:
        """List prompts with optional filtering."""
        filtered_prompts = []

        for prompt in self.prompts.values():
            # Filter by status
            if status and prompt.get("status") != status.value:
                continue

            # Filter by type
            if prompt_type and prompt.get("type") != prompt_type.value:
                continue

            filtered_prompts.append(prompt)

        return filtered_prompts

    def update_prompt_metadata(self, prompt_id: str, metadata: PromptMetadata) -> bool:
        """Update prompt metadata."""
        try:
            if prompt_id not in self.prompts:
                return False

            self.prompts[prompt_id]["metadata"] = {
                "created_at": metadata.created_at.isoformat(),
                "updated_at": metadata.updated_at.isoformat(),
                "version": metadata.version,
                "author": metadata.author,
                "tags": metadata.tags,
                "description": metadata.description,
                "usage_count": metadata.usage_count,
                "performance_score": metadata.performance_score,
            }

            self._save_prompts()
            return True

        except Exception as e:
            logger.error(f"Error updating prompt metadata {prompt_id}: {e}")
            return False

    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt."""
        try:
            if prompt_id in self.prompts:
                del self.prompts[prompt_id]
                self._save_prompts()
                logger.info(f"Deleted prompt {prompt_id}")
                return True
            return False

        except Exception as e:
            logger.error(f"Error deleting prompt {prompt_id}: {e}")
            return False

    def _save_prompts(self) -> None:
        """Save prompts to storage."""
        try:
            prompts_file = self.storage_dir / "prompts.json"
            with open(prompts_file, "w") as f:
                json.dump(self.prompts, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving prompts: {e}")


__all__ = ["PromptStorage"]
