import tweepy
from discopilot.configuration_loader import ConfigurationLoader

config = ConfigurationLoader.load_config()


# Option 1: doesn't work for v2 API now
twitter_client = tweepy.Client(
        consumer_key = config['Twitter']['CONSUMER_KEY'],
        consumer_secret = config['Twitter']['CONSUMER_SECRET'],
        access_token = config['Twitter']['ACCESS_TOKEN'],
        access_token_secret = config['Twitter']['ACCESS_TOKEN_SECRET'],
        bearer_token = config['Twitter']['BEARER_TOKEN'],
        wait_on_rate_limit = True
    )

auth = tweepy.OAuth1UserHandler(
    consumer_key = config['Twitter']['CONSUMER_KEY'],  
    consumer_secret = config['Twitter']['CONSUMER_SECRET'],
    access_token =  config['Twitter']['ACCESS_TOKEN'], 
    access_token_secret = config['Twitter']['ACCESS_TOKEN_SECRET']
)

api = tweepy.API(auth)
tweet_text = "This is a test tweet using Tweepy!"
tweet = api.create_tweet(status=tweet_text)

api.rate_limit_status()['resources']['statuses']
tweepy.Client(retu)
tresponse = twitter_client.create_tweet(text = "test") 
tresponse.headers
dir(tresponse)

auth = tweepy.OAuthHandler(twitter_client.consumer_key, twitter_client.consumer_secret)
auth.set_access_token(twitter_client.access_token, twitter_client.access_token_secret)
api = tweepy.API(auth)
rate_limit_status = api.rate_limit_status()
tweet_post_limit = rate_limit_status['resources']['statuses']['/statuses/update']['remaining']

api = tweepy.API(auth)

# Option 2: 

import requests
bearer = twitter_client.bearer_token

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer}"
    return r


params = {"x-rate-limit-remaining": "search"}
params = {"query": "search"}
    
response = requests.get("https://api.twitter.com/2/tweets/search/recent", params=params, auth=bearer_oauth)
response.headers