from .security_policies import allow_guild, allow_channel, allow_user

def check_context(ctx) -> bool:
    g = ctx.guild.id if ctx.guild else None
    c = ctx.channel.id
    u = ctx.author.id
    return (g is None or allow_guild(g)) and allow_channel(c) and allow_user(u)
