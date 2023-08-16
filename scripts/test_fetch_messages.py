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

#t = threading.Thread(target=news_bot.run)
#t.start()
# asyncio.run(news_bot.run())
# asyncio.run(news_bot.fetch_messages(channel_id=discord_details['channel_id_en'], hours=24))
#loop = asyncio.get_event_loop()
#loop.run_until_complete(news_bot.fetch_messages(channel_id=discord_details['channel_id_en'], hours=24)) 
task = asyncio.create_task(news_bot.run())
messages = await news_bot.fetch_messages(channel_id=discord_details['channel_id_en'], hours=24)
print(messages)

print(msg)

import threading
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(news_bot.run())

thread = threading.Thread(target=run_bot)
thread.start()

async def main_test():
    await asyncio.wait_for(news_bot.fetch_messages(channel_id=discord_details['channel_id_en'], hours=24), timeout=10)

results = asyncio.run(main_test())


async def fetch_messages(self, channel_id, start_time=None, end_time=None, hours=None):
          
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