"""GitHub Book Data Loader - Extracted from github_book_viewer.py for V2 compliance."""

from pathlib import Path
from typing import Any
import re


class GitHubBookData:
    """Loads and manages GitHub book repo data."""

    def __init__(self):
        self.devlogs_path = Path("swarm_brain/devlogs/repository_analysis")
        self.book_path = Path("GITHUB_75_REPOS_COMPREHENSIVE_ANALYSIS_BOOK.md")
        self.repos_data = self._load_all_repos()

    def _load_all_repos(self) -> dict[int, dict[str, Any]]:
        """Load all repo data from devlogs."""
        repos = {}
        if self.devlogs_path.exists():
            for devlog_file in sorted(self.devlogs_path.glob("*.md")):
                repo_num = self._extract_repo_number(devlog_file.name)
                if repo_num:
                    repos[repo_num] = self._parse_devlog(devlog_file)
        return repos

    def _extract_repo_number(self, filename: str) -> int | None:
        """Extract repo number from filename."""
        patterns = [r"Repo_(\d+)_", r"github_repo_analysis_(\d+)_", r"github_analysis_(\d+)_"]
        for pattern in patterns:
            match = re.search(pattern, filename)
            if match:
                return int(match.group(1))
        return None

    def _parse_devlog(self, devlog_path: Path) -> dict[str, Any]:
        """Parse devlog file."""
        try:
            content = devlog_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            return {
                "name": self._extract_repo_name(devlog_path.stem, content),
                "devlog_path": str(devlog_path),
                "agent": self._extract_agent(content),
                "purpose": self._extract_purpose(lines),
                "roi": self._extract_roi(content),
                "integration_hours": self._extract_integration_hours(content),
                "quality_rating": self._extract_quality(content),
                "key_features": self._extract_key_features(lines),
                "integration_value": self._extract_integration_value(lines),
                "recommendations": self._extract_recommendations(lines),
                "goldmine": self._is_goldmine(content),
                "content_preview": content[:500],
            }
        except Exception:
            return {"name": "Unknown", "error": "Parse failed"}

    def _extract_repo_name(self, stem: str, content: str) -> str:
        """Extract repo name."""
        for line in content.split("\n")[:20]:
            if "Repo #" in line or "Repository:" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    return parts[-1].strip()
        return stem.replace("_", " ").title()

    def _extract_agent(self, content: str) -> str:
        """Extract analyzing agent."""
        for line in content.split("\n")[:30]:
            if "Analyzed By:" in line or "Agent:" in line:
                return line.split(":")[-1].strip()
        return "Unknown"

    def _extract_purpose(self, lines: list[str]) -> str:
        """Extract purpose."""
        for i, line in enumerate(lines):
            if "Purpose:" in line or "PRIMARY FUNCTION" in line:
                return lines[i].split(":")[-1].strip() if ":" in lines[i] else "Unknown"
        return "Unknown"

    def _extract_roi(self, content: str) -> str:
        """Extract ROI."""
        roi_match = re.search(r"ROI[:\s]+([0-9.]+\s*[→x×]\s*[0-9.]+)", content, re.IGNORECASE)
        return roi_match.group(1) if roi_match else "Unknown"

    def _extract_integration_hours(self, content: str) -> str:
        """Extract integration hours."""
        hours_match = re.search(r"(\d+-\d+)\s*hours?", content, re.IGNORECASE)
        return hours_match.group(1) if hours_match else "Unknown"

    def _extract_quality(self, content: str) -> str:
        """Extract quality rating."""
        quality_match = re.search(r"Quality[:\s]+([⭐]+|\d+/10)", content, re.IGNORECASE)
        return quality_match.group(1) if quality_match else "Unknown"

    def _extract_key_features(self, lines: list[str]) -> list[str]:
        """Extract key features."""
        features = []
        in_features = False
        for line in lines:
            if "Key Features" in line or "What It Provides" in line:
                in_features = True
            elif in_features and line.strip().startswith("-"):
                features.append(line.strip()[2:])
                if len(features) >= 5:
                    break
        return features[:5]

    def _extract_integration_value(self, lines: list[str]) -> str:
        """Extract integration value."""
        for line in lines:
            if "Integration Value:" in line:
                return line.split(":")[-1].strip()
        return "Unknown"

    def _extract_recommendations(self, lines: list[str]) -> str:
        """Extract recommendations."""
        for line in lines:
            if "Recommendation:" in line or "VERDICT:" in line:
                return line.split(":")[-1].strip()
        return "Unknown"

    def _is_goldmine(self, content: str) -> bool:
        """Check if repo is goldmine."""
        keywords = ["JACKPOT", "GOLDMINE", "CRITICAL DISCOVERY", "LEGENDARY", "💎", "🏆"]
        return any(keyword in content.upper() for keyword in keywords)

    def get_repo(self, repo_num: int) -> dict[str, Any] | None:
        """Get repo by number."""
        return self.repos_data.get(repo_num)

    def get_goldmines(self) -> list[dict[str, Any]]:
        """Get all goldmine repos."""
        return [
            {"num": num, **data}
            for num, data in sorted(self.repos_data.items())
            if data.get("goldmine", False)
        ]

    def get_all_repos(self) -> dict[int, dict[str, Any]]:
        """Get all repos."""
        return self.repos_data

    def get_analyzed_count(self) -> int:
        """Get count of analyzed repos."""
        return len(self.repos_data)

