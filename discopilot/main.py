import os

import discord
from os import environ


# Twitter Credentials
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# Twiiter client
twitter_client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

# Discord Credentials
DISCORD_BOT_TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

# Discord channel to listen to
INTERNAL_NEWS_CID = os.environ.get('INTERNAL_NEWS_CID')
CN_CID = os.environ.get('CN_CID')
EN_CID = os.environ.get('EN_CID')

#intents = discord.Intents(messages = True)
intents = discord.Intents.default()  
intents.message_content = True
intents.reactions = True
# Discord client
discord_client = discord.Client(intents=intents)

# google translate
trans_client = create_translate_client()

# Project
PROJECT_ID = os.environ.get('PROJECT_ID')
assert PROJECT_ID
PARENT = f"projects/{PROJECT_ID}"


last_seen_id = None
# Store the timestamp of the last seen entry
last_seen_timestamp = None


# Cooldown variable to handle rate limiting
cooldown_time = None


# on_message: This event triggers when the bot sees english news and translate it to chinese and shared to the Chibnese channel.
# this will get ready to be published on weibo
@discord_client.event
async def on_message(message):
    global cooldown_time
    # Check if the message is from the bot itself
    if not message.author.bot:
        return

    # Check for the specific channel you want to listen to
    if str(message.channel.id) != INTERNAL_NEWS_CID:
        return
    
    # Check for cooldown period
    if cooldown_time and time.time() < cooldown_time:
        print("In cooldown period, exiting.")
        return

    # Check if the message contains any embeds
    if message.embeds:
        for embed in message.embeds:  # Loop through all embeds

            # breakdown from list to single item to public news room
            en_channel = await discord_client.fetch_channel(EN_CID)
            await en_channel.send(embed = embed)
            
            # Translate the embed title and description to Chinese
            embed_cn_title = translate_to_chinese(str(embed.title))
            embed_cn_description = translate_to_chinese(str(embed.description)) 
            #tweet_content_cn = f"{embed_cn_title} {embed.url}"
            #print("tweet_cn:" + tweet_content_cn)
            
            # Generate Chinese embed (creating a copy to avoid modifying the original)
            embed_cn = embed.copy()
            embed_cn.title = embed_cn_title
            embed_cn.description = embed_cn_description     
            cn_channel = await discord_client.fetch_channel(CN_CID)
            await cn_channel.send(embed = embed_cn)
    else:
        return
  
# when liked, pushed to twitter, so control quality and #
ADMIN_ID = os.environ.get('ADMIN_ID')  # Replace with your Discord user ID
#SPECIFIC_REACTION = '👍'  # Change to the specific reaction you want to detect
SPECIFIC_REACTION = 'newspaper2'
        
@discord_client.event
async def on_raw_reaction_add(payload):
    print("on_raw_reaction_add")
    if str(payload.user_id) == ADMIN_ID and str(payload.emoji) == SPECIFIC_REACTION:

        if(str(payload.channel_id) != EN_CID):
            return
        
        # Get the channel and message IDs from the payload
        channel = discord_client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message.embeds:
            for embed in message.embeds:
                tweet_content = f"{embed.title} {embed.url}"
                try:
                    print("tweet:" + tweet_content)
                    post_to_twitter(tweet_content)
                except tweepy.TweepyException as e:
                 # Check if the error is related to rate limiting (status code 429)
                    if e.api_codes == 429:
                        print("Too many requests, entering cooldown period.")
                        cooldown_time = time.time() + 5 * 60 * 60 # 5 hours from now
                # Check if the error is related to duplicate content (status code 187)
                 #   elif e.api_codes == 187:
                  #      print("Duplicate content, ignoring this message.")
                    else:
                        print(f"An error occurred: {e}")
        else:
            return
    else:
        return
    
    

discord_client.run(DISCORD_BOT_TOKEN)



