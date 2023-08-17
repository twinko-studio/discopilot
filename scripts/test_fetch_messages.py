import os
import discord
import asyncio
from datetime import datetime, timedelta
from discopilot.bot.news import NewsBot
from discopilot.configuration_loader import ConfigurationLoader


# Read the configuration file
config_file = os.environ.get('DISCOPILOT_CONFIG')
config = ConfigurationLoader.load_config(config_file)

# Extract Twitter credentials
twitter_creds = {
    'consumer_key': config['Twitter']['CONSUMER_KEY'],
    'consumer_secret': config['Twitter']['CONSUMER_SECRET'],
    'access_token': config['Twitter']['ACCESS_TOKEN'],
    'access_token_secret': config['Twitter']['ACCESS_TOKEN_SECRET'],
}

# Extract Google Translate details
google_translate_details = {
    'project_id': config['Google']['PROJECT_ID'],
    'credentials_file': config['Google']['GOOGLE_APPLICATION_CREDENTIALS'],
}

# Extract Discord details
discord_details = {
    'token': config['Discord']['DISCORD_BOT_TOKEN'],
    'internal_news_cid': config['Discord']['INTERNAL_NEWS_CID'],
    'channel_id_cn': config['Discord']['CN_CID'],
    'channel_id_en': config['Discord']['EN_CID'],
    'admin_id': config['Discord']['ADMIN_ID'],
    'emoji_id': config['Discord']['SPECIFIC_REACTION']
}

# Initialize bots
news_bot = NewsBot(twitter_creds = twitter_creds, 
                    discord_details = discord_details, 
                    google_translate_details = google_translate_details)

# Run the bots
#news_bot.run()

