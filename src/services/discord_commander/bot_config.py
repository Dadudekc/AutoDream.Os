"""
Discord Commander Bot Configuration
V2 Compliant bot configuration management
"""

import os
from pathlib import Path
from typing import Optional


class BotConfig:
    """Bot configuration manager"""
    
    def __init__(self):
        """Initialize configuration"""
        self.project_root = Path(__file__).parent.parent.parent.parent
        self._load_env()
    
    def _load_env(self):
        """Load environment variables"""
        try:
            from dotenv import load_dotenv
            env_path = self.project_root / ".env"
            if env_path.exists():
                load_dotenv(env_path)
        except ImportError:
            pass
    
    def get_token(self) -> Optional[str]:
        """Get Discord bot token"""
        return os.getenv("DISCORD_BOT_TOKEN")
    
    def get_prefix(self) -> str:
        """Get command prefix"""
        return os.getenv("DISCORD_PREFIX", "!")
    
    def get_guild_id(self) -> Optional[int]:
        """Get guild ID"""
        guild_id = os.getenv("DISCORD_GUILD_ID")
        return int(guild_id) if guild_id else None
    
    def get_log_level(self) -> str:
        """Get log level"""
        return os.getenv("LOG_LEVEL", "INFO")
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled"""
        return os.getenv("DEBUG", "false").lower() == "true"
