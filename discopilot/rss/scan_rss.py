def scan_rss(data, context):
    global last_seen_timestamp
    
    # Decode the data payload from Pub/Sub message
    message = base64.b64decode(data['data']).decode('utf-8')
    feed_url = message
    
    feed = feedparser.parse(feed_url)

    # If we've never seen a post before, initialize to 24 hours ago
    if last_seen_timestamp is None:
        last_seen_timestamp = datetime.utcnow() - timedelta(hours=24)
    
    # Time limit for posts, 24 hours ago from now
    time_limit = datetime.utcnow() - timedelta(hours=24)
    
    for entry in feed.entries:
        # Convert the entry's published date to a datetime object
        entry_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
        
        if entry_date > last_seen_timestamp and entry_date > time_limit:
            tweet_text = f"{entry.title} {entry.link}"
            # Translate the tweet to Chinese
            # chinese_text = translate_to_chinese(tweet_text)

            post_to_twitter(tweet_text)
        else:
            # We've hit an older entry, so we break out of the loop
            break

    # Update the last seen timestamp to the timestamp of the latest entry
    if feed.entries:
        last_seen_timestamp = datetime.strptime(feed.entries[0].published, "%a, %d %b %Y %H:%M:%S %Z")