"""
AletheiaPromptManager - Native Dream.OS prompt management system
V2 Compliant: ≤400 lines, ≤3 enums, ≤5 classes, ≤10 functions
"""

import hashlib
import time
from dataclasses import dataclass
from enum import Enum


class PromptType(Enum):
    """Simple prompt type enum"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class OptimizationLevel(Enum):
    """Simple optimization level enum"""

    BASIC = 1
    STANDARD = 2
    ADVANCED = 3


@dataclass
class PromptConfig:
    """Simple configuration with defaults"""

    max_length: int = 1000
    optimization_level: OptimizationLevel = OptimizationLevel.STANDARD
    cache_size: int = 100
    cache_ttl: int = 3600


class AletheiaPromptManager:
    """Native Dream.OS prompt management system"""

    def __init__(self, config: PromptConfig):
        self.config = config
        self.prompt_cache: dict[str, dict] = {}
        self.generation_time = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_requests = 0
        self._cache_access_times: dict[str, float] = {}

    def generate_prompt(
        self, context: str, intent: str, prompt_type: PromptType = PromptType.USER
    ) -> str:
        """Generate optimized prompt for Dream.OS"""
        start_time = time.time()
        cache_key = self._create_cache_key(context, intent, prompt_type)

        # Check cache first
        cached_prompt = self._get_from_cache(cache_key)
        if cached_prompt:
            self.cache_hits += 1
            return cached_prompt

        self.cache_misses += 1

        # Generate new prompt
        prompt = self._build_prompt(context, intent, prompt_type)

        # Optimize prompt if needed
        if self.config.optimization_level != OptimizationLevel.BASIC:
            prompt = self._optimize_prompt(prompt)

        # Cache the prompt
        self._cache_prompt(cache_key, prompt)

        # Record performance
        self.generation_time = (time.time() - start_time) * 1000
        self.total_requests += 1

        return prompt

    def get_cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total_cache_requests = self.cache_hits + self.cache_misses
        if total_cache_requests == 0:
            return 0.0
        return (self.cache_hits / total_cache_requests) * 100

    def clear_cache(self) -> None:
        """Clear prompt cache"""
        self.prompt_cache.clear()
        self._cache_access_times.clear()

    def _create_cache_key(self, context: str, intent: str, prompt_type: PromptType) -> str:
        """Create cache key from inputs"""
        content = f"{context}:{intent}:{prompt_type.value}"
        return hashlib.md5(content.encode()).hexdigest()

    def _build_prompt(self, context: str, intent: str, prompt_type: PromptType) -> str:
        """Build basic prompt structure"""
        if prompt_type == PromptType.SYSTEM:
            return f"System: {context}\nIntent: {intent}"
        elif prompt_type == PromptType.USER:
            return f"User: {context}\nRequest: {intent}"
        else:
            return f"Assistant: {context}\nResponse: {intent}"

    def _optimize_prompt(self, prompt: str) -> str:
        """Optimize prompt for performance"""
        optimized = prompt.strip()
        optimized = " ".join(optimized.split())
        if len(optimized) > self.config.max_length:
            optimized = optimized[: self.config.max_length - 3] + "..."
        return optimized

    def _cache_prompt(self, key: str, prompt: str) -> None:
        """Cache prompt with TTL"""
        current_time = time.time()
        if len(self.prompt_cache) >= self.config.cache_size:
            self._evict_oldest_cache_entry()
        self.prompt_cache[key] = {
            "prompt": prompt,
            "timestamp": current_time,
            "ttl": self.config.cache_ttl,
        }
        self._cache_access_times[key] = current_time

    def _get_from_cache(self, key: str) -> str | None:
        """Get prompt from cache if valid"""
        if key not in self.prompt_cache:
            return None
        cache_entry = self.prompt_cache[key]
        current_time = time.time()
        if current_time - cache_entry["timestamp"] > cache_entry["ttl"]:
            del self.prompt_cache[key]
            if key in self._cache_access_times:
                del self._cache_access_times[key]
            return None
        self._cache_access_times[key] = current_time
        return cache_entry["prompt"]

    def _evict_oldest_cache_entry(self) -> None:
        """Evict oldest cache entry"""
        if not self._cache_access_times:
            return
        oldest_key = min(self._cache_access_times.keys(), key=lambda k: self._cache_access_times[k])
        if oldest_key in self.prompt_cache:
            del self.prompt_cache[oldest_key]
        if oldest_key in self._cache_access_times:
            del self._cache_access_times[oldest_key]


# Example usage:
# config = PromptConfig(max_length=500, optimization_level=OptimizationLevel.STANDARD, cache_size=50)
# manager = AletheiaPromptManager(config)
# prompt = manager.generate_prompt("Hello", "greeting", PromptType.USER)
