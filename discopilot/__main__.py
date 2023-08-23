from discopilot.bot.news import NewsBot
from discopilot.configuration_loader import ConfigurationLoader
from discopilot.utils import twitter_creds, google_translate_details, discord_details


def main(config_file):

    # Read the configuration file
    # use loader
    config = ConfigurationLoader.load_config(config_file)

    # Extract Twitter credentials
    twitter_creds = twitter_creds(config)

    # Extract Google Translate details
    google_translate_details = google_translate_details(config)

    # Extract Discord details
    discord_details = discord_details(config)

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
