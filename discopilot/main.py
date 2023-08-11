import os

import discord
from os import environ



# Project
PROJECT_ID = os.environ.get('PROJECT_ID')

# Discord channel to listen to
INTERNAL_NEWS_CID = os.environ.get('INTERNAL_NEWS_CID')
CN_CID = os.environ.get('CN_CID')
EN_CID = os.environ.get('EN_CID')

# Twitter Credentials
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
  
# when liked, pushed to twitter, so control quality and #
ADMIN_ID = os.environ.get('ADMIN_ID')  # Replace with your Discord user ID
#SPECIFIC_REACTION = '👍'  # Change to the specific reaction you want to detect
SPECIFIC_REACTION = 'newspaper2'

# Twiiter client
twitter_client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

# Discord Credentials
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

twitter_creds = {
            'consumer_key': CONSUMER_KEY,
            'consumer_secret': CONSUMER_SECRET,
            'access_token': ACCESS_TOKEN,
            'access_token_secret': ACCESS_TOKEN_SECRET
        }

bot = NewsBot(twitter_creds = twitter_creds, discord_token = DISCORD_BOT_TOKEN, 
              google_project_id = PROJECT_ID, internal_channel_id = INTERNAL_NEWS_CID, 
              channel_id_cn = CN_CID, channel_id_en = EN_CID, admin_id = ADMIN_ID, emoji_id = EMOJI_ID)

bot.run()






# Cooldown variable to handle rate limiting

