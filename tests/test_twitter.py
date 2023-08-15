import tweepy
import configparser

config = configparser.ConfigParser()
config_file = "/Users/tengfei/Code/key/config.ini"
config.read(config_file)

twitter_client = tweepy.Client(
        consumer_key = config['Twitter']['CONSUMER_KEY'],
        consumer_secret = config['Twitter']['CONSUMER_SECRET'],
        access_token = config['Twitter']['ACCESS_TOKEN'],
        access_token_secret = config['Twitter']['ACCESS_TOKEN_SECRET'],
        wait_on_rate_limit = True
    )

# don't know how to get rate limit yet, maybe 