from datetime import datetime

import discord
from discord import app_commands, tasks
import tweepy

from discopilot.channel_mapper import ChannelMapper
from discopilot.ai.c3po import c3po

import os
import random
import asyncio




class Hedwig:
    """
    A bot that interacts with Twitter, Google Translate, and Discord.
    """

    def __init__(self, config_file):
        """Initialize the NewsBot with credentials for Twitter, Discord, and Google 
        Translate."""
        
        # Read the configuration file
        config = ConfigurationLoader.load_config(config_file)

        # Extract information
        twitter_creds = get_twitter_creds(config)
        google_translate_details = get_google_translate_details(config)
        discord_details = get_discord_details(config)
        settings = config['Settings']

        # Twitter rate limit control
        # Twitter credentials
        self.consumer_key = twitter_creds['consumer_key']
        self.consumer_secret = twitter_creds['consumer_secret']
        self.access_token = twitter_creds['access_token']
        self.access_token_secret = twitter_creds['access_token_secret']

        # Discord 
        self.discord_token = discord_details['token']
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

        # Google Translate details
        self.project_id = google_translate_details['project_id']
        self.credentials_file = google_translate_details['credentials_file']

        # Initialize Twitter client
        self.twitter_client = self.initialize_twitter_client()
       

        # Initialize Google Translate client c3po
        self.c3po = c3po(engine="google", project_id=self.project_id, credentials_file=self.credentials_file)

        # Initialize Discord client
        def create_discord_client(message_content = True, reactions = True):
            """Initialize the Discord bot."""
            intents = discord.Intents.default()  
            intents.message_content = message_content
            intents.reactions = reactions
            discord_client = discord.Client(intents=intents)
            return discord_client
        
        def create_discord_slash_client(discord_client):
            """Initialize the Discord bot."""
            app_commands.CommandTree(discord_client)
            return app_commands

        self.discord_client = create_discord_client()
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
        
     

    def setup_discord_events(self):
        """Set up Discord events for handling messages and reactions."""

        @self.discord_client.event
        async def on_ready():
            self.monitor_channel = await self.discord_client.fetch_channel(self.monitor_cid)
            await self.monitor_channel.send("Hello, Hedwig is online!")
            print(f'Logged in as {self.discord_client.user.name}({self.discord_client.user.id})')

        @tasks.loop(count=1)
        async def delayed_tweet(self, msg, embed, en_cid):
            """A loop that runs once to delay tweeting."""
            current_hour = datetime.now().hour
            

            if current_hour in self.high_freq_hrs:
                sleep_time = random.randint(5, 10) * 60  # 5 to 10 minutes
            else:
                sleep_time = random.randint(30, 60) * 60  # 30 to 60 minutes

            await asyncio.sleep(sleep_time)

            self.check_and_reset_tweet_count()
            # check quotas
            if self.global_tweet_count > self.max_tweet_per_day:
                self.monitor_channel.send("tweet limits rate exceeded")
                return

            en_name = self.cid_mapper.get_name_from_id(en_cid)

            if self.channel_tweet_count[en_name] < int(self.channel_quotas[en_name]):
                print("Bot tweeting")

                tweet_content = f"{embed.title} {embed.url}"
                self.post_to_twitter(tweet_content)

                # quota update
                self.global_tweet_count += 1
                self.channel_tweet_count[en_name] += 1
                self.save_tweet_count()
                
                # Add reaction to the message
                await msg.add_reaction(self.emoji_id)

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
                    embed_cn_title = self.c3po.translate_to_chinese(str(embed.title))
                    embed_cn_description = self.c3po.translate_to_chinese(str(embed.description)) 
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
                    await self.delayed_tweet(embed, msg = en_msg, embed = embed, en_cid = en_cid)              
            else:
                return

        @self.discord_client.event
        async def on_raw_reaction_add(payload):

            if str(payload.user_id) == self.admin_id and str(payload.emoji) == self.emoji_id:

                self.check_and_reset_tweet_count()
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

    def post_to_twitter(self, tweet_text):
        """Post a tweet to Twitter."""
        print(f"Tweeted: {tweet_text}")
        self.twitter_client.create_tweet(text = tweet_text) 
    
    async def fetch(self, channel_id, start_time=None, end_time=None, hours=None):
        """Fetches messages from a Discord channel based on the given time range."""



    # Hedwig: future action Hedwig.deliver Hedwig.hoot
    
    def hoot(self, channel_id):
        pass

    # Hedwig's main method
    def fly(self, version = "production"):
        """Start the Hedwig news bot."""
        if version == "production":
            self.discord_client.run(self.discord_token)
        elif version == "development":
            self.discord_client.run(self.discord_dev_token)
