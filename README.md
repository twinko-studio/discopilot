[![build](https://github.com/twinko-studio/discopilot/actions/workflows/build.yml/badge.svg)](https://github.com/twinko-studio/discopilot/actions/workflows/build.yml)
![PythonVersion](https://img.shields.io/badge/python-3.9%20%7C%203.8%20%7C%203.10%20%7C%203.11-blue)

# discopilot
Using discord bots to automate RSS feed processing, translation, summarization and publishing to other services such as twitter, weibo etc.


## Neo or Nexus: just give discopilot a real name [Not started yet]

The super AGI bot, the brain of the system.

Features:

- Chat bot: talk to me like my real copilot
- AI capabilities: 

Slash command central

Bot commander:

- start, stop and restart other bots, like news bot
- slash command central

Monitor:

- Monitor bot status and send alerts to monitor channel
- Monitor rate limits and send alerts to monitor channel
- Monitor social posting actions and send alerts to monitor channel

```bash
discopilot.py commander
```

## Hedwig: the message and news bot

Features:

- RSS message processing: fetch news from channels, split embedes to single messages and run filters on them
- Filtering: filter news by spam detector
- Translation: translate news to other languages and repost to language specific channels
- Summarization: summarize news by date, time, hours and daily summary and weekly summary repost to summary channel
- Publishing: publish news to other services such as twitter, weibo etc.


```bash
# start hedwig bot on discord
discopilot.py hedwig fly 
# start hedwig bot on discord with dev version
discopilot.py hedwig fly --version dev 
# fetch news from channel 1234567890 in last 24 hours
discopilot.py hedwig fetch --channel 1234567890 --hour 24 
# fetch news from channel 1234567890 between 2023-08-23 and 2023-08-24
discopilot.py hedwig fetch --channel 1234567890 --start 2023-08-23 --end 2023-08-24 
# send a message to channel 1234567890
discopilot.py hedwig hoot "Hello World" --channel 1234567890
# send a message to channel named monitor in config file
discopilot.py hedwig hoot "Hello World" --channel_name monitor
```

### Espresso: the information summarizer AI

```bash
discopilot.py espresso ./news.md > ./news_summary.md
discopilot.py espresso ./news.md --output_dir ./output
discopilot.py espresso ./news.md --filter spam
discopilot.py espresso --summary
```

### C-3PO: the translator AI

```bash
discopilot.py c3po "Hello World" --target_lang zh-cn
discopilot.py c3po "Hello World" --target_lang zh-cn --engine google
# discopilot.py c3po "Hello World" --target zh-cn --engine huggingface
discopilot.py c3po "Hello World" --list-engines
discopilot.py c3po --list-supported_target --source-lang "en"
discopilot.py c3po --list-sources
discopilot.py c3po detect "Hello World"
```

```

### the spam detector AI

```bash
```