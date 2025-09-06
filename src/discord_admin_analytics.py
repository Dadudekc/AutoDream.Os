"""Discord Admin Analytics Modules V2 Compliant analytics utilities for Discord
Administrator Commander.

Author: Agent-1 - Integration & Core Systems Specialist
Version: 1.0.0 - V2 Compliance
License: MIT
"""

logger = logging.getLogger(__name__)


class AnalyticsModules:
    """Analytics utilities for Discord Administrator Commander."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.analytics_data: Dict[str, Any] = {
            "member_activity": {},
            "message_stats": {},
            "channel_stats": {},
            "server_growth": [],
        }
        self.tracking_enabled = config.get("analytics", {}).get(
            "track_member_activity", True
        )

    async def track_member_activity(self, member: discord.Member, action: str):
        """Track member activity."""
        if not self.tracking_enabled:
            return

        member_id = str(member.id)
        if member_id not in self.analytics_data["member_activity"]:
            self.analytics_data["member_activity"][member_id] = {
                "username": member.display_name,
                "joined_at": member.joined_at.isoformat() if member.joined_at else None,
                "activities": [],
            }

        activity_entry = {
            "action": action,
            "timestamp": datetime.utcnow().isoformat(),
            "channel": (
                str(member.voice.channel)
                if member.voice and member.voice.channel
                else None
            ),
        }

        self.analytics_data["member_activity"][member_id]["activities"].append(
            activity_entry
        )

        # Keep only last 100 activities per member
        if len(self.analytics_data["member_activity"][member_id]["activities"]) > 100:
            self.analytics_data["member_activity"][member_id]["activities"] = (
                self.analytics_data["member_activity"][member_id]["activities"][-100:]
            )

    async def track_message_stats(self, message: discord.Message):
        """Track message statistics."""
        if not self.config.get("analytics", {}).get("track_message_stats", True):
            return

        channel_id = str(message.channel.id)
        if channel_id not in self.analytics_data["message_stats"]:
            self.analytics_data["message_stats"][channel_id] = {
                "channel_name": message.channel.name,
                "total_messages": 0,
                "messages_by_hour": {},
                "messages_by_user": {},
            }

        # Update total messages
        self.analytics_data["message_stats"][channel_id]["total_messages"] += 1

        # Track by hour
        hour = datetime.utcnow().hour
        if (
            hour
            not in self.analytics_data["message_stats"][channel_id]["messages_by_hour"]
        ):
            self.analytics_data["message_stats"][channel_id]["messages_by_hour"][
                hour
            ] = 0
        self.analytics_data["message_stats"][channel_id]["messages_by_hour"][hour] += 1

        # Track by user
        user_id = str(message.author.id)
        if (
            user_id
            not in self.analytics_data["message_stats"][channel_id]["messages_by_user"]
        ):
            self.analytics_data["message_stats"][channel_id]["messages_by_user"][
                user_id
            ] = {"username": message.author.display_name, "count": 0}
        self.analytics_data["message_stats"][channel_id]["messages_by_user"][user_id][
            "count"
        ] += 1

    async def track_server_growth(self, guild: discord.Guild):
        """Track server growth metrics."""
        growth_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "member_count": len(guild.members),
            "channel_count": len(guild.channels),
            "role_count": len(guild.roles),
        }

        self.analytics_data["server_growth"].append(growth_entry)

        # Keep only last 1000 entries
        if len(self.analytics_data["server_growth"]) > 1000:
            self.analytics_data["server_growth"] = self.analytics_data["server_growth"][
                -1000:
            ]

    def get_member_activity_report(
        self, member_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get member activity report."""
        if member_id:
            return self.analytics_data["member_activity"].get(member_id, {})

        # Get summary of all members
        summary = {
            "total_members_tracked": len(self.analytics_data["member_activity"]),
            "most_active_members": [],
        }

        # Find most active members
        member_activity_counts = {}
        for member_id, data in self.analytics_data["member_activity"].items():
            member_activity_counts[member_id] = len(data["activities"])

        # Sort by activity count
        sorted_members = sorted(
            member_activity_counts.items(), key=lambda x: x[1], reverse=True
        )

        for member_id, count in sorted_members[:10]:  # Top 10
            member_data = self.analytics_data["member_activity"][member_id]
            summary["most_active_members"].append(
                {
                    "username": member_data["username"],
                    "activity_count": count,
                    "joined_at": member_data["joined_at"],
                }
            )

        return summary

    def get_message_stats_report(
        self, channel_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get message statistics report."""
        if channel_id:
            return self.analytics_data["message_stats"].get(channel_id, {})

        # Get summary of all channels
        summary = {
            "total_channels_tracked": len(self.analytics_data["message_stats"]),
            "total_messages": 0,
            "most_active_channels": [],
            "most_active_users": {},
        }

        # Calculate totals and find most active
        channel_totals = {}
        user_totals = {}

        for channel_id, data in self.analytics_data["message_stats"].items():
            channel_totals[channel_id] = data["total_messages"]
            summary["total_messages"] += data["total_messages"]

            # Aggregate user stats across channels
            for user_id, user_data in data["messages_by_user"].items():
                if user_id not in user_totals:
                    user_totals[user_id] = {
                        "username": user_data["username"],
                        "count": 0,
                    }
                user_totals[user_id]["count"] += user_data["count"]

        # Sort channels by activity
        sorted_channels = sorted(
            channel_totals.items(), key=lambda x: x[1], reverse=True
        )
        for channel_id, count in sorted_channels[:10]:  # Top 10
            channel_data = self.analytics_data["message_stats"][channel_id]
            summary["most_active_channels"].append(
                {"channel_name": channel_data["channel_name"], "message_count": count}
            )

        # Sort users by activity
        sorted_users = sorted(
            user_totals.items(), key=lambda x: x[1]["count"], reverse=True
        )
        summary["most_active_users"] = [
            user_data for user_id, user_data in sorted_users[:10]
        ]

        return summary

    def get_server_growth_report(self, days: int = 30) -> Dict[str, Any]:
        """Get server growth report."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Filter data by date
        recent_data = [
            entry
            for entry in self.analytics_data["server_growth"]
            if datetime.fromisoformat(entry["timestamp"]) > cutoff_date
        ]

        if not get_unified_validator().validate_required(recent_data):
            return {"error": "No data available for the specified period"}

        # Calculate growth metrics
        first_entry = recent_data[0]
        last_entry = recent_data[-1]

        member_growth = last_entry["member_count"] - first_entry["member_count"]
        channel_growth = last_entry["channel_count"] - first_entry["channel_count"]
        role_growth = last_entry["role_count"] - first_entry["role_count"]

        # Calculate daily averages
        days_span = (
            datetime.fromisoformat(last_entry["timestamp"])
            - datetime.fromisoformat(first_entry["timestamp"])
        ).days or 1

        daily_member_growth = member_growth / days_span
        daily_channel_growth = channel_growth / days_span
        daily_role_growth = role_growth / days_span

        return {
            "period_days": days,
            "data_points": len(recent_data),
            "member_growth": {
                "total": member_growth,
                "daily_average": round(daily_member_growth, 2),
                "current_count": last_entry["member_count"],
            },
            "channel_growth": {
                "total": channel_growth,
                "daily_average": round(daily_channel_growth, 2),
                "current_count": last_entry["channel_count"],
            },
            "role_growth": {
                "total": role_growth,
                "daily_average": round(daily_role_growth, 2),
                "current_count": last_entry["role_count"],
            },
            "growth_trend": (
                "positive"
                if member_growth > 0
                else "negative" if member_growth < 0 else "stable"
            ),
        }

    def export_analytics_data(self, filename: Optional[str] = None) -> str:
        """Export analytics data to JSON file."""
        if not get_unified_validator().validate_required(filename):
            filename = (
                f"discord_analytics_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            )

        export_data = {
            "export_timestamp": datetime.utcnow().isoformat(),
            "analytics_data": self.analytics_data,
        }

        with open(filename, "w") as f:
            write_json(export_data, f, indent=2)

        get_logger(__name__).info(f"Analytics data exported to {filename}")
        return filename

    def clear_analytics_data(self):
        """Clear all analytics data."""
        self.analytics_data = {
            "member_activity": {},
            "message_stats": {},
            "channel_stats": {},
            "server_growth": [],
        }
        get_logger(__name__).info("Analytics data cleared")

    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get overall analytics summary."""
        return {
            "tracking_enabled": self.tracking_enabled,
            "data_summary": {
                "members_tracked": len(self.analytics_data["member_activity"]),
                "channels_tracked": len(self.analytics_data["message_stats"]),
                "growth_data_points": len(self.analytics_data["server_growth"]),
                "total_messages": sum(
                    data["total_messages"]
                    for data in self.analytics_data["message_stats"].values()
                ),
            },
            "last_updated": datetime.utcnow().isoformat(),
        }
