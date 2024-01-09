import discord
from discord import app_commands
from discopilot.channel_mapper import ChannelMapper
from discopilot.utils import get_discord_details
from datetime import datetime, timedelta

class DiscordBot:
    """A bot that interacts with Discord
    
    Example usage:
    import os
    import asyncio
    config_file_path = os.getenv("DISCOPILOT_CONFIG")
    discord_bot = DiscordBot(config_file_path, version = 'dev')
    asyncio.run(discord_bot.post("Hello, world!")) # default channel_id need to be set in config file
    asyncio.run(discord_bot.post("Hello, world!", channel_id = 1234567890) # try a different channel_id
    asyncio.run(discord_bot.fetch(hours = 24))
    asyncio.run(discord_bot.fetch(start_time = datetime(2023, 9, 1), end_time = datetime(2023, 9, 2)))
    asyncio.run(discord_bot.fetch(channel_id = 1234567890, hours = 24))
    asyncio.run(discord_bot.fetch(channel_id = 1234567890, start_time = datetime(2021, 1, 1), end_time = datetime(2021, 1, 2)))

    """
    def __init__(self, config_file, message_content = True, reactions = True, version = 'production'):
        # Initialization code, e.g., authentication
        discord_details = get_discord_details(config_file)

        # Initialize variables
        if version == 'production':
            self.discord_token = discord_details['token']
        elif version == 'dev':
            self.discord_token = discord_details['dev_token']
        else:
            print("Invalid version!")
            return
        
        self.discord_dev_token = discord_details['dev_token']
        self.guild_id = discord_details['guild_id']
        self.admin_id = discord_details['admin_id']
        self.emoji_id = discord_details['emoji_id']
        self.command_prefix = discord_details['command_prefix']
        self.cid_mapper = ChannelMapper(discord_details = discord_details)
        self.raw_news_cid = self.cid_mapper.get_all_raw_cid()
        self.all_target_cid = self.cid_mapper.get_all_target_cid()
        self.monitor_cid = self.cid_mapper.get_id_from_name('MONITOR_CID')
        self.channel_quotas = discord_details['channel_quotas']

        # Initialize bots
        self.discord_client = self.create_client(message_content=message_content, reactions=reactions)
        self.discord_slash = app_commands.CommandTree(self.discord_client)

    async def fetch(self, channel_id, start_time=None, end_time=None, hours=None):
        if channel_id is None:
            if self.monitor_cid:
                channel_id = self.monitor_cid
            else:
                print("No channel ID specified!")
                return

        print("start fetching channel", channel_id)
        channel = await self.discord_client.fetch_channel(channel_id)
        if channel is None:
            print("Channel not found!")
            return

        if hours:
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours)

        print(channel_id, "Fetching messages from:", start_time, "to", end_time)

        if start_time and end_time:
            messages = [self.format_msg_embed(message) async for message in channel.history(after=start_time, before=end_time)]
            messages = "\n\n".join(messages)
        else:
            print("Invalid time range!")
            return
        return messages
    
    async def post(self, message, channel_id=None):
        # Code to post a message to Discord
        if channel_id is None:
            if self.monitor_cid:
                channel_id = self.monitor_cid
            else:
                print("No channel ID specified!")
                return
        print("start posting to channel", channel_id)
        channel = await self.discord_client.fetch_channel(channel_id)
        # channel = discord.utils.get(self.discord_client.get_all_channels(), id=channel_id)
        if channel is None:
            print("Channel not found!")
            return
        await channel.send(message)

    async def start(self):
        """Start the Discord bot."""
        self.discord_client = self.create_client()
        await self.discord_client.start()

    async def stop(self):
        """Stop the Discord bot."""
        await self.discord_client.close()
        self.discord_client = None

    def create_client(self, message_content = True, reactions = True):
        """Initialize the Discord bot."""
        intents = discord.Intents.default()  
        intents.message_content = message_content
        intents.reactions = reactions
        discord_client = discord.Client(intents=intents)
        return discord_client
        
    def create_slash_client(self, discord_client):
        """Initialize the Discord bot."""
        app_commands.CommandTree(discord_client)
        return app_commands
    
    def format_msg_embed(self, msg):   
        
        # Check if the message has any embeds
        if not msg.embeds:
            return ["The message does not contain any embeds."]
        
        # Create a list of formatted strings for each embed
        formatted_embeds = [
            f"[**{embed.title}**]({embed.url})\n{embed.description}\n\n_{embed.footer.text}_"
            if embed.footer and embed.footer.text else
            f"[**{embed.title}**]({embed.url})\n{embed.description}"
            for embed in msg.embeds
        ]

        # If there's only one embed, return its formatted string directly
        if len(formatted_embeds) == 1:
            return formatted_embeds[0]
        
        # If there are multiple embeds, join them with "\n\n" and return
        return "\n\n".join(formatted_embeds)


    def run(self):
        """Run the Discord bot."""
        self.discord_client.run(self.discord_token)
