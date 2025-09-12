from __future__ import annotations

import os


def _ids(env_key: str) -> set[int]:
    raw = os.getenv(env_key, "")
    return {int(x.strip()) for x in raw.split(",") if x.strip().isdigit()}


ALLOWED_GUILDS = _ids("ALLOWED_GUILD_IDS")
ALLOWED_CHANNELS = _ids("ALLOWED_CHANNEL_IDS")
ALLOWED_USERS = _ids("ALLOWED_USER_IDS")


def allow_guild(guild_id: int) -> bool:
    return not ALLOWED_GUILDS or guild_id in ALLOWED_GUILDS


def allow_channel(channel_id: int) -> bool:
    return not ALLOWED_CHANNELS or channel_id in ALLOWED_CHANNELS


def allow_user(user_id: int) -> bool:
    return not ALLOWED_USERS or user_id in ALLOWED_USERS
