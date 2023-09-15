import os
import tweepy
from discopilot.utils import get_twitter_creds, get_settings



class TwitterBot:
    """A bot that posts tweets to Twitter and interacts with the Twitter API.
    Example usage:
    
    config_file_path = os.getenv("DISCOPILOT_CONFIG")
    twitter_bot = TwitterBot(config_file_path)
    twitter_bot.post("Hello, world!")
    """
    def __init__(self, config_file = None, wait_on_rate = True):
        # Initialization code, e.g., authentication
        twitter_creds = get_twitter_creds(config_file)
        settings = get_settings(config_file)
        
        # Initialize variables
        self.consumer_key = twitter_creds['consumer_key']
        self.consumer_secret = twitter_creds['consumer_secret']
        self.access_token = twitter_creds['access_token']
        self.access_token_secret = twitter_creds['access_token_secret']
        self.wait_on_rate = wait_on_rate
        self.twitter_client = self.create_client()


    def create_client(self):
        """Create a Twitter client."""
        twitter_client = tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret = self.consumer_secret,
            access_token = self.access_token,
            access_token_secret = self.access_token_secret
            #wait_on_rate = self.wait_on_rate
        )
        return twitter_client
    # ... other methods related to Twitter interactions

    def post(self, tweet_text):
        """Post a tweet to Twitter."""
        print(f"Tweeted: {tweet_text}")
        self.twitter_client.create_tweet(text = tweet_text) 

