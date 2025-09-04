"""
Discord Commander Devlog Integrator Module

Provides devlog integration functionality for the Discord commander system.
"""

from ..core.unified_import_system import logging


class DiscordCommanderDevlogIntegrator:
    """
    Devlog integrator for Discord Commander.

    Manages devlog entries, Discord posting, and file logging.
    """

    def __init__(self, bot: discord.Client, config_manager):
        self.bot = bot
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)

        # Load devlog configuration
        self.devlog_config = self.config_manager.load_devlog_config()

        # Ensure log directory exists
        self.log_directory = get_unified_utility().Path(self.devlog_config.get('log_directory', 'logs/devlog'))
        self.log_directory.mkdir(parents=True, exist_ok=True)

    async def create_devlog_entry(self, title: str, content: str,
                                category: str = "general", agent_id: str = None) -> bool:
        """Create a devlog entry with Discord posting and file logging."""
        try:
            # Create devlog entry
            entry = {
                'id': self._generate_entry_id(),
                'timestamp': datetime.now().isoformat(),
                'title': title,
                'content': content,
                'category': category,
                'agent_id': agent_id or 'DiscordCommander',
                'color': self._get_category_color(category)
            }

            # Save to file
            file_saved = await self._save_devlog_to_file(entry)

            # Post to Discord
            discord_posted = await self._post_devlog_to_discord(entry)

            success = file_saved and discord_posted
            if success:
                self.get_logger(__name__).info(f"Devlog entry created: {title}")
            else:
                self.get_logger(__name__).warning(f"Devlog entry partially created: {title}")

            return success

        except Exception as e:
            self.get_logger(__name__).error(f"Error creating devlog entry '{title}': {e}")
            return False

    def _generate_entry_id(self) -> str:
        """Generate unique entry ID."""
        return f"devlog_{uuid.uuid4().hex[:8]}"

    def _get_category_color(self, category: str) -> int:
        """Get color for devlog category."""
        category_colors = self.devlog_config.get('categories', {})

        if category in category_colors:
            return category_colors[category].get('color', 0x000000)
        else:
            # Default color for unknown categories
            return 0x808080

    async def _save_devlog_to_file(self, entry: dict) -> bool:
        """Save devlog entry to file."""
        try:
            if not self.devlog_config.get('file_logging', True):
                return True  # Skip file logging if disabled

            # Create filename with date
            date_str = datetime.now().strftime('%Y-%m-%d')
            filename = f"devlog_{date_str}.json"
            filepath = self.log_directory / filename

            # Load existing entries or create new list
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    entries = read_json(f)
            else:
                entries = []

            # Add new entry
            entries.append(entry)

            # Save updated entries
            with open(filepath, 'w', encoding='utf-8') as f:
                write_json(entries, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            self.get_logger(__name__).error(f"Error saving devlog to file: {e}")
            return False

    async def _post_devlog_to_discord(self, entry: dict) -> bool:
        """Post devlog entry to Discord."""
        try:
            if not self.devlog_config.get('auto_post', True):
                return True  # Skip Discord posting if disabled

            channel_id = self.devlog_config.get('channel_id')
            if not get_unified_validator().validate_required(channel_id):
                self.get_logger(__name__).warning("No devlog channel ID configured")
                return False

            channel = self.bot.get_channel(int(channel_id))
            if not get_unified_validator().validate_required(channel):
                self.get_logger(__name__).warning(f"Devlog channel {channel_id} not found")
                return False

            # Create embed
            embed = discord.Embed(
                title=f"📋 {entry['title']}",
                description=entry['content'],
                color=entry['color'],
                timestamp=datetime.fromisoformat(entry['timestamp'])
            )

            # Add category emoji if available
            category_info = self.devlog_config.get('categories', {}).get(entry['category'], {})
            emoji = category_info.get('emoji', '📝')
            embed.title = f"{emoji} {entry['title']}"

            # Add fields
            embed.add_field(name="Category", value=entry['category'].title(), inline=True)
            embed.add_field(name="Agent", value=entry['agent_id'], inline=True)
            embed.add_field(name="ID", value=entry['id'], inline=True)

            # Set footer
            embed.set_footer(text=f"Devlog Entry • {entry['timestamp']}")

            # Send embed
            await channel.send(embed=embed)

            return True

        except Exception as e:
            self.get_logger(__name__).error(f"Error posting devlog to Discord: {e}")
            return False

    async def get_recent_entries(self, limit: int = 10) -> list:
        """Get recent devlog entries."""
        try:
            # Find most recent log file
            log_files = list(self.log_directory.glob('devlog_*.json'))
            if not get_unified_validator().validate_required(log_files):
                return []

            # Sort by date (most recent first)
            log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            recent_file = log_files[0]

            # Load entries
            with open(recent_file, 'r', encoding='utf-8') as f:
                entries = read_json(f)

            # Sort by timestamp (most recent first) and limit
            entries.sort(key=lambda x: x['timestamp'], reverse=True)
            return entries[:limit]

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting recent devlog entries: {e}")
            return []

    async def search_entries(self, query: str, limit: int = 20) -> list:
        """Search devlog entries by content."""
        try:
            results = []

            # Search through all log files
            for log_file in self.log_directory.glob('devlog_*.json'):
                with open(log_file, 'r', encoding='utf-8') as f:
                    entries = read_json(f)

                # Search entries
                for entry in entries:
                    if (query.lower() in entry['title'].lower() or
                        query.lower() in entry['content'].lower() or
                        query.lower() in entry['category'].lower()):
                        results.append(entry)

                        if len(results) >= limit:
                            break

                if len(results) >= limit:
                    break

            # Sort by timestamp (most recent first)
            results.sort(key=lambda x: x['timestamp'], reverse=True)
            return results[:limit]

        except Exception as e:
            self.get_logger(__name__).error(f"Error searching devlog entries: {e}")
            return []

    def get_devlog_stats(self) -> Dict[str, Any]:
        """Get devlog statistics."""
        try:
            total_entries = 0
            category_counts = {}
            recent_activity = []

            # Analyze all log files
            for log_file in self.log_directory.glob('devlog_*.json'):
                with open(log_file, 'r', encoding='utf-8') as f:
                    entries = read_json(f)

                total_entries += len(entries)

                for entry in entries:
                    category = entry.get('category', 'unknown')
                    category_counts[category] = category_counts.get(category, 0) + 1

                    # Track recent activity (last 24 hours)
                    entry_time = datetime.fromisoformat(entry['timestamp'])
                    if (datetime.now() - entry_time).total_seconds() < 86400:  # 24 hours
                        recent_activity.append(entry)

            return {
                'total_entries': total_entries,
                'categories': category_counts,
                'recent_activity_count': len(recent_activity),
                'log_files_count': len(list(self.log_directory.glob('devlog_*.json')))
            }

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting devlog stats: {e}")
            return {
                'total_entries': 0,
                'categories': {},
                'recent_activity_count': 0,
                'log_files_count': 0
            }

