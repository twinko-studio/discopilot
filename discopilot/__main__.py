from discopilot.bot.news import NewsBot
from discopilot.configuration_loader import ConfigurationLoader
from discopilot.utils import get_twitter_creds, get_google_translate_details, get_discord_details


def hedwig(config_file, version = "production"):

    # Read the configuration file
    # use loader
    config = ConfigurationLoader.load_config(config_file)
    # Extract Twitter credentials
    twitter_creds = get_twitter_creds(config)

    # Extract Google Translate details
    google_translate_details = get_google_translate_details(config)

    # Extract Discord details
    discord_details = get_discord_details(config)

    settings = config['Settings']

    # Initialize bots
    hedwig_bot  = Hedwig(config))

    # Run the bots
    hedwig_bot.fly(version = version)

if __name__ == '__main__':
    import sys
    config_file = sys.argv[1] if len(sys.argv) == 2 else None
    hedwig(config_file)
