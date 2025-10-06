"""
Thea Content Scraper Module - V2 Compliance
==========================================

Handles content scraping and processing for Thea Manager.
Provides structured data extraction from web content.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import re
import logging
import time
from typing import Dict, List, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ScrapedContent:
    """Represents scraped content from Thea Manager."""
    content: str
    timestamp: str
    metadata: Dict[str, Any] = None
    quality_score: float = 0.0
    processing_time: float = 0.0

    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}
        if not self.timestamp:
            self.timestamp = str(int(time.time()))


class TheaContentScraper:
    """Handles content scraping and processing for Thea Manager."""

    def __init__(self, config_manager: Any):
        """Initialize content scraper."""
        self.config_manager = config_manager
        self._content_patterns = self._load_content_patterns()

    def scrape_content(self, raw_content: str) -> ScrapedContent:
        """
        Scrape and process content from raw text.

        Args:
            raw_content: Raw content to process

        Returns:
            Processed ScrapedContent object
        """
        start_time = time.time()

        try:
            # Clean and normalize content
            cleaned_content = self._clean_content(raw_content)

            # Extract metadata
            metadata = self._extract_metadata(cleaned_content)

            # Calculate quality score
            quality_score = self._calculate_quality_score(cleaned_content)

            processing_time = time.time() - start_time

            return ScrapedContent(
                content=cleaned_content,
                timestamp=str(int(time.time())),
                metadata=metadata,
                quality_score=quality_score,
                processing_time=processing_time
            )

        except Exception as e:
            logger.error(f"Content scraping failed: {e}")
            return ScrapedContent(
                content=raw_content,
                timestamp=str(int(time.time())),
                metadata={'error': str(e)},
                quality_score=0.0,
                processing_time=time.time() - start_time
            )

    def _clean_content(self, content: str) -> str:
        """Clean and normalize content."""
        if not content:
            return ""

        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content.strip())

        # Remove common artifacts
        content = re.sub(r'\[.*?\]', '', content)  # Remove bracketed text
        content = re.sub(r'<.*?>', '', content)    # Remove HTML tags
        content = re.sub(r'http[s]?://\S+', '', content)  # Remove URLs

        # Normalize quotes and apostrophes
        content = content.replace('"', '"').replace('"', '"')
        content = content.replace(''', "'").replace(''', "'")

        return content.strip()

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from content."""
        metadata = {
            'length': len(content),
            'word_count': len(content.split()),
            'has_code': bool(re.search(r'```|def |class |import ', content)),
            'has_lists': bool(re.search(r'^\s*[-*]\s+', content, re.MULTILINE)),
            'has_headers': bool(re.search(r'^#{1,6}\s+', content, re.MULTILINE)),
        }

        # Extract project-related information
        project_patterns = self.config_manager.get_project_patterns()
        file_types_found = []

        for file_type, pattern in project_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                file_types_found.append(file_type)

        metadata['project_files_mentioned'] = file_types_found
        metadata['project_relevance_score'] = len(file_types_found) / len(project_patterns)

        return metadata

    def _calculate_quality_score(self, content: str) -> float:
        """Calculate content quality score."""
        if not content:
            return 0.0

        score = 0.0
        total_weight = 0.0

        # Length score (0-20 points)
        length = len(content)
        if length > 500:
            score += 20
        elif length > 200:
            score += 15
        elif length > 50:
            score += 10
        else:
            score += 5
        total_weight += 20

        # Structure score (0-30 points)
        if re.search(r'^#{1,6}\s+', content, re.MULTILINE):
            score += 15  # Has headers
        if re.search(r'^\s*[-*]\s+', content, re.MULTILINE):
            score += 10  # Has lists
        if re.search(r'```', content):
            score += 5   # Has code blocks
        total_weight += 30

        # Content score (0-30 points)
        word_count = len(content.split())
        if word_count > 100:
            score += 15
        elif word_count > 50:
            score += 10
        elif word_count > 20:
            score += 5

        # Check for meaningful content
        if re.search(r'\b(project|code|file|system|architecture)\b', content, re.IGNORECASE):
            score += 15
        total_weight += 30

        # Completeness score (0-20 points)
        sentences = len(re.findall(r'[.!?]+', content))
        if sentences > 5:
            score += 15
        elif sentences > 2:
            score += 10
        elif sentences > 0:
            score += 5
        total_weight += 20

        return min(100.0, (score / total_weight) * 100) if total_weight > 0 else 0.0

    def _load_content_patterns(self) -> Dict[str, str]:
        """Load content processing patterns."""
        return {
            'code_block': r'```[\s\S]*?```',
            'header': r'^#{1,6}\s+.+$',
            'list_item': r'^\s*[-*]\s+.+$',
            'url': r'http[s]?://\S+',
            'file_path': r'[\w/\\.-]+\.(py|js|ts|java|cpp|h|md|json|yml|yaml)',
            'project_reference': r'\b(project|repository|codebase|system)\b'
        }

    def validate_content(self, content: ScrapedContent) -> Dict[str, Any]:
        """Validate scraped content quality."""
        issues = []

        if not content.content.strip():
            issues.append("Content is empty")

        if content.quality_score < 30:
            issues.append("Content quality is too low")

        if content.processing_time > 10:
            issues.append("Processing took too long")

        if len(content.metadata.get('project_files_mentioned', [])) == 0:
            issues.append("No project-related content detected")

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'quality_score': content.quality_score,
            'processing_time': content.processing_time
        }


class TheaContentProcessor:
    """Processes and analyzes scraped content."""

    def __init__(self, scraper: TheaContentScraper):
        """Initialize content processor."""
        self.scraper = scraper

    def process_batch(self, raw_contents: List[str]) -> List[ScrapedContent]:
        """
        Process a batch of raw content.

        Args:
            raw_contents: List of raw content strings

        Returns:
            List of processed ScrapedContent objects
        """
        processed = []
        for raw_content in raw_contents:
            scraped = self.scraper.scrape_content(raw_content)
            processed.append(scraped)

        return processed

    def filter_high_quality(self, contents: List[ScrapedContent],
                          min_score: float = 70.0) -> List[ScrapedContent]:
        """
        Filter content by quality score.

        Args:
            contents: List of content to filter
            min_score: Minimum quality score

        Returns:
            Filtered list of high-quality content
        """
        return [content for content in contents if content.quality_score >= min_score]

    def generate_summary(self, contents: List[ScrapedContent]) -> Dict[str, Any]:
        """Generate summary statistics for content batch."""
        if not contents:
            return {'total_items': 0}

        quality_scores = [c.quality_score for c in contents]
        processing_times = [c.processing_time for c in contents]

        return {
            'total_items': len(contents),
            'avg_quality_score': sum(quality_scores) / len(quality_scores),
            'max_quality_score': max(quality_scores),
            'min_quality_score': min(quality_scores),
            'avg_processing_time': sum(processing_times) / len(processing_times),
            'total_processing_time': sum(processing_times),
            'high_quality_count': len([c for c in contents if c.quality_score >= 80])
        }
