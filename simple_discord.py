#!/usr/bin/env python3
"""Simple Discord Integration - SSOT messaging helper."""

import os
import sys
import json
import requests
import argparse
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Dict, Optional, Tuple


class SimpleDiscordIntegration:
    """Simple Discord integration with SSOT principles"""

    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        self.default_channel = os.getenv('DISCORD_CHANNEL_ID', 'general')

        if not self.webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL environment variable not set")

        print("✅ Discord integration initialized")
        print(f"📱 Webhook: {self.webhook_url[:50]}...")
        print(f"📺 Default channel: {self.default_channel}")

    def send_message(
        self,
        content: str,
        title: str = "Update",
        channel: str | None = None,
        color: int = 0x00FF00,
        fields: Optional[Dict[str, str]] = None,
    ) -> bool:
        try:
            message = {
                "embeds": [
                    {
                        "title": title,
                        "description": content,
                        "color": color,
                        "timestamp": datetime.now().isoformat(),
                        "footer": {
                            "text": "Agent Cellphone V2 - SSOT Discord Integration"
                        },
                    }
                ]
            }

            # Add fields if provided
            if fields:
                message["embeds"][0]["fields"] = [
                    {"name": k, "value": v, "inline": True}
                    for k, v in fields.items()
                ]
            print("📤 Sending message to Discord...")
            print(f"   Title: {title}")
            print(f"   Content: {content[:100]}{'...' if len(content) > 100 else ''}")

            response = requests.post(
                self.webhook_url,
                json=message,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )

            if response.status_code == 204:
                print("✅ Message sent successfully to Discord!")
                return True
            print(f"❌ Failed to send message. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False

        except Exception as e:  # noqa: BLE001
            print(f"❌ Error sending message: {e}")
            return False

    def send_devlog(
        self,
        title: str,
        content: str,
        agent: str = "unknown",
        category: str = "project_update",
        priority: str = "normal",
    ) -> bool:
        formatted_content = f"""📝 **{title}**
🏷️ **Category**: {category}
🤖 **Agent**: {agent}
📊 **Priority**: {priority}
📅 **Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📋 **Content**:
{content}"""

        color_map = {
            "low": 0x00FF00,  # Green
            "normal": 0x0099FF,  # Blue
            "high": 0xFF9900,  # Orange
            "critical": 0xFF0000,  # Red
        }
        color = color_map.get(priority.lower(), 0x0099FF)

        return self.send_message(
            content=formatted_content,
            title=f"Devlog: {title}",
            color=color,
        )

    def send_status_update(
        self,
        status: str,
        details: str = "",
        component: str = "System",
    ) -> bool:
        status_config = {
            "success": {"emoji": "✅", "color": 0x00FF00},
            "warning": {"emoji": "⚠️", "color": 0xFF9900},
            "error": {"emoji": "❌", "color": 0xFF0000},
            "info": {"emoji": "ℹ️", "color": 0x0099FF},
        }

        config = status_config.get(status.lower(), status_config["info"])
        content = f"{config['emoji']} **{component} Status Update**\n\n{details}"

        return self.send_message(
            content=content,
            title=f"Status: {status.title()}",
            color=config["color"],
        )

    def test_connection(self) -> bool:
        print("🧪 Testing Discord connection...")

        success = self.send_message(
            content="This is a test message to verify Discord integration is working.",
            title="Connection Test",
            color=0x00FF00,
        )

        if success:
            print("✅ Discord connection test successful!")
        else:
            print("❌ Discord connection test failed!")

        return success


@dataclass
class CommandSpec:
    help: str
    add_arguments: Callable[[argparse.ArgumentParser], None]
    handler: Callable[[SimpleDiscordIntegration, argparse.Namespace], Tuple[bool, str]]


def _add_content_title(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("content", help="Message content")
    parser.add_argument("title", help="Message title")


def _add_message_args(parser: argparse.ArgumentParser) -> None:
    _add_content_title(parser)
    parser.add_argument("--channel", "-c", help="Discord channel")
    parser.add_argument(
        "--color",
        "-cl",
        type=lambda x: int(x, 16),
        default=0x00FF00,
        help="Embed color (hex)",
    )


def _add_devlog_args(parser: argparse.ArgumentParser) -> None:
    _add_content_title(parser)
    parser.add_argument("--agent", "-a", default="unknown", help="Agent ID for devlog")
    parser.add_argument("--category", "-cat", default="project_update", help="Devlog category")
    parser.add_argument("--priority", "-p", default="normal", help="Devlog priority")


def _add_status_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("status", help="Status (success/warning/error/info)")
    parser.add_argument("details", help="Status details")
    parser.add_argument(
        "--component",
        "-comp",
        default="System",
        help="Component name for status",
    )


def _handle_message(
    discord: SimpleDiscordIntegration, args: argparse.Namespace
) -> Tuple[bool, str]:
    success = discord.send_message(
        content=args.content,
        title=args.title,
        channel=args.channel,
        color=args.color,
    )
    return success, (
        "Message sent successfully" if success else "Failed to send message"
    )


def _handle_devlog(
    discord: SimpleDiscordIntegration, args: argparse.Namespace
) -> Tuple[bool, str]:
    success = discord.send_devlog(
        title=args.title,
        content=args.content,
        agent=args.agent,
        category=args.category,
        priority=args.priority,
    )
    return success, (
        "Devlog entry sent" if success else "Failed to send devlog entry"
    )


def _handle_status(
    discord: SimpleDiscordIntegration, args: argparse.Namespace
) -> Tuple[bool, str]:
    success = discord.send_status_update(
        status=args.status,
        details=args.details,
        component=args.component,
    )
    return success, (
        "Status update sent" if success else "Failed to send status update"
    )


def _handle_test(
    discord: SimpleDiscordIntegration, args: argparse.Namespace
) -> Tuple[bool, str]:
    success = discord.test_connection()
    return success, (
        "Discord connection test successful!"
        if success
        else "Discord connection test failed!"
    )


COMMANDS: Dict[str, CommandSpec] = {
    "message": CommandSpec("Send a standard Discord message", _add_message_args, _handle_message),
    "devlog": CommandSpec("Send a formatted devlog entry", _add_devlog_args, _handle_devlog),
    "status": CommandSpec("Send a status update message", _add_status_args, _handle_status),
    "test": CommandSpec("Test Discord connection", lambda p: None, _handle_test),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simple Discord Integration - SSOT Implementation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python simple_discord.py message \"Hello\" \"Test\"\n"
            "  python simple_discord.py devlog \"Done\" \"All systems integrated\" --agent agent-1\n"
            "  python simple_discord.py status success \"Deployment completed\"\n"
            "  python simple_discord.py test"
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    for name, spec in COMMANDS.items():
        sub = subparsers.add_parser(name, help=spec.help)
        spec.add_arguments(sub)
        sub.set_defaults(command=name)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        discord = SimpleDiscordIntegration()
        spec = COMMANDS[args.command]
        success, message = spec.handler(discord, args)
        print(message)
        return 0 if success else 1

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return 1
    except Exception as e:  # noqa: BLE001
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

