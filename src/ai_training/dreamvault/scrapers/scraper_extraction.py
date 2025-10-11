"""ChatGPT Scraper Extraction Methods - V2 Compliance | Agent-5"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ScraperExtraction:
    """Handles conversation extraction logic."""

    @staticmethod
    def reverse_file_numbering(output_dir: str, total_count: int):
        """Reverse file numbering to match conversation order."""
        try:
            output_path = Path(output_dir)
            json_files = sorted(output_path.glob("*.json"))
            for idx, file in enumerate(json_files, 1):
                new_number = total_count - idx + 1
                new_name = f"conversation_{new_number:04d}.json"
                new_path = output_path / new_name
                temp_path = output_path / f"temp_{new_number:04d}.json"
                file.rename(temp_path)
            temp_files = sorted(output_path.glob("temp_*.json"))
            for temp_file in temp_files:
                final_name = temp_file.name.replace("temp_", "")
                temp_file.rename(output_path / final_name)
            logger.info(f"✅ Reversed numbering for {len(json_files)} files")
        except Exception as e:
            logger.error(f"Error reversing file numbering: {e}")
