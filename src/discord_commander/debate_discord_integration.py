#!/usr/bin/env python3
"""
Debate Discord Integration
===========================

Posts agent debates to Discord channel for Commander visibility.
Shows which agent said what with proper attribution.

Channel ID: 1375424568969265152 (Commander's debate channel)

Author: Captain Agent-4
Date: 2025-10-15
"""

import json
import logging
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Commander's debate channel ID
DEBATE_CHANNEL_ID = "1375424568969265152"


class DebateDiscordPoster:
    """Posts debate activity to Discord for visibility."""

    def __init__(self, webhook_url: str | None = None):
        """Initialize with webhook URL."""
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")

        if not self.webhook_url:
            logger.warning("No DISCORD_WEBHOOK_URL found - debate posting disabled")

    def post_debate_start(self, debate_data: dict[str, Any]) -> bool:
        """Post debate start announcement to Discord."""
        if not self.webhook_url:
            return False

        try:
            content = self._format_debate_start(debate_data)
            return self._send_to_discord(content, username="Debate System")
        except Exception as e:
            logger.error(f"Error posting debate start: {e}")
            return False

    def post_vote(
        self, debate_id: str, agent_id: str, option: str, argument: str = "", confidence: int = 5
    ) -> bool:
        """Post agent vote to Discord with attribution."""
        if not self.webhook_url:
            return False

        try:
            # Load debate for context
            debate_file = Path("debates") / f"{debate_id}.json"
            if not debate_file.exists():
                return False

            debate_data = json.loads(debate_file.read_text())

            content = self._format_vote(
                agent_id=agent_id,
                option=option,
                argument=argument,
                confidence=confidence,
                topic=debate_data.get("topic", "Unknown"),
                debate_id=debate_id,
            )

            # Use agent-specific username
            username = f"{agent_id} Vote"

            return self._send_to_discord(content, username=username)
        except Exception as e:
            logger.error(f"Error posting vote: {e}")
            return False

    def post_debate_status(self, debate_id: str, status_data: dict[str, Any]) -> bool:
        """Post debate status/results to Discord."""
        if not self.webhook_url:
            return False

        try:
            content = self._format_status(status_data)
            return self._send_to_discord(content, username="Debate Results")
        except Exception as e:
            logger.error(f"Error posting status: {e}")
            return False

    def _format_debate_start(self, debate_data: dict[str, Any]) -> str:
        """Format debate start message."""
        options_text = "\n".join(f"  {i+1}. {opt}" for i, opt in enumerate(debate_data["options"]))

        return f"""🗳️ **NEW DEBATE STARTED**

**Topic:** {debate_data['topic']}
{f"**Description:** {debate_data['description']}" if debate_data.get('description') else ""}

**Options:**
{options_text}

**Debate ID:** `{debate_data['debate_id']}`
{f"**Deadline:** {debate_data['deadline']}" if debate_data.get('deadline') else ""}

All agents: Cast your votes! 🐝"""

    def _format_vote(
        self,
        agent_id: str,
        option: str,
        argument: str,
        confidence: int,
        topic: str,
        debate_id: str,
    ) -> str:
        """Format vote announcement with agent attribution."""
        confidence_emoji = {
            1: "❓",
            2: "🤔",
            3: "💭",
            4: "👍",
            5: "✅",
            6: "💪",
            7: "🎯",
            8: "🔥",
            9: "⚡",
            10: "🏆",
        }

        emoji = confidence_emoji.get(confidence, "✅")

        msg = f"""**{agent_id}** voted {emoji}

**Debate:** {topic[:60]}
**Choice:** **{option}**
**Confidence:** {confidence}/10"""

        if argument:
            # Truncate long arguments
            arg_preview = argument[:300] + "..." if len(argument) > 300 else argument
            msg += f"\n\n**Argument:**\n> {arg_preview}"

        msg += f"\n\n*Debate ID: `{debate_id}`*"

        return msg

    def _format_status(self, status_data: dict[str, Any]) -> str:
        """Format debate status/results."""
        vote_dist = status_data.get("vote_distribution", {})
        consensus = status_data.get("consensus")

        msg = f"""📊 **DEBATE STATUS UPDATE**

**Topic:** {status_data['topic']}
**Total Votes:** {status_data['total_votes']}/8

**Vote Distribution:**
"""

        for option, count in vote_dist.items():
            percentage = (
                (count / status_data["total_votes"] * 100) if status_data["total_votes"] > 0 else 0
            )
            bar_length = int(percentage / 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            msg += f"  **{option}**: {count} votes ({percentage:.1f}%) {bar}\n"

        if consensus:
            msg += f"\n**Leading Option:** **{consensus['option']}** ({consensus['percent']}%)"
            if consensus["percent"] >= 50:
                msg += " ✅ **MAJORITY REACHED**"
            elif consensus["percent"] >= 66:
                msg += " 🎯 **STRONG CONSENSUS**"

        if status_data.get("arguments_count", 0) > 0:
            msg += f"\n\n**Arguments Posted:** {status_data['arguments_count']}"

        msg += f"\n\n*Debate ID: `{status_data['debate_id']}`*"

        return msg

    def _send_to_discord(self, content: str, username: str = "Swarm Debate") -> bool:
        """Send message to Discord webhook."""
        try:
            payload = {"content": content, "username": username}

            response = requests.post(self.webhook_url, json=payload, timeout=10)

            if response.status_code == 204:
                logger.info(f"✅ Posted debate update to Discord ({username})")
                return True
            else:
                logger.error(f"Discord API returned {response.status_code}: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Error sending to Discord: {e}")
            return False


def post_debate_start_to_discord(debate_data: dict[str, Any]) -> bool:
    """Helper: Post debate start to Discord."""
    poster = DebateDiscordPoster()
    return poster.post_debate_start(debate_data)


def post_vote_to_discord(
    debate_id: str, agent_id: str, option: str, argument: str = "", confidence: int = 5
) -> bool:
    """Helper: Post agent vote to Discord."""
    poster = DebateDiscordPoster()
    return poster.post_vote(debate_id, agent_id, option, argument, confidence)


def post_debate_status_to_discord(debate_id: str, status_data: dict[str, Any]) -> bool:
    """Helper: Post debate status to Discord."""
    poster = DebateDiscordPoster()
    return poster.post_debate_status(debate_id, status_data)
