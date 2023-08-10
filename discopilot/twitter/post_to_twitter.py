import tweepy

# Post to twitter
def post_to_twitter(tweet, consumer_key, consumer_secret, access_token, access_token_secret):
    """ Post to twitter

    Args:
        tweet (str): The tweet to post
        consumer_key (str): Twitter consumer key
        consumer_secret (str): Twitter consumer secret
        access_token (str): Twitter access token
        access_token_secret (str): Twitter access token secret
        
    Returns:
        Response from twitter

    Raises:
        tweepy.TweepyException: an exception from tweepy

    Examples:
    
    """
    twitter_client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret = consumer_secret,
        access_token = access_token,
        access_token_secret = access_token_secret
    )
    print("tweet:" + tweet)
    twitter_client.create_tweet(text = tweet)
 
    