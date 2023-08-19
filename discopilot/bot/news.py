import time
from datetime import datetime, timedelta

import discord
from discord import app_commands
import tweepy

from discopilot.bot.translate import TranslateBot
from discopilot.google.google_translate import create_translate_client



class NewsBot:
    """
    A bot that interacts with Twitter, Google Translate, and Discord.

    Attributes:
        twitter_client (tweepy.API): A Tweepy client for interacting with Twitter.
        translate_client (translate.Client): A Google Cloud Translate client.
        discord_client (discord.Client): A Discord bot.

    Example:
        twitter_creds = {
            'consumer_key': 'key',
            'consumer_secret': 'secret',
            'access_token': 'token',
            'access_token_secret': 'token_secret',
        }
        discord_token = 'discord_token'
        google_project_id = 'projects/my_project/locations/my_location'
        bot = NewsBot(twitter_creds, discord_token, google_project_id)
        bot.run()
    """

    def __init__(self, twitter_creds, discord_details, google_translate_details):
        """Initialize the NewsBot with credentials for Twitter, Discord, and Google 
        Translate."""
        
        # Twitter cooldown time
        self.cooldown_time = None

        # Twitter credentials
        self.consumer_key = twitter_creds['consumer_key']
        self.consumer_secret = twitter_creds['consumer_secret']
        self.access_token = twitter_creds['access_token']
        self.access_token_secret = twitter_creds['access_token_secret']

        # Discord 
        self.discord_token = discord_details['token']
        self.guild_id = discord_details['guild_id']
        self.internal_news_cid = discord_details['internal_news_cid']
        self.channel_id_cn = discord_details['channel_id_cn']
        self.channel_id_en = discord_details['channel_id_en']
        self.admin_id = discord_details['admin_id']
        self.emoji_id = discord_details['emoji_id']
        self.command_prefix = discord_details['command_prefix']

        # Initialize Twitter client
        self.twitter_client = self.initialize_twitter_client()

        # Initialize Google Translate client
        self.translate_bot = TranslateBot(project_id = google_translate_details['project_id'], 
                                          credentials_file = google_translate_details['credentials_file'])

        # Initialize Discord bot
        self.intents = discord.Intents.default()  
        self.intents.message_content = True
        self.intents.reactions = True
        self.discord_client = self.initialize_discord_client()
        self.tree = app_commands.CommandTree(self.discord_client)

        # setup discord event
        self.setup_discord_events()

        # setup discord slash commands
        self.setup_discord_slash_commands()
    
    def initialize_discord_client(self):
        """Initialize the Discord bot."""
        discord_client = discord.Client(intents = self.intents)
        return discord_client
        

    def setup_discord_events(self):
        """Set up Discord events for handling messages and reactions."""

        @self.discord_client.event
        async def on_message(message):
            print("on_message")
            # Check if the message is from the bot itself
            if not message.author.bot:
                return

            print("message.channel.id: " + str(message.channel.id)) 
            # Check for the specific channel you want to listen to
            if str(message.channel.id) != self.internal_news_cid:
                return
            print("message.embeds: " + str(message.embeds))
            # Check if the message contains any embeds
            if message.embeds:
                for embed in message.embeds:  # Loop through all embeds

                    # breakdown from list to single item to public news room
                    en_channel = await self.discord_client.fetch_channel(self.channel_id_en)
                    await en_channel.send(embed = embed)
                    
                    # Translate the embed title and description to Chinese
                    embed_cn_title = self.translate_bot.translate_to_chinese(str(embed.title))
                    embed_cn_description = self.translate.translate_to_chinese(str(embed.description)) 
        
                    # Generate Chinese embed (creating a copy to avoid modifying the original)
                    embed_cn = embed.copy()
                    embed_cn.title = embed_cn_title
                    embed_cn.description = embed_cn_description     
                    cn_channel = await self.discord_client.fetch_channel(self.channel_id_cn)
                    await cn_channel.send(embed = embed_cn)
            else:
                return

        @self.discord_client.event
        async def on_raw_reaction_add(payload):
            print("on_raw_reaction_add")
            
            if str(payload.user_id) == self.admin_id and str(payload.emoji) == self.emoji_id:
                print(str(payload.emoji) + "matched")
                return
                if(str(payload.channel_id) != self.channel_id_en):
                    return
                
                # Get the channel and message IDs from the payload
                channel = self.discord_client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                if message.embeds:
                    for embed in message.embeds:
                        tweet_content = f"{embed.title} {embed.url}"
                        self.post_to_twitter(tweet_content)
                else:
                    return
            else:
                return 

    def setup_discord_slash_commands(self):
        @self.tree.command(name = "hello", description = "test hello", guild = discord.Object(id=self.guild_id)) 
        async def hello(interaction):
            await interaction.response.send_message("Hello!")


    def initialize_twitter_client(self, wait_on_rate_limit  = True):
        """Initialize the Twitter client using Tweepy."""
        twitter_client = tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret = self.consumer_secret,
            access_token = self.access_token,
            access_token_secret = self.access_token_secret,
            wait_on_rate_limit  = wait_on_rate_limit 
        )
        return twitter_client

    def initialize_google_translate_client(self):
        """Initialize the Google Translate client."""
        translate_client = create_translate_client()
        return translate_client

    def post_to_twitter(self, tweet_text):
        """Post a tweet to Twitter."""
        self.twitter_client.create_tweet(text = tweet_text) 

    async def fetch_messages(self, channel_id, start_time=None, end_time=None, hours=None):
        """Fetches messages from a Discord channel based on the given time range."""
        
        channel = await self.discord_client.fetch_channel(channel_id)

        if channel is None:
            print("Channel not found!")
            return

        # If 'hours' is specified, override the start and end times.
        if hours:
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours)
        
        print("start_time: " + str(start_time))
        print("end_time: " + str(end_time))

        # Filter the messages based on the start and end times.
        if start_time and end_time:
            messages = await channel.history(after=start_time, before=end_time).flatten()
        else:
            messages = await channel.history().flatten()

        return messages


    def run(self):
        """Start the Discord bot."""
        self.discord_client.run(self.discord_token)
