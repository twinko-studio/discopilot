import tweepy
import discord
from discopiot.google.google_translate import create_translate_client, traslate_to_chinese
from disocpiot.bot.translate import TranslateBot


class NewsBot:
    """
    A bot that interacts with Twitter, Google Translate, and Discord.

    Attributes:
        twitter_client (tweepy.API): A Tweepy client for interacting with Twitter.
        translate_client (translate.Client): A Google Cloud Translate client.
        discord_client (discord.Client): A Discord client.

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
        """Initialize the NewsBot with credentials for Twitter, Discord, and Google Translate."""
        
        # Twitter cooldown time
        cooldown_time = None

        # Twitter credentials
        self.consumer_key = twitter_creds['consumer_key']
        self.consumer_secret = twitter_creds['consumer_secret']
        self.access_token = twitter_creds['access_token']
        self.access_token_secret = twitter_creds['access_token_secret']

        # Discord 
        self.discord_token = discord_details['discord_token']
        self.internal_channel_id = discord_details['internal_channel_id']
        self.channel_id_cn = discord_details['channel_id_cn']
        self.channel_id_en = discord_details['channel_id_en']
        self.admin_id = discord_details['admin_id']
        self.emoji_id = discord_details['emoji_id']

        # Google translate
        self.google_project_id = google_translate_details['google_project_id']

        # Initialize Twitter client
        self.twitter_client = self.initialize_twitter_client()

        # Initialize Google Translate client
        self.translate_bot = TranslateBot(self.google_project_id)

        # Initialize Discord client
        self.intents = discord.Intents.default()  
        self.intents.message_content = True
        self.intents.reactions = True
        self.discord_client = self.initialize_discord_client()

        # Set up Discord bot action status
        self.on_message_check = True
        self.on_reaction_add_check = True

        # Set up Discord events
        self.setup_discord_events()
    
    def initialize_discord_client(self):
        """Initialize the Discord client."""
        discord_client = discord.Client(intents=self.intents)
        return discord_client

    def initialize_twitter_client(self):
        """Initialize the Twitter client using Tweepy."""
        twitter_client = tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret = self.consumer_secret,
            access_token = self.access_token,
            access_token_secret = self.access_token_secret
        )
        return twitter_client

    def initialize_google_translate_client(self):
        """Initialize the Google Translate client."""
        translate_client = create_translate_client()
        return translate_client
    
    def setup_discord_events(self):
        """Set up Discord events for handling messages and reactions."""
        # ... (same as before)
        @self.discord_client.event
        async def on_message(message):
        global cooldown_time
        # Check switch
        if not self.on_message_check:
            return
        # Check if the message is from the bot itself
        if not message.author.bot:
            return

        # Check for the specific channel you want to listen to
        if str(message.channel.id) != self.internal_channel_id:
            return
        
        # Check for cooldown period
        if cooldown_time and time.time() < cooldown_time:
            print("In cooldown period, exiting.")
            return

        # Check if the message contains any embeds
        if message.embeds:
            for embed in message.embeds:  # Loop through all embeds

                # breakdown from list to single item to public news room
                en_channel = await discord_client.fetch_channel(self.channel_id_en)
                await en_channel.send(embed = embed)
                
                # Translate the embed title and description to Chinese
                embed_cn_title = self.translate_bot.translate_to_chinese(str(embed.title))
                embed_cn_description = self.translate.translate_to_chinese(str(embed.description)) 
       
                # Generate Chinese embed (creating a copy to avoid modifying the original)
                embed_cn = embed.copy()
                embed_cn.title = embed_cn_title
                embed_cn.description = embed_cn_description     
                cn_channel = await discord_client.fetch_channel(self.channel_id_cn)
                await cn_channel.send(embed = embed_cn)
        else:
            return

        @self.discord_client.event
        async def on_raw_reaction_add(payload):
            if not self.on_reaction_add_check:
                return
                
            print("on_raw_reaction_add")
            if str(payload.user_id) == self.admin_id and str(payload.emoji) == self.emoji_id:

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

    def post_to_twitter(self, tweet_text):
        """
        Post a tweet to Twitter.

        Args:
            tweet_text (str): The text of the tweet to post.

        Example:
            bot.post_to_twitter("Hello, Twitter!")
        """
        try:
            print("tweet:" + tweet_content)
            self.twitter_client.create_tweet(text = tweet_text)
        except tweepy.TweepyException as e:
            # Check if the error is related to rate limiting (status code 429)
            if e.api_codes == 429:
                print("Too many requests, entering cooldown period.")
                self.cooldown_time = time.time() + 5 * 60 * 60 # 5 hours from now
            else:
                print(f"An error occurred: {e}")
        

    def run(self):
        """Start the Discord bot."""
        self.discord_client.run(self.discord_token)
