from discopilot.bot.news import NewsBot
from discopilot.configuration_loader import ConfigurationLoader
import os

def main(config_file):

    # Read the configuration file
    # use loader
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
        'credentials_file': os.path.expanduser(config['Google']['GOOGLE_APPLICATION_CREDENTIALS']),
    }

    # Extract Discord details
    discord_details = {
        'token': config['Discord']['DISCORD_BOT_TOKEN'],
        'guild_id': config['Discord']['TS_GUILD_ID'],
        'admin_id': config['Discord']['ADMIN_ID'],
        'emoji_id': config['Discord']['SPECIFIC_REACTION'],
        'command_prefix': config['Discord']['COMMAND_PREFIX'],
        'channel_ids' : config['Discord_CID'],
        'channel_mapping': config['Channel_Mapping'],
        'chinese_mapping': config['Chinese_Mapping'],
        'channel_quotas': config['Channel_Quotas']
    }

    settings = config['Settings']

    # Initialize bots
    news_bot = NewsBot(twitter_creds = twitter_creds, 
                       discord_details = discord_details, 
                       google_translate_details = google_translate_details,
                       settings = settings)

    # Run the bots
    news_bot.run()

if __name__ == '__main__':
    import sys
    config_file = sys.argv[1] if len(sys.argv) == 2 else None
    main(config_file)
