import configparser
from discopilot.bot.news import NewsBot
from discopilot.bot.translate import TranslateBot
from discopilot.configuration_loader import ConfigurationLoader
import os

def main(config_file):

    if config_file is None:
        # try to parse from env
        config_file = os.environ.get('DISCOPILOT_CONFIG')
        if config_file is None:
            raise ValueError("config_file cannot be None: \\ Usage: python mypackage config.ini or set up DISCOPILOT_CONFIG environment varaible")
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
        'credentials_file': config['Google']['GOOGLE_APPLICATION_CREDENTIALS'],
    }

    # Extract Discord details
    discord_details = {
        'token': config['Discord']['DISCORD_BOT_TOKEN'],
        'internal_news_cid': config['Discord']['INTERNAL_NEWS_CID'],
        'channel_id_cn': config['Discord']['CN_CID'],
        'channel_id_en': config['Discord']['EN_CID'],
        'admin_id': config['Discord']['ADMIN_ID'],
        'emoji_id': config['Discord']['SPECIFIC_REACTION'],
        'command_prefix': config['Discord']['COMMAND_PREFIX']
    }

    # Initialize bots
    news_bot = NewsBot(twitter_creds = twitter_creds, 
                       discord_details = discord_details, 
                       google_translate_details = google_translate_details)

    # Run the bots
    news_bot.run()

if __name__ == '__main__':
    import sys
    config_file = sys.argv[1] if len(sys.argv) == 2 else None
    main(config_file)
