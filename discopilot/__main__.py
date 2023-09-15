from discopilot.bot.news import NewsBot
from discopilot.configuration_loader import ConfigurationLoader
from discopilot.utils import get_twitter_creds, get_google_translate_details, get_discord_details


def hedwig(config_file, version = "production"):
    # Initialize bots
    hedwig_bot  = Hedwig(config_file)
    # Run the bots
    hedwig_bot.fly(version = version)

if __name__ == '__main__':
    import sys
    config_file = sys.argv[1] if len(sys.argv) == 2 else None
    hedwig(config_file)
