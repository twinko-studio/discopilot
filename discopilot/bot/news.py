from datetime import datetime, timedelta

import discord
from discord import app_commands
import tweepy

from discopilot.bot.translate import TranslateBot
from discopilot.google.google_translate import create_translate_client
from discopilot.channel_mapper import ChannelMapper

import os
import random
import asyncio



class NewsBot:
    """
    A bot that interacts with Twitter, Google Translate, and Discord.
    """

    def __init__(self, twitter_creds, discord_details, google_translate_details, settings):
        """Initialize the NewsBot with credentials for Twitter, Discord, and Google 
        Translate."""
        
        # Twitter rate limit control


        # Twitter credentials
        self.consumer_key = twitter_creds['consumer_key']
        self.consumer_secret = twitter_creds['consumer_secret']
        self.access_token = twitter_creds['access_token']
        self.access_token_secret = twitter_creds['access_token_secret']

     

        # Discord 
        self.discord_token = discord_details['token']
        self.guild_id = discord_details['guild_id']
        self.admin_id = discord_details['admin_id']
        self.emoji_id = discord_details['emoji_id']
        self.command_prefix = discord_details['command_prefix']
        self.cid_mapper = ChannelMapper(discord_details = discord_details)
        self.raw_news_cid = self.cid_mapper.get_all_raw_cid()
        self.all_target_cid = self.cid_mapper.get_all_target_cid()
        self.monitor_cid = self.cid_mapper.get_id_from_name('MONITOR_CID')
        self.channel_quotas = discord_details['channel_quotas']

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

      

        # settings
        self.high_freq_hrs = [int(hour) for hour in settings['HIGH_FREQUENCY_HOURS'].split(',')]
      
        self.tweet_count_file = os.path.expanduser(settings['TWEET_COUNT_FILE'])
        self.max_tweet_per_day = int(settings['MAX_TWEET_PER_DAY'])
        self.load_tweet_count()
        
     
    
    def initialize_discord_client(self):
        """Initialize the Discord bot."""
        discord_client = discord.Client(intents = self.intents)
        return discord_client
        

    def setup_discord_events(self):
        """Set up Discord events for handling messages and reactions."""

        @self.discord_client.event
        async def on_ready():
            self.monitor_channel = await self.discord_client.fetch_channel(self.monitor_cid)
            await self.monitor_channel.send("Hello, the news bot is back online!")
            print(f'Logged in as {self.discord_client.user.name}({self.discord_client.user.id})')

        @self.discord_client.event
        async def on_message(message):

            # Check if the message is from the bot itself
            if not message.author.bot:
                return

            cid_name = self.cid_mapper.get_name_from_id(message.channel.id)

            # Check for the specific channel you want to listen to
            if cid_name not in self.raw_news_cid: 
                return
          
            # Check if the message contains any embeds
            if message.embeds:
                for embed in message.embeds:  # Loop through all embeds
                    
                    # breakdown from list to single item to public news room
                    en_cid = self.cid_mapper.get_target_channel_id(message.channel.id)
                    en_channel = await self.discord_client.fetch_channel(en_cid)

                    en_msg = await en_channel.send(embed = embed)
                    
                    # Translate the embed title and description to Chinese
                    embed_cn_title = self.translate_bot.translate_to_chinese(str(embed.title))
                    embed_cn_description = self.translate_bot.translate_to_chinese(str(embed.description)) 
                    # Generate Chinese embed (creating a copy to avoid modifying the original)
                    embed_cn = embed.copy()
                    embed_cn.title = embed_cn_title
                    embed_cn.description = embed_cn_description     
                    # get target chinese channel id
                    cn_cid = self.cid_mapper.get_chinese_channel_id(message.channel.id)
                    cn_channel = await self.discord_client.fetch_channel(cn_cid)
                    await cn_channel.send(embed = embed_cn)

                    ## Bot posting tweets, so need to check rate limit, quotas, etc.

                    # sleep for a random amount of time for posting to twitter at right time
                    current_hour = datetime.now().hour
                    if current_hour in self.high_freq_hrs:
                        sleep_time = random.randint(5, 10) * 60  # 5 to 10 minutes
                    else:
                        sleep_time = random.randint(30, 60) * 60  # 30 to 60 minutes
                
                    await asyncio.sleep(sleep_time)

                    # Post the tweet to Twitter 
                    # set a rate limit control, via a global counter, 
                    # every 24 hours reset to 0, 40 tweets per day at most
                    if self.global_tweet_count > self.max_tweet_per_day:
                        self.monitor_channel.send("tweet limits rate exceeded")
                        return

                    en_name = self.cid_mapper.get_name_from_id(en_cid)
                    
                    if self.channel_tweet_count[en_name] < self.channel_quotas[en_name]:
                        print("Bot tweeting")
                         # check tweets count first
                        self.check_and_reset_tweet_count()
                        
                        tweet_content = f"{embed.title} {embed.url}"
                        self.post_to_twitter(tweet_content)
                 
                        self.global_tweet_count += 1
                        self.channel_tweet_count[en_name] += 1
                        self.save_tweet_count()
                        
                        # Add reaction to the message
                        await en_msg.add_reaction(self.emoji_id)

            else:
                return

        @self.discord_client.event
        async def on_raw_reaction_add(payload):

            if str(payload.user_id) == self.admin_id and str(payload.emoji) == self.emoji_id:

                # only listen to the specific news channel
                cid_name = self.cid_mapper.get_name_from_id(payload.channel_id)

                if cid_name not in self.all_target_cid:
                    return
                
                # check daily limits of tweets
                if self.global_tweet_count > self.max_tweet_per_day:
                    return

                # Get the channel and message IDs from the payload
                channel = self.discord_client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                if message.embeds:
                    for embed in message.embeds:
                        # check tweets count first
                        self.check_and_reset_tweet_count()
                        tweet_content = f"{embed.title} {embed.url}"
                        self.post_to_twitter(tweet_content)
                         # save count
                        self.global_tweet_count += 1
                        self.channel_tweet_count[cid_name] += 1
                        self.save_tweet_count()
                else:
                    ## update this to monitor channel.
                    self.monitor_channel.send("tweet limits rate exceeded")
                    return
            else:
                return 

          # establish monitor channe

        

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

    def load_tweet_count(self):
        # Check if today's date is stored in the tweet count file
        current_date = datetime.now().date().isoformat()

        if os.path.exists(self.tweet_count_file):
            with open(self.tweet_count_file, 'r') as f:
                stored_data = f.read().splitlines()
                # Check if the stored date matches the current date
                if stored_data[0] == current_date:
                    self.date = stored_data[0]
                    self.global_tweet_count = int(stored_data[1])
                    self.channel_tweet_count = {line.split(":")[0]: int(line.split(":")[1]) for line in stored_data[2:]}
                else:
                    # If the stored date doesn't match, reset everything
                    self.date = current_date
                    self.global_tweet_count = 0
                    self.channel_tweet_count = {channel: 0 for channel in self.channel_quotas.keys()}

        else:
            self.date = datetime.now().date().isoformat()
            self.global_tweet_count = 0
            self.channel_tweet_count = {channel: 0 for channel in self.channel_quotas.keys()}


    def save_tweet_count(self):
        print("save tweet count")
        with open(self.tweet_count_file, 'w') as f:
            f.write(f"{self.date}\n{self.global_tweet_count}\n")
            for channel, count in self.channel_tweet_count.items():
                f.write(f"{channel}:{count}\n")

    def check_and_reset_tweet_count(self):
        current_date = datetime.now().date().isoformat()
        if self.date != current_date:
            self.date = current_date
            self.global_tweet_count = 0
            self.channel_tweet_count = {channel: 0 for channel in self.channel_quotas.keys()}


    def initialize_google_translate_client(self):
        """Initialize the Google Translate client."""
        translate_client = create_translate_client()
        return translate_client

    def post_to_twitter(self, tweet_text):
        """Post a tweet to Twitter."""
        print(f"Tweeted: {tweet_text}")
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
