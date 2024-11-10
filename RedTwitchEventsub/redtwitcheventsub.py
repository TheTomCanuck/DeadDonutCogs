from redbot.core import commands, Config
from redbot.core.bot import Red
import discord

class TwitchEventSub(commands.Cog):
    """A cog for managing Twitch EventSub subscriptions and forwarding events to Discord channels."""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890, force_registration=True)

        # Default configuration structure
        default_global = {
            "twitch_api_key": "",
            "twitch_websocket_secret": "",
            "webhook": {
                "url": "",
                "secret": ""
            },
            "event_subscriptions": {}
        }
        self.config.register_global(**default_global)

    ### Configuration Commands ###

    @commands.is_owner()
    @commands.group()
    async def eventsub(self, ctx: commands.Context):
        """Base command for Twitch EventSub configuration."""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @eventsub.command()
    async def add(self, ctx: commands.Context, event_type: str, post_channel: discord.TextChannel, *, message_template: str):
        """Add or update a Twitch EventSub subscription."""
        async with self.config.event_subscriptions() as subscriptions:
            subscriptions[event_type] = {
                "enabled": True,
                "post_channel": post_channel.id,
                "message_template": message_template
            }
        await ctx.send(f"Subscription for `{event_type}` added or updated successfully.")

    @eventsub.command()
    async def remove(self, ctx: commands.Context, event_type: str):
        """Remove a Twitch EventSub subscription."""
        async with self.config.event_subscriptions() as subscriptions:
            if event_type in subscriptions:
                del subscriptions[event_type]
                await ctx.send(f"Subscription for `{event_type}` removed successfully.")
            else:
                await ctx.send(f"No subscription found for `{event_type}`.")

    @eventsub.command()
    async def list(self, ctx: commands.Context):
        """List all current Twitch EventSub subscriptions."""
        subscriptions = await self.config.event_subscriptions()
        if not subscriptions:
            await ctx.send("No subscriptions found.")
            return
        result = "Current EventSub Subscriptions:\n"
        for event_type, details in subscriptions.items():
            enabled = "Enabled" if details.get("enabled") else "Disabled"
            channel_id = details.get("post_channel", None)
            channel = f"<#{channel_id}>" if channel_id else "None"
            template = details.get("message_template", "None")
            result += f"- `{event_type}`: {enabled}, Channel: {channel}, Template: `{template}`\n"
        await ctx.send(result)

    @eventsub.command()
    async def webhook(self, ctx: commands.Context, url: str):
        """Set the webhook URL for forwarding events."""
        await self.config.webhook.url.set(url)
        await ctx.send(f"Webhook URL set to `{url}`.")

    @eventsub.command()
    async def webhook_secret(self, ctx: commands.Context, secret: str):
        """Set the webhook secret for HMAC verification."""
        await self.config.webhook.secret.set(secret)
        await ctx.send("Webhook secret set successfully.")

    @eventsub.command()
    async def api_key(self, ctx: commands.Context, api_key: str):
        """Set the Twitch API key for EventSub."""
        await self.config.twitch_api_key.set(api_key)
        await ctx.send("Twitch API key set successfully.")

    @eventsub.command()
    async def websocket_secret(self, ctx: commands.Context, websocket_secret: str):
        """Set the WebSocket secret for connecting to Twitch EventSub."""
        await self.config.twitch_websocket_secret.set(websocket_secret)
        await ctx.send("Twitch WebSocket secret set successfully.")
