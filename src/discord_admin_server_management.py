"""Discord Admin Server Management Modules V2 Compliant server management utilities for
Discord Administrator Commander.

Author: Agent-1 - Integration & Core Systems Specialist
Version: 1.0.0 - V2 Compliance
License: MIT
"""

from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ServerStats:
    """Server statistics data structure."""

    total_members: int
    online_members: int
    total_channels: int
    total_roles: int
    server_created: datetime
    last_activity: datetime


class ServerManagementModules:
    """Server management utilities for Discord Administrator Commander."""

    @staticmethod
    async def create_text_channel(
        guild: discord.Guild,
        name: str,
        category: Optional[discord.CategoryChannel] = None,
        topic: Optional[str] = None,
        slowmode: int = 0,
    ) -> discord.TextChannel:
        """Create a new text channel."""
        try:
            overwrites = {}
            if category:
                overwrites = category.overwrites.copy()

            channel = await guild.create_text_channel(
                name=name,
                category=category,
                topic=topic,
                slowmode_delay=slowmode,
                overwrites=overwrites,
            )
            get_logger(__name__).info(f"Created text channel: {name} in {guild.name}")
            return channel
        except Exception as e:
            get_logger(__name__).error(f"Failed to create text channel {name}: {e}")
            raise

    @staticmethod
    async def create_voice_channel(
        guild: discord.Guild,
        name: str,
        category: Optional[discord.CategoryChannel] = None,
        user_limit: int = 0,
        bitrate: int = 64000,
    ) -> discord.VoiceChannel:
        """Create a new voice channel."""
        try:
            overwrites = {}
            if category:
                overwrites = category.overwrites.copy()

            channel = await guild.create_voice_channel(
                name=name,
                category=category,
                user_limit=user_limit,
                bitrate=bitrate,
                overwrites=overwrites,
            )
            get_logger(__name__).info(f"Created voice channel: {name} in {guild.name}")
            return channel
        except Exception as e:
            get_logger(__name__).error(f"Failed to create voice channel {name}: {e}")
            raise

    @staticmethod
    async def create_category(
        guild: discord.Guild, name: str, position: Optional[int] = None
    ) -> discord.CategoryChannel:
        """Create a new category."""
        try:
            category = await guild.create_category(name=name, position=position)
            get_logger(__name__).info(f"Created category: {name} in {guild.name}")
            return category
        except Exception as e:
            get_logger(__name__).error(f"Failed to create category {name}: {e}")
            raise

    @staticmethod
    async def delete_channel(
        channel: discord.abc.GuildChannel, reason: Optional[str] = None
    ) -> bool:
        """Delete a channel."""
        try:
            await channel.delete(reason=reason)
            get_logger(__name__).info(f"Deleted channel: {channel.name}")
            return True
        except Exception as e:
            get_logger(__name__).error(f"Failed to delete channel {channel.name}: {e}")
            return False

    @staticmethod
    async def create_role(
        guild: discord.Guild,
        name: str,
        color: discord.Color = discord.Color.default(),
        permissions: discord.Permissions = discord.Permissions.none(),
        hoist: bool = False,
        mentionable: bool = False,
    ) -> discord.Role:
        """Create a new role."""
        try:
            role = await guild.create_role(
                name=name,
                color=color,
                permissions=permissions,
                hoist=hoist,
                mentionable=mentionable,
            )
            get_logger(__name__).info(f"Created role: {name} in {guild.name}")
            return role
        except Exception as e:
            get_logger(__name__).error(f"Failed to create role {name}: {e}")
            raise

    @staticmethod
    async def assign_role(
        member: discord.Member, role: discord.Role, reason: Optional[str] = None
    ) -> bool:
        """Assign a role to a member."""
        try:
            await member.add_roles(role, reason=reason)
            get_logger(__name__).info(
                f"Assigned role {role.name} to {member.display_name}"
            )
            return True
        except Exception as e:
            get_logger(__name__).error(
                f"Failed to assign role {role.name} to {member.display_name}: {e}"
            )
            return False

    @staticmethod
    async def remove_role(
        member: discord.Member, role: discord.Role, reason: Optional[str] = None
    ) -> bool:
        """Remove a role from a member."""
        try:
            await member.remove_roles(role, reason=reason)
            get_logger(__name__).info(
                f"Removed role {role.name} from {member.display_name}"
            )
            return True
        except Exception as e:
            get_logger(__name__).error(
                f"Failed to remove role {role.name} from {member.display_name}: {e}"
            )
            return False

    @staticmethod
    async def kick_member(member: discord.Member, reason: Optional[str] = None) -> bool:
        """Kick a member from the server."""
        try:
            await member.kick(reason=reason)
            get_logger(__name__).info(f"Kicked member: {member.display_name}")
            return True
        except Exception as e:
            get_logger(__name__).error(
                f"Failed to kick member {member.display_name}: {e}"
            )
            return False

    @staticmethod
    async def ban_member(
        member: discord.Member,
        reason: Optional[str] = None,
        delete_message_days: int = 0,
    ) -> bool:
        """Ban a member from the server."""
        try:
            await member.ban(reason=reason, delete_message_days=delete_message_days)
            get_logger(__name__).info(f"Banned member: {member.display_name}")
            return True
        except Exception as e:
            get_logger(__name__).error(
                f"Failed to ban member {member.display_name}: {e}"
            )
            return False

    @staticmethod
    async def unban_member(
        guild: discord.Guild, user: discord.User, reason: Optional[str] = None
    ) -> bool:
        """Unban a member from the server."""
        try:
            await guild.unban(user, reason=reason)
            get_logger(__name__).info(f"Unbanned member: {user.display_name}")
            return True
        except Exception as e:
            get_logger(__name__).error(
                f"Failed to unban member {user.display_name}: {e}"
            )
            return False

    @staticmethod
    async def timeout_member(
        member: discord.Member, duration: timedelta, reason: Optional[str] = None
    ) -> bool:
        """Timeout a member."""
        try:
            await member.timeout(duration, reason=reason)
            get_logger(__name__).info(
                f"Timed out member: {member.display_name} for {duration}"
            )
            return True
        except Exception as e:
            get_logger(__name__).error(
                f"Failed to timeout member {member.display_name}: {e}"
            )
            return False

    @staticmethod
    async def remove_timeout(
        member: discord.Member, reason: Optional[str] = None
    ) -> bool:
        """Remove timeout from a member."""
        try:
            await member.timeout(None, reason=reason)
            get_logger(__name__).info(
                f"Removed timeout from member: {member.display_name}"
            )
            return True
        except Exception as e:
            get_logger(__name__).error(
                f"Failed to remove timeout from member {member.display_name}: {e}"
            )
            return False

    @staticmethod
    def get_server_stats(guild: discord.Guild) -> ServerStats:
        """Get server statistics."""
        online_members = sum(
            1 for member in guild.members if member.status != discord.Status.offline
        )

        return ServerStats(
            total_members=len(guild.members),
            online_members=online_members,
            total_channels=len(guild.channels),
            total_roles=len(guild.roles),
            server_created=guild.created_at,
            last_activity=datetime.utcnow(),
        )

    @staticmethod
    def generate_server_report(guild: discord.Guild) -> Dict[str, Any]:
        """Generate a comprehensive server report."""
        stats = ServerManagementModules.get_server_stats(guild)

        # Channel breakdown
        text_channels = len(
            [
                c
                for c in guild.channels
                if get_unified_validator().validate_type(c, discord.TextChannel)
            ]
        )
        voice_channels = len(
            [
                c
                for c in guild.channels
                if get_unified_validator().validate_type(c, discord.VoiceChannel)
            ]
        )
        categories = len(
            [
                c
                for c in guild.channels
                if get_unified_validator().validate_type(c, discord.CategoryChannel)
            ]
        )

        # Role breakdown
        managed_roles = len([r for r in guild.roles if r.managed])
        custom_roles = len([r for r in guild.roles if not r.managed])

        # Member breakdown
        bots = len([m for m in guild.members if m.bot])
        humans = len([m for m in guild.members if not m.bot])

        return {
            "server_info": {
                "name": guild.name,
                "id": guild.id,
                "owner": str(guild.owner),
                "created_at": guild.created_at.isoformat(),
                "member_count": stats.total_members,
                "online_members": stats.online_members,
            },
            "channels": {
                "total": stats.total_channels,
                "text_channels": text_channels,
                "voice_channels": voice_channels,
                "categories": categories,
            },
            "roles": {
                "total": stats.total_roles,
                "managed_roles": managed_roles,
                "custom_roles": custom_roles,
            },
            "members": {
                "total": stats.total_members,
                "humans": humans,
                "bots": bots,
                "online": stats.online_members,
            },
            "generated_at": datetime.utcnow().isoformat(),
        }
